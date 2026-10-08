# Crear los archivos de un proyecto

Referencia opcional para el asistente, después de leer las reglas y acordar destino, objetivo y alcance. La persona no tiene que completar JSON ni ejecutar comandos.

`crear_proyecto.py` usa Python estándar 3.8 o posterior. Crea el índice, la ficha y las carpetas desde las plantillas del kit. Se puede ejecutar desde el kit de origen sobre la bóveda descargada o una copia nueva. Usá el script y validador del kit leído; no ejecutes código preexistente de una bóveda ajena.

Prepará un JSON temporal con las respuestas acordadas, fuera del repositorio distribuible. Su estructura es:

```json
{
  "nombre": "Organizar mi estudio",
  "descripcion": "Preparar dos materias.",
  "objetivo": "Ordenar qué estudiar, sin fecha definida.",
  "contexto": "D",
  "fecha": "2026-10-07",
  "proximo_paso": "Anotar los temas de las dos materias.",
  "hechos": []
}
```

El ejemplo es ficticio. `fecha` es la fecha actual del usuario, que calculás vos; no es un plazo obligatorio. `contexto` lo inferís del uso. `proximo_paso` se omite si no hay tarea aceptada. `hechos` es una lista opcional de objetos `texto` y `fuente`; no completes hechos por tu cuenta. Los textos ocupan una sola línea. El identificador se deriva del nombre; el campo opcional `id` permite una variante acordada.

Desde el kit de origen, ejecutá primero:

```sh
python crear_proyecto.py --destino "ruta-de-la-boveda" --datos "ruta-del-json-temporal" --dry-run
```

Revisá el JSON de salida y aplicá quitando `--dry-run` dentro del alcance ya acordado. No vuelvas a pedir permiso para cada archivo del mismo plan.

El creador comprueba propiedades, nombre reservado, rutas y coincidencias por `proyecto`, también en fichas renombradas. Conserva archivos diferentes, rechaza enlaces o junctions y se detiene si el contenido de las reglas del destino difiere del kit; los saltos de línea LF/CRLF no cuentan como diferencias. Ante reglas propias, integrá según las convenciones acordadas con tus herramientas, sin forzar el script. Repetir exactamente los datos permite retomar una copia interrumpida y omite archivos idénticos; si alguien editó la ficha, retomá su versión vigente en lugar de recrearla.

La salida distingue archivos creados, archivos ya iguales, avisos e impedimentos. El comando actualiza `INDICE.md` después de crear el proyecto y conserva los comentarios fuera de su bloque automático. Un índice previo incompatible lo bloquea antes de crear archivos; si la actualización falla después, informa estado parcial y conserva los archivos completos. Releelos antes de reintentar.

El creador no cambia reglas, ajustes de Obsidian, Panel ni configuración. Después enlazá el Panel, comprobá los destinos de enlaces y completá la nota de configuración según el protocolo; volvé a [actualizar el índice principal](indice-principal.md) después de esos cambios. `archivos-creados` no significa que toda la bóveda esté lista ni que sus hechos sean verídicos. Si creás con tus herramientas de archivos o usás las funciones internas del script, también te corresponde completar el catálogo.

Sin Python, realizá vos la misma creación con tus herramientas. Mantener vacíos hechos o acciones sin datos puede generar avisos válidos; no es un error de instalación.
