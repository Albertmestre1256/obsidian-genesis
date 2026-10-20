#!/usr/bin/env python3
"""Índices de líneas para notas editables. Python estándar 3.8+."""
import argparse
import errno
from contextlib import contextmanager
import os
from pathlib import Path
import re
import stat
import sys
import tempfile

HEADER = '> [!info]- Índice de esta nota (líneas)'
HEADERS = (HEADER, '> [!info] Índice de esta nota (líneas)')
ENTRY = re.compile(r'^> - Líneas (\d+)–(\d+): (.+)$')
# Primera línea de atribución del README y sus traducciones.
ATRIBUCIONES = ('> **Crédito principal', '> **Main credit', '> **Besonderer Dank', '> **主要致谢')
IGNORAR = {'.git', '.obsidian', '.obsidian-mcp', '.claude', '.agents', '.opencode', '.github',
           '__pycache__', '.pytest_cache', '.trash', 'node_modules', '.venv', 'venv', '_archivo'}

# Raíces ya validadas: sus carpetas contenedoras no se revisan (p. ej. /home enlazado).
_RAICES = set()


def es_enlace(info):
    """Symlink o junction. Archivos en la nube (OneDrive) y deduplicación de Windows no redirigen rutas."""
    if stat.S_ISLNK(info.st_mode):
        return True
    if getattr(info, 'st_file_attributes', 0) & 0x400:
        tag = getattr(info, 'st_reparse_tag', None)
        return tag is None or not ((tag & 0xFFFF0FFF) == 0x9000001A or tag == 0x80000013)
    return False


def ruta_real(path):
    path = Path(os.path.abspath(str(path)))
    for part in (path,) + tuple(path.parents):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if es_enlace(info):
            raise ValueError('No seguir enlaces ni junctions: ' + str(part))
        if os.path.normcase(str(part)) in _RAICES:
            break
    return path


def raiz_confiable(path):
    """Validar la raíz de trabajo sin exigir lo mismo a las carpetas que la contienen."""
    path = Path(os.path.abspath(str(path)))
    try:
        if es_enlace(path.lstat()):
            raise ValueError('La raíz es un enlace o junction: ' + str(path))
    except FileNotFoundError:
        pass
    _RAICES.add(os.path.normcase(str(path)))
    return path


@contextmanager
def bloqueo(path):
    """Coordinar escritores del kit; los clientes MCP usan sus propios etags."""
    lock = ruta_real(path.with_name('.' + path.name + '.kit-lock'))
    try:
        stream = lock.open('xb')
    except FileExistsError:
        raise ValueError('Otra escritura está en curso; releé y reintentá después. No retires el bloqueo: ' + str(lock))
    identity = os.fstat(stream.fileno())
    try:
        with stream:
            yield
    finally:
        try:
            if os.path.samestat(identity, ruta_real(lock).lstat()):
                lock.unlink()
        except FileNotFoundError:
            pass


def modo_final(path):
    """Permisos de la nota: los actuales o los que daría la máscara del sistema a una nota nueva."""
    try:
        return stat.S_IMODE(path.stat().st_mode)
    except FileNotFoundError:
        mascara = os.umask(0)
        os.umask(mascara)
        return 0o666 & ~mascara


def guardar(path, before, after):
    path = ruta_real(path)
    if before == after:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    # El bloqueo abarca la comprobación, el reemplazo y la relectura.
    with bloqueo(path):
        temporary = None
        try:
            with tempfile.NamedTemporaryFile(prefix='.nota-', suffix='.tmp', dir=str(path.parent), delete=False) as stream:
                temporary = Path(stream.name)
                stream.write(after)
            # NamedTemporaryFile crea con 0600; la nota publicada conserva sus permisos.
            os.chmod(str(temporary), modo_final(path))
            if before is None:
                # Publicar completo sin reemplazar un archivo aparecido mientras se escribía.
                try:
                    os.link(str(temporary), str(ruta_real(path)))
                except OSError as error:
                    if error.errno not in {errno.ENOTSUP, errno.ENOSYS, errno.EPERM, errno.EINVAL} and getattr(error, 'winerror', None) not in {1, 50}:
                        raise
                    # Sin enlaces duros, crear exclusivamente y conservar cualquier
                    # salida parcial para releerla, sin retirar posibles ediciones ajenas.
                    with ruta_real(path).open('xb') as stream:
                        stream.write(after)
            else:
                if ruta_real(path).read_bytes() != before:
                    raise ValueError('La nota cambió; releé antes de guardar: ' + str(path))
                os.replace(str(temporary), str(path))
                temporary = None
        finally:
            if temporary is not None:
                temporary.unlink()
        if path.read_bytes() != after:
            raise OSError('No coincide el contenido guardado: ' + str(path))
    return True


def partir(text):
    # Solo \n separa líneas; splitlines también corta en \x0c, U+2028 y otros que Obsidian no cuenta.
    return re.findall(r'[^\n]*\n|[^\n]+\Z', text)


def separar(text, reubicar=False):
    lines = partir(text)
    clean = [line.rstrip('\r\n') for line in lines]
    first = 0
    if clean and clean[0] == '---':
        first = next((i + 1 for i in range(1, len(clean)) if clean[i] == '---'), 0)
        if not first:
            raise ValueError('Propiedades sin cierre; no se modifica la nota.')
    elif clean and clean[0].startswith(ATRIBUCIONES):
        first = 1  # La atribución del README permanece siempre primera.
    start = first
    while start < len(clean) and not clean[start].strip():
        start += 1
    count = sum(line in HEADERS for line in clean)
    if count:
        if reubicar and count == 1:
            start = next(i for i, line in enumerate(clean) if line in HEADERS)
        if count != 1 or start < first or start >= len(clean) or clean[start] not in HEADERS:
            raise ValueError('Índice duplicado o fuera del comienzo; revisar sin reemplazarlo.')
        end = start + 1
        while end < len(clean) and clean[end].startswith('>'):
            if not ENTRY.fullmatch(clean[end]):
                raise ValueError('Índice de líneas incompatible; se conserva.')
            end += 1
        lines = lines[:start] + lines[end:]
    head, body = lines[:first], lines[first:]
    while body and not body[0].strip():
        body.pop(0)
    return head, body


def sin_indice(text, reubicar=False):
    head, body = separar(text, reubicar)
    return ''.join(head + body)


def render(text, reubicar=False):
    head, body = separar(text, reubicar)
    newline = '\r\n' if '\r\n' in text else '\n'
    if head and not head[-1].endswith(('\n', '\r')):
        head[-1] += newline
    sections, fence = [], None
    for i, line in enumerate(body):
        raw = line.rstrip('\r\n')
        match = re.match(r'^\s{0,3}(`{3,}|~{3,})(.*)$', raw)
        if fence:
            if match and match[1][0] == fence[0] and len(match[1]) >= fence[1] and not match[2].strip():
                fence = None
            continue
        if match:
            fence = (match[1][0], len(match[1]))
            continue
        heading = re.match(r'^#{1,3}\s+(.+?)\s*#*\s*$', raw)
        if heading:
            sections.append((i, heading[1].strip()[:100]))
    if not sections or sections[0][0] > 0:
        sections.insert(0, (0, 'Contenido' if not sections else 'Introducción'))
    sections = [(i, title) for i, title in sections if i < len(body)]
    block_len = 2 + bool(head) + len(sections)
    body_start = len(head) + block_len + 2
    block = [HEADER]
    if head:
        block.append('> - Líneas 1–{}: {}'.format(len(head), 'Propiedades' if head[0].strip() == '---' else 'Atribución'))
    block.append('> - Líneas {}–{}: Este índice'.format(len(head) + 1, len(head) + block_len))
    for k, (start, title) in enumerate(sections):
        end = sections[k + 1][0] - 1 if k + 1 < len(sections) else len(body) - 1
        block.append('> - Líneas {}–{}: {}'.format(body_start + start, body_start + end, title))
    return ''.join(head) + newline.join(block) + newline * 2 + ''.join(body)


def contenido(raw):
    bom = b'\xef\xbb\xbf' if raw.startswith(b'\xef\xbb\xbf') else b''
    return bom + render(raw.decode('utf-8-sig')).encode('utf-8')


def protegida(path, raiz=None):
    # Conservar originales, copias históricas y formatos de integraciones dentro de la bóveda;
    # las carpetas que contienen a la bóveda no cuentan.
    path = Path(os.path.abspath(str(path)))
    if raiz is not None:
        try:
            path = path.relative_to(os.path.abspath(str(raiz)))
        except ValueError:
            pass
    parts = tuple(p.casefold() for p in path.parts)
    return (any(p in IGNORAR or p == '01_fuentes' for p in parts)
            or any(parts[i:i+3] == ('00_core', 'logs', 'historial') for i in range(len(parts)-2)))


def archivos(root):
    root = raiz_confiable(root)
    historial = tuple(p.casefold() for p in root.parts[-3:]) == ('00_core', 'logs', 'historial')
    if not root.is_dir() or protegida(root, root.parent) or historial:
        raise ValueError('Indicá una carpeta de bóveda existente y editable: ' + str(root))
    for base, dirs, names in os.walk(str(root), followlinks=False):
        dirs[:] = sorted(d for d in dirs if not protegida(Path(base) / d, root))
        for d in dirs:
            ruta_real(Path(base) / d)
        for name in sorted(names):
            if name.lower().endswith('.md'):
                yield ruta_real(Path(base) / name)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('modo', choices=['apply', 'check'])
    parser.add_argument('notas', nargs='*')
    parser.add_argument('--vault', help='Revisar notas editables de esta carpeta; excluye originales e integraciones')
    args = parser.parse_args(argv)
    try:
        if bool(args.notas) == bool(args.vault):
            raise ValueError('Indicá notas concretas o --vault, nunca ambos.')
        paths = list(archivos(Path(args.vault))) if args.vault else [ruta_real(Path(p)) for p in args.notas]
        plans = []
        raiz = Path(args.vault) if args.vault else Path.cwd()
        for path in paths:
            if protegida(path, raiz):
                raise ValueError('Original, histórico o integración protegido; describirlo en el mapa del nodo: ' + str(path))
            raw = path.read_bytes()
            plans.append((path, raw, contenido(raw)))
        # Preflight completo: una nota incompatible no deja otras a medio actualizar.
        for path, before, after in plans:
            if before != after:
                print(('Actualizar: ' if args.modo == 'apply' else 'Pendiente: ') + str(path))
                if args.modo == 'apply':
                    guardar(path, before, after)
        return 1 if args.modo == 'check' and any(a != b for _, a, b in plans) else 0
    except (OSError, ValueError, UnicodeError) as error:
        print(str(error), file=sys.stderr)
        return 2


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    sys.exit(main())
