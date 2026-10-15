> [!info]- Índice de esta nota (líneas)
> - Líneas 1–7: Este índice
> - Líneas 9–12: Mantener notas, mapas y registro
> - Líneas 13–20: Al crear o editar notas
> - Líneas 21–35: Índices de líneas con Python
> - Líneas 36–65: Registro identificado y períodos de cinco días
> - Líneas 66–70: Sin Python o con archivos adjuntos

# Mantener notas, mapas y registro

La IA realiza este mantenimiento dentro del pedido autorizado; la persona no prepara JSON, ejecuta comandos ni cuenta líneas. El orden de lectura está en [las reglas](../00_CORE/atoms/00_vault-rules.md).

## Al crear o editar notas

1. Identificarse con nombre de IA, herramienta y modelo conocido; declarar lo desconocido. Al crear un nodo, dejar «Creado por» en su índice.
2. Releer y editar los destinos acordados, conservando cambios ajenos. Recalcular el índice de cada nota editable: sección y líneas inicial/final del archivo completo, incluidas propiedades e índice. La atribución del README conserva la primera línea.
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

```sh
python 00_CORE/schemas/registrar_cambios.py --destino "ruta-de-la-boveda" --datos "evento-temporal.json" --dry-run
python 00_CORE/schemas/registrar_cambios.py --destino "ruta-de-la-boveda" --datos "evento-temporal.json"
```

El script escribe solo registros e históricos. Archiva antes de renovar, conserva registros incompatibles y bloquea escrituras concurrentes. Si aparece `.registro-cambios.lock`, releer y resolver la operación, sin quitarlo por iniciativa propia. Tras un fallo, puede existir el histórico y seguir vigente el activo anterior; reintentar conserva ambas copias. Un id ya registrado devuelve `ya-registrado` aunque la nota haya cambiado después; datos distintos con ese id se rechazan.

## Sin Python o con archivos adjuntos

La IA cuenta líneas del archivo final, excluye títulos dentro de código como secciones y comprueba los rangos tras cada edición. Si no puede, los declara pendientes.

Mantiene los mismos mapas y registro: autor, fecha con zona, operación, rutas y resultado comprobado. Antes de renovar, comprueba `inicio` y guarda una copia íntegra en una ruta libre; relee el resultado y sus rangos. Con adjuntos, entrega la copia actualizada y aclara que los originales no están sincronizados.
