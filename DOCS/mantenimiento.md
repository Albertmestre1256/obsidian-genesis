> [!info]- Índice de esta nota (líneas)
> - Líneas 1–10: Este índice
> - Líneas 12–15: Mantener notas, mapas y registro
> - Líneas 16–23: Al crear o editar notas
> - Líneas 24–40: Índices de líneas con Python
> - Líneas 41–78: Registro identificado y períodos de cinco días
> - Líneas 79–80: Cierre de la operación
> - Líneas 81–95: Secuencia de cierre compartida
> - Líneas 96–101: Sin Python o con archivos adjuntos
> - Líneas 102–111: Entregar una copia como ZIP

# Mantener notas, mapas y registro

La IA realiza este mantenimiento dentro del pedido autorizado; la persona no prepara JSON, ejecuta comandos ni cuenta líneas. El orden de lectura está en [las reglas](../00_CORE/atoms/00_vault-rules.md).

## Al crear o editar notas

1. Identificarse con nombre de IA, herramienta y modelo conocido; declarar lo desconocido. Al crear un nodo, dejar «Creado por» en su índice.
2. Releer y editar los destinos acordados, conservando cambios ajenos. Recalcular el índice de las notas editables creadas o modificadas por esta operación: sección y líneas inicial/final del archivo completo, incluidas propiedades e índice. No recorrer toda la bóveda por rutina. La atribución del README conserva la primera línea.
3. Actualizar resúmenes y enlaces de los [mapas del nodo y general](indice-principal.md). Para originales existentes, describir contenido y líneas en el índice del nodo; no reescribirlos. Las fuentes Markdown nuevas elaboradas por la IA llevan su índice antes de guardarse. Históricos e integraciones de herramientas conservan su formato.
4. Elegir el ID de esta operación real. Si se edita la configuración y tiene «Última operación de mantenimiento», actualizar esa etiqueta con el ID exacto **antes** de recalcular rangos y registrar: forma parte de la huella del archivo. Verificar archivos, rangos y enlaces. Si cambió una ficha, aplicar [Revisar fichas](usar-con-otras-ias.md#revisar-fichas) antes de declarar el trabajo verificado; corregir errores o guardar el resultado como pendiente. Registrar cambios reales, incluidos `INDICE.md` y cada índice local que cambió, origen y destino de movimientos y resultados parciales. Cada evento enumera los archivos de esa operación: una fila anterior no registra su nueva edición. No guardar credenciales ni afirmar comprobaciones que no ocurrieron.
5. Refrescar el mapa tras crear registros o históricos. Los hashes describen el momento del registro; las regeneraciones auxiliares forman parte de la misma operación.

## Índices de líneas con Python

Usar la herramienta del kit leído:

```sh
python 00_CORE/schemas/note_index.py apply "ruta/Nota.md"
python 00_CORE/schemas/note_index.py check "ruta/Nota.md"
```

`--vault "ruta-de-la-boveda"` procesa notas editables en lote; requiere ese alcance acordado. Excluye `01_FUENTES/`, `_archivo/`, `00_CORE/logs/historial/` e integraciones; rechaza enlaces/junctions en el material a procesar. `check` no escribe: 0 vigente, 1 pendiente, 2 impedido. `apply` valida antes de escribir; ante un fallo, releer las salidas e informar lo parcial. Los títulos dan las descripciones; el script no resume cuerpos ni verifica hechos.

Preferí pasar las rutas concretas de las notas afectadas. El cierre no autoriza por sí solo `apply --vault`: que un archivo tenga extensión `.md` no autoriza modificarlo. Las transcripciones exportadas conservan su contenido y formato; no les agregues índices ni corrijas su texto. Para evidencia técnica, usá un destino acordado fuera de la bóveda de trabajo cuando haya acceso; si se incorporan como material del proyecto, guardalas como originales en `01_FUENTES/` y describilas desde el índice del nodo. No muevas una exportación existente sin autorización. Si la comprobación global señala rangos pendientes en un original fuera de esas carpetas, informá la ruta y el impedimento; no lo reescribas para hacer pasar el cierre.

El actualizador de mapas refresca los rangos de índices que ya los tienen. El creador genera ficha e índice con rangos y los recalcula después de llenar las plantillas. No conservar números de una plantilla al copiarla o ampliar el bloque de un nodo.

El índice usa `> [!info]- Índice de esta nota (líneas)`: está plegado al leer en Obsidian y se abre al pulsar su título. Los rangos siguen presentes en el archivo para la IA. La herramienta admite el encabezado anterior y lo convierte al mantener una nota autorizada, sin tocar originales, históricos ni integraciones. Sin Python, usar el mismo encabezado y comprobar los rangos como siempre.

## Registro identificado y períodos de cinco días

`00_CORE/logs/registro-cambios.md` nace en la bóveda configurada cuando hay cambios que registrar. No se distribuye con actividad personal. Su propiedad `inicio`, con zona horaria, inicia un período de cinco días; editar el archivo no reinicia el plazo.

En el primer guardado tras cinco días, conservar el registro íntegro en `00_CORE/logs/historial/` y comenzar uno nuevo. El historial no se purga ni se reindexa; sin modificaciones no hace falta rotar ni programar tareas. La herramienta toma la hora real con la zona local del equipo. Si difiere de la del usuario, obtener la misma hora del reloj en su zona y pasar `--fecha` con ese valor explícito; no estimarla. La CLI rechaza fechas futuras. Prevalece la política de una bóveda existente.

La IA prepara un evento JSON fuera del kit distribuible. Ejemplo ficticio:

```json
{
  "id": "sesion-estudio-001",
  "ia": "ChatGPT",
  "herramienta": "herramientas de archivos",
  "resumen": "Añadida una síntesis de la primera unidad.",
  "verificado": true,
  "cambios": [{"accion": "crear", "ruta": "Estudio/Unidad-1.md"}]
}
```

Usar un id estable por operación; `modelo` es opcional. Acciones: `crear`, `editar`, `mover`, `renombrar`, `archivar`, `borrar`. Registrar no autoriza ejecutarlas. Los movimientos requieren `desde`; un archivo declarado borrado debe estar ausente. El script comprueba rutas y hashes de resultados presentes. Con `verificado: true`, también rechaza errores de formato de las fichas modificadas en `00_CORE/cells/`; admite avisos y conserva plantillas e históricos. Con `false`, permite registrar trabajo incompleto. Ese campo declara la revisión de la IA, no prueba la verdad del contenido ni valida todos los archivos del vault.

El cierre compartido contrasta el ID registrado con la etiqueta de la configuración cuando contiene un valor. Reconoce la etiqueta con o sin tildes, énfasis o lista numerada. Admite el ID solo, entre backticks o seguido de `(AAAA-MM-DD)`. Una etiqueta anterior, varias etiquetas o texto ambiguo requieren revisión manual; el chequeo no los corrige. Las configuraciones anteriores sin etiqueta, con valor vacío, «-» o «—» siguen siendo compatibles. Si se modifica la configuración después de registrarla, hace falta una nueva operación real con su nueva huella; no basta cambiar la etiqueta para hacer pasar el cierre.

En configuraciones con `## Proyecto inicial`, el cierre también comprueba la coherencia del proyecto declarado:

- Con `estado: lista`, el Identificador debe corresponder a una ficha propia incluida en la revisión diaria y a un único índice de ese proyecto, reconocidos por sus propiedades. No puede compartir identidad con una ficha de ejemplo. Se conservan los nombres propios de archivos; una ficha en subcarpetas o llamada `TEMPLATE_cell.md` queda pendiente porque el revisor diario no la incluye.
- Si «Ficha e índice» contiene referencias, deben enlazar ambos archivos. Admite wikilinks con rutas desde la raíz o nombres cortos únicos, alias y fragmentos, y enlaces Markdown relativos a la configuración. Rechaza destinos ausentes, ambiguos, ajenos o externos reconocidos, incluidas URL con esquema y autolinks. Un enlace escrito como código inline no cuenta como referencia.
- Con `estado: parcial`, el proyecto acordado puede esperar su creación y conservar marcadores o referencias vacías. Las referencias concretas siguen requiriendo comprobación. No hace falta aportar CV, plazo, tareas ni cerrar el inventario opcional.

Se conserva compatibilidad con el formato anterior sin esa sección y con «Ficha e índice» ausente, vacía, «-» o «—»; en este último caso se comprueba la identidad por propiedades. Los campos o secciones canónicos repetidos requieren revisión manual. El chequeo interpreta los formatos anunciados, no cualquier presentación de Markdown ni la verdad de las notas. Ante un impedimento, releer lo guardado y explicar el pendiente; no mover ni recrear una ficha para eludirlo.

```sh
python 00_CORE/schemas/registrar_cambios.py --destino "ruta-de-la-boveda" --datos "evento-temporal.json" --dry-run
python 00_CORE/schemas/registrar_cambios.py --destino "ruta-de-la-boveda" --datos "evento-temporal.json"
```

El script escribe solo registros e históricos. Archiva antes de renovar, conserva registros incompatibles y bloquea escrituras concurrentes. Si aparece `.registro-cambios.lock`, releer y resolver la operación, sin quitarlo mientras otra pueda estar activa; si quedó de una operación interrumpida, seguir «Aparece un bloqueo» en [Solución de problemas](TROUBLESHOOTING.md). Tras un fallo, puede existir el histórico y seguir vigente el activo anterior; reintentar conserva ambas copias. Un id ya registrado devuelve `ya-registrado` aunque la nota haya cambiado después; datos distintos con ese id se rechazan.

## Cierre de la operación

### Secuencia de cierre compartida

Para cerrar una sesión de trabajo (referencia: `DOCS/mantenimiento.md`):

Indicá la raíz de la bóveda en los comandos y contrastala con «Bóveda revisada» antes de informar el resultado. Sin ese argumento, el validador usa la bóveda donde está el script, aunque la carpeta actual sea otra. Si moviste o extrajiste el ZIP en otro lugar, usá su ruta actual; no recrees las notas para corregir una ruta.

1. **Chequeo parcial**: para registrar avances actuales, elegí su ID y actualizá «Última operación de mantenimiento» si esa etiqueta existe en la configuración. Recalculá rangos y mapas, registrá los cambios y refrescá el mapa. Después ejecutá `python 00_CORE/schemas/validate.py "<raíz-de-la-bóveda>" --cierre --operacion <ID-parcial>`. Si esa operación ya estaba registrada, verificá su estado sin editarla. Este chequeo no escribe.
2. **Estado final `lista`**: si la bóveda pasa a `estado: lista`, actualizá `00_CORE/configuracion.md` (cambiar `estado` y `fecha`). Elegí un nuevo ID para esa operación final y actualizá la etiqueta existente antes de calcular su huella.
3. **Mantenimiento de rangos y mapas**: corré `python 00_CORE/schemas/note_index.py apply "<nota-editada>"` con las rutas de las notas editables de esta operación, y `python actualizar_indice.py <raíz>` para refrescar los mapas. Usá `--vault <raíz>` solo si se acordó expresamente un mantenimiento en lote; no para resolver por fuerza un impedimento ajeno a la tarea.
4. **Registrar edición final**: registrá ese cambio de configuración como **nueva operación real** (ID elegido en el paso 2, `verificado: true`, fecha actual con zona). No reutilicés el ID del chequeo parcial ni edites la configuración después de registrar su huella.
5. **Refrescar y volver a chequear**: corré `actualizar_indice.py` otra vez (el registro ya existe) y luego `validate.py "<raíz-de-la-bóveda>" --cierre --operacion <ID-final>` con el nuevo ID. El chequeo anterior no sirve para la edición final.

La IA gestiona los IDs y pasos técnicos; la persona no los proporciona. Índices manuales o logs incompatibles generan error explícito de «revisión manual pendiente», sin reescritura ni aprobación automática.


## Sin Python o con archivos adjuntos

La IA cuenta líneas del archivo final, excluye títulos dentro de código como secciones y comprueba los rangos tras cada edición. Si no puede, los declara pendientes.

Mantiene los mismos mapas y registro: autor, fecha con zona, operación, rutas y resultado comprobado. Antes de renovar, comprueba `inicio` y guarda una copia íntegra en una ruta libre; relee el resultado y sus rangos. Con adjuntos, entrega la copia actualizada según [Entregar una copia como ZIP](#entregar-una-copia-como-zip) y aclara que los originales no están sincronizados.

## Entregar una copia como ZIP

Cuando la IA no puede escribir en la carpeta de la persona y entrega una copia para descargar, descomprime el kit recibido con `zipfile` de Python, no con `unzip`: otras herramientas pueden cambiar nombres con tildes, como `PROJECT_TEMPLATE/00 - Índice y Contexto.md`. Con Python, crea el proyecto con el [creador](creacion-para-asistentes.md). Después completa estos pasos antes de ofrecer el enlace:

1. **Próximo paso:** si todavía no se habló, preguntá cuál es el primer paso concreto. Si la persona no lo sabe, queda pendiente; no lo inventes.
2. **Cierre completo:** seguí la [secuencia de cierre](#secuencia-de-cierre-compartida) sobre la copia de trabajo. La configuración queda `lista` solo si la operación final termina en «CIERRE VERIFICADO»; con errores, corregilos o dejá `parcial` y decí qué falta.
3. **ZIP con nombres UTF-8:** armá el ZIP con una herramienta que marque los nombres como UTF-8, por ejemplo `zipfile` de Python, e incluí los archivos ocultos del kit. Sin esa marca, Windows muestra nombres como «├ìndice» o «fotografÃ­a» y los enlaces se rompen.
4. **Comprobar lo que se entrega:** descomprimí ese mismo ZIP en una carpeta nueva y compará su lista de archivos con la del kit recibido: ningún archivo del kit puede faltar ni cambiar de nombre; solo se agregan los creados. Después volvé a correr el cierre con el ID final sobre esa carpeta.

Informá qué se comprobó y qué no, por ejemplo la vista en Obsidian. Sin Python, aplicá las alternativas manuales y declará que el cierre automático no se ejecutó. Si no podés completar algún paso, decilo antes de entregar.
