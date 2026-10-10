> [!info] Índice de esta nota (líneas)
> - Líneas 1–3: Este índice
> - Líneas 5–21: Agregar el kit a una bóveda sin Python

# Agregar el kit a una bóveda sin Python

Usá esta guía si ya tenés una bóveda. Conservá la carpeta descargada del kit separada de la bóveda de destino.

1. Abrí ambas carpetas en el explorador de archivos.
2. Desde el kit, copiá a la raíz de tu bóveda estas carpetas: `00_CORE/`, `PROJECT_TEMPLATE/`, `DOCS/`, `.claude/` y `.opencode/`. Agregá también `Panel.md`, `Proyectos.base`, `AI-INSTRUCTIONS.md`, `AGENTS.md`, `CLAUDE.md`, `crear_proyecto.py` y `actualizar_indice.py`.
3. Si una carpeta ya existe, agregá dentro solo los archivos que falten. Ante un archivo con el mismo nombre, elegí **Omitir**, aunque su contenido sea diferente. Si el explorador solo ofrece reemplazar la carpeta completa, cancelá y copiá los archivos ausentes por separado.
4. Conservá `.obsidian/` tal como está en tu bóveda: no la copies desde el kit. Para habilitar las funciones opcionales, seguí [Plantillas y panel de proyectos](obsidian.md).
5. En Obsidian, abrí [Panel](../Panel.md) y seguí [Usar con otras IAs](usar-con-otras-ias.md) o los comandos de Claude Code.

Si omitiste archivos del kit que ya tenían contenido diferente, compará ambas versiones antes de seguir sus instrucciones. Conservar el archivo existente evita reemplazar tus reglas y notas, pero no actualiza su contenido.

Las carpetas `.claude/` y `.opencode/` pueden estar ocultas en el explorador. En macOS, mostrá los archivos ocultos con `Cmd + Shift + .`; en Windows, con Ver → Mostrar → Elementos ocultos si hace falta.

El kit funciona sin Python. Si más adelante lo instalás, podés revisar tus fichas desde la raíz de la bóveda con `python 00_CORE/schemas/validate.py` (o `python3` / `py`, según el equipo).

Antes de terminar, agregá o integrá `INDICE.md` como entrada principal y actualizá su catálogo con los archivos reales de tu bóveda. Conservá un índice previo propio; la [guía de mantenimiento](indice-principal.md) explica la integración y la alternativa con herramientas de archivos.
