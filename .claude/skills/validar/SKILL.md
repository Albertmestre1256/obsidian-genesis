---
name: validar
allowed-tools:
  - Bash(python 00_CORE/schemas/validate.py)
  - Bash(python3 00_CORE/schemas/validate.py)
  - Bash(py 00_CORE/schemas/validate.py)
description: Revisa las células de proyecto y explica en simple cualquier problema
---

Primero leé `INDICE.md` y después `00_CORE/atoms/00_vault-rules.md`.

1. Corré `python 00_CORE/schemas/validate.py`. Si el comando no está disponible, probá con `python3` y, en Windows, con `py`. Un resultado con errores de las fichas no significa que falte Python: informá esos errores.
   - **Si no hay Python**, leé las reglas y las funciones de lectura y validación de `00_CORE/schemas/validate.py`; son la fuente de verdad. Revisá cada `00_CORE/cells/*-context.md` sin ejecutar el script. Usá este resumen para orientarte:
     - ERRORES de propiedades: falta el bloque inicial entre `---`, hay sintaxis no admitida o claves repetidas, falta una propiedad obligatoria o su valor no sirve. Son obligatorias `tipo`, `proyecto`, `descripcion`, `contexto` y `actualizado`. `tipo` debe ser `celula`; `proyecto` y `descripcion`, texto no vacío; `contexto` acepta A/B/C/D, también minúsculas o formas como `D - operativo`; `actualizado` debe ser una fecha real en formato AAAA-MM-DD.
     - El lector admite propiedades planas con valores en una línea, comillas cerradas, comentarios y listas simples en campos adicionales como `tags`. Informa como no admitidos los mapas, bloques multilínea y referencias YAML. No confundas una limitación de este lector con sintaxis YAML inválida.
     - ERRORES del cuerpo: faltan `## Hechos clave` o `## Próximas acciones`, o una viñeta de acciones no es una tarea con texto. Admite los marcadores `-`, `*` y `+`, y las casillas `[ ]`, `[x]` o `[X]`. Para reconocer títulos y viñetas, seguí las funciones `normalizar` y `secciones`.
     - AVISOS: no hay hechos o acciones; un hecho no termina con `(fuente: ...)` o la fuente está vacía; una decisión no empieza con fecha válida; quedan marcadores `[completar: ...]` en los campos o viñetas revisados; o la estimación de tamaño supera `MAX_TOKENS_CELULA`.
     - Al revisar secciones, ignorá los bloques entre `%%` y las sub-viñetas, como hace el script. Su estimación de tamaño usa el texto completo.
     Indicá qué archivos revisaste, que la revisión fue manual y cualquier comprobación que no pudiste resolver. No afirmes que el script pasó.
2. Si sale "TODO BIEN" sin avisos, decímelo en una línea y listo.
3. Si hay ERRORES o avisos, para cada uno:
   - explicame en una oración qué significa (usá `DOCS/TROUBLESHOOTING.md` si hace falta),
   - mostrame la corrección exacta: cómo está la línea ahora y cómo quedaría.
4. No apliques ninguna corrección hasta que te diga que sí.
