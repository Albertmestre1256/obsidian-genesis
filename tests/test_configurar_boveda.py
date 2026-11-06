"""Ruta corta de configuración: un comando deja la bóveda lista y verificada."""
import json
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

RAIZ = Path(__file__).resolve().parent.parent
IGNORAR = shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache', 'node_modules')


@pytest.fixture
def kit(tmp_path):
    destino = tmp_path / 'Mi bóveda'
    shutil.copytree(RAIZ, destino, ignore=IGNORAR)
    return destino


def datos_base(**extra):
    datos = {'nombre': 'Estudio de astronomía', 'objetivo': 'Entender las bases y guardar resúmenes.',
             'ia': 'Prueba', 'herramienta': 'pytest', 'fecha': '2026-11-05',
             'respuestas': {'presentacion': {'estado': 'omitido'}, 'plazo': {'estado': 'no-aplica', 'dato': 'Sin fecha'}}}
    datos.update(extra)
    return datos


def correr(kit, tmp_path, datos, *extra):
    archivo = tmp_path / 'datos.json'
    archivo.write_text(json.dumps(datos, ensure_ascii=False), encoding='utf-8')
    proceso = subprocess.run([sys.executable, str(kit / 'configurar_boveda.py'), '--destino', str(kit),
                              '--datos', str(archivo)] + list(extra),
                             capture_output=True, text=True, encoding='utf-8')
    return proceso.returncode, json.loads(proceso.stdout)


def test_configura_y_cierra_verificado(kit, tmp_path):
    codigo, salida = correr(kit, tmp_path, datos_base())
    assert codigo == 0, salida
    assert salida['estado'] == 'CIERRE VERIFICADO'
    config = (kit / '00_CORE/configuracion.md').read_text(encoding='utf-8')
    assert 'estado: lista' in config and '[completar' not in config
    assert 'Última operación de mantenimiento: config-estudio-de-astronomia-final' in config
    assert '| presentacion | boveda | omitido |' in config
    assert (kit / salida['ficha']).is_file() and (kit / salida['indice_proyecto']).is_file()
    panel = (kit / 'Panel.md').read_text(encoding='utf-8')
    assert 'Para empezar' not in panel and 'Bienvenida' in panel and 'seguí con Estudio de astronomía' in panel
    assert '@INDICE.md' in (kit / 'CLAUDE.md').read_text(encoding='utf-8')
    assert (kit / '00_CORE/logs/registro-cambios.md').is_file()
    # Nada se retira: solo se proponen candidatos.
    assert (kit / 'tests').is_dir() and 'tests/test_kit.py' in salida['retiro_candidatos_habituales']


def test_el_resultado_pasa_los_validadores_del_kit(kit, tmp_path):
    codigo, _ = correr(kit, tmp_path, datos_base())
    assert codigo == 0
    comandos = [[kit / '00_CORE/schemas/validate.py', kit],
                [kit / 'actualizar_indice.py', kit, '--comprobar'],
                [kit / '00_CORE/schemas/note_index.py', 'check', '--vault', kit]]
    for comando in comandos:
        proceso = subprocess.run([sys.executable] + [str(c) for c in comando], capture_output=True, text=True,
                                 encoding='utf-8')
        assert proceso.returncode == 0, proceso.stdout + proceso.stderr


def test_simulacion_no_escribe(kit, tmp_path):
    codigo, salida = correr(kit, tmp_path, datos_base(), '--dry-run')
    assert codigo == 0 and salida['estado'] == 'plan'
    assert not (kit / '00_CORE/configuracion.md').exists()
    assert not (kit / 'estudio-de-astronomia').exists()


def test_rechaza_bovedas_ya_configuradas(kit, tmp_path):
    assert correr(kit, tmp_path, datos_base())[0] == 0
    codigo, salida = correr(kit, tmp_path, datos_base(nombre='Otro proyecto'))
    assert codigo == 1 and salida['estado'] == 'bloqueado' and 'configuracion.md' in salida['error']
    assert not (kit / 'otro-proyecto').exists()


@pytest.mark.parametrize('cambio, texto', [
    ({'ia': ''}, 'ia'),
    ({'objetivo': 'dos\nlíneas'}, 'una sola línea'),
    ({'id': 'Mal Id'}, 'identificador'),
    ({'fecha': '5/11/2026'}, 'AAAA-MM-DD'),
    ({'respuestas': {'inventado': {'estado': 'omitido'}}}, 'desconocido'),
    ({'respuestas': {'plazo': {'estado': 'quizás'}}}, 'estado'),
])
def test_datos_invalidos_bloquean_sin_escribir(kit, tmp_path, cambio, texto):
    codigo, salida = correr(kit, tmp_path, datos_base(**cambio))
    assert codigo == 1 and salida['estado'] == 'bloqueado' and texto in salida['error']
    assert not (kit / '00_CORE/configuracion.md').exists()
    assert not (kit / '00_CORE/logs').exists()


def test_barra_vertical_en_respuestas_no_rompe_la_tabla(kit, tmp_path):
    datos = datos_base(respuestas={'rutina': {'estado': 'confirmado', 'dato': 'Lunes | miércoles'}})
    codigo, salida = correr(kit, tmp_path, datos)
    assert codigo == 0, salida
    config = (kit / '00_CORE/configuracion.md').read_text(encoding='utf-8')
    assert 'Lunes \\| miércoles' in config
