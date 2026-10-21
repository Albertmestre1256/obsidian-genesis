"""Distribución real de las skills: traslado, preservación y conflictos."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys

import pytest

RAIZ = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location('instalar_skills', RAIZ / 'instalar_skills.py')
instalador = importlib.util.module_from_spec(spec)
spec.loader.exec_module(instalador)


def boveda(path):
    path.mkdir(parents=True)
    (path / 'INDICE.md').write_text('# Mapa', encoding='utf-8')
    reglas = path / '00_CORE/atoms/00_vault-rules.md'
    reglas.parent.mkdir(parents=True)
    reglas.write_text('# Reglas', encoding='utf-8')
    return path


@pytest.mark.parametrize('asistente', sorted(instalador.DESTINOS))
def test_instala_conserva_otras_skills_y_reintenta(tmp_path, asistente):
    destino = boveda(tmp_path / 'Bóveda con espacios')
    carpeta = destino / instalador.DESTINOS[asistente]
    propia = carpeta / 'mi-skill/SKILL.md'
    propia.parent.mkdir(parents=True)
    propia.write_bytes(b'skill del usuario')
    assert instalador.main([str(destino), '--asistente', asistente]) == 0
    assert list(carpeta.rglob('SKILL.md')) == [propia]
    assert instalador.main([str(destino), '--asistente', asistente, '--yes']) == 0
    for nombre in instalador.SKILLS:
        assert (carpeta / nombre / 'SKILL.md').read_bytes() == (RAIZ / 'skills' / nombre / 'SKILL.md').read_bytes()
    assert propia.read_bytes() == b'skill del usuario'
    antes = {p: p.stat().st_mtime_ns for p in carpeta.rglob('*') if p.is_file()}
    assert instalador.main([str(destino), '--asistente', asistente, '--yes']) == 0
    assert antes == {p: p.stat().st_mtime_ns for p in antes}


def test_una_personalizacion_impide_todo_el_lote(tmp_path):
    destino = boveda(tmp_path / 'boveda')
    carpeta = destino / '.agents/skills'
    personalizada = carpeta / 'vault-token-optimizer/SKILL.md'
    personalizada.parent.mkdir(parents=True)
    personalizada.write_bytes(b'contenido personalizado')
    assert instalador.main([str(destino), '--asistente', 'codex', '--yes']) == 2
    assert list(carpeta.rglob('SKILL.md')) == [personalizada]
    assert personalizada.read_bytes() == b'contenido personalizado'


def test_destino_ajeno_no_se_convierte_en_genesis(tmp_path):
    destino = tmp_path / 'notas-existentes'
    destino.mkdir()
    assert instalador.main([str(destino), '--asistente', 'claude', '--yes']) == 2
    assert list(destino.iterdir()) == []


def test_trasladar_paquete_copia_recursos_y_no_depende_del_original(tmp_path):
    fuente = tmp_path / 'Paquete trasladado'
    shutil.copytree(RAIZ / 'skills', fuente / 'skills')
    shutil.copy2(RAIZ / 'instalar_skills.py', fuente / 'instalar_skills.py')
    recurso = fuente / 'skills/volcar/references/convenciones.md'
    recurso.parent.mkdir()
    recurso.write_text('Reglas locales del usuario', encoding='utf-8')
    destino = boveda(tmp_path / 'Segunda ubicación')
    proceso = subprocess.run([sys.executable, str(fuente / 'instalar_skills.py'), str(destino),
                              '--asistente', 'codex', '--yes'], cwd=tmp_path,
                             capture_output=True, text=True, encoding='utf-8')
    assert proceso.returncode == 0, proceso.stderr
    assert (destino / '.agents/skills/volcar/references/convenciones.md').read_bytes() == recurso.read_bytes()
    assert not list(fuente.rglob('__pycache__'))


def test_carpeta_ocupada_no_deja_instalacion_parcial(tmp_path):
    destino = boveda(tmp_path / 'boveda')
    ocupada = destino / '.claude/skills/vault-token-optimizer'
    ocupada.parent.mkdir(parents=True)
    ocupada.write_bytes(b'archivo conservado')
    assert instalador.main([str(destino), '--asistente', 'claude', '--yes']) == 2
    assert list(ocupada.parent.iterdir()) == [ocupada]


def test_enlace_de_destino_no_escribe_fuera(tmp_path):
    destino = boveda(tmp_path / 'boveda')
    exterior = tmp_path / 'fuera'
    exterior.mkdir()
    try:
        (destino / '.claude').symlink_to(exterior, target_is_directory=True)
    except OSError:
        if os.name != 'nt':
            pytest.skip('La plataforma no permite crear enlaces en esta cuenta')
        junction = subprocess.run(['cmd', '/c', 'mklink', '/J', str(destino / '.claude'), str(exterior)],
                                  capture_output=True)
        if junction.returncode:
            pytest.skip('La cuenta no permite crear enlaces ni junctions')
    try:
        assert instalador.main([str(destino), '--asistente', 'claude', '--yes']) == 2
        assert list(exterior.iterdir()) == []
    finally:
        enlace = destino / '.claude'
        os.unlink(str(enlace)) if enlace.is_symlink() else os.rmdir(str(enlace))


def test_conflicto_aparecido_al_escribir_se_conserva(tmp_path, monkeypatch, capsys):
    destino = boveda(tmp_path / 'boveda')
    original = Path.open
    ocupada = destino / '.agents/skills/volcar/SKILL.md'

    def abrir(path, mode='r', *args, **kwargs):
        if path == ocupada and mode == 'xb':
            with original(path, 'wb') as stream:
                stream.write(b'edicion concurrente')
        return original(path, mode, *args, **kwargs)

    monkeypatch.setattr(Path, 'open', abrir)
    assert instalador.main([str(destino), '--asistente', 'codex', '--yes']) == 2
    assert ocupada.read_bytes() == b'edicion concurrente'
    assert (destino / '.agents/skills/inicio/SKILL.md').is_file()
    assert 'parcial' in capsys.readouterr().err


def test_catalogo_incluye_codex_y_lineador_conserva_su_formato(tmp_path):
    destino = boveda(tmp_path / 'boveda')
    shutil.copy2(RAIZ / 'INDICE.md', destino / 'INDICE.md')
    skill = destino / '.agents/skills/propia/SKILL.md'
    skill.parent.mkdir(parents=True)
    skill.write_text('---\nname: propia\ndescription: Skill personalizada\n---\nTexto sin índice\n', encoding='utf-8')
    spec_indice = importlib.util.spec_from_file_location('mapa_skills', RAIZ / 'actualizar_indice.py')
    mapa = importlib.util.module_from_spec(spec_indice)
    spec_indice.loader.exec_module(mapa)
    assert mapa.main([str(destino)]) == 0
    assert '.agents/skills/propia/SKILL.md' in (destino / 'INDICE.md').read_text(encoding='utf-8')
    spec_lineas = importlib.util.spec_from_file_location('lineas_skills', RAIZ / '00_CORE/schemas/note_index.py')
    lineas = importlib.util.module_from_spec(spec_lineas)
    spec_lineas.loader.exec_module(lineas)
    assert lineas.protegida(skill)
    antes = skill.read_bytes()
    assert lineas.main(['apply', str(skill)]) == 2
    assert skill.read_bytes() == antes


def test_boveda_bajo_enlace_externo_se_instala(tmp_path):
    real = tmp_path / 'real'
    real.mkdir()
    boveda(real / 'boveda')
    enlace = tmp_path / 'enlace'
    try:
        enlace.symlink_to(real, target_is_directory=True)
    except OSError:
        if os.name != 'nt' or subprocess.run(['cmd', '/c', 'mklink', '/J', str(enlace), str(real)],
                                             capture_output=True).returncode:
            pytest.skip('La cuenta no permite crear enlaces ni junctions')
    try:
        assert instalador.main([str(enlace / 'boveda'), '--asistente', 'claude', '--yes']) == 0
        assert (real / 'boveda/.claude/skills/inicio/SKILL.md').is_file()
    finally:
        os.unlink(str(enlace)) if enlace.is_symlink() else os.rmdir(str(enlace))
