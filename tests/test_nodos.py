"""Jerarquía navegable, actualización local y protección de índices propios."""
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
from urllib.parse import unquote

import pytest
from test_indice import ROOT, guardar, indice, run


def nodo(root, folder, description='Colección de notas.', name='00 - Índice y Contexto.md'):
    return guardar(root, folder + '/' + name, '---\ntipo: indice-nodo\ndescripcion: ' +
                   json.dumps(description, ensure_ascii=False) + '\n---\n\n# ' + Path(folder).name +
                   '\n\n' + indice.NODO_INICIO + '\n' + indice.NODO_FIN + '\n')


def foto(root):
    return {p.relative_to(root).as_posix(): p.read_bytes() for p in root.rglob('*') if p.is_file()}


def comprobar_enlaces(root, indexes):
    for path in indexes:
        text = re.sub(r'\A---\n.*?\n---\n', '', path.read_text(encoding='utf-8'), flags=re.S)
        for link in re.findall(r'(?<!\\)\]\(([^)]+)\)', text):
            assert (path.parent / unquote(link)).is_file(), (path, link)
        for link in re.findall(r'\[\[([^\]|]+)', text):
            target = link.rstrip('\\') + '.md'
            assert (root / target).is_file(), (path, target)


def test_grafo_conecta_raices_entrada_mapa_padres_y_notas(tmp_path):
    guardar(tmp_path, 'LEER_PRIMERO.md', '# Leer primero\n[[INDICE]]\n')
    parent = nodo(tmp_path, 'Estudio', 'Preparar materias.')
    child = nodo(tmp_path, 'Estudio/Resúmenes', 'Resúmenes propios.')
    other = nodo(tmp_path, 'Trabajo', 'Organizar un trabajo.')
    note = guardar(tmp_path, 'Estudio/Resúmenes/Primera nota.md', '# Resumen\nTexto propio.\n')
    original = note.read_bytes()
    indice.actualizar(tmp_path)
    for top in (parent, other):
        text = top.read_text(encoding='utf-8')
        assert '[[LEER_PRIMERO|Leer primero]]' in text
        assert '[[INDICE|Mapa general]]' in text
    text = child.read_text(encoding='utf-8')
    assert '[[Estudio/00 - Índice y Contexto|Nodo padre]]' in text
    assert '[[Estudio/Resúmenes/Primera nota\\|Primera nota.md]]' in text
    assert 'LEER_PRIMERO' not in text  # alcanza mediante su padre y el mapa.
    assert note.read_bytes() == original
    comprobar_enlaces(tmp_path, [parent, child, other, tmp_path / 'INDICE.md'])
    assert indice.actualizar(tmp_path, comprobar=True)['estado'] == 'vigente'


def test_grafo_respeta_entrada_propia_existente(tmp_path):
    own = guardar(tmp_path, '00 - Leer primero.md', '# Reglas propias\nNo reemplazar.\n')
    guardar(tmp_path, 'LEER_PRIMERO.md', '# Entrada del kit\n')
    node = nodo(tmp_path, 'Proyecto')
    before = own.read_bytes()
    indice.actualizar(tmp_path)
    text = node.read_text(encoding='utf-8')
    assert '[[00 - Leer primero|Leer primero]]' in text and '[[LEER_PRIMERO' not in text
    assert own.read_bytes() == before


def test_grafo_no_inventa_entrada_que_no_existe(tmp_path):
    node = nodo(tmp_path, 'Notas')
    indice.actualizar(tmp_path)
    assert 'LEER_PRIMERO' not in node.read_text(encoding='utf-8')


def test_grafo_no_mezcla_notas_con_el_mismo_nombre(tmp_path):
    first = nodo(tmp_path, 'Materia A')
    second = nodo(tmp_path, 'Materia B')
    guardar(tmp_path, 'Materia A/Resumen.md', '# Tema A\n')
    guardar(tmp_path, 'Materia B/Resumen.md', '# Tema B\n')
    indice.actualizar(tmp_path)
    assert '[[Materia A/Resumen\\|Resumen.md]]' in first.read_text(encoding='utf-8')
    assert '[[Materia B/Resumen\\|Resumen.md]]' in second.read_text(encoding='utf-8')
    comprobar_enlaces(tmp_path, [first, second])


def test_alias_de_nodo_no_rompe_tablas_ni_oculta_vinculos(tmp_path):
    parent = nodo(tmp_path, 'Proyecto')
    child = nodo(tmp_path, 'Proyecto/Hijo')
    child.write_text(child.read_text(encoding='utf-8').replace('# Hijo', '# Tema | [otro] %% oculto %% <html>'), encoding='utf-8')
    indice.actualizar(tmp_path)
    block = parent.read_text(encoding='utf-8').split(indice.NODO_INICIO)[1].split(indice.NODO_FIN)[0]
    row = next(line for line in block.splitlines() if '[[Proyecto/Hijo/' in line)
    assert 'Contexto\\|Tema' in row and '&#37;&#37; oculto &#37;&#37; &lt;html&gt;]]' in row
    assert '[otro]' not in row and '%%' not in row and '<html>' not in row
    assert len(re.findall(r'(?<!\\)\|', row)) == 3
    comprobar_enlaces(tmp_path, [parent])


@pytest.mark.parametrize('cantidad', [3, 30])
def test_grafo_crece_conectado_sin_enlaces_entre_todas_las_notas(tmp_path, cantidad):
    guardar(tmp_path, 'LEER_PRIMERO.md', '# Entrada\n[[INDICE]]\n')
    roots, indexes, notes = [], [], []
    for i in range(cantidad):
        folder = 'Proyecto-{}'.format(i)
        roots.append(nodo(tmp_path, folder))
        indexes.append(nodo(tmp_path, folder + '/Temas'))
        indexes.append(nodo(tmp_path, folder + '/Temas/Resúmenes'))
        for j in range(10):
            notes.append(guardar(tmp_path, folder + '/Temas/Resúmenes/Nota-{}.md'.format(j), '# Nota\n'))
    indexes += roots
    indice.actualizar(tmp_path)
    # Aristas reales de los mapas locales, sin contar el catálogo redundante.
    edges = set()
    for path in indexes:
        for target in re.findall(r'\[\[([^\]|]+)', path.read_text(encoding='utf-8')):
            dest = tmp_path / (target.rstrip('\\') + '.md')
            assert dest.is_file()
            edges.add((path, dest))
    assert len(edges) == cantidad * 18  # 10 notas + 3 mapas + 4 padre/hijo + entrada.
    adjacency = {}
    for left, right in edges:
        adjacency.setdefault(left, set()).add(right)
        adjacency.setdefault(right, set()).add(left)
    seen, pending = set(), [tmp_path / 'LEER_PRIMERO.md']
    while pending:
        path = pending.pop()
        if path not in seen:
            seen.add(path)
            pending.extend(adjacency.get(path, ()) - seen)
    assert set(indexes + notes + [tmp_path / 'INDICE.md']) <= seen
    assert not any(left in notes and right in notes for left, right in edges)
    assert indice.actualizar(tmp_path, comprobar=True)['estado'] == 'vigente'


def test_jerarquia_enlaza_todos_los_nodos_sin_duplicar_subarboles(tmp_path):
    study = nodo(tmp_path, 'Estudio', 'Organizar las materias.')
    summaries = nodo(tmp_path, 'Estudio/Resúmenes', 'Resúmenes por materia.')
    anatomy = nodo(tmp_path, 'Estudio/Resúmenes/Anatomía', 'Estructura del cuerpo.')
    note = guardar(tmp_path, 'Estudio/Resúmenes/Anatomía/Corazón.md',
                   '---\ndescripcion: Cavidades y circulación cardíaca.\n---\n# Corazón\n')
    source = guardar(tmp_path, 'Estudio/Resúmenes/Anatomía/materiales/original.txt', 'No modificar.\n')
    originals = note.read_bytes(), source.read_bytes()
    assert indice.actualizar(tmp_path)['estado'] == 'actualizado'
    general = (tmp_path / 'INDICE.md').read_text(encoding='utf-8').split('## Mapa de nodos')[1].split('## Catálogo completo')[0]
    assert 'Estudio/Resúmenes/Anatomía' in general and 'Resúmenes por materia.' in general
    assert 'Corazón.md' not in study.read_text(encoding='utf-8')
    assert 'Corazón.md' not in summaries.read_text(encoding='utf-8')
    text = anatomy.read_text(encoding='utf-8')
    assert 'Cavidades y circulación cardíaca.' in text and 'materiales/original.txt' in text
    assert originals == (note.read_bytes(), source.read_bytes())
    comprobar_enlaces(tmp_path, [study, summaries, anatomy, tmp_path / 'INDICE.md'])
    assert indice.actualizar(tmp_path, comprobar=True)['estado'] == 'vigente'


def test_ampliar_nodo_actualiza_solo_bloques_afectados(tmp_path):
    first, other = nodo(tmp_path, 'Resúmenes'), nodo(tmp_path, 'Trabajo')
    indice.actualizar(tmp_path)
    untouched = other.read_bytes()
    local_before = first.read_bytes()
    guardar(tmp_path, 'Resúmenes/Materia nueva.md', '---\ndescripcion: Conceptos del programa.\n---\n# Materia\n')
    before = foto(tmp_path)
    assert run(tmp_path, '--comprobar').returncode == 1
    assert foto(tmp_path) == before
    assert run(tmp_path).returncode == 0
    assert other.read_bytes() == untouched and first.read_bytes() != local_before
    after = foto(tmp_path)
    assert run(tmp_path).returncode == 0 and foto(tmp_path) == after


def test_resumen_cambiado_refresca_indice_local_y_general(tmp_path):
    path = nodo(tmp_path, 'Notas')
    note = guardar(tmp_path, 'Notas/Nota.md', '---\ndescripcion: Primera versión.\n---\n# Nota\n')
    indice.actualizar(tmp_path)
    note.write_text('---\ndescripcion: Contenido ampliado.\n---\n# Nota\n', encoding='utf-8')
    assert indice.actualizar(tmp_path, comprobar=True)['estado'] == 'desactualizado'
    indice.actualizar(tmp_path)
    assert 'Contenido ampliado.' in path.read_text(encoding='utf-8')
    assert 'Contenido ampliado.' in (tmp_path / 'INDICE.md').read_text(encoding='utf-8')


def test_indice_manual_se_conserva_y_se_identifica(tmp_path):
    path = guardar(tmp_path, 'Colección/Entrada propia.md',
                   '---\ntipo: indice-nodo\ndescripcion: Índice del usuario.\n---\n# Mi mapa\nTexto propio.\n')
    before = path.read_bytes()
    result = indice.actualizar(tmp_path)
    assert result['indices_manuales'] == ['Colección/Entrada propia.md']
    assert path.read_bytes() == before
    assert 'Entrada%20propia.md' in (tmp_path / 'INDICE.md').read_text(encoding='utf-8')


@pytest.mark.parametrize('block', [indice.NODO_INICIO, indice.NODO_FIN,
    indice.NODO_FIN + '\n' + indice.NODO_INICIO,
    indice.NODO_INICIO + '\n' + indice.NODO_INICIO + '\n' + indice.NODO_FIN])
def test_marcadores_invalidos_no_modifican_ningun_indice(tmp_path, block):
    nodo(tmp_path, 'Válido')
    path = nodo(tmp_path, 'Roto')
    path.write_text('---\ntipo: indice-nodo\n---\n# Roto\n' + block, encoding='utf-8')
    before = foto(tmp_path)
    assert run(tmp_path).returncode == 2
    assert foto(tmp_path) == before


def test_dos_indices_en_la_misma_carpeta_requieren_eleccion(tmp_path):
    nodo(tmp_path, 'Colección')
    nodo(tmp_path, 'Colección', name='Otro índice.md')
    before = foto(tmp_path)
    assert run(tmp_path).returncode == 2 and foto(tmp_path) == before


@pytest.mark.parametrize('newline', [b'\n', b'\r\n'])
def test_conserva_saltos_y_resumenes_manuales(tmp_path, newline):
    path = nodo(tmp_path, 'Fuentes')
    source = guardar(tmp_path, 'Fuentes/original.txt', 'Texto fuente intacto.\n')
    prefix = path.read_bytes().split(indice.NODO_INICIO.encode())[0].replace(b'\n', newline)
    suffix = '\n## Resúmenes manuales\n[Fuente](original.txt): resumen escrito por la persona.\n'.encode('utf-8')
    path.write_bytes(prefix + indice.NODO_INICIO.encode() + newline + indice.NODO_FIN.encode() + suffix)
    before_source = source.read_bytes()
    indice.actualizar(tmp_path)
    after = path.read_bytes()
    assert after.startswith(prefix) and after.endswith(suffix)
    block = after.split(indice.NODO_INICIO.encode())[1].split(indice.NODO_FIN.encode())[0]
    assert b'\n' not in block.replace(b'\r\n', b'') if newline == b'\r\n' else b'\r' not in block
    assert source.read_bytes() == before_source
    assert indice.actualizar(tmp_path, comprobar=True)['estado'] == 'vigente'


def test_sin_descripcion_no_inventa_un_resumen(tmp_path):
    path = nodo(tmp_path, 'Notas')
    guardar(tmp_path, 'Notas/Nota.md', '# Tema\nEl cuerpo no se resume automáticamente.\n')
    indice.actualizar(tmp_path)
    text = path.read_text(encoding='utf-8')
    assert 'Sin resumen; Tema' in text and 'El cuerpo no se resume' not in text


def test_enlaces_especiales_y_nombres_de_indices_libres(tmp_path):
    path = nodo(tmp_path, 'Colección [nueva]', 'Contenido con | barras y [enlaces](orden).', 'Mapa #1.md')
    child = nodo(tmp_path, 'Colección [nueva]/Hijo', name='Entrar.md')
    guardar(tmp_path, 'Colección [nueva]/Hijo/Nota #1%.md', '# Nota\n')
    indice.actualizar(tmp_path)
    comprobar_enlaces(tmp_path, [path, child, tmp_path / 'INDICE.md'])
    text = path.read_text(encoding='utf-8')
    assert 'Entrar.md' in text
    assert 'Mapa%20%231.md' in child.read_text(encoding='utf-8')


def test_proyecto_es_nodo_y_reintento_conserva_indice_generado(tmp_path):
    vault = tmp_path / 'vault'
    shutil.copytree(ROOT / '00_CORE', vault / '00_CORE', ignore=shutil.ignore_patterns('__pycache__'))
    data = {'nombre': 'Estudio', 'descripcion': 'Resumen: "dos materias".', 'objetivo': 'Preparar materias.',
            'contexto': 'D', 'fecha': '2026-10-08'}
    payload = guardar(tmp_path, 'datos.json', json.dumps(data, ensure_ascii=False))
    command = [sys.executable, '-B', str(ROOT / 'crear_proyecto.py'), '--destino', str(vault), '--datos', str(payload)]
    result = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0, result.stdout + result.stderr
    path = vault / 'estudio/00 - Índice - estudio.md'
    assert '01_FUENTES/README.md' in path.read_text(encoding='utf-8')
    assert indice.metadatos(path)['descripcion'] == data['descripcion']
    before = foto(vault)
    repeated = subprocess.run(command, capture_output=True, text=True, encoding='utf-8')
    assert repeated.returncode == 0, repeated.stdout + repeated.stderr
    assert json.loads(repeated.stdout)['creados'] == [] and foto(vault) == before


def test_varios_niveles_catalogan_cada_archivo_una_vez(tmp_path, monkeypatch):
    for i in range(12):
        nodo(tmp_path, 'Estudio/Materia-' + str(i))
        for j in range(8):
            nodo(tmp_path, 'Estudio/Materia-{}/Tema-{}'.format(i, j))
            guardar(tmp_path, 'Estudio/Materia-{}/Tema-{}/Nota.md'.format(i, j), '# Nota\n')
    calls, original = [], indice.metadatos
    def counted(path):
        calls.append(path)
        return original(path)
    monkeypatch.setattr(indice, 'metadatos', counted)
    indice.actualizar(tmp_path)
    assert len(calls) == len(set(calls)) == 204
    assert indice.actualizar(tmp_path, comprobar=True)['estado'] == 'vigente'


def test_error_en_nodo_conserva_mapa_general_previo(tmp_path):
    nodo(tmp_path, 'Notas')
    indice.actualizar(tmp_path)
    path = nodo(tmp_path, 'Otro')
    path.write_text('---\ntipo: indice-nodo\n---\n' + indice.NODO_INICIO, encoding='utf-8')
    before = foto(tmp_path)
    assert run(tmp_path).returncode == 2 and foto(tmp_path) == before


def test_nodo_en_boveda_dentro_de_archivo_no_queda_manual(tmp_path):
    root = tmp_path / '_archivo' / 'boveda'
    guardar(root, 'INDICE.md', '# Mapa\n\n' + indice.INICIO + '\n' + indice.FIN + '\n')
    guardar(root, '00_CORE/atoms/00_vault-rules.md', '# Reglas\n')
    nodo(root, 'Coleccion')
    assert indice.actualizar(root)['indices_manuales'] == []
