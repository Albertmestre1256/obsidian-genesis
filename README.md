> **Crédito principal a [davidkimai](https://github.com/davidkimai):** este kit se basa en su trabajo [Context Engineering](https://github.com/davidkimai/Context-Engineering). Obsidian Genesis adapta ese trabajo para iniciar y organizar bóvedas de Obsidian con ayuda de una IA.
> [!info] Índice de esta nota (líneas)
> - Líneas 1–1: Atribución
> - Líneas 2–13: Este índice
> - Líneas 15–20: Obsidian Genesis: tu bóveda, configurada por una IA
> - Líneas 21–41: Empezar en tres pasos
> - Líneas 42–47: Adjuntos o bóveda existente
> - Líneas 48–55: Continuar
> - Líneas 56–67: Qué contiene
> - Líneas 68–76: Ayuda opcional
> - Líneas 77–80: Privacidad
> - Líneas 81–84: English
> - Líneas 85–87: Licencia

# Obsidian Genesis: tu bóveda, configurada por una IA

Descargá el kit, dale la carpeta a una IA y respondé sus preguntas. El asistente prepara tus notas y tu primer proyecto usando las reglas del kit. No necesitás programar ni conocer Obsidian.

Una **bóveda** es una carpeta de notas que abrís con [Obsidian](https://obsidian.md). El kit está en español y sirve para estudio, trabajo o cualquier proyecto personal.

## Empezar en tres pasos

1. **Descargá y descomprimí** el repositorio: Code → Download ZIP.
2. **Abrí la carpeta en una IA que pueda leer y escribir archivos.** Elegí la que contiene este README y `AI-INSTRUCTIONS.md`.
3. **Pegá este mensaje y respondé sus preguntas:**

   > Quiero que configures mi bóveda de Obsidian con este kit. Leé primero `INDICE.md`, después `00_CORE/atoms/00_vault-rules.md` y `AI-INSTRUCTIONS.md`. No conozco Obsidian: guiame con preguntas simples, de a una o dos por vez, y encargate de los archivos según mis respuestas. Antes de escribir, explicame dónde vas a guardar todo y qué vas a crear. Mantené el índice principal actualizado. Si no tenés acceso para hacerlo, decímelo.

| Usás | Cómo abrir el kit |
|---|---|
| OpenCode | Abrí la carpeta y usá el mensaje anterior o `/configurar`. [Guía](DOCS/opencode.md). |
| ChatGPT | Carpeta local con herramientas de archivos o copia adjunta. [Guía](DOCS/chatgpt.md). |
| Claude Code | Abrí la carpeta y usá el mensaje anterior o `/configurar`. |
| Otra IA | Dale acceso a la carpeta y usá el mismo mensaje. |

La IA pregunta qué querés organizar, qué notas conservar y cuál es el objetivo. Podés responder «todavía no sé» o «no tengo fecha»; la primera tarea puede elegirse después.

También guarda un **inventario de personalización**: lo respondido, lo pendiente y lo que elegiste saltar. Presentación, CV, formación, rutina y duración de la bóveda son opcionales. Podés empezar con lo básico y decir después **«qué falta para personalizar mi bóveda»** o **«completemos mi perfil»**. [Cómo funciona](00_CORE/protocols/personalizar-vault.md).

**Recibís:** carpeta preparada, ficha del proyecto, Panel para acceder y explicación para abrirla en Obsidian. La IA verifica los archivos; la prueba visual se hace en Obsidian. Si aún no lo tenés, instalalo desde [obsidian.md](https://obsidian.md), abrí la carpeta preparada como bóveda y entrá a `Panel.md`.

## Adjuntos o bóveda existente

Un ZIP adjunto no da acceso a tu computadora. Si el chat genera archivos, puede devolverte una copia configurada para descargar. Si solo responde texto, queda pendiente guardarlo. La [guía de acceso](DOCS/empezar-con-ia.md) explica las opciones.

Si ya tenés una bóveda, dale acceso también a esa carpeta y señalala como destino. La IA lee sus reglas y conserva notas y ajustes. Los conflictos se comparan antes de integrar.

## Continuar

Decí **«Seguí con [proyecto]»**. La IA lee primero el índice, después las reglas y la ficha vigente, y retoma lo pendiente. Podés pedir otro proyecto, un borrador, una revisión o guardar el cierre: [pedidos de uso diario](DOCS/usar-con-otras-ias.md).

Para organizar más contenido, pedí **«Agregá un nodo para resúmenes de mis materias»**. Cada nodo tiene un índice con enlaces y resúmenes; el mapa general conecta todos los nodos y la IA los mantiene al agregar notas. [Guía](DOCS/indice-principal.md).

Claude Code y OpenCode incluyen `/configurar`, `/empezar`, `/nuevo-proyecto`, `/redactar`, `/validar` y `/cerrar`. En Claude, crear otro proyecto y cerrar son de invocación manual. Los permisos dependen del asistente. Con adjuntos, compartí siempre las notas vigentes: no están sincronizadas.

## Qué contiene

| Lugar | Uso |
|---|---|
| `INDICE.md` | Primera lectura: catálogo completo de archivos y proyectos |
| `Panel.md` | Acceso a proyectos y tareas |
| `00_CORE/` | Reglas, fichas, guías y herramientas |
| `PROJECT_TEMPLATE/` | Carpetas para fuentes, borradores, entregables e historial |
| `DOCS/` | Ayuda opcional |

El ejemplo `aprender-python` es ficticio y está separado de proyectos propios. Tus datos se completan con tus respuestas; las secciones sin información pueden quedar vacías.

## Ayuda opcional

- [Crear un proyecto a mano](DOCS/primer-proyecto.md).
- [Integrar el kit sin Python](DOCS/instalacion-manual.md).
- [Plantillas y panel](DOCS/obsidian.md).
- [Solución de problemas](DOCS/TROUBLESHOOTING.md).

Python 3.8 o posterior automatiza instalación, creación, validación e índice con la biblioteca estándar. La IA también puede configurar usando sus herramientas de archivos. Para contribuir: [CONTRIBUTING](CONTRIBUTING.md).

## Privacidad

El kit guarda archivos locales y no instala sincronización. La IA procesa lo compartido según su servicio y configuración: dale solo el contexto necesario.

## English

An AI-guided Obsidian starter kit for OpenCode, ChatGPT, Claude Code and other file-capable assistants. Give the AI the folder and the setup prompt above. It reads the index and rules first and prepares your project through simple questions. Documentation is in Spanish. Attachments alone cannot grant access to your local folder.

## Licencia

[MIT](LICENSE), con los créditos de davidkimai y Albert Mestre. Adaptación independiente de Context Engineering, sin afiliación al proyecto original.
