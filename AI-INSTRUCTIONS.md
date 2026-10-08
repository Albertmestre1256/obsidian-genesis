# Entrada para la IA

Leé primero `INDICE.md` completo, después `00_CORE/atoms/00_vault-rules.md`. Este kit prepara una bóveda mediante preguntas simples; la persona no necesita editar plantillas ni conocer YAML.

El índice es el mapa común: proyectos, notas, recursos y herramientas. Contrastalo con la carpeta real al iniciar y actualizalo después de guardar cambios, antes de entregar o cerrar. Usá `actualizar_indice.py` del kit leído o tus herramientas de archivos, según `DOCS/indice-principal.md`. Si falta, quedó desactualizado o solo tenés una copia adjunta, aclaralo y verificá las rutas necesarias; no supongas que un enlace prueba acceso. En una bóveda con índice propio, seguí la entrada acordada y sus reglas sin sustituirlas. Leer el mapa no obliga a cargar todas las notas.

## Elegir el recorrido

| Pedido | Qué leer y hacer |
|---|---|
| Configurar una bóveda nueva o adaptar una existente | Seguí `00_CORE/protocols/configurar-vault.md`; incluye entrevista, integración y verificación. |
| «Seguí» o «quiero empezar», con configuración vigente | Leé `00_CORE/configuracion.md` y la ficha del proyecto indicado. Retomá lo pendiente; si hay varios proyectos y no está claro cuál, preguntá. |
| Trabajar en un proyecto | Buscá su ficha por la propiedad `proyecto`. Sumá fuentes o índice solo cuando la tarea los necesite. |
| Escribir un texto elaborado | Consultá `00_CORE/protocols/context-injection.md` para elegir las guías. |
| Desarrollar o revisar el kit | Atendé ese pedido; no inicies la entrevista ni personalices el repositorio. |

La ausencia de `00_CORE/configuracion.md` no demuestra que la bóveda esté vacía. Esa nota se crea al configurar, no viene rellenada en el kit. Si la configuración quedó parcial, conservá lo creado y retomá solo lo pendiente. Una bóveda lista no implica que el proyecto esté terminado.

Al configurar, guardá primero las respuestas acordadas con estado parcial y actualizá el avance por grupos de archivos según el protocolo. Para retomar una ficha editada, leé su contenido vigente y completá lo pendiente; no la recrees con el creador ni repitas la entrevista.

## Herramientas opcionales

- **Integrar en una bóveda existente:** desde el kit leído, ejecutá `python instalar.py "ruta-del-destino" --dry-run`. Revisá el plan y aplicá con `--yes` dentro del alcance autorizado. No reemplaza archivos ni ajustes de `.obsidian`; ante conflictos, compará y proponé una integración puntual. Sin Python, seguí `DOCS/instalacion-manual.md` con tus herramientas de archivos.
- **Crear índice, ficha y carpetas:** `crear_proyecto.py`; consultá `DOCS/creacion-para-asistentes.md` si lo vas a usar. No completa el Panel ni la nota de configuración.
- **Revisar fichas:** `python 00_CORE/schemas/validate.py`, opcionalmente con la carpeta de fichas como argumento. Ejecutá el validador del kit leído, no código preexistente de una bóveda ajena. Sin Python, aplicá la revisión manual de `.claude/skills/validar/SKILL.md`.

En una bóveda nueva dentro de la carpeta descargada, los archivos ya están: no ejecutes el instalador sobre sí mismo. Con convenciones propias, respetá las reglas del destino y adaptá los archivos dentro del alcance acordado.

`AGENTS.md` y `CLAUDE.md` remiten a esta guía. OpenCode incluye `/configurar` en `.opencode/commands/` y usa este mismo protocolo; consultá `DOCS/opencode.md` para su acceso. ChatGPT sigue `DOCS/chatgpt.md`, con carpeta local o copia descargable según sus herramientas. Claude Code incluye `/configurar` y skills de trabajo diario; `/nuevo-proyecto` y `/cerrar` conservan su invocación manual. Los pedidos comunes están en `DOCS/usar-con-otras-ias.md`.
