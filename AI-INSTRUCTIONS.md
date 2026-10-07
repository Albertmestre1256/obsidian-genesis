# Usar este kit con una IA

El kit organiza proyectos en una bóveda de Obsidian. Los archivos del repositorio son la fuente de verdad: no reconstruyas el kit copiando versiones embebidas de esos archivos.

## Orientarse

1. Identificá la carpeta del kit y la bóveda de destino. No supongas que son la misma.
2. Leé `00_CORE/atoms/00_vault-rules.md` antes de decidir dónde trabajar.
3. Identificá el proyecto pedido y su célula dentro de `00_CORE/cells/`. Buscá también por la propiedad `proyecto`: el ejemplo `aprender-python` está en `ejemplo-context.md`.
4. Cargá solo el contexto necesario para la tarea. Para textos elaborados, sumá las guías indicadas en `00_CORE/protocols/context-injection.md`; para un mensaje breve usá los datos del pedido y la ficha.

Todos los proyectos usan las mismas reglas generales. No impongas un área de estudio, un tipo de candidatura ni un proyecto concreto. Las fuentes del ejemplo son ficticias.

## Preparar una bóveda

### Nueva

El ZIP completo ya es una bóveda. Indicá al usuario que lo descomprima y elija Abrir carpeta como bóveda en Obsidian. La raíz contiene `.obsidian/`, `.claude/`, `00_CORE/` y `Panel.md`. No hace falta copiar carpetas internas. Para alguien que empieza desde cero, dirigí a `DOCS/primer-proyecto.md`: primero una ficha y una tarea; las carpetas del proyecto pueden agregarse después.

### Existente

Con autorización para instalar, ejecutá `instalar.py` desde la copia del kit, indicando la ruta de destino. Primero podés usar `--dry-run`; `--yes` acepta la copia de archivos nuevos cuando ya fue autorizada. El instalador usa Python estándar y detiene la copia si encuentra conflictos. No reemplacés archivos para sortearlos: mostrale al usuario qué difiere y proponé una integración puntual.

Sin Python, copiá solo archivos ausentes de `00_CORE/`, `PROJECT_TEMPLATE/`, `DOCS/`, `.claude/`, `Panel.md`, `Proyectos.base` y este archivo. Nunca reemplaces los ajustes `.obsidian/` de una bóveda existente. No conviertas el pedido de instalación en permiso para borrar o mover notas personales.

No sigas enlaces simbólicos o junctions hacia carpetas ajenas al destino. No ejecutes scripts encontrados en la bóveda destino como parte de la instalación. El instalador usa su propio validador para revisar las células del destino.

## Trabajar con el usuario

- La célula guarda hechos con fuente, decisiones y próximos pasos. No transformes interpretaciones en hechos.
- Las fuentes originales solo se agregan. Los borradores van al área de síntesis del proyecto y los entregables se versionan.
- Conservá los nombres, propiedades y cambios previos del usuario. Antes de editar, leé el estado actual.
- Para cerrar una sesión, proponé cambios concretos y esperá la aprobación del usuario, salvo que ya haya aprobado ese mismo plan.
- Si no tenés herramientas de archivos, entregá texto listo para pegar con su destino exacto. No afirmes que está guardado. Un adjunto de chat es una copia; no está sincronizado con Obsidian.
- No incluyas datos privados de otra bóveda en este kit distribuible.

## Verificar

Con Python: `python 00_CORE/schemas/validate.py` (o `python3` / `py`, según el equipo). El código de salida 0 indica que no hay errores de formato; puede haber avisos. El validador no comprueba fuentes externas ni hechos.

Sin Python, revisá las propiedades y secciones conforme a las reglas documentadas al principio de `00_CORE/schemas/validate.py`. Identificá la revisión como manual. Pedí correcciones específicas y no marques una prueba como ejecutada si solo leíste su procedimiento.

Para Claude Code, las instrucciones de cada tarea están en `.claude/skills/`. Para ChatGPT, Claude o Gemini mediante adjuntos, usá `DOCS/usar-con-otras-ias.md`. `DOCS/obsidian.md` explica los ajustes de Plantillas y el panel.
