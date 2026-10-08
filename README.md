> **Crédito principal a [davidkimai](https://github.com/davidkimai):** este kit se basa en su trabajo [Context Engineering](https://github.com/davidkimai/Context-Engineering). Obsidian Genesis adapta ese trabajo para iniciar y organizar bóvedas de Obsidian con ayuda de una IA.

# Obsidian Genesis: tu bóveda, configurada por una IA

Descargá el kit, dale la carpeta a una IA con acceso a archivos y respondé sus preguntas. El asistente usa las reglas del kit para preparar tus notas y tu primer proyecto. No necesitás programar, editar plantillas ni conocer Obsidian.

Una **bóveda** es una carpeta de notas que abrís con [Obsidian](https://obsidian.md). El kit está en español y sirve para estudio, trabajo o cualquier proyecto personal.

## Elegí tu IA

| Usás | Cómo iniciar |
|---|---|
| OpenCode | Abrí la carpeta del kit y escribí `/configurar`. [Guía](DOCS/opencode.md). |
| ChatGPT | Abrí la carpeta en la app con acceso local o trabajá con una copia adjunta. [Guía](DOCS/chatgpt.md). |
| Claude Code | Abrí la carpeta del kit y escribí `/configurar`. |
| Otra IA con herramientas de archivos | Seguí los tres pasos de abajo. |

Todas usan el mismo índice, reglas y protocolo de preguntas. Si tu asistente no muestra `/configurar`, podés pegar el mensaje de inicio de abajo.

## Empezar en tres pasos

1. **Descargá y descomprimí** el repositorio: Code → Download ZIP, o el ZIP de una versión publicada.
2. **Abrí la carpeta en un asistente que pueda leer y escribir archivos.** Elegí la que contiene este README y `AI-INSTRUCTIONS.md`.
3. **Pegá este mensaje y respondé sus preguntas:**

   > Quiero que configures mi bóveda de Obsidian con este kit. Leé primero `INDICE.md`, después `00_CORE/atoms/00_vault-rules.md` y `AI-INSTRUCTIONS.md`. No conozco Obsidian: guiame con preguntas simples, de a una o dos por vez, y encargate de los archivos según mis respuestas. Antes de escribir, explicame en qué carpeta vas a guardar todo y qué vas a crear. Mantené el índice principal actualizado. Si no tenés acceso para hacerlo, decímelo.

La IA pregunta qué querés organizar, si empezás de cero o tenés notas que conservar y cuál es el objetivo del primer proyecto. Podés responder «todavía no sé» o «no tengo fecha»; la primera tarea puede elegirse después.

**Al terminar recibís:** la carpeta preparada, una ficha con el estado del proyecto, un Panel para acceder a ella y la explicación para abrir la bóveda en Obsidian. La IA verifica los archivos; el funcionamiento visual se comprueba en Obsidian.

Si todavía no tenés Obsidian, podés preparar la carpeta igual. Después instalalo desde [obsidian.md](https://obsidian.md), elegí abrir una carpeta como bóveda, seleccioná la carpeta preparada y abrí `Panel.md`.

## Si usás adjuntos o ya tenés una bóveda

Un ZIP adjunto no da acceso a tu computadora. Si el chat puede generar archivos, puede devolverte una copia configurada para descargar y descomprimir. Si solo responde texto, quedará pendiente guardar los contenidos. La [guía de acceso a la carpeta](DOCS/empezar-con-ia.md) explica estas opciones.

Si ya tenés una bóveda, dale acceso también a esa carpeta y aclarale que es el destino. La IA debe leer sus reglas y conservar tus notas y ajustes. El instalador agrega archivos ausentes y se detiene ante incompatibilidades; la integración se acuerda antes de modificar contenido existente.

## Continuar con tu proyecto

Decí **«Seguí con [nombre del proyecto]»**. La IA lee las reglas y la ficha guardada y retoma lo pendiente, sin repetir la entrevista inicial. También podés pedir que redacte, cree otro proyecto o proponga qué guardar al cerrar la sesión.

Los [pedidos de uso diario](DOCS/usar-con-otras-ias.md) sirven con cualquier IA que lea el contexto. Con adjuntos, usá la ficha vigente y actualizá la nota original con los cambios aprobados: son copias, no archivos sincronizados.

Claude Code incluye `/configurar`, `/empezar`, `/redactar`, `/validar`, `/nuevo-proyecto` y `/cerrar`. Los dos últimos conservan su invocación manual. El acceso y los permisos dependen del asistente.

OpenCode incluye `/configurar` y usa los pedidos de uso diario para continuar. En ChatGPT podés usar esos mismos pedidos y las instrucciones de proyecto de su guía.

## Dónde está cada cosa

| Lugar | Uso |
|---|---|
| `INDICE.md` | Primera lectura de la IA: catálogo completo de la bóveda, proyectos y recursos |
| `Panel.md` | Acceso a proyectos propios y tareas pendientes |
| `00_CORE/atoms/` | Reglas compartidas |
| `00_CORE/cells/` | Una ficha por proyecto: objetivo, hechos, decisiones y acciones |
| `00_CORE/configuracion.md` | Estado de la configuración; se crea al configurar |
| Carpeta de cada proyecto | Material original, borradores, resultados finales e historial |
| `PROJECT_TEMPLATE/` | Modelo que la IA usa para crear proyectos |
| `DOCS/` | Ayuda opcional y guías de uso |

La ficha también se llama **célula** en los archivos. El ejemplo `aprender-python` es ficticio: podés consultarlo desde la ayuda del Panel, separado de tus proyectos. Tus datos y tareas se completan con tus respuestas; las secciones sin información pueden quedar vacías.

La IA empieza por el [índice principal](INDICE.md) para saber qué hay, lee las reglas y elige las notas necesarias para el proyecto. Mantiene el catálogo al guardar cambios; vos no tenés que editarlo. [Cómo se mantiene](DOCS/indice-principal.md).

## Ayuda opcional

- [Crear un proyecto a mano](DOCS/primer-proyecto.md).
- [Agregar el kit a una bóveda existente sin Python](DOCS/instalacion-manual.md).
- [Plantillas y panel](DOCS/obsidian.md).
- [Solución de problemas](DOCS/TROUBLESHOOTING.md).

La IA puede configurar con sus propias herramientas. Python 3.8 o posterior permite usar el instalador, el creador de proyectos y el validador, todos con la biblioteca estándar; no es un requisito para el inicio conversacional. La [guía para asistentes](DOCS/creacion-para-asistentes.md) explica el creador opcional.

El validador revisa el formato de las fichas, no la veracidad de los datos. Los avisos por hechos o tareas vacíos no bloquean la configuración. Para revisar desde la carpeta del kit:

```sh
python 00_CORE/schemas/validate.py
```

Para contribuir: [CONTRIBUTING](CONTRIBUTING.md).

## Privacidad

El kit guarda archivos locales y no instala sincronización. La IA puede procesar lo que le compartas según su servicio y configuración. Dale solo el contexto necesario para la tarea.

## English

An AI-guided Obsidian starter kit for OpenCode, ChatGPT, Claude Code, and other file-capable assistants. Use the guide for your assistant and the setup prompt above. It reads the vault index and rules first and prepares your project through simple questions. Documentation is in Spanish. Attachments alone cannot grant access to your local folder.

## Licencia

[MIT](LICENSE), con los créditos de davidkimai y Albert Mestre. Este kit es una adaptación independiente de Context Engineering y no está afiliado al proyecto original.
