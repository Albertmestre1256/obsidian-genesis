> [!info]- Índice de esta nota (líneas)
> - Líneas 1–7: Este índice
> - Líneas 9–12: Plantillas y panel
> - Líneas 13–16: Abrir la bóveda preparada
> - Líneas 17–24: En una bóveda existente
> - Líneas 25–30: Qué muestra el Panel
> - Líneas 31–39: Ver las conexiones

# Plantillas y panel

Una bóveda nueva del kit incluye ajustes para **Plantillas**, **Bases**, **Búsqueda** y **Vista de gráfico**, todos integrados en Obsidian. La visualización se comprueba por separado en tu instalación.

## Abrir la bóveda preparada

En Obsidian, elegí abrir una carpeta como bóveda y seleccioná la que te entregó la IA. Abrí `Panel.md` para encontrar tu proyecto. Si la tabla no aparece, podés abrir su ficha directamente en `00_CORE/cells/` mientras resolvés el problema.

## En una bóveda existente

El instalador conserva `.obsidian/`. Para usar estas funciones, activá Plantillas, Bases y Búsqueda en Ajustes → Plugins principales. Bases requiere Obsidian 1.9.10 o posterior.

Si querés el gráfico en una bóveda existente, activá también **Vista de gráfico**. La IA conserva tus ajustes; no reemplaza `.obsidian/` por los del kit.

En los ajustes de Plantillas, indicá `00_CORE/templates` como carpeta de plantillas y `YYYY-MM-DD` como formato de fecha. Allí están las plantillas; las fichas creadas se guardan en `00_CORE/cells/`, para que no aparezcan como opciones para insertar. Si creás la ficha con una IA, ella completa los archivos; la [guía manual](primer-proyecto.md) explica cómo insertarla por tu cuenta.

## Qué muestra el Panel

La tabla de `Proyectos.base` reúne fichas propias. La búsqueda muestra tareas pendientes; para completarlas, abrí la nota original. El ejemplo lleva la propiedad `ejemplo: true` y se consulta desde un enlace de ayuda, separado de las vistas de trabajo.

Fuentes: [Plantillas](https://obsidian.md/help/plugins/templates), [Bases](https://obsidian.md/help/bases/syntax), [Búsqueda](https://obsidian.md/help/plugins/search) y [Obsidian 1.9.10](https://obsidian.md/changelog/2025-08-18-desktop-v1.9.10/).

## Ver las conexiones

Abrí **Vista de gráfico** desde el icono lateral de Obsidian. Los puntos son notas y las líneas corresponden a sus enlaces internos; una carpeta o etiqueta sola no crea esa conexión. El kit muestra notas existentes, sin destinos pendientes ni adjuntos, y mantiene visibles las notas aisladas para poder revisarlas.

Para trabajar sin cargar visualmente toda la bóveda, abrí el índice de un nodo y usá **Abrir gráfico local**; ajustá la profundidad según quieras ver sus notas o también nodos vecinos. Las relaciones temáticas se añaden al contenido, y la IA mantiene los enlaces jerárquicos al agregar notas.

La red contiene una entrada **Leer primero**, [[INDICE|Índice general]], índices de nodos y notas. Un nodo nuevo se conecta al mapa y al padre; un nodo general conecta además con la entrada que use la bóveda. No hace falta instalar un plugin comunitario.

Fuentes: [Vista de gráfico](https://obsidian.md/help/plugins/graph) y [Enlaces internos](https://obsidian.md/help/links). Comprobar los archivos y enlaces no equivale a haber abierto la vista en Obsidian.
