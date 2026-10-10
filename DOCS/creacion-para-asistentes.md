> [!info] Índice de esta nota (líneas)
> - Líneas 1–3: Este índice
> - Líneas 5–40: Crear los archivos de un proyecto

# Crear los archivos de un proyecto

Referencia del asistente para «Crear el proyecto» del [protocolo](../00_CORE/protocols/configurar-vault.md), con destino, objetivo y alcance acordados. `crear_proyecto.py` usa Python estándar 3.8+ y las plantillas del kit leído. La persona no prepara JSON ni ejecuta comandos.

Desde ese kit, prepará un JSON temporal con las respuestas, fuera del repositorio distribuible:

```json
{
  "nombre": "Organizar mi estudio",
  "descripcion": "Preparar dos materias.",
  "objetivo": "Ordenar qué estudiar, sin fecha definida.",
  "contexto": "D",
  "autor": "IA identificada (herramienta y modelo si se conoce)",
  "fecha": "2026-10-07",
  "proximo_paso": "Anotar los temas de las dos materias.",
  "hechos": []
}
```

Ejemplo ficticio: calculá la fecha actual del usuario e inferí `contexto` del uso. Omití `proximo_paso` si no hay tarea aceptada; `hechos` admite objetos `texto`/`fuente`, sin inventarlos. Textos en una línea; el identificador deriva del nombre o de un `id` opcional acordado.

Simulá primero:

```sh
python crear_proyecto.py --destino "ruta-de-la-boveda" --datos "ruta-del-json-temporal" --dry-run
```

Revisá la salida y aplicá quitando `--dry-run`, sin repetir permisos del mismo alcance.

El creador verifica propiedades, nombres, rutas y coincidencias por `proyecto`, incluidas fichas renombradas. Conserva archivos diferentes y rechaza enlaces/junctions. Requiere reglas compatibles: LF/CRLF se consideran iguales; ante reglas propias, creá con herramientas de archivos según sus convenciones.

Repetir los mismos datos recupera una copia interrumpida y omite archivos idénticos. Si editaron una ficha, retomá esa versión. La salida distingue creados, iguales, avisos e impedimentos. Un índice incompatible bloquea la creación; un fallo posterior deja estado parcial y conserva archivos completos. Releé antes de reintentar.

El comando crea ficha, índice y carpetas y actualiza `INDICE.md`. Luego completá Panel, configuración e inventario según el protocolo y volvé a [actualizar el catálogo](indice-principal.md). `archivos-creados` solo acredita esa etapa, sin verificar hechos ni interfaz.

Sin Python, hacé la creación con tus herramientas y mantené el mismo catálogo. Hechos o acciones vacíos pueden generar avisos válidos.
