---
tipo: guia-documentos
descripcion: "Qué contiene cada documento del kit, para qué sirve y cuándo consultarlo."
---
> [!info]- Índice de esta nota (líneas)
> - Líneas 1–4: Propiedades
> - Líneas 5–17: Este índice
> - Líneas 19–26: Guía de documentos y herramientas del kit
> - Líneas 27–37: Índice de esta guía
> - Líneas 38–47: Entradas
> - Líneas 48–65: Reglas y proyectos
> - Líneas 66–85: Ayuda
> - Líneas 86–99: Integraciones y ajustes
> - Líneas 100–113: Python y pruebas
> - Líneas 114–124: Repositorio y créditos
> - Líneas 125–133: Recursos opcionales
> - Líneas 134–146: Archivos creados durante el uso

# Guía de documentos y herramientas del kit

**README principal y sus idiomas:** [Español](../README.md) · [English](../README.en.md) · [Deutsch](../README.de.md) · [中文](../README.zh.md)

**Esta guía en otros idiomas:** [Español](README.md) · [English](README.en.md) · [Deutsch](README.de.md) · [中文](README.zh.md)

No necesitás leer todo para empezar: seguí el README principal y respondé las preguntas de tu IA. Esta guía sirve para entender los archivos o encontrar ayuda. Las rutas son las mismas en todos los idiomas; las instrucciones comunes del kit siguen en español. Esta guía describe el repositorio completo y se consulta en la carpeta descargada del kit. Al integrar el kit en otra bóveda, se conserva aquí junto con las pruebas y la documentación de desarrollo; la ayuda de uso sí se copia.

## Índice de esta guía

- [Entradas](#entradas)
- [Reglas y proyectos](#reglas-y-proyectos)
- [Ayuda](#ayuda)
- [Integraciones y ajustes](#integraciones-y-ajustes)
- [Python y pruebas](#python-y-pruebas)
- [Repositorio y créditos](#repositorio-y-créditos)
- [Recursos opcionales](#recursos-opcionales)
- [Archivos creados durante el uso](#archivos-creados-durante-el-uso)

## Entradas

| Documento o herramienta | Función |
|---|---|
| [`README.md`](../README.md) · [`README.en.md`](../README.en.md) · [`README.de.md`](../README.de.md) · [`README.zh.md`](../README.zh.md) | Inicio, estado y mensaje para configurar con una IA. |
| [`LEER_PRIMERO.md`](../LEER_PRIMERO.md) | Puerta de entrada que conecta Panel, mapa y reglas. |
| [`Panel.md`](../Panel.md) | Acceso cotidiano a proyectos y tareas. |
| [`INDICE.md`](../INDICE.md) | Catálogo real de toda la bóveda; primera lectura de la IA. |
| [`AI-INSTRUCTIONS.md`](../AI-INSTRUCTIONS.md) · [`AGENTS.md`](../AGENTS.md) · [`CLAUDE.md`](../CLAUDE.md) | La entrada para asistentes elige el recorrido; AGENTS y CLAUDE remiten a ella. |

## Reglas y proyectos

| Documento o herramienta | Función |
|---|---|
| [`00_CORE/atoms/00_vault-rules.md`](../00_CORE/atoms/00_vault-rules.md) | Reglas compartidas: contexto, conservación, enlaces y autoría. |
| [`00_CORE/protocols/configurar-vault.md`](../00_CORE/protocols/configurar-vault.md) | Entrevista y creación de una bóveda con datos parciales. |
| [`00_CORE/protocols/personalizar-vault.md`](../00_CORE/protocols/personalizar-vault.md) | Inventario de respuestas, omisiones y datos que se pueden completar después. |
| [`00_CORE/protocols/context-injection.md`](../00_CORE/protocols/context-injection.md) | Qué contexto cargar según el pedido, sin leer toda la bóveda. |
| [`00_CORE/protocols/ai-write-protocol.md`](../00_CORE/protocols/ai-write-protocol.md) | Preparar, redactar y revisar un texto con contexto suficiente. |
| [`00_CORE/molecules/marco-comunicacion-general.md`](../00_CORE/molecules/marco-comunicacion-general.md) | Elegir propósito, destinatario y tipo de comunicación. |
| [`00_CORE/cognitive-tools/redaccion-tecnica.md`](../00_CORE/cognitive-tools/redaccion-tecnica.md) · [`00_CORE/cognitive-tools/redaccion-narrativa.md`](../00_CORE/cognitive-tools/redaccion-narrativa.md) · [`00_CORE/cognitive-tools/redaccion-operativa.md`](../00_CORE/cognitive-tools/redaccion-operativa.md) · [`00_CORE/cognitive-tools/redaccion-persuasiva.md`](../00_CORE/cognitive-tools/redaccion-persuasiva.md) | Guías de redacción técnica, narrativa, operativa y persuasiva, según la tarea. |
| [`00_CORE/cells/ejemplo-context.md`](../00_CORE/cells/ejemplo-context.md) | Ejemplo ficticio para entender una ficha; no son tus datos. |
| [`00_CORE/templates/TEMPLATE_cell.md`](../00_CORE/templates/TEMPLATE_cell.md) | Modelo de ficha de proyecto. |
| [`00_CORE/templates/TEMPLATE_configuracion.md`](../00_CORE/templates/TEMPLATE_configuracion.md) | Modelo de configuración e inventario opcional y reanudable. |
| [`00_CORE/templates/TEMPLATE_nodo.md`](../00_CORE/templates/TEMPLATE_nodo.md) | Modelo de índice para una colección de notas. |
| [`PROJECT_TEMPLATE/00 - Índice y Contexto.md`](../PROJECT_TEMPLATE/00%20-%20%C3%8Dndice%20y%20Contexto.md) | Base para el índice conectado de cada proyecto nuevo. |
| [`PROJECT_TEMPLATE/01_FUENTES/README.md`](../PROJECT_TEMPLATE/01_FUENTES/README.md) · [`PROJECT_TEMPLATE/02_SINTESIS/README.md`](../PROJECT_TEMPLATE/02_SINTESIS/README.md) · [`PROJECT_TEMPLATE/03_ENTREGABLES/README.md`](../PROJECT_TEMPLATE/03_ENTREGABLES/README.md) · [`PROJECT_TEMPLATE/_archivo/README.md`](../PROJECT_TEMPLATE/_archivo/README.md) | Explican dónde van originales, trabajo, resultados e historia. |

## Ayuda

| Documento o herramienta | Función |
|---|---|
| [`DOCS/QUICKSTART.md`](../DOCS/QUICKSTART.md) | Atajo al inicio principal y a las guías de acceso. |
| [`DOCS/empezar-con-ia.md`](../DOCS/empezar-con-ia.md) | Cómo dar acceso real a una carpeta o trabajar con una copia adjunta. |
| [`DOCS/opencode.md`](../DOCS/opencode.md) | Abrir el kit y usar sus comandos desde OpenCode. |
| [`DOCS/chatgpt.md`](../DOCS/chatgpt.md) | Recorridos de ChatGPT con carpeta o archivos adjuntos. |
| [`DOCS/usar-con-otras-ias.md`](../DOCS/usar-con-otras-ias.md) | Pedidos de uso diario para retomar, redactar o guardar avances. |
| [`DOCS/primer-proyecto.md`](../DOCS/primer-proyecto.md) | Crear un proyecto a mano como alternativa. |
| [`DOCS/instalacion-manual.md`](../DOCS/instalacion-manual.md) | Integrar el kit sin ejecutar Python. |
| [`DOCS/creacion-para-asistentes.md`](../DOCS/creacion-para-asistentes.md) | Referencia técnica para que la IA prepare archivos del proyecto. |
| [`DOCS/indice-principal.md`](../DOCS/indice-principal.md) | Mantener el mapa, los índices locales y sus enlaces escalables. |
| [`DOCS/mantenimiento.md`](../DOCS/mantenimiento.md) | Actualizar rangos, mapas y registro, y comprobar el cierre. |
| [`DOCS/obsidian.md`](../DOCS/obsidian.md) | Plantillas, Panel, Bases y gráfico dentro de Obsidian. |
| [`DOCS/TROUBLESHOOTING.md`](../DOCS/TROUBLESHOOTING.md) | Errores frecuentes y cómo diagnosticar el paso impedido. |
| [`DOCS/mcp-claude.md`](../DOCS/mcp-claude.md) | Diagnóstico de conexión y esquemas MCP en Claude. |
| [`DOCS/prueba-con-usuarios.md`](../DOCS/prueba-con-usuarios.md) | Guion y criterios para probar el kit con principiantes reales. |
| [`DOCS/publicacion.md`](../DOCS/publicacion.md) | Controles pendientes antes de publicar una versión. |

## Integraciones y ajustes

| Documento o herramienta | Función |
|---|---|
| [`.claude/skills/configurar/SKILL.md`](../.claude/skills/configurar/SKILL.md) · [`.opencode/commands/configurar.md`](../.opencode/commands/configurar.md) | /configurar: iniciar la entrevista o retomar una configuración parcial. |
| [`.claude/skills/empezar/SKILL.md`](../.claude/skills/empezar/SKILL.md) · [`.opencode/commands/empezar.md`](../.opencode/commands/empezar.md) | /empezar: cargar el contexto del proyecto y continuar. |
| [`.claude/skills/nuevo-proyecto/SKILL.md`](../.claude/skills/nuevo-proyecto/SKILL.md) · [`.opencode/commands/nuevo-proyecto.md`](../.opencode/commands/nuevo-proyecto.md) | /nuevo-proyecto: acordar y agregar otro proyecto. |
| [`.claude/skills/redactar/SKILL.md`](../.claude/skills/redactar/SKILL.md) · [`.opencode/commands/redactar.md`](../.opencode/commands/redactar.md) | /redactar: escribir con el contexto y los hechos disponibles. |
| [`.claude/skills/validar/SKILL.md`](../.claude/skills/validar/SKILL.md) · [`.opencode/commands/validar.md`](../.opencode/commands/validar.md) | /validar: revisar fichas y explicar errores o avisos. |
| [`.claude/skills/cerrar/SKILL.md`](../.claude/skills/cerrar/SKILL.md) · [`.opencode/commands/cerrar.md`](../.opencode/commands/cerrar.md) | /cerrar: proponer guardar cambios y verificar lo aprobado. |
| [`.claude/skills/vault-manager/SKILL.md`](../.claude/skills/vault-manager/SKILL.md) · [`.claude/settings.json`](../.claude/settings.json) | Orientación de uso de la bóveda y ajustes de la integración Claude. |
| [`.obsidian/app.json`](../.obsidian/app.json) · [`.obsidian/core-plugins.json`](../.obsidian/core-plugins.json) · [`.obsidian/graph.json`](../.obsidian/graph.json) · [`.obsidian/templates.json`](../.obsidian/templates.json) · [`.obsidian/appearance.json`](../.obsidian/appearance.json) · [`.obsidian/snippets/genesis-vista-simple.css`](../.obsidian/snippets/genesis-vista-simple.css) | Ajustes iniciales y vista simple activa en una bóveda nueva; conservar los propios al integrar. |
| [`Proyectos.base`](../Proyectos.base) | Tabla de proyectos que usa el Panel; no es una nota ni un script. |

## Python y pruebas

Python automatiza tareas; no hace falta programar para usar el kit con una IA que pueda gestionar archivos. Las pruebas son para quienes desarrollan el kit y el instalador no las copia a una bóveda instalada.

| Documento o herramienta | Función |
|---|---|
| [`instalar.py`](../instalar.py) | Agregar el kit a otra bóveda sin reemplazar archivos existentes. |
| [`crear_proyecto.py`](../crear_proyecto.py) | Crear ficha y carpetas de un proyecto acordado. |
| [`actualizar_indice.py`](../actualizar_indice.py) | Generar o comprobar el índice general y los índices de nodos. |
| [`00_CORE/schemas/validate.py`](../00_CORE/schemas/validate.py) | Revisar fichas/configuración; con --cierre, contrastar una operación. |
| [`00_CORE/schemas/note_index.py`](../00_CORE/schemas/note_index.py) | Calcular y comprobar los rangos de líneas de notas editables. |
| [`00_CORE/schemas/registrar_cambios.py`](../00_CORE/schemas/registrar_cambios.py) | Registrar autoría, archivos modificados e historial conservado. |
| [`tests/conftest.py`](../tests/conftest.py) · [`tests/test_crear_proyecto.py`](../tests/test_crear_proyecto.py) · [`tests/test_indice.py`](../tests/test_indice.py) · [`tests/test_instalar.py`](../tests/test_instalar.py) · [`tests/test_kit.py`](../tests/test_kit.py) · [`tests/test_mantenimiento.py`](../tests/test_mantenimiento.py) · [`tests/test_nodos.py`](../tests/test_nodos.py) · [`tests/test_validate.py`](../tests/test_validate.py) | Preparación compartida y pruebas de creación, índices, instalación, paquete, mantenimiento, nodos y validación. |

## Repositorio y créditos

| Documento o herramienta | Función |
|---|---|
| [`LICENSE`](../LICENSE) | Licencia MIT y atribución de davidkimai y Albert Mestre. |
| [`CHANGELOG.md`](../CHANGELOG.md) | Cambios del kit por versión o fecha. |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | Cómo contribuir, pedir ayuda y comprobar cambios. |
| [`.github/ISSUE_TEMPLATE/no-me-funciona.md`](../.github/ISSUE_TEMPLATE/no-me-funciona.md) | Formulario breve para informar un fallo con un ejemplo ficticio. |
| [`.github/workflows/tests.yml`](../.github/workflows/tests.yml) | Definición de las pruebas remotas de GitHub Actions. |
| [`.gitignore`](../.gitignore) | Archivos locales que Git debe omitir. |

## Recursos opcionales

| Documento o herramienta | Función |
|---|---|
| [`00_CORE/davidkimai-resources/README.md`](../00_CORE/davidkimai-resources/README.md) | Entrada a recursos adaptados del trabajo original; lectura opcional. |
| [`00_CORE/davidkimai-resources/protocols/01_extract_information.md`](../00_CORE/davidkimai-resources/protocols/01_extract_information.md) | Extraer información de una fuente sin inventar lo que falta. |
| [`00_CORE/davidkimai-resources/evaluation/token_budgeting.md`](../00_CORE/davidkimai-resources/evaluation/token_budgeting.md) | Elegir contexto suficiente sin cargar material irrelevante. |
| [`00_CORE/davidkimai-resources/field-theory/field_dynamics.md`](../00_CORE/davidkimai-resources/field-theory/field_dynamics.md) | Modelo conceptual opcional para relacionar y mantener contexto. |

## Archivos creados durante el uso

Estos archivos no vienen personalizados en el kit: la IA los crea con tus respuestas. Los nombres de proyectos son ejemplos de rutas, no archivos que debas crear a mano. En las rutas de ejemplo, `{ID}` o `ID` representa el identificador elegido para el proyecto; no es un nombre literal.

| Documento o herramienta | Función |
|---|---|
| `00_CORE/configuracion.md` | Respuestas, datos omitidos y estado de la configuración; permite retomar sin repetir preguntas. |
| `00_CORE/cells/{ID}-context.md` | Ficha de cada proyecto: objetivo, hechos, decisiones y próximas acciones. |
| `ID/00 - Índice - ID.md` | Índice propio del proyecto; conecta sus notas y subnodos. Un nodo independiente también tiene índice. |
| `ID/01_FUENTES/ · ID/02_SINTESIS/ · ID/03_ENTREGABLES/ · ID/_archivo/` | Originales, trabajo en curso, resultados y material histórico, según el alcance acordado. |
| `00_CORE/logs/registro-cambios.md · 00_CORE/logs/historial/` | Registro identificado de cambios; al renovarlo después de cinco días, conserva el anterior archivado. |

El índice general mantiene el inventario real. Esta guía explica funciones y no sustituye las reglas ni ordena cargar todos los documentos en cada conversación.
