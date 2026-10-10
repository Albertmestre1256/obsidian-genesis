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

HEADER = '> [!info] Índice de esta nota (líneas)'
ENTRY = re.compile(r'^> - Líneas (\d+)–(\d+): (.+)$')
IGNORAR = {'.git', '.obsidian', '.obsidian-mcp', '.claude', '.opencode', '.github',
           '__pycache__', '.pytest_cache', '.trash', 'node_modules', '.venv', 'venv', '_archivo'}


def ruta_real(path):
    path = Path(os.path.abspath(str(path)))
    for part in (path,) + tuple(path.parents):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('No seguir enlaces ni junctions: ' + str(part))
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


def separar(text, reubicar=False):
    lines = text.splitlines(keepends=True)
    clean = [line.rstrip('\r\n') for line in lines]
    first = 0
    if clean and clean[0] == '---':
        first = next((i + 1 for i in range(1, len(clean)) if clean[i] == '---'), 0)
        if not first:
            raise ValueError('Propiedades sin cierre; no se modifica la nota.')
    elif clean and clean[0].startswith('> **Crédito principal'):
        first = 1  # La atribución del README permanece siempre primera.
    start = first
    while start < len(clean) and not clean[start].strip():
        start += 1
    count = sum(line == HEADER for line in clean)
    if count:
        if reubicar and count == 1:
            start = clean.index(HEADER)
        if count != 1 or start < first or start >= len(clean) or clean[start] != HEADER:
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


def protegida(path):
    # Conservar originales, copias históricas y formatos de integraciones.
    parts = tuple(p.casefold() for p in path.parts)
    return (any(p in IGNORAR or p == '01_fuentes' for p in parts)
            or any(parts[i:i+3] == ('00_core', 'logs', 'historial') for i in range(len(parts)-2)))


def archivos(root):
    root = ruta_real(root)
    if not root.is_dir() or protegida(root):
        raise ValueError('Indicá una carpeta de bóveda existente y editable: ' + str(root))
    for base, dirs, names in os.walk(str(root), followlinks=False):
        dirs[:] = sorted(d for d in dirs if not protegida(Path(base) / d))
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
        for path in paths:
            if protegida(path):
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
