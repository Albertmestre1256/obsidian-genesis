"""Conservación, recuperación y confirmación de la vista simple opcional."""
from datetime import datetime
import json
import shutil

import pytest

from test_instalar import RAIZ, ejecutar, foto, instalar

CSS = '.obsidian/snippets/genesis-vista-simple.css'
APP = '.obsidian/appearance.json'
GRAPH = '.obsidian/graph.json'
SNIPPET = 'genesis-vista-simple'


@pytest.fixture
def vault(tmp_path):
    (tmp_path / '.obsidian/snippets').mkdir(parents=True)
    (tmp_path / 'nota.md').write_bytes(b'Mi nota original\r\n')
    (tmp_path / APP).write_text('{"theme":"moonstone","enabledCssSnippets":["propio"],"baseFontSize":18}', encoding='utf-8')
    (tmp_path / GRAPH).write_text('{"search":"tag:#estudio","showOrphans":false,"repelStrength":7}', encoding='utf-8')
    (tmp_path / '.obsidian/snippets/propio.css').write_bytes(b'/* estilo propio */\r\n')
    return tmp_path


def test_activacion_conserva_preferencias_y_se_puede_revertir(vault):
    before = foto(vault)
    result = ejecutar(vault, '--vista-simple', '--yes')
    assert result.returncode == 0, result.stdout + result.stderr
    expected = json.loads(before[APP])
    expected['enabledCssSnippets'].append(SNIPPET)
    assert json.loads((vault / APP).read_text(encoding='utf-8')) == expected
    assert (vault / GRAPH).read_bytes() == before[GRAPH]
    assert 'pendiente' in result.stdout.lower()
    assert (vault / 'nota.md').read_bytes() == before['nota.md']
    assert (vault / '.obsidian/snippets/propio.css').read_bytes() == before['.obsidian/snippets/propio.css']
    backups = list((vault / '.obsidian').glob('*.bak-*'))
    assert len(backups) == 1
    assert backups[0].read_bytes() == before[APP]
    (vault / APP).write_bytes(backups[0].read_bytes())
    backups[0].unlink()
    (vault / CSS).unlink()  # Esta ejecución lo creó, no existía antes.
    assert foto(vault / '.obsidian') == {k[len('.obsidian/'):]: v for k, v in before.items() if k.startswith('.obsidian/')}


def test_vista_nueva_no_respalda_archivos_que_no_existian(tmp_path):
    result = ejecutar(tmp_path, '--vista-simple', '--yes')
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads((tmp_path / APP).read_text()) == {'enabledCssSnippets': [SNIPPET]}
    assert json.loads((tmp_path / GRAPH).read_text()) == {'search': json.loads((RAIZ / GRAPH).read_text())['search']}
    assert (tmp_path / CSS).read_bytes() == (RAIZ / CSS).read_bytes()
    assert not list((tmp_path / '.obsidian').glob('*.bak-*'))
    for path in (APP, GRAPH, CSS):
        assert 'Creado (retirar al revertir): ' + str(tmp_path / path) in result.stdout


@pytest.mark.parametrize('path,value', [(APP, '[]'), (APP, 'null'), (APP, '{'),
    (APP, '{"enabledCssSnippets":null}'), (APP, '{"enabledCssSnippets":"propio"}'),
    (APP, '{"enabledCssSnippets":[7]}'), (GRAPH, '[]'), (GRAPH, '{"search":null}')])
def test_ajustes_incompatibles_no_dejan_copia_parcial(vault, path, value):
    (vault / path).write_text(value, encoding='utf-8')
    before = foto(vault)
    result = ejecutar(vault, '--vista-simple', '--yes')
    assert result.returncode == 2, result.stdout + result.stderr
    assert path in result.stdout
    assert foto(vault) == before


def test_css_distinto_impide_toda_escritura(vault):
    (vault / CSS).write_bytes(b'/* mi otro estilo */')
    before = foto(vault)
    result = ejecutar(vault, '--vista-simple', '--yes')
    assert result.returncode == 2
    assert CSS in result.stdout
    assert foto(vault) == before


def test_css_preexistente_identico_no_se_respalda_ni_se_marca_para_retirar(vault):
    shutil.copyfile(RAIZ / CSS, vault / CSS)
    before = (vault / CSS).read_bytes()
    result = ejecutar(vault, '--vista-simple', '--yes')
    assert result.returncode == 0, result.stdout + result.stderr
    assert (vault / CSS).read_bytes() == before
    assert not list((vault / '.obsidian/snippets').glob('*.bak-*'))
    assert 'Creado (retirar al revertir): ' + str(vault / CSS) not in result.stdout


def test_simulacion_y_falta_de_confirmacion_conservan_todo(vault):
    assert ejecutar(vault, '--yes').returncode == 0
    shutil.copyfile(RAIZ / CSS, vault / CSS)
    before = foto(vault)
    assert ejecutar(vault, '--vista-simple', '--dry-run').returncode == 0
    assert foto(vault) == before
    assert ejecutar(vault, '--vista-simple').returncode == 2
    assert foto(vault) == before


def test_repeticion_es_idempotente_y_respaldos_son_exclusivos(vault, monkeypatch):
    class RelojFijo(datetime):
        @classmethod
        def now(cls):
            return cls(2026, 10, 18, 6, 0, 0)

    monkeypatch.setattr(instalar, 'datetime', RelojFijo)
    original = (vault / APP).read_bytes()
    assert instalar.main([str(vault), '--vista-simple', '--yes']) == 0
    before = foto(vault)
    assert instalar.main([str(vault), '--vista-simple', '--yes']) == 0
    assert foto(vault) == before
    second = b'{"enabledCssSnippets":["otro"]}'
    (vault / APP).write_bytes(second)
    assert instalar.main([str(vault), '--vista-simple', '--yes']) == 0
    assert {p.read_bytes() for p in (vault / '.obsidian').glob('*.bak-*')} == {original, second}


def test_edicion_ajena_tras_plan_se_conserva(vault, monkeypatch):
    copy = instalar.copiar_nuevos
    own = b'{"theme":"edicion posterior"}'

    def editar_durante_copia(new):
        copy(new)
        (vault / APP).write_bytes(own)

    monkeypatch.setattr(instalar, 'copiar_nuevos', editar_durante_copia)
    assert instalar.main([str(vault), '--vista-simple', '--yes']) == 1
    assert (vault / APP).read_bytes() == own
    assert not list((vault / '.obsidian').glob('*.bak-*'))
