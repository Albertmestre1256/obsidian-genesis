"""Pruebas del validador de células (00_CORE/schemas/validate.py)."""
import re

import pytest


def reemplazar(texto, viejo, nuevo):
    assert viejo in texto, f"el ejemplo ya no contiene {viejo!r}"
    return texto.replace(viejo, nuevo, 1)


# ------------------------------------------------------------------
# Células que tienen que pasar
# ------------------------------------------------------------------
def test_ejemplo_pasa_sin_avisos(revisar, ejemplo):
    assert revisar(ejemplo) == ([], [])


def test_bom_de_windows(revisar, ejemplo):
    assert revisar(ejemplo, encoding="utf-8-sig") == ([], [])


def test_fin_de_linea_windows(revisar, ejemplo):
    assert revisar(ejemplo, newline="\r\n") == ([], [])


def test_tipo_con_tilde_y_mayuscula(revisar, ejemplo):
    assert revisar(reemplazar(ejemplo, "tipo: celula", "tipo: Célula"))[0] == []


def test_contexto_en_minuscula_o_con_texto(revisar, ejemplo):
    for valor in ["d", "D - operativo", '"D"', "D (operativo)"]:
        errores, _ = revisar(reemplazar(ejemplo, "contexto: D", f"contexto: {valor}"))
        assert errores == [], valor


def test_fecha_entre_comillas(revisar, ejemplo):
    assert revisar(reemplazar(ejemplo, "actualizado: 2026-09-27", 'actualizado: "2026-09-27"')) == ([], [])


def test_vinetas_con_asterisco(revisar, ejemplo):
    texto = reemplazar(ejemplo, "- [ ] Abrir la planilla", "* [ ] Abrir la planilla")
    assert revisar(texto) == ([], [])


def test_subvinetas_no_cuentan_como_hechos(revisar, ejemplo):
    texto = reemplazar(ejemplo, "(fuente: mi agenda)\n", "(fuente: mi agenda)\n  - martes 2 h, jueves 3 h\n")
    assert revisar(texto) == ([], [])


def test_titulo_con_emoji_y_mayusculas(revisar, ejemplo):
    assert revisar(reemplazar(ejemplo, "## Hechos clave", "## Hechos Clave 📌")) == ([], [])


def test_propiedades_extra_de_obsidian(revisar, ejemplo):
    texto = reemplazar(ejemplo, "contexto: D\n", "contexto: D\ntags:\n  - aprendizaje\n  - python\naliases: [python, curso]\n")
    assert revisar(texto) == ([], [])


def test_texto_con_dos_puntos(revisar, ejemplo):
    texto = re.sub(r"^descripcion: .*$", 'descripcion: "Meta: automatizar planillas"', ejemplo, flags=re.M)
    assert revisar(texto)[0] == []


@pytest.mark.parametrize("valor", [
    "'Meta: automatizar # un texto, con coma'",
    "'El proyecto de l''autor'",
    '"Una descripcion con \\"comillas\\""',
    '"Una descripcion" # comentario',
    "Un enlace https://example.com/#seccion # comentario",
])
def test_textos_yaml_validos(revisar, ejemplo, valor):
    texto = re.sub(r"^descripcion: .*$", lambda _: "descripcion: " + valor, ejemplo, flags=re.M)
    assert revisar(texto) == ([], [])


def test_comentario_en_fecha_y_listas_con_comas(revisar, ejemplo):
    texto = reemplazar(ejemplo, "actualizado: 2026-09-27",
                       "actualizado: 2026-09-27 # ultima revision\n"
                       'aliases: ["Python, desde cero", \'l\'\'autor\', curso] # aliases')
    assert revisar(texto) == ([], [])


@pytest.mark.parametrize("valor", [
    "Meta: automatizar planillas",
    '"Sin cierre',
    "'Sin cierre",
    '"Texto" sobrante',
    '"Escape \\q no valido"',
    "[una lista sin cierre",
    "[texto, [lista anidada]]",
    "{campo: valor}",
    ">\n  Una descripcion en bloque",
    "*referencia",
])
def test_yaml_roto_o_no_admitido_no_se_aprueba(revisar, ejemplo, valor):
    texto = re.sub(r"^descripcion: .*$", lambda _: "descripcion: " + valor, ejemplo, flags=re.M)
    errores, _ = revisar(texto)
    assert errores and "propiedad 'descripcion'" in errores[0]


@pytest.mark.parametrize("campo", ["proyecto", "descripcion"])
@pytest.mark.parametrize("valor", ["", "null", "~", "[]", "[texto]", "true", "123", '" "'])
def test_campos_de_texto_no_aceptan_vacios_ni_otros_tipos(revisar, ejemplo, campo, valor):
    texto = re.sub(r"^" + campo + r": .*$", lambda _: campo + ": " + valor, ejemplo, flags=re.M)
    errores, _ = revisar(texto)
    assert any("'" + campo + "'" in error for error in errores)


def test_propiedad_repetida_no_se_ignora(revisar, ejemplo):
    texto = reemplazar(ejemplo, "contexto: D", "contexto: D\ncontexto: A")
    errores, _ = revisar(texto)
    assert errores and "repetida" in errores[0]


def test_sangria_invalida_no_se_ignora(revisar, ejemplo):
    texto = reemplazar(ejemplo, "contexto: D", "contexto: D\n  clave: contenido")
    errores, _ = revisar(texto)
    assert errores and "sangría" in errores[0]


def test_lista_no_reemplaza_valor_previo(revisar, ejemplo):
    texto = reemplazar(ejemplo, "contexto: D", "contexto: D\n  - A")
    errores, _ = revisar(texto)
    assert errores and "ya tiene un valor" in errores[0]


# ------------------------------------------------------------------
# Células que tienen que fallar o avisar
# ------------------------------------------------------------------
def test_plantilla_sin_completar(revisar, plantilla):
    errores, avisos = revisar(plantilla)
    assert any("'contexto'" in e for e in errores)
    assert any("'actualizado'" in e for e in errores)
    assert not any("Falta la sección" in e for e in errores), "los bloques %% no deben esconder secciones"
    assert any("[completar" in a for a in avisos)


def test_sin_propiedades(revisar):
    errores, _ = revisar("sin propiedades\n## Hechos clave\n")
    assert errores and "No encuentro las propiedades" in errores[0]


def test_propiedades_rotas(revisar, ejemplo):
    errores, _ = revisar(reemplazar(ejemplo, "contexto: D\n", "contexto: D\nesto no es una propiedad\n"))
    assert errores and "no tiene el formato 'nombre: valor'" in errores[0]


def test_contexto_invalido(revisar, ejemplo):
    for valor in ["E", "Operativo", "Borrador"]:
        errores, _ = revisar(reemplazar(ejemplo, "contexto: D", f"contexto: {valor}"))
        assert any("'contexto'" in e for e in errores), valor


def test_fecha_invalida(revisar, ejemplo):
    errores, _ = revisar(reemplazar(ejemplo, "actualizado: 2026-09-27", "actualizado: 27/09/2026"))
    assert any("'actualizado'" in e for e in errores)


def test_falta_seccion_obligatoria(revisar, ejemplo):
    errores, _ = revisar(reemplazar(ejemplo, "## Próximas acciones", "## Pendientes"))
    assert any("Próximas acciones" in e for e in errores)


def test_accion_sin_casilla(revisar, ejemplo):
    errores, _ = revisar(reemplazar(ejemplo, "- [x] Instalar", "- Instalar"))
    assert any("tiene que empezar con '- [ ] '" in e for e in errores)


def test_hecho_sin_fuente(revisar, ejemplo):
    errores, avisos = revisar(reemplazar(ejemplo, " (fuente: mi agenda)", ""))
    assert errores == []
    assert any("no tiene fuente" in a for a in avisos)


def test_decision_sin_fecha(revisar, ejemplo):
    _, avisos = revisar(reemplazar(ejemplo, "- 2026-09-20: ", "- ayer: "))
    assert any("no empieza con una fecha" in a for a in avisos)


def test_celula_demasiado_larga(revisar, ejemplo):
    relleno = "".join(f"- Dato de relleno número {i}. (fuente: prueba)\n" for i in range(400))
    _, avisos = revisar(reemplazar(ejemplo, "## Decisiones", relleno + "\n## Decisiones"))
    assert any("tokens" in a for a in avisos)


# ------------------------------------------------------------------
# Programa completo
# ------------------------------------------------------------------
def test_main_carpeta_vacia(validador, tmp_path, capsys):
    assert validador.main(tmp_path) == 0
    assert "Todavía no hay células" in capsys.readouterr().out


def test_main_ignora_la_plantilla(validador, tmp_path, ejemplo, plantilla, capsys):
    (tmp_path / "TEMPLATE_cell.md").write_text(plantilla, encoding="utf-8")
    (tmp_path / "ejemplo-context.md").write_text(ejemplo, encoding="utf-8")
    assert validador.main(tmp_path) == 0
    assert "TODO BIEN" in capsys.readouterr().out


def test_main_con_error_devuelve_1(validador, tmp_path, plantilla):
    (tmp_path / "nuevo-context.md").write_text(plantilla, encoding="utf-8")
    assert validador.main(tmp_path) == 1
