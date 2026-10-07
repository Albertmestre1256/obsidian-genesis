# Usar el kit con ChatGPT, Claude o Gemini

Podés trabajar desde un chat sin terminal. Abrí la bóveda en Obsidian y adjuntá las notas necesarias a tu IA. Al terminar, revisá su propuesta y copiá los cambios aprobados a la nota original. En la siguiente sesión adjuntá la versión actualizada.

Si tu asistente tiene acceso autorizado a la carpeta, puede leer y editar los archivos directamente. Confirmá ese acceso antes de pedirle que guarde algo. Subir una nota como adjunto no mantiene su contenido sincronizado.

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
Quiero crear el proyecto [nombre]. Lee las reglas y las plantillas adjuntas. Pregunta solo lo que falte sobre objetivo, audiencia, hechos con fuentes y próximo paso. Prepara una ficha con propiedades válidas y un índice del proyecto. Usa un nombre corto en minúsculas, sin tildes y con guiones entre palabras para el archivo y la carpeta. Si puedes leer mi bóveda, comprueba que no existan las rutas de destino ni otra ficha con ese identificador en la propiedad proyecto, aunque tenga otro nombre de archivo. Ante una coincidencia, indícala y pide que elija entre retomar ese proyecto o usar otro identificador. Si no puedes comprobarlo, indícame qué revisar antes de crear archivos. No inventes datos. Si no puedes escribir en mi bóveda, dame cada texto con su destino y las carpetas que tengo que crear.
```

Antes de guardar, revisá la propiedad `proyecto` de las fichas en `00_CORE/cells/` y las rutas propuestas. El ejemplo ya usa el identificador `aprender-python`, aunque su archivo se llame `ejemplo-context.md`. Si el nombre está libre, guardá la ficha dentro de `00_CORE/cells/`, con un nombre terminado en `-context.md`; duplicá `PROJECT_TEMPLATE/` para la carpeta del proyecto y actualizá su índice. Completá la fecha real; los marcadores de Plantillas se resuelven en Obsidian al insertar la plantilla, no al adjuntarla a un chat.

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

Después de aprobar: actualizá la nota en Obsidian y reemplazá el adjunto del proyecto o Gem cuando corresponda. Así la próxima conversación recibe el avance real.

## Fuentes de configuración

Guía revisada el 29 de septiembre de 2026. Los nombres de menús pueden variar por idioma y cuenta.

- [Proyectos y chats de ChatGPT](https://learn.chatgpt.com/docs/projects).
- [Crear y administrar proyectos de Claude](https://support.claude.com/en/articles/9519177-how-can-i-create-and-manage-projects).
- [Instrucciones y archivos de una Gem](https://support.google.com/gemini/answer/15235603).
