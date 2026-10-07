---
disable-model-invocation: true
name: nuevo-proyecto
description: Crea las carpetas y la ficha de un proyecto mediante preguntas simples.
argument-hint: <nombre del proyecto>
---

Proyecto solicitado: $ARGUMENTS

1. Leé primero `00_CORE/atoms/00_vault-rules.md`. Reutilizá las respuestas disponibles y preguntá solo por nombre, propósito y objetivo que falten, de a una o dos preguntas por turno. El plazo, los hechos y la primera tarea pueden quedar pendientes; una sugerencia no es una tarea aceptada. Inferí el contexto de comunicación.
2. Derivá un identificador corto válido. Comprobá rutas y coincidencias por la propiedad `proyecto`, aunque la ficha tenga otro nombre. Ante una coincidencia propia, ofrecé retomar o elegir otro identificador. Si es el ejemplo ficticio, conservá sus datos y proponé un identificador distinto para el proyecto personal.
3. Mostrá destino, objetivo, paso aceptado si lo hay y archivos que vas a crear. La solicitud explícita autoriza ese alcance, sin reemplazar archivos existentes.
4. Aplicá la sección **Crear el proyecto** de `00_CORE/protocols/configurar-vault.md`, que comparte las mismas plantillas y comprobaciones con la configuración inicial. No reinicies la entrevista de la bóveda ni ejecutes su instalación. Con Python podés usar `crear_proyecto.py`, siguiendo `DOCS/creacion-para-asistentes.md`; si lo usás, no recrees a mano lo que ya produjo.
5. Releé y verificá los archivos, los enlaces del Panel y el formato de la ficha con el validador del kit. Sin Python, aplicá la revisión manual de `.claude/skills/validar/SKILL.md`. Conservá los datos y ajustes existentes; si hay una nota de configuración, agregá el enlace al proyecto sin rehacerla.
6. Entregá un acceso a la ficha y el próximo paso elegido o pendiente. Para retomar puede decir «seguí con este proyecto» o usar `/empezar <nombre-corto>`.
