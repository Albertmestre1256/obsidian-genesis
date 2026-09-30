"""Configuración compartida de las pruebas."""
import importlib.util
from pathlib import Path

import pytest

RAIZ = Path(__file__).resolve().parent.parent
CELLS = RAIZ / "00_CORE" / "cells"


def _cargar_validador():
    spec = importlib.util.spec_from_file_location("validate", RAIZ / "00_CORE" / "schemas" / "validate.py")
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


@pytest.fixture(scope="session")
def validador():
    return _cargar_validador()


@pytest.fixture(scope="session")
def ejemplo():
    """Texto de la célula de ejemplo: es la base de casi todos los casos."""
    return (CELLS / "ejemplo-context.md").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def plantilla():
    return (CELLS / "TEMPLATE_cell.md").read_text(encoding="utf-8")


@pytest.fixture
def revisar(validador, tmp_path):
    """Escribe una célula y devuelve (errores, avisos)."""
    def _revisar(texto, nombre="prueba-context.md", encoding="utf-8", newline=None):
        p = tmp_path / nombre
        with open(p, "w", encoding=encoding, newline=newline) as f:
            f.write(texto)
        return validador.validar(p)
    return _revisar
