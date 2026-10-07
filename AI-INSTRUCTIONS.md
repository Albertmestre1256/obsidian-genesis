# Entrada para la IA

Este kit permite que una persona entregue la carpeta, responda preguntas simples y reciba su bóveda de Obsidian preparada. La IA realiza la configuración; el usuario no necesita editar plantillas ni aprender términos técnicos.

## Primero, las reglas

Leé `00_CORE/atoms/00_vault-rules.md` antes de elegir proyecto o destino. Si vas a integrar el kit en una bóveda existente, leé también sus reglas y conservá sus convenciones. No confundas este repositorio con la bóveda personal de quien desarrolla el kit.

## Elegir el recorrido

| Pedido | Acción |
|---|---|
| «Configurá mi bóveda», «quiero empezar», «no sé usar esta carpeta» | Seguí `00_CORE/protocols/configurar-vault.md`. Comprobá acceso, conversá y configurá con sus respuestas. |
| Retomar un proyecto | Leé su ficha en `00_CORE/cells/`, buscando también por la propiedad `proyecto`. Cargá solo los archivos necesarios. |
| Desarrollar, revisar o corregir el kit | Trabajá sobre el pedido técnico. No inicies la entrevista ni personalices el repositorio con datos del mantenedor. |

Si el pedido ya aclara qué quiere, actuá sobre ese alcance. No reinicies la configuración por la ausencia de un archivo marcador. `00_CORE/configuracion.md` se crea durante un arranque real; no viene rellenado en el kit público.

Con configuración vigente, «quiero empezar» o «seguí» significa retomar el proyecto indicado. Si no está claro cuál, ofrecé los proyectos propios disponibles; no elijas el ejemplo como destino. No vuelvas a preguntar datos ya guardados.

## Instalación en una bóveda existente

Identificá origen y destino reales antes de escribir. Con Python, ejecutá `instalar.py` desde el kit y pasale el destino; `--dry-run` muestra el plan y `--yes` aplica la copia ya autorizada. El instalador no reemplaza archivos y no cambia `.obsidian`. Ante conflictos, compará y proponé una integración puntual, sin forzar la copia.

Sin Python, usá tus herramientas para agregar solo archivos ausentes: `00_CORE/`, `PROJECT_TEMPLATE/`, `DOCS/`, `.claude/`, `Panel.md`, `Proyectos.base`, `AI-INSTRUCTIONS.md`, `AGENTS.md`, `CLAUDE.md` y `crear_proyecto.py`. No reemplaces instrucciones locales ni ajustes existentes. No sigas enlaces simbólicos o junctions fuera del destino. La guía manual está en `DOCS/instalacion-manual.md`, para quien elija hacerlo por su cuenta.

Una bóveda nueva en la carpeta descargada ya tiene los archivos: no ejecutes el instalador sobre sí mismo. Para una nueva en otra ubicación, el protocolo de configuración explica qué copiar.

Para crear el índice y la ficha con Python, el kit incluye `crear_proyecto.py`. Consultá `DOCS/creacion-para-asistentes.md` solo cuando vayas a usarlo. Es opcional: sin Python, hacé la misma creación con tus herramientas de archivos. La persona sigue respondiendo preguntas; no necesita ejecutar comandos.

## Trabajo diario

- Ningún proyecto es el destino por defecto. aprender-python es un ejemplo ficticio.
- Antes de editar, leé el estado actual. La ficha conserva hechos con fuente, decisiones y próximos pasos; los borradores van en el proyecto correspondiente.
- Para un texto breve, usá los datos disponibles. Para escritura elaborada, consultá `00_CORE/protocols/context-injection.md`.
- Al cerrar, proponé los cambios nuevos y aplicá el plan aprobado sin repetir la aprobación del mismo alcance.
- Un adjunto es una copia. Sin acceso a archivos, no afirmes que guardaste o sincronizaste algo.

## Verificar

Con Python, ejecutá el validador del kit: `python 00_CORE/schemas/validate.py` (también puede ser `python3` o `py`). Admite como argumento una carpeta de fichas distinta; no ejecutes un script preexistente del destino. El código 0 significa ausencia de errores de formato, no veracidad comprobada; puede haber avisos.

Sin Python, seguí `.claude/skills/validar/SKILL.md` y las reglas del validador como revisión manual. Informá qué se verificó y qué falta.

Entradas: `AGENTS.md` para asistentes que lo reconocen y `CLAUDE.md` para Claude Code. `/configurar` y el pedido en lenguaje natural comparten el mismo protocolo. El flujo diario está en `DOCS/usar-con-otras-ias.md`.
