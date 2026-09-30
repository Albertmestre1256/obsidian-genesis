---
name: validar
allowed-tools:
  - Bash(python 00_CORE/schemas/validate.py)
  - Bash(python3 00_CORE/schemas/validate.py)
  - Bash(py 00_CORE/schemas/validate.py)
description: Revisa las células de proyecto y explica en simple cualquier problema
---

Primero leé `00_CORE/atoms/00_vault-rules.md`.

1. Corré `python 00_CORE/schemas/validate.py`. Si no funciona, probá con `python3` y, en Windows, con `py`.
   - **Si no hay Python**, revisá vos cada `00_CORE/cells/*-context.md` con estas reglas (son las mismas del script):
     - ERROR si falta alguna propiedad: `tipo` (celula), `proyecto`, `descripcion`, `contexto` (A, B, C o D), `actualizado` (fecha AAAA-MM-DD).
     - ERROR si faltan las secciones `## Hechos clave` o `## Próximas acciones`, o si una acción no empieza con `- [ ] ` o `- [x] `.
     - Aviso si un hecho no termina con `(fuente: ...)`, si una decisión no empieza con una fecha, si quedan `[completar: ...]` o si la célula es muy larga (más de ~12.000 caracteres).
     - Ignorá los bloques entre `%%` y las sub-viñetas.
     Aclarame que la revisión la hiciste vos, no el script.
2. Si sale "TODO BIEN" sin avisos, decímelo en una línea y listo.
3. Si hay ERRORES o avisos, para cada uno:
   - explicame en una oración qué significa (usá `DOCS/TROUBLESHOOTING.md` si hace falta),
   - mostrame la corrección exacta: cómo está la línea ahora y cómo quedaría.
4. No apliques ninguna corrección hasta que te diga que sí.
