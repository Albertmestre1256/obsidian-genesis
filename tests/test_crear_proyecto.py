"""Creación real, invariantes de datos y conservación al reintentar."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

RAIZ = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('crear_proyecto', RAIZ / 'crear_proyecto.py')
crear = importlib.util.module_from_spec(spec)
spec.loader.exec_module(crear)


@pytest.fixture
def vault(tmp_path):
    target = tmp_path / 'Mi bóveda'
    shutil.copytree(RAIZ / '00_CORE', target / '00_CORE', ignore=shutil.ignore_patterns('__pycache__'))
    (target / '.obsidian').mkdir()
    (target / '.obsidian/app.json').write_bytes(b'{"personal":true}')
    (target / 'Panel.md').write_bytes(b'Mi panel\r\n')
    (target / 'nota privada.md').write_bytes(b'Mi contenido original\r\n')
    return target


@pytest.fixture
def datos():
    return {'nombre': 'Preparar dos materias', 'descripcion': 'Organizar el estudio.',
            'objetivo': 'Ordenar qué estudiar, sin fecha definida.', 'contexto': 'D',
            'fecha': '2026-10-07', 'proximo_paso': 'Anotar los temas de las dos materias.'}


def foto(target):
    return {p.relative_to(target).as_posix(): p.read_bytes() for p in target.rglob('*') if p.is_file()}


def test_crea_con_datos_reales_sin_inventar_y_conserva_originales(vault, datos, validador):
    before = foto(vault)
    plan = crear.planificar(vault, datos)
    written = []
    crear.aplicar(plan, written)
    after = foto(vault)
    assert all(after[rel] == contenido for rel, contenido in before.items())
    cell = vault / plan['ficha']
    errors, warnings = validador.validar(cell)
    assert not errors
    assert len(warnings) == 1  # Sin hechos, no se inventan para completar una plantilla.
    text = cell.read_text(encoding='utf-8')
    props, error = validador.leer_propiedades(validador.separar(text)[0], 2)
    assert not error and props['objetivo'] == datos['objetivo']
    assert props['actualizado'] == datos['fecha']
    assert '[completar' not in text and '{{date' not in text
    assert text.count('- [ ] ') == 1
    index = vault / 'preparar-dos-materias/00 - Índice y Contexto.md'
    assert index.is_file() and '[completar' not in index.read_text(encoding='utf-8')
    assert all((index.parent / name).is_dir() for name in crear.SUBCARPETAS)
    assert not (vault / '00_CORE/configuracion.md').exists()


def test_repetir_mismos_datos_no_duplica(vault, datos):
    crear.aplicar(crear.planificar(vault, datos), [])
    before = foto(vault)
    repeated = crear.planificar(vault, datos)
    assert not repeated['nuevos']
    crear.aplicar(repeated, [])
    assert foto(vault) == before


def test_fecha_del_plazo_y_hechos_son_opcionales(vault, datos, validador):
    datos.pop('proximo_paso')
    plan = crear.planificar(vault, datos)
    crear.aplicar(plan, [])
    cell = vault / plan['ficha']
    assert not validador.validar(cell)[0]
    assert '- [ ] ' not in cell.read_text(encoding='utf-8')


def test_comillas_y_dos_puntos_se_conservan_en_propiedades(vault, datos, validador):
    datos.update(nombre='Mi "tesis": planificación', objetivo='Meta: revisar "tres" temas.',
                 hechos=[{'texto': 'Elegí organizar mi estudio.', 'fuente': 'Mensaje del usuario del 07/10/2026'}])
    plan = crear.planificar(vault, datos)
    crear.aplicar(plan, [])
    cell = vault / plan['ficha']
    assert validador.validar(cell) == ([], [])
    props, error = validador.leer_propiedades(validador.separar(cell.read_text(encoding='utf-8'))[0], 2)
    assert not error and props['objetivo'] == datos['objetivo']


@pytest.mark.parametrize('codigo', ['con', 'aux', 'com1', '../otro', 'Proyecto', 'a/b', ''])
def test_identificador_invalido_no_modifica(vault, datos, codigo):
    datos['id'] = codigo
    before = foto(vault)
    with pytest.raises(ValueError):
        crear.planificar(vault, datos)
    assert foto(vault) == before


def test_colision_por_propiedad_en_archivo_con_otro_nombre(vault, datos):
    datos['nombre'] = 'Aprender Python'
    before = foto(vault)
    with pytest.raises(ValueError, match='ya tiene ficha'):
        crear.planificar(vault, datos)
    assert foto(vault) == before


@pytest.mark.parametrize('nombre', ['Estudio.md', 'ESTUDIO.MD'])
def test_ficha_renombrada_sin_sufijo_no_duplica_proyecto(vault, datos, nombre):
    crear.aplicar(crear.planificar(vault, datos), [])
    original = vault / '00_CORE/cells/preparar-dos-materias-context.md'
    original.rename(original.with_name(nombre))
    before = foto(vault)
    with pytest.raises(ValueError, match='ya tiene ficha'):
        crear.planificar(vault, datos)
    assert foto(vault) == before


@pytest.mark.parametrize('newline', [b'\n', b'\r\n'], ids=['LF', 'CRLF'])
def test_mismas_reglas_con_otro_salto_de_linea_no_bloquean(vault, datos, newline):
    path = vault / '00_CORE/atoms/00_vault-rules.md'
    path.write_bytes(path.read_bytes().replace(b'\r\n', b'\n').replace(b'\n', newline))
    before = foto(vault)
    plan = crear.planificar(vault, datos)
    assert plan['id'] == 'preparar-dos-materias'
    assert foto(vault) == before


def test_carpeta_ocupada_no_modifica(vault, datos):
    folder = vault / 'preparar-dos-materias'
    folder.mkdir()
    (folder / 'propio.md').write_bytes(b'Contenido previo')
    before = foto(vault)
    with pytest.raises(ValueError, match='ocupada'):
        crear.planificar(vault, datos)
    assert foto(vault) == before


def test_reintento_no_reemplaza_ficha_editada(vault, datos):
    plan = crear.planificar(vault, datos)
    crear.aplicar(plan, [])
    cell = vault / plan['ficha']
    cell.write_text(cell.read_text(encoding='utf-8') + '\nMi avance nuevo.\n', encoding='utf-8')
    before = foto(vault)
    with pytest.raises(ValueError, match='ya tiene ficha'):
        crear.planificar(vault, datos)
    assert foto(vault) == before


def test_reglas_propias_no_modifica(vault, datos):
    (vault / '00_CORE/atoms/00_vault-rules.md').write_bytes(b'Mis reglas')
    before = foto(vault)
    with pytest.raises(ValueError, match='otras reglas'):
        crear.planificar(vault, datos)
    assert foto(vault) == before


def test_ficha_sin_identificador_no_oculta_posible_coincidencia(vault, datos):
    (vault / '00_CORE/cells/incompleto-context.md').write_bytes(b'---\ntipo: celula\n---\n')
    before = foto(vault)
    with pytest.raises(ValueError, match='falta su identificador'):
        crear.planificar(vault, datos)
    assert foto(vault) == before


def test_cambio_despues_del_plan_se_conserva(vault, datos):
    plan = crear.planificar(vault, datos)
    index = vault / 'preparar-dos-materias/00 - Índice y Contexto.md'
    index.parent.mkdir()
    index.write_bytes(b'Creado por otra persona')
    before = foto(vault)
    with pytest.raises(FileExistsError):
        crear.aplicar(plan, [])
    assert foto(vault) == before


def test_interrupcion_y_reanudacion_conserva_archivos_completos(vault, datos, monkeypatch):
    original = os.link
    calls = []

    def interrupted(source, target, *args, **kwargs):
        calls.append(target)
        if len(calls) == 2:
            raise KeyboardInterrupt()
        return original(source, target, *args, **kwargs)

    before = foto(vault)
    plan = crear.planificar(vault, datos)
    written = []
    with monkeypatch.context() as patched:
        patched.setattr(os, 'link', interrupted)
        with pytest.raises(KeyboardInterrupt):
            crear.aplicar(plan, written)
    assert len(written) == 1
    crear.aplicar(crear.planificar(vault, datos), [])
    after = foto(vault)
    assert all(after[rel] == content for rel, content in before.items())
    assert all((vault / rel).read_bytes() == content for rel, content in plan['nuevos'].items())


def test_dry_run_cli_no_cambia_boveda(vault, datos, tmp_path):
    payload = tmp_path / 'respuestas.json'
    payload.write_text(json.dumps(datos), encoding='utf-8')
    before = foto(vault)
    result = subprocess.run([sys.executable, str(RAIZ / 'crear_proyecto.py'), '--destino', str(vault),
                             '--datos', str(payload), '--dry-run'], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr
    report = json.loads(result.stdout)
    assert report['estado'] == 'plan' and report['por_crear'] and not report['creados']
    assert foto(vault) == before


@pytest.mark.skipif(os.name != 'nt', reason='Junctions de Windows')
def test_junction_no_escribe_fuera(vault, datos, tmp_path):
    outside = tmp_path / 'externo'
    outside.mkdir()
    junction = vault / 'preparar-dos-materias'
    result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(junction), str(outside)], capture_output=True)
    assert result.returncode == 0
    try:
        with pytest.raises(ValueError, match='junction'):
            crear.planificar(vault, datos)
        assert foto(outside) == {}
    finally:
        os.rmdir(str(junction))


@pytest.mark.parametrize('template', ['# Ficha sin propiedades\n', '---\ntipo: celula\n'])
def test_plantilla_danada_informa_bloqueo_sin_traceback(vault, datos, tmp_path, monkeypatch, capsys, template):
    kit = tmp_path/'kit'
    shutil.copytree(RAIZ/'00_CORE', kit/'00_CORE', ignore=shutil.ignore_patterns('__pycache__'))
    (kit/'00_CORE/cells/TEMPLATE_cell.md').write_text(template, encoding='utf-8')
    original = crear.planificar
    monkeypatch.setattr(crear, 'planificar', lambda destino, data: original(destino, data, origen=kit))
    payload = tmp_path/'datos.json'
    payload.write_text(json.dumps(datos), encoding='utf-8')
    before = foto(vault)
    assert crear.main(['--destino', str(vault), '--datos', str(payload)]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report['estado'] == 'bloqueado' and not report['creados']
    assert 'plantilla' in report['error'].lower() and 'propiedades' in report['error']
    assert 'antes de' in report['error']
    assert foto(vault) == before


def test_retoma_archivos_creados_si_falla_mapa_sin_repetir_perfil(vault, datos, tmp_path, monkeypatch, capsys, validador):
    # El inventario y el perfil pertenecen al usuario; crear un proyecto no los rellena.
    config = vault/'00_CORE/configuracion.md'
    config.write_text('---\nestado: parcial\npersonalizacion: abierta\n---\n# Configuración\n'
                      '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n'
                      '|---|---|---|---|---|---|\n'
                      '| documento-perfil | boveda | omitido | Prefiero no compartir | Usuario | — |\n'
                      '| plazo | proyecto:preparar-dos-materias | confirmado | Sin fecha | Usuario | — |\n', encoding='utf-8')
    datos.pop('proximo_paso')
    datos['autor'] = 'IA de prueba (fixture de recuperación)'
    payload = tmp_path/'datos.json'
    payload.write_text(json.dumps(datos), encoding='utf-8')
    before = foto(vault)
    index = crear.indexador()
    def fail(*args):
        raise OSError('Mapa ocupado durante la prueba')
    with monkeypatch.context() as patch:
        patch.setattr(index, 'actualizar', fail)
        patch.setattr(crear, 'indexador', lambda: index)
        assert crear.main(['--destino', str(vault), '--datos', str(payload)]) == 1
    partial = json.loads(capsys.readouterr().out)
    assert partial['estado'] == 'parcial' and partial['creados']
    completed = {p:(vault/p).read_bytes() for p in partial['creados']}
    assert all(foto(vault)[p] == raw for p,raw in before.items())
    assert crear.main(['--destino', str(vault), '--datos', str(payload)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result['estado'] == 'archivos-creados' and not result['creados']
    assert set(result['ya_iguales']) == set(partial['creados'])
    assert result['indice_principal']['estado'] == 'actualizado'
    assert all(foto(vault)[p] == raw for p,raw in before.items())
    assert (vault/result['ficha']).read_bytes() == completed[result['ficha']]
    errors, warnings = validador.validar(vault/result['ficha'])
    assert not errors and any('no bloquea' in w for w in warnings)
    assert crear.indexador().actualizar(vault, comprobar=True)['estado'] == 'vigente'
    assert crear.lineador().main(['check', str(vault/result['ficha']),
                                 str(vault/'preparar-dos-materias/00 - Índice y Contexto.md')]) == 0
