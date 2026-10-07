---
disable-model-invocation: true
name: nuevo-proyecto
description: Crea un proyecto nuevo (carpetas + célula) haciéndote preguntas simples
argument-hint: <nombre del proyecto>
---

Quiero crear un proyecto nuevo llamado: $ARGUMENTS

Primero leé `00_CORE/atoms/00_vault-rules.md`. Reutilizá las respuestas ya disponibles; preguntá solo lo que falte.

1. Si no te di un nombre, preguntámelo.
2. Armá un "nombre corto": minúsculas, sin tildes, palabras separadas por guiones. Ejemplo: "Mi Tesis 2026" → `mi-tesis-2026`.
3. Fijate que no existan ya `00_CORE/cells/<nombre-corto>-context.md` ni una carpeta `<nombre-corto>/` en la raíz del vault. Buscá también ese identificador en la propiedad `proyecto` de las fichas de `00_CORE/cells/`, aplicando el mismo criterio de nombre corto, aunque el archivo tenga otro nombre: por ejemplo, `aprender-python` ya pertenece a `ejemplo-context.md`. Si hay alguna coincidencia por ruta o propiedad, mostrá cuál es y preguntá si retomamos ese proyecto o elegimos otro identificador. No crees una segunda ficha con el mismo identificador.
4. Completá estos datos conmigo en lenguaje simple, agrupando las preguntas que falten:
   a. ¿De qué se trata el proyecto? (1 a 3 oraciones)
   b. ¿Qué querés lograr, y para cuándo?
   c. ¿Qué tipo de textos vas a escribir más? Explicame las 4 opciones con un ejemplo cada una:
      A = técnico (informes, documentación), B = narrativo (cartas, ensayos),
      C = persuasivo (propuestas, ventas), D = operativo (mails, coordinación).
   d. Contame 2 o 3 cosas que ya sean verdad sobre el proyecto, y dónde se pueden comprobar.
   e. ¿Cuál es el próximo paso concreto?
Antes de crear archivos, mostrá las rutas y los datos reunidos. La solicitud explícita de crear el proyecto autoriza crearlos dentro de ese alcance.

5. Copiá la carpeta `PROJECT_TEMPLATE/` como `<nombre-corto>/` en la raíz del vault. En su `00 - Índice y Contexto.md`, reemplazá los `[completar: ...]` con lo que te conté (los que no sepas, dejalos), cambiá el enlace de la célula por `[[<nombre-corto>-context]]` y poné la fecha de hoy en la propiedad `creado`.
6. Creá `00_CORE/cells/<nombre-corto>-context.md` a partir de `00_CORE/cells/TEMPLATE_cell.md`, con mis respuestas. Respetá su formato: propiedades arriba; hechos como `- hecho (fuente: ...)`; acciones como `- [ ] acción`.
   - **No inventes hechos.** Si no te di una fuente, dejá `(fuente: )` vacío.
   - Poné la fecha de hoy en la propiedad `actualizado`.
   - Borrá los bloques de ayuda de la plantilla (los que están entre `%%`).
7. Si hay Python, corré `python 00_CORE/schemas/validate.py` y corregí los errores de la célula nueva, si los hay. Si no hay Python, seguí la revisión manual de `.claude/skills/validar/SKILL.md` y aclaralo.
8. Mostrame un resumen corto de lo que creaste y recordame que para trabajar uso: `/empezar <nombre-corto>`
