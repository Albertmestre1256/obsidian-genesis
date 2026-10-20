#!/usr/bin/env python3
"""Revisa propiedades y secciones de las fichas, también las renombradas.

Desde la raíz:
    python 00_CORE/schemas/validate.py

Errores: formato que corregir. Avisos: datos que revisar, sin bloquear.
Ignora ayuda entre %%...%%. Python estándar 3.8+; ver DOCS/TROUBLESHOOTING.md.
"""

import argparse
import datetime
import hashlib
import importlib.util
import json
import os
import posixpath
import re
import stat
import sys
sys.dont_write_bytecode = True  # no dejar __pycache__ dentro de la bóveda
import unicodedata
from pathlib import Path
from urllib.parse import unquote

# Reglas de validación
PROPIEDADES_OBLIGATORIAS = ["tipo", "proyecto", "descripcion", "contexto", "actualizado"]
SECCIONES_OBLIGATORIAS = ["Hechos clave", "Próximas acciones"]
CONTEXTOS = {"A": "técnico", "B": "narrativo", "C": "persuasivo", "D": "operativo"}
MARCA_PENDIENTE = "[completar"
MAX_TOKENS_CELULA = 3000  # ver davidkimai-resources/evaluation/token_budgeting.md

# El inventario de personalización: cabecera canónica de 6 columnas
INVENTARIO_CABECERA = ["Ítem", "Alcance", "Estado", "Dato o referencia", "Origen y fecha", "Para retomar"]
INVENTARIO_ESTADOS_VALIDOS = {"confirmado", "pendiente", "omitido", "propuesto", "no-aplica"}

CELLS_DIR = Path(__file__).resolve().parent.parent / "cells"

# Cargar módulos de confianza desde la raíz del kit (no de la bóveda destino)
_KIT_ROOT = Path(__file__).resolve().parent.parent.parent
def _cargar_modulo(nombre, relativo):
    spec = importlib.util.spec_from_file_location(nombre, _KIT_ROOT / relativo)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo

_lineas = None
# registrar_cambios y actualizar_indice se cargan perezosamente en validar_cierre para evitar ciclo de importación
_registro = None
_mapas = None

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


def es_celula(path):
    """La misma clasificación para buscar fichas y verificar una ficha tocada."""
    path = Path(path)
    if path.suffix.lower() != '.md' or path.name.lower() == 'template_cell.md' or not path.is_file():
        return False
    if path.name.lower().endswith('-context.md'):
        return True
    text, error = leer_nota(path)
    if error:
        return True  # No ocultar posibles fichas que no pudimos clasificar.
    partes = separar(text)
    if partes is not None:
        for linea in partes[0].splitlines():
            if re.match(r'^proyecto\s*:', linea):
                return True
            if re.match(r'^tipo\s*:', linea):
                props, error = leer_propiedades(linea, primera_linea=2)
                if not error and normalizar(props.get('tipo', '')) == 'celula':
                    return True
    return False


def buscar_celulas(cells_dir):
    """Reconoce fichas por propiedades; conserva nombres convencionales rotos."""
    return [path for path in sorted(Path(cells_dir).iterdir()) if es_celula(path)]


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


def _parsear_fila_tabla(linea):
    """Divide celdas por barras no escapadas, según paridad de backslashes."""
    linea = linea.strip()
    if not linea.startswith('|') or not linea.endswith('|'):
        return None
    contenido, inicio = linea[1:-1], 0
    celdas, actual = [], []
    for barra in re.finditer(r'(\\*)\|', contenido):
        cuenta = len(barra[1])
        actual.extend((contenido[inicio:barra.start()], '\\' * (cuenta // 2)))
        if cuenta % 2:
            actual.append('|')
        else:
            celdas.append(''.join(actual).strip())
            actual = []
        inicio = barra.end()
    actual.append(contenido[inicio:])
    celdas.append(''.join(actual).strip())
    return celdas


def _es_cabecera_inventario(celdas):
    """Comprueba las seis columnas en su orden canónico."""
    if len(celdas) != 6:
        return False
    return all(normalizar(c.strip()) == normalizar(e) for c, e in zip(celdas, INVENTARIO_CABECERA))


def _es_separador_valido(celdas):
    """Comprueba un separador Markdown de seis columnas."""
    if len(celdas) != 6:
        return False
    patron = re.compile(r'^:?-+:?$')
    return all(patron.match(c.strip()) for c in celdas)


def _extraer_seccion_inventario(cuerpo):
    """Extrae el inventario sin ejemplos en comentarios o código.
    Acepta tabla plana O un único callout info depth1 que la envuelva.
    """
    cuerpo = re.sub(r'<!--.*?-->', '', cuerpo, flags=re.DOTALL)
    cuerpo = re.sub(r'%%.*?%%', '', cuerpo, flags=re.DOTALL)
    cuerpo = re.sub(r'^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$', '', cuerpo, flags=re.M | re.S)
    lineas = cuerpo.splitlines()
    en_inventario = False
    lineas_seccion = []
    for linea in lineas:
        if linea.startswith('## '):
            titulo = normalizar(linea[3:].strip())
            if titulo == 'inventario de personalizacion':
                en_inventario = True
                continue
            elif en_inventario:
                break
        if en_inventario:
            lineas_seccion.append(linea)

    # Normalizar: detectar callout info depth1 único con tabla, o tabla plana.
    # callout: > [!info]- título  (info case-insensitive, +/- tras ])
    # contenido: líneas que empiezan con '> ' (incluye '>' solo).
    # Fin del callout en primera línea sin '> '.
    # Error si hay ambas formas, dos callouts, o filas sueltas mezcladas.
    lineas_tabla = []
    en_callout = False
    vio_tabla_plana = False
    vio_tabla_callout = False

    for linea in lineas_seccion:
        stripped = linea.strip()
        if not en_callout:
            # Detectar inicio de callout info
            m = re.match(r'^> ?\[!info\][+-]?(?:[ \t].*)?$', linea, re.IGNORECASE)
            if m:
                if vio_tabla_plana or vio_tabla_callout:
                    # Ya vimos tabla antes -> mezcla inválida
                    lineas_tabla = ['__MEZCLA_INVALIDA__']
                    break
                en_callout = True
                continue
            # Línea de tabla plana (empieza con |)
            if stripped.startswith('|'):
                if vio_tabla_callout:
                    lineas_tabla = ['__MEZCLA_INVALIDA__']
                    break
                vio_tabla_plana = True
                lineas_tabla.append(linea)
            elif vio_tabla_plana and re.match(r'^>\s*\|', linea):
                return ['__ERROR_MEZCLA__']
            # Prosa permitida antes/después de tabla plana (se ignora)
        else:
            # Dentro de callout: línea debe empezar con '> '
            if linea.startswith('> '):
                contenido = linea[2:]  # quitar '> '
                if contenido.strip().startswith('|'):
                    vio_tabla_callout = True
                lineas_tabla.append(contenido)
            elif linea == '>':
                # '>' en blanco válido dentro del callout
                lineas_tabla.append('')
            else:
                # Fin del callout al primer contenido sin '> '
                en_callout = False
                # Si hay más contenido con '|' tras el callout -> error
                if stripped.startswith('|'):
                    lineas_tabla = ['__MEZCLA_INVALIDA__']
                    break
                # Prosa tras callout se ignora

    if '__MEZCLA_INVALIDA__' in lineas_tabla:
        return ['__ERROR_MEZCLA__']
    # Los fences citados se reconocen después de quitar el wrapper explícito.
    limpio = re.sub(r'^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$', '', '\n'.join(lineas_tabla), flags=re.M | re.S)
    normalizadas = limpio.splitlines()
    en_tabla, terminada = False, False
    for linea in normalizadas:
        if linea.strip().startswith('|'):
            if terminada:
                return ['__ERROR_MEZCLA__']
            en_tabla = True
        elif linea.strip() and en_tabla:
            terminada = True
    return normalizadas


def _validar_tabla_inventario(lineas_inventario):
    """Valida estructura, estados, alcances y duplicados sin escribir."""
    if not lineas_inventario:
        return ['El inventario de personalización: falta la tabla (cabecera, separador y filas).'], []
    if lineas_inventario == ['__ERROR_MEZCLA__']:
        return ['El inventario de personalización: mezcla una tabla suelta con un bloque plegable, o tiene dos bloques; dejá una sola tabla en un único lugar.'], []
    idx_tabla = next((i for i, linea in enumerate(lineas_inventario) if linea.strip().startswith('|')), None)
    if idx_tabla is None:
        return ['El inventario de personalización: no se encuentra tabla markdown.'], []
    if idx_tabla + 2 >= len(lineas_inventario):
        return ['El inventario de personalización: tabla incompleta (falta separador o filas de datos).'], []
    cabecera = _parsear_fila_tabla(lineas_inventario[idx_tabla])
    if cabecera is None:
        return ['El inventario de personalización: la cabecera no es una fila de tabla válida.'], []
    if not _es_cabecera_inventario(cabecera):
        return ['El inventario de personalización: la cabecera no coincide con la canónica (Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar).'], []
    separador = _parsear_fila_tabla(lineas_inventario[idx_tabla + 1])
    if separador is None:
        return ['El inventario de personalización: falta el separador markdown tras la cabecera.'], []
    if not _es_separador_valido(separador):
        return ['El inventario de personalización: el separador debe tener 6 columnas (formato |---|---|---|---|---|---|).'], []
    errores, filas_datos, vistas = [], [], set()
    for i in range(idx_tabla + 2, len(lineas_inventario)):
        linea = lineas_inventario[i].strip()
        if not linea:
            continue
        if not linea.startswith('|'):
            break
        celdas = _parsear_fila_tabla(linea)
        if celdas is None or len(celdas) != 6:
            errores.append(f'El inventario de personalización: fila {i - idx_tabla - 1} malformada (se esperan 6 columnas, pipes no escapados en celdas).')
            continue
        item, alcance, estado, dato, origen, retomar = celdas
        if not item.strip():
            errores.append(f'El inventario de personalización: fila {i - idx_tabla - 1}: "Ítem" no puede estar vacío.')
        alcance_norm = alcance.strip().lower()
        if alcance_norm != 'boveda':
            if not alcance_norm.startswith('proyecto:'):
                errores.append(f'El inventario de personalización: fila {i - idx_tabla - 1}: "Alcance" debe ser "boveda" o "proyecto:identificador" (recibido: {alcance!r}).')
            else:
                proj_id = alcance_norm[len('proyecto:'):]
                if not proj_id or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', proj_id):
                    errores.append(f'El inventario de personalización: fila {i - idx_tabla - 1}: identificador de proyecto inválido en "Alcance" (usá minúsculas, números y guiones simples: proyecto:mi-proyecto).')
        estado_norm = estado.strip().lower()
        if estado_norm not in INVENTARIO_ESTADOS_VALIDOS:
            errores.append(f'El inventario de personalización: fila {i - idx_tabla - 1}: "Estado" inválido {estado!r}. Valores: confirmado, pendiente, omitido, propuesto, no-aplica.')
        clave = (item.strip().lower(), alcance_norm)
        if clave in vistas:
            errores.append(f'El inventario de personalización: fila {i - idx_tabla - 1}: duplicado "Ítem + Alcance" ({item} / {alcance}).')
        vistas.add(clave)
        filas_datos.append({
            'item': item.strip(),
            'alcance': alcance.strip(),
            'estado': estado_norm,
            'dato': dato.strip(),
            'origen': origen.strip(),
            'retomar': retomar.strip()
        })
    if not filas_datos:
        errores.append('El inventario de personalización: no hay filas de datos (se requiere al menos una).')
    return errores, filas_datos


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


def _es_enlace(ruta):
    info = os.lstat(ruta)
    if stat.S_ISLNK(info.st_mode):
        return True
    if getattr(info, 'st_file_attributes', 0) & 0x400:
        # Como note_index.es_enlace: archivos en la nube y deduplicación no redirigen rutas.
        tag = getattr(info, 'st_reparse_tag', None)
        return tag is None or not ((tag & 0xFFFF0FFF) == 0x9000001A or tag == 0x80000013)
    return False


def _notas_con_nombre(raiz, nombre):
    """Notas con ese nombre que Obsidian indexa: sin carpetas ocultas, dependencias, enlaces ni junctions."""
    encontradas = []
    for base, dirs, names in os.walk(str(raiz), followlinks=False):
        dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ('node_modules', '__pycache__')
                   and not _es_enlace(os.path.join(base, d))]
        if nombre in names:
            encontradas.append(Path(base) / nombre)
    return encontradas


def validar_configuracion(raiz):
    """Comprueba el cierre básico y el inventario de personalización cuando existe la configuración del kit.

    No comprueba hechos, interfaz ni todos los enlaces. No escribe archivos.
    """
    path = Path(raiz) / '00_CORE/configuracion.md'
    if not path.exists():
        return []
    texto, error = leer_nota(path)
    if error:
        return [f'Configuración: {error}']
    partes = separar(texto)
    if partes is None:
        return ['La configuración necesita propiedades entre --- al comienzo.']
    props, error = leer_propiedades(partes[0], 2)
    if error:
        return [f'Configuración: {error}']
    errores = []
    if props.get('estado') not in ('parcial', 'lista'):
        errores.append('La configuración necesita estado parcial o lista.')
    if props.get('personalizacion') not in ('abierta', 'completa'):
        errores.append('La configuración necesita personalizacion abierta o completa.')
    
    # Validar inventario de personalización
    cuerpo = partes[1]
    lineas_inventario = _extraer_seccion_inventario(cuerpo)
    errores_inventario, filas = _validar_tabla_inventario(lineas_inventario)
    errores.extend(errores_inventario)
    
    # Validar coherencia personalizacion: completa con filas pendiente/propuesto
    if not errores_inventario and props.get('personalizacion') == 'completa':
        for fila in filas:
            if fila['estado'] in ('pendiente', 'propuesto'):
                errores.append('El inventario de personalización: "personalizacion: completa" no permite filas "pendiente" ni "propuesto" (item: {}).'.format(fila['item']))
                break
    
    # Panel: verificar acceso al inventario
    panel, error = leer_nota(Path(raiz) / 'Panel.md')
    if error:
        return errores + [f'Panel: {error}']
    # Un ejemplo dentro de código o comentarios no es un acceso utilizable.
    panel = _texto_visible(panel)
    rutas = re.findall(r'\[\[([^\]|]+)(?:\|[^\]]*)?\]\]|\[[^\]]*\]\(([^)]+)\)', panel)
    relativa = path.relative_to(Path(raiz)).as_posix()
    acceso = False
    for wiki, markdown in rutas:
        if markdown:
            destino = re.fullmatch(r'''(<[^>]+>|\S+?)(?:\s+["'].*["'])?''', markdown.strip())
            if destino is None:
                continue
            markdown = destino.group(1)
        ruta = unquote(wiki.rstrip('\\') if wiki else markdown).split('#', 1)[0].strip().strip('<>')
        ruta = re.sub(r'\\([_\[\] ()])', r'\1', ruta).replace('\\', '/')
        while ruta.startswith('./'):
            ruta = ruta[2:]
        if ruta in {relativa, relativa[:-3]}:
            acceso = True
        elif wiki and ruta in {path.name, path.stem}:
            # Obsidian admite nombres cortos; exigir una única nota con ese nombre.
            acceso = acceso or _notas_con_nombre(raiz, path.name) == [path]
    if not acceso:
        errores.append('El Panel no da acceso al inventario: añadí un enlace a 00_CORE/configuracion.md.')
    return errores


def _texto_visible(texto):
    texto = re.sub(r'%%.*?%%|<!--.*?-->', '', texto, flags=re.S)
    texto = re.sub(r'^(`{3,}|~{3,})[^\n]*\n.*?^\1\s*$', '', texto, flags=re.M | re.S)
    return re.sub(r'(`+).*?\1', '', texto)


def _lineas_visibles(texto):
    """Líneas fuera de comentarios y bloques de código; conserva valores inline."""
    partes = separar(texto)
    cuerpo = partes[1] if partes is not None else texto
    fence, comentario = None, None
    for original in cuerpo.splitlines():
        # Guardar cada nivel: dentro de código, otros '>' son texto literal.
        niveles = [original]
        while True:
            cita = re.match(r'^ {0,3}>[ \t]?', niveles[-1])
            if cita is None:
                break
            niveles.append(niveles[-1][cita.end():])
        profundidad = len(niveles) - 1
        if fence:
            caracter, largo, nivel = fence
            if profundidad < nivel:
                fence = None  # Terminó el contenedor de la cita; esta línea ya es visible.
            else:
                cierre = re.fullmatch(r' {0,3}(' + re.escape(caracter) + r'{'+str(largo)+r',})[ \t]*', niveles[nivel])
                if cierre:
                    fence = None
                continue
        linea = niveles[-1]
        if not comentario:
            if linea.startswith(('    ', '\t')):
                continue
            marca = re.match(r'^ {0,3}(`{3,}|~{3,})(.*)$', linea)
            if marca and not (marca[1][0] == '`' and '`' in marca[2]):
                fence = (marca[1][0], len(marca[1]), profundidad)
                continue
        visible = ''
        while linea:
            if comentario:
                fin = linea.find(comentario)
                if fin < 0:
                    break
                linea = linea[fin + len(comentario):]
                comentario = None
                continue
            token = re.search(r'`+|%%|<!--', linea)
            if token is None:
                visible += linea
                break
            visible += linea[:token.start()]
            if token[0].startswith('`'):
                resto = linea[token.end():]
                cierre = re.search(r'(?<!`)' + re.escape(token[0]) + r'(?!`)', resto)
                fin = token.end() + cierre.end() if cierre else token.end()
                visible += linea[token.start():fin]
                linea = linea[fin:]
            else:
                visible += ' '
                comentario = '%%' if token[0] == '%%' else '-->'
                linea = linea[token.end():]
        yield visible


def _validar_operacion_visible(texto, operacion):
    """Contrasta la etiqueta opcional con la operación, sin alterar el ID."""
    valores = []
    for visible in _lineas_visibles(texto):
        etiqueta = re.fullmatch(r' {0,3}(?:(?:[-*+]|\d{1,9}[.)])[ \t]+)?([^:]+):(.*)', visible)
        if etiqueta:
            nombre, valor = etiqueta[1].strip(), etiqueta[2].strip()
            enfasis = re.match(r'^(\*{1,3}|_{1,3})', nombre)
            if enfasis and not nombre.endswith(enfasis[0]) and valor.startswith(enfasis[0]):
                # También **etiqueta:** valor; el énfasis corresponde al título, no al ID.
                valor = valor[len(enfasis[0]):].strip()
            if normalizar(nombre.strip('*_ ')) == 'ultima operacion de mantenimiento':
                valores.append(valor)
    prefijo = 'Configuración: última operación de mantenimiento; revisión manual pendiente: '
    if len(valores) > 1:
        return [prefijo + 'hay varias etiquetas; conservar una sola tras revisar sus datos.']
    if not valores or valores[0] in ('', '-', '—'):
        return []  # Compatibilidad: las configuraciones anteriores pueden omitirla.
    valor = re.fullmatch(r'(`?)([a-zA-Z0-9_-]{1,80})\1(?:[ \t]+\((\d{4}-\d{2}-\d{2})\))?', valores[0])
    if valor is None or valor[3] and not es_fecha(valor[3]):
        return [prefijo + 'usar un ID exacto, opcionalmente entre backticks y con fecha (AAAA-MM-DD).']
    if valor[2] != operacion:
        return [prefijo + f'la etiqueta "{valor[2]}" no coincide con la operación "{operacion}".']
    return []


def _validar_proyecto_inicial(texto, raiz):
    """Contrasta la declaración canónica con fichas e índices reales, sin escribir."""
    prefijo = 'Configuración: proyecto inicial; revisión manual pendiente: '
    partes = separar(texto)
    if partes is None:
        return []  # La validación de configuración informa las propiedades inválidas.
    props, error = leer_propiedades(partes[0], 2)
    if error:
        return []
    campos, secciones, dentro = {}, 0, False
    for visible in _lineas_visibles(texto):
        titulo = re.fullmatch(r' {0,3}(#{1,6})[ \t]+(.+?)(?:[ \t]+#+)?[ \t]*', visible)
        if titulo:
            dentro = len(titulo[1]) == 2 and normalizar(titulo[2].strip('*_ ')) == 'proyecto inicial'
            if dentro:
                secciones += 1
            continue
        if not dentro:
            continue
        campo = re.fullmatch(r' {0,3}(?:(?:[-*+]|\d{1,9}[.)])[ \t]+)?([^:]+):(.*)', visible)
        if not campo:
            continue
        etiqueta, valor = campo[1].strip(), campo[2].strip()
        enfasis = re.match(r'^(\*{1,3}|_{1,3})', etiqueta)
        if enfasis and not etiqueta.endswith(enfasis[0]) and valor.startswith(enfasis[0]):
            valor = valor[len(enfasis[0]):].strip()
        nombre = normalizar(etiqueta.strip('*_ '))
        if nombre in {'identificador', 'ficha e indice'}:
            campos.setdefault(nombre, []).append(valor)
    if not secciones:
        return []  # El formato anterior sin esta sección sigue siendo compatible.
    if secciones > 1 or any(len(v) > 1 for v in campos.values()):
        return [prefijo + 'hay secciones o campos repetidos; revisar y conservar una declaración inequívoca.']
    parcial = props.get('estado') == 'parcial'
    codigo = campos.get('identificador', [''])[0]
    referencias = campos.get('ficha e indice', [''])[0]
    vacios = {'', '-', '—'}
    sin_codigo = codigo in vacios or codigo.startswith(MARCA_PENDIENTE)
    sin_referencias = referencias in vacios or parcial and referencias.startswith(MARCA_PENDIENTE)
    if sin_codigo and parcial and sin_referencias:
        return []
    identificador = re.fullmatch(r'(`?)([a-z0-9]+(?:-[a-z0-9]+)*)\1', codigo)
    if identificador is None:
        return [prefijo + 'falta un Identificador concreto con minúsculas, números y guiones simples.']
    if parcial and sin_referencias:
        return []  # Un proyecto acordado puede esperar su creación durante la entrevista.
    codigo = identificador[2]
    try:
        registros = _mapas.catalogo(raiz)
        cells = Path(raiz) / '00_CORE/cells'
        diarias = {p.relative_to(raiz).as_posix() for p in buscar_celulas(cells)} if cells.is_dir() else set()
    except (OSError, ValueError) as error:
        return [prefijo + f'no se pudo comprobar el catálogo: {error}']
    fichas, indices = [], []
    for registro in registros:
        ruta, meta = registro['ruta'], registro['meta']
        tipo = _mapas.tipo(meta)
        if ruta.startswith(('PROJECT_TEMPLATE/', '00_CORE/templates/')):
            continue
        if meta.get('aviso') and tipo in {'celula', 'indice-proyecto'}:
            return [prefijo + f'metadatos ambiguos en {ruta}; revisarlos antes de elegir proyecto.']
        if (tipo == 'celula' and ruta.startswith('00_CORE/cells/')
                and meta.get('proyecto') == codigo and str(meta.get('ejemplo')).lower() == 'true'):
            return [prefijo + 'el Identificador coincide con una ficha de ejemplo; acordar otro sin mezclar sus datos.']
        if meta.get('proyecto') != codigo or str(meta.get('ejemplo')).lower() == 'true':
            continue
        if tipo == 'celula' and ruta.startswith('00_CORE/cells/') and ruta not in diarias:
            return [prefijo + 'la ficha no está incluida en la revisión diaria de 00_CORE/cells; revisar su nombre y ubicación.']
        if tipo == 'celula' and ruta.startswith('00_CORE/cells/'):
            fichas.append(ruta)
        elif tipo == 'indice-proyecto':
            indices.append(ruta)
    if len(fichas) != 1 or len(indices) != 1:
        return [prefijo + f'para {codigo} se necesita una ficha propia y un índice de proyecto inequívocos '
                f'(encontrados: {len(fichas)} fichas y {len(indices)} índices); comprobar sus propiedades proyecto y tipo.']
    if sin_referencias:
        return []  # Compatibilidad de la ficha/índice no enlazados explícitamente.
    rutas = {r['ruta'] for r in registros if r['ruta'].lower().endswith('.md')}
    # Resolver solo contra el catálogo: nunca abrir un destino aportado por el usuario.
    def resolver(destino, wiki):
        destino = unquote(destino.strip('<>')).split('#', 1)[0].strip()
        destino = re.sub(r'\\([_\[\] ()])', r'\1', destino).replace('\\', '/')
        if not destino or re.match(r'^/|^[A-Za-z][A-Za-z0-9+.-]*:', destino):
            return None
        if wiki and '/' not in destino:
            candidatos = [r for r in rutas if Path(r).name == destino or Path(r).stem == destino]
        else:
            ruta = posixpath.normpath(destino if wiki else posixpath.join('00_CORE', destino))
            if ruta == '..' or ruta.startswith('../'):
                return None
            candidatos = [r for r in rutas if r == ruta or wiki and r == ruta + '.md']
        return candidatos[0] if len(candidatos) == 1 else None
    visibles = _texto_visible(referencias)
    if re.search(r'[A-Za-z][A-Za-z0-9+.-]*://|<[A-Za-z][A-Za-z0-9+.-]*:', visibles):
        return [prefijo + 'Ficha e índice contiene un enlace externo; usar los enlaces internos de la ficha y su índice.']
    encontrados = set()
    enlaces = re.findall(r'''\[\[([^\]\n]+)\]\]|\[[^\]\n]*\]\((<[^>\n]+>|[^\s)]+)(?:[ \t]+["'][^"']*["'])?\)''',
                         visibles)
    for wiki, markdown in enlaces:
        ruta = resolver(wiki.split('|', 1)[0] if wiki else markdown, bool(wiki))
        if ruta not in fichas + indices:
            return [prefijo + 'Ficha e índice contiene un enlace ausente, ambiguo, externo o de otro destino; revisar sus referencias.']
        encontrados.add(ruta)
    if encontrados != set(fichas + indices):
        return [prefijo + 'Ficha e índice debe enlazar la ficha propia y el índice de ese proyecto mediante enlaces utilizables.']
    return []


def validar_cierre(raiz, operacion):
    """Validación de cierre: comprueba configuración, mapas, rangos, registro y fichas.
    No escribe ni repara nada. Devuelve lista de errores en español (vacía = ok)."""
    global _registro, _mapas, _lineas
    try:
        if _lineas is None:
            _lineas = _cargar_modulo('lineas_cierre', '00_CORE/schemas/note_index.py')
        if _registro is None:
            _registro = _cargar_modulo('registro_cierre', '00_CORE/schemas/registrar_cambios.py')
        if _mapas is None:
            _mapas = _cargar_modulo('mapas_cierre', 'actualizar_indice.py')
    except (OSError, ValueError, ImportError) as error:
        return [f'Herramientas de cierre no disponibles: {error}']
    
    raiz = Path(raiz)
    errores = []

    # 1. Configuración debe existir y pasar validación existente
    config_path = raiz / '00_CORE' / 'configuracion.md'
    if not config_path.is_file():
        errores.append('Falta 00_CORE/configuracion.md.')
    else:
        config_errores = validar_configuracion(raiz)
        if config_errores:
            errores.extend(f'Configuración: {e}' for e in config_errores)
        config_texto, error = leer_nota(config_path)
        if not error:
            errores.extend(_validar_operacion_visible(config_texto, operacion))
            errores.extend(_validar_proyecto_inicial(config_texto, raiz))

    # 2. Panel: aviso inicial "Para empezar:" debe estar adaptado (no ejemplo)
    panel_path = raiz / 'Panel.md'
    if panel_path.is_file():
        texto, error = leer_nota(panel_path)
        if error:
            errores.append(f'Panel: {error}')
        else:
            if re.search(r'\*\*Para empezar:\*\*.*(?:Dale la carpeta a tu IA|respondé sus preguntas)', _texto_visible(texto)):
                errores.append('Panel: aviso inicial "Para empezar:" aún contiene el texto de ejemplo.')
    else:
        errores.append('Falta Panel.md.')

    # 3. Mapas actualizados (actualizar_indice.actualizar con comprobar=True)
    try:
        resultado_mapas = _mapas.actualizar(raiz, comprobar=True)
    except (OSError, ValueError) as e:
        errores.append(f'Mapas: {e}')
    else:
        if resultado_mapas.get('estado') != 'vigente':
            errores.append('Mapas desactualizados (general o nodos).')
        indices_manuales = resultado_mapas.get('indices_manuales', [])
        if indices_manuales:
            for idx in indices_manuales:
                errores.append(f'Índice manual pendiente de revisión: {idx}')

    # 4. Rangos de líneas en notas editables (note_index.archivos + contenido)
    try:
        for nota in _lineas.archivos(raiz):
            if _lineas.protegida(nota, raiz):
                continue
            raw = nota.read_bytes()
            esperado = _lineas.contenido(raw)
            if raw != esperado:
                errores.append(f'Rangos desactualizados: {nota.relative_to(raiz)}')
    except (OSError, ValueError) as e:
        errores.append(f'Rangos: {e}')

    # 5. Fichas (células) válidas según pipeline existente
    try:
        cells_dir = raiz / '00_CORE' / 'cells'
        if not cells_dir.is_dir():
            errores.append('Falta la carpeta de fichas: 00_CORE/cells.')
        else:
            for ficha in buscar_celulas(cells_dir):
                ficha_errores, _ = validar(ficha)
                if ficha_errores:
                    for e in ficha_errores:
                        errores.append(f'Ficha {ficha.name}: {e}')
    except (OSError, ValueError) as e:
        errores.append(f'Fichas: {e}')

    # 6. Registro de cambios: operación exacta, verificada, fecha válida, config hash coincide
    try:
        # Leer registro activo e histórico
        registro_path = raiz / _registro.REGISTRO
        if not registro_path.is_file():
            errores.append('Falta registro activo (00_CORE/logs/registro-cambios.md).')
        else:
            raw_registro = registro_path.read_bytes()
            inicio, actuales = _registro.entradas(raw_registro)

            # Histórico
            historicos = []
            historial_dir = raiz / _registro.ARCHIVO
            if historial_dir.is_dir():
                for arch in sorted(historial_dir.glob('*.md')):
                    try:
                        raw = _lineas.ruta_real(arch).read_bytes()
                        _, prev = _registro.entradas(raw)
                        historicos.extend(prev)
                    except (OSError, ValueError) as e:
                        errores.append(f'Historial incompatible: {arch.name} ({e})')

            all_entries = historicos + actuales
            matches = [e for e in all_entries if e.get('id') == operacion]
            if not matches:
                errores.append(f'Operación "{operacion}" no encontrada en registro activo ni histórico.')
            elif len(matches) > 1:
                errores.append(f'Operación "{operacion}" ambigua: varias entradas con ese id.')
            else:
                entry = matches[0]
                if not entry.get('verificado'):
                    errores.append(f'Operación "{operacion}" no verificada (verificado: false).')
                # Fecha aware y no futura
                try:
                    fecha_op = _registro.momento(entry['fecha'])
                    if fecha_op > datetime.datetime.now().astimezone():
                        errores.append(f'Operación "{operacion}": fecha en el futuro.')
                except (KeyError, ValueError):
                    errores.append(f'Operación "{operacion}": fecha inválida o ausente.')

                # Cambio no borrado para 00_CORE/configuracion.md con sha256 actual
                config_changes = [c for c in entry.get('cambios', []) if c.get('ruta') == '00_CORE/configuracion.md' and c.get('accion') != 'borrar']
                if not config_changes:
                    errores.append(f'Operación "{operacion}": sin cambio de configuración (crear/editar 00_CORE/configuracion.md).')
                else:
                    # Verificar hash actual
                    if not config_path.is_file():
                        errores.append(f'Operación "{operacion}": configuración no existe para verificar hash.')
                    else:
                        actual_hash = hashlib.sha256(config_path.read_bytes()).hexdigest()
                        for cambio in config_changes:
                            guardado = cambio.get('sha256')
                            if guardado is None:
                                errores.append(f'Operación "{operacion}": hash de configuración ausente en el registro.')
                                break
                            if not isinstance(guardado, str):
                                errores.append(f'Operación "{operacion}": hash de configuración inválido (tipo {type(guardado).__name__}).')
                                break
                            if guardado != actual_hash:
                                errores.append(f'Operación "{operacion}": hash de configuración no coincide (guardado: {guardado[:12]}..., actual: {actual_hash[:12]}...).')
                                break

    except (OSError, ValueError) as e:
        errores.append(f'Registro: {e}')

    # 7. Bloqueo de registro concurrente
    lock_path = raiz / '00_CORE' / 'logs' / '.registro-cambios.lock'
    if lock_path.exists():
        errores.append('Registro bloqueado por otra operación (.registro-cambios.lock).')

    return errores


def main(cells_dir=CELLS_DIR):
    """API diaria preservada: main(cells_dir=CELLS_DIR) para revisión de fichas."""
    cells_dir = Path(cells_dir)
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    if (cells_dir / '00_CORE').is_dir():
        cells_dir = cells_dir / '00_CORE' / 'cells'
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
        print("Copiá 00_CORE/templates/TEMPLATE_cell.md a 00_CORE/cells/nombre-de-tu-proyecto-context.md")

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
    if cells_dir.name.lower() == 'cells' and cells_dir.parent.name == '00_CORE':
        configuracion = validar_configuracion(cells_dir.parent.parent)
        for mensaje in configuracion:
            print(f'CONFIGURACIÓN INCOMPLETA: {mensaje}')
        if configuracion:
            print('Conservá el estado parcial hasta completar esta integración; fichas válidas no equivalen a bóveda lista.')
            return 1
    if con_error:
        print(f"HAY ERRORES en {con_error} célula(s). Arreglalos antes de usarlas con la IA.")
        print("¿No entendés un mensaje? Mirá DOCS/TROUBLESHOOTING.md")
        return 1
    if celulas:
        print("TODO BIEN — las células están listas para usar con la IA; esto no comprueba la interfaz de Obsidian.")
    if total_av:
        print(f"({total_av} aviso(s): no bloquean, pero conviene revisarlos.)")
    return 0


def _main_cli(argv=None):
    """CLI separado para cierre y modo diario desde raíz."""
    parser = argparse.ArgumentParser(description=__doc__, add_help=False)
    parser.add_argument('ruta', nargs='?', default=str(CELLS_DIR),
                        help='Raíz de la bóveda o carpeta cells. Sin argumento usa la bóveda donde está este script, no la carpeta actual.')
    parser.add_argument('--cierre', action='store_true', help='Modo cierre: validar operación de cierre')
    parser.add_argument('--operacion', help='ID de operación para --cierre (obligatorio)')
    parser.add_argument('-h', '--help', action='help', help='Mostrar esta ayuda')
    args = parser.parse_args(argv)

    # La consola de Windows a veces no muestra bien acentos y símbolos.
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

    # Validar combinaciones de flags
    if args.operacion is not None and not args.cierre:
        print('Error: --operacion requiere --cierre', file=sys.stderr)
        return 2

    # Modo cierre
    if args.cierre:
        if not args.operacion:
            print('Error: --cierre requiere --operacion ID', file=sys.stderr)
            return 2
        raiz = Path(args.ruta).absolute()
        if raiz.name.lower() == 'cells' and raiz.parent.name == '00_CORE':
            raiz = raiz.parent.parent
        if not raiz.is_dir():
            print(f'Error: ruta no es un directorio: {raiz}', file=sys.stderr)
            return 2
        print(f'Bóveda revisada: {raiz.absolute()}')
        errores = validar_cierre(raiz, args.operacion)
        if errores:
            for e in errores:
                print(f'ERROR: {e}')
            return 1
        print(f'CIERRE VERIFICADO — operación: {args.operacion} (fichas, configuración, mapas, rangos y registro).')
        print('Comprueba archivos y la operación declarada; no la verdad de los datos ni la interfaz de Obsidian.')
        return 0

    return main(args.ruta)


if __name__ == "__main__":
    sys.exit(_main_cli())
