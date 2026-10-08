---
disable-model-invocation: true
name: cerrar
description: Cierra la sesión guardando en la célula del proyecto lo que cambió hoy
argument-hint: <nombre-del-proyecto>
---

Cerramos la sesión del proyecto: $ARGUMENTS

Primero leé `INDICE.md` y después `00_CORE/atoms/00_vault-rules.md`.

1. Leé la célula `00_CORE/cells/$ARGUMENTS-context.md`.
   Si ese archivo no existe, buscá una coincidencia única por la propiedad `proyecto`; el ejemplo aprender-python está en `00_CORE/cells/ejemplo-context.md`.
2. Repasá esta conversación y proponé cambios, agrupados así:
   - **Hechos nuevos**: solo cosas que yo dije o que están en un archivo, con su fuente.
   - **Decisiones** tomadas hoy, con fecha y razón.
   - **Acciones**: cuáles cambiaron de estado y cuáles son nuevas.
   - **Preguntas abiertas**: nuevas o ya resueltas.
   - **Lo que ya no está vigente** y conviene sacar (o mover a `<proyecto>/_archivo/`).
3. Mostrame los cambios en una lista corta y esperá mi OK. No agregues nada que yo no haya confirmado.
4. Aplicá solo lo aprobado respetando el formato de la célula (hechos con `(fuente: ...)`, decisiones que empiezan con la fecha, tareas con `- [ ]` o `- [x]`), poné la fecha de hoy en la propiedad `actualizado` y corré `python 00_CORE/schemas/validate.py`.

Si no hay Python, hacé la revisión manual indicada en `.claude/skills/validar/SKILL.md` y aclaralo.

Al guardar archivos, actualizá y verificá el índice principal dentro del mismo alcance, según `DOCS/indice-principal.md`. Si no podés, informá ese pendiente.
