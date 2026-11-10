#!/usr/bin/env python3
"""Configura una bóveda nueva en un solo paso: proyecto, configuración, Panel y cierre verificado.

Es la ruta corta del protocolo: la IA pregunta, escribe un JSON y ejecuta este script. Reúne lo que antes eran
la creación del proyecto, la nota de configuración, la adaptación del Panel y las dos operaciones de cierre
(parcial y final). Python estándar 3.8+; reutiliza las herramientas del kit y no agrega dependencias.
"""
import argparse
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

sys.dont_write_bytecode = True  # no dejar __pycache__ dentro de la bóveda
RAIZ = Path(__file__).resolve().parent
sys.path.insert(0, str(RAIZ))
import crear_proyecto as creador  # noqa: E402

ESTADOS = ('confirmado', 'pendiente', 'omitido', 'no-aplica')
ITEMS_BOVEDA = ('uso', 'destino', 'conservacion', 'presentacion', 'documento-perfil', 'alcance', 'vida-util',
                'rutina', 'preferencias')
ITEMS_PROYECTO = ('objetivo', 'formacion', 'experiencia', 'materiales', 'plazo', 'primer-paso')
ORDEN = ('uso', 'destino', 'conservacion', 'objetivo', 'presentacion', 'documento-perfil', 'formacion',
         'experiencia', 'alcance', 'vida-util', 'materiales', 'rutina', 'preferencias', 'plazo', 'primer-paso')
# Candidatos habituales a retirar de una bóveda lista (se contrastan con el kit original antes de borrar).
CANDIDATOS_RETIRO = ('CONTRIBUTING.md', 'README.en.md', 'README.de.md', 'README.zh.md', 'DOCS/README.md',
                     'DOCS/README.en.md', 'DOCS/README.de.md', 'DOCS/README.zh.md', 'DOCS/publicacion.md',
                     'DOCS/prueba-con-usuarios.md')
CARPETAS_RETIRO = ('tests', '.github')


class Bloqueo(Exception):
    """Fallo con mensaje claro para la persona o la IA."""


def escribir(ruta, texto):
    """Escribe con saltos LF; Path.write_text no admite newline antes de Python 3.10."""
    with open(str(ruta), 'w', encoding='utf-8', newline='\n') as archivo:
        archivo.write(texto)


def linea(valor, campo, opcional=False):
    try:
        return creador.texto_linea(valor, campo, opcional)
    except ValueError as error:
        raise Bloqueo(str(error))


def celda(texto):
    return str(texto).replace('|', '\\|')


def fecha_hoy():
    return datetime.now().astimezone().strftime('%Y-%m-%d')


def validar_datos(datos, destino):
    if not isinstance(datos, dict):
        raise Bloqueo('El JSON debe ser un objeto.')
    nombre = linea(datos.get('nombre'), 'nombre')
    objetivo = linea(datos.get('objetivo'), 'objetivo')
    descripcion = linea(datos.get('descripcion') or objetivo, 'descripcion')
    ia = linea(datos.get('ia'), 'ia')
    herramienta = linea(datos.get('herramienta') or 'scripts del kit', 'herramienta')
    modelo = linea(datos.get('modelo'), 'modelo', opcional=True)
    try:
        codigo = creador.comprobar_id(datos.get('id') or creador.identificador(nombre))
    except ValueError as error:
        raise Bloqueo(str(error))
    fecha = linea(datos.get('fecha') or fecha_hoy(), 'fecha')
    if not re.fullmatch(r'\d{4}-\d{2}-\d{2}', fecha):
        raise Bloqueo('fecha debe tener la forma AAAA-MM-DD.')
    respuestas = datos.get('respuestas') or {}
    if not isinstance(respuestas, dict):
        raise Bloqueo('respuestas debe ser un objeto con un ítem por clave.')
    for item, valor in respuestas.items():
        if item not in ORDEN:
            raise Bloqueo('Ítem de inventario desconocido: {}.'.format(item))
        if not isinstance(valor, dict) or valor.get('estado') not in ESTADOS:
            raise Bloqueo('«{}» necesita un estado entre: {}.'.format(item, ', '.join(ESTADOS)))
        for campo in ('dato', 'retomar'):
            linea(valor.get(campo), '{}.{}'.format(item, campo), opcional=True)
    if (destino / '00_CORE' / 'configuracion.md').exists():
        raise Bloqueo('Ya existe 00_CORE/configuracion.md: esta ruta es solo para bóvedas sin configurar. '
                      'Para retomar seguí 00_CORE/protocols/configurar-vault.md y personalizar-vault.md.')
    return {'nombre': nombre, 'id': codigo, 'objetivo': objetivo, 'descripcion': descripcion, 'ia': ia,
            'herramienta': herramienta, 'modelo': modelo, 'fecha': fecha, 'respuestas': respuestas}


def datos_creador(datos, original):
    salida = {'nombre': datos['nombre'], 'id': datos['id'], 'descripcion': datos['descripcion'],
              'objetivo': datos['objetivo'], 'contexto': original.get('contexto', 'D'),
              'autor': 'IA:{} ({}{})'.format(datos['ia'], datos['herramienta'],
                                              ', ' + datos['modelo'] if datos['modelo'] else ''),
              'fecha': datos['fecha']}
    for clave in ('proximo_paso', 'hechos'):
        if original.get(clave):
            salida[clave] = original[clave]
    return salida


def ejecutar(args, paso):
    """Corre una herramienta del kit y devuelve su salida; ante un fallo, detiene con el paso y el motivo."""
    proceso = subprocess.run([sys.executable] + [str(a) for a in args], capture_output=True, text=True,
                             encoding='utf-8', errors='replace')
    salida = (proceso.stdout or '') + (proceso.stderr or '')
    if proceso.returncode != 0:
        raise Bloqueo('{} falló: {}'.format(paso, salida.strip()[-800:] or 'sin mensaje'))
    return salida


def inventario(datos, proximo_paso):
    cod, fecha = datos['id'], datos['fecha']
    base = {
        'uso': ('confirmado', datos['descripcion'], '—'),
        'destino': ('confirmado', 'Carpeta acordada con la persona; lectura y escritura comprobadas', '—'),
        'conservacion': ('confirmado', 'Empieza de cero, sin notas previas', '—'),
        'objetivo': ('confirmado', datos['objetivo'], '—'),
        'primer-paso': ('confirmado', proximo_paso, '—') if proximo_paso else
                       ('pendiente', '—', 'Cuando quiera, elegir el primer paso; no guardar una propuesta como tarea aceptada'),
    }
    filas = []
    for item in ORDEN:
        estado, dato, retomar = base.get(item, ('pendiente', '—', 'Preguntar cuando corresponda'))
        extra = datos['respuestas'].get(item)
        if extra:
            estado = extra['estado']
            dato = extra.get('dato') or ('Dejado para después' if estado == 'omitido' else '—')
            retomar = extra.get('retomar') or ('Retomar solo si la persona lo pide' if estado == 'omitido' else '—')
        origen = '—' if estado == 'pendiente' and item not in base else 'Usuario, {}'.format(fecha)
        alcance = 'proyecto:' + cod if item in ITEMS_PROYECTO else 'boveda'
        filas.append('> | {} | {} | {} | {} | {} | {} |'.format(item, alcance, estado, celda(dato), origen, celda(retomar)))
    return filas


def construir_configuracion(datos, proximo_paso, ficha, indice_proyecto):
    texto = (RAIZ / '00_CORE' / 'templates' / 'TEMPLATE_configuracion.md').read_text(encoding='utf-8')
    cod = datos['id']
    cabecera = {'tipo: plantilla-configuracion': 'tipo: configuracion',
                'descripcion: Punto de partida e inventario reanudable de una bóveda, sin datos personales.':
                    'descripcion: {}'.format(json.dumps('Punto de partida e inventario reanudable de la bóveda «{}».'.format(
                        datos['nombre']), ensure_ascii=False)),
                'fecha: ""': 'fecha: "{}"'.format(datos['fecha'])}
    for viejo, nuevo in cabecera.items():
        if viejo not in texto:
            raise Bloqueo('La plantilla de configuración cambió: falta «{}».'.format(viejo))
        texto = texto.replace(viejo, nuevo, 1)
    salida = []
    en_inventario = False
    for fila in texto.splitlines():
        if fila.startswith('- Nombre:'):
            fila = '- Nombre: ' + datos['nombre']
        elif fila.startswith('- Identificador:'):
            fila = '- Identificador: ' + cod
        elif fila.startswith('- Objetivo:'):
            fila = '- Objetivo: ' + datos['objetivo']
        elif fila.startswith('- Ficha e índice:'):
            fila = '- Ficha e índice: [[{}|Ficha]] · [[{}|Índice del proyecto]]'.format(
                ficha[:-3], indice_proyecto[:-3])
        elif fila.startswith('- Preparado y comprobado:'):
            fila = '- Preparado y comprobado: Configuración e inventario guardados; proyecto creado (ficha, índice y carpetas); Panel adaptado ({}).'.format(datos['fecha'])
        elif fila.startswith('- Pendiente o impedido:'):
            fila = '- Pendiente o impedido: Cierre final en curso.'
        elif fila.startswith('- Última operación de mantenimiento:'):
            fila = '- Última operación de mantenimiento: ' + datos['op_parcial']
        elif fila.startswith('> | ') and not fila.startswith('> | Ítem') and not fila.startswith('> |---'):
            if not en_inventario:
                salida.extend(inventario(datos, proximo_paso))
                en_inventario = True
            continue
        salida.append(fila)
    resultado = '\n'.join(salida) + '\n'
    if '[completar' in resultado:
        raise Bloqueo('Quedaron marcadores [completar…] en la configuración.')
    return resultado


def reemplazar(texto, viejo, nuevo, archivo):
    if viejo not in texto:
        raise Bloqueo('No se pudo adaptar {}: el texto esperado cambió ({}).'.format(archivo, viejo[:50]))
    return texto.replace(viejo, nuevo, 1)


def adaptar_panel(destino, datos, ficha, indice_proyecto):
    ruta = destino / 'Panel.md'
    texto = ruta.read_text(encoding='utf-8')
    alias = re.sub(r'[\[\]|#^]', '', datos['nombre'])
    nuevo = ('**Bienvenida:** tu bóveda está preparada. Abrí [[{}|la ficha de {}]] o [[{}|el índice del proyecto]]. '
             'Lo que falta por completar está en [[00_CORE/configuracion.md#Inventario de personalización|el inventario de personalización]].'
             '\n\nPara retomar, pedí «seguí con {}».').format(ficha[:-3], alias, indice_proyecto[:-3], alias)
    inicio = texto.index('**Para empezar:**') if '**Para empezar:**' in texto else -1
    fin = texto.index('pedí «seguí con [proyecto]».') + len('pedí «seguí con [proyecto]».') if 'pedí «seguí con [proyecto]».' in texto else -1
    if inicio < 0 or fin < 0 or fin < inicio:
        raise Bloqueo('No se pudo adaptar Panel.md: el aviso inicial cambió. Adaptalo a mano según configurar-vault.md.')
    texto = texto[:inicio] + nuevo + texto[fin:]
    texto = reemplazar(texto, 'Abrí la ficha original para completar una tarea.',
                       'Tus tareas aparecen en Acciones pendientes; si no hay ninguna, pedí «seguí con {}» para elegir la próxima. '
                       'Abrí la ficha original para completar una tarea.'.format(alias), 'Panel.md')
    escribir(ruta, texto)


def activar_indice_en_claude(destino):
    """Con la bóveda configurada, Claude Code vuelve a cargar INDICE.md al iniciar."""
    ruta = destino / 'CLAUDE.md'
    if not ruta.is_file():
        return False
    texto = ruta.read_text(encoding='utf-8')
    if '@INDICE.md' in texto or '@AGENTS.md' not in texto:
        return False
    escribir(ruta, texto.replace('@AGENTS.md', '@INDICE.md\n@AGENTS.md', 1))
    return True


def fijar(texto, etiqueta, valor):
    patron = re.compile(r'^(- {}:).*$'.format(re.escape(etiqueta)), re.M)
    if not patron.search(texto):
        raise Bloqueo('Falta «{}» en la configuración.'.format(etiqueta))
    return patron.sub(lambda m: '{} {}'.format(m.group(1), valor), texto, count=1)


def candidatos_retiro(destino):
    rutas = [r for r in CANDIDATOS_RETIRO if (destino / r).is_file()]
    for carpeta in CARPETAS_RETIRO:
        base = destino / carpeta
        if base.is_dir() and not base.is_symlink():
            rutas += sorted(p.relative_to(destino).as_posix() for p in base.rglob('*')
                            if p.is_file() and '__pycache__' not in p.parts and '.pytest_cache' not in p.parts)
    return rutas


def configurar(destino, datos_crudos, dry_run=False):
    datos = validar_datos(datos_crudos, destino)
    cod = datos['id']
    datos['op_parcial'] = 'config-{}-parcial'.format(cod)
    datos['op_final'] = 'config-{}-final'.format(cod)
    proximo_paso = linea(datos_crudos.get('proximo_paso'), 'proximo_paso', opcional=True)
    with tempfile.TemporaryDirectory(prefix='genesis-') as tmp:
        json_creador = Path(tmp) / 'proyecto.json'
        json_creador.write_text(json.dumps(datos_creador(datos, datos_crudos), ensure_ascii=False), encoding='utf-8')
        comando = [RAIZ / 'crear_proyecto.py', '--destino', destino, '--datos', json_creador]
        if dry_run:
            salida = ejecutar(comando + ['--dry-run'], 'La simulación del proyecto')
            return {'estado': 'plan', 'id': cod, 'creador': json.loads(salida)}
        creado = json.loads(ejecutar(comando, 'La creación del proyecto'))
        ficha = creado['ficha']
        indice_proyecto = '{}/{}'.format(cod, creador.nombre_indice_proyecto(cod))
        if not (destino / indice_proyecto).is_file():
            raise Bloqueo('No se encontró el índice del proyecto en {}.'.format(indice_proyecto))
        config = destino / '00_CORE' / 'configuracion.md'
        escribir(config, construir_configuracion(datos, proximo_paso, ficha, indice_proyecto))
        adaptar_panel(destino, datos, ficha, indice_proyecto)
        claude_editado = activar_indice_en_claude(destino)
        herramientas = RAIZ / '00_CORE' / 'schemas'
        notas = [config, destino / 'Panel.md', destino / ficha, destino / indice_proyecto]
        if claude_editado:
            notas.append(destino / 'CLAUDE.md')
        ejecutar([herramientas / 'note_index.py', 'apply'] + notas, 'El cálculo de rangos')
        ejecutar([RAIZ / 'actualizar_indice.py', destino], 'La actualización del índice')
        rutas_nuevas = [r for r in creado.get('creados', []) if r != 'INDICE.md']
        cambios = [{'accion': 'crear', 'ruta': r} for r in rutas_nuevas]
        if '00_CORE/configuracion.md' not in rutas_nuevas:
            cambios.append({'accion': 'crear', 'ruta': '00_CORE/configuracion.md'})
        cambios += [{'accion': 'editar', 'ruta': 'Panel.md'}, {'accion': 'editar', 'ruta': 'INDICE.md'}]
        if claude_editado:
            cambios.append({'accion': 'editar', 'ruta': 'CLAUDE.md'})
        etiquetas = {'ia': datos['ia'], 'herramienta': datos['herramienta']}
        if datos['modelo']:
            etiquetas['modelo'] = datos['modelo']

        def registrar(identificador, resumen, lista):
            evento = dict(etiquetas, id=identificador, resumen=resumen, verificado=True, cambios=lista)
            ruta = Path(tmp) / (identificador + '.json')
            ruta.write_text(json.dumps(evento, ensure_ascii=False), encoding='utf-8')
            ejecutar([herramientas / 'registrar_cambios.py', '--destino', destino, '--datos', ruta], 'El registro de cambios')

        def cerrar(identificador):
            salida = ejecutar([herramientas / 'validate.py', destino, '--cierre', '--operacion', identificador],
                              'El cierre ' + identificador)
            if 'CIERRE VERIFICADO' not in salida:
                raise Bloqueo('El cierre {} no quedó verificado: {}'.format(identificador, salida.strip()[-600:]))
            return salida

        registrar(datos['op_parcial'], 'Configuración parcial: inventario, proyecto {} (ficha, índice y carpetas) y Panel adaptado.'.format(cod), cambios)
        ejecutar([RAIZ / 'actualizar_indice.py', destino], 'La actualización del índice')
        cerrar(datos['op_parcial'])
        texto = config.read_text(encoding='utf-8')
        texto = texto.replace('estado: parcial', 'estado: lista', 1)
        texto = fijar(texto, 'Preparado y comprobado', 'Configuración e inventario guardados; proyecto creado (ficha, índice y carpetas); Panel adaptado; cierre verificado ({}).'.format(datos['fecha']))
        texto = fijar(texto, 'Pendiente o impedido', 'Retiro del material del kit: pendiente de decisión. Prueba visual en Obsidian: pendiente.')
        texto = fijar(texto, 'Última operación de mantenimiento', datos['op_final'])
        escribir(config, texto)
        ejecutar([herramientas / 'note_index.py', 'apply', config], 'El cálculo de rangos')
        registrar(datos['op_final'], 'Configuración marcada como lista tras el cierre parcial verificado; retiro del material del kit pendiente de decisión.',
                  [{'accion': 'editar', 'ruta': '00_CORE/configuracion.md'}])
        ejecutar([RAIZ / 'actualizar_indice.py', destino], 'La actualización del índice')
        cerrar(datos['op_final'])
    return {'estado': 'CIERRE VERIFICADO', 'id': cod, 'ficha': ficha, 'indice_proyecto': indice_proyecto,
            'configuracion': '00_CORE/configuracion.md', 'operaciones': [datos['op_parcial'], datos['op_final']],
            'pendiente': ['Retiro del material del kit: mostrar la lista y pedir la decisión', 'Prueba visual en Obsidian'],
            'retiro_candidatos_habituales': candidatos_retiro(destino),
            'aviso_retiro': 'Son candidatos por nombre, sin contrastar con el kit original. No se retiró nada.'}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--destino', required=True, help='Carpeta que contiene el kit, sin configurar')
    parser.add_argument('--datos', required=True, help='JSON con las respuestas ya acordadas')
    parser.add_argument('--dry-run', action='store_true', help='Simular la creación sin escribir')
    args = parser.parse_args(argv)
    try:
        destino = Path(args.destino).resolve()
        datos = json.loads(Path(args.datos).read_text(encoding='utf-8-sig'))
        resultado = configurar(destino, datos, args.dry_run)
        print(json.dumps(resultado, ensure_ascii=False))
        return 0
    except (Bloqueo, OSError, ValueError, KeyError) as error:
        print(json.dumps({'estado': 'bloqueado', 'error': str(error),
                          'pendiente': 'Releer lo guardado antes de reintentar; no reemplazar archivos diferentes. '
                                       'Guía completa: 00_CORE/protocols/configurar-vault.md'}, ensure_ascii=False))
        return 1


if __name__ == '__main__':
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8')
    sys.exit(main())
