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
   Si la coincidencia es el ejemplo ficticio, proponé otro identificador para el proyecto propio. Conservá el ejemplo y no trates sus datos como personales; solo usalo para practicar si la persona lo elige.
4. Completá estos datos conmigo en lenguaje simple, agrupando las preguntas que falten:
   a. ¿De qué se trata el proyecto? (1 a 3 oraciones)
   b. ¿Qué querés lograr? La fecha del objetivo es opcional; no la exijas si no tiene una.
   c. ¿Para qué vas a usar estas notas? Inferí el contexto A/B/C/D de su respuesta; no exijas que el usuario conozca esas letras.
   d. ¿Hay algún dato que ya deba tener en cuenta? Si lo hay, preguntá de dónde sale. No exijas una cantidad mínima de hechos.
   e. ¿Cuál es el próximo paso concreto?
Hacé una o dos preguntas por turno, sin repetir lo ya respondido. Antes de crear archivos, mostrá las rutas y los datos reunidos. La solicitud explícita de crear el proyecto autoriza crearlos dentro de ese alcance.

5. Creá índice, ficha y carpetas con las respuestas acordadas. Con Python y las reglas del kit sin cambios, podés usar `crear_proyecto.py` siguiendo `DOCS/creacion-para-asistentes.md`. Si lo usás, no vuelvas a crear a mano esos mismos archivos. Sin esa herramienta, copiá `PROJECT_TEMPLATE/` como `<nombre-corto>/`, completá el índice, cambiá el enlace por el de la ficha y poné la fecha de hoy en `creado`.
6. Creá `00_CORE/cells/<nombre-corto>-context.md` a partir de `00_CORE/cells/TEMPLATE_cell.md`, con mis respuestas. Respetá su formato: propiedades arriba; hechos como `- hecho (fuente: ...)`; acciones como `- [ ] acción`.
   - **No inventes hechos.** Si no te di una fuente, dejá `(fuente: )` vacío.
   - Poné la fecha de hoy en la propiedad `actualizado`.
   - Borrá los bloques de ayuda de la plantilla (los que están entre `%%`).
   - Quitá los marcadores de ejemplo. Si no hay hechos o un próximo paso aceptado, dejá vacía esa sección; si falta el objetivo del proyecto, preguntalo. No inventes un plazo ni una acción para silenciar avisos.
   - Enlazá ficha e índice y agregá un acceso al Panel conservando su contenido.
7. Si hay Python, corré `python 00_CORE/schemas/validate.py` y corregí los errores de la célula nueva, si los hay. Si no hay Python, seguí la revisión manual de `.claude/skills/validar/SKILL.md` y aclaralo.
8. Mostrame un resumen corto de lo que creaste y recordame que para trabajar uso: `/empezar <nombre-corto>`
