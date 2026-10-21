"""Creación real, invariantes de datos y conservación al reintentar."""
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import unicodedata

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
    # Nuevo formato: 00 - Índice - <id>.md
    index = vault / 'preparar-dos-materias/00 - Índice - preparar-dos-materias.md'
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
    # Simular índice legacy con metadata correcta para probar preservación
    index_dir = vault / 'preparar-dos-materias'
    index_dir.mkdir()
    legacy_index = index_dir / '00 - Índice y Contexto.md'
    legacy_index.write_text('---\ntipo: indice-proyecto\nproyecto: preparar-dos-materias\n---\n# Legacy\n', encoding='utf-8')
    before = foto(vault)
    with pytest.raises(ValueError, match='ya está ocupada'):
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
    (kit/'00_CORE/templates/TEMPLATE_cell.md').write_text(template, encoding='utf-8')
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
        patch.setattr(crear, 'indexador', lambda origen=RAIZ: index)
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
                                  str(vault/'preparar-dos-materias/00 - Índice - preparar-dos-materias.md')]) == 0


# Regresiones de nombres propios de índices — 13/10/2026
import hashlib
import re
from urllib.parse import quote as _nombres_quote
_nombres_maps=crear.indexador(RAIZ)
_nombres_lines=crear.lineador(RAIZ)

def _nombres_foto(v):return {p.relative_to(v).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in v.rglob('*') if p.is_file()}

def _nombres_datos(code='proyecto-uno',title='Proyecto uno'):
    return {'id':code,'nombre':title,'descripcion':'Caso ficticio de nombres propios.','objetivo':'Ordenar apuntes ficticios.','contexto':'D','fecha':'2026-10-13','autor':'IA:ChatGPT (Codex), prueba de archivos'}

def _nombres_crear(v,d):
    crear.aplicar(crear.planificar(v,d,origen=RAIZ),[])
    _nombres_maps.actualizar(v)

def _nombres_indice(v,code):
    records=[r for r in _nombres_maps.catalogo(v) if Path(r['ruta']).parent.as_posix()==code and _nombres_maps.tipo(r['meta']) in ('indice-nodo','indice-proyecto')]
    assert len(records)==1
    return v/records[0]['ruta']

def _nombres_renombrar(v,name,fix_link=True):
    old=_nombres_indice(v,'proyecto-uno');new=old.with_name(name);old.rename(new)
    if fix_link:
        cell=v/'00_CORE/cells/proyecto-uno-context.md';raw=cell.read_bytes();s=raw.decode('utf-8')
        # Tanto wikilinks como un eventual enlace Markdown relativo del creador.
        s=s.replace(old.stem,new.stem).replace(_nombres_quote(old.name),_nombres_quote(new.name))
        assert s!=raw.decode('utf-8') or old.name==new.name
        cell.write_bytes(_nombres_lines.contenido(s.encode('utf-8')))
    _nombres_maps.actualizar(v)
    return new

def test_new_project_names_differ_and_all_links_resolve(vault):
    _nombres_crear(vault,_nombres_datos());_nombres_crear(vault,_nombres_datos('proyecto-dos','Proyecto dos'))
    a=_nombres_indice(vault,'proyecto-uno');b=_nombres_indice(vault,'proyecto-dos')
    assert a.name!=b.name
    assert 'proyecto-uno' in a.name and 'proyecto-dos' in b.name
    assert _nombres_maps.actualizar(vault,comprobar=True)['estado']=='vigente'
    for code,idx in [('proyecto-uno',a),('proyecto-dos',b)]:
        s=(vault/('00_CORE/cells/'+code+'-context.md')).read_text(encoding='utf-8')
        assert code+'/'+idx.stem in s or _nombres_quote(idx.name) in s
        assert idx.is_file()

@pytest.mark.parametrize('name',['00 - Índice y Contexto.md','Guía principal.md'])
def test_legacy_and_named_generated_index_retries_are_byte_idempotent(vault,name):
    _nombres_crear(vault,_nombres_datos());expected=_nombres_renombrar(vault,name)
    before=_nombres_foto(vault);plan=crear.planificar(vault,_nombres_datos(),origen=RAIZ)
    assert not plan['nuevos']
    crear.aplicar(plan,[])
    assert _nombres_foto(vault)==before and _nombres_indice(vault,'proyecto-uno')==expected

def test_stale_ficha_link_does_not_propose_duplicate_or_modify(vault):
    _nombres_crear(vault,_nombres_datos());_nombres_renombrar(vault,'Guía principal.md',fix_link=False)
    before=_nombres_foto(vault)
    with pytest.raises(ValueError):crear.planificar(vault,_nombres_datos(),origen=RAIZ)
    assert _nombres_foto(vault)==before
    assert len(list((vault/'proyecto-uno').glob('00 - Índice*.md')))==0

def test_ambiguous_local_indexes_are_rejected_in_planning(vault):
    _nombres_crear(vault,_nombres_datos())
    other=vault/'proyecto-uno/Otro índice.md'
    other.write_text('---\ntipo: indice-nodo\ndescripcion: Otra entrada local.\n---\n# Otra entrada\n',encoding='utf-8')
    before=_nombres_foto(vault)
    with pytest.raises(ValueError):crear.planificar(vault,_nombres_datos(),origen=RAIZ)
    assert _nombres_foto(vault)==before

def test_human_title_is_not_a_filename(vault):
    _nombres_crear(vault,_nombres_datos(title='Estudio [corazón] | # : ¿ensayo?'))
    idx=_nombres_indice(vault,'proyecto-uno')
    assert not re.search(r'[<>:"/\\|?*]',idx.name)
    assert _nombres_maps.actualizar(vault,comprobar=True)['estado']=='vigente'

def test_handwritten_index_is_not_overwritten_on_retry(vault):
    _nombres_crear(vault,_nombres_datos());idx=_nombres_indice(vault,'proyecto-uno')
    idx.write_bytes(idx.read_bytes()+b'\n## Contenido propio\nNo sobrescribir.\n')
    before=_nombres_foto(vault)
    with pytest.raises(ValueError):crear.planificar(vault,_nombres_datos(),origen=RAIZ)
    assert _nombres_foto(vault)==before

def test_redirected_local_note_is_rejected_before_metadata_read(vault,monkeypatch):
    _nombres_crear(vault,_nombres_datos())
    redirect=vault/'proyecto-uno/Enlace redirigido.md'
    redirect.write_text('# Archivo que debe quedar protegido\n',encoding='utf-8')
    original=crear.ruta_real
    def checked(path):
        if Path(path)==redirect:raise ValueError('ruta redirigida: no leer')
        return original(path)
    monkeypatch.setattr(crear,'ruta_real',checked)
    before=_nombres_foto(vault)
    with pytest.raises(ValueError,match='redirigida'):crear.planificar(vault,_nombres_datos(),origen=RAIZ)
    assert _nombres_foto(vault)==before


def test_nombre_de_indice_nuevo_no_supera_limite_portable():
    with pytest.raises(ValueError,match='demasiado largo'):
        crear.nombre_indice_proyecto('a' * 240)


def test_indice_roto_se_comprueba_antes_de_is_file(vault,monkeypatch):
    _nombres_crear(vault,_nombres_datos())
    bad=vault/'proyecto-uno/Enlace roto.md'
    bad.write_text('# Simulación de enlace roto\n',encoding='utf-8')
    raw=bad.read_bytes()
    original=crear.ruta_real
    original_is_file=type(bad).is_file
    def checked(path):
        if Path(path)==bad:raise ValueError('ruta redirigida: no leer')
        return original(path)
    monkeypatch.setattr(crear,'ruta_real',checked)
    monkeypatch.setattr(type(bad),'is_file',lambda path:False if path==bad else original_is_file(path))
    before=_nombres_foto(vault)
    with pytest.raises(ValueError,match='redirigida'):
        crear.planificar(vault,_nombres_datos(),origen=RAIZ)
    assert _nombres_foto(vault)==before and bad.read_bytes()==raw



def test_destino_planificado_creado_por_otro_editor_se_conserva(vault,datos):
    plan=crear.planificar(vault,datos)
    target=vault/plan['indice']
    target.parent.mkdir()
    target.write_bytes(b'# Contenido ajeno posterior al plan\n')
    before=foto(vault)
    with pytest.raises(FileExistsError):
        crear.aplicar(plan,[])
    assert foto(vault)==before


@pytest.fixture
def _contexto_conservacion(vault, datos):
    return crear, vault, dict(datos, id="estudio-ficticio", autor="IA de prueba ficticia")

@pytest.mark.parametrize('different',[False,True],ids=['identica','con-avance-propio'])
def test_conservacion_same_project_cell_appearing_after_plan_blocks(_contexto_conservacion,different):
    c,v,d = _contexto_conservacion
    plan = c.planificar(v,d)
    raw = plan['nuevos'][plan['ficha']]
    if different:
        raw = c.lineador().contenido(raw+b'\n## Mi avance\nContenido propio nuevo.\n')
    other = v/'00_CORE/cells/Ficha propia del usuario.md'
    other.write_bytes(raw)
    assert not c.validador(RAIZ).validar(other)[0]
    before = foto(v)
    written = []
    with pytest.raises(ValueError):
        c.aplicar(plan,written)
    assert not written and foto(v)==before

def test_conservacion_occupied_folder_after_plan_blocks_before_writing(_contexto_conservacion):
    c,v,d = _contexto_conservacion
    plan = c.planificar(v,d)
    folder = v/d['id']
    folder.mkdir()
    (folder/'nota-personal.md').write_bytes(b'Contenido ajeno posterior al plan.\n')
    before = foto(v)
    written = []
    with pytest.raises(ValueError):
        c.aplicar(plan,written)
    assert not written and foto(v)==before

def test_conservacion_changed_rules_after_plan_block_without_replacing(_contexto_conservacion):
    c,v,d = _contexto_conservacion
    plan = c.planificar(v,d)
    rules = v/'00_CORE/atoms/00_vault-rules.md'
    rules.write_bytes(rules.read_bytes()+b'\n## Regla propia nueva\nNo mezclar proyectos.\n')
    before = foto(v)
    written = []
    with pytest.raises(ValueError):
        c.aplicar(plan,written)
    assert not written and foto(v)==before

def test_conservacion_edited_cell_after_noop_plan_blocks(_contexto_conservacion):
    c,v,d = _contexto_conservacion
    c.aplicar(c.planificar(v,d),[])
    c.indexador().actualizar(v)
    plan = c.planificar(v,d)
    assert not plan['nuevos']
    cell = v/plan['ficha']
    cell.write_bytes(c.lineador().contenido(cell.read_bytes()+b'\n## Avance propio\nNo reemplazar.\n'))
    before = foto(v)
    written = []
    with pytest.raises(ValueError):
        c.aplicar(plan,written)
    assert not written and foto(v)==before

def test_conservacion_explicit_origin_is_used_during_apply(_contexto_conservacion,tmp_path,monkeypatch):
    c,v,d = _contexto_conservacion
    origin = tmp_path/'otro-kit'
    shutil.copytree(RAIZ,origin)
    plan = c.planificar(v,d,origen=origin)
    monkeypatch.setattr(c,'RAIZ',tmp_path/'no-es-el-origen')
    before = foto(v)
    written = []
    c.aplicar(plan,written)
    assert written and all(foto(v).get(p)==raw for p,raw in before.items())

def test_conservacion_input_data_mutated_after_plan_does_not_change_approved_output(_contexto_conservacion):
    c,v,d = _contexto_conservacion
    plan = c.planificar(v,d)
    expected = plan['nuevos'][plan['ficha']]
    d['objetivo']='Otro objetivo no aprobado para este plan.'
    written = []
    c.aplicar(plan,written)
    assert written and (v/plan['ficha']).read_bytes()==expected

def test_conservacion_cli_reports_blocked_when_guard_stops_before_first_write(_contexto_conservacion,tmp_path,monkeypatch,capsys):
    c,v,d = _contexto_conservacion
    datafile = tmp_path/'datos.json'
    datafile.write_text(json.dumps(d),encoding='utf-8')
    index = c.indexador()
    original = index.planificar
    snapshots = []
    def occupied_after_plan(dest):
        result = original(dest)
        if not snapshots:
            rules = v/'00_CORE/atoms/00_vault-rules.md'
            rules.write_bytes(rules.read_bytes()+b'\n## Regla nueva\nRespetar notas propias.\n')
            snapshots.append(foto(v))
        return result
    monkeypatch.setattr(index,'planificar',occupied_after_plan)
    monkeypatch.setattr(c,'indexador',lambda origen=RAIZ:index)
    assert c.main(['--destino',str(v),'--datos',str(datafile)])==1
    result = json.loads(capsys.readouterr().out)
    assert result['estado']=='bloqueado' and result['creados']==[]
    assert foto(v)==snapshots[0]

def test_conservacion_cli_first_write_oserror_still_reports_partial(_contexto_conservacion,tmp_path,monkeypatch,capsys):
    c,v,d = _contexto_conservacion
    payload = tmp_path/'datos.json'
    payload.write_text(json.dumps(d),encoding='utf-8')
    lines = c.lineador()
    remnants = []
    def partial_write(path,before,after):
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(after[:8])
        remnants.append(path)
        raise OSError('Fallo de disco simulado después de comenzar la escritura.')
    monkeypatch.setattr(lines,'guardar',partial_write)
    monkeypatch.setattr(c,'lineador',lambda origen=None:lines)
    assert c.main(['--destino',str(v),'--datos',str(payload)])==1
    result = json.loads(capsys.readouterr().out)
    assert remnants and remnants[0].is_file()
    assert result['creados']==[]  # Ningún archivo completo acreditado.
    assert result['estado']=='parcial'

@pytest.mark.parametrize('artifact',['ficha','indice'])
def test_conservacion_cli_planned_file_appeared_identical_blocks_and_fresh_plan_resumes(_contexto_conservacion,tmp_path,monkeypatch,capsys,artifact):
    c,v,d = _contexto_conservacion
    approved = c.planificar(v,d)
    rel = approved[artifact]
    data = approved['nuevos'][rel]
    payload = tmp_path/'datos.json'
    payload.write_text(json.dumps(d),encoding='utf-8')
    idx = c.indexador()
    original = idx.planificar
    snapshots = []
    def appeared(dest):
        result = original(dest)
        if not snapshots:
            path = v/rel
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(data)
            snapshots.append(foto(v))
        return result
    with monkeypatch.context() as patch:
        patch.setattr(idx,'planificar',appeared)
        patch.setattr(c,'indexador',lambda origen=None:idx)
        assert c.main(['--destino',str(v),'--datos',str(payload)])==1
    result = json.loads(capsys.readouterr().out)
    assert result['estado']=='bloqueado' and not result['creados']
    assert foto(v)==snapshots[0]
    fresh = c.planificar(v,d)
    assert rel in fresh['iguales'] and rel not in fresh['nuevos']
    written = []
    c.aplicar(fresh,written)
    assert written and rel not in written and (v/rel).read_bytes()==data

def test_conservacion_cli_keyboard_interrupt_inside_revalidation_is_blocked(_contexto_conservacion,tmp_path,monkeypatch,capsys):
    c,v,d = _contexto_conservacion
    payload = tmp_path/'datos.json'
    payload.write_text(json.dumps(d),encoding='utf-8')
    original = c.planificar
    calls = []
    def interrupted(*args,**kwargs):
        calls.append(True)
        if len(calls)==2:
            raise KeyboardInterrupt()
        return original(*args,**kwargs)
    before = foto(v)
    monkeypatch.setattr(c,'planificar',interrupted)
    assert c.main(['--destino',str(v),'--datos',str(payload)])==1
    result = json.loads(capsys.readouterr().out)
    assert len(calls)==2 and result['estado']=='bloqueado' and not result['creados']
    assert foto(v)==before

def test_conservacion_cli_value_error_after_writer_created_directory_is_partial(_contexto_conservacion,tmp_path,monkeypatch,capsys):
    c,v,d = _contexto_conservacion
    payload = tmp_path/'datos.json'
    payload.write_text(json.dumps(d),encoding='utf-8')
    lines = c.lineador()
    directories = []
    def interrupted(path,before,after):
        path.parent.mkdir(parents=True,exist_ok=True)
        directories.append(path.parent)
        raise ValueError('Bloqueo ocupado durante la escritura simulada.')
    monkeypatch.setattr(lines,'guardar',interrupted)
    monkeypatch.setattr(c,'lineador',lambda origen=None:lines)
    assert c.main(['--destino',str(v),'--datos',str(payload)])==1
    result = json.loads(capsys.readouterr().out)
    assert directories and directories[0].is_dir()
    assert result['estado']=='parcial' and not result['creados']

def test_conservacion_cli_keyboard_interrupt_after_first_guardar_is_partial(_contexto_conservacion,tmp_path,monkeypatch,capsys):
    c,v,d = _contexto_conservacion
    payload = tmp_path/'datos.json'
    payload.write_text(json.dumps(d),encoding='utf-8')
    lines = c.lineador()
    original = lines.guardar
    written = []
    def interrupted(path,before,after):
        original(path,before,after)
        written.append(path)
        raise KeyboardInterrupt()
    monkeypatch.setattr(lines,'guardar',interrupted)
    monkeypatch.setattr(c,'lineador',lambda origen=None:lines)
    assert c.main(['--destino',str(v),'--datos',str(payload)])==1
    result = json.loads(capsys.readouterr().out)
    assert written and written[0].is_file()
    assert result['estado']=='parcial'


def test_boveda_bajo_enlace_externo_crea_el_proyecto(vault, datos, tmp_path):
    (vault / 'INDICE.md').write_text('# Mapa\n', encoding='utf-8')
    real = tmp_path / 'real'
    real.mkdir()
    movida = Path(shutil.move(str(vault), str(real / vault.name)))
    enlace = tmp_path / 'enlace'
    try:
        enlace.symlink_to(real, target_is_directory=True)
    except OSError:
        if os.name != 'nt' or subprocess.run(['cmd', '/c', 'mklink', '/J', str(enlace), str(real)],
                                             capture_output=True).returncode:
            pytest.skip('La cuenta no permite crear enlaces ni junctions')
    try:
        plan = crear.planificar(enlace / movida.name, datos)
        crear.aplicar(plan, [])
        assert (movida / 'preparar-dos-materias').is_dir()
    finally:
        os.unlink(str(enlace)) if enlace.is_symlink() else os.rmdir(str(enlace))


def _cuerpo(texto):
    return texto.split('\n---\n', 1)[1] if texto.startswith('---\n') else texto


def test_porcentajes_no_abren_comentarios_de_obsidian(vault, datos, validador):
    datos.update(nombre='Ahorro %%oculto%% visible', descripcion='Subir 20%% el ahorro.',
                 hechos=[{'texto': 'Ahorro actual: 10%.', 'fuente': 'Planilla %%mensual%%'}])
    plan = crear.planificar(vault, datos)
    crear.aplicar(plan, [])
    for rel in (plan['ficha'], plan['indice']):
        cuerpo = _cuerpo((vault / rel).read_text(encoding='utf-8'))
        cuerpo = cuerpo.replace('%% node-index:start %%', '').replace('%% node-index:end %%', '')
        assert '%%' not in cuerpo and 'oculto' in cuerpo
    assert validador.validar(vault / plan['ficha']) == ([], [])


def test_fuente_con_parentesis_no_se_toma_como_faltante(vault, datos, validador):
    datos['hechos'] = [{'texto': 'Hay dos materias.', 'fuente': 'Plan de estudios (versión 2026)'},
                       {'texto': 'Falta elegir horario.'}]
    plan = crear.planificar(vault, datos)
    crear.aplicar(plan, [])
    errores, avisos = validador.validar(vault / plan['ficha'])
    assert not errores and len(avisos) == 1 and 'Falta elegir horario' in avisos[0]


def test_nombre_sin_letras_latinas_pide_acordar_identificador(vault, datos):
    datos['nombre'] = '数据分析'
    before = foto(vault)
    with pytest.raises(ValueError, match='identificador'):
        crear.planificar(vault, datos)
    assert foto(vault) == before
    datos['id'] = 'analisis-de-datos'
    assert crear.planificar(vault, datos)['id'] == 'analisis-de-datos'


def test_plantilla_sin_archivos_del_sistema_ni_temporales(vault, datos, tmp_path):
    origen = tmp_path / 'otro-kit'
    shutil.copytree(RAIZ, origen, ignore=shutil.ignore_patterns('.git', '__pycache__', '.pytest_cache', 'tests'))
    limpio = set(crear.planificar(vault, datos, origen=origen)['nuevos'])
    plantilla = origen / 'PROJECT_TEMPLATE'
    indice = '00 - Índice y Contexto.md'
    (plantilla / unicodedata.normalize('NFD', indice)).write_bytes((plantilla / indice).read_bytes())
    for basura in ['.DS_Store', 'Thumbs.db', '02_SINTESIS/~$borrador.docx', '02_SINTESIS/borrador.md.tmp',
                   '03_ENTREGABLES/copia.md~', '.oculta/nota.md', '__pycache__/modulo.pyc']:
        (plantilla / basura).parent.mkdir(exist_ok=True)
        (plantilla / basura).write_bytes(b'basura')
    assert set(crear.planificar(vault, datos, origen=origen)['nuevos']) == limpio
