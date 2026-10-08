#!/usr/bin/env python3
"""Agrega el kit a una bóveda existente sin reemplazar archivos. Python 3.8+."""
import argparse
import importlib.util
import os
from pathlib import Path
import shutil
import stat
import sys

RAIZ = Path(__file__).resolve().parent
CARPETAS = ("00_CORE", "PROJECT_TEMPLATE", "DOCS", ".claude", ".opencode")
ARCHIVOS = ("Panel.md", "Proyectos.base", "AI-INSTRUCTIONS.md", "AGENTS.md", "CLAUDE.md", "crear_proyecto.py", "actualizar_indice.py")
IGNORAR = {"__pycache__", ".pytest_cache", ".DS_Store", "Thumbs.db"}


def comprobar_ruta(path):
    """No seguir enlaces ni junctions, tampoco en los padres del destino."""
    path = Path(os.path.abspath(str(path)))
    for parte in reversed((path,) + tuple(path.parents)):
        try:
            info = parte.lstat()
        except (FileNotFoundError, NotADirectoryError):
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & 0x400:
            raise ValueError("La ruta contiene un enlace o junction: {}".format(parte))
    return path


def archivos_kit(origen):
    for nombre in CARPETAS + ARCHIVOS:
        inicio = comprobar_ruta(origen / nombre)
        if not inicio.exists():
            raise ValueError("Kit incompleto: falta {}".format(nombre))
        if nombre in ARCHIVOS:
            if not inicio.is_file():
                raise ValueError("Se esperaba un archivo: {}".format(nombre))
            yield inicio
            continue
        if not inicio.is_dir():
            raise ValueError("Se esperaba una carpeta: {}".format(nombre))
        for base, carpetas, archivos in os.walk(str(inicio), followlinks=False):
            carpetas[:] = sorted(c for c in carpetas if c not in IGNORAR)
            for carpeta in carpetas:
                comprobar_ruta(Path(base) / carpeta)
            for archivo in sorted(archivos):
                if archivo not in IGNORAR and not archivo.endswith((".pyc", ".pyo")):
                    yield comprobar_ruta(Path(base) / archivo)


def planificar(destino, origen=RAIZ):
    origen = comprobar_ruta(origen)
    destino = comprobar_ruta(destino)
    if not destino.is_dir():
        raise ValueError("Elegí una carpeta de bóveda que ya exista: {}".format(destino))
    if destino == origen or origen in destino.parents or destino in origen.parents:
        raise ValueError("La bóveda y el kit deben estar en carpetas separadas, sin contenerse.")
    nuevos, iguales, conflictos = [], [], []
    for fuente in archivos_kit(origen):
        relativa = fuente.relative_to(origen)
        objetivo = comprobar_ruta(destino / relativa)
        padres = [p for p in objetivo.parents if p != destino and destino in p.parents]
        if any(p.exists() and not p.is_dir() for p in padres):
            conflictos.append(relativa.as_posix())
        elif objetivo.exists():
            if objetivo.is_file() and objetivo.read_bytes() == fuente.read_bytes():
                iguales.append(relativa.as_posix())
            else:
                conflictos.append(relativa.as_posix())
        else:
            nuevos.append((fuente, objetivo))
    return destino, nuevos, iguales, conflictos


def copiar_nuevos(nuevos):
    """La apertura exclusiva también evita pisar un archivo creado tras el plan."""
    for fuente, objetivo in nuevos:
        comprobar_ruta(objetivo)
        objetivo.parent.mkdir(parents=True, exist_ok=True)
        comprobar_ruta(objetivo)
        creado = None
        try:
            with fuente.open("rb") as entrada, objetivo.open("xb") as salida:
                creado = os.fstat(salida.fileno())
                shutil.copyfileobj(entrada, salida)
        except BaseException:
            # Solo retirar nuestro archivo incompleto. Si otro proceso cambió
            # la ruta, conservarla. Nunca borrar un archivo que ya existía.
            if creado is not None:
                try:
                    comprobar_ruta(objetivo)
                    if os.path.samestat(creado, objetivo.lstat()):
                        objetivo.unlink()
                except (OSError, ValueError):
                    print("No se pudo retirar el archivo incompleto: {}. Revisalo antes de reintentar."
                          .format(objetivo), file=sys.stderr)
            raise
        print("Agregado: {}".format(objetivo))


def revisar_celulas(destino, origen=RAIZ):
    # Ejecutar el validador del kit, nunca un script preexistente del destino.
    spec = importlib.util.spec_from_file_location("validador_kit", origen / "00_CORE/schemas/validate.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo.main(destino / "00_CORE/cells")


def indexador(origen=RAIZ):
    spec = importlib.util.spec_from_file_location("indice_kit", comprobar_ruta(origen / "actualizar_indice.py"))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destino", nargs="?", help="Carpeta de una bóveda existente")
    parser.add_argument("--dry-run", action="store_true", help="Mostrar el plan sin copiar")
    parser.add_argument("--yes", action="store_true", help="Aceptar la copia de archivos nuevos")
    args = parser.parse_args(argv)
    try:
        if not args.destino:
            if not sys.stdin.isatty():
                parser.error("indicá la ruta de la bóveda")
            args.destino = input("Ruta de tu bóveda: ").strip().strip('"')
            if not args.destino:
                raise ValueError("La ruta está vacía.")
        destino, nuevos, iguales, conflictos = planificar(Path(args.destino).expanduser())
        print("Destino: {}\nNuevos: {} | Ya iguales: {} | Conflictos: {}".format(
            destino, len(nuevos), len(iguales), len(conflictos)))
        print("La configuración .obsidian y las notas existentes se conservan.")
        if conflictos:
            print("No se copió nada. Revisá estos conflictos antes de instalar:")
            for ruta in conflictos:
                print("  " + ruta)
            return 2
        indice = indexador()
        indice.planificar(destino)  # Conservar un índice previo sin bloque compatible.
        if args.dry_run:
            for _, objetivo in nuevos:
                print("Agregar: {}".format(objetivo.relative_to(destino)))
            print("Generar o actualizar INDICE.md con el catálogo real del destino.")
            return 0
        if nuevos and not args.yes:
            if not sys.stdin.isatty():
                print("Usá --yes para aceptar la copia, o --dry-run para revisar el plan.")
                return 2
            if input("¿Agregar estos archivos? [s/N]: ").strip().lower() not in {"s", "si", "sí"}:
                print("Cancelado. No se copió nada.")
                return 0
        copiar_nuevos(nuevos)
        estado_indice = indice.actualizar(destino)
        print("Índice principal: {}".format(estado_indice['estado']))
        print("\nCopia completa. Revisando las células de la bóveda...")
        codigo = revisar_celulas(destino)
        print("Abrí Panel.md. Para activar Plantillas y Bases en una bóveda existente, seguí DOCS/obsidian.md.")
        if codigo:
            print("Los archivos se agregaron, pero hay células que necesitan revisión.")
        return codigo
    except EOFError:
        print("Entrada cerrada. No se aceptó la instalación.", file=sys.stderr)
        return 2
    except (OSError, ValueError) as error:
        print("No se completó la instalación: {}".format(error), file=sys.stderr)
        print("Si hubo archivos agregados, aparecen arriba. Un reintento conserva los existentes.", file=sys.stderr)
        return 1


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    codigo = main()
    if os.name == "nt" and len(sys.argv) == 1 and sys.stdin.isatty():
        input("Enter para cerrar...")
    sys.exit(codigo)
