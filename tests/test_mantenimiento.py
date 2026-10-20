"""Rangos reales, conservación, renovación temporal y reintentos de registros."""
from datetime import datetime
import errno
import importlib.util
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import time

import pytest

ROOT = Path(__file__).resolve().parent.parent


def load(name, filename):
    spec = importlib.util.spec_from_file_location(name, ROOT / '00_CORE/schemas' / filename)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


lines = load('rangos_test', 'note_index.py')
log = load('registro_test', 'registrar_cambios.py')


@pytest.mark.parametrize('eol,bom', [('\n', b''), ('\r\n', b''), ('\n', b'\xef\xbb\xbf')])
def test_rangos_apuntan_a_secciones_y_respetan_cuerpo(eol, bom):
    text = '---\ntipo: sintesis\n---\n\n# Apunte\n\n## Bases\nTexto propio.\n```md\n## No es sección\n```\n\n### Detalle\nÚltima línea'.replace('\n', eol)
    raw = bom + text.encode('utf-8')
    out = lines.contenido(raw)
    rendered = out.decode('utf-8-sig')
    assert lines.sin_indice(rendered) == lines.sin_indice(text)
    assert out.startswith(bom) and lines.contenido(out) == out
    source = rendered.splitlines()
    entries = [lines.ENTRY.fullmatch(line) for line in source]
    for entry in [e for e in entries if e]:
        start, end, description = int(entry[1]), int(entry[2]), entry[3]
        assert 1 <= start <= end <= len(source)
        if description in {'Apunte', 'Bases', 'Detalle'}:
            assert source[start-1].lstrip('# ') == description
    assert not any(e and e[3] == 'No es sección' for e in entries)


@pytest.mark.parametrize('atribucion', ['> **Main credit to davidkimai.**', '> **Besonderer Dank an davidkimai.**',
                                        '> **主要致谢：davidkimai。**'])
def test_atribucion_traducida_queda_primera(atribucion):
    text = atribucion + '\n\n# Kit\n## Uso\nHola\n'
    result = lines.render(text)
    assert result.splitlines()[0] == atribucion
    assert result.splitlines()[1].startswith('> [!info]')
    assert result.splitlines()[2] == '> - Líneas 1–1: Atribución'
    assert lines.render(result) == result


def test_atribucion_primera_y_fences_tilde():
    text = '> **Crédito principal a davidkimai.**\n\n# Kit\n~~~md\n## Código\n~~~\n## Uso\nHola\n'
    result = lines.render(text)
    assert result.splitlines()[0] == text.splitlines()[0]
    assert not re.search(r'> - Líneas .+: Código', result)


@pytest.mark.parametrize('marker', ['', '-'])
@pytest.mark.parametrize('eol,bom', [('\n', b''), ('\r\n', b''), ('\n', b'\xef\xbb\xbf')])
def test_formato_anterior_y_plegable_conservan_contenido(marker, eol, bom):
    body = '# Nota\n## Tema\nContenido propio.\n> [!warning] Aviso propio\n> No modificar este aviso.\n'
    text = ('---\ntipo: apunte\n---\n> [!info]'+marker+' Índice de esta nota (líneas)\n'
            '> - Líneas 1–1: Rango anterior\n\n'+body).replace('\n', eol)
    out = lines.contenido(bom+text.encode('utf-8'))
    rendered = out.decode('utf-8-sig')
    assert rendered.startswith('---'+eol+'tipo: apunte'+eol+'---'+eol+'> [!info]- Índice de esta nota (líneas)'+eol)
    assert rendered.endswith(body.replace('\n', eol))
    assert rendered.count('Índice de esta nota (líneas)')==1
    assert out.startswith(bom) and lines.contenido(out)==out
    entry = next(lines.ENTRY.fullmatch(s) for s in rendered.splitlines() if s.endswith(': Tema'))
    assert rendered.splitlines()[int(entry[1])-1]=='## Tema'
    assert int(entry[2])==len(rendered.splitlines())


@pytest.mark.parametrize('headers', [('', '-'), ('-', '')])
def test_indices_duplicados_de_ambos_formatos_impiden_el_lote(tmp_path, headers):
    valid = tmp_path/'Valida.md'
    valid.write_bytes(b'# Nota\nTexto conservado.\n')
    broken = tmp_path/'Duplicada.md'
    broken.write_text('\n'.join('> [!info]'+s+' Índice de esta nota (líneas)' for s in headers)+'\n# Nota\n', encoding='utf-8')
    before = {p:p.read_bytes() for p in (valid, broken)}
    assert lines.main(['apply', str(valid), str(broken)])==2
    assert all(p.read_bytes()==raw for p,raw in before.items())


@pytest.mark.parametrize('marker', ['', '-'])
def test_actualizador_refresca_rangos_de_mapas_de_ambos_formatos(tmp_path, marker):
    from test_indice import indice
    indice.actualizar(tmp_path)
    general = tmp_path/'INDICE.md'
    raw = general.read_text(encoding='utf-8')
    general.write_text(raw.replace('> [!info]-', '> [!info]'+marker), encoding='utf-8')
    note = tmp_path/'Nueva.md'
    note.write_bytes(b'# Nota nueva\nContenido conservado.\n')
    indice.actualizar(tmp_path)
    assert 'Nueva.md' in general.read_text(encoding='utf-8')
    assert lines.contenido(general.read_bytes())==general.read_bytes()
    assert general.read_text(encoding='utf-8').startswith('> [!info]-')
    assert note.read_bytes()==b'# Nota nueva\nContenido conservado.\n'
    assert indice.actualizar(tmp_path, comprobar=True)['estado']=='vigente'


@pytest.mark.parametrize('text', ['---\npropiedad: sin cierre\n', '# Nota\n' + lines.HEADER,
    lines.HEADER + '\n> lista propia\n# Nota\n', lines.HEADER + '\n' + lines.HEADER])
def test_indices_incompatibles_no_se_reemplazan(text):
    with pytest.raises(ValueError):
        lines.render(text)


def test_check_no_escribe_y_apply_preflight(tmp_path):
    valid = tmp_path / 'Nota.md'
    valid.write_text('# Nota\nHola.\n', encoding='utf-8')
    before = valid.read_bytes()
    assert lines.main(['check', str(valid)]) == 1 and valid.read_bytes() == before
    broken = tmp_path / 'Rota.md'
    broken.write_text('---\nsin cierre\n', encoding='utf-8')
    assert lines.main(['apply', str(valid), str(broken)]) == 2
    assert valid.read_bytes() == before
    assert lines.main(['apply', str(valid)]) == 0
    assert lines.main(['check', str(valid)]) == 0


@pytest.mark.parametrize('herramienta', ['nota', 'proyecto'])
@pytest.mark.parametrize('otro_editor', [False, True], ids=['parcial-propio', 'edicion-ajena'])
@pytest.mark.parametrize('sin_enlaces', [False, True], ids=['publicacion-completa', 'sin-enlaces-duros'])
def test_fallo_de_creacion_conserva_edicion_de_otro_proceso(tmp_path, monkeypatch, herramienta, otro_editor, sin_enlaces):
    target = tmp_path/'Nota.md'
    expected = b'# Nota\nContenido completo previsto.\n'
    foreign = b'Avance del otro editor\n'
    sibling = tmp_path/'Previa.md'
    sibling.write_bytes(b'Nota existente intacta.\n')
    original_open = Path.open
    original_temp = tempfile.NamedTemporaryFile

    class Interrupted:
        def __init__(self, stream):
            self.stream = stream
        def __enter__(self):
            return self
        def __exit__(self, *args):
            return self.stream.__exit__(*args)
        def fileno(self):
            return self.stream.fileno()
        def __getattr__(self, name):
            return getattr(self.stream, name)
        def write(self, data):
            self.stream.write(data[:7])
            self.stream.flush()
            if otro_editor:
                # Otro proceso escribe sin cooperar con el bloqueo del kit.
                subprocess.run([sys.executable, '-c',
                                'from pathlib import Path; import sys; Path(sys.argv[1]).write_bytes(b"Avance del otro editor\\n")',
                                str(target)], check=True, capture_output=True, timeout=10)
                if Path(self.stream.name) == target:
                    assert os.path.samestat(os.fstat(self.fileno()), target.stat())
            raise OSError('Escritura interrumpida durante la prueba')

    def interrupted(path, mode='r', *args, **kwargs):
        stream = original_open(path, mode, *args, **kwargs)
        return Interrupted(stream) if path == target and mode == 'xb' else stream

    if herramienta == 'nota':
        write = lambda: lines.guardar(target, None, expected)
    else:
        spec = importlib.util.spec_from_file_location('creador_interrumpido', ROOT/'crear_proyecto.py')
        creator = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(creator)
        created = []
        write = lambda: creator.aplicar({'destino':tmp_path, 'nuevos':{'Nota.md':expected}}, created)
    with monkeypatch.context() as patch:
        patch.setattr(Path, 'open', interrupted)
        if sin_enlaces:
            def unsupported(*args):
                raise OSError(errno.ENOTSUP, 'Sin enlaces duros en la prueba')
            patch.setattr(os, 'link', unsupported)
        else:
            patch.setattr(tempfile, 'NamedTemporaryFile', lambda *a, **kw: Interrupted(original_temp(*a, **kw)))
        with pytest.raises(OSError, match='interrumpida'):
            write()
    if otro_editor:
        assert target.exists(), 'La limpieza borró la edición ajena en el mismo archivo.'
        assert target.read_bytes() == foreign
    elif sin_enlaces:
        assert target.read_bytes() == expected[:7]  # Conservar para releer antes de reparar.
    else:
        assert not target.exists()  # El fallo fue anterior a publicar la nota definitiva.
    assert sibling.read_bytes() == b'Nota existente intacta.\n'
    assert not list(tmp_path.glob('*.kit-lock'))
    assert not list(tmp_path.glob('.nota-*.tmp'))


def test_lote_conserva_fuentes_y_comandos(tmp_path):
    for folder in ['01_FUENTES', '.claude', '.opencode', 'Notas']:
        (tmp_path / folder).mkdir()
        (tmp_path / folder / 'Nota.md').write_text('# Original\n', encoding='utf-8')
    before = {p:p.read_bytes() for p in tmp_path.rglob('*.md')}
    assert lines.main(['apply', '--vault', str(tmp_path)]) == 0
    assert all(p.read_bytes() == b for p,b in before.items() if p.parent.name != 'Notas')
    assert lines.main(['apply', str(tmp_path / '01_FUENTES/Nota.md')]) == 2


@pytest.mark.parametrize('aparece_archivo', [False, True])
def test_creacion_sin_enlaces_duros_conserva_archivo_aparecido(tmp_path, monkeypatch, aparece_archivo):
    target = tmp_path/'Nota.md'
    foreign = b'Nota creada por otra herramienta.\n'
    def unsupported(source, dest):
        if aparece_archivo:
            Path(dest).write_bytes(foreign)
        raise OSError(errno.ENOTSUP, 'El sistema no admite enlaces duros')
    monkeypatch.setattr(os, 'link', unsupported)
    if aparece_archivo:
        with pytest.raises(FileExistsError):
            lines.guardar(target, None, b'Nota prevista.\n')
        assert target.read_bytes() == foreign
    else:
        assert lines.guardar(target, None, b'Nota prevista.\n')
        assert target.read_bytes() == b'Nota prevista.\n'
    assert not list(tmp_path.glob('.nota-*.tmp'))
    assert not list(tmp_path.glob('*.kit-lock'))


def event(root, code='test-1', action='crear', **extra):
    target = root / 'Notas/Apunte.md'
    target.parent.mkdir(parents=True, exist_ok=True)
    if not target.exists():
        target.write_text('# Apunte\nTexto original.\n', encoding='utf-8')
    result = {'id':code, 'ia':'IA de prueba', 'herramienta':'Prueba virtual', 'resumen':'Nota guardada.',
              'verificado':True, 'cambios':[{'accion':action,'ruta':'Notas/Apunte.md'}]}
    result.update(extra)
    return result


def test_rotacion_exactamente_cinco_dias_archiva_bytes_y_no_mtime(tmp_path):
    data = event(tmp_path)
    note = (tmp_path/'Notas/Apunte.md').read_bytes()
    first = log.registrar(tmp_path, data, '2026-10-09T10:00:00-03:00')
    active = tmp_path/log.REGISTRO
    os.utime(active, (1,1))
    assert not log.registrar(tmp_path, event(tmp_path,'test-2'), '2026-10-14T09:59:59-03:00')['rotado']
    original = active.read_bytes()
    result = log.registrar(tmp_path, event(tmp_path,'test-3'), '2026-10-14T10:00:00-03:00')
    assert result['rotado'] and (tmp_path/result['archivo']).read_bytes() == original
    assert log.entradas(active.read_bytes())[0] == datetime.fromisoformat('2026-10-14T10:00:00-03:00')
    assert (tmp_path/'Notas/Apunte.md').read_bytes() == note
    assert lines.contenido(active.read_bytes()) == active.read_bytes()
    assert first['estado'] == 'registrado'


def test_reintento_incluso_archivado_no_duplica_y_conflicto_conserva(tmp_path):
    first = event(tmp_path)
    log.registrar(tmp_path, first, '2026-10-09T10:00:00-03:00')
    log.registrar(tmp_path, event(tmp_path,'test-2'), '2026-10-15T10:00:00-03:00')
    before = {p:p.read_bytes() for p in tmp_path.rglob('*.md')}
    assert log.registrar(tmp_path, first, '2026-10-16T10:00:00-03:00')['estado'] == 'ya-registrado'
    assert before == {p:p.read_bytes() for p in tmp_path.rglob('*.md')}
    with pytest.raises(ValueError):
        log.registrar(tmp_path, event(tmp_path, resumen='Cambio incompatible.'), '2026-10-16T10:00:00-03:00')
    assert before == {p:p.read_bytes() for p in tmp_path.rglob('*.md')}


def test_dry_run_no_crea_registro_y_periodo_futuro_se_conserva(tmp_path):
    data = event(tmp_path)
    assert log.registrar(tmp_path,data,'2026-10-09T10:00:00-03:00',True)['estado'] == 'plan'
    assert not (tmp_path/'00_CORE').exists()
    log.registrar(tmp_path,data,'2026-10-09T10:00:00-03:00')
    before = (tmp_path/log.REGISTRO).read_bytes()
    with pytest.raises(ValueError):
        log.registrar(tmp_path,event(tmp_path,'test-2'),'2026-10-08T10:00:00-03:00')
    assert (tmp_path/log.REGISTRO).read_bytes() == before


@pytest.mark.parametrize('change', [{'accion':'editar','ruta':'../fuera.md'}, {'accion':'editar','ruta':'C:/fuera.md'},
    {'accion':'editar','ruta':'No-existe.md'}, {'accion':'mover','ruta':'Notas/Apunte.md'},
    {'accion':'editar','ruta':log.REGISTRO}])
def test_eventos_invalidos_no_crean_log(tmp_path, change):
    data = event(tmp_path)
    data['cambios'] = [change]
    with pytest.raises(ValueError):
        log.registrar(tmp_path,data,'2026-10-09T10:00:00-03:00')
    assert not (tmp_path/'00_CORE').exists()


def test_movimiento_registra_origen_y_hash_sin_mover_notas(tmp_path):
    data = event(tmp_path,action='mover')
    data['cambios'][0]['desde'] = 'Antes/Apunte.md'
    result = log.registrar(tmp_path,data,'2026-10-09T10:00:00-03:00')
    entry = log.entradas((tmp_path/result['registro']).read_bytes())[1][0]
    assert entry['cambios'][0]['desde'] == 'Antes/Apunte.md'
    assert len(entry['cambios'][0]['sha256']) == 64
    assert not (tmp_path/'Antes').exists()


def evento_ficha(root, contenido, nombre='estudio-context.md', verificado=True):
    path = root / '00_CORE/cells' / nombre
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(contenido, encoding='utf-8')
    return path, {'id': 'ficha-estudio', 'ia': 'Prueba', 'herramienta': 'pytest',
                  'resumen': 'Ficha de prueba.', 'verificado': verificado,
                  'cambios': [{'accion': 'editar', 'ruta': path.relative_to(root).as_posix()}]}


@pytest.mark.parametrize('nombre', ['estudio-context.md', 'Ficha personal.MD'])
def test_registro_no_declara_verificada_ficha_invalida(tmp_path, ejemplo, nombre):
    path, data = evento_ficha(tmp_path, ejemplo.replace('contexto: D', 'contexto: E'), nombre)
    before = path.read_bytes()
    with pytest.raises(ValueError, match='[Ff]icha'):
        log.registrar(tmp_path, data)
    assert path.read_bytes() == before and not (tmp_path / log.REGISTRO).exists()


def test_registro_admite_ficha_incompleta_como_pendiente(tmp_path):
    _, data = evento_ficha(tmp_path, '# Ficha incompleta\n', verificado=False)
    log.registrar(tmp_path, data)
    assert log.entradas((tmp_path / log.REGISTRO).read_bytes())[1][0]['verificado'] is False


def test_registro_detecta_propuesta_sin_casilla_del_ensayo(tmp_path, ejemplo):
    accion = '- [x] Instalar Python y un editor'
    assert accion in ejemplo
    _, data = evento_ficha(tmp_path, ejemplo.replace(accion, '- Propuesta: estudiar planetas.'))
    with pytest.raises(ValueError, match='acción'):
        log.registrar(tmp_path, data)
    assert not (tmp_path / log.REGISTRO).exists()


def test_registro_verifica_solo_fichas_tocadas_y_admite_avisos(tmp_path, ejemplo):
    path, data = evento_ficha(tmp_path, ejemplo.replace('## Hechos clave', '## Hechos clave\n\n- Sin fuente.'))
    (path.parent / 'ajena-context.md').write_text('# No editar ni validar\n', encoding='utf-8')
    log.registrar(tmp_path, data)
    assert log.entradas((tmp_path / log.REGISTRO).read_bytes())[1][0]['verificado'] is True


@pytest.mark.parametrize('nombre', ['TEMPLATE_cell.md', 'README.md'])
def test_registro_no_confunde_plantillas_y_ayuda_con_fichas(tmp_path, plantilla, nombre):
    _, data = evento_ficha(tmp_path, plantilla if nombre == 'TEMPLATE_cell.md' else '# Ayuda\n', nombre)
    assert log.registrar(tmp_path, data)['estado'] == 'registrado'


def test_reintento_ficha_no_valida_ni_reescribe_resultado_futuro(tmp_path, ejemplo):
    path, data = evento_ficha(tmp_path, ejemplo)
    log.registrar(tmp_path, data)
    before = (tmp_path / log.REGISTRO).read_bytes()
    path.write_text('# Modificación posterior\n', encoding='utf-8')
    assert log.registrar(tmp_path, data)['estado'] == 'ya-registrado'
    assert (tmp_path / log.REGISTRO).read_bytes() == before


def test_registro_ficha_borrada_no_intenta_validarla(tmp_path):
    _, data = evento_ficha(tmp_path, '# Ficha rota\n')
    (tmp_path / data['cambios'][0]['ruta']).unlink()
    data['cambios'][0]['accion'] = 'borrar'
    assert log.registrar(tmp_path, data)['estado'] == 'registrado'


@pytest.mark.parametrize('fecha', ['2026-10-12T19:20:00-03:00', '2026-10-13T00:10:00+02:00'])
def test_cli_registro_rechaza_fecha_futura_sin_escribir(tmp_path, monkeypatch, fecha):
    class Reloj(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.fromisoformat('2026-10-12T19:03:00-03:00')
    monkeypatch.setattr(log, 'datetime', Reloj)
    data = event(tmp_path)
    payload = tmp_path / 'evento.json'
    payload.write_text(json.dumps(data), encoding='utf-8')
    assert log.main(['--destino', str(tmp_path), '--datos', str(payload), '--fecha', fecha]) == 2
    assert not (tmp_path / log.REGISTRO).exists()


def test_api_registro_conserva_simulacion_con_fechas_explicitas(tmp_path):
    assert log.registrar(tmp_path, event(tmp_path), '2099-10-12T19:20:00-03:00')['estado'] == 'registrado'


@pytest.mark.parametrize('fecha', ['2026-10-12T19:00:00-03:00', '2026-10-13T00:03:00+02:00'])
def test_cli_registro_admite_pasado_y_hora_actual_en_otra_zona(tmp_path, monkeypatch, fecha):
    class Reloj(datetime):
        @classmethod
        def now(cls, tz=None):
            return datetime.fromisoformat('2026-10-12T19:03:00-03:00')
    monkeypatch.setattr(log, 'datetime', Reloj)
    data = event(tmp_path)
    payload = tmp_path / 'evento.json'
    payload.write_text(json.dumps(data), encoding='utf-8')
    assert log.main(['--destino', str(tmp_path), '--datos', str(payload), '--fecha', fecha]) == 0


def test_registro_propio_o_bloqueo_ajeno_se_conserva(tmp_path):
    data = event(tmp_path)
    path = tmp_path/log.REGISTRO
    path.parent.mkdir(parents=True)
    path.write_bytes(b'# Mi registro manual\n')
    with pytest.raises(ValueError):
        log.registrar(tmp_path,data,'2026-10-09T10:00:00-03:00')
    assert path.read_bytes() == b'# Mi registro manual\n'
    lock = path.parent/'.registro-cambios.lock'
    lock.write_bytes(b'Otra operacion')
    with pytest.raises(ValueError):
        log.registrar(tmp_path,data,'2026-10-09T10:00:00-03:00')
    assert lock.read_bytes() == b'Otra operacion'


def test_fallo_despues_de_archivar_se_puede_reintentar(tmp_path, monkeypatch):
    log.registrar(tmp_path,event(tmp_path),'2026-10-09T10:00:00-03:00')
    before = (tmp_path/log.REGISTRO).read_bytes()
    original = log.lineas.guardar
    def failed(path, old, new):
        if path.name == 'registro-cambios.md':
            raise OSError('Fallo simulado')
        return original(path,old,new)
    monkeypatch.setattr(log.lineas,'guardar',failed)
    with pytest.raises(OSError):
        log.registrar(tmp_path,event(tmp_path,'test-2'),'2026-10-15T10:00:00-03:00')
    assert (tmp_path/log.REGISTRO).read_bytes() == before
    assert len(list((tmp_path/log.ARCHIVO).glob('*.md'))) == 1
    monkeypatch.setattr(log.lineas,'guardar',original)
    log.registrar(tmp_path,event(tmp_path,'test-2'),'2026-10-15T10:00:00-03:00')
    assert len(list((tmp_path/log.ARCHIVO).glob('*.md'))) == 1


def test_creador_y_mapa_recalculan_rangos_al_crecer(tmp_path):
    import shutil
    vault = tmp_path/'vault'
    shutil.copytree(ROOT/'00_CORE',vault/'00_CORE',ignore=shutil.ignore_patterns('__pycache__'))
    payload = tmp_path/'datos.json'
    payload.write_text(json.dumps({'nombre':'Estudio','descripcion':'Materias.','objetivo':'Estudiar.',
        'contexto':'D','fecha':'2026-10-09','autor':'IA de prueba (fixture)'}),encoding='utf-8')
    command = [sys.executable,'-B',str(ROOT/'crear_proyecto.py'),'--destino',str(vault),'--datos',str(payload)]
    for _ in range(2):
        result = subprocess.run(command,capture_output=True,text=True,encoding='utf-8')
        assert result.returncode == 0, result.stdout
    local = vault/'estudio/00 - Índice - estudio.md'
    assert 'Creado por: IA de prueba' in local.read_text(encoding='utf-8')
    (vault/'estudio/02_SINTESIS/Apunte.md').write_text('# Apunte\n',encoding='utf-8')
    result = subprocess.run([sys.executable,'-B',str(ROOT/'actualizar_indice.py'),str(vault)],capture_output=True,text=True,encoding='utf-8')
    assert result.returncode == 0, result.stdout
    assert lines.contenido(local.read_bytes()) == local.read_bytes()


def test_lote_preserva_archivos_y_registros_historicos(tmp_path):
    protected = [tmp_path/'Proyecto/_archivo/Nota.md',
                 tmp_path/'00_CORE/logs/historial/Periodo.md']
    for path in protected:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b'# Copia inmutable\nTexto original.\n')
    editable = tmp_path/'Notas/Actual.md'
    editable.parent.mkdir()
    editable.write_bytes(b'# Actual\n')
    before = {p:p.read_bytes() for p in protected}
    assert lines.main(['apply', '--vault', str(tmp_path)]) == 0
    assert before == {p:p.read_bytes() for p in protected}
    assert lines.main(['apply', str(protected[1])]) == 2
    assert lines.contenido(editable.read_bytes()) == editable.read_bytes()


def test_lote_no_declara_vigente_una_carpeta_inexistente(tmp_path):
    assert lines.main(['check', '--vault', str(tmp_path/'No-existe')]) == 2


def test_propiedades_sin_salto_final_producen_markdown_valido():
    text = '---\ntipo: sintesis\n---'
    result = lines.render(text)
    assert result.splitlines()[:3] == text.splitlines()
    assert result.splitlines()[3] == lines.HEADER
    assert lines.render(result) == result


def test_reintento_con_nota_editada_o_eliminada_no_reescribe_historial(tmp_path):
    data = event(tmp_path)
    log.registrar(tmp_path, data, '2026-10-09T10:00:00-03:00')
    log.registrar(tmp_path, event(tmp_path, 'otro'), '2026-10-15T10:00:00-03:00')
    original = {p:p.read_bytes() for p in (tmp_path/'00_CORE').rglob('*.md')}
    note = tmp_path/'Notas/Apunte.md'
    note.write_bytes(b'# Nota editada despues\n')
    for exists in [True, False]:
        if not exists:
            note.unlink()
        assert log.registrar(tmp_path, data, '2026-10-16T10:00:00-03:00')['estado'] == 'ya-registrado'
        assert original == {p:p.read_bytes() for p in (tmp_path/'00_CORE').rglob('*.md')}


def test_borrar_no_registra_eliminacion_si_el_archivo_sigue_presente(tmp_path):
    data = event(tmp_path, action='borrar')
    with pytest.raises(ValueError):
        log.registrar(tmp_path, data, '2026-10-09T10:00:00-03:00')
    assert not (tmp_path/'00_CORE').exists()


@pytest.mark.parametrize('raw', [
    b'---\notra: propiedad\n---\n\ntipo: registro-cambios\ninicio: "2026-10-09T10:00:00-03:00"\n',
    b'---\ntipo: registro-cambios\ninicio: "2026-10-09T10:00:00-03:00"\n',
    b'---\ntipo: registro-cambios\ninicio: "2026-10-09T10:00:00-03:00"\ninicio: "2026-10-10T10:00:00-03:00"\n---\n',
])
def test_registro_con_propiedades_danadas_se_conserva(tmp_path, raw):
    data = event(tmp_path)
    active = tmp_path/log.REGISTRO
    active.parent.mkdir(parents=True)
    active.write_bytes(raw)
    with pytest.raises(ValueError):
        log.registrar(tmp_path, data, '2026-10-16T10:00:00-03:00')
    assert active.read_bytes() == raw
    assert not (tmp_path/log.ARCHIVO).exists()


def test_archivo_nuevo_incompleto_no_bloquea_reintento(tmp_path, monkeypatch):
    target = tmp_path/'Periodo.md'
    original = tempfile.NamedTemporaryFile
    class FalloEscritura:
        def __enter__(self):
            return self
        def __exit__(self, *args):
            self.stream.close()
        def fileno(self):
            return self.stream.fileno()
        def __getattr__(self, name):
            return getattr(self.stream, name)
        def write(self, data):
            self.stream.write(data[:3])
            raise OSError('Escritura interrumpida')
    def failing(*args, **kwargs):
        wrapped = FalloEscritura()
        wrapped.stream = original(*args, **kwargs)
        return wrapped
    with monkeypatch.context() as patch:
        patch.setattr(tempfile, 'NamedTemporaryFile', failing)
        with pytest.raises(OSError):
            lines.guardar(target, None, b'Contenido completo')
    assert not target.exists()
    assert lines.guardar(target, None, b'Contenido completo')


def test_mapa_nuevo_incluye_rangos_y_es_idempotente(tmp_path):
    import importlib.util
    spec = importlib.util.spec_from_file_location('mapa_revision', ROOT/'actualizar_indice.py')
    index = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(index)
    (tmp_path/'Nota.md').write_bytes(b'# Nota\n')
    index.actualizar(tmp_path)
    general = tmp_path/'INDICE.md'
    assert lines.HEADER in general.read_text(encoding='utf-8')
    assert lines.contenido(general.read_bytes()) == general.read_bytes()
    assert index.actualizar(tmp_path, comprobar=True)['estado'] == 'vigente'


def test_registro_por_defecto_usa_zona_local_y_borrado_real(tmp_path):
    data = event(tmp_path, action='borrar')
    (tmp_path/'Notas/Apunte.md').unlink()
    lower = datetime.now().astimezone()
    log.registrar(tmp_path, data)
    upper = datetime.now().astimezone()
    start, entries = log.entradas((tmp_path/log.REGISTRO).read_bytes())
    assert lower <= start <= upper
    assert start.utcoffset() == lower.utcoffset()
    assert 'sha256' not in entries[0]['cambios'][0]


def test_mapa_y_registro_conservan_bom_al_actualizar(tmp_path):
    spec = importlib.util.spec_from_file_location('mapa_bom', ROOT/'actualizar_indice.py')
    index = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(index)
    bom = b'\xef\xbb\xbf'
    index.actualizar(tmp_path)
    general = tmp_path/'INDICE.md'
    general.write_bytes(bom + general.read_bytes())
    data = event(tmp_path)
    index.actualizar(tmp_path)
    assert general.read_bytes().startswith(bom)
    assert lines.contenido(general.read_bytes()) == general.read_bytes()
    log.registrar(tmp_path, data, '2026-10-09T10:00:00-03:00')
    active = tmp_path/log.REGISTRO
    active.write_bytes(bom + active.read_bytes())
    log.registrar(tmp_path, event(tmp_path, 'segundo'), '2026-10-10T10:00:00-03:00')
    assert active.read_bytes().startswith(bom)


def test_entrada_historica_incompatible_no_se_reemplaza(tmp_path):
    data = event(tmp_path)
    log.registrar(tmp_path, data, '2026-10-09T10:00:00-03:00')
    active = tmp_path/log.REGISTRO
    text = active.read_text(encoding='utf-8')
    text = log.MARCA.sub('%% cambio: {"id": "danado", "cambios": [null]} %%', text)
    active.write_bytes(text.encode('utf-8'))
    before = active.read_bytes()
    with pytest.raises(ValueError):
        log.registrar(tmp_path, event(tmp_path, 'segundo'), '2026-10-16T10:00:00-03:00')
    assert active.read_bytes() == before
    assert not (tmp_path/log.ARCHIVO).exists()


@pytest.mark.parametrize('folder', ['Proyecto/01_FUENTES', 'Proyecto/_archivo', '00_CORE/logs/historial'])
def test_actualizar_mapas_no_reescribe_indices_protegidos(tmp_path, folder):
    spec = importlib.util.spec_from_file_location('mapa_protegido', ROOT/'actualizar_indice.py')
    index = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(index)
    path = tmp_path/folder/'Indice.md'
    path.parent.mkdir(parents=True)
    raw = b'---\ntipo: indice-nodo\n---\n# Copia original\n\n%% node-index:start %%\n%% node-index:end %%\n'
    path.write_bytes(raw)
    result = index.actualizar(tmp_path)
    assert path.read_bytes() == raw
    assert path.relative_to(tmp_path).as_posix() in result['indices_manuales']
    assert path.relative_to(tmp_path).as_posix() in (tmp_path/'INDICE.md').read_text(encoding='utf-8')
    assert index.actualizar(tmp_path, comprobar=True)['estado'] == 'vigente'


def test_fecha_utc_iso_con_z_es_portable():
    assert log.momento('2026-10-09T10:00:00Z').isoformat() == '2026-10-09T10:00:00+00:00'


# Dos intérpretes independientes, detenidos justo antes del reemplazo real.
ESCRITOR_CONCURRENTE = r'''
import importlib.util, json, os, sys, time
from pathlib import Path
module_path, mode, target, author, ready, release = sys.argv[1:]
spec = importlib.util.spec_from_file_location('escritor', module_path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
path = Path(target)
before = path.read_bytes()
after = before + author.encode('utf-8') + b'\n'
original = os.replace
def gated(source, destination):
    if ready:
        Path(ready).write_bytes(b'listo')
        deadline = time.monotonic() + 20
        while not Path(release).exists():
            if time.monotonic() > deadline:
                raise TimeoutError('No se liberó el escritor de prueba')
            time.sleep(0.01)
    return original(source, destination)
os.replace = gated
try:
    if mode == 'mapa':
        module.guardar_plan({'ruta':path, 'antes':before, 'contenido':after})
    elif mode == 'registro':
        module.registrar(path.parents[2], {
            'id':author, 'ia':author, 'herramienta':'Proceso de prueba',
            'resumen':'Cambio ficticio.', 'verificado':True,
            'cambios':[{'accion':'editar','ruta':'Notas/Apunte.md'}]
        }, '2026-10-10T10:00:00-03:00')
    else:
        module.guardar(path, before, after)
    result = {'estado':'guardado'}
except (OSError, ValueError) as error:
    result = {'estado':'pendiente', 'error':str(error)}
print(json.dumps(result))
'''


@pytest.mark.parametrize('mode,second_mode', [
    ('nota', 'nota'), ('mapa', 'mapa'), ('registro', 'registro'),
    ('nota', 'mapa'), ('mapa', 'nota'),
])
def test_dos_procesos_no_pisan_cambios_y_reintento_conserva_ambos(tmp_path, mode, second_mode):
    if mode == 'registro':
        log.registrar(tmp_path, event(tmp_path), '2026-10-09T10:00:00-03:00')
        target = tmp_path/log.REGISTRO
        module_path = ROOT/'00_CORE/schemas/registrar_cambios.py'
    else:
        target = tmp_path/('INDICE.md' if mode == 'mapa' else 'Nota.md')
        target.write_bytes(b'# Contenido inicial\n')
        module_path = ROOT/('actualizar_indice.py' if mode == 'mapa' else '00_CORE/schemas/note_index.py')
    before = target.read_bytes()
    ready, release = tmp_path/'escritor-listo', tmp_path/'liberar-escritor'
    command = [sys.executable, '-B', '-c', ESCRITOR_CONCURRENTE, str(module_path), mode, str(target)]
    second_module = ROOT/({'nota':'00_CORE/schemas/note_index.py',
                          'mapa':'actualizar_indice.py',
                          'registro':'00_CORE/schemas/registrar_cambios.py'}[second_mode])
    second_command = [sys.executable, '-B', '-c', ESCRITOR_CONCURRENTE,
                      str(second_module), second_mode, str(target)]
    first = subprocess.Popen(command+['autor-1', str(ready), str(release)], stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, text=True, encoding='utf-8')
    try:
        deadline = time.monotonic()+10
        while not ready.exists():
            assert first.poll() is None, 'El primer escritor terminó antes del reemplazo'
            assert time.monotonic() < deadline, 'El primer escritor no llegó al reemplazo'
            time.sleep(0.01)
        second = subprocess.run(second_command+['autor-2', '', ''], capture_output=True,
                                text=True, encoding='utf-8', timeout=10)
        assert second.returncode == 0, second.stderr
        assert json.loads(second.stdout)['estado'] == 'pendiente'
        assert target.read_bytes() == before
        if mode != 'registro':
            # Un archivo ocupado no debe impedir trabajar en otro.
            other = tmp_path/'Otra-nota.md'
            other.write_bytes(b'# Otra nota\n')
            independent = subprocess.run(second_command[:-1]+[str(other), 'autor-2', '', ''],
                                         capture_output=True, text=True, encoding='utf-8', timeout=10)
            assert independent.returncode == 0, independent.stderr
            assert json.loads(independent.stdout)['estado'] == 'guardado'
            assert other.read_bytes() == b'# Otra nota\nautor-2\n'
    finally:
        release.write_bytes(b'continuar')
        try:
            stdout, stderr = first.communicate(timeout=10)
        except subprocess.TimeoutExpired:
            first.kill()
            first.communicate()
            raise
    assert first.returncode == 0, stderr
    assert json.loads(stdout)['estado'] == 'guardado'
    retry = subprocess.run(second_command+['autor-2', '', ''], capture_output=True,
                           text=True, encoding='utf-8', timeout=10)
    assert retry.returncode == 0, retry.stderr
    assert json.loads(retry.stdout)['estado'] == 'guardado'
    final = target.read_bytes()
    if mode == 'registro':
        assert [e['id'] for e in log.entradas(final)[1]] == ['test-1', 'autor-1', 'autor-2']
    else:
        assert final == before+b'autor-1\nautor-2\n'
    assert not list(tmp_path.rglob('*.kit-lock'))
    assert not list(tmp_path.rglob('.nota-*.tmp'))
    assert not (tmp_path/'00_CORE/logs/.registro-cambios.lock').exists()


@pytest.mark.parametrize('existing', [False, True])
def test_bloqueo_de_nota_ajeno_se_conserva(tmp_path, existing):
    target = tmp_path/'Nota.md'
    before = b'Original' if existing else None
    if existing:
        target.write_bytes(before)
    lock = tmp_path/'.Nota.md.kit-lock'
    lock.write_bytes(b'Otro asistente')
    with pytest.raises(ValueError, match='curso'):
        lines.guardar(target, before, b'Mi cambio')
    assert lock.read_bytes() == b'Otro asistente'
    assert (target.read_bytes() if target.exists() else None) == before


def test_fallo_reemplazo_conserva_nota_y_libera_bloqueo(tmp_path, monkeypatch):
    target = tmp_path/'Nota.md'
    target.write_bytes(b'Original')
    def fail(*args):
        raise OSError('Fallo de reemplazo simulado')
    with monkeypatch.context() as patch:
        patch.setattr(lines.os, 'replace', fail)
        with pytest.raises(OSError):
            lines.guardar(target, b'Original', b'Mi cambio')
    assert target.read_bytes() == b'Original'
    assert sorted(p.name for p in tmp_path.iterdir()) == ['Nota.md']
    assert lines.guardar(target, b'Original', b'Mi cambio')


def test_lectura_vieja_se_rechaza_y_no_deja_bloqueo(tmp_path):
    target = tmp_path/'Nota.md'
    target.write_bytes(b'Cambio de otro asistente')
    with pytest.raises(ValueError, match='cambió'):
        lines.guardar(target, b'Lectura anterior', b'Mi cambio')
    assert target.read_bytes() == b'Cambio de otro asistente'
    assert sorted(p.name for p in tmp_path.iterdir()) == ['Nota.md']


@pytest.mark.parametrize('accion', [[], {}, ['crear'], 3])
def test_accion_no_textual_es_error_controlado(tmp_path, accion):
    data = event(tmp_path)
    data['cambios'] = [{'accion': accion, 'ruta': 'Notas/Apunte.md'}]
    with pytest.raises(ValueError):
        log.registrar(tmp_path, data, '2026-10-09T10:00:00-03:00')
    assert not (tmp_path / '00_CORE').exists()


def test_bloqueo_retirado_por_otro_no_oculta_el_registro(tmp_path, monkeypatch):
    original = log._registrar

    def registrar_y_retirar(root, *args):
        resultado = original(root, *args)
        bloqueo = root / '00_CORE/logs/.registro-cambios.lock'
        if bloqueo.exists():  # La simulación previa no toma el bloqueo.
            bloqueo.unlink()
        return resultado

    monkeypatch.setattr(log, '_registrar', registrar_y_retirar)
    resultado = log.registrar(tmp_path, event(tmp_path), '2026-10-09T10:00:00-03:00')
    assert isinstance(resultado, dict)
    assert (tmp_path / log.REGISTRO).is_file()


@pytest.mark.skipif(os.name == 'nt', reason='Permisos POSIX')
def test_guardar_conserva_permisos_de_la_nota(tmp_path):
    nota = tmp_path / 'Nota.md'
    nota.write_text('# Título\nTexto.\n', encoding='utf-8')
    os.chmod(str(nota), 0o644)
    raw = nota.read_bytes()
    assert lines.guardar(nota, raw, lines.contenido(raw))
    assert nota.stat().st_mode & 0o777 == 0o644


@pytest.mark.skipif(os.name == 'nt', reason='Permisos POSIX')
def test_guardar_nota_nueva_respeta_la_mascara(tmp_path):
    anterior = os.umask(0o022)
    try:
        nota = tmp_path / 'Nueva.md'
        assert lines.guardar(nota, None, b'# Nueva\n')
    finally:
        os.umask(anterior)
    assert nota.stat().st_mode & 0o777 == 0o644


@pytest.mark.parametrize('separador', ['\x0c', '\u2028', '\x85', '\x0b'])
def test_rangos_cuentan_solo_saltos_de_linea_reales(separador):
    texto = '# Uno\nTexto' + separador + 'pegado de un PDF.\n## Dos\nFin.\n'
    salida = lines.render(texto).split('\n')
    rango = next(l for l in salida if l.endswith(': Dos'))
    inicio = int(re.search(r'Líneas (\d+)–', rango).group(1))
    assert salida[inicio - 1] == '## Dos'
    assert lines.contenido(lines.render(texto).encode('utf-8')) == lines.render(texto).encode('utf-8')


@pytest.mark.parametrize('contenedor', ['_archivo', '01_FUENTES', '.trash', 'venv'])
def test_boveda_dentro_de_carpeta_con_nombre_protegido(tmp_path, monkeypatch, contenedor):
    vault = tmp_path / contenedor / 'boveda'
    (vault / 'Notas').mkdir(parents=True)
    (vault / 'Notas/Apunte.md').write_text('# Apunte\nTexto.\n', encoding='utf-8')
    (vault / '01_FUENTES').mkdir()
    (vault / '01_FUENTES/Original.md').write_text('# Original\n', encoding='utf-8')
    assert [p.name for p in lines.archivos(vault)] == ['Apunte.md']
    assert lines.main(['check', '--vault', str(vault)]) == 1
    monkeypatch.chdir(vault)
    assert lines.main(['check', 'Notas/Apunte.md']) == 1
    assert lines.main(['check', '01_FUENTES/Original.md']) == 2


@pytest.mark.parametrize('carpeta', ['01_FUENTES', '00_CORE/logs/historial', '_archivo'])
def test_raiz_protegida_sigue_rechazada(tmp_path, carpeta):
    (tmp_path / carpeta).mkdir(parents=True)
    with pytest.raises(ValueError):
        list(lines.archivos(tmp_path / carpeta))
