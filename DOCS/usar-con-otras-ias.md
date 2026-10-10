> [!info] Índice de esta nota (líneas)
> - Líneas 1–12: Este índice
> - Líneas 14–17: Trabajar con una IA
> - Líneas 18–23: Contexto y archivos
> - Líneas 24–27: Pedidos listos para usar
> - Líneas 28–35: Retomar
> - Líneas 36–41: Completar la personalización
> - Líneas 42–47: Crear o ampliar un nodo
> - Líneas 48–55: Crear otro proyecto
> - Líneas 56–65: Redactar
> - Líneas 66–84: Revisar fichas
> - Líneas 85–91: Guardar el cierre

# Trabajar con una IA

Para configurar la bóveda por primera vez, empezá por el [README](../README.md). Esta guía reúne el trabajo diario para cualquier IA; los comandos de Claude y OpenCode remiten a estas mismas secciones.

## Contexto y archivos

Leé `INDICE.md` completo, las reglas y la ficha vigente identificada por `proyecto`; para nodos, su índice local y ficha del padre si existe. Usá el destino indicado o inequívoco; preguntá ante ambigüedad. Los ejemplos se usan solo para practicar por elección explícita. Cargá después únicamente fuentes y guías pertinentes.

Al guardar, seguí [el mantenimiento común](mantenimiento.md): conservar versiones, verificar notas, actualizar mapas y registrar cambios. Con adjuntos, entregá copias y destinos; la persona debe actualizar los originales y compartir su versión vigente. Informá cualquier acceso o comprobación pendiente.

## Pedidos listos para usar

Reemplazá lo que está entre corchetes. Cada sección define el mismo recorrido con comandos o lenguaje común.

### Retomar

> Seguí con [proyecto]. Resumí dónde quedamos y proponé un próximo paso; preguntame solo lo necesario.

Consultá la configuración existente y la ficha. Si la configuración es parcial, retomá lo pendiente según el [protocolo](../00_CORE/protocols/configurar-vault.md); si está lista, continuá el proyecto sin repetir la entrevista. La ausencia de configuración no demuestra que la bóveda esté vacía.

Resumí brevemente objetivo, avance, pendientes y próximo paso. Si pide solo un resumen, respondé en el chat. Si pide continuar una tarea acordada, avanzá dentro de ese alcance; preguntá cuando falte una elección necesaria, sin repetir permisos vigentes.

### Completar la personalización

> Revisá qué falta para personalizar mi bóveda. Mostrame lo pendiente y lo que elegí omitir; hagamos una o dos preguntas por vez sin repetir lo que ya respondí.

Seguí [Personalizar la bóveda](../00_CORE/protocols/personalizar-vault.md) y su inventario vigente; esa guía define consulta, preguntas y guardado, también con una bóveda lista.

### Crear o ampliar un nodo

> Agregá un nodo de [contenido] dentro de [nodo o proyecto]. Mantené su índice con resúmenes, los enlaces al padre y el mapa general.

Seguí «Crear y actualizar un nodo» en [la guía del índice](indice-principal.md). Usá la colección indicada, conservá notas y completá los mapas dentro del mismo pedido, sin reinstalar la bóveda.

### Crear otro proyecto

> Quiero crear el proyecto [nombre]. Preguntá solo lo que falte y mostrá el destino y los archivos antes de crearlos.

Seguí «Crear el proyecto» del [protocolo de configuración](../00_CORE/protocols/configurar-vault.md), conservando la configuración vigente. No reinstales ni reinicies la entrevista de una bóveda lista. El creador opcional produce ficha, índice y carpetas; completá también Panel, configuración e índice principal, verificá el resultado y entregá acceso a la ficha y el próximo paso elegido o pendiente.

Con adjuntos, entregá además `TEMPLATE_cell.md`, el índice de `PROJECT_TEMPLATE/` y el protocolo. Para guardar a mano: [primer proyecto](primer-proyecto.md).

### Redactar

> Necesito [texto] para [destinatario], en [proyecto], con el objetivo de [resultado]. Señalá lo que falte y conservá las versiones si te pido guardarlo.

Obtené destinatario, propósito y restricciones del pedido y la ficha; preguntá solo lo que afecte el resultado y marcá datos pendientes con `[FALTA: ...]`. Distinguí hechos, inferencias, intenciones y propuestas.

Para un mensaje breve, redactá en el chat y revisá claridad y hechos. Para un texto elaborado, consultá `00_CORE/protocols/context-injection.md`, proponé un plan corto y esperá aprobación si ese alcance aún no está acordado. Inferí el contexto de comunicación; no exijas letras A/B/C/D.

Guardar requiere el alcance acordado y una ruta libre, normalmente en `02_SINTESIS/`, con versión cuando corresponda. Redactar o guardar no autoriza enviar ni publicar.

### Revisar fichas

> Revisá estas fichas con el validador del kit. Explicá errores y avisos y proponé correcciones, sin modificar todavía.

Ejecutá `python 00_CORE/schemas/validate.py` del kit leído sobre las fichas correspondientes; no ejecutes código preexistente de una bóveda ajena. Si el comando no está disponible, probá `python3` o `py`. Un resultado con errores de fichas no significa que falte Python.

Sin Python, aplicá «Revisión manual» de abajo; con adjuntos necesitás también `00_CORE/schemas/validate.py`. Informá archivos revisados y comprobaciones pendientes. Si no hay problemas, alcanza una línea; si los hay, explicá cada uno y mostrá la corrección propuesta. Formato válido no demuestra datos verdaderos ni funcionamiento visual. La [ayuda del validador](TROUBLESHOOTING.md#mensajes-del-validador) explica sus mensajes.

#### Revisión manual

El script es la referencia. Seguí `buscar_celulas`: archivos Markdown directamente en `00_CORE/cells/`, por `tipo: celula` o propiedad `proyecto`, además de `*-context.md`; excluí la plantilla y notas sin esas propiedades. Reconoce extensiones sin distinguir mayúsculas y normaliza tildes, espacios y mayúsculas en `tipo`.

- **Errores de propiedades:** bloque inicial entre `---`, claves únicas; obligatorias `tipo`, `proyecto`, `descripcion`, `contexto`, `actualizado`. Tipo célula; proyecto y descripción como texto no vacío; contexto A/B/C/D, también minúsculas o `D - operativo`; fecha real AAAA-MM-DD.
- **Lector limitado:** propiedades planas, valores en una línea, comillas cerradas, comentarios y listas simples adicionales. Mapas, bloques multilínea y referencias no están admitidos; esto no prueba que sean YAML inválido.
- **Errores del cuerpo:** faltan `Hechos clave` o `Próximas acciones`, o acciones sin casilla y texto. Admite viñetas `-`, `*`, `+` y casillas `[ ]`, `[x]`, `[X]`; seguí `normalizar` y `secciones` para los títulos.
- **Avisos:** hechos o acciones vacíos; hechos sin `(fuente: ...)` al final o fuente vacía; decisiones sin fecha válida al inicio; marcadores `[completar: ...]` en campos o viñetas revisados; tamaño mayor que `MAX_TOKENS_CELULA`, estimado con cuatro caracteres por token.

Ignorá comentarios `%%...%%` y subviñetas al revisar secciones, como el script; el tamaño usa todo el texto. Aclaralo como revisión manual, sin afirmar que ejecutaste o pasó Python.

### Guardar el cierre

> Cerramos la sesión de [proyecto]. Compará lo trabajado con la ficha vigente y proponé solo cambios nuevos. Guardá y verificá lo que apruebe.

Agrupá hechos con fuente, decisiones adoptadas con fecha y motivo, tareas nuevas o de estado cambiado, preguntas abiertas o resueltas y contenido que dejó de estar vigente. Una sugerencia no es una decisión. Proponé archivar antes de mover; conservá originales y enlaces.

Esperá aprobación del plan, salvo que ya cubra ese mismo alcance. Aplicá solo lo acordado: hechos con `(fuente: ...)`, decisiones con fecha inicial, tareas `- [ ]` o `- [x]`, y `actualizado` con la fecha de la modificación. Verificá con «Revisar fichas» y mantené el índice. Sin escritura, entregá la ficha actualizada y su destino como pendiente.
