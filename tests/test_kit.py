"""Pruebas de coherencia del kit: rutas citadas y archivos esperados."""
import re
import json
from urllib.parse import unquote
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TEXTOS = [p for p in RAIZ.rglob("*") if p.suffix in {".md", ".py", ".yaml", ".json"}
          and ".git" not in p.parts and "tests" not in p.parts]
# Salidas personales documentadas que se crean en la bóveda del usuario.
RUTAS_GENERADAS = {"00_CORE/configuracion.md"}


def test_rutas_citadas_existen():
    """Toda ruta 00_CORE/... o PROJECT_TEMPLATE/... que aparece en el kit tiene que existir."""
    rotas = []
    patron = re.compile(r"((?:00_CORE|PROJECT_TEMPLATE|DOCS)/[A-Za-z0-9_./ÁÉÍÓÚáéíóúñ -]*[A-Za-z0-9_/])")
    for archivo in TEXTOS:
        for ruta in patron.findall(archivo.read_text(encoding="utf-8")):
            ruta = ruta.rstrip("/.")
            if ruta in RUTAS_GENERADAS:
                assert not (RAIZ / ruta).exists(), "No distribuir una configuración personal"
                continue
            if "<" in ruta or " " in ruta:
                continue
            base = RAIZ
            if not (base / ruta).exists() and not (base / (ruta + ".md")).is_file():
                rotas.append(f"{archivo.relative_to(RAIZ)} → {ruta}")
    assert not rotas, "Rutas que no existen:\n" + "\n".join(sorted(set(rotas)))


def test_archivos_esenciales():
    for ruta in ["LICENSE", "README.md", "AI-INSTRUCTIONS.md", "AGENTS.md", "CLAUDE.md",
                 "00_CORE/protocols/configurar-vault.md", ".claude/skills/configurar/SKILL.md",
                 "DOCS/empezar-con-ia.md", "DOCS/creacion-para-asistentes.md", "crear_proyecto.py",
                 "00_CORE/atoms/00_vault-rules.md", "00_CORE/cells/TEMPLATE_cell.md",
                 "00_CORE/cells/ejemplo-context.md", "00_CORE/schemas/validate.py",
                 ".claude/settings.json", ".obsidian/app.json", "Panel.md", "Proyectos.base", "instalar.py", ".github/workflows/tests.yml"]:
        assert (RAIZ / ruta).exists(), ruta


def test_licencia_da_credito():
    texto = (RAIZ / "LICENSE").read_text(encoding="utf-8")
    assert "Copyright (c) 2025 davidkimai" in texto
    assert "MIT License" in texto


def test_sin_marcadores_invisibles_en_obsidian():
    """Obsidian oculta '<texto>' fuera de código: las notas no deben usarlo para pendientes."""
    malos = []
    for archivo in RAIZ.rglob("*.md"):
        if ".claude" in archivo.parts or archivo.name == "AI-INSTRUCTIONS.md" or "tests" in archivo.parts:
            continue
        t = archivo.read_text(encoding="utf-8")
        t = re.sub(r"```.*?```", "", t, flags=re.S)
        t = "\n".join(l for l in t.splitlines() if not l.startswith("    "))
        t = re.sub(r"`[^`]*`", "", t)
        t = re.sub(r"%%.*?%%", "", t, flags=re.S)
        if re.search(r"<[^<>\n]{1,60}>", t):
            malos.append(str(archivo.relative_to(RAIZ)))
    assert not malos, malos


def test_enlaces_markdown_locales():
    rotos = []
    for archivo in RAIZ.rglob("*.md"):
        if "tests" in archivo.parts or ".git" in archivo.parts:
            continue
        texto = archivo.read_text(encoding="utf-8")
        for enlace in re.findall(r"(?<!!)\[[^\]\n]*\]\(([^)\n]+)\)", texto):
            if "://" in enlace or enlace.startswith(("#", "mailto:")):
                continue
            ruta = unquote(enlace.split("#")[0].strip("<>"))
            if ruta and not (archivo.parent / ruta).exists():
                rotos.append((str(archivo.relative_to(RAIZ)), ruta))
    assert not rotos, rotos


def test_configuraciones_json_validas():
    for archivo in list((RAIZ / ".obsidian").glob("*.json")) + list((RAIZ / ".claude").glob("*.json")):
        json.loads(archivo.read_text(encoding="utf-8"))


def test_textos_sin_caracteres_de_control():
    for archivo in RAIZ.rglob("*.md"):
        texto = archivo.read_text(encoding="utf-8")
        assert not any(ord(c) < 32 and c not in "\n\r\t" for c in texto), archivo


def test_instrucciones_livianas_y_sin_codigo_duplicado():
    archivo = RAIZ / "AI-INSTRUCTIONS.md"
    assert archivo.stat().st_size < 10000
    assert "def validar(" not in archivo.read_text(encoding="utf-8")
