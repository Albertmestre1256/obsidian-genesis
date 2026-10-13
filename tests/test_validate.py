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


@pytest.mark.parametrize('fallo', ['aviso-panel', 'mapa-general', 'mapa-nodo', 'rango',
    'sin-registro', 'id-ajeno', 'sin-config-en-evento', 'evento-no-verificado',
    'hash-config-viejo', 'registro-roto', 'fecha-futura', 'registro-bloqueado', 'sin-config'])
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
        node = next(p for p in vault.rglob('00 - Índice y Contexto.md') if 'PROJECT_TEMPLATE' not in p.parts)
        note = node.parent / 'Nota nueva.md'
        note.write_bytes(lines.contenido(b'# Nota\n'))
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
    node = next(p for p in vault.rglob('00 - Índice y Contexto.md') if 'PROJECT_TEMPLATE' not in p.parts)
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
                     '00_CORE/schemas/registrar_cambios.py']:
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
