"""La política compartida se carga del kit propio antes de revisar una bóveda."""
import importlib.util
import os
from pathlib import Path
import shutil
import subprocess
import sys
import types

import pytest

ROOT = Path(__file__).resolve().parent.parent
ENTRADAS = ['actualizar_indice.py', 'crear_proyecto.py', '00_CORE/schemas/note_index.py']
COMPARTIDO = '00_CORE/schemas/rutas_boveda.py'


def cargar(path):
    # El importador de la prueba equivale a -B; no mide la caché de su propio entrypoint.
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location('herramienta_rutas_test', path)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(params=ENTRADAS)
def kit(tmp_path, request):
    root = tmp_path / 'Kit de prueba'
    for rel in [request.param, COMPARTIDO]:
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / rel, path)
    (root / 'INDICE.md').write_text('# Mapa\n', encoding='utf-8')
    reglas = root / '00_CORE/atoms/00_vault-rules.md'
    reglas.parent.mkdir(parents=True)
    reglas.write_text('# Reglas\n', encoding='utf-8')
    return root, root / request.param


def foto(root):
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob('*') if p.is_file()}


def enlazar(link, target, directorio=False):
    try:
        link.symlink_to(target, target_is_directory=directorio)
    except OSError:
        if not directorio or os.name != 'nt':
            pytest.skip('La cuenta no permite crear este enlace')
        result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(target)],
                                capture_output=True)
        if result.returncode:
            pytest.skip('La cuenta no permite crear junctions')


def desenlazar(link):
    if link.is_symlink():
        link.unlink()
    else:
        link.rmdir()  # retira solo el junction, no el directorio al que apunta


def test_biblioteca_ausente_conserva_el_kit(kit):
    root, entrada = kit
    (root / COMPARTIDO).unlink()
    antes = foto(root)
    with pytest.raises(FileNotFoundError):
        cargar(entrada)
    assert foto(root) == antes


def test_biblioteca_enlazada_no_ejecuta_codigo(kit, tmp_path):
    root, entrada = kit
    marca = tmp_path / 'codigo-ajeno-ejecutado'
    ajeno = tmp_path / 'ajeno.py'
    ajeno.write_text('from pathlib import Path\nPath({!r}).touch()\n'.format(str(marca)),
                     encoding='utf-8')
    link = root / COMPARTIDO
    link.unlink()
    enlazar(link, ajeno)
    antes = foto(root)
    try:
        with pytest.raises(ValueError, match='enlaces|junctions'):
            cargar(entrada)
        assert not marca.exists() and foto(root) == antes
    finally:
        desenlazar(link)


def test_directorio_de_biblioteca_redirigido_no_ejecuta_codigo(kit, tmp_path):
    root, entrada = kit
    schemas = root / '00_CORE/schemas'
    ajeno = tmp_path / 'bibliotecas redirigidas'
    schemas.rename(ajeno)
    marca = tmp_path / 'codigo-ajeno-ejecutado'
    (ajeno / 'rutas_boveda.py').write_text(
        'from pathlib import Path\nPath({!r}).touch()\n'.format(str(marca)), encoding='utf-8')
    enlazar(schemas, ajeno, directorio=True)
    antes = foto(root)
    try:
        with pytest.raises(ValueError, match='enlaces|junctions'):
            cargar(entrada)
        assert not marca.exists() and foto(root) == antes
    finally:
        desenlazar(schemas)


@pytest.mark.parametrize('tag,rechazado', [(None, True), (0xA0000003, True),
                                          (0, False), (0x9000001A, False)])
def test_arranque_distingue_redireccion_de_archivo_de_nube(kit, monkeypatch, tag, rechazado):
    root, entrada = kit
    biblioteca = root / COMPARTIDO
    original = Path.lstat
    antes = foto(root)

    def estado(path, *args, **kwargs):
        info = original(path, *args, **kwargs)
        if path == biblioteca:
            return types.SimpleNamespace(st_mode=info.st_mode, st_file_attributes=0x400,
                                         st_reparse_tag=tag)
        return info

    with monkeypatch.context() as patch:
        patch.setattr(Path, 'lstat', estado)
        if rechazado:
            with pytest.raises(ValueError, match='enlaces|junctions'):
                cargar(entrada)
        else:
            modulo = cargar(entrada)
            assert modulo.raiz_boveda(root) == root
    assert foto(root) == antes


def test_nombre_ajeno_en_cwd_y_sys_modules_no_sustituye_la_biblioteca(kit, tmp_path, monkeypatch):
    root, entrada = kit
    ajeno = tmp_path / 'directorio actual'
    ajeno.mkdir()
    (ajeno / 'rutas_boveda.py').write_text('raise RuntimeError("No cargar desde cwd")\n',
                                         encoding='utf-8')

    def prohibido(*args, **kwargs):
        raise RuntimeError('No usar biblioteca ajena')

    veneno = types.SimpleNamespace(es_enlace=prohibido, raiz_boveda=prohibido, ruta_real=prohibido)
    monkeypatch.setitem(sys.modules, 'rutas_boveda_kit', veneno)
    monkeypatch.setitem(sys.modules, 'rutas_boveda', veneno)
    monkeypatch.syspath_prepend(str(ajeno))
    monkeypatch.chdir(ajeno)
    antes = foto(root)
    modulo = cargar(entrada)
    # Conservar también los argumentos con nombre de cada herramienta existente.
    parametro = 'path' if entrada.name == 'note_index.py' else 'ruta'
    assert modulo.raiz_boveda(**{parametro: root}) == root
    assert modulo.ruta_real(**{parametro: root / 'nota-nueva.md', 'raiz': root}) == root / 'nota-nueva.md'
    assert foto(root) == antes


def test_enlace_por_encima_del_kit_no_se_confunde_con_enlace_interno(kit, tmp_path):
    root, entrada = kit
    link = tmp_path / 'acceso al contenedor'
    enlazar(link, root.parent, directorio=True)
    try:
        acceso = link / root.name
        modulo = cargar(acceso / entrada.relative_to(root))
        assert modulo.raiz_boveda(acceso) == acceso
        assert modulo.ruta_real(acceso / 'nota-nueva.md') == acceso / 'nota-nueva.md'
        assert not list(root.rglob('__pycache__'))
    finally:
        desenlazar(link)
