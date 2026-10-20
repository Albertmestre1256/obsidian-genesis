#!/usr/bin/env python3
"""Agrega el kit; --vista-simple permite ajustar la vista con respaldo. Python 3.8+."""
import argparse
import importlib.util
import json
import os
from datetime import datetime
from pathlib import Path
import shutil
import stat
import sys
sys.dont_write_bytecode = True  # no dejar __pycache__ dentro de la bóveda

RAIZ = Path(__file__).resolve().parent
CARPETAS = ("00_CORE", "PROJECT_TEMPLATE", "DOCS", ".claude", ".opencode")
ARCHIVOS = ("Panel.md", "Proyectos.base", "LEER_PRIMERO.md", "AI-INSTRUCTIONS.md", "AGENTS.md", "CLAUDE.md", "crear_proyecto.py", "actualizar_indice.py")
IGNORAR = {"__pycache__", ".pytest_cache", ".DS_Store", "Thumbs.db", "node_modules"}
# OpenCode instala aquí sus dependencias al abrir el kit; no forman parte de él.
GENERADOS_OPENCODE = {"package.json", "package-lock.json", "bun.lock", ".gitignore"}
# Describen el repositorio completo, incluidos README y tests que no se instalan.
GUIAS_REPOSITORIO = {"README.md", "README.en.md", "README.de.md", "README.zh.md"}

# Vista simple opcional para bóvedas existentes: reusa CSS y filtro del kit.
VISTA_SIMPLE_CSS = ".obsidian/snippets/genesis-vista-simple.css"
VISTA_SIMPLE_APARIENCIA = ".obsidian/appearance.json"
VISTA_SIMPLE_GRAFO = ".obsidian/graph.json"
SNIPPET_NOMBRE = "genesis-vista-simple"


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
            carpetas[:] = sorted(c for c in carpetas if c not in IGNORAR
                                 and (Path(base).relative_to(origen).as_posix(), c) != ('.claude', 'worktrees'))
            for carpeta in carpetas:
                comprobar_ruta(Path(base) / carpeta)
            omitidos = GENERADOS_OPENCODE if Path(base) == origen / ".opencode" else ()
            if Path(base) == origen / "DOCS":
                omitidos = GUIAS_REPOSITORIO
            for archivo in sorted(archivos):
                if archivo not in IGNORAR and archivo not in omitidos and not archivo.endswith((".pyc", ".pyo")):
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
        if relativa.as_posix() == 'LEER_PRIMERO.md' and comprobar_ruta(destino / '00 - Leer primero.md').is_file():
            # La entrada propia permanece como referencia de los nodos; no crear
            # otra puerta de entrada que pueda contradecir sus reglas.
            continue
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


def _leer_json(ruta):
    """Distinguir un archivo ausente de un JSON incompatible."""
    ruta = comprobar_ruta(ruta)
    raw = ruta.read_bytes() if ruta.exists() else None
    actual = json.loads(raw.decode("utf-8-sig")) if raw is not None else {}
    if not isinstance(actual, dict):
        raise ValueError("Se esperaba un objeto JSON: {}".format(ruta))
    return actual, raw


def planificar_vista_simple(destino, origen=RAIZ):
    """Validar todo sin escribir; separar altas CSS de cambios de ajustes."""
    nuevos, iguales, conflictos, cambios, avisos = [], [], [], [], []
    for relativa in (VISTA_SIMPLE_CSS, VISTA_SIMPLE_APARIENCIA, VISTA_SIMPLE_GRAFO):
        try:
            path = comprobar_ruta(destino / relativa)
            if any(p.exists() and not p.is_dir() for p in path.parents):
                raise ValueError("Un padre no es una carpeta: {}".format(path))
            if relativa == VISTA_SIMPLE_CSS:
                fuente = comprobar_ruta(origen / relativa)
                contenido_css = fuente.read_bytes()
                if not path.exists():
                    nuevos.append((fuente, path))
                elif path.read_bytes() == contenido_css:
                    iguales.append(relativa)
                else:
                    raise ValueError("CSS con mismo nombre y contenido distinto")
                continue
            actual, antes = _leer_json(path)
            if relativa == VISTA_SIMPLE_APARIENCIA:
                snippets = actual.get("enabledCssSnippets", [])
                if not isinstance(snippets, list) or not all(isinstance(s, str) for s in snippets):
                    raise ValueError("enabledCssSnippets debe ser una lista de textos")
                if SNIPPET_NOMBRE not in snippets:
                    actual["enabledCssSnippets"] = snippets + [SNIPPET_NOMBRE]
                else:
                    iguales.append(relativa)
                    continue
            else:
                referencia, _ = _leer_json(origen / relativa)
                filtro = referencia.get("search")
                search = actual.get("search", "")
                if not isinstance(filtro, str) or not filtro:
                    raise ValueError("Falta el filtro search del kit")
                if not isinstance(search, str):
                    raise ValueError("search debe ser un texto")
                if search:
                    iguales.append(relativa)
                    if search != filtro:
                        avisos.append("Filtro Genesis pendiente: se conserva la búsqueda propia del gráfico.")
                    continue
                actual["search"] = filtro
            despues = (json.dumps(actual, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
            cambios.append((path, antes, despues))
        except (OSError, ValueError) as error:
            conflictos.append("{}: {}".format(relativa, error))
    return nuevos, iguales, conflictos, cambios, avisos


def comprobar_cambios(cambios):
    for path, antes, _ in cambios:
        path = comprobar_ruta(path)
        vigente = path.read_bytes() if path.exists() else None
        if vigente != antes:
            raise ValueError("Un ajuste cambió; releé antes de instalar: {}".format(path))


def aplicar_vista_simple(cambios, guardar):
    """Reusar guardado exclusivo/atómico y contraste de bytes del kit."""
    comprobar_cambios(cambios)
    for path, antes, despues in cambios:
        if antes is not None:
            marca = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            for numero in range(1000):
                backup = path.with_name(path.name + ".bak-{}-{}".format(marca, numero))
                try:
                    guardar(backup, None, antes)
                    break
                except FileExistsError:
                    continue
            else:
                raise ValueError("No se pudo crear un respaldo exclusivo: {}".format(path))
            print("Respaldo para restaurar {}: {}".format(path, backup))
        guardar(path, antes, despues)
        print(("Creado (retirar al revertir): " if antes is None else "Actualizado: ") + str(path))


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


def modulo_kit(origen, ruta, nombre):
    """Cargar herramientas del origen comprobado, no scripts del destino."""
    spec = importlib.util.spec_from_file_location(nombre, comprobar_ruta(origen / ruta))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def revisar_celulas(destino, origen=RAIZ):
    return modulo_kit(origen, "00_CORE/schemas/validate.py", "validador_kit").main(destino / "00_CORE/cells")


def indexador(origen=RAIZ):
    return modulo_kit(origen, "actualizar_indice.py", "indice_kit")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destino", nargs="?", help="Carpeta de una bóveda existente")
    parser.add_argument("--dry-run", action="store_true", help="Mostrar el plan sin copiar")
    parser.add_argument("--yes", action="store_true", help="Aceptar la copia de archivos nuevos")
    parser.add_argument("--vista-simple", action="store_true", help="Activar la vista simple opcional (CSS y filtro de grafo) preservando preferencias")
    args = parser.parse_args(argv)
    try:
        if not args.destino:
            if not sys.stdin.isatty():
                parser.error("indicá la ruta de la bóveda")
            args.destino = input("Ruta de tu bóveda: ").strip().strip('"')
            if not args.destino:
                raise ValueError("La ruta está vacía.")
        destino, nuevos, iguales, conflictos = planificar(Path(args.destino).expanduser())
        v_cambios, v_avisos = [], []
        if args.vista_simple:
            v_nuevos, v_iguales, v_conflictos, v_cambios, v_avisos = planificar_vista_simple(destino)
            nuevos.extend(v_nuevos)
            iguales.extend(v_iguales)
            conflictos.extend(v_conflictos)
        print("Destino: {}\nNuevos: {} | Ya iguales: {} | Conflictos: {}".format(
            destino, len(nuevos), len(iguales), len(conflictos)))
        print("Las notas existentes se conservan; solo se ajusta la vista con --vista-simple.")
        for aviso in v_avisos:
            print(aviso)
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
            if args.vista_simple:
                print("Vista simple:")
                for path, antes, _ in v_cambios:
                    print("  {}: {}".format("Crear" if antes is None else "Respaldar y actualizar", path))
            print("Generar o actualizar INDICE.md y los bloques de índices locales del destino.")
            return 0
        if (nuevos or v_cambios) and not args.yes:
            if not sys.stdin.isatty():
                print("Usá --yes para aceptar la copia, o --dry-run para revisar el plan.")
                return 2
            if input("¿Agregar estos archivos? [s/N]: ").strip().lower() not in {"s", "si", "sí"}:
                print("Cancelado. No se copió nada.")
                return 0
        comprobar_cambios(v_cambios)
        copiar_nuevos(nuevos)
        for fuente, objetivo in (v_nuevos if args.vista_simple else []):
            print("Creado (retirar al revertir): {}".format(objetivo))
        aplicar_vista_simple(v_cambios, indice.lineador().guardar)
        estado_indice = indice.actualizar(destino)
        print("Índice principal: {}".format(estado_indice['estado']))
        if estado_indice['indices_manuales']:
            print("Índices locales manuales para revisar, conservados: " + ", ".join(estado_indice['indices_manuales']))
        print("\nCopia completa. Revisando las células de la bóveda...")
        codigo = revisar_celulas(destino)
        print("Abrí Panel.md. Activá Plantillas y Bases en Ajustes → Plugins principales (Bases requiere Obsidian 1.9.10 o posterior).")
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
