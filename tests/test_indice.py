"""Catálogo real, frescura, conservación e integración de comandos."""
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
from urllib.parse import unquote

import pytest

ROOT = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('indice', ROOT / 'actualizar_indice.py')
indice = importlib.util.module_from_spec(spec)
spec.loader.exec_module(indice)


def guardar(root, rel, text):
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding='utf-8')
    return path


def run(root, *extra):
    return subprocess.run([sys.executable, '-B', str(ROOT / 'actualizar_indice.py'), str(root)] + list(extra),
                          capture_output=True, text=True, encoding='utf-8')


def test_catalogo_notas_adjuntos_y_enlaces_con_caracteres_especiales(tmp_path):
    note = guardar(tmp_path, 'viaje/Plan [final].md', '# Plan del viaje\n\nEste cuerpo no se copia.\n')
    attachment = tmp_path / 'viaje/foto.png'
    attachment.write_bytes(b'\x89PNG\xff\xfe\x00')
    indice.actualizar(tmp_path)
    records = indice.catalogo(tmp_path)
    assert {r['ruta'] for r in records} == {'viaje/Plan [final].md', 'viaje/foto.png', 'INDICE.md'}
    output = (tmp_path / 'INDICE.md').read_text(encoding='utf-8')
    assert 'Este cuerpo no se copia.' not in output
    for path in re.findall(r'\]\(([^)]+)\)', output):
        assert (tmp_path / unquote(path)).is_file()
    assert note.read_text(encoding='utf-8').endswith('Este cuerpo no se copia.\n')


def test_propiedad_renombrada_ejemplo_y_duplicados(tmp_path):
    guardar(tmp_path, '00_CORE/cells/renombrada.md', '---\ntipo: celula\nproyecto: "estudiar"\ndescripcion: "Preparar materias."\n---\n# Estudio\n')
    guardar(tmp_path, '00_CORE/cells/ejemplo.md', '---\ntipo: celula\nproyecto: "python"\nejemplo: true\n---\n# Ejemplo\n')
    guardar(tmp_path, 'Cursos/Entrada.md', '---\ntipo: indice-proyecto\nproyecto: "estudiar"\n---\n# Cursos\n')
    records = indice.catalogo(tmp_path)
    output = indice.bloque(records)
    own = output.split('## Proyectos propios\n', 1)[1].split('## Ejemplos ficticios', 1)[0]
    examples = output.split('## Ejemplos ficticios\n', 1)[1].split('## Catálogo completo', 1)[0]
    assert 'renombrada.md' in own and 'Cursos/Entrada.md' in own and 'ejemplo.md' not in own
    assert 'ejemplo.md' in examples and 'renombrada.md' not in examples
    guardar(tmp_path, '00_CORE/cells/otra.md', '---\ntipo: celula\nproyecto: "estudiar"\n---\n')
    assert 'identificadores repetidos' in indice.bloque(indice.catalogo(tmp_path))


@pytest.mark.parametrize('tipo', ['célula', ' CELULA '])
def test_indice_reconoce_tipo_admitido_en_ficha_renombrada(tmp_path, tipo):
    guardar(tmp_path, '00_CORE/cells/Estudio.md',
            '---\ntipo: ' + json.dumps(tipo, ensure_ascii=False) + '\nproyecto: estudiar\n---\n')
    indice.actualizar(tmp_path)
    text = (tmp_path / 'INDICE.md').read_text(encoding='utf-8')
    own = text.split('## Proyectos propios\n', 1)[1].split('## Ejemplos ficticios', 1)[0]
    assert 'estudiar' in own and 'Estudio.md' in own


def test_comprobar_no_escribe_y_actualizar_es_idempotente(tmp_path):
    guardar(tmp_path, 'nota.md', '# Mi nota\n')
    assert run(tmp_path, '--comprobar').returncode == 1
    assert not (tmp_path / 'INDICE.md').exists()
    assert run(tmp_path).returncode == 0
    before = (tmp_path / 'INDICE.md').read_bytes()
    assert run(tmp_path, '--comprobar').returncode == 0
    assert run(tmp_path).returncode == 0
    assert (tmp_path / 'INDICE.md').read_bytes() == before
    guardar(tmp_path, 'nota.md', '# Otro título\n')
    assert run(tmp_path, '--comprobar').returncode == 1
    assert (tmp_path / 'INDICE.md').read_bytes() == before
    assert run(tmp_path).returncode == 0


def test_conserva_comentarios_fuera_del_bloque(tmp_path):
    indice.actualizar(tmp_path)
    path = tmp_path / 'INDICE.md'
    original = path.read_text(encoding='utf-8')
    prefix = '# Presentación de la persona\n\n'
    suffix = '\n## Comentarios propios\nNo borrar esta aclaración.\n'
    path.write_bytes((prefix + original + suffix).encode('utf-8'))
    guardar(tmp_path, 'nueva.md', '# Nueva nota\n')
    indice.actualizar(tmp_path)
    after = path.read_text(encoding='utf-8')
    lines = indice.lineador()
    assert lines.sin_indice(after).startswith(lines.sin_indice(prefix + original, reubicar=True).split(indice.INICIO)[0])
    assert after.endswith(suffix) and 'nueva.md' in after


@pytest.mark.parametrize('newline', [b'\n', b'\r\n'], ids=['LF', 'CRLF'])
def test_frescura_y_actualizacion_conservan_saltos_y_comentarios(tmp_path, newline):
    indice.actualizar(tmp_path)
    path = tmp_path / 'INDICE.md'
    prefix = b'# Comentario personal\r\n\n'
    suffix = b'\n## Conservar literalmente\r\n'
    original = path.read_bytes().replace(b'\n', newline)
    before = prefix + original + suffix
    path.write_bytes(before)
    assert run(tmp_path, '--comprobar').returncode == 1  # Reubicar y recalcular el índice de líneas.
    assert path.read_bytes() == before

    guardar(tmp_path, 'nueva.md', '# Nueva nota\n')
    assert run(tmp_path, '--comprobar').returncode == 1
    assert path.read_bytes() == before
    assert run(tmp_path).returncode == 0
    after = path.read_bytes()
    start, end = indice.INICIO.encode('utf-8'), indice.FIN.encode('utf-8')
    lines = indice.lineador()
    without = lambda raw: lines.sin_indice(raw.decode('utf-8'), reubicar=True).encode('utf-8')
    assert without(after).split(start)[0] == without(before).split(start)[0]
    assert after.split(end)[1] == before.split(end)[1]
    block = after.split(start)[1].split(end)[0]
    assert b'nueva.md' in block
    if newline == b'\r\n':
        assert b'\n' not in block.replace(b'\r\n', b'')
    else:
        assert b'\r' not in block
    assert run(tmp_path, '--comprobar').returncode == 0
    assert run(tmp_path).returncode == 0
    assert path.read_bytes() == after


@pytest.mark.parametrize('text', ['# Índice propio\n', indice.FIN + '\n' + indice.INICIO,
                                       indice.INICIO + '\n' + indice.FIN + '\n' + indice.FIN])
def test_indice_incompatible_no_se_reemplaza(tmp_path, text):
    path = guardar(tmp_path, 'INDICE.md', text)
    before = path.read_bytes()
    result = run(tmp_path)
    assert result.returncode == 2
    assert path.read_bytes() == before


def test_excluye_secretos_caches_y_sesiones_sin_leerlos(tmp_path, monkeypatch):
    excluded = ['.env', 'credenciales.txt', 'llave.key', '.git/config', '__pycache__/a.pyc',
                '.obsidian/workspace.json', '.obsidian-mcp/registro.md', 'node_modules/nota.md']
    for rel in excluded:
        guardar(tmp_path, rel, 'SECRETO que no se debe leer')
    included = ['.obsidian/app.json', '.claude/skills/nota.md', '.gitignore', 'apunte.md']
    for rel in included:
        guardar(tmp_path, rel, '# Apunte\n')
    open_original = Path.open
    def guarded(path, *args, **kwargs):
        assert path.relative_to(tmp_path).as_posix() not in excluded
        return open_original(path, *args, **kwargs)
    monkeypatch.setattr(Path, 'open', guarded)
    records = indice.catalogo(tmp_path)
    assert {r['ruta'] for r in records} == set(included) | {'INDICE.md'}


def test_catalogo_incluye_opencode_y_omite_dependencias(tmp_path):
    guardar(tmp_path, '.opencode/commands/configurar.md',
            '---\ndescription: Iniciar con preguntas.\n---\n')
    guardar(tmp_path, '.opencode/node_modules/interno.md', '# No catalogar\n')
    records = indice.catalogo(tmp_path)
    assert {r['ruta'] for r in records} == {'.opencode/commands/configurar.md', 'INDICE.md'}
    command = next(r for r in records if r['ruta'].endswith('configurar.md'))
    assert command['grupo'] == 'Integración OpenCode'
    indice.actualizar(tmp_path)
    assert '.opencode/commands/configurar.md' in (tmp_path / 'INDICE.md').read_text(encoding='utf-8')
    assert indice.actualizar(tmp_path, comprobar=True)['estado'] == 'vigente'


def test_textos_de_notas_no_rompen_bloque_automatico(tmp_path):
    guardar(tmp_path, 'rara.md', '# Título | [texto] %% vault-index:end %%\n')
    indice.actualizar(tmp_path)
    assert indice.actualizar(tmp_path)['estado'] == 'vigente'


@pytest.mark.skipif(os.name != 'nt', reason='Junctions de Windows')
def test_no_sigue_junction_ni_reemplaza_indice(tmp_path):
    root = tmp_path / 'vault'
    root.mkdir()
    indice.actualizar(root)
    before = (root / 'INDICE.md').read_bytes()
    outside = tmp_path / 'otro'
    outside.mkdir()
    guardar(outside, 'privada.md', '# Privada\n')
    junction = root / 'externo'
    made = subprocess.run(['cmd', '/c', 'mklink', '/J', str(junction), str(outside)], capture_output=True)
    assert made.returncode == 0
    try:
        assert run(root).returncode == 2
        assert (root / 'INDICE.md').read_bytes() == before
    finally:
        os.rmdir(str(junction))


def test_instalacion_catalogo_del_destino_y_reinstalacion(tmp_path):
    guardar(tmp_path, 'apuntes/original.md', '# Nota previa\n')
    command = [sys.executable, '-B', str(ROOT / 'instalar.py'), str(tmp_path), '--yes']
    first = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    assert first.returncode == 0, first.stdout + first.stderr
    before = (tmp_path / 'INDICE.md').read_bytes()
    assert 'apuntes/original.md' in before.decode('utf-8')
    assert run(tmp_path, '--comprobar').returncode == 0
    assert subprocess.run(command, capture_output=True).returncode == 0
    assert (tmp_path / 'INDICE.md').read_bytes() == before


def test_instalacion_indice_propio_impide_copia(tmp_path):
    path = guardar(tmp_path, 'INDICE.md', '# Mi entrada propia\n')
    result = subprocess.run([sys.executable, '-B', str(ROOT / 'instalar.py'), str(tmp_path), '--yes'], capture_output=True)
    assert result.returncode == 1
    assert {p.name for p in tmp_path.iterdir()} == {'INDICE.md'}
    assert path.read_text(encoding='utf-8') == '# Mi entrada propia\n'


def test_creacion_cli_registra_proyecto_en_indice(tmp_path):
    vault = tmp_path / 'vault'
    shutil.copytree(ROOT / '00_CORE', vault / '00_CORE', ignore=shutil.ignore_patterns('__pycache__'))
    data = {'nombre': 'Organizar clases', 'descripcion': 'Ordenar apuntes.', 'objetivo': 'Encontrar mis apuntes.',
            'contexto': 'D', 'fecha': '2026-10-07'}
    payload = guardar(tmp_path, 'respuestas.json', json.dumps(data))
    result = subprocess.run([sys.executable, '-B', str(ROOT / 'crear_proyecto.py'), '--destino', str(vault),
                             '--datos', str(payload)], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)['indice_principal']['estado'] == 'actualizado'
    text = (vault / 'INDICE.md').read_text(encoding='utf-8')
    assert 'organizar-clases-context.md' in text and 'organizar-clases/00' in text
    assert run(vault, '--comprobar').returncode == 0


def test_creador_no_escribe_con_indice_incompatible(tmp_path):
    vault = tmp_path / 'vault'
    shutil.copytree(ROOT / '00_CORE', vault / '00_CORE', ignore=shutil.ignore_patterns('__pycache__'))
    guardar(vault, 'INDICE.md', '# Inicio propio\n')
    data = {'nombre': 'Nuevo', 'descripcion': 'Un proyecto.', 'objetivo': 'Ordenar notas.', 'contexto': 'D', 'fecha': '2026-10-07'}
    payload = guardar(tmp_path, 'respuestas.json', json.dumps(data))
    result = subprocess.run([sys.executable, '-B', str(ROOT / 'crear_proyecto.py'), '--destino', str(vault),
                             '--datos', str(payload)], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 1 and json.loads(result.stdout)['estado'] == 'bloqueado'
    assert not (vault / 'nuevo').exists()
    assert (vault / 'INDICE.md').read_text(encoding='utf-8') == '# Inicio propio\n'


def test_fallo_primera_escritura_retira_solo_archivo_incompleto(tmp_path, monkeypatch):
    original = tempfile.NamedTemporaryFile
    class Interrupted:
        def __init__(self, stream):
            self.stream = stream
        def __enter__(self):
            return self
        def __exit__(self, *args):
            self.stream.close()
        def fileno(self):
            return self.stream.fileno()
        def __getattr__(self, name):
            return getattr(self.stream, name)
        def write(self, data):
            self.stream.write(data[:16])
            raise OSError('Interrupción ficticia durante la escritura.')
    def patched(*args, **kwargs):
        return Interrupted(original(*args, **kwargs))
    with monkeypatch.context() as patch:
        patch.setattr(tempfile, 'NamedTemporaryFile', patched)
        with pytest.raises(OSError):
            indice.actualizar(tmp_path)
    assert not (tmp_path / 'INDICE.md').exists()
    assert indice.actualizar(tmp_path)['estado'] == 'actualizado'


def test_cambio_ajeno_antes_del_reemplazo_se_conserva(tmp_path, monkeypatch):
    indice.actualizar(tmp_path)
    path = tmp_path / 'INDICE.md'
    guardar(tmp_path, 'nueva.md', '# Nueva\n')
    original = indice.planificar
    def concurrent(root):
        plan = original(root)
        path.write_bytes(b'# Cambio concurrente de la persona\n')
        return plan
    monkeypatch.setattr(indice, 'planificar', concurrent)
    with pytest.raises(ValueError, match='cambió'):
        indice.actualizar(tmp_path)
    assert path.read_bytes() == b'# Cambio concurrente de la persona\n'
    assert not list(tmp_path.glob('.indice-*.tmp'))


def test_indice_distribuido_coincide_con_archivos_del_kit():
    assert indice.actualizar(ROOT, comprobar=True)['estado'] == 'vigente'


def test_checkout_de_claude_no_duplica_proyectos_en_indice(tmp_path):
    guardar(tmp_path, '.claude/worktrees/otra-copia/00_CORE/cells/otro.md',
            '---\ntipo: celula\nproyecto: otro\n---\n')
    guardar(tmp_path, '.claude/skills/configurar/SKILL.md', '# Configurar\n')
    guardar(tmp_path, 'investigacion/worktrees/nota.md', '# Nota propia\n')
    records = indice.catalogo(tmp_path)
    paths = {r['ruta'] for r in records}
    assert '.claude/skills/configurar/SKILL.md' in paths
    assert 'investigacion/worktrees/nota.md' in paths
    assert not any(p.startswith('.claude/worktrees/') for p in paths)
    assert 'otro' not in indice.bloque(records).split('## Ejemplos ficticios')[0]


def test_etiquetas_distinguen_archivos_repetidos_y_conservan_destinos(tmp_path):
    paths = ['proyecto/a/README.md', 'proyecto/b/README.md',
             'proyecto/x/a/SKILL.md', 'proyecto/y/a/SKILL.md',
             'proyecto/Nota.md', 'proyecto/sub/nota.md', 'proyecto/Plan [final].md']
    for path in paths:
        guardar(tmp_path, path, '# Nota\n')
    records = indice.catalogo(tmp_path)
    labels = indice.etiquetas(records)
    assert labels['proyecto/a/README.md'] == 'a/README.md'
    assert labels['proyecto/b/README.md'] == 'b/README.md'
    assert labels['proyecto/x/a/SKILL.md'] == 'x/a/SKILL.md'
    assert labels['proyecto/y/a/SKILL.md'] == 'y/a/SKILL.md'
    assert labels['proyecto/Nota.md'] == 'proyecto/Nota.md'
    assert labels['proyecto/sub/nota.md'] == 'sub/nota.md'
    indice.actualizar(tmp_path)
    text = (tmp_path / 'INDICE.md').read_text(encoding='utf-8')
    assert {unquote(p) for p in re.findall(r'\]\(([^)]+)\)', text)} == set(paths) | {'INDICE.md'}
    assert indice.actualizar(tmp_path, comprobar=True)['estado'] == 'vigente'


def test_indice_del_proyecto_normaliza_tipo_como_la_ficha(tmp_path):
    guardar(tmp_path, '00_CORE/cells/Estudio.md', '---\ntipo: Célula\nproyecto: estudio\n---\n')
    guardar(tmp_path, 'Estudio/Entrada.md', '---\ntipo: " ÍNDICE-PROYECTO "\nproyecto: estudio\n---\n')
    text = indice.bloque(indice.catalogo(tmp_path))
    own = text.split('## Proyectos propios\n', 1)[1].split('## Ejemplos ficticios', 1)[0]
    assert 'Estudio/Entrada.md' in own
    assert 'Sin índice identificado' not in own
