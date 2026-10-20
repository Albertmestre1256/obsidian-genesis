> [!info]- Índice de esta nota (líneas)
> - Líneas 1–9: Este índice
> - Líneas 11–14: Plantillas y panel
> - Líneas 15–18: Abrir la bóveda preparada
> - Líneas 19–26: Vista simple de una bóveda nueva
> - Líneas 27–32: Ajustes de Plantillas
> - Líneas 33–38: Qué muestra el Panel
> - Líneas 39–50: Ver las conexiones
> - Líneas 51–70: Retirar material del kit que ya no usás

# Plantillas y panel

Una bóveda nueva del kit incluye ajustes para **Plantillas**, **Bases**, **Búsqueda** y **Vista de gráfico**, todos integrados en Obsidian. La visualización se comprueba por separado en tu instalación.

## Abrir la bóveda preparada

En Obsidian, elegí abrir una carpeta como bóveda y seleccioná la que te entregó la IA. Abrí `Panel.md` para encontrar tu proyecto. Si la tabla no aparece, podés abrir su ficha directamente en `00_CORE/cells/` mientras resolvés el problema.

## Vista simple de una bóveda nueva

La carpeta nueva preparada incluye el fragmento `.obsidian/snippets/genesis-vista-simple.css` activado desde `.obsidian/appearance.json` y el filtro inicial de `.obsidian/graph.json`. La IA conserva esos ajustes al entregar la copia, incluidos los archivos ocultos; el principiante no tiene que copiar CSS, activar interruptores ni pegar filtros.

El explorador prioriza `Panel.md`, `INDICE.md`, `Proyectos.base` y los proyectos: oculta las carpetas de soporte `00_CORE`, `DOCS`, `tests`, `PROJECT_TEMPLATE`, los README y las entradas técnicas del kit. El gráfico filtra documentación y plantillas, pero mantiene las fichas en `00_CORE/cells/` y las notas de trabajo. Los archivos y enlaces siguen existiendo y las IA pueden leerlos; es presentación, no privacidad ni control de acceso.

Si querés volver a ver el soporte, pedíselo a la IA: puede desactivar solo `genesis-vista-simple` en `enabledCssSnippets` y retirar el filtro de `search`, conservando los demás ajustes. La alternativa manual está en Ajustes → Apariencia → Fragmentos CSS y en los filtros del gráfico. Preparar estos archivos no acredita una comprobación visual en la app. Si Obsidian ya estaba abierto, puede mantener ajustes en memoria; no cerrar procesos por fuerza. Ocultar no elimina: para sacar de la bóveda el material que no usás, ver [Retirar material del kit](#retirar-material-del-kit-que-ya-no-usás).

## Ajustes de Plantillas

La bóveda nueva ya trae Plantillas, Bases, Búsqueda y la vista simple configuradas; activarlas en una bóveda existente queda fuera del alcance del kit.

En los ajustes de Plantillas, indicá `00_CORE/templates` como carpeta de plantillas y `YYYY-MM-DD` como formato de fecha. Allí están las plantillas; las fichas creadas se guardan en `00_CORE/cells/`, para que no aparezcan como opciones para insertar. Si creás la ficha con una IA, ella completa los archivos; la [guía manual](primer-proyecto.md) explica cómo insertarla por tu cuenta.

## Qué muestra el Panel

La tabla de `Proyectos.base` reúne fichas propias. La búsqueda muestra tareas pendientes; para completarlas, abrí la nota original. El ejemplo lleva la propiedad `ejemplo: true` y se consulta desde un enlace de ayuda, separado de las vistas de trabajo. La tabla usa Bases, que requiere Obsidian 1.9.10 o posterior.

Fuentes: [Plantillas](https://obsidian.md/help/plugins/templates), [Bases](https://obsidian.md/help/bases/syntax), [Búsqueda](https://obsidian.md/help/plugins/search) y [Obsidian 1.9.10](https://obsidian.md/changelog/2025-08-18-desktop-v1.9.10/).

## Ver las conexiones

Abrí **Vista de gráfico** desde el icono lateral de Obsidian. Los puntos son notas y las líneas corresponden a sus enlaces internos; una carpeta o etiqueta sola no crea esa conexión. El kit muestra notas existentes, sin destinos pendientes ni adjuntos, y mantiene visibles las notas aisladas para poder revisarlas.

Para trabajar sin cargar visualmente toda la bóveda, abrí el índice de un nodo y usá **Abrir gráfico local**; ajustá la profundidad según quieras ver sus notas o también nodos vecinos. Las relaciones temáticas se añaden al contenido, y la IA mantiene los enlaces jerárquicos al agregar notas.

La red conserva una entrada **Leer primero**, [[INDICE|Índice general]], índices de nodos y notas. La vista simple oculta el soporte del gráfico, no elimina esos enlaces. Un nodo nuevo se conecta al mapa y al padre; un nodo general conecta además con la entrada que use la bóveda. No hace falta instalar un plugin comunitario.

Fuentes: [Vista de gráfico](https://obsidian.md/help/plugins/graph) y [Enlaces internos](https://obsidian.md/help/links). Comprobar los archivos y enlaces no equivale a haber abierto la vista en Obsidian.

Referencia de los fragmentos de estilo: [CSS snippets](https://obsidian.md/help/snippets).

## Retirar material del kit que ya no usás

**Paso obligatorio al terminar de configurar la bóveda.** La IA revisa el material sobrante y muestra la lista exacta antes de cerrar la entrega; la persona no tiene que descubrir ni recordar este pedido. Para autorizar el retiro de esa lista, debe responder explícitamente: **«Retirá de esta bóveda el material del kit que ya no necesito»**. La frase autoriza únicamente los archivos presentados, con las exclusiones que indique la persona; no autoriza un borrado general. La vista simple solo oculta el soporte. La IA identifica, respalda, verifica, retira y mantiene; la persona decide sobre la lista y el respaldo, sin ejecutar comandos. Puede conservar todo o postergarlo expresamente; sin respuesta, el retiro queda pendiente y se conserva todo.

1. **Destino.** Solo una bóveda de uso con configuración `lista` y entrega comprobada; con `parcial`, terminá antes la configuración. Nunca la fuente original del kit, un repositorio de desarrollo ni una raíz ambigua: ante `.git`, `.claude/worktrees` u otras señales de desarrollo, conservá todo y explicá el motivo. No sigas enlaces ni junctions ni rutas fuera de la raíz; una ruta que no podés comprobar se conserva y se declara el límite.
2. **Candidatos.** Contrastá ruta y contenido con una copia original identificada del kit, de la misma versión según `CHANGELOG.md`, solo para leer. Es candidato únicamente lo idéntico a esa referencia; lo propio, modificado o sin referencia fiable se conserva y no se promete descartable. Un nombre de carpeta no prueba el origen: comprobá cada archivo. Candidatos habituales en la carpeta descargada:
   - `tests/` y `.github/`: pruebas y metadatos de GitHub.
   - `DOCS/README*.md` y las traducciones `README.en.md`, `README.de.md` y `README.zh.md` de la raíz que la persona no use.
   - `CONTRIBUTING.md`, `DOCS/publicacion.md` y `DOCS/prueba-con-usuarios.md`, si su lectura confirma que sirven para desarrollar o publicar el kit.
   - `instalar.py` y `DOCS/instalacion-manual.md`: material heredado para bóvedas existentes, que una bóveda nueva no usa.

   Estas categorías son ejemplos, nunca una lista autorizada: reemplazalas por las rutas concretas que existan y sean retirables.
3. **Siempre se conserva.** Proyectos y sus carpetas, originales, `00_CORE/configuracion.md` con inventario y omisiones, fichas, registros e historial, índices, `Panel.md`, `Proyectos.base` y `.obsidian/`. También `INDICE.md`, `AGENTS.md`, `CLAUDE.md`, `AI-INSTRUCTIONS.md`, `LEER_PRIMERO.md`, reglas, protocolos, plantillas, `PROJECT_TEMPLATE/`, `.claude/`, `.opencode/`, herramientas y guías de uso (salvo los heredados `instalar.py` y `DOCS/instalacion-manual.md`) de `DOCS/` que estas entradas citan para retomar, ampliar, configurar otra parte o revisar. `LICENSE` y los créditos del kit permanecen: si una traducción se retira, el README que la persona lee conserva la atribución.
4. **Referencias.** Buscá cada ruta y nombre candidato en lo que permanece: notas, guías, plantillas, herramientas y ajustes. Los enlaces del bloque automático de `INDICE.md` e índices generados son catálogo y se refrescan después; un filtro que oculta una ruta tampoco depende de ella. Un enlace manual o de una guía conservada debe seguir válido: conservá el candidato o incluí en la propuesta la adaptación concreta (archivo, texto actual y nuevo). Ninguna reescritura global.
5. **Decisión obligatoria de cierre.** Mostrá una tabla con cada archivo por su ruta exacta, nunca una carpeta entera, con qué contiene, por qué ya no hace falta, dependencias o adaptación, respaldo y restauración, y el destino del respaldo **fuera de la bóveda**: otra carpeta con acceso o un ZIP descargable. Separá «Se eliminará si lo autorizás» de «Se conserva»; la segunda lista identifica las reglas, entradas, herramientas y datos necesarios. Un respaldo dentro vuelve a cargar gráfico y catálogo. Pedí la frase explícita del comienzo para aceptar la lista, o que indique exclusiones, conservación o postergación. Registrá su decisión y las rutas en el avance de configuración. Sin respuesta, registrá «retiro pendiente de decisión»; la integración puede seguir `lista`, pero no presentes el retiro ni el cierre de entrega como resueltos. Una decisión ya registrada no se vuelve a preguntar mientras la lista siga vigente. Aprobar una carpeta por su nombre abarca solo los archivos listados, no los que aparezcan después. Sin candidatos seguros, informá «Nada se eliminará», registrá el motivo y cerrá este paso conservando todo, sin pedir una orden vacía ni anunciar ahorro.
6. **Respaldo.** Copiá cada archivo aprobado conservando su ruta relativa, con una nota de restauración: versión del kit, fecha, rutas, autoría y una copia de `LICENSE`. Contrastá cada archivo copiado con el de la bóveda. Sin destino, sin acceso o ante una diferencia, no se retira nada.
7. **Retiro.** Borrá archivo por archivo, sin borrado recursivo. Justo antes de cada uno, comprobá que sigue en la ruta aprobada, sin enlace ni junction, y con contenido idéntico al respaldado; si cambió, falta o no podés comprobarlo, conservalo junto con sus adaptaciones dependientes e informalo. Aplicá cada adaptación aprobada solo si el texto actual sigue igual. Lo aparecido o cambiado después se conserva; una carpeta se retira solo si quedó vacía. Comprobá que los archivos retirados faltan y el resto sigue presente.
8. **Mantenimiento.** Seguí [Mantener notas, mapas y registro](mantenimiento.md#secuencia-de-cierre-compartida): rangos de notas editadas, mapas refrescados y registro con `borrar` por cada archivo retirado y el respaldo en el resumen. Verificá los enlaces de lo que permanece. Comprobá la reanudación leyendo `INDICE.md`, `AI-INSTRUCTIONS.md`, reglas, configuración y ficha del proyecto. Informá rutas retiradas, respaldo, cómo restaurar y lo no comprobado, como la vista en Obsidian.

Para restaurar, copiá desde el respaldo a las mismas rutas sin sobrescribir archivos cambiados después; refrescá mapas y registrá la operación.
