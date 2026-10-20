#!/usr/bin/env python3
"""Copia las cinco skills portables en una bóveda Genesis. Python estándar 3.8+."""
import argparse
import os
from pathlib import Path
import stat
import sys

sys.dont_write_bytecode = True
RAIZ = Path(__file__).resolve().parent
SKILLS = ('inicio', 'volcar', 'vault-reorganizer', 'vault-coherence-auditor',
          'vault-token-optimizer')
DESTINOS = {'claude': '.claude/skills', 'codex': '.agents/skills',
            'opencode': '.opencode/skills'}


def ruta_segura(path):
    """Conservar la ruta literal; rechazar symlinks y junctions en sus ancestros."""
    path = Path(os.path.abspath(str(path)))
    for part in (path,) + tuple(path.parents):
        try:
            info = part.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('No se siguen enlaces ni junctions: ' + str(part))
    return path


def archivos_skill(folder):
    folder = ruta_segura(folder)
    if not folder.is_dir() or not ruta_segura(folder / 'SKILL.md').is_file():
        raise ValueError('Falta la skill fuente: ' + str(folder))
    for base, dirs, names in os.walk(str(folder), followlinks=False):
        for name in sorted(dirs):
            ruta_segura(Path(base) / name)
        dirs.sort()
        for name in sorted(names):
            path = ruta_segura(Path(base) / name)
            if not stat.S_ISREG(path.stat().st_mode):
                raise ValueError('Se esperaba un archivo regular: ' + str(path))
            yield path.relative_to(folder), path.read_bytes()


def planificar(destino, asistente, origen=RAIZ):
    destino = ruta_segura(destino)
    if not destino.is_dir():
        raise ValueError('El destino debe ser una bóveda Genesis ya copiada: ' + str(destino))
    for marca in ('INDICE.md', '00_CORE/atoms/00_vault-rules.md'):
        if not ruta_segura(destino / marca).is_file():
            raise ValueError('No se reconoce una bóveda Genesis; falta ' + marca)
    planes = []
    for skill in SKILLS:
        for relativa, contenido in archivos_skill(Path(origen) / 'skills' / skill):
            path = ruta_segura(destino / DESTINOS[asistente] / skill / relativa)
            # Preflight de todos los padres antes de cualquier escritura.
            for parent in path.parents:
                if parent == destino:
                    break
                if parent.exists() and not parent.is_dir():
                    raise ValueError('Una carpeta está ocupada por un archivo: ' + str(parent))
            if path.exists():
                if not path.is_file() or path.read_bytes() != contenido:
                    raise ValueError('Se conserva una skill diferente; no se sobrescribe: ' + str(path))
                accion = 'igual'
            else:
                accion = 'crear'
            planes.append((path, contenido, accion))
    return planes


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('destino', help='Raíz actual de la bóveda Genesis')
    parser.add_argument('--asistente', required=True, choices=sorted(DESTINOS))
    modo = parser.add_mutually_exclusive_group()
    modo.add_argument('--dry-run', action='store_true', help='Mostrar sin escribir (predeterminado)')
    modo.add_argument('--yes', action='store_true', help='Crear las skills nuevas del plan')
    args = parser.parse_args(argv)
    creados = []
    try:
        planes = planificar(args.destino, args.asistente)
        for path, _, accion in planes:
            print('{}: {}'.format(accion, path))
        if not args.yes:
            print('Consulta: no se escribió ningún archivo.')
            return 0
        # Cada archivo usa creación exclusiva: un conflicto concurrente no se reemplaza.
        for path, contenido, accion in planes:
            ruta_segura(path)
            if accion == 'igual':
                if path.read_bytes() != contenido:
                    raise ValueError('La skill cambió durante la operación: ' + str(path))
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            ruta_segura(path)
            with path.open('xb') as stream:
                creados.append(path)
                stream.write(contenido)
            if path.read_bytes() != contenido:
                raise ValueError('Copia no verificada: ' + str(path))
        print('Archivos nuevos verificados: {}. Completar mapas y registro según DOCS/mantenimiento.md.'.format(len(creados)))
        return 0
    except (OSError, ValueError) as error:
        print('Impedido: ' + str(error), file=sys.stderr)
        if creados:
            print('Operación parcial; revisar y registrar estos archivos:', file=sys.stderr)
            for path in creados:
                print(str(path), file=sys.stderr)
        return 2


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    sys.exit(main())
