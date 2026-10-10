#!/usr/bin/env python3
"""Revisa propiedades y secciones de las fichas, también las renombradas.

Desde la raíz:
    python 00_CORE/schemas/validate.py

Errores: formato que corregir. Avisos: datos que revisar, sin bloquear.
Ignora ayuda entre %%...%%. Python estándar 3.8+; ver DOCS/TROUBLESHOOTING.md.
"""

import datetime
import json
import re
import sys
import unicodedata
from pathlib import Path

# Reglas de validación
PROPIEDADES_OBLIGATORIAS = ["tipo", "proyecto", "descripcion", "contexto", "actualizado"]
SECCIONES_OBLIGATORIAS = ["Hechos clave", "Próximas acciones"]
CONTEXTOS = {"A": "técnico", "B": "narrativo", "C": "persuasivo", "D": "operativo"}
MARCA_PENDIENTE = "[completar"
MAX_TOKENS_CELULA = 3000  # ver davidkimai-resources/evaluation/token_budgeting.md

CELLS_DIR = Path(__file__).resolve().parent.parent / "cells"

RE_VINETA = re.compile(r"^[-*+] +(.*)$")                 # viñeta de primer nivel
RE_TAREA = re.compile(r"^[-*+] \[( |x|X)\] +\S")         # - [ ] tarea / - [x] tarea
RE_FUENTE = re.compile(r"\(fuente:\s*([^)]*)\)\s*$", re.IGNORECASE)
RE_FECHA_INICIO = re.compile(r"^(\d{4}-\d{2}-\d{2})\b")
RE_CONTEXTO = re.compile(r"^\s*([ABCD])(?![A-Za-zÀ-ÿ])", re.IGNORECASE)
RE_CLAVE = re.compile(r"^([A-Za-zÀ-ÿ0-9_-][^:]*):(?:\s+(.*)|\s*)$")


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


def leer_escalar(valor):
    """Lee un valor de una línea; rechaza YAML que no sabe interpretar."""
    valor = valor.strip()
    if valor.startswith(('"', "'")):
        patron = r'("(?:[^"\\]|\\.)*"|\'(?:[^\']|\'\')*\')(?:\s+#.*)?\s*'
        m = re.fullmatch(patron, valor)
        if not m:
            raise ValueError("Hay comillas sin cerrar o texto después de las comillas.")
        texto = m.group(1)
        if texto.startswith("'"):
            return texto[1:-1].replace("''", "'")
        try:
            return json.loads(texto)
        except ValueError:
            raise ValueError("El texto entre comillas dobles tiene un escape no admitido; "
                             "usá comillas simples o editá la propiedad en Obsidian.")
    valor = re.split(r"(?:^|\s+)#", valor, maxsplit=1)[0].rstrip()
    if not valor or valor.lower() in {"null", "~"}:
        return None
    if valor[0] in "[]{}!&*|>@`" or re.match(r"[-?:](?:\s|$)", valor):
        raise ValueError("Usá texto en una línea entre comillas o una lista simple; "
                         "el revisor no admite mapas, bloques multilínea ni referencias YAML.")
    if re.search(r":(?:\s|$)", valor):
        raise ValueError("El texto que contiene dos puntos seguidos de un espacio "
                         "debe estar entre comillas, por ejemplo: 'Meta: automatizar'.")
    if valor.lower() in {"true", "false"}:
        return valor.lower() == "true"
    if re.fullmatch(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][-+]?\d+)?", valor):
        return float(valor)
    return valor


def leer_valor(valor):
    """Admite escalares y listas de una línea, incluidas comas entre comillas."""
    valor = valor.strip()
    if not valor.startswith("["):
        return leer_escalar(valor)
    items, inicio, comilla, i = [], 1, None, 1
    while i < len(valor):
        caracter = valor[i]
        if comilla:
            if comilla == '"' and caracter == "\\":
                i += 2
                continue
            if caracter == comilla:
                if comilla == "'" and valor[i:i + 2] == "''":
                    i += 2
                    continue
                comilla = None
        elif caracter in "\"'" and not valor[inicio:i].strip():
            comilla = caracter
        elif caracter in "[{":
            raise ValueError("El revisor admite listas simples, sin listas ni mapas dentro.")
        elif caracter in ",]":
            item = valor[inicio:i].strip()
            if item:
                items.append(leer_escalar(item))
            elif caracter == ",":
                raise ValueError("Hay un elemento vacío en la lista.")
            if caracter == "]":
                resto = valor[i + 1:]
                if resto.strip() and not re.match(r"\s+#", resto):
                    raise ValueError("Hay texto después del cierre de la lista.")
                return items
            inicio = i + 1
        i += 1
    raise ValueError("La lista tiene corchetes o comillas sin cerrar.")


def leer_propiedades(texto, primera_linea):
    """Lee propiedades simples ('clave: valor' y listas) sin librerías externas.

    Devuelve (propiedades, error). No es un lector de todo YAML: las estructuras
    no admitidas se informan, nunca se ignoran ni se dan por válidas.
    """
    props, ultima_clave = {}, None
    for n, linea in enumerate(texto.splitlines(), start=primera_linea):
        if not linea.strip() or linea.lstrip().startswith("#"):
            continue
        item = linea.strip()
        if item.startswith("- "):
            if ultima_clave is None or props[ultima_clave] is not None and not isinstance(props[ultima_clave], list):
                return None, f"La línea {n} agrega una lista a una propiedad que ya tiene un valor."
            if props[ultima_clave] is None:
                props[ultima_clave] = []
            try:
                props[ultima_clave].append(leer_escalar(item[2:]))
            except ValueError as error:
                return None, f"La línea {n} de las propiedades: {error}"
            continue
        if linea[0] in " \t":
            return None, (f"La línea {n} usa sangría no admitida. "
                          "Usá propiedades sin sangría y texto en una línea entre comillas.")
        m = RE_CLAVE.match(linea)
        if not m:
            return None, (f"La línea {n} de las propiedades no tiene el formato 'nombre: valor' "
                          f"(dice: {linea.strip()[:40]!r}).")
        clave, valor = m.group(1).strip(), (m.group(2) or "").strip()
        if clave in props:
            return None, f"La propiedad '{clave}' está repetida en la línea {n}; dejá una sola."
        try:
            props[clave] = leer_valor(valor)
        except ValueError as error:
            return None, f"La línea {n} de la propiedad '{clave}': {error}"
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


def leer_nota(path):
    """Un archivo ilegible se informa sin convertirlo ni abortar el resto."""
    try:
        return Path(path).read_text(encoding='utf-8-sig'), None
    except UnicodeError:
        return None, ('No puedo leer este archivo como UTF-8. Conservá el original y '
                      'verificá su codificación antes de volver a revisarlo.')
    except OSError:
        return None, ('No puedo leer este archivo. Comprobá el permiso de lectura y '
                      'que siga disponible antes de volver a revisarlo.')


def buscar_celulas(cells_dir):
    """Reconoce fichas por propiedades; conserva la detección de nombres convencionales rotos."""
    celulas = []
    for path in sorted(Path(cells_dir).iterdir()):
        if path.suffix.lower() != '.md' or path.name.lower() == 'template_cell.md' or not path.is_file():
            continue
        if path.name.lower().endswith('-context.md'):
            celulas.append(path)
            continue
        text, error = leer_nota(path)
        if error:
            celulas.append(path)  # No ocultar posibles fichas que no pudimos clasificar.
            continue
        partes = separar(text)
        if partes is None:
            continue
        for linea in partes[0].splitlines():
            if re.match(r'^proyecto\s*:', linea):
                celulas.append(path)
                break
            if re.match(r'^tipo\s*:', linea):
                props, error = leer_propiedades(linea, primera_linea=2)
                if not error and normalizar(props.get('tipo', '')) == 'celula':
                    celulas.append(path)
                    break
    return celulas


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


def validar(path):
    errores, avisos = [], []
    texto, error = leer_nota(path)
    if error:
        return [error], []

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
        if campo in props:
            if props[campo] is None or props[campo] == "":
                errores.append(f"La propiedad '{campo}' está vacía.")
            elif not isinstance(props[campo], str) or not props[campo].strip():
                errores.append(f"La propiedad '{campo}' tiene que ser texto no vacío, "
                               "no una lista, número o casilla. Usá comillas si es necesario.")

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
    _, hechos = secs.get("hechos clave", (None, None))
    if hechos is not None:
        if not hechos:
            avisos.append("No hay hechos clave: la IA va a trabajar sin datos comprobados de tu proyecto.")
        for h in hechos:
            m = RE_FUENTE.search(h)
            if not m or not m.group(1).strip():
                avisos.append(f"El hecho '{recortar(contenido(h))}' no tiene fuente: tratalo como no comprobado.")

    # 6. Próximas acciones
    _, acciones = secs.get("proximas acciones", (None, None))
    if acciones is not None:
        if not acciones:
            avisos.append("No hay próximas acciones: podés elegir el primer paso después. Este aviso no bloquea la configuración.")
        for a in acciones:
            if not RE_TAREA.match(a):
                errores.append(f"La acción '{recortar(contenido(a))}' tiene que empezar con '- [ ] ' "
                               "(pendiente) o '- [x] ' (hecha).")

    # 7. Decisiones (opcional)
    _, decisiones = secs.get("decisiones", (None, []))
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

    try:
        celulas = buscar_celulas(cells_dir)
    except OSError:
        print('No puedo revisar esta carpeta. Comprobá que esté disponible y tengas permiso de lectura.')
        return 1
    if not celulas:
        print("Todavía no hay células para revisar.")
        print("Creá una copiando 00_CORE/cells/TEMPLATE_cell.md como nombre-de-tu-proyecto-context.md")
        return 0

    total_av = con_error = 0
    print(f"Revisando {len(celulas)} célula(s) en {cells_dir}\n")

    for path in celulas:
        errores, avisos = validar(path)
        marca = "✖" if errores else ("!" if avisos else "✔")
        print(f"{marca} {path.name}")
        for etiqueta, mensajes in (("ERROR", errores), ("aviso", avisos)):
            for mensaje in mensajes:
                print(f"    {etiqueta}: {mensaje}")
        total_av += len(avisos)
        con_error += bool(errores)

    print("\n" + "=" * 60)
    if con_error:
        print(f"HAY ERRORES en {con_error} célula(s). Arreglalos antes de usarlas con la IA.")
        print("¿No entendés un mensaje? Mirá DOCS/TROUBLESHOOTING.md")
        return 1
    print("TODO BIEN — las células están listas para usar con la IA.")
    if total_av:
        print(f"({total_av} aviso(s): no bloquean, pero conviene revisarlos.)")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else CELLS_DIR))
