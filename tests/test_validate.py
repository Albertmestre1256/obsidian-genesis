"""Pruebas del validador de células (00_CORE/schemas/validate.py)."""
import re
import subprocess
import sys
from pathlib import Path

import pytest


def preparar_configuracion(tmp_path, panel):
    core = tmp_path / '00_CORE'
    (core / 'cells').mkdir(parents=True)
    (core / 'configuracion.md').write_text(
        '---\ntipo: configuracion\nestado: lista\npersonalizacion: abierta\n---\n'
        '\n## Inventario de personalización\n\n'
        '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n'
        '|---|---|---|---|---|---|\n'
        '| documento-perfil | boveda | omitido | — | — | — |\n', encoding='utf-8')
    (tmp_path / 'Panel.md').write_text(panel, encoding='utf-8')
    return core / 'cells'


def test_fichas_validas_no_ocultan_panel_sin_inventario(validador, tmp_path, ejemplo, capsys):
    cells = preparar_configuracion(tmp_path, '# Mis proyectos\n\n![[Proyectos.base]]\n')
    (cells / 'propio-context.md').write_text(ejemplo, encoding='utf-8')
    assert validador.main(cells) == 1
    output = capsys.readouterr().out
    assert 'CONFIGURACIÓN INCOMPLETA' in output and 'TODO BIEN' not in output


@pytest.mark.parametrize('link', ['[[00_CORE/configuracion#Inventario de personalización|Completar después]]',
                                '[Personalizar](00_CORE/configuracion.md#inventario)',
                                '[[configuracion]]'])
def test_inventario_abierto_no_exige_cv_para_validar(validador, tmp_path, link):
    preparar_configuracion(tmp_path, '# Mi bóveda\n\n'+link+'\n')
    assert validador.validar_configuracion(tmp_path) == []


@pytest.mark.parametrize('panel', ['```md\n[[00_CORE/configuracion]]\n```\n',
                                 '%% [[00_CORE/configuracion]] %%\n',
                                 '[Perfil](https://example.com/00_CORE/configuracion.md)\n'])
def test_ejemplos_y_enlaces_externos_no_integran_el_panel(validador, tmp_path, panel):
    preparar_configuracion(tmp_path, panel)
    assert any('Panel no da acceso' in error for error in validador.validar_configuracion(tmp_path))


def test_configuracion_incompleta_sin_fichas_no_pasa(validador, tmp_path, capsys):
    cells = preparar_configuracion(tmp_path, '# Sin acceso\n')
    assert validador.main(cells) == 1
    assert 'CONFIGURACIÓN INCOMPLETA' in capsys.readouterr().out


@pytest.mark.parametrize('rota', [False, True])
def test_raiz_del_vault_revisa_fichas_reales(validador, tmp_path, ejemplo, capsys, rota):
    cells = preparar_configuracion(tmp_path, '[[00_CORE/configuracion]]\n')
    (cells / 'propio-context.md').write_text(
        ejemplo.replace('contexto: D', 'contexto: E') if rota else ejemplo, encoding='utf-8')
    # Una nota ajena con forma de ficha en la raíz no pertenece a cells.
    (tmp_path / 'ajena-context.md').write_text('# No validar esta nota\n', encoding='utf-8')
    assert validador.main(tmp_path) == int(rota)
    output = capsys.readouterr().out
    assert 'propio-context.md' in output and 'ajena-context.md' not in output
    assert 'Todavía no hay células' not in output


def test_raiz_del_vault_no_omite_configuracion_incompleta(validador, tmp_path, capsys):
    preparar_configuracion(tmp_path, '# Sin acceso al inventario\n')
    assert validador.main(tmp_path) == 1
    assert 'CONFIGURACIÓN INCOMPLETA' in capsys.readouterr().out


def test_raiz_del_vault_con_cells_ausente_no_declara_revision_vacia(validador, tmp_path, capsys):
    (tmp_path / '00_CORE').mkdir()
    assert validador.main(tmp_path) == 1
    assert 'No encuentro la carpeta' in capsys.readouterr().out


def test_cli_punto_revisa_cells_desde_vault_con_espacios(validador, tmp_path, ejemplo):
    root = tmp_path / 'Mi bóveda de estudio'
    cells = preparar_configuracion(root, '[[00_CORE/configuracion]]\n')
    path = cells / 'propio-context.md'
    path.write_text(ejemplo.replace('contexto: D', 'contexto: E'), encoding='utf-8')
    before = path.read_bytes()
    result = subprocess.run([sys.executable, '-B', validador.__file__, '.'], cwd=root,
                            capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 1 and 'propio-context.md' in result.stdout
    assert path.read_bytes() == before


def test_configuracion_ilegible_se_conserva(validador, tmp_path):
    preparar_configuracion(tmp_path, '[[00_CORE/configuracion]]\n')
    config = tmp_path / '00_CORE/configuracion.md'
    config.write_bytes(b'\xff datos originales')
    assert validador.validar_configuracion(tmp_path)
    assert config.read_bytes() == b'\xff datos originales'


def test_tabla_sin_datos_no_es_inventario(validador, tmp_path):
    preparar_configuracion(tmp_path, '[[00_CORE/configuracion]]\n')
    path = tmp_path / '00_CORE/configuracion.md'
    path.write_text(path.read_text(encoding='utf-8').replace('| documento-perfil | boveda | omitido | — | — | — |\n', ''), encoding='utf-8')
    assert any('inventario' in mensaje for mensaje in validador.validar_configuracion(tmp_path))


@pytest.mark.parametrize('campo', ['estado', 'personalizacion'])
def test_estados_complejos_se_informan_sin_abortar(validador, tmp_path, campo):
    preparar_configuracion(tmp_path, '[[00_CORE/configuracion]]\n')
    path = tmp_path / '00_CORE/configuracion.md'
    before = path.read_text(encoding='utf-8')
    path.write_text(re.sub(r'^'+campo+r':.*$', campo+': [valor]', before, flags=re.M), encoding='utf-8')
    assert any(campo in mensaje for mensaje in validador.validar_configuracion(tmp_path))


@pytest.mark.parametrize('panel,duplicado,correcto', [
    ('| Perfil | [[00_CORE/configuracion\\|Completar]] |\n', False, True),
    ('[Perfil](00_CORE/configuracion.md "Más adelante")\n', False, True),
    ('[Perfil](configuracion.md)\n', False, False),
    ('[[configuracion]]\n', True, False),
    ('`[[00_CORE/configuracion]]`\n', False, False),
    ('``[[00_CORE/configuracion]]``\n', False, False)])
def test_enlaces_del_panel_se_resuelven_sin_falsos_resultados(validador, tmp_path, panel, duplicado, correcto):
    preparar_configuracion(tmp_path, panel)
    if duplicado:
        (tmp_path / 'configuracion.md').write_text('# Otra nota\n', encoding='utf-8')
    errores = validador.validar_configuracion(tmp_path)
    assert (not errores) == correcto


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


@pytest.mark.parametrize('fuente,avisa', [(' (fuente: mi agenda (2026))', False),
    (' (fuente: ) más datos (otro)', True), (' (fuente: ) (ver anexo)', True)])
def test_fuente_con_parentesis(revisar, ejemplo, fuente, avisa):
    errores, avisos = revisar(reemplazar(ejemplo, " (fuente: mi agenda)", fuente))
    assert errores == []
    assert any("no tiene fuente" in a for a in avisos) == avisa


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


@pytest.mark.parametrize('nombre', ['Estudio.md', 'ESTUDIO.MD'])
def test_main_revisa_ficha_renombrada_y_detecta_errores(validador, tmp_path, ejemplo, nombre, capsys):
    path = tmp_path / nombre
    path.write_text(ejemplo, encoding='utf-8')
    assert validador.main(tmp_path) == 0
    assert nombre in capsys.readouterr().out
    path.write_text(ejemplo.replace('contexto: D', 'contexto: E'), encoding='utf-8')
    assert validador.main(tmp_path) == 1
    assert "'contexto'" in capsys.readouterr().out


def test_busqueda_distingue_fichas_de_notas_y_plantilla(validador, tmp_path, ejemplo, plantilla):
    (tmp_path / 'TEMPLATE_cell.md').write_text(plantilla, encoding='utf-8')
    (tmp_path / 'README.md').write_text('# Información sobre fichas\n', encoding='utf-8')
    (tmp_path / 'Estudio.md').write_text(ejemplo, encoding='utf-8')
    (tmp_path / 'rota-context.md').write_text('# Ficha sin propiedades\n', encoding='utf-8')
    (tmp_path / 'Ficha incompleta.md').write_text('---\ntipo: celula\n---\n', encoding='utf-8')
    assert {p.name for p in validador.buscar_celulas(tmp_path)} == {
        'Estudio.md', 'rota-context.md', 'Ficha incompleta.md'}


@pytest.mark.parametrize('nombre', ['rota-context.md', 'Ficha renombrada.md'])
def test_revision_continua_ante_ficha_no_utf8(validador, tmp_path, ejemplo, capsys, nombre):
    broken = tmp_path/nombre
    raw = '---\ntipo: celula\n---\n'.encode('utf-16')
    broken.write_bytes(raw)
    (tmp_path/'sana-context.md').write_text(ejemplo, encoding='utf-8')
    assert validador.main(tmp_path) == 1
    output = capsys.readouterr().out
    assert nombre in output and 'UTF-8' in output
    assert 'sana-context.md' in output
    assert broken.read_bytes() == raw


def test_revision_sin_permiso_conserva_archivo_y_continua(validador, tmp_path, ejemplo, monkeypatch, capsys):
    broken = tmp_path/'Ficha personal.md'
    broken.write_text(ejemplo, encoding='utf-8')
    original = Path.read_text
    def denied(path, *args, **kwargs):
        if path == broken:
            raise PermissionError('Permiso denegado en la prueba')
        return original(path, *args, **kwargs)
    (tmp_path/'sana-context.md').write_text(ejemplo, encoding='utf-8')
    with monkeypatch.context() as patch:
        patch.setattr(Path, 'read_text', denied)
        assert validador.main(tmp_path) == 1
    output = capsys.readouterr().out
    assert broken.name in output and 'permiso' in output.lower()
    assert 'sana-context.md' in output
    assert broken.read_text(encoding='utf-8') == ejemplo


def test_carpeta_con_nombre_de_ficha_no_se_valida_como_nota(validador, tmp_path, ejemplo, capsys):
    (tmp_path/'archivo-context.md').mkdir()
    (tmp_path/'sana-context.md').write_text(ejemplo, encoding='utf-8')
    assert validador.main(tmp_path) == 0
    assert 'archivo-context.md' not in capsys.readouterr().out


def test_carpeta_inaccesible_informa_como_seguir(validador, tmp_path, monkeypatch, capsys):
    original = Path.iterdir
    def denied(path):
        if path == tmp_path:
            raise PermissionError('Carpeta inaccesible en la prueba')
        return original(path)
    monkeypatch.setattr(Path, 'iterdir', denied)
    assert validador.main(tmp_path) == 1
    output = capsys.readouterr().out
    assert 'permiso de lectura' in output
    assert 'TODO BIEN' not in output


INVENTARIOS_PRUEBA = [
    ('abierta-omisiones', True, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n| documento-perfil | boveda | omitido | Prefiero no compartir. | usuario, 2026-10-12 | Solo si lo solicita. |\n'),
    ('completa-omision', True, 'completa', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| documento-perfil | boveda | omitido | Prefiero no compartir. | usuario, 2026-10-12 | Solo si lo solicita. |\n'),
    ('item-extra', True, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| biblioteca | boveda | propuesto | Leer cuentos. | IA, 2026-10-12 | Adoptar o cambiar. |\n'),
    ('dos-proyectos', True, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| objetivo | proyecto:estudio | confirmado | Estudiar. | usuario, 2026-10-12 | — |\n| objetivo | proyecto:podcast | pendiente | — | — | Elegir tema. |\n'),
    ('barra-alias', True, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| materiales | proyecto:estudio | pendiente | [[Notas/Indice\\|Resumen]] y A\\|B | documento, 2026-10-12 | Revisar. |\n'),
    ('dos-columnas', False, 'abierta', '| Ítem | Estado |\n|---|---|\n| documento-perfil | omitido |\n'),
    ('cabecera-como-dato', False, 'abierta', '| Dato | Estado |\n|---|---|\n'),
    ('cabecera-reordenada', False, 'abierta', '| Alcance | Ítem | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('sin-separador', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('separador-sin-filas', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n'),
    ('estado-ajeno', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| documento-perfil | boveda | completado | Prefiero no compartir. | usuario, 2026-10-12 | Solo si lo solicita. |\n'),
    ('alcance-vacio', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina |  | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('proyecto-marcador', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | proyecto:[completar: identificador] | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('proyecto-ruta', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | proyecto:../secreto | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('duplicado', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('completa-pendiente', False, 'completa', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('completa-propuesto', False, 'completa', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | propuesto | — | — | ¿Cómo revisar las notas? |\n'),
    ('columna-faltante', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — |\n'),
    ('barra-no-escapada', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | ¿A|B? |\n'),
    ('tablas-de-ejemplo', False, 'abierta', '```md\n| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n```\n%%\n| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| documento-perfil | boveda | omitido | Prefiero no compartir. | usuario, 2026-10-12 | Solo si lo solicita. |\n%%\n'),
    ('otra-seccion-despues', True, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n\n## Avance de archivos\n\nPendiente de revisión.\n'),
    ('sin-cabecera-con-fila', False, 'abierta', '|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('separador-incompleto', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('comentario-html-no-es-tabla', False, 'abierta', '<!--\n| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n-->\n'),
    ('comentario-html-antes-de-tabla', True, 'abierta', '<!--\n| Falso | Ejemplo |\n|---|---|\n-->\n| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('pipe-con-dos-barras-inversas', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | A\\\\|B |\n'),
    ('pipe-con-tres-barras-inversas', True, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | A\\\\\\|B |\n'),
    ('cabecera-normalizada', True, 'abierta', '| ITEM | Alcance | ESTADO | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('item-vacio', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n|  | boveda | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('id--estudio', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | proyecto:-estudio | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('id-estudio-', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | proyecto:estudio- | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('id-estudio--cardio', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | proyecto:estudio--cardio | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
    ('id--', False, 'abierta', '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | proyecto:- | pendiente | — | — | ¿Cómo revisar las notas? |\n'),
]

@pytest.mark.parametrize('nombre,valido,perfil,tabla', INVENTARIOS_PRUEBA,
                         ids=[row[0] for row in INVENTARIOS_PRUEBA])
def test_inventario_canonico_y_configuracion_intacta(validador, tmp_path, nombre, valido, perfil, tabla):
    preparar_configuracion(tmp_path, '[[00_CORE/configuracion]]\n')
    path = tmp_path / '00_CORE/configuracion.md'
    path.write_text('---\ntipo: configuracion\nestado: lista\npersonalizacion: '+perfil+
                    '\n---\n## Inventario de personalización\n'+tabla, encoding='utf-8')
    before = path.read_bytes()
    errors = validador.validar_configuracion(tmp_path)
    assert (not errors) == valido, (nombre, errors)
    assert path.read_bytes() == before


def test_plantilla_configuracion_real_parcial_no_se_rechaza(validador, tmp_path):
    preparar_configuracion(tmp_path, '[[00_CORE/configuracion]]\n')
    template = (Path(__file__).resolve().parents[1] / '00_CORE/templates/TEMPLATE_configuracion.md')
    text = template.read_text(encoding='utf-8').replace('tipo: plantilla-configuracion', 'tipo: configuracion')
    text = text.replace('[completar: identificador]', 'estudio').replace('fecha: ""', 'fecha: "2026-10-13"')
    path = tmp_path / '00_CORE/configuracion.md'
    path.write_text(text, encoding='utf-8')
    before = path.read_bytes()
    assert validador.validar_configuracion(tmp_path) == []
    assert path.read_bytes() == before


def test_inventario_roto_no_produce_todo_bien_en_cli(validador, tmp_path, ejemplo, capsys):
    cells = preparar_configuracion(tmp_path, '[[00_CORE/configuracion]]\n')
    (cells / 'estudio-context.md').write_text(ejemplo, encoding='utf-8')
    path = tmp_path / '00_CORE/configuracion.md'
    text = path.read_text(encoding='utf-8').replace('omitido', 'completado')
    path.write_text(text, encoding='utf-8')
    before = path.read_bytes()
    assert validador.main(tmp_path) == 1
    output = capsys.readouterr().out
    assert 'TODO BIEN' not in output and 'CONFIGURACIÓN INCOMPLETA' in output
    assert path.read_bytes() == before


# Cierre de configuración: reutiliza mapas, rangos y registro, sin inventar perfil.
@pytest.fixture
def boveda_cierre(tmp_path):
    import importlib.util
    import shutil
    from datetime import datetime
    root = Path(__file__).resolve().parents[1]
    def load(name, relative):
        spec = importlib.util.spec_from_file_location(name, root / relative)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    maps = load('mapas_cierre_test', 'actualizar_indice.py')
    lines = load('lineas_cierre_test', '00_CORE/schemas/note_index.py')
    registry = load('registro_cierre_test', '00_CORE/schemas/registrar_cambios.py')
    creator = load('creador_cierre_test', 'crear_proyecto.py')
    def make(estado='lista'):
        vault = tmp_path / ('Mi bóveda '+estado)
        shutil.copytree(root, vault, ignore=shutil.ignore_patterns(
            'node_modules', '__pycache__', '.pytest_cache', '.git', 'worktrees',
            'package.json', 'package-lock.json', 'bun.lock'))
        config = vault / '00_CORE/configuracion.md'
        text = (vault / '00_CORE/templates/TEMPLATE_configuracion.md').read_text(encoding='utf-8')
        text = text.replace('tipo: plantilla-configuracion', 'tipo: configuracion')
        text = text.replace('estado: parcial', 'estado: '+estado)
        text = text.replace('fecha: ""', 'fecha: "'+datetime.now().date().isoformat()+'"')
        text = text.replace('[completar: identificador]', 'estudio')
        text = text.replace('[completar: nombre acordado]', 'Estudio ficticio')
        text = text.replace('[completar: objetivo acordado]', 'Ordenar el estudio de prueba')
        text = text.replace('| documento-perfil | boveda | pendiente |', '| documento-perfil | boveda | omitido |')
        config.write_text(text, encoding='utf-8')
        written = []
        plan = creator.planificar(vault, {'nombre':'Estudio ficticio', 'id':'estudio',
            'objetivo':'Ordenar el estudio de prueba', 'descripcion':'Caso ficticio de cierre.',
            'contexto':'D', 'fecha':datetime.now().date().isoformat()})
        creator.aplicar(plan, written)
        panel = vault / 'Panel.md'
        panel.write_text('# Bienvenida\n\n[[00_CORE/configuracion|Perfil y pendientes]]\n', encoding='utf-8')
        for path in lines.archivos(vault):
            path.write_bytes(lines.contenido(path.read_bytes()))
        maps.actualizar(vault)
        event = {'id':'preparar-cierre', 'ia':'Prueba', 'herramienta':'fixture',
            'resumen':'Preparación ficticia.', 'verificado':True,
            'cambios':[{'accion':'editar','ruta':'Panel.md'}]}
        registry.registrar(vault, event)
        maps.actualizar(vault)  # El registro ya existe antes de registrar el cierre final.
        event.update(id='cierre-final', resumen='Cierre ficticio.', cambios=[
            {'accion':'crear','ruta':'00_CORE/configuracion.md'},
            {'accion':'editar','ruta':'Panel.md'}, {'accion':'editar','ruta':'INDICE.md'}])
        registry.registrar(vault, event)
        assert maps.actualizar(vault, comprobar=True)['estado'] == 'vigente'
        return vault, maps, lines, registry
    return make


def foto_cierre(root):
    return {p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}


def alterar_evento_cierre(vault, registry, change):
    import json
    path = vault / registry.REGISTRO
    text = path.read_text(encoding='utf-8')
    match = next(m for m in registry.MARCA.finditer(text) if json.loads(m.group(1))['id']=='cierre-final')
    event = json.loads(match.group(1))
    change(event)
    replacement = '%% cambio: '+json.dumps(event, ensure_ascii=False, sort_keys=True)+' %%'
    path.write_bytes(registry.lineas.contenido((text[:match.start()]+replacement+text[match.end():]).encode('utf-8')))


@pytest.mark.parametrize('estado', ['lista', 'parcial'])
def test_cierre_correcto_no_exige_cv_y_no_escribe(validador, boveda_cierre, estado):
    vault, _, _, _ = boveda_cierre(estado)
    before = foto_cierre(vault)
    assert validador.validar_cierre(vault, 'cierre-final') == []
    assert foto_cierre(vault) == before


# Cada escenario debe fallar por su propio control, no por otro que lo tape.
CIERRE_ESPERADO = {
    'aviso-panel': 'Para empezar', 'mapa-general': 'Mapas desactualizados', 'mapa-nodo': 'Mapas desactualizados',
    'rango': 'Rangos desactualizados', 'sin-registro': 'Falta registro activo', 'id-ajeno': 'no encontrada',
    'sin-config-en-evento': 'sin cambio de configuración', 'evento-no-verificado': 'no verificada',
    'hash-config-viejo': 'hash de configuración no coincide', 'registro-roto': 'Registro propio sin propiedades',
    'fecha-futura': 'fecha en el futuro', 'registro-bloqueado': 'Registro bloqueado',
    'sin-config': 'Falta 00_CORE/configuracion.md'}


@pytest.mark.parametrize('fallo', list(CIERRE_ESPERADO))
def test_cierre_incompleto_falla_sin_reparar(validador, boveda_cierre, fallo):
    from datetime import datetime, timedelta
    vault, maps, lines, registry = boveda_cierre()
    operation = 'cierre-final'
    if fallo == 'aviso-panel':
        panel = vault / 'Panel.md'
        panel.write_bytes(lines.contenido((panel.read_text(encoding='utf-8')+
            '\n**Para empezar:** [[DOCS/empezar-con-ia|Dale la carpeta a tu IA y respondé sus preguntas]].\n').encode('utf-8')))
    elif fallo == 'mapa-general':
        (vault / 'Apunte.md').write_bytes(lines.contenido(b'# Apunte\n'))
    elif fallo == 'mapa-nodo':
        # Solo el bloque del nodo: una nota nueva cambiaría también el mapa general y lo taparía.
        node = vault / 'estudio/00 - Índice - estudio.md'
        text = node.read_text(encoding='utf-8').replace(maps.NODO_INICIO, maps.NODO_INICIO+'\n- [[Nota inventada]]', 1)
        node.write_bytes(lines.contenido(text.encode('utf-8')))
    elif fallo == 'rango':
        config = vault / '00_CORE/configuracion.md'
        config.write_text(config.read_text(encoding='utf-8')+'\n## Detalle nuevo\nTexto.\n', encoding='utf-8')
    elif fallo == 'sin-registro':
        (vault / registry.REGISTRO).unlink()
    elif fallo == 'id-ajeno':
        operation = 'otra-operacion'
    elif fallo == 'sin-config-en-evento':
        alterar_evento_cierre(vault, registry, lambda e:e.update(cambios=[c for c in e['cambios'] if c['ruta']!='00_CORE/configuracion.md']))
    elif fallo == 'evento-no-verificado':
        alterar_evento_cierre(vault, registry, lambda e:e.update(verificado=False))
    elif fallo == 'hash-config-viejo':
        config = vault / '00_CORE/configuracion.md'
        config.write_bytes(lines.contenido((config.read_text(encoding='utf-8')+'\nDato añadido después del registro.\n').encode('utf-8')))
    elif fallo == 'registro-roto':
        (vault / registry.REGISTRO).write_text('# Registro propio incompatible\n', encoding='utf-8')
    elif fallo == 'fecha-futura':
        alterar_evento_cierre(vault, registry, lambda e:e.update(fecha=(datetime.now().astimezone()+timedelta(days=1)).isoformat()))
    elif fallo == 'registro-bloqueado':
        (vault / '00_CORE/logs/.registro-cambios.lock').write_text('otro escritor', encoding='utf-8')
    elif fallo == 'sin-config':
        (vault / '00_CORE/configuracion.md').unlink()
    before = foto_cierre(vault)
    errors = validador.validar_cierre(vault, operation)
    assert errors and all(isinstance(e,str) and e.strip() for e in errors)
    assert any(CIERRE_ESPERADO[fallo] in e for e in errors), errors
    assert foto_cierre(vault) == before


def test_cierre_cli_rechaza_mantenimiento_pendiente_y_diario_se_conserva(validador, boveda_cierre):
    vault, _, _, _ = boveda_cierre()
    (vault / 'Apunte sin catalogar.md').write_text('# Apunte\n', encoding='utf-8')
    before = foto_cierre(vault)
    daily = subprocess.run([sys.executable, '-B', validador.__file__, str(vault)],
        capture_output=True, text=True, encoding='utf-8')
    assert daily.returncode == 0
    closing = subprocess.run([sys.executable, '-B', validador.__file__, str(vault),
        '--cierre', '--operacion', 'cierre-final'], capture_output=True, text=True, encoding='utf-8')
    assert closing.returncode != 0 and 'TODO BIEN' not in closing.stdout and 'Traceback' not in closing.stderr
    assert foto_cierre(vault) == before


def test_cierre_cli_correcto_identifica_su_alcance(validador, boveda_cierre):
    vault, _, _, _ = boveda_cierre()
    before = foto_cierre(vault)
    result = subprocess.run([sys.executable, '-B', validador.__file__, str(vault),
        '--cierre', '--operacion', 'cierre-final'], capture_output=True, text=True, encoding='utf-8')
    assert result.returncode == 0 and 'CIERRE VERIFICADO' in result.stdout
    assert foto_cierre(vault) == before


@pytest.mark.parametrize('operation', [None, '', 'bad id'])
def test_cierre_sin_identificador_falla_sin_excepcion(validador, boveda_cierre, operation):
    vault, _, _, _ = boveda_cierre()
    before = foto_cierre(vault)
    assert validador.validar_cierre(vault, operation)
    assert foto_cierre(vault) == before


@pytest.mark.parametrize('wrapper', ['%%\n{}\n%%', '<!--\n{}\n-->', '```markdown\n{}\n```'])
def test_cierre_aviso_en_comentario_o_ejemplo_no_es_aviso_real(validador, boveda_cierre, wrapper):
    vault, _, lines, registry = boveda_cierre()
    panel = vault/'Panel.md'
    example = '**Para empezar:** [[DOCS/empezar-con-ia|Dale la carpeta a tu IA y respondé sus preguntas]].'
    panel.write_bytes(lines.contenido((panel.read_text(encoding='utf-8')+'\n'+wrapper.format(example)+'\n').encode('utf-8')))
    before = foto_cierre(vault)
    assert validador.validar_cierre(vault, 'cierre-final') == []
    assert foto_cierre(vault) == before


def test_cierre_op_archivada_sigue_valida_y_duplicado_es_ambiguo(validador, boveda_cierre):
    vault, maps, _, registry = boveda_cierre()
    active = vault/registry.REGISTRO
    archive = vault/registry.ARCHIVO/'anterior.md'
    archive.parent.mkdir(parents=True)
    archive.write_bytes(active.read_bytes())
    active.unlink()
    registry.registrar(vault, {'id':'periodo-nuevo','ia':'Prueba','herramienta':'fixture',
        'resumen':'Nuevo periodo ficticio.','verificado':True,
        'cambios':[{'accion':'editar','ruta':'Panel.md'}]})
    maps.actualizar(vault)
    before = foto_cierre(vault)
    assert validador.validar_cierre(vault,'cierre-final') == []
    assert foto_cierre(vault) == before
    (archive.parent/'duplicado.md').write_bytes(archive.read_bytes())
    maps.actualizar(vault)
    before = foto_cierre(vault)
    assert validador.validar_cierre(vault,'cierre-final')
    assert foto_cierre(vault) == before


def test_cierre_historico_incompatible_no_se_ignora(validador, boveda_cierre):
    vault, maps, _, registry = boveda_cierre()
    path = vault/registry.ARCHIVO/'roto.md'
    path.parent.mkdir(parents=True)
    path.write_bytes(b'Registro ajeno sin propiedades.\n')
    maps.actualizar(vault)
    before = foto_cierre(vault)
    assert validador.validar_cierre(vault,'cierre-final')
    assert foto_cierre(vault) == before


def test_cierre_indice_manual_exige_revision_explicita(validador, boveda_cierre):
    vault, maps, lines, _ = boveda_cierre()
    node = vault / 'estudio/00 - Índice - estudio.md'
    head, _ = lines.separar(node.read_text(encoding='utf-8'))
    node.write_bytes(lines.contenido((''.join(head)+'\n# Índice propio\nContenido conservado.\n').encode('utf-8')))
    maps.actualizar(vault)
    assert maps.actualizar(vault,comprobar=True)['estado']=='vigente'
    assert node.relative_to(vault).as_posix() in maps.actualizar(vault,comprobar=True)['indices_manuales']
    before = foto_cierre(vault)
    errors = validador.validar_cierre(vault,'cierre-final')
    assert any('manual' in e.lower() for e in errors)
    assert foto_cierre(vault) == before


def test_cierre_no_ejecuta_scripts_del_destino(validador, boveda_cierre):
    vault, _, _, _ = boveda_cierre()
    for relative in ['actualizar_indice.py','00_CORE/schemas/note_index.py',
                     '00_CORE/schemas/registrar_cambios.py', '00_CORE/schemas/rutas_boveda.py']:
        (vault/relative).write_text('raise RuntimeError("No ejecutar código del destino")\n',encoding='utf-8')
    before = foto_cierre(vault)
    assert validador.validar_cierre(vault,'cierre-final') == []
    assert foto_cierre(vault) == before


def test_cierre_cli_sin_operacion_no_da_exito(validador, boveda_cierre):
    vault, _, _, _ = boveda_cierre()
    before = foto_cierre(vault)
    result = subprocess.run([sys.executable,'-B',validador.__file__,str(vault),'--cierre'],
        capture_output=True,text=True,encoding='utf-8')
    assert result.returncode != 0 and 'CIERRE VERIFICADO' not in result.stdout and 'Traceback' not in result.stderr
    assert foto_cierre(vault) == before


def test_cierre_cli_rechaza_ficha_invalida(validador, boveda_cierre):
    vault, maps, lines, _ = boveda_cierre()
    ficha = vault/'00_CORE/cells/estudio-context.md'
    text = ficha.read_text(encoding='utf-8')
    text = __import__('re').sub(r'^contexto:.*$', 'contexto: X', text, flags=__import__('re').M)
    ficha.write_bytes(lines.contenido(text.encode('utf-8')))
    maps.actualizar(vault)
    assert validador.validar(ficha)[0]
    before = foto_cierre(vault)
    result = subprocess.run([sys.executable,'-B',validador.__file__,str(vault),
        '--cierre','--operacion','cierre-final'],capture_output=True,text=True,encoding='utf-8')
    assert result.returncode != 0 and 'CIERRE VERIFICADO' not in result.stdout and 'Traceback' not in result.stderr
    assert foto_cierre(vault) == before


@pytest.mark.parametrize('relative', ['Panel.md','00_CORE/configuracion.md','00_CORE/logs/registro-cambios.md'])
def test_cierre_archivo_ilegible_informa_error(validador,boveda_cierre,relative):
    vault, _, _, _ = boveda_cierre()
    (vault/relative).write_bytes(b'\xff\xfe\xff')
    before = foto_cierre(vault)
    assert validador.validar_cierre(vault,'cierre-final')
    assert foto_cierre(vault) == before



@pytest.mark.parametrize('kind', ['ausente', 'numero'])
def test_cierre_hash_incompatible_informa_error(validador,boveda_cierre,kind):
    vault, _, _, registry = boveda_cierre()
    def change(event):
        for item in event['cambios']:
            if item['ruta']=='00_CORE/configuracion.md':
                if kind=='ausente':
                    item.pop('sha256')
                else:
                    item['sha256']=123
    alterar_evento_cierre(vault,registry,change)
    before = foto_cierre(vault)
    assert validador.validar_cierre(vault,'cierre-final')
    assert foto_cierre(vault)==before


def test_cierre_carga_biblioteca_propia_aunque_exista_nombre_ajeno(validador,boveda_cierre,monkeypatch):
    import importlib.util
    import types
    vault, _, _, _ = boveda_cierre()
    def foreign(*args,**kwargs):
        raise RuntimeError('No usar módulo ajeno de sys.modules')
    monkeypatch.setitem(sys.modules,'lineas_kit',types.SimpleNamespace(archivos=foreign))
    spec = importlib.util.spec_from_file_location('validate_cierre_aislado',validador.__file__)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    before = foto_cierre(vault)
    assert module.validar_cierre(vault,'cierre-final')==[]
    assert foto_cierre(vault)==before


def test_cierre_fecha_utc_z(validador,boveda_cierre):
    from datetime import datetime, timezone
    vault, _, _, registry = boveda_cierre()
    stamp = datetime.now(timezone.utc).isoformat().replace('+00:00','Z')
    alterar_evento_cierre(vault,registry,lambda event:event.update(fecha=stamp))
    before = foto_cierre(vault)
    assert validador.validar_cierre(vault,'cierre-final')==[]
    assert foto_cierre(vault)==before


def test_cierre_cli_admite_ruta_cells(validador,boveda_cierre):
    vault, _, _, _ = boveda_cierre()
    before = foto_cierre(vault)
    result = subprocess.run([sys.executable,'-B',validador.__file__,str(vault/'00_CORE/cells'),
        '--cierre','--operacion','cierre-final'],capture_output=True,text=True,encoding='utf-8')
    assert result.returncode==0 and 'CIERRE VERIFICADO' in result.stdout
    assert foto_cierre(vault)==before


@pytest.mark.parametrize('operation',['cierre-final',''])
def test_operacion_sin_modo_cierre_se_rechaza(validador,boveda_cierre,operation):
    vault, _, _, _ = boveda_cierre()
    before = foto_cierre(vault)
    result = subprocess.run([sys.executable,'-B',validador.__file__,str(vault),'--operacion',operation],
        capture_output=True,text=True,encoding='utf-8')
    assert result.returncode!=0 and 'TODO BIEN' not in result.stdout and 'Traceback' not in result.stderr
    assert foto_cierre(vault)==before


def test_cierre_sin_bibliotecas_informa_y_api_diaria_sigue(validador,boveda_cierre,tmp_path):
    import importlib.util
    vault, _, _, _ = boveda_cierre()
    isolated = tmp_path/'kit sin bibliotecas/00_CORE/schemas/validate.py'
    isolated.parent.mkdir(parents=True)
    isolated.write_bytes(Path(validador.__file__).read_bytes())
    spec = importlib.util.spec_from_file_location('validate_sin_bibliotecas',isolated)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    before = foto_cierre(vault)
    assert module.validar_cierre(vault,'cierre-final')
    assert module.main(vault)==0
    assert foto_cierre(vault)==before


def test_cierre_sin_carpeta_fichas_es_incompleto(validador,boveda_cierre):
    vault, maps, _, _ = boveda_cierre()
    folder = vault/'00_CORE/cells'
    for path in folder.iterdir():
        assert path.is_file()
        path.unlink()
    folder.rmdir()
    maps.actualizar(vault)
    before = foto_cierre(vault)
    assert validador.validar_cierre(vault,'cierre-final')
    assert foto_cierre(vault)==before


@pytest.mark.parametrize('etiqueta,extra,ok', [
    ('- Última operación de mantenimiento: visible-final', '', True),
    ('- Última operación de mantenimiento: `visible-final`', '', True),
    ('- **Última operación de mantenimiento:** `visible-final`', '', True),
    ('- Última operación de mantenimiento: visible-final (2026-10-14)', '', True),
    ('- Última operación de mantenimiento: anterior', '', False),
    ('- Última operación de mantenimiento: registro del martes', '', False),
    ('- Última operación de mantenimiento: `visible-final', '', False),
    ('- Última operación de mantenimiento: visible-final otra', '', False),
    ('- Última operación de mantenimiento: visible-final (2026-02-31)', '', False),
    ('- Última operación de mantenimiento: —', '', True),
    ('- Última operación de mantenimiento: -', '', True),
    ('- Última operación de mantenimiento: ', '', True),
    ('', '', True),
    ('- Última operación de mantenimiento: visible-final',
     '\n- Última operación de mantenimiento: visible-final\n', False),
    ('- Última operación de mantenimiento: visible-final',
     '\n%%\n- Última operación de mantenimiento: falso\n%%\n'
     '<!--\n- Última operación de mantenimiento: falso\n-->\n', True),
    ('- Última operación de mantenimiento: visible-final',
     '\n```md\n- Última operación de mantenimiento: falso\n```\n', True),
    ('- Última operación de mantenimiento: visible-final',
     '\n> ```md\n> - Última operación de mantenimiento: falso\n> ```\n', True),
    ('- Última operación de mantenimiento: visible-final',
     '\n  ~~~~md\n- Última operación de mantenimiento: falso\n  ~~~~~\n', True),
    ('- Última operación de mantenimiento: visible-final',
     '\n    - Última operación de mantenimiento: ejemplo indentado\n', True),
])
def test_cierre_contrasta_operacion_visible_sin_reparar(
        validador, boveda_cierre, etiqueta, extra, ok):
    vault, maps, lines, registry = boveda_cierre()
    config = vault / '00_CORE/configuracion.md'
    text = config.read_text(encoding='utf-8').replace(
        '- Última operación de mantenimiento: —', etiqueta) + extra
    config.write_bytes(lines.contenido(text.encode('utf-8')))
    maps.actualizar(vault)
    registry.registrar(vault, {'id':'visible-final', 'ia':'Prueba', 'herramienta':'fixture',
        'resumen':'Comprobar coherencia del avance.', 'verificado':True,
        'cambios':[{'accion':'editar','ruta':'00_CORE/configuracion.md'}]})
    maps.actualizar(vault)
    before = foto_cierre(vault)
    errors = validador.validar_cierre(vault, 'visible-final')
    assert (errors == []) is ok, errors
    if not ok:
        assert all('última operación de mantenimiento; revisión manual pendiente' in e for e in errors)
    assert foto_cierre(vault) == before


def test_cierre_etiqueta_editada_despues_del_registro_no_elude_hash(validador, boveda_cierre):
    vault, maps, lines, _ = boveda_cierre()
    config = vault / '00_CORE/configuracion.md'
    text = config.read_text(encoding='utf-8').replace(
        '- Última operación de mantenimiento: —',
        '- Última operación de mantenimiento: cierre-final')
    config.write_bytes(lines.contenido(text.encode('utf-8')))
    maps.actualizar(vault)
    before = foto_cierre(vault)
    errors = validador.validar_cierre(vault, 'cierre-final')
    assert errors and all('hash de configuración no coincide' in e for e in errors), errors
    assert foto_cierre(vault) == before


# Contrato independiente de presentación; datos ficticios, no notas personales.
"""Contrato independiente: presentación sin perder filas o validar ejemplos."""
import importlib.util
import os

_PERFIL_DEFAULT = Path(__file__).resolve().parents[1]/'00_CORE/schemas/validate.py'
_PERFIL_HEADER = '| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n'
_PERFIL_ROWS = ['| objetivo | proyecto:frances | confirmado | Leer francés. | usuario, 2026-10-13 | — |',
        '| documento-perfil | boveda | omitido | Prefiero no compartir. | usuario, 2026-10-13 | Solo si lo pide. |',
        r'| materiales | proyecto:frances | pendiente | [[Notas/Indice\|Resumen]] y A\|B | documento, 2026-10-13 | Revisar. |']
_PERFIL_TABLE = _PERFIL_HEADER+'\n'.join(_PERFIL_ROWS)+'\n'


@pytest.fixture
def perfil_validador():
    path=Path(os.environ.get('GENESIS_VALIDATOR_PATH',str(_PERFIL_DEFAULT)))
    spec=importlib.util.spec_from_file_location('perfil_independiente',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    return mod


def _perfil_plegable(table=_PERFIL_TABLE, header='> [!info]- Datos para retomar'):
    return header+'\n>\n'+'\n'.join('> '+x for x in table.rstrip().splitlines())+'\n'


def _perfil_comprobar(perfil_validador, tmp_path, block, profile='abierta'):
    root=tmp_path/'Bóveda ficticia';(root/'00_CORE/cells').mkdir(parents=True)
    path=root/'00_CORE/configuracion.md'
    text='---\ntipo: configuracion\nestado: lista\npersonalizacion: '+profile+'\n---\n\n## Inventario de personalización\n\n'+block+'\n\n## Avance\nPendiente.\n'
    path.write_text(text,encoding='utf-8');(root/'Panel.md').write_text('[[00_CORE/configuracion]]\n',encoding='utf-8')
    before=path.read_bytes()
    errors=perfil_validador.validar_configuracion(root)
    table_errors, rows=perfil_validador._validar_tabla_inventario(perfil_validador._extraer_seccion_inventario(text))
    assert path.read_bytes()==before
    return errors,table_errors,rows


@pytest.mark.parametrize('header',[None,'> [!info]- Datos para retomar','> [!info]+ Datos para retomar','> [!INFO]- Mis respuestas'])
def test_perfil_presentacion_conserva_todos_los_datos(perfil_validador,tmp_path,header):
    block=_PERFIL_TABLE if header is None else _perfil_plegable(header=header)
    errors, table_errors, rows=_perfil_comprobar(perfil_validador,tmp_path,block)
    assert errors==table_errors==[]
    assert len(rows)==3
    assert [r['estado'] for r in rows]==['confirmado','omitido','pendiente']
    assert rows[2]['dato']=='[[Notas/Indice|Resumen]] y A|B'


@pytest.mark.parametrize('name,block',[
    ('cita-sin-callout','\n'.join('> '+x for x in _PERFIL_TABLE.splitlines())),
    ('otro-callout',_perfil_plegable(header='> [!example]- Ejemplo')),
    ('codigo-citado',_perfil_plegable('```md\n'+_PERFIL_TABLE+'```')),
    ('comentario-citado',_perfil_plegable('<!--\n'+_PERFIL_TABLE+'-->')),
    ('comentario-obsidian-citado',_perfil_plegable('%%\n'+_PERFIL_TABLE+'%%')),
    ('codigo-externo','```md\n'+_perfil_plegable()+'```'),
    ('info-anidado',_perfil_plegable('> [!info]- Anidado\n>\n'+'\n'.join('> '+x for x in _PERFIL_TABLE.splitlines()))),
    ('fila-fuera',_perfil_plegable().replace('> '+_PERFIL_ROWS[-1],_PERFIL_ROWS[-1])),
    ('fila-no-citada-intermedia',_perfil_plegable().replace('> '+_PERFIL_ROWS[1],_PERFIL_ROWS[1])),
    ('tabla-plana-interrumpida',_PERFIL_HEADER+_PERFIL_ROWS[0]+'\n> '+_PERFIL_ROWS[1]+'\n> '+_PERFIL_ROWS[2]),
    ('dos-plegables',_perfil_plegable()+'\n'+_perfil_plegable()),
    ('plana-y-plegable',_PERFIL_TABLE+'\n'+_perfil_plegable()),
    ('dos-planas',_PERFIL_TABLE+'\n'+_PERFIL_TABLE),
    ('dos-tablas-en-info',_perfil_plegable(_PERFIL_TABLE+'\n'+_PERFIL_TABLE)),
])
def test_perfil_ejemplos_y_tablas_cortadas_no_declaran_lista(perfil_validador,tmp_path,name,block):
    errors,_,_=_perfil_comprobar(perfil_validador,tmp_path,block)
    assert errors, name


@pytest.mark.parametrize('malformed',[_PERFIL_TABLE.replace('pendiente','completado'),_PERFIL_TABLE.replace('| documento-perfil | boveda |','| documento-perfil | |'),_PERFIL_TABLE.replace('| Revisar. |','|'),_PERFIL_HEADER+'\n'])
def test_perfil_plegable_mantiene_controles_de_tabla(perfil_validador,tmp_path,malformed):
    errors,_,_=_perfil_comprobar(perfil_validador,tmp_path,_perfil_plegable(malformed))
    assert errors


def test_perfil_plegable_no_confirma_personalizacion_con_pendientes(perfil_validador,tmp_path):
    errors,table_errors,rows=_perfil_comprobar(perfil_validador,tmp_path,_perfil_plegable(),'completa')
    assert not table_errors and len(rows)==3
    assert any('completa' in error for error in errors)


def test_perfil_plegable_excluye_codigo_y_comentarios_previos(perfil_validador,tmp_path):
    decoy='```md\n'+_PERFIL_TABLE+'```\n\n<!--\n'+_PERFIL_TABLE+'-->\n'
    errors,table_errors,rows=_perfil_comprobar(perfil_validador,tmp_path,decoy+_perfil_plegable())
    assert errors==table_errors==[] and len(rows)==3


def test_perfil_plantilla_actual_se_instancia_sin_perder_filas(perfil_validador, tmp_path):
    root=tmp_path/'Bóveda nueva'
    (root/'00_CORE/cells').mkdir(parents=True)
    source=Path(__file__).resolve().parents[1]/'00_CORE/templates/TEMPLATE_configuracion.md'
    text=source.read_text(encoding='utf-8').replace('tipo: plantilla-configuracion','tipo: configuracion').replace('proyecto:[completar: identificador]','proyecto:frances')
    path=root/'00_CORE/configuracion.md';path.write_text(text,encoding='utf-8')
    (root/'Panel.md').write_text('[[00_CORE/configuracion]]\n',encoding='utf-8')
    before=path.read_bytes()
    errors=perfil_validador.validar_configuracion(root)
    table_errors,rows=perfil_validador._validar_tabla_inventario(perfil_validador._extraer_seccion_inventario(text))
    assert errors==table_errors==[] and len(rows)==15
    assert all(row['estado']=='pendiente' for row in rows)
    assert path.read_bytes()==before


"""Dos tablas en el mismo bloque no deben permitir aceptar solo la primera."""


@pytest.mark.parametrize('between',['Detalle después de la tabla.','[!info]- Otro inventario'])
def test_perfil_no_omite_tabla_despues_de_prosa_o_segundo_titulo(tmp_path,between):
    path=Path(__file__).resolve().parents[1]/'00_CORE/schemas/validate.py'
    spec=importlib.util.spec_from_file_location('perfil_tabla_completa',path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod)
    table='| Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar |\n|---|---|---|---|---|---|\n| rutina | boveda | pendiente | — | — | Revisar. |\n'
    body='## Inventario de personalización\n\n> [!info]- Datos\n>\n'+'\n'.join('> '+x for x in table.splitlines())+'\n> '+between+'\n>\n'+'\n'.join('> '+x for x in table.splitlines())+'\n'
    p=tmp_path/'Perfil.md';p.write_text(body,encoding='utf-8');before=p.read_bytes()
    errors,_=mod._validar_tabla_inventario(mod._extraer_seccion_inventario(body))
    assert errors
    assert p.read_bytes()==before


@pytest.mark.parametrize('prefix,label,ok', [
    ('', '- Ultima operacion de mantenimiento: anterior', False),
    ('', '- Ultima operacion de mantenimiento: opus-final', True),
    ('', '1. Última operación de mantenimiento: anterior', False),
    ('', '1. Última operación de mantenimiento: opus-final', True),
    ('', '2) Última operación de mantenimiento: anterior', False),
    ('', '*Última operación de mantenimiento*: anterior', False),
    ('', '*Última operación de mantenimiento*: opus-final', True),
    ('', 'Última operación de mantenimiento: anterior', False),
    ('', 'Última operación de mantenimiento: opus-final', True),
    ('', '> - Última operación de mantenimiento: anterior', False),
    ('```md\n%% comentario de ejemplo sin cerrar\n```\n\n',
     '- Última operación de mantenimiento: anterior', False),
    ('Objetivo: aprender a usar `%%` en una nota.\n\n',
     '- Última operación de mantenimiento: anterior', False),
    ('Objetivo: aprender a usar `<!--` en una nota.\n\n',
     '- Última operación de mantenimiento: anterior', False),
    ('> ```md\n> ejemplo\n\n', '- Última operación de mantenimiento: anterior', False),
    ('> > ~~~md\n> > ejemplo\n\n', '- Última operación de mantenimiento: anterior', False),
    ('> > ```md\n> > ejemplo\n', '> - Última operación de mantenimiento: anterior', False),
    ('```md\n> ```\n- Última operación de mantenimiento: falso-ejemplo\n```\n\n',
     '- Última operación de mantenimiento: opus-final', True),
    ('<!-- comentario\n- Última operación de mantenimiento: falso-ejemplo\n-->\n\n',
     '- Última operación de mantenimiento: opus-final', True),
])
def test_cierre_regresiones_opus_markdown(validador,boveda_cierre,prefix,label,ok):
    vault,maps,lines,registry=boveda_cierre()
    config=vault/'00_CORE/configuracion.md'
    text=config.read_text(encoding='utf-8').replace(
        '- Última operación de mantenimiento: —',label)
    text=text.replace('## Avance de archivos y comprobaciones',
        prefix+'## Avance de archivos y comprobaciones',1)
    config.write_bytes(lines.contenido(text.encode('utf-8')))
    maps.actualizar(vault)
    registry.registrar(vault,{'id':'opus-final','ia':'Prueba','herramienta':'Regresión tras Opus',
        'resumen':'Comprobar etiqueta Markdown y su operación real.','verificado':True,
        'cambios':[{'accion':'editar','ruta':'00_CORE/configuracion.md'}]})
    maps.actualizar(vault)
    before=foto_cierre(vault)
    errors=validador.validar_cierre(vault,'opus-final')
    assert (errors==[]) is ok,errors
    if not ok:
        assert any('última operación de mantenimiento' in e for e in errors),errors
    assert foto_cierre(vault)==before


def test_cierre_opus_conserva_mayusculas_del_id(validador,boveda_cierre):
    vault,maps,lines,registry=boveda_cierre()
    config=vault/'00_CORE/configuracion.md'
    text=config.read_text(encoding='utf-8').replace(
        '- Última operación de mantenimiento: —',
        '- Última operación de mantenimiento: OPUS-Final')
    config.write_bytes(lines.contenido(text.encode('utf-8')))
    maps.actualizar(vault)
    registry.registrar(vault,{'id':'OPUS-Final','ia':'Prueba','herramienta':'Regresión de ID exacto',
        'resumen':'El estilo de la etiqueta no modifica el ID.','verificado':True,
        'cambios':[{'accion':'editar','ruta':'00_CORE/configuracion.md'}]})
    maps.actualizar(vault)
    before=foto_cierre(vault)
    assert validador.validar_cierre(vault,'OPUS-Final')==[]
    assert any('no coincide' in e for e in validador.validar_cierre(vault,'opus-final'))
    assert foto_cierre(vault)==before


def test_operacion_visible_opus_no_abre_comentarios_en_codigo_indentado(validador):
    for opener in ('%%','<!--'):
        text='    '+opener+' ejemplo literal\n\n- Última operación de mantenimiento: anterior\n'
        assert validador._validar_operacion_visible(text,'actual')


@pytest.mark.parametrize('example', [
    '```ejemplo``` de comillas\n- Última operación de mantenimiento: anterior\n',
    '> > ```md\n> > ejemplo\n> - Última operación de mantenimiento: anterior\n',
])
def test_cierre_opus_extremos_de_cercas_y_citas(validador,boveda_cierre,example):
    vault,maps,lines,registry=boveda_cierre()
    config=vault/'00_CORE/configuracion.md'
    text=config.read_text(encoding='utf-8').replace('- Última operación de mantenimiento: —','')
    # Sin título intermedio de profundidad0: el segundo caso prueba realmente2→1.
    text+='\n'+example
    config.write_bytes(lines.contenido(text.encode('utf-8')))
    maps.actualizar(vault)
    registry.registrar(vault,{'id':'opus-extremo','ia':'Prueba','herramienta':'Regresión de citas/cercas',
        'resumen':'No ocultar la etiqueta visible detrás de código aparente.','verificado':True,
        'cambios':[{'accion':'editar','ruta':'00_CORE/configuracion.md'}]})
    maps.actualizar(vault)
    before=foto_cierre(vault)
    assert any('última operación de mantenimiento' in e for e in validador.validar_cierre(vault,'opus-extremo'))
    assert foto_cierre(vault)==before


# Coherencia del proyecto inicial: casos ficticios, independientes de nombres de archivo.
@pytest.mark.parametrize('caso,ok,detalle', [
    ('coherente', True, ''), ('id-ajeno', False, 'una ficha propia'),
    ('id-no-portable', False, 'Identificador'), ('referencias-ausentes', False, 'enlace ausente'),
    ('sin-ficha-inicial', False, '0 fichas'), ('indice-otro-proyecto', False, '0 índices'),
    ('ficha-renombrada', True, ''), ('indice-renombrado', True, ''),
    ('dos-proyectos', True, ''), ('formato-heredado', True, ''),
    ('parcial-planificado', True, ''), ('parcial-placeholder', True, ''),
    ('parcial-referencia-ausente', False, '0 fichas'), ('lista-sin-id', False, 'Identificador'),
    ('id-repetido', False, 'repetidos'), ('seccion-repetida', False, 'repetidos'),
    ('referencias-repetidas', False, 'repetidos'), ('solo-ficha-ejemplo', False, 'ejemplo'),
    ('ficha-ambigua', False, '2 fichas'), ('indice-ambiguo', False, '2 índices'),
    ('wiki-corto', True, ''), ('wiki-corto-ambiguo', False, 'enlace ausente'),
    ('markdown-relativo', True, ''), ('referencias-ajenas', False, 'otro destino'),
    ('referencia-externa', False, 'externo'), ('referencia-fuera-raiz', False, 'enlace ausente'),
    ('ejemplos-ocultos', True, ''), ('enlaces-en-codigo-inline', False, 'enlaces utilizables'),
    ('id-backticks', True, ''), ('id-con-mayusculas', False, 'Identificador'),
    ('id-otra-seccion', True, ''), ('id-oculto', False, 'Identificador'),
    ('referencias-vacias', True, ''), ('etiquetas-enfasis', True, ''),
    ('referencias-prosa', False, 'enlaces utilizables'), ('choque-con-ejemplo', False, 'ejemplo'),
    ('ficha-anidada-invalida', False, 'revisión diaria'), ('ficha-anidada-valida', False, 'revisión diaria'),
    ('url-suelta', False, 'externo'), ('autolink', False, 'externo'),
    ('parcial-enlace-extra-roto', False, 'enlace ausente'), ('url-solo-en-codigo', True, ''),
    ('ficha-excluida-invalida', False, 'revisión diaria'), ('ficha-excluida-valida', False, 'revisión diaria'),
])
def test_cierre_coherencia_proyecto_inicial(validador, boveda_cierre, caso, ok, detalle):
    import importlib.util
    from datetime import datetime
    from urllib.parse import quote
    vault, maps, lines, registry = boveda_cierre()
    before = foto_cierre(vault)
    config = vault/'00_CORE/configuracion.md'
    text = config.read_text(encoding='utf-8')
    refs = '- Ficha e índice: [[00_CORE/cells/estudio-context|Ficha]] · [[estudio/00 - Índice - estudio|Proyecto]]'
    assert '- Ficha e índice: —' in text
    text = text.replace('- Ficha e índice: —', refs)
    cell = vault/'00_CORE/cells/estudio-context.md'
    index = vault/'estudio/00 - Índice - estudio.md'
    moves = {}

    def mover(origen, destino):
        nonlocal text
        origen.resolve().relative_to(vault.resolve())
        destino.resolve().relative_to(vault.resolve())
        desde, hasta = origen.relative_to(vault).as_posix(), destino.relative_to(vault).as_posix()
        destino.parent.mkdir(parents=True, exist_ok=True)
        origen.rename(destino)
        moves[hasta] = desde
        text = text.replace(desde[:-3], hasta[:-3])
        for path in vault.rglob('*.md'):
            if path == config or lines.protegida(path):
                continue
            body = path.read_text(encoding='utf-8')
            changed = body.replace(desde[:-3], hasta[:-3])
            if changed != body:
                path.write_bytes(lines.contenido(changed.encode('utf-8')))

    def quitar(path):
        path.resolve().relative_to(vault.resolve())
        path.unlink()

    if caso == 'id-ajeno': text = text.replace('- Identificador: estudio', '- Identificador: otro-proyecto')
    elif caso == 'id-no-portable': text = text.replace('- Identificador: estudio', '- Identificador: ../otra')
    elif caso == 'referencias-ausentes': text = text.replace(refs, '- Ficha e índice: [[ausente]] · [[tambien-ausente]]')
    elif caso == 'sin-ficha-inicial': quitar(cell)
    elif caso == 'indice-otro-proyecto':
        body = index.read_text(encoding='utf-8'); assert 'proyecto: "estudio"' in body
        index.write_text(body.replace('proyecto: "estudio"', 'proyecto: "otro-proyecto"', 1), encoding='utf-8')
    elif caso == 'ficha-renombrada': mover(cell, cell.with_name('Ficha propia.md'))
    elif caso == 'indice-renombrado': mover(index, index.with_name('00 - Índice - Mi estudio.md'))
    elif caso == 'dos-proyectos':
        root = Path(validador.__file__).resolve().parents[2]
        spec = importlib.util.spec_from_file_location('creador_coherencia_publica', root/'crear_proyecto.py')
        creator = importlib.util.module_from_spec(spec); spec.loader.exec_module(creator)
        plan = creator.planificar(vault, {'nombre':'Otro estudio ficticio', 'id':'otro-estudio',
            'objetivo':'Ordenar otra materia', 'descripcion':'Control de proyectos independientes.',
            'contexto':'D', 'fecha':datetime.now().date().isoformat()})
        creator.aplicar(plan, [])
    elif caso == 'formato-heredado':
        start = text.index('## Proyecto inicial'); end = text.index('## Avance de archivos y comprobaciones', start)
        text = text[:start] + text[end:]
    elif caso.startswith('parcial-') and caso != 'parcial-enlace-extra-roto':
        text = text.replace('estado: lista', 'estado: parcial')
        quitar(cell); quitar(index)
        if caso == 'parcial-planificado':
            text = text.replace('- Identificador: estudio', '- Identificador: nuevo-proyecto').replace(refs, '- Ficha e índice: —')
        elif caso == 'parcial-placeholder':
            text = text.replace('- Identificador: estudio', '- Identificador: [completar: identificador]').replace(refs, '- Ficha e índice: —')
    elif caso == 'lista-sin-id': text = text.replace('- Identificador: estudio', '- Identificador: —')
    elif caso == 'id-repetido': text = text.replace('- Identificador: estudio', '- Identificador: estudio\n- Identificador: estudio')
    elif caso == 'seccion-repetida': text += '\n## Proyecto inicial\n- Identificador: otro\n'
    elif caso == 'referencias-repetidas': text = text.replace(refs, refs+'\n'+refs)
    elif caso == 'solo-ficha-ejemplo':
        body = cell.read_text(encoding='utf-8'); assert 'tipo: "celula"' in body and 'ejemplo:' not in body
        cell.write_text(body.replace('tipo: "celula"', 'tipo: "celula"\nejemplo: true', 1), encoding='utf-8')
    elif caso == 'ficha-ambigua': cell.with_name('Ficha duplicada.md').write_bytes(cell.read_bytes())
    elif caso == 'indice-ambiguo':
        other = vault/'indice alternativo/Índice.md'; other.parent.mkdir(); other.write_bytes(index.read_bytes())
    elif caso == 'wiki-corto': text = text.replace(refs, '- Ficha e índice: [[estudio-context.md#Hechos clave|Ficha]] · [[00 - Índice - estudio|Proyecto]]')
    elif caso == 'wiki-corto-ambiguo':
        text = text.replace(refs, '- Ficha e índice: [[estudio-context|Ficha]] · [[00 - Índice - estudio|Proyecto]]')
        other = vault/'Notas/estudio-context.md'; other.parent.mkdir(); other.write_text('# Otra nota\n', encoding='utf-8')
    elif caso == 'markdown-relativo':
        target = quote('../estudio/00 - Índice - estudio.md')
        text = text.replace(refs, '- Ficha e índice: [Ficha](cells/estudio-context.md) · [Proyecto](<'+target+'#Resumen>)')
    elif caso == 'referencias-ajenas': text = text.replace(refs, '- Ficha e índice: [[Panel]] · [[INDICE]]')
    elif caso == 'referencia-externa': text = text.replace(refs, refs+' · [Ejemplo](https://example.invalid/no-leer)')
    elif caso == 'referencia-fuera-raiz': text = text.replace(refs, refs+' · [Fuera](../../fuera.md)')
    elif caso == 'ejemplos-ocultos':
        decoy = '## Proyecto inicial\n- Identificador: falso\n- Ficha e índice: [[no-existe]]\n'
        text = text.replace('## Proyecto inicial', '```md\n'+decoy+'```\n\n%%\n'+decoy+'%%\n\n<!--\n'+decoy+'-->\n\n## Proyecto inicial', 1)
    elif caso == 'enlaces-en-codigo-inline': text = text.replace(refs, '- Ficha e índice: `[[00_CORE/cells/estudio-context]]` · `[[estudio/00 - Índice - estudio]]`')
    elif caso == 'id-backticks': text = text.replace('- Identificador: estudio', '- Identificador: `estudio`')
    elif caso == 'id-con-mayusculas': text = text.replace('- Identificador: estudio', '- Identificador: Estudio')
    elif caso == 'id-otra-seccion': text += '\n## Historial de una idea\n- Identificador: otro-proyecto\n'
    elif caso == 'id-oculto': text = text.replace('- Identificador: estudio', '<!-- - Identificador: estudio -->')
    elif caso == 'referencias-vacias': text = text.replace(refs, '- Ficha e índice: —')
    elif caso == 'etiquetas-enfasis':
        text = text.replace('## Proyecto inicial', '## **Proyecto inicial**').replace('- Identificador: estudio', '1. **Identificador:** `estudio`').replace('- Ficha e índice:', '- **Ficha e índice:**')
    elif caso == 'referencias-prosa': text = text.replace(refs, '- Ficha e índice: pendiente de ubicar')
    elif caso == 'choque-con-ejemplo':
        example = vault/'00_CORE/cells/ejemplo-context.md'; body = example.read_text(encoding='utf-8')
        assert 'proyecto: aprender-python' in body and 'ejemplo: true' in body
        example.write_text(body.replace('proyecto: aprender-python', 'proyecto: estudio', 1), encoding='utf-8')
    elif caso.startswith(('ficha-anidada-', 'ficha-excluida-')):
        new = cell.parent/'activos/estudio-context.md' if caso.startswith('ficha-anidada-') else cell.with_name('TEMPLATE_cell.md')
        mover(cell, new)
        assert new not in validador.buscar_celulas(cell.parent)
        if caso.endswith('invalida'):
            body = new.read_text(encoding='utf-8')
            changed = re.sub(r'^## Próximas acciones\n.*?(?=^## |\Z)', '', body, flags=re.M | re.S)
            assert changed != body; new.write_text(changed, encoding='utf-8')
            assert any('Próximas acciones' in e for e in validador.validar(new)[0])
        else:
            assert validador.validar(new)[0] == []
    elif caso == 'url-suelta': text = text.replace(refs, refs+' · https://example.invalid/no-leer')
    elif caso == 'autolink': text = text.replace(refs, refs+' · <https://example.invalid/no-leer>')
    elif caso == 'parcial-enlace-extra-roto': text = text.replace('estado: lista', 'estado: parcial').replace(refs, refs+' · [[ausente]]')
    elif caso == 'url-solo-en-codigo': text = text.replace(refs, refs+' · `https://example.invalid/no-leer`')
    elif caso != 'coherente': raise AssertionError('Caso sin preparación: '+caso)

    config.write_bytes(lines.contenido(text.replace('- Última operación de mantenimiento: —',
        '- Última operación de mantenimiento: coherencia-proyecto').encode('utf-8')))
    for path in lines.archivos(vault):
        if not lines.protegida(path): path.write_bytes(lines.contenido(path.read_bytes()))
    maps.actualizar(vault)
    after = foto_cierre(vault); changes = []
    for name in sorted(before.keys() | after.keys()):
        if name in moves.values() or before.get(name) == after.get(name): continue
        if name in moves: changes.append({'accion':'renombrar', 'ruta':name, 'desde':moves[name]})
        else: changes.append({'accion':'borrar' if name not in after else 'crear' if name not in before else 'editar', 'ruta':name})
    registry.registrar(vault, {'id':'coherencia-proyecto', 'ia':'Prueba', 'herramienta':'Regresión de cierre',
        'resumen':'Caso ficticio: '+caso, 'verificado':True, 'cambios':changes})
    maps.actualizar(vault)
    snapshot = foto_cierre(vault)
    errors = validador.validar_cierre(vault, 'coherencia-proyecto')
    assert foto_cierre(vault) == snapshot
    assert (errors == []) is ok, errors
    if not ok:
        assert any('proyecto inicial' in e and detalle in e for e in errors), errors


# Raíz del cierre: indicar el destino real sin alterar selección ni API diaria.
def _raiz_cierre_ejecutar(script, cwd, *args):
    return subprocess.run([sys.executable, '-B', str(script), *map(str,args)],
                          cwd=cwd, capture_output=True, text=True, encoding='utf-8')


def _raiz_cierre_mostrada(vault):
    return 'Bóveda revisada: '+str(vault.absolute())


@pytest.mark.parametrize('form',['root','cells'])
def test_raiz_cierre_explicita_desde_otro_directorio(validador,boveda_cierre,tmp_path,form):
    vault,_,_,_ = boveda_cierre()
    before = foto_cierre(vault)
    target = vault if form == 'root' else vault/'00_CORE/cells'
    p = _raiz_cierre_ejecutar(validador.__file__,tmp_path,target,'--cierre','--operacion','cierre-final')
    assert p.returncode == 0 and 'CIERRE VERIFICADO' in p.stdout
    assert _raiz_cierre_mostrada(vault) in p.stdout and foto_cierre(vault) == before


def test_raiz_cierre_implicita_usa_script_y_no_carpeta_actual(validador,boveda_cierre):
    vault,_,_,_ = boveda_cierre()
    root = Path(validador.__file__).resolve().parents[2]
    before,source_before = foto_cierre(vault),foto_cierre(root)
    p = _raiz_cierre_ejecutar(validador.__file__,vault,'--cierre','--operacion','cierre-final')
    assert p.returncode == 1 and 'CIERRE VERIFICADO' not in p.stdout
    assert _raiz_cierre_mostrada(root) in p.stdout and _raiz_cierre_mostrada(vault) not in p.stdout
    assert foto_cierre(vault) == before and foto_cierre(root) == source_before


def test_raiz_cierre_boveda_movida_conserva_archivos(validador,boveda_cierre,tmp_path):
    vault,_,_,_ = boveda_cierre()
    before = foto_cierre(vault)
    moved = tmp_path/'Bóveda movida con espacios'
    assert tmp_path.resolve() in vault.resolve().parents and tmp_path.resolve() in moved.resolve().parents
    vault.rename(moved)
    assert foto_cierre(moved) == before
    p = _raiz_cierre_ejecutar(moved/'00_CORE/schemas/validate.py',tmp_path,'--cierre','--operacion','cierre-final')
    assert p.returncode == 0 and 'CIERRE VERIFICADO' in p.stdout
    assert _raiz_cierre_mostrada(moved) in p.stdout and _raiz_cierre_mostrada(vault) not in p.stdout
    assert foto_cierre(moved) == before


def test_raiz_cierre_dos_bovedas_identifica_la_que_aprueba(validador,boveda_cierre,tmp_path):
    import shutil
    vault,_,_,_ = boveda_cierre()
    other = tmp_path/'Otra bóveda válida'
    shutil.copytree(vault,other)
    config = vault/'00_CORE/configuracion.md'
    config.write_bytes(config.read_bytes()+b'\nCambio sin nueva operacion.\n')
    before,other_before = foto_cierre(vault),foto_cierre(other)
    script = other/'00_CORE/schemas/validate.py'
    implicit = _raiz_cierre_ejecutar(script,vault,'--cierre','--operacion','cierre-final')
    explicit = _raiz_cierre_ejecutar(script,tmp_path,vault,'--cierre','--operacion','cierre-final')
    assert implicit.returncode == 0 and explicit.returncode == 1
    assert 'CIERRE VERIFICADO' in implicit.stdout and 'CIERRE VERIFICADO' not in explicit.stdout
    assert _raiz_cierre_mostrada(other) in implicit.stdout and _raiz_cierre_mostrada(vault) not in implicit.stdout
    assert _raiz_cierre_mostrada(vault) in explicit.stdout
    assert foto_cierre(vault) == before and foto_cierre(other) == other_before


def test_raiz_cierre_destino_inexistente_no_se_crea(validador,boveda_cierre,tmp_path):
    vault,_,_,_ = boveda_cierre()
    target = tmp_path/'No existe'
    before = foto_cierre(vault)
    p = _raiz_cierre_ejecutar(validador.__file__,tmp_path,target,'--cierre','--operacion','cierre-final')
    assert p.returncode == 2 and str(target) in p.stderr
    assert not target.exists() and 'CIERRE VERIFICADO' not in p.stdout and foto_cierre(vault) == before


def test_raiz_cierre_diario_y_api_mantienen_contrato(validador,boveda_cierre):
    vault,_,_,_ = boveda_cierre()
    root = Path(validador.__file__).resolve().parents[2]
    before,source_before = foto_cierre(vault),foto_cierre(root)
    p = _raiz_cierre_ejecutar(validador.__file__,vault)
    assert p.returncode == 0 and str(root/'00_CORE/cells') in p.stdout
    assert 'CIERRE VERIFICADO' not in p.stdout and validador.validar_cierre(vault,'cierre-final') == []
    assert foto_cierre(vault) == before and foto_cierre(root) == source_before


# Regresión CLI: rutas relativas del cierre, conservando la bóveda y sus comprobaciones.
@pytest.mark.parametrize('forma', ['cells-desde-core', 'punto-desde-cells', 'cells-desde-raiz', 'raiz-punto'])
def test_cierre_rutas_relativas_usan_la_boveda_correcta(validador,boveda_cierre,forma):
    vault,_,_,_ = boveda_cierre()
    cwd,ruta = {
        'cells-desde-core': (vault/'00_CORE','cells'),
        'punto-desde-cells': (vault/'00_CORE/cells','.'),
        'cells-desde-raiz': (vault,'00_CORE/cells'),
        'raiz-punto': (vault,'.'),
    }[forma]
    before = foto_cierre(vault)
    result = _raiz_cierre_ejecutar(validador.__file__,cwd,ruta,'--cierre','--operacion','cierre-final')
    assert result.returncode == 0 and 'CIERRE VERIFICADO' in result.stdout
    assert _raiz_cierre_mostrada(vault) in result.stdout.splitlines()
    assert foto_cierre(vault) == before


def test_cierre_cells_relativa_rechaza_configuracion_modificada(validador,boveda_cierre):
    from hashlib import sha256
    vault,_,_,_ = boveda_cierre()
    config = vault/'00_CORE/configuracion.md'
    guardado = sha256(config.read_bytes()).hexdigest()
    config.write_bytes(config.read_bytes()+b'\nCambio posterior al registro.\n')
    actual = sha256(config.read_bytes()).hexdigest()
    before = foto_cierre(vault)
    result = _raiz_cierre_ejecutar(validador.__file__,vault/'00_CORE','cells','--cierre','--operacion','cierre-final')
    assert result.returncode == 1 and 'CIERRE VERIFICADO' not in result.stdout
    assert _raiz_cierre_mostrada(vault) in result.stdout.splitlines()
    error = ('ERROR: Operación "cierre-final": hash de configuración no coincide '
             f'(guardado: {guardado[:12]}..., actual: {actual[:12]}...).')
    assert error in result.stdout.splitlines()
    assert foto_cierre(vault) == before


def test_cierre_cells_relativa_ajena_no_se_confunde_con_boveda(validador,boveda_cierre,tmp_path):
    vault,_,_,_ = boveda_cierre()
    other = tmp_path/'Otra carpeta/cells'
    other.mkdir(parents=True)
    (other/'original.bin').write_bytes(b'\x00Conservar\r\n')
    before = foto_cierre(tmp_path)
    result = _raiz_cierre_ejecutar(validador.__file__,other.parent,'cells','--cierre','--operacion','cierre-final')
    assert result.returncode == 1 and 'CIERRE VERIFICADO' not in result.stdout
    assert _raiz_cierre_mostrada(other) in result.stdout.splitlines()
    assert foto_cierre(tmp_path) == before


@pytest.mark.parametrize('fila,esperado', [
    (r'| A\|B | fin |', ['A|B', 'fin']),
    (r'| A\\|B |', ['A\\', 'B']),
    (r'| A\\\|B |', [r'A\|B']),
    (r'| ruta\nota | |', [r'ruta\nota', '']),
])
def test_fila_inventario_conserva_barras_y_columnas(validador, fila, esperado):
    assert validador._parsear_fila_tabla(fila) == esperado


@pytest.mark.parametrize('copia', ['.trash/configuracion.md', '.obsidian/configuracion.md',
                                   'node_modules/paquete/configuracion.md'])
def test_nombre_corto_del_panel_ignora_carpetas_no_indexadas(validador, tmp_path, copia):
    preparar_configuracion(tmp_path, '[[configuracion]]\n')
    destino = tmp_path / copia
    destino.parent.mkdir(parents=True, exist_ok=True)
    destino.write_text('# Copia vieja\n', encoding='utf-8')
    assert validador.validar_configuracion(tmp_path) == []


def test_nombre_corto_repetido_en_la_boveda_sigue_sin_dar_acceso(validador, tmp_path):
    preparar_configuracion(tmp_path, '[[configuracion]]\n')
    (tmp_path / 'Otra').mkdir()
    (tmp_path / 'Otra/configuracion.md').write_text('# Otra\n', encoding='utf-8')
    assert any('Panel no da acceso' in error for error in validador.validar_configuracion(tmp_path))


def test_inventario_mezclado_explica_la_mezcla(validador, tmp_path):
    preparar_configuracion(tmp_path, '[[00_CORE/configuracion]]\n')
    configuracion = tmp_path / '00_CORE/configuracion.md'
    configuracion.write_text(configuracion.read_text(encoding='utf-8')
                             + '> | otro-item | boveda | pendiente | — | — | — |\n', encoding='utf-8')
    errores = validador.validar_configuracion(tmp_path)
    assert any('mezcla una tabla suelta' in error for error in errores)
    assert not any('no se encuentra tabla' in error for error in errores)
