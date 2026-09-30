# Plantillas y panel de proyectos

Una bóveda nueva abierta desde el kit incluye configuración para los plugins integrados **Plantillas**, **Bases** y **Búsqueda**. No necesita plugins comunitarios. La visualización debe comprobarse en tu instalación de Obsidian.

En una bóveda existente, el instalador conserva tus ajustes. Para usar estas funciones:

1. En Ajustes → Plugins principales, activá Plantillas, Bases y Búsqueda.
2. En los ajustes de Plantillas, elegí `00_CORE/cells` como carpeta de plantillas y `YYYY-MM-DD` como formato de fecha.
3. Creá una nota vacía en esa carpeta y nombrala, por ejemplo, `mi-proyecto-context.md`.
4. Abrí la paleta de comandos, buscá **Plantillas: Insertar plantilla** y elegí `TEMPLATE_cell`. Completá las propiedades y las secciones. `actualizado` se completa con la fecha al insertar la plantilla.
5. Abrí `Panel.md` para ver las fichas y las tareas pendientes.

Al duplicar la plantilla a mano, el texto `{{date:YYYY-MM-DD}}` no se transforma: reemplazalo por la fecha del día. Usá la plantilla solo en una nota vacía para evitar duplicar las propiedades.

La tabla de proyectos utiliza el archivo `Proyectos.base`. Bases trabaja con archivos y propiedades; las casillas de tareas del cuerpo se muestran aparte con una búsqueda integrada. Si la tabla no aparece, activá Bases y comprobá tu versión de Obsidian. Se publicó para todos los usuarios en **1.9.10**.

Fuentes: [Plantillas](https://obsidian.md/help/plugins/templates), [formato de Bases](https://obsidian.md/help/bases/syntax), [búsquedas](https://obsidian.md/help/plugins/search) y [Obsidian 1.9.10](https://obsidian.md/changelog/2025-08-18-desktop-v1.9.10/).
