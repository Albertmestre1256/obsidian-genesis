> [!info] Índice de esta nota (líneas)
> - Líneas 1–7: Este índice
> - Líneas 9–12: Mantener notas, mapas y registro
> - Líneas 13–20: Al crear o editar notas
> - Líneas 21–33: Índices de líneas con Python
> - Líneas 34–61: Registro identificado y períodos de cinco días
> - Líneas 62–66: Sin Python o con archivos adjuntos

# Mantener notas, mapas y registro

La IA realiza este mantenimiento dentro del pedido autorizado; la persona no prepara JSON, ejecuta comandos ni cuenta líneas. El orden de lectura está en [las reglas](../00_CORE/atoms/00_vault-rules.md).

## Al crear o editar notas

1. Identificarse con nombre de IA, herramienta y modelo conocido; declarar lo desconocido. Al crear un nodo, dejar «Creado por» en su índice.
2. Releer y editar los destinos acordados, conservando cambios ajenos. Recalcular el índice de cada nota editable: sección y líneas inicial/final del archivo completo, incluidas propiedades e índice. La atribución del README conserva la primera línea.
3. Actualizar resúmenes y enlaces de los [mapas del nodo y general](indice-principal.md). Para originales existentes, describir contenido y líneas en el índice del nodo; no reescribirlos. Las fuentes Markdown nuevas elaboradas por la IA llevan su índice antes de guardarse. Históricos e integraciones de herramientas conservan su formato.
4. Verificar archivos, rangos y enlaces; registrar cambios reales, origen y destino de movimientos y resultados parciales. No guardar credenciales ni afirmar comprobaciones que no ocurrieron.
5. Refrescar el mapa tras crear registros o históricos. Los hashes describen el momento del registro; las regeneraciones auxiliares forman parte de la misma operación.

## Índices de líneas con Python

Usar la herramienta del kit leído:

```sh
python 00_CORE/schemas/note_index.py apply "ruta/Nota.md"
python 00_CORE/schemas/note_index.py check "ruta/Nota.md"
```

`--vault "ruta-de-la-boveda"` procesa notas editables en lote; requiere ese alcance acordado. Excluye `01_FUENTES/`, `_archivo/`, `00_CORE/logs/historial/` e integraciones; rechaza enlaces/junctions en el material a procesar. `check` no escribe: 0 vigente, 1 pendiente, 2 impedido. `apply` valida antes de escribir; ante un fallo, releer las salidas e informar lo parcial. Los títulos dan las descripciones; el script no resume cuerpos ni verifica hechos.

El actualizador de mapas refresca los rangos de índices que ya los tienen. El creador genera ficha e índice con rangos y los recalcula después de llenar las plantillas. No conservar números de una plantilla al copiarla o ampliar el bloque de un nodo.

## Registro identificado y períodos de cinco días

`00_CORE/logs/registro-cambios.md` nace en la bóveda configurada cuando hay cambios que registrar. No se distribuye con actividad personal. Su propiedad `inicio`, con zona horaria, inicia un período de cinco días; editar el archivo no reinicia el plazo.

En el primer guardado tras cinco días, conservar el registro íntegro en `00_CORE/logs/historial/` y comenzar uno nuevo. El historial no se purga ni se reindexa; sin modificaciones no hace falta rotar ni programar tareas. La herramienta usa la zona local del equipo; pasar `--fecha` con zona explícita si difiere de la del usuario. Prevalece la política de una bóveda existente.

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

Usar un id estable por operación; `modelo` es opcional. Acciones: `crear`, `editar`, `mover`, `renombrar`, `archivar`, `borrar`. Registrar no autoriza ejecutarlas. Los movimientos requieren `desde`; un archivo declarado borrado debe estar ausente. El script comprueba rutas y hashes de resultados presentes. `verificado` declara la revisión de la IA; no prueba la verdad del contenido.

```sh
python 00_CORE/schemas/registrar_cambios.py --destino "ruta-de-la-boveda" --datos "evento-temporal.json" --dry-run
python 00_CORE/schemas/registrar_cambios.py --destino "ruta-de-la-boveda" --datos "evento-temporal.json"
```

El script escribe solo registros e históricos. Archiva antes de renovar, conserva registros incompatibles y bloquea escrituras concurrentes. Si aparece `.registro-cambios.lock`, releer y resolver la operación, sin quitarlo por iniciativa propia. Tras un fallo, puede existir el histórico y seguir vigente el activo anterior; reintentar conserva ambas copias. Un id ya registrado devuelve `ya-registrado` aunque la nota haya cambiado después; datos distintos con ese id se rechazan.

## Sin Python o con archivos adjuntos

La IA cuenta líneas del archivo final, excluye títulos dentro de código como secciones y comprueba los rangos tras cada edición. Si no puede, los declara pendientes.

Mantiene los mismos mapas y registro: autor, fecha con zona, operación, rutas y resultado comprobado. Antes de renovar, comprueba `inicio` y guarda una copia íntegra en una ruta libre; relee el resultado y sus rangos. Con adjuntos, entrega la copia actualizada y aclara que los originales no están sincronizados.
