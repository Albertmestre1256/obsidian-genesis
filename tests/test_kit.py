"""Pruebas de coherencia del kit: rutas citadas y archivos esperados."""
import re
import json
from urllib.parse import unquote
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
TEXTOS = [p for p in RAIZ.rglob("*") if p.suffix in {".md", ".py", ".yaml", ".json"}
          and ".git" not in p.parts and "tests" not in p.parts]
# Salidas personales documentadas que se crean en la bóveda del usuario.
RUTAS_GENERADAS = {"00_CORE/configuracion.md", "00_CORE/logs/registro-cambios.md",
                   "00_CORE/logs/historial", "00_CORE/logs/.registro-cambios.lock"}


def test_rutas_citadas_existen():
    """Toda ruta 00_CORE/... o PROJECT_TEMPLATE/... que aparece en el kit tiene que existir."""
    rotas = []
    patron = re.compile(r"((?:00_CORE|PROJECT_TEMPLATE|DOCS)/[A-Za-z0-9_./ÁÉÍÓÚáéíóúñ -]*[A-Za-z0-9_/])")
    for archivo in TEXTOS:
        for ruta in patron.findall(unquote(archivo.read_text(encoding="utf-8"))):
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
    for ruta in ["LICENSE", "README.md", "INDICE.md", "actualizar_indice.py", "DOCS/indice-principal.md", "AI-INSTRUCTIONS.md", "AGENTS.md", "CLAUDE.md",
                 "00_CORE/protocols/configurar-vault.md", ".claude/skills/configurar/SKILL.md",
                 "DOCS/QUICKSTART.md", "DOCS/creacion-para-asistentes.md", "crear_proyecto.py",
                 ".opencode/commands/configurar.md", "DOCS/opencode.md", "DOCS/chatgpt.md",
                 "00_CORE/atoms/00_vault-rules.md", "00_CORE/templates/TEMPLATE_cell.md",
                 "00_CORE/cells/ejemplo-context.md", "00_CORE/schemas/validate.py", "00_CORE/schemas/rutas_boveda.py",
                 ".claude/settings.json", ".obsidian/app.json", "Panel.md", "Proyectos.base", ".github/workflows/tests.yml"]:
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
    for archivo in list((RAIZ / ".obsidian").glob("*.json")) + list((RAIZ / ".claude").glob("*.json")) + list(RAIZ.glob("opencode*.example.json")):
        json.loads(archivo.read_text(encoding="utf-8"))
    apariencia = json.loads((RAIZ / '.obsidian/appearance.json').read_text(encoding='utf-8'))
    assert set(apariencia) == {'enabledCssSnippets'}  # no distribuir preferencias personales
    assert 'genesis-vista-simple' in apariencia['enabledCssSnippets']
    for nombre in apariencia['enabledCssSnippets']:
        assert (RAIZ / '.obsidian/snippets' / (nombre + '.css')).is_file()


def test_perfiles_opencode_referencian_archivos_distribuidos():
    for archivo in RAIZ.glob("opencode*.example.json"):
        config = json.loads(archivo.read_text(encoding="utf-8"))
        for ruta in config['instructions']:
            assert (RAIZ / ruta).is_file(), (archivo.name, ruta)
        for plugin in config['plugin']:
            ruta, opciones = plugin if isinstance(plugin, list) else (plugin, {})
            assert (RAIZ / ruta).is_file(), (archivo.name, ruta)
            for lectura in opciones.get('readPaths', []):
                assert (RAIZ / lectura).is_file(), (archivo.name, lectura)


def test_selector_plantillas_no_incluye_fichas_existentes():
    settings = json.loads((RAIZ/'.obsidian/templates.json').read_text(encoding='utf-8'))
    folder = RAIZ/settings['folder']
    candidates = list(folder.rglob('*.md'))
    assert folder.is_dir() and candidates
    assert folder != RAIZ/'00_CORE/cells'
    assert (folder/'TEMPLATE_cell.md').is_file()
    assert all(p.name.startswith('TEMPLATE_') for p in candidates)
    assert not (RAIZ/'00_CORE/cells/TEMPLATE_cell.md').exists()


def test_grafo_nativo_prioriza_notas_del_usuario():
    assert 'graph' in json.loads((RAIZ / '.obsidian/core-plugins.json').read_text(encoding='utf-8'))
    config = json.loads((RAIZ / '.obsidian/graph.json').read_text(encoding='utf-8'))
    assert config['showOrphans'] is True
    assert config['hideUnresolved'] is True and config['showAttachments'] is False
    assert (RAIZ / 'LEER_PRIMERO.md').is_file()
    terminos = config['search'].split()
    assert terminos and all(t.startswith('-path:/') and t.endswith('/') for t in terminos)
    filtros = [re.compile(t[7:-1]) for t in terminos]
    for ruta in ['Panel.md', 'INDICE.md', 'Viaje/02_SINTESIS/itinerario.md',
                 'Viaje/01_FUENTES/reserva.md', 'Viaje/README-del-curso.md',
                 '00_CORE/cells/viaje-context.md', 'Viaje/DOCS/apuntes.md']:
        assert not any(f.search(ruta) for f in filtros), ruta
    for ruta in ['DOCS/obsidian.md', 'PROJECT_TEMPLATE/02_SINTESIS/README.md',
                 'tests/test_kit.py', '00_CORE/templates/TEMPLATE_cell.md',
                 '00_CORE/atoms/00_vault-rules.md', 'README.de.md', 'AGENTS.md']:
        assert any(f.search(ruta) for f in filtros), ruta


def test_textos_sin_caracteres_de_control():
    for archivo in RAIZ.rglob("*.md"):
        texto = archivo.read_text(encoding="utf-8")
        assert not any(ord(c) < 32 and c not in "\n\r\t" for c in texto), archivo


def test_instrucciones_livianas_y_sin_codigo_duplicado():
    archivo = RAIZ / "AI-INSTRUCTIONS.md"
    assert archivo.stat().st_size < 10000
    assert "def validar(" not in archivo.read_text(encoding="utf-8")


def test_scripts_no_dejan_pycache_en_la_boveda(tmp_path):
    """Usar los scripts dentro de la bóveda no debe dejar carpetas __pycache__."""
    import os
    import shutil
    import subprocess
    import sys
    boveda = tmp_path / "boveda"
    shutil.copytree(RAIZ, boveda, ignore=shutil.ignore_patterns(
        ".git", "tests", "__pycache__", ".pytest_cache", ".agents"))
    entorno = {k: v for k, v in os.environ.items() if k not in ("PYTHONDONTWRITEBYTECODE", "PYTHONPYCACHEPREFIX")}
    entorno["PYTHONIOENCODING"] = "utf-8"
    for argumentos in (["00_CORE/schemas/validate.py", ".", "--cierre", "--operacion", "prueba-pycache"],
                       ["actualizar_indice.py", "--comprobar"],
                       ["00_CORE/schemas/registrar_cambios.py", "--help"]):
        resultado = subprocess.run([sys.executable, *argumentos], cwd=boveda, env=entorno,
                                   capture_output=True, text=True, encoding="utf-8")
        assert resultado.returncode in (0, 1) and "Traceback" not in resultado.stderr, resultado.stderr
    assert not list(boveda.rglob("__pycache__"))
