> [!info] Índice de esta nota (líneas)
> - Líneas 1–5: Este índice
> - Líneas 7–12: Entrada para la IA
> - Líneas 13–24: Elegir el recorrido
> - Líneas 25–40: Herramientas opcionales

# Entrada para la IA

Leé primero `INDICE.md` completo y después `00_CORE/atoms/00_vault-rules.md`. Este kit prepara una bóveda mediante preguntas simples; la persona no necesita editar plantillas ni conocer YAML.

El índice muestra lo disponible; contrastalo con la carpeta real al iniciar y mantenelo después de guardar, según `DOCS/indice-principal.md`. Con una copia adjunta, aclarás qué no podés verificar. En una bóveda existente, respetá su entrada y sus reglas sin sustituirlas. Después del mapa, cargá solo el contexto necesario.

## Elegir el recorrido

| Pedido | Referencia |
|---|---|
| Configurar una bóveda nueva, integrar una existente o retomar configuración parcial | `00_CORE/protocols/configurar-vault.md` |
| Completar el perfil, revisar qué falta o retomar datos omitidos | `00_CORE/protocols/personalizar-vault.md` |
| Crear, ampliar o consultar un nodo de notas | «Crear y actualizar un nodo» en `DOCS/indice-principal.md` |
| Retomar, crear otro proyecto, redactar, revisar o cerrar | `DOCS/usar-con-otras-ias.md` |
| Desarrollar o revisar el kit | Atendé ese pedido; no personalices el repositorio ni inicies la entrevista. |

`00_CORE/configuracion.md` se crea durante la configuración, con el inventario de personalización; su ausencia no demuestra una bóveda vacía. Estado parcial: retomá pendientes conservando lo creado. Estado lista: continuá el proyecto sin reiniciar preguntas opcionales. Para completar el perfil, seguí su guía aunque la bóveda esté lista. Buscá fichas por `proyecto`; ante ambigüedad, preguntá.

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

`AGENTS.md` y `CLAUDE.md` remiten acá. Claude Code y OpenCode ofrecen `/configurar`, `/empezar`, `/nuevo-proyecto`, `/redactar`, `/validar` y `/cerrar`. En Claude, crear otro proyecto y cerrar conservan invocación manual. Para acceso y arranque: `DOCS/opencode.md` y `DOCS/chatgpt.md`. Los pedidos comunes funcionan con cualquier IA que pueda leer el contexto.
