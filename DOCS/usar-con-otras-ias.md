# Usar el kit con ChatGPT, Claude o Gemini

**¿Todavía no tenés configurada la bóveda?** Empezá por [darle la carpeta a tu IA](empezar-con-ia.md). Esta guía sirve para el trabajo diario después del arranque.

Con una IA que tenga acceso a tu carpeta, pedile que lea las reglas y la ficha y se encargue de los archivos. Al terminar, revisá su propuesta de cambios; después de aprobarla, la IA guarda y verifica lo acordado.

También podés trabajar desde un chat sin terminal usando adjuntos. En ese caso, revisá su propuesta y copiá los cambios aprobados a la nota original; en la siguiente sesión adjuntá la versión actualizada. Subir una nota como adjunto no mantiene su contenido sincronizado. El asistente debe aclarar qué acceso tiene antes de afirmar que guardó algo.

## Dejar preparado un espacio por proyecto

| Producto | Preparación |
|---|---|
| ChatGPT | Creá un Proyecto, añadí las reglas y la ficha del proyecto como archivos e incorporá la instrucción de abajo en las instrucciones del proyecto. Los proyectos locales del escritorio pueden trabajar con carpetas adjuntas. |
| Claude | Creá un Project, agregá reglas y ficha al conocimiento del proyecto y guardá la instrucción de abajo en sus instrucciones. |
| Gemini | Creá una Gem, guardá la instrucción de abajo y agregá reglas y ficha en Knowledge/Conocimientos, si esa opción está disponible en tu cuenta. |

También podés usar un chat común y volver a adjuntar ambos archivos. No hace falta subir todo el vault.

**Instrucción de arranque para copiar:**

```text
Trabajamos con un proyecto documentado en Obsidian. Primero lee las reglas de la bóveda adjuntas y después la ficha del proyecto que te indique. Usa solo información disponible y distingue hechos, interpretación y pendientes. Pide los archivos que falten para la tarea. Antes de guardar el cierre de sesión, presenta los cambios concretos para que los revise. Si no tienes acceso de escritura, entrega el texto listo para pegar e indica su archivo; no digas que ya lo guardaste. No mezcles este proyecto con otros.
```

## Cinco prompts listos para pegar

Reemplazá los campos entre corchetes. Los prompts no dependen de comandos slash ni de variables de Claude Code.

### 1. Empezar

Adjuntá reglas y ficha. Para probar, usá `00_CORE/cells/ejemplo-context.md` y el proyecto `aprender-python`; su contenido es ficticio.

```text
Retomemos [nombre del proyecto]. Lee primero las reglas de la bóveda y después su ficha adjunta. Resume el objetivo, las decisiones vigentes, las acciones pendientes y el siguiente paso. Si falta información, indícalo. No cambies archivos todavía.
```

### 2. Crear un proyecto

Adjuntá las reglas, `00_CORE/cells/TEMPLATE_cell.md` y el índice de `PROJECT_TEMPLATE/`.

```text
Quiero crear el proyecto [nombre]. Lee las reglas y las plantillas. Pregunta solo lo que falte, de a una o dos preguntas, sobre objetivo, uso y próximo paso. No exijas una fecha ni hechos que todavía no tengo. Prepara una ficha con propiedades válidas y un índice del proyecto; deja vacías las secciones sin datos y quita los marcadores de ejemplo. Usa un nombre corto en minúsculas, sin tildes y con guiones. Si puedes leer mi bóveda, comprueba que no existan las rutas de destino ni otra ficha con ese identificador en la propiedad proyecto, aunque tenga otro nombre. Ante una coincidencia, ofrece retomar ese proyecto o usar otro identificador. Si puedes escribir, crea y verifica los archivos dentro del alcance acordado, sin mandarme a copiarlos. Si no puedes comprobar o escribir, acláralo y entrega los textos con sus destinos. No inventes datos.
```

La IA con acceso a archivos debe comprobar las coincidencias, crear la ficha y el índice y enlazar el Panel. El ejemplo ya usa `aprender-python`, aunque su archivo se llame `ejemplo-context.md`. Si trabajás solo con adjuntos, guardá los textos entregados en los destinos indicados y usá la [guía manual](primer-proyecto.md). La fecha de actualización debe ser real; adjuntar una plantilla a un chat no resuelve automáticamente sus marcadores.

### 3. Redactar

Para un mensaje breve, bastan reglas, ficha y tu pedido con destinatario y objetivo. Para un informe, carta o propuesta con estructura, agregá el marco `00_CORE/molecules/marco-comunicacion-general.md`, el protocolo `00_CORE/protocols/ai-write-protocol.md` y la guía de redacción adecuada en `00_CORE/cognitive-tools/` (técnica, narrativa, persuasiva u operativa).

```text
Necesito [tipo de texto] para [destinatario], en el proyecto [nombre]. Quiero que el destinatario [acción o idea principal]. Lee primero las reglas y la ficha. Si es un texto breve, redacta un borrador en el chat. Si necesita estructura, consulta las guías adjuntas, propón un plan breve y espera mi aprobación. Pregunta solo por datos que cambien el resultado. Usa hechos respaldados; marca los datos que falten. Entrega el borrador y una ruta dentro de la síntesis de este proyecto. No envíes el texto a nadie.
```

### 4. Validar

Adjuntá las fichas y `00_CORE/schemas/validate.py` para que la IA tenga las reglas reales. Si el chat puede ejecutar Python sobre adjuntos, puede correr el script con la carpeta de esas copias; eso no modifica el vault.

```text
Revisa las fichas adjuntas usando las reglas del validador. Si puedes ejecutarlo, informa qué archivos revisó y su resultado. Si no, haz una revisión manual y acláralo. Distingue errores de formato de avisos y no confundas formato correcto con hechos verificados. Propón correcciones concretas sin modificar nada.
```

### 5. Cerrar

```text
Cerramos la sesión de [nombre del proyecto]. Compara lo trabajado con la ficha adjunta más reciente. Propón solo hechos nuevos con fuente, decisiones, cambios en acciones y preguntas abiertas. No dupliques lo existente ni conviertas propuestas en decisiones. Espera mi aprobación. Después entrega la ficha actualizada, o guarda los cambios si tienes acceso autorizado, y verifica el resultado.
```

Después de aprobar, la IA con acceso guarda y verifica la nota. Si usás solo adjuntos, actualizá la nota en Obsidian y reemplazá el adjunto del proyecto o Gem cuando corresponda. Así la próxima conversación recibe el avance real.

## Fuentes de configuración

Guía revisada el 29 de septiembre de 2026. Los nombres de menús pueden variar por idioma y cuenta.

- [Proyectos y chats de ChatGPT](https://learn.chatgpt.com/docs/projects).
- [Crear y administrar proyectos de Claude](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects).
- [Instrucciones y archivos de una Gem](https://support.google.com/gemini/answer/15235603).
