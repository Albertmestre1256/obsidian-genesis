# Trabajar con una IA

Si todavía no configuraste la bóveda, empezá por el [README principal](../README.md). Esta guía sirve para el trabajo diario con cualquier asistente que pueda leer los archivos que le entregues.

Con acceso a tu carpeta, la IA puede leer y guardar dentro del alcance acordado. Con adjuntos, trabajará sobre copias: vos actualizás la nota original con los cambios aprobados y entregás esa versión en la siguiente sesión. Adjuntar una nota no la mantiene sincronizada.

## Qué información darle

Entregá primero `INDICE.md`, el mapa completo de la bóveda. Después, las reglas de `00_CORE/atoms/00_vault-rules.md` y la ficha vigente del proyecto en `00_CORE/cells/`. Agregá solo el material que la tarea necesite. Si el asistente tiene acceso a la bóveda, puede buscarlo; si usás adjuntos, agregás esos archivos al chat. No necesitás subir todos los proyectos.

## Pedidos listos para usar

Reemplazá lo que está entre corchetes. El asistente debe leer primero el índice principal y después las reglas, trabajar con el proyecto indicado y distinguir datos, propuestas y pendientes.

### Retomar

> Seguí con [proyecto]. Leé primero el índice principal, después las reglas y su ficha vigente. Resumí dónde quedamos y proponé un próximo paso; preguntame solo lo que falte para hacerlo.

Si querés practicar, podés elegir explícitamente la ficha `ejemplo-context.md`: sus datos son ficticios.

### Crear otro proyecto

Con adjuntos, agregá también `TEMPLATE_cell.md`, el índice de `PROJECT_TEMPLATE/` y `00_CORE/protocols/configurar-vault.md`.

> Quiero crear el proyecto [nombre]. Leé primero el índice principal, después las reglas y seguí la sección «Crear el proyecto» del protocolo de configuración. Preguntá solo lo que falte sobre propósito, objetivo y próximo paso. Mostrá el destino y los archivos antes de crearlos. Conservá lo existente; si no podés leer o escribir mi bóveda, aclará qué queda pendiente y entregá los contenidos con sus destinos.

Con acceso a archivos, la IA comprueba las coincidencias por identificador y crea ficha, índice y carpetas, además del acceso en el Panel. En un chat de texto, podés guardar los contenidos siguiendo la [guía manual](primer-proyecto.md).

### Redactar

Para un mensaje breve bastan el índice principal, el pedido, las reglas y la ficha. Para un texto elaborado, agregá las guías indicadas en `00_CORE/protocols/context-injection.md` si la IA no puede leerlas por su cuenta.

> Necesito [texto] para [destinatario], en [proyecto], con el objetivo de [resultado]. Usá los datos disponibles y señalá lo que falte. Para un texto breve, redactá en el chat; si necesita estructura, proponé un plan corto antes del borrador. No envíes ni publiques el texto. Si te pido guardarlo, usá la carpeta de borradores del proyecto y conservá versiones anteriores.

### Revisar fichas

Con adjuntos, agregá `00_CORE/schemas/validate.py`: contiene las reglas de revisión.

> Revisá estas fichas con el validador del kit. Si podés ejecutarlo, informá el resultado; si no, hacé la revisión manual y aclaralo. Explicá los errores y avisos y proponé correcciones. Un formato válido no demuestra que los datos sean verdaderos. No modifiques las fichas todavía.

### Guardar el cierre

> Cerramos la sesión de [proyecto]. Compará lo trabajado con la ficha más reciente y proponé solo los cambios nuevos: hechos con fuente, decisiones, tareas y preguntas. No conviertas sugerencias en decisiones. Después de mi aprobación, guardá y verificá lo acordado si tenés acceso; si no, entregá la ficha actualizada y su destino.

Al retomar, usá siempre la ficha vigente. La configuración del espacio o cuenta del asistente es opcional: estos pedidos también sirven en un chat común.

Cuando la IA guarda cambios, también mantiene el [índice principal](indice-principal.md). Con adjuntos, pedile esa copia actualizada además de las notas modificadas; si no pudo verificar la bóveda real, debe aclararlo.
