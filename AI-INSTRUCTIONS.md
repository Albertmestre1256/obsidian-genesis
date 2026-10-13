> [!info] Índice de esta nota (líneas)
> - Líneas 1–6: Este índice
> - Líneas 8–13: Entrada para la IA
> - Líneas 14–21: Antes de trabajar
> - Líneas 22–35: Elegir el recorrido
> - Líneas 36–53: Herramientas opcionales

# Entrada para la IA

Este kit prepara una bóveda mediante preguntas simples; la persona no necesita editar plantillas ni conocer YAML.

Si recibiste la carpeta exterior de un ZIP, ubicá su raíz real: la que contiene `INDICE.md` y estas instrucciones. Si hay varias bóvedas posibles, preguntá cuál usar.

## Antes de trabajar

1. Abrí `INDICE.md` y leelo completo, continuando las páginas si la herramienta recorta la salida. Listar carpetas, buscar palabras o ejecutar el actualizador no completa esta lectura.
2. Leé `00_CORE/atoms/00_vault-rules.md`; ubicá desde el catálogo la ficha del proyecto y el índice del nodo solicitado, si corresponde. Contrastá esas rutas con los archivos reales.
3. Elegí el recorrido de abajo y leé su referencia antes de escribir. Si falta alguna lectura, completala primero; no crees carpetas ni notas todavía.

Al guardar, mantené el mapa según `DOCS/indice-principal.md`. Con una copia adjunta, aclarás qué no podés verificar. En una bóveda existente, respetá su entrada y sus reglas sin sustituirlas. Después de este recorrido, cargá solo el contexto necesario.

## Elegir el recorrido

| Pedido | Referencia |
|---|---|
| Configurar una bóveda nueva, integrar una existente o retomar configuración parcial | `00_CORE/protocols/configurar-vault.md` |
| Completar el perfil, revisar qué falta o retomar datos omitidos | `00_CORE/protocols/personalizar-vault.md` |
| Crear, ampliar o consultar un nodo de notas | «Crear y actualizar un nodo» en `DOCS/indice-principal.md` |
| Retomar, crear otro proyecto, redactar, revisar o cerrar | `DOCS/usar-con-otras-ias.md` |
| Desarrollar o revisar el kit | Atendé ese pedido; no personalices el repositorio ni inicies la entrevista. |

**Leé la referencia elegida antes de escribir.** Para configurar, acordá los datos indispensables que falten y guardá la configuración parcial con su inventario **antes de crear el proyecto**. Derivar un nombre no permite confirmar un objetivo propuesto ni inventar una primera tarea. El creador de proyectos no sustituye este recorrido.

`00_CORE/configuracion.md` se crea durante la configuración, con el inventario de personalización; su ausencia no demuestra una bóveda vacía. Estado parcial: retomá pendientes conservando lo creado. Estado lista: continuá el proyecto sin reiniciar preguntas opcionales. Para completar el perfil, seguí su guía aunque la bóveda esté lista. Buscá fichas por `proyecto`; ante ambigüedad, preguntá. Declarar la bóveda lista exige comprobar también el Panel adaptado y su acceso al inventario; un validador de fichas correcto no comprueba esa integración.

## Herramientas opcionales

Usá los scripts del kit leído, no código preexistente de una bóveda ajena. Python automatiza pasos; sin él, realizalos con herramientas de archivos siguiendo las mismas guías.

| Herramienta | Referencia y alcance |
|---|---|
| `instalar.py` | Integración conservadora; simulá con `python instalar.py "ruta-del-destino" --dry-run` y aplicá con `--yes` dentro del alcance acordado. Conserva archivos y `.obsidian`; `DOCS/instalacion-manual.md` cubre la alternativa. No se usa sobre el propio kit. |
| `crear_proyecto.py` | `DOCS/creacion-para-asistentes.md`; crea ficha, índice y carpetas, sin completar Panel ni configuración. |
| `00_CORE/schemas/validate.py` | «Revisar fichas» de `DOCS/usar-con-otras-ias.md`, incluida revisión manual. |
| `actualizar_indice.py` | `DOCS/indice-principal.md`; mantiene mapa general e índices de nodos, conservando índices propios y resúmenes manuales. |
| `00_CORE/schemas/note_index.py` | `DOCS/mantenimiento.md`; crea, actualiza y comprueba rangos de líneas de notas editables. |
| `00_CORE/schemas/registrar_cambios.py` | Misma guía; registra identidad y cambios, renovando el activo a los cinco días con historial archivado. |

Cada escritura autorizada incluye el mantenimiento de notas, mapas y registro definido en `DOCS/mantenimiento.md`. La IA se identifica y realiza esas operaciones; no las delega al principiante. Al desarrollar este kit, guarda evidencia de desarrollo fuera del contenido distribuible, sin crear un registro personal en el repositorio.

Si una herramienta impide leer o guardar, consultá el mensaje en `DOCS/TROUBLESHOOTING.md` y su guía específica antes de repetirla. Para errores MCP de Claude, usá `DOCS/mcp-claude.md`; si esa conexión impide leer la guía, explicá el límite y pedí el documento o acceso por otra herramienta autorizada, sin fingir una reparación.

`AGENTS.md` y `CLAUDE.md` remiten acá. Claude Code y OpenCode ofrecen `/configurar`, `/empezar`, `/nuevo-proyecto`, `/redactar`, `/validar` y `/cerrar`. En Claude, crear otro proyecto y cerrar conservan invocación manual. Para acceso y arranque: `DOCS/opencode.md` y `DOCS/chatgpt.md`. Los pedidos comunes funcionan con cualquier IA que pueda leer el contexto.
