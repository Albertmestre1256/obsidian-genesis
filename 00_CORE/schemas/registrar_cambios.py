#!/usr/bin/env python3
"""Registro identificado, reanudable y con períodos de cinco días. Python 3.8+."""
import argparse
from datetime import datetime, timedelta
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import sys

spec = importlib.util.spec_from_file_location('lineas_kit', Path(__file__).with_name('note_index.py'))
lineas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(lineas)
REGISTRO = '00_CORE/logs/registro-cambios.md'
ARCHIVO = '00_CORE/logs/historial'
MARCA = re.compile(r'^%% cambio: (.+) %%$', re.M)
ACCIONES = {'crear', 'editar', 'mover', 'renombrar', 'archivar', 'borrar'}


def texto(value, campo):
    if not isinstance(value, str) or not value.strip() or len(value) > 500 or any(ord(c) < 32 for c in value):
        raise ValueError(campo + ' debe contener texto breve en una línea.')
    return value.strip()


def relativa(value):
    value = texto(value, 'ruta')
    parts = value.split('/')
    if '\\' in value or ':' in value or any(p in {'', '.', '..'} or (p.startswith('.') and p not in {'.obsidian', '.claude', '.opencode', '.github'}) for p in parts):
        raise ValueError('Usá una ruta relativa portable, sin partes ocultas ni escapes: ' + value)
    return value


def momento(value):
    if not isinstance(value, str):
        raise ValueError('La fecha debe ser texto ISO con zona horaria explícita.')
    result = datetime.fromisoformat(value[:-1] + '+00:00' if value.endswith('Z') else value)
    if result.tzinfo is None:
        raise ValueError('La fecha necesita zona horaria explícita.')
    return result


def entradas(raw):
    text = raw.decode('utf-8-sig')
    head, _ = lineas.separar(text)
    if not head or head[0].strip() != '---':
        raise ValueError('Registro propio sin propiedades: se conserva.')
    properties = ''.join(head[1:-1])
    starts = re.findall(r'^inicio: "([^"]+)"\r?$', properties, re.M)
    types = re.findall(r'^tipo: (.+?)\r?$', properties, re.M)
    if (len(starts) != 1 or types != ['registro-cambios']
            or len(re.findall(r'^inicio:', properties, re.M)) != 1):
        raise ValueError('Registro incompatible: no se reemplaza.')
    # No descartar silenciosamente una entrada dañada al rotar.
    marked = [line for line in text.splitlines() if line.startswith('%% cambio:')]
    found = MARCA.findall(text.replace('\r\n', '\n'))
    if len(marked) != len(found):
        raise ValueError('Entrada de registro incompleta; releer antes de continuar.')
    data = [json.loads(s) for s in found]
    if any(not isinstance(e, dict) or not e.get('id') for e in data):
        raise ValueError('Entrada de registro inválida; se conserva.')
    for entry in data:
        evento(None, entry, comprobar=False)  # Validar estructura sin releer notas históricas.
        momento(entry.get('fecha'))
    return momento(starts[0]), data


def evento(root, data, comprobar=True):
    if not isinstance(data, dict):
        raise ValueError('El evento debe ser un objeto JSON.')
    result = {'id': texto(data.get('id'), 'id')}
    if not re.fullmatch(r'[a-zA-Z0-9_-]{1,80}', result['id']):
        raise ValueError('El id debe ser estable, corto y sin espacios para reintentar.')
    result['ia'] = texto(data.get('ia'), 'ia')
    result['herramienta'] = texto(data.get('herramienta'), 'herramienta')
    if data.get('modelo'):
        result['modelo'] = texto(data['modelo'], 'modelo')
    result['resumen'] = texto(data.get('resumen'), 'resumen')
    if type(data.get('verificado')) is not bool:
        raise ValueError('verificado debe ser true o false; no inventar comprobaciones.')
    result['verificado'] = data['verificado']
    changes = data.get('cambios')
    if not isinstance(changes, list) or not changes:
        raise ValueError('cambios debe incluir los archivos efectivamente cambiados.')
    result['cambios'] = []
    for change in changes:
        if not isinstance(change, dict) or change.get('accion') not in ACCIONES:
            raise ValueError('Acción de cambio no reconocida.')
        item = {'accion': change['accion'], 'ruta': relativa(change.get('ruta'))}
        if item['ruta'] == REGISTRO or item['ruta'].startswith(ARCHIVO + '/'):
            raise ValueError('No registrar el propio registro como un cambio recursivo.')
        path = lineas.ruta_real(root / item['ruta']) if root is not None else None
        if comprobar and item['accion'] == 'borrar' and path.exists():
            raise ValueError('El archivo declarado como borrado sigue presente: ' + item['ruta'])
        if comprobar and item['accion'] != 'borrar':
            if not path.is_file():
                raise ValueError('No existe el resultado del cambio: ' + item['ruta'])
            item['sha256'] = hashlib.sha256(path.read_bytes()).hexdigest()
        if item['accion'] in {'mover', 'renombrar', 'archivar'}:
            item['desde'] = relativa(change.get('desde'))
            if root is not None:
                lineas.ruta_real(root / item['desde'])
        result['cambios'].append(item)
    return result


def _registrar(root, data, fecha=None, dry_run=False):
    root = lineas.ruta_real(root)
    if not root.is_dir():
        raise ValueError('La bóveda debe existir.')
    now = momento(fecha) if fecha else datetime.now().astimezone()
    event = evento(root, data, comprobar=False)
    path = lineas.ruta_real(root / REGISTRO)
    before = path.read_bytes() if path.exists() else None
    start, current = entradas(before) if before is not None else (now, [])
    history = lineas.ruta_real(root / ARCHIVO)
    logs = [current]
    if history.exists():
        for archived in sorted(history.glob('*.md')):
            _, previous = entradas(lineas.ruta_real(archived).read_bytes())
            logs.append(previous)
    for group in logs:
        for entry in group:
            if entry.get('id') != event['id']:
                continue
            # Comparar la operación declarada, no el estado futuro de sus notas.
            declared = {k:v for k,v in entry.items() if k != 'fecha'}
            declared['cambios'] = [{k:v for k,v in c.items() if k != 'sha256'} for c in entry.get('cambios', [])]
            if declared != event:
                raise ValueError('El id ya tiene otro contenido; releer, no duplicar.')
            return {'estado': 'ya-registrado', 'registro': REGISTRO, 'rotado': False}
    event = evento(root, data)
    if now < start:
        raise ValueError('La fecha es anterior al período activo; no se rota.')
    rotate = before is not None and now - start >= timedelta(days=5)
    archived = None
    if rotate:
        digest = hashlib.sha256(before).hexdigest()[:12]
        archived = lineas.ruta_real(history / (start.strftime('%Y%m%d-%H%M%S') + '-' + digest + '.md'))
        if archived.exists() and archived.read_bytes() != before:
            raise ValueError('El archivo histórico difiere; se conserva todo.')
        start = now
    if rotate or before is None:
        base = '---\ntipo: registro-cambios\ninicio: "{}"\n---\n\n# Registro de cambios\n\nPeríodo de cinco días desde inicio; editar no reinicia el plazo. Historial en `historial/`.\n'.format(start.isoformat())
    else:
        base = lineas.sin_indice(before.decode('utf-8-sig'))
    event['fecha'] = now.isoformat()
    author = 'IA:{} ({})'.format(event['ia'], ', '.join([event['herramienta']] + ([event['modelo']] if 'modelo' in event else [])))
    esc = lambda s: s.replace('|', '\\|').replace('<', '&lt;').replace('>', '&gt;')
    added = '\n## {} · {}\n\nAutor: {}. Verificado: {}.\n\n{}\n\n| Acción | Ruta | Desde | SHA-256 del resultado |\n|---|---|---|---|\n'.format(event['fecha'], event['id'], esc(author), 'sí' if event['verificado'] else 'no', esc(event['resumen']))
    for change in event['cambios']:
        added += '| {} | {} | {} | {} |\n'.format(change['accion'], esc(change['ruta']), esc(change.get('desde', '')), change.get('sha256', 'archivo eliminado; no es un hash comprobado'))
    added += '\n%% cambio: ' + json.dumps(event, ensure_ascii=False, sort_keys=True) + ' %%\n'
    after = lineas.contenido((base.rstrip() + '\n' + added).encode('utf-8'))
    if not rotate and before and before.startswith(b'\xef\xbb\xbf'):
        after = b'\xef\xbb\xbf' + after
    if not dry_run:
        if archived is not None and not archived.exists():
            # Archivar primero; un fallo posterior puede reintentarse sin perder el activo.
            lineas.guardar(archived, None, before)
        lineas.guardar(path, before, after)
    return {'estado': 'plan' if dry_run else 'registrado', 'registro': REGISTRO,
            'rotado': rotate, 'archivo': archived.relative_to(root).as_posix() if archived else None}


def registrar(root, data, fecha=None, dry_run=False):
    if dry_run:
        return _registrar(root, data, fecha, True)
    root = lineas.ruta_real(root)
    if not root.is_dir():
        raise ValueError('La bóveda debe existir.')
    # Comprobar el plan antes de crear carpetas; repetir bajo bloqueo para guardar.
    plan = _registrar(root, data, fecha, True)
    if plan['estado'] == 'ya-registrado':
        return plan
    lock = lineas.ruta_real(root / '00_CORE/logs/.registro-cambios.lock')
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        with lock.open('xb') as stream:
            identity = os.fstat(stream.fileno())
    except FileExistsError:
        raise ValueError('Otro registro está en curso; releer y reintentar después. No retirar su bloqueo.')
    try:
        return _registrar(root, data, fecha)
    finally:
        if os.path.samestat(identity, lineas.ruta_real(lock).lstat()):
            lock.unlink()


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', required=True)
    parser.add_argument('--datos', required=True, help='JSON del evento, preparado por la IA')
    parser.add_argument('--fecha', help='Fecha ISO con zona; por defecto la zona local del equipo')
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args(argv)
    try:
        data = json.loads(Path(args.datos).read_text(encoding='utf-8-sig'))
        print(json.dumps(registrar(Path(args.destino), data, args.fecha, args.dry_run), ensure_ascii=False))
        return 0
    except (OSError, ValueError) as error:
        print(json.dumps({'estado': 'pendiente', 'error': str(error), 'releer_antes_de_reintentar': True}, ensure_ascii=False))
        return 2


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
