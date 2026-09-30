#!/usr/bin/env python3
"""
validate.py — Revisa que tus células de proyecto estén bien armadas.

Uso (desde la carpeta raíz de tu vault):
    python 00_CORE/schemas/validate.py

Revisa todos los archivos 00_CORE/cells/*-context.md y muestra:
  ERRORES → hay que arreglarlos (falta una propiedad o una sección,
            valor no permitido, propiedades ilegibles). Mientras haya
            errores, la IA puede recibir contexto roto.
  AVISOS  → conviene mirarlos ([completar: ...] sin completar,
            hechos sin fuente, célula demasiado larga).

Una célula es una nota de Obsidian con:
  - propiedades arriba (entre las dos líneas ---),
  - secciones abajo: ## Hechos clave, ## Decisiones,
    ## Próximas acciones, ## Preguntas abiertas.
Los bloques entre %% ... %% son ayuda y se ignoran.

Requiere solo Python 3.8 o más nuevo. No hace falta instalar nada más.
"""

import datetime
import re
import sys
import unicodedata
from pathlib import Path

# ------------------------------------------------------------------
# REGLAS DE VALIDACIÓN — si querés cambiar qué se revisa, editá acá
# ------------------------------------------------------------------
PROPIEDADES_OBLIGATORIAS = ["tipo", "proyecto", "descripcion", "contexto", "actualizado"]
SECCIONES_OBLIGATORIAS = ["Hechos clave", "Próximas acciones"]
CONTEXTOS = {"A": "técnico", "B": "narrativo", "C": "persuasivo", "D": "operativo"}
MARCA_PENDIENTE = "[completar"
MAX_TOKENS_CELULA = 3000  # ver davidkimai-resources/evaluation/token_budgeting.md
# ------------------------------------------------------------------

CELLS_DIR = Path(__file__).resolve().parent.parent / "cells"

RE_VINETA = re.compile(r"^[-*+] +(.*)$")                 # viñeta de primer nivel
RE_TAREA = re.compile(r"^[-*+] \[( |x|X)\] +\S")         # - [ ] tarea / - [x] tarea
RE_FUENTE = re.compile(r"\(fuente:\s*([^)]*)\)\s*$", re.IGNORECASE)
RE_FECHA_INICIO = re.compile(r"^(\d{4}-\d{2}-\d{2})\b")
RE_CONTEXTO = re.compile(r"^\s*([ABCD])(?![A-Za-zÀ-ÿ])", re.IGNORECASE)
RE_CLAVE = re.compile(r"^([A-Za-zÀ-ÿ0-9_-][^:]*):(?:\s+(.*)|\s*)$")


# ------------------------------------------------------------------
# Lectura
# ------------------------------------------------------------------
def normalizar(texto):
    """'Próximas  Acciones 📌' → 'proximas acciones' (sin tildes, emojis ni mayúsculas)."""
    sin_tildes = unicodedata.normalize("NFKD", str(texto)).encode("ascii", "ignore").decode()
    return " ".join(sin_tildes.lower().split())


def es_fecha(valor):
    try:
        datetime.datetime.strptime(str(valor).strip(), "%Y-%m-%d")
        return True
    except ValueError:
        return False


def quitar_comillas(valor):
    valor = valor.strip()
    if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
        return valor[1:-1]
    return valor


def leer_propiedades(texto, primera_linea):
    """Lee propiedades simples ('clave: valor' y listas) sin librerías externas.

    Devuelve (propiedades, error). Las células solo usan propiedades simples,
    que son las únicas que Obsidian deja editar desde el recuadro de propiedades.
    """
    props, ultima_clave = {}, None
    for n, linea in enumerate(texto.splitlines(), start=primera_linea):
        if not linea.strip() or linea.lstrip().startswith("#"):
            continue
        if linea[0] in " \t":                      # contenido de una lista
            item = linea.strip()
            if ultima_clave is not None and item.startswith("- "):
                if not isinstance(props[ultima_clave], list):
                    props[ultima_clave] = []
                props[ultima_clave].append(quitar_comillas(item[2:]))
            continue                               # otras sangrías: se ignoran
        m = RE_CLAVE.match(linea)
        if not m:
            return None, (f"La línea {n} de las propiedades no tiene el formato 'nombre: valor' "
                          f"(dice: {linea.strip()[:40]!r}).")
        clave, valor = m.group(1).strip(), (m.group(2) or "").strip()
        if valor.startswith("[") and valor.endswith("]") and not valor.lower().startswith(MARCA_PENDIENTE):
            valor = [quitar_comillas(v) for v in valor[1:-1].split(",") if v.strip()]
        else:
            valor = quitar_comillas(valor)
        props[clave] = valor
        ultima_clave = clave
    return props, None


def separar(texto):
    """Devuelve (texto_de_propiedades, cuerpo) o None si no hay bloque de propiedades."""
    lineas = texto.splitlines()
    if not lineas or lineas[0].strip() != "---":
        return None
    for i in range(1, len(lineas)):
        if lineas[i].strip() == "---":
            return "\n".join(lineas[1:i]), "\n".join(lineas[i + 1:])
    return None


def secciones(cuerpo):
    """{'hechos clave': (titulo_original, [contenido de cada viñeta de primer nivel])}"""
    cuerpo = re.sub(r"%%.*?%%", "", cuerpo, flags=re.DOTALL)  # quitar la ayuda
    resultado, actual = {}, None
    for linea in cuerpo.splitlines():
        if linea.startswith("## "):
            titulo = linea[3:].strip()
            actual = normalizar(titulo)
            resultado[actual] = (titulo, [])
        elif actual and RE_VINETA.match(linea.rstrip()):   # sin sangría: las sub-viñetas no cuentan
            resultado[actual][1].append(linea.rstrip())
    return resultado


def recortar(texto, n=45):
    return texto if len(texto) <= n else texto[: n - 1] + "…"


def contenido(vineta):
    return RE_VINETA.match(vineta).group(1)


# ------------------------------------------------------------------
# Validación de una célula
# ------------------------------------------------------------------
def validar(path):
    errores, avisos = [], []
    texto = Path(path).read_text(encoding="utf-8-sig")  # -sig: tolera la marca BOM de Windows

    partes = separar(texto)
    if partes is None:
        return ["No encuentro las propiedades. La nota tiene que empezar con una línea '---', "
                "las propiedades, y otra línea '---' (copiá el comienzo de TEMPLATE_cell.md)."], []
    props_txt, cuerpo = partes

    props, error = leer_propiedades(props_txt, primera_linea=2)
    if error:
        return [error + " Lo más fácil es editarlas desde el recuadro de propiedades de Obsidian."], []

    # 1. Propiedades obligatorias
    for campo in PROPIEDADES_OBLIGATORIAS:
        if campo not in props:
            errores.append(f"Falta la propiedad '{campo}' (copiala de TEMPLATE_cell.md).")
    if "tipo" in props and normalizar(props["tipo"]) != "celula":
        errores.append("La propiedad 'tipo' tiene que ser: celula")
    for campo in ("proyecto", "descripcion"):
        if campo in props and not str(props[campo]).strip():
            errores.append(f"La propiedad '{campo}' está vacía.")

    # 2. Contexto: alcanza con que empiece con la letra (acepta 'd' o 'D - operativo')
    if "contexto" in props:
        ctx = str(props["contexto"])
        if not RE_CONTEXTO.match(ctx):
            opciones = ", ".join(f"{k} = {v}" for k, v in CONTEXTOS.items())
            errores.append(f"'contexto' vale '{ctx}'. Tiene que ser una letra: {opciones}.")

    # 3. Fecha
    if "actualizado" in props:
        act = props["actualizado"]
        if act in ("", None, []):
            errores.append("'actualizado' está vacío: poné la fecha de hoy (AAAA-MM-DD, por ejemplo 2026-01-31).")
        elif not es_fecha(act):
            errores.append(f"'actualizado' vale '{act}'. Tiene que ser una fecha AAAA-MM-DD, por ejemplo 2026-01-31.")

    # 4. Secciones
    secs = secciones(cuerpo)
    for nombre in SECCIONES_OBLIGATORIAS:
        if normalizar(nombre) not in secs:
            errores.append(f"Falta la sección '## {nombre}' (copiala de TEMPLATE_cell.md).")

    # 5. Hechos clave
    _, hechos = secs.get(normalizar("Hechos clave"), (None, None))
    if hechos is not None:
        if not hechos:
            avisos.append("No hay hechos clave: la IA va a trabajar sin datos comprobados de tu proyecto.")
        for h in hechos:
            m = RE_FUENTE.search(h)
            if not m or not m.group(1).strip():
                avisos.append(f"El hecho '{recortar(contenido(h))}' no tiene fuente: tratalo como no comprobado.")

    # 6. Próximas acciones
    _, acciones = secs.get(normalizar("Próximas acciones"), (None, None))
    if acciones is not None:
        if not acciones:
            avisos.append("No hay próximas acciones: anotá al menos el próximo paso.")
        for a in acciones:
            if not RE_TAREA.match(a):
                errores.append(f"La acción '{recortar(contenido(a))}' tiene que empezar con '- [ ] ' "
                               "(pendiente) o '- [x] ' (hecha).")

    # 7. Decisiones (opcional)
    _, decisiones = secs.get(normalizar("Decisiones"), (None, []))
    for d in decisiones:
        m = RE_FECHA_INICIO.match(contenido(d))
        if not m or not es_fecha(m.group(1)):
            avisos.append(f"La decisión '{recortar(contenido(d))}' no empieza con una fecha AAAA-MM-DD.")

    # 8. Textos de ejemplo sin completar (contexto ya se reporta arriba)
    pendientes = [k for k, v in props.items()
                  if k != "contexto" and MARCA_PENDIENTE in str(v).lower()]
    for _, (titulo, lineas) in secs.items():
        if any(MARCA_PENDIENTE in l.lower() for l in lineas):
            pendientes.append(f"sección {titulo}")
    if pendientes:
        avisos.append(f"Quedan textos [completar: ...] sin reemplazar en: {', '.join(pendientes)}.")

    # 9. Tamaño (estimación: ~4 caracteres por token)
    tokens = len(texto) // 4
    if tokens > MAX_TOKENS_CELULA:
        avisos.append(
            f"La célula ocupa ~{tokens} tokens (máximo recomendado: {MAX_TOKENS_CELULA}). "
            "Resumí o mové lo viejo a _archivo."
        )

    return errores, avisos


# ------------------------------------------------------------------
# Programa
# ------------------------------------------------------------------
def main(cells_dir=CELLS_DIR):
    # La consola de Windows a veces no muestra bien acentos y símbolos.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    cells_dir = Path(cells_dir)
    if not cells_dir.is_dir():
        print(f"No encuentro la carpeta de células: {cells_dir}")
        print("Corré este script desde la raíz de tu vault:  python 00_CORE/schemas/validate.py")
        return 1

    celulas = sorted(cells_dir.glob("*-context.md"))
    if not celulas:
        print("Todavía no hay células para revisar.")
        print("Creá una copiando 00_CORE/cells/TEMPLATE_cell.md como nombre-de-tu-proyecto-context.md")
        return 0

    total_err = total_av = con_error = 0
    print(f"Revisando {len(celulas)} célula(s) en {cells_dir}\n")

    for path in celulas:
        errores, avisos = validar(path)
        marca = "✖" if errores else ("!" if avisos else "✔")
        print(f"{marca} {path.name}")
        for e in errores:
            print(f"    ERROR: {e}")
        for a in avisos:
            print(f"    aviso: {a}")
        total_err += len(errores)
        total_av += len(avisos)
        con_error += bool(errores)

    print("\n" + "=" * 60)
    if total_err:
        print(f"HAY ERRORES en {con_error} célula(s). Arreglalos antes de usarlas con la IA.")
        print("¿No entendés un mensaje? Mirá DOCS/TROUBLESHOOTING.md")
        return 1
    print("TODO BIEN — las células están listas para usar con la IA.")
    if total_av:
        print(f"({total_av} aviso(s): no bloquean, pero conviene revisarlos.)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else CELLS_DIR))
