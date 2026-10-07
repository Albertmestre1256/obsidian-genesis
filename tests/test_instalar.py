"""Comprueba conservación de datos y comportamiento de la instalación real."""
import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("instalar", RAIZ / "instalar.py")
instalar = importlib.util.module_from_spec(spec)
spec.loader.exec_module(instalar)


def foto(carpeta):
    return {p.relative_to(carpeta).as_posix(): p.read_bytes()
            for p in carpeta.rglob("*") if p.is_file()}


def ejecutar(destino, *args):
    return subprocess.run([sys.executable, str(RAIZ / "instalar.py"), str(destino)] + list(args),
                          capture_output=True, input="", text=True, encoding="utf-8")


def test_instala_y_preserva_notas_y_configuracion(tmp_path):
    vault = tmp_path / "Mi bóveda con espacios"
    (vault / ".obsidian").mkdir(parents=True)
    (vault / ".obsidian/app.json").write_bytes(b'{"propio": true}')
    (vault / "mi nota.md").write_bytes(b"Nota privada\r\n")
    antes = foto(vault)
    resultado = ejecutar(vault, "--yes")
    assert resultado.returncode == 0, resultado.stdout + resultado.stderr
    despues = foto(vault)
    assert all(despues[ruta] == contenido for ruta, contenido in antes.items())
    assert (vault / ".claude/skills/empezar/SKILL.md").is_file()
    assert "TODO BIEN" in resultado.stdout
    assert not (vault / ".obsidian/core-plugins.json").exists()
    assert not (vault / "tests").exists()


def test_reinstalar_es_idempotente(tmp_path):
    assert ejecutar(tmp_path, "--yes").returncode == 0
    antes = foto(tmp_path)
    assert ejecutar(tmp_path, "--yes").returncode == 0
    assert foto(tmp_path) == antes


def test_conflicto_no_copia_nada(tmp_path):
    (tmp_path / "Panel.md").write_text("Mi panel", encoding="utf-8")
    antes = foto(tmp_path)
    resultado = ejecutar(tmp_path, "--yes")
    assert resultado.returncode == 2
    assert "Panel.md" in resultado.stdout
    assert foto(tmp_path) == antes


def test_archivo_en_lugar_de_carpeta(tmp_path):
    (tmp_path / "DOCS").write_bytes(b"no es una carpeta")
    antes = foto(tmp_path)
    assert ejecutar(tmp_path, "--yes").returncode == 2
    assert foto(tmp_path) == antes


def test_simulacion_no_escribe(tmp_path):
    assert ejecutar(tmp_path, "--dry-run").returncode == 0
    assert foto(tmp_path) == {}


def test_sin_confirmacion_no_escribe(tmp_path):
    assert ejecutar(tmp_path).returncode == 2
    assert foto(tmp_path) == {}


def test_destino_inexistente_no_se_crea(tmp_path):
    destino = tmp_path / "no-existe"
    assert ejecutar(destino, "--yes").returncode == 1
    assert not destino.exists()


def test_no_instala_en_si_mismo_ni_en_subcarpeta(tmp_path):
    origen = tmp_path / "kit"
    hijo = origen / "vault"
    hijo.mkdir(parents=True)
    for destino in (origen, hijo, tmp_path):
        with pytest.raises(ValueError, match="separadas"):
            instalar.planificar(destino, origen)


def test_archivo_creado_despues_del_plan_no_se_pisa(tmp_path):
    fuente = tmp_path / "fuente"
    destino = tmp_path / "destino"
    fuente.write_bytes(b"kit")
    destino.write_bytes(b"edicion simultanea")
    with pytest.raises(FileExistsError):
        instalar.copiar_nuevos([(fuente, destino)])
    assert destino.read_bytes() == b"edicion simultanea"


@pytest.mark.parametrize("fallo", [OSError, KeyboardInterrupt])
def test_copia_interrumpida_se_puede_reintentar(tmp_path, monkeypatch, fallo):
    vault = tmp_path / "vault"
    vault.mkdir()
    nota = vault / "mi-nota.md"
    nota.write_bytes(b"contenido privado")
    _, nuevos, _, conflictos = instalar.planificar(vault)
    assert not conflictos
    copiar = instalar.shutil.copyfileobj
    intentos = []

    def fallar_en_segundo_archivo(entrada, salida):
        intentos.append(salida.name)
        if len(intentos) == 2:
            salida.write(entrada.read(4))
            raise fallo("copia interrumpida")
        return copiar(entrada, salida)

    with monkeypatch.context() as parche:
        parche.setattr(instalar.shutil, "copyfileobj", fallar_en_segundo_archivo)
        with pytest.raises(fallo):
            instalar.copiar_nuevos(nuevos)
    assert nuevos[0][1].read_bytes() == nuevos[0][0].read_bytes()
    assert not nuevos[1][1].exists()
    assert nota.read_bytes() == b"contenido privado"

    _, pendientes, iguales, conflictos = instalar.planificar(vault)
    assert not conflictos
    assert len(iguales) == 1
    instalar.copiar_nuevos(pendientes)
    assert all(objetivo.read_bytes() == fuente.read_bytes() for fuente, objetivo in nuevos)
    assert nota.read_bytes() == b"contenido privado"


def test_padre_archivo_se_informa_como_conflicto_tambien_en_posix(tmp_path, monkeypatch):
    """En POSIX lstat(hijo de archivo) lanza ENOTDIR, no FileNotFoundError."""
    (tmp_path / "DOCS").write_bytes(b"archivo personal")
    original_lstat = Path.lstat

    def simular_posix(path, *args, **kwargs):
        if tmp_path / "DOCS" in path.parents:
            raise NotADirectoryError(str(path))
        return original_lstat(path, *args, **kwargs)

    monkeypatch.setattr(Path, "lstat", simular_posix)
    _, _, _, conflictos = instalar.planificar(tmp_path)
    assert any(ruta.startswith("DOCS/") for ruta in conflictos)
    assert (tmp_path / "DOCS").read_bytes() == b"archivo personal"


def test_enlace_en_destino_se_rechaza(tmp_path):
    externo = tmp_path / "externo"
    externo.mkdir()
    vault = tmp_path / "vault"
    vault.mkdir()
    try:
        (vault / "DOCS").symlink_to(externo, target_is_directory=True)
    except OSError:
        pytest.skip("El sistema no permite crear symlinks sin privilegios")
    assert ejecutar(vault, "--yes").returncode == 1
    assert foto(externo) == {}


def test_informa_error_en_celula_preexistente_sin_alterarla(tmp_path):
    celulas = tmp_path / "00_CORE/cells"
    celulas.mkdir(parents=True)
    nota = celulas / "mio-context.md"
    nota.write_bytes(b"contenido incompleto")
    resultado = ejecutar(tmp_path, "--yes")
    assert resultado.returncode == 1
    assert "se agregaron" in resultado.stdout
    assert nota.read_bytes() == b"contenido incompleto"


@pytest.mark.skipif(os.name != "nt", reason="Junctions de Windows")
def test_junction_en_destino_se_rechaza(tmp_path):
    externo = tmp_path / "externo"
    externo.mkdir()
    vault = tmp_path / "vault"
    vault.mkdir()
    enlace = vault / "DOCS"
    resultado = subprocess.run(["cmd", "/c", "mklink", "/J", str(enlace), str(externo)],
                               capture_output=True)
    assert resultado.returncode == 0, resultado.stderr
    try:
        assert ejecutar(vault, "--yes").returncode == 1
        assert foto(externo) == {}
    finally:
        os.rmdir(str(enlace))  # Retira la junction, conserva el directorio externo.
