> [!info]- Índice de esta nota (líneas)
> - Líneas 1–8: Este índice
> - Líneas 10–13: Plantillas y panel
> - Líneas 14–17: Abrir la bóveda preparada
> - Líneas 18–25: Vista simple de una bóveda nueva
> - Líneas 26–35: En una bóveda existente
> - Líneas 36–41: Qué muestra el Panel
> - Líneas 42–52: Ver las conexiones

# Plantillas y panel

Una bóveda nueva del kit incluye ajustes para **Plantillas**, **Bases**, **Búsqueda** y **Vista de gráfico**, todos integrados en Obsidian. La visualización se comprueba por separado en tu instalación.

## Abrir la bóveda preparada

En Obsidian, elegí abrir una carpeta como bóveda y seleccioná la que te entregó la IA. Abrí `Panel.md` para encontrar tu proyecto. Si la tabla no aparece, podés abrir su ficha directamente en `00_CORE/cells/` mientras resolvés el problema.

## Vista simple de una bóveda nueva

La carpeta nueva preparada incluye el fragmento `.obsidian/snippets/genesis-vista-simple.css` activado desde `.obsidian/appearance.json` y el filtro inicial de `.obsidian/graph.json`. La IA conserva esos ajustes al entregar la copia, incluidos los archivos ocultos; el principiante no tiene que copiar CSS, activar interruptores ni pegar filtros.

El explorador prioriza `Panel.md`, `INDICE.md`, `Proyectos.base` y los proyectos: oculta las carpetas de soporte `00_CORE`, `DOCS`, `tests`, `PROJECT_TEMPLATE`, los README y las entradas técnicas del kit. El gráfico filtra documentación y plantillas, pero mantiene las fichas en `00_CORE/cells/` y las notas de trabajo. Los archivos y enlaces siguen existiendo y las IA pueden leerlos; es presentación, no privacidad ni control de acceso.

Si querés volver a ver el soporte, pedíselo a la IA: puede desactivar solo `genesis-vista-simple` en `enabledCssSnippets` y retirar el filtro de `search`, conservando los demás ajustes. La alternativa manual está en Ajustes → Apariencia → Fragmentos CSS y en los filtros del gráfico. Preparar estos archivos no acredita una comprobación visual en la app. Si Obsidian ya estaba abierto, puede mantener ajustes en memoria; no cerrar procesos por fuerza.

## En una bóveda existente

El instalador conserva `.obsidian/`. Para usar estas funciones, activá Plantillas, Bases y Búsqueda en Ajustes → Plugins principales. Bases requiere Obsidian 1.9.10 o posterior.

Si querés el gráfico en una bóveda existente, activá también **Vista de gráfico**. La IA conserva tus ajustes; no reemplaza `.obsidian/` por los del kit.

La vista simple anterior es el valor inicial de una carpeta nueva. El instalador actual no copia esos ajustes a una bóveda existente; no sustituyas su `appearance.json` o `graph.json` por los del kit. La integración automática conservando sus preferencias se prepara por separado.

En los ajustes de Plantillas, indicá `00_CORE/templates` como carpeta de plantillas y `YYYY-MM-DD` como formato de fecha. Allí están las plantillas; las fichas creadas se guardan en `00_CORE/cells/`, para que no aparezcan como opciones para insertar. Si creás la ficha con una IA, ella completa los archivos; la [guía manual](primer-proyecto.md) explica cómo insertarla por tu cuenta.

## Qué muestra el Panel

La tabla de `Proyectos.base` reúne fichas propias. La búsqueda muestra tareas pendientes; para completarlas, abrí la nota original. El ejemplo lleva la propiedad `ejemplo: true` y se consulta desde un enlace de ayuda, separado de las vistas de trabajo.

Fuentes: [Plantillas](https://obsidian.md/help/plugins/templates), [Bases](https://obsidian.md/help/bases/syntax), [Búsqueda](https://obsidian.md/help/plugins/search) y [Obsidian 1.9.10](https://obsidian.md/changelog/2025-08-18-desktop-v1.9.10/).

## Ver las conexiones

Abrí **Vista de gráfico** desde el icono lateral de Obsidian. Los puntos son notas y las líneas corresponden a sus enlaces internos; una carpeta o etiqueta sola no crea esa conexión. El kit muestra notas existentes, sin destinos pendientes ni adjuntos, y mantiene visibles las notas aisladas para poder revisarlas.

Para trabajar sin cargar visualmente toda la bóveda, abrí el índice de un nodo y usá **Abrir gráfico local**; ajustá la profundidad según quieras ver sus notas o también nodos vecinos. Las relaciones temáticas se añaden al contenido, y la IA mantiene los enlaces jerárquicos al agregar notas.

La red conserva una entrada **Leer primero**, [[INDICE|Índice general]], índices de nodos y notas. La vista simple oculta el soporte del gráfico, no elimina esos enlaces. Un nodo nuevo se conecta al mapa y al padre; un nodo general conecta además con la entrada que use la bóveda. No hace falta instalar un plugin comunitario.

Fuentes: [Vista de gráfico](https://obsidian.md/help/plugins/graph) y [Enlaces internos](https://obsidian.md/help/links). Comprobar los archivos y enlaces no equivale a haber abierto la vista en Obsidian.

Referencia de los fragmentos de estilo: [CSS snippets](https://obsidian.md/help/snippets).
