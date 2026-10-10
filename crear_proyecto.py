#!/usr/bin/env python3
"""Crea un proyecto acordado en una bóveda con las reglas del kit. Python 3.8+."""
import argparse
import importlib.util
import json
import os
from pathlib import Path
import re
import stat
import sys
import tempfile
import unicodedata

RAIZ = Path(__file__).resolve().parent
SUBCARPETAS = ('01_FUENTES', '02_SINTESIS', '03_ENTREGABLES', '_archivo')


def ruta_real(ruta):
    ruta = Path(os.path.abspath(str(ruta)))
    for parte in (ruta,) + tuple(ruta.parents):
        try:
            info = parte.lstat()
        except FileNotFoundError:
            continue
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 0x400:
            raise ValueError('La ruta contiene un enlace o junction: {}'.format(parte))
    return ruta


def texto_linea(valor, campo, opcional=False):
    if opcional and valor is None:
        return ''
    if not isinstance(valor, str) or (not opcional and not valor.strip()):
        raise ValueError('{} debe contener texto.'.format(campo))
    if any(ord(c) < 32 or ord(c) == 127 for c in valor):
        raise ValueError('{} debe ocupar una sola línea, sin caracteres de control.'.format(campo))
    return valor.strip()


def identificador(nombre):
    ascii_text = unicodedata.normalize('NFKD', nombre).encode('ascii', 'ignore').decode()
    return re.sub(r'[^a-z0-9]+', '-', ascii_text.lower()).strip('-')


def comprobar_id(valor):
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', valor) or len(valor) > 80:
        raise ValueError('Usá un identificador corto con letras, números y guiones; acordá una variante.')
    if valor in {'con', 'prn', 'aux', 'nul'} or re.fullmatch(r'(?:com|lpt)[0-9]', valor):
        raise ValueError('El nombre está reservado en Windows; acordá otro identificador.')
    return valor


def markdown(valor):
    return re.sub(r'([\\\[\]<>#|*_`])', r'\\\1', valor)


def modulo_kit(origen, ruta, nombre):
    spec = importlib.util.spec_from_file_location(nombre, ruta_real(origen / ruta))
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


def validador(origen):
    return modulo_kit(origen, '00_CORE/schemas/validate.py', 'validador_kit')


def indexador(origen=RAIZ):
    return modulo_kit(origen, 'actualizar_indice.py', 'indice_kit')


def lineador(origen=RAIZ):
    return modulo_kit(origen, '00_CORE/schemas/note_index.py', 'lineas_creador')


def planificar(destino, datos, origen=RAIZ):
    origen, destino = ruta_real(origen), ruta_real(destino)
    if not destino.is_dir():
        raise ValueError('La carpeta de bóveda debe existir y tener los archivos del kit.')
    reglas = Path('00_CORE/atoms/00_vault-rules.md')
    if ruta_real(destino / reglas).read_text(encoding='utf-8-sig') != ruta_real(origen / reglas).read_text(encoding='utf-8-sig'):
        raise ValueError('La bóveda tiene otras reglas; integrá el proyecto según sus convenciones sin usar este creador.')
    if not isinstance(datos, dict):
        raise ValueError('Los datos deben ser un objeto JSON.')
    nombre, descripcion, objetivo = [texto_linea(datos.get(k), k) for k in ('nombre', 'descripcion', 'objetivo')]
    contexto = texto_linea(datos.get('contexto'), 'contexto').upper()
    fecha = texto_linea(datos.get('fecha'), 'fecha')
    codigo = comprobar_id(texto_linea(datos.get('id', identificador(nombre)), 'id'))
    paso = texto_linea(datos.get('proximo_paso'), 'proximo_paso', opcional=True)
    revisar = validador(origen)
    if contexto not in revisar.CONTEXTOS or not revisar.es_fecha(fecha):
        raise ValueError('El contexto debe ser A/B/C/D y la fecha actual debe ser AAAA-MM-DD.')
    hechos = datos.get('hechos', [])
    if not isinstance(hechos, list):
        raise ValueError('hechos debe ser una lista de objetos texto/fuente.')
    lineas_hechos = []
    for hecho in hechos:
        if not isinstance(hecho, dict):
            raise ValueError('Cada hecho debe contener texto y fuente.')
        texto = texto_linea(hecho.get('texto'), 'hecho')
        fuente = texto_linea(hecho.get('fuente'), 'fuente', opcional=True)
        lineas_hechos.append('- {} (fuente: {})'.format(markdown(texto), markdown(fuente)))
    plantilla = ruta_real(origen / '00_CORE/cells/TEMPLATE_cell.md').read_text(encoding='utf-8-sig')
    separado = revisar.separar(plantilla)
    if separado is None:
        raise ValueError('La plantilla de ficha no tiene un bloque de propiedades cerrado. '
                         'Restaurá TEMPLATE_cell.md desde una copia íntegra del kit antes de reintentar; '
                         'no cambies las notas existentes.')
    bloque, cuerpo = separado
    props, error = revisar.leer_propiedades(bloque, 2)
    if error:
        raise ValueError('Plantilla de ficha inválida: ' + error)
    props.update(proyecto=codigo, descripcion=descripcion, objetivo=objetivo, contexto=contexto, actualizado=fecha)
    cuerpo = re.sub(r'%%.*?%%', '', cuerpo, flags=re.S)
    cuerpo = cuerpo.replace('# Célula del proyecto', '# ' + markdown(nombre), 1)
    cuerpo = cuerpo.replace('- [completar: algo concreto y verdadero sobre el proyecto] (fuente: [completar: dónde se puede comprobar])', '\n'.join(lineas_hechos))
    cuerpo = cuerpo.replace('- [ ] [completar: próximo paso concreto]', '- [ ] ' + markdown(paso) if paso else '')
    cuerpo = re.sub(r'\n{3,}', '\n\n', cuerpo).strip()
    cuerpo += '\n\n[[{}/00 - Índice y Contexto|Abrir el proyecto]]\n'.format(codigo)
    ficha = '---\n' + '\n'.join('{}: {}'.format(k, json.dumps(v, ensure_ascii=False)) for k, v in props.items()) + '\n---\n\n' + cuerpo
    indice = ruta_real(origen / 'PROJECT_TEMPLATE/00 - Índice y Contexto.md').read_text(encoding='utf-8')
    indice = re.sub(r'%%.*?%%', lambda m: m.group() if m.group() in
                    {'%% node-index:start %%', '%% node-index:end %%'} else '', indice, flags=re.S)
    indice = indice.replace('"[completar: nombre-corto-del-proyecto]"', json.dumps(codigo))
    indice = indice.replace('"[completar: A, B, C o D]"', json.dumps(contexto))
    indice = indice.replace('"[completar: resumen-del-nodo]"', json.dumps(descripcion, ensure_ascii=False))
    indice = indice.replace('creado:\n', 'creado: "{}"\n'.format(fecha), 1)
    indice = indice.replace('[completar: Nombre del proyecto]', markdown(nombre))
    autor = texto_linea(datos.get('autor'), 'autor', opcional=True) or 'Sin identificar; pendiente antes de entregar.'
    indice = indice.replace('[completar: autor del nodo]', markdown(autor))
    indice = indice.replace('[completar: de qué se trata el proyecto, en 2 o 3 líneas]', markdown(descripcion))
    indice = re.sub(r'^> \*\*Célula del proyecto:.*$', '> **Ficha:** [[00_CORE/cells/{}-context]]'.format(codigo), indice, flags=re.M)
    files = {'{}/00 - Índice y Contexto.md'.format(codigo): indice.encode('utf-8')}
    template = ruta_real(origen / 'PROJECT_TEMPLATE')
    for actual in sorted(template.rglob('*')):
        ruta_real(actual)
        if actual.is_file() and actual.name != '00 - Índice y Contexto.md':
            files[codigo + '/' + actual.relative_to(template).as_posix()] = actual.read_bytes()
    cell_rel = '00_CORE/cells/{}-context.md'.format(codigo)
    files[cell_rel] = ficha.encode('utf-8')
    lineas = lineador(origen)
    for rel, raw in list(files.items()):
        if rel.endswith('.md') and '01_FUENTES' not in Path(rel).parts:
            files[rel] = lineas.contenido(raw)
    if '[completar' in ficha or '[completar' in indice or '{{date' in ficha:
        raise ValueError('La plantilla cambió o hay marcadores sin resolver; revisá antes de crear.')
    with tempfile.TemporaryDirectory(prefix='obsidian-ficha-') as carpeta:
        note = Path(carpeta) / (codigo + '-context.md')
        note.write_bytes(files[cell_rel])
        errores, avisos = revisar.validar(note)
    if errores:
        raise ValueError('La ficha propuesta no valida: ' + '; '.join(errores))
    cells = ruta_real(destino / '00_CORE/cells')
    for actual in cells.iterdir():
        if actual.suffix.lower() == '.md':
            ruta_real(actual)
    for actual in revisar.buscar_celulas(cells):
        ruta_real(actual)
        separado = revisar.separar(actual.read_text(encoding='utf-8-sig'))
        if separado is None:
            raise ValueError('No se puede comprobar el proyecto de {}: revisá su ficha.'.format(actual))
        propiedades, error = revisar.leer_propiedades(separado[0], 2)
        if error:
            raise ValueError('No se puede comprobar el proyecto de {}: {}'.format(actual, error))
        if not isinstance(propiedades.get('proyecto'), str) or not propiedades['proyecto'].strip():
            raise ValueError('No se puede comprobar el proyecto de {}: falta su identificador.'.format(actual))
        if identificador(str(propiedades.get('proyecto', ''))) == codigo:
            if actual != destino / cell_rel or actual.read_bytes() != files[cell_rel]:
                raise ValueError('El proyecto ya tiene ficha: {}. Si es propia, retomalo; si es un ejemplo ficticio, acordá otro identificador para tu proyecto sin copiar sus datos.'.format(actual))
    for rel in files:
        ruta_real(destino / rel)
    # El bloque local se regenera después de crear: no es una edición del usuario.
    index_rel = codigo + '/00 - Índice y Contexto.md'
    index_path = destino / index_rel
    if index_path.is_file():
        actual, expected = index_path.read_bytes(), files[index_rel]
        start, end = b'%% node-index:start %%', b'%% node-index:end %%'
        if all(text.count(start) == text.count(end) == 1 and text.index(start) < text.index(end)
               for text in (actual, expected)):
            pattern = re.escape(start) + b'.*?' + re.escape(end)
            without = lambda raw: lineas.sin_indice(re.sub(pattern, b'', raw, flags=re.S).decode('utf-8'))
            if without(actual) == without(expected):
                files[index_rel] = actual
    anchor = any((destino / rel).is_file() and (destino / rel).read_bytes() == files[rel]
                 for rel in [cell_rel, codigo + '/00 - Índice y Contexto.md'])
    if (destino / codigo).exists() and not anchor:
        raise ValueError('La carpeta del proyecto ya está ocupada; acordá retomar o usar otro identificador.')
    nuevos, iguales = {}, []
    for rel, data in files.items():
        objetivo_path = ruta_real(destino / rel)
        if objetivo_path.exists():
            if not objetivo_path.is_file() or objetivo_path.read_bytes() != data:
                raise ValueError('Se conserva el archivo diferente: {}'.format(objetivo_path))
            iguales.append(rel)
        else:
            nuevos[rel] = data
    return {'destino': destino, 'id': codigo, 'ficha': cell_rel,
            'nuevos': nuevos, 'iguales': iguales, 'avisos': avisos}


def aplicar(plan, creados):
    lineas = lineador()
    for rel, data in plan['nuevos'].items():
        objetivo = ruta_real(plan['destino'] / rel)
        lineas.guardar(objetivo, None, data)
        creados.append(rel)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', required=True)
    parser.add_argument('--datos', required=True, help='JSON con las respuestas ya acordadas')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    creados, intento_aplicar = [], False
    try:
        datos = json.loads(Path(args.datos).read_text(encoding='utf-8-sig'))
        plan = planificar(Path(args.destino), datos)
        indice = indexador()
        indice.planificar(plan['destino'])  # Comprobar compatibilidad sin escribir.
        resultado_indice = {'estado': 'pendiente-de-aplicar', 'modificado': False}
        if not args.dry_run:
            intento_aplicar = True
            aplicar(plan, creados)
            resultado_indice = indice.actualizar(plan['destino'])
        print(json.dumps({'estado': 'plan' if args.dry_run else 'archivos-creados',
                          'id': plan['id'], 'ficha': plan['ficha'], 'creados': creados,
                          'por_crear': list(plan['nuevos']) if args.dry_run else [],
                          'ya_iguales': plan['iguales'], 'avisos': plan['avisos'],
                          'indice_principal': resultado_indice,
                          'pendiente': 'Enlazar el Panel y verificar la configuración completa.'}, ensure_ascii=False))
        return 0
    except (OSError, ValueError, KeyboardInterrupt) as error:
        print(json.dumps({'estado': 'parcial' if intento_aplicar else 'bloqueado',
                          'creados': creados, 'error': str(error),
                          'pendiente': 'Releer antes de reintentar; no reemplazar archivos diferentes.'}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
