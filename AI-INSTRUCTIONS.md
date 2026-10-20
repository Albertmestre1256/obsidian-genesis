> [!info]- Índice de esta nota (líneas)
> - Líneas 1–6: Este índice
> - Líneas 8–11: Entrada para la IA
> - Líneas 12–17: Antes de trabajar
> - Líneas 18–30: Elegir el recorrido
> - Líneas 31–49: Herramientas opcionales

# Entrada para la IA

Configurá la bóveda con preguntas simples; la persona no edita plantillas ni necesita conocer YAML.

## Antes de trabajar

1. Ubicá la raíz que contiene `INDICE.md` y estas instrucciones, incluso dentro de un ZIP. Ante varias bóvedas posibles, preguntá cuál usar.
2. Leé `INDICE.md` completo, continuando si la salida se recorta; listar archivos o ejecutar el actualizador no sustituye esa lectura. Después leé `00_CORE/atoms/00_vault-rules.md` y ubicá la ficha por `proyecto` o el índice del nodo solicitado, contrastando sus rutas reales. En una bóveda existente, respetá su entrada y sus reglas.
3. Leé la referencia del recorrido elegido **antes de escribir**; después cargá solo el contexto necesario. Reutilizá las lecturas vigentes de esta sesión. Con adjuntos, aclarás los límites de acceso y comprobación.

## Elegir el recorrido

| Pedido | Referencia obligatoria |
|---|---|
| Configurar una bóveda nueva, integrar una existente o retomar configuración parcial | `00_CORE/protocols/configurar-vault.md`: preguntas, configuración e inventario antes del proyecto, Panel y comprobación de entrega. |
| Completar el perfil, revisar faltantes o retomar datos omitidos, también con la bóveda lista | `00_CORE/protocols/personalizar-vault.md` |
| Retirar de una bóveda lista el material del kit que ya no se usa | «Retirar material del kit que ya no usás» en `DOCS/obsidian.md`, sin repetir la entrevista |
| Crear, ampliar o consultar un nodo | «Crear y actualizar un nodo» en `DOCS/indice-principal.md` |
| Retomar, crear otro proyecto, redactar, revisar o cerrar | Sección correspondiente de `DOCS/usar-con-otras-ias.md` |
| Desarrollar o revisar el kit | Atendé ese pedido sin personalizar el repositorio ni iniciar la entrevista. |

Una idea de proyecto no confirma datos pendientes; crear una ficha no completa la configuración. El protocolo distingue configuración parcial, bóveda lista y ausencia de configuración: conservá el trabajo y las omisiones al retomar.

## Herramientas opcionales

Usá herramientas del kit leído, no código preexistente de otra bóveda. Python automatiza las guías; sin él, seguí sus alternativas con herramientas de archivos.

| Herramienta | Cuándo y dónde consultar |
|---|---|
| `instalar.py` | Para integrar otra bóveda: simulá con `python instalar.py "ruta-del-destino" --dry-run` y aplicá con `--yes` dentro del alcance acordado. Conserva archivos y `.obsidian`; alternativa en `DOCS/instalacion-manual.md`. No se usa sobre el propio kit. |
| `crear_proyecto.py` | `DOCS/creacion-para-asistentes.md`; crea ficha, índice y carpetas, sin completar Panel ni configuración. |
| `00_CORE/schemas/validate.py` | «Revisar fichas» en `DOCS/usar-con-otras-ias.md`, incluida revisión manual. |
| `actualizar_indice.py` | `DOCS/indice-principal.md`: mapas generales y locales. |
| `00_CORE/schemas/note_index.py` y `00_CORE/schemas/registrar_cambios.py` | `DOCS/mantenimiento.md`: rangos, autoría y registro de cambios. |

Para rangos, fichas, mapas y hashes del registro, decidí con la salida de la herramienta y no con otra revisión de IA. Consultá primero con los modos que no escriben de su guía (`validate.py`, `note_index.py check`, `--dry-run`) y aplicá solo dentro del alcance acordado. Informá estado, archivos afectados y errores concretos; leé el rango o filtro necesario sin volcar cuerpos, logs ni árboles completos. Una salida correcta acredita formato o igualdad, no la verdad del contenido. Sin Python, comprobá por lectura según la guía y declará lo no comprobado.

Cada escritura incluye el mantenimiento de `DOCS/mantenimiento.md`, realizado por la IA. Al desarrollar el kit, guardá la evidencia fuera de su contenido distribuible, sin crear un registro personal en el repositorio.

Ante fallos de lectura o escritura, consultá `DOCS/TROUBLESHOOTING.md` y la guía de la herramienta antes de repetirla. Para errores MCP de Claude: `DOCS/mcp-claude.md`; si tampoco podés leerla, explicá el límite y pedí el documento o acceso autorizado.

Claude Code ofrece las skills de `.claude/skills/`; para acceso y comandos de OpenCode, consultá `DOCS/opencode.md`; para ChatGPT, `DOCS/chatgpt.md`. Los mismos recorridos funcionan con pedidos comunes y cualquier IA con acceso real.
