---
name: empezar
description: Arranca una sesión de trabajo en un proyecto cargando solo el contexto necesario
argument-hint: <nombre-del-proyecto>
---

Vamos a trabajar en el proyecto: $ARGUMENTS

1. Leé `00_CORE/atoms/00_vault-rules.md` (las reglas del vault).
2. Leé la célula `00_CORE/cells/$ARGUMENTS-context.md`.
   - Si no existe, buscá una célula cuya propiedad `proyecto` coincida con el nombre pedido. Por ejemplo, `aprender-python` está en `00_CORE/cells/ejemplo-context.md`. Si hay una coincidencia única, usala; si hay varias o ninguna, listá las opciones y preguntá. No confundas los datos ficticios del ejemplo con datos del usuario.
   - Si no hay ninguna, sugerime crear una con `/nuevo-proyecto`.
3. No leas otros proyectos, índices ni archivos que no te pida: cuanto menos contexto de más, mejor trabajás.
4. Respondeme en no más de 8 líneas:
   - De qué trata el proyecto y cuál es su objetivo
   - Qué acciones están en curso y cuáles pendientes
   - Preguntas abiertas, si hay
   - Qué me sugerís hacer primero y por qué
5. Esperá mi respuesta antes de cambiar cualquier archivo.
