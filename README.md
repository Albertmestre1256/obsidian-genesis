> **Crédito principal a [davidkimai](https://github.com/davidkimai):** este kit se basa en su trabajo [Context Engineering](https://github.com/davidkimai/Context-Engineering). Obsidian Genesis adapta ese trabajo para iniciar y organizar bóvedas de Obsidian con ayuda de una IA.

# Obsidian Genesis: tu bóveda, configurada por una IA

Descargá el kit, dale la carpeta a una IA que pueda leer y escribir archivos y respondé sus preguntas. El asistente usa las reglas del kit para preparar tu bóveda y tu primer proyecto. Vos contás qué necesitás; la IA se encarga de los archivos.

Una **bóveda** es una carpeta de notas que podés abrir con [Obsidian](https://obsidian.md). El kit está en español y sirve para estudio, trabajo o proyectos personales.

## Empezar

1. **Descargá y descomprimí** el repositorio: Code → Download ZIP. Si hay una versión publicada, también podés usar su ZIP.
2. **Abrí la carpeta en tu asistente con acceso a archivos.** Elegí la carpeta que contiene este README y `AI-INSTRUCTIONS.md`. Si solo usás un chat con adjuntos, consultá el apartado siguiente.
3. **Pegá este mensaje y respondé sus preguntas:**

   > Quiero que configures mi bóveda de Obsidian con este kit. Leé primero `00_CORE/atoms/00_vault-rules.md` y después `AI-INSTRUCTIONS.md`. No conozco Obsidian: guiame con preguntas simples, de a una o dos por vez, y encargate de los archivos según mis respuestas. Antes de escribir, explicame en qué carpeta vas a guardar todo y qué vas a crear. Si no tenés acceso para hacerlo, decímelo.

La IA pregunta qué querés organizar y si empezás de cero o tenés notas que conservar. Después define con vos el objetivo del primer proyecto, muestra qué va a preparar y crea los archivos. No necesitás programar, elegir una estructura de carpetas ni editar plantillas.

Podés responder «todavía no sé» o «no tengo una fecha». Si todavía no elegiste una primera tarea, el proyecto puede quedar preparado para elegirla después. La IA debe distinguir tus respuestas de sus sugerencias y de los datos que falten.

Al terminar, recibís la ubicación de la bóveda, un acceso a tu proyecto y una explicación para abrir esa carpeta en Obsidian. Podés empezar a trabajar con la IA en la misma conversación.

## Si usás un chat con adjuntos

Adjuntar un ZIP no le permite al chat editar la carpeta de tu computadora. Si puede leerlo y generar archivos, puede devolverte una copia configurada: descargala, descomprimila y abrí esa carpeta en Obsidian. Si solo responde texto, podrá preparar contenidos, pero la configuración quedará pendiente de guardarlos.

Encontrá más detalles en [Empezar con una IA](DOCS/empezar-con-ia.md).

## Si ya tenés una bóveda

Decíselo a la IA y dale acceso tanto al kit como a la carpeta de tu bóveda. Aclará cuál es el destino. El asistente debe leer las reglas de ambas carpetas y conservar tus notas y convenciones.

El instalador del kit agrega archivos ausentes, conserva los ajustes de Obsidian y se detiene ante archivos incompatibles. En ese caso, la IA explica la diferencia y propone una integración puntual antes de modificar contenido existente.

## Qué queda preparado

- Reglas para que la IA lea primero el contexto correcto y no mezcle proyectos.
- Una ficha con el objetivo, los datos disponibles y las tareas que hayas elegido.
- Carpetas para material original, borradores y resultados, creadas por el asistente.
- Un Panel con acceso al proyecto y una nota que registra la configuración y cualquier parte pendiente.

El kit sirve para cualquier proyecto. **aprender-python es un ejemplo ficticio**, identificado como tal; tu proyecto se crea con tus respuestas. No hace falta tener datos ni fuentes para empezar: esas secciones pueden quedar vacías.

## Uso diario

Para retomar, podés decir **«Seguí con [nombre del proyecto]»**. La IA debe leer las reglas y la ficha guardada, recuperar lo pendiente y preguntarte solo por los datos que falten. Si ya configuraste la bóveda, no necesita repetir la entrevista inicial.

| Tarea | Pedido en lenguaje común | Claude Code |
|---|---|---|
| Configurar la bóveda | Usá el mensaje de inicio de este README | `/configurar` |
| Retomar | «Seguí con [proyecto]» | `/empezar nombre-corto` |
| Redactar | «Ayudame a escribir [texto] para [proyecto]» | `/redactar nombre-corto qué necesitás` |
| Guardar avances | «Proponé qué actualizar en la ficha»; revisá la propuesta | `/cerrar nombre-corto` |
| Crear otro proyecto | «Quiero organizar otro proyecto» | `/nuevo-proyecto Nombre del proyecto` |
| Revisar fichas | «Revisá las fichas y explicame si falta algo» | `/validar` |

Si la IA tiene acceso a la carpeta, puede leer y guardar ahí. Si trabajás con adjuntos, dale las reglas y la ficha vigente del proyecto; los adjuntos son copias. Los [mensajes para otras IAs](DOCS/usar-con-otras-ias.md) detallan cada tarea.

`/cerrar` y `/nuevo-proyecto` se invocan manualmente en Claude Code. El kit pide revisar la propuesta antes de guardar un cierre. Las escrituras y permisos dependen del asistente y su configuración.

## Dónde está cada cosa

| Lugar | Para qué sirve |
|---|---|
| `00_CORE/atoms/` | Reglas compartidas por todos los proyectos |
| `00_CORE/cells/` | Una ficha o **célula** por proyecto: hechos, decisiones y acciones |
| `00_CORE/configuracion.md` | Estado y preferencias acordadas; la IA crea esta nota al configurar |
| `PROJECT_TEMPLATE/` | Modelo que la IA usa para crear las carpetas de cada proyecto |
| `Panel.md` | Acceso a proyectos y tareas pendientes |
| `.claude/skills/` | Instrucciones que Claude Code carga cuando las necesitás |
| `.obsidian/` | Ajustes para la bóveda nueva: Plantillas, Bases y búsqueda |
| `DOCS/` | Guía rápida, solución de problemas y uso con otras IAs |

Una **ficha** o **célula** es una nota corta que conserva el estado del proyecto. La IA elige el tipo de comunicación y completa sus propiedades según lo que le cuentes.

Las carpetas con punto pueden estar ocultas en macOS/Linux. En Finder se muestran con `Cmd + Shift + .`. En Windows, el punto por sí solo no las oculta; si tienen el atributo oculto, activá Ver → Mostrar → Elementos ocultos. Para abrir el ZIP como bóveda no necesitás manipularlas.

## Ayuda opcional y herramientas

- [Tu primer proyecto a mano](DOCS/primer-proyecto.md), si preferís configurarlo vos.
- [Instalación manual](DOCS/instalacion-manual.md), para una bóveda existente.
- [Plantillas y panel](DOCS/obsidian.md), para revisar esas funciones en Obsidian.
- [Solución de problemas](DOCS/TROUBLESHOOTING.md).

La IA puede crear los archivos con sus propias herramientas. Si dispone de Python, el kit también incluye `instalar.py`, `crear_proyecto.py` y un validador, todos con la biblioteca estándar. No necesitás ejecutar comandos para seguir el inicio conversacional. La [guía de creación para asistentes](DOCS/creacion-para-asistentes.md) explica la herramienta opcional.

Para revisar el formato de las fichas desde la carpeta del kit:

```sh
python 00_CORE/schemas/validate.py
```

El validador comprueba formato y campos, **no la veracidad de las fuentes**. Los avisos por hechos o tareas vacíos no impiden preparar la bóveda: la información puede completarse después. La visualización del Panel se comprueba por separado en Obsidian.

Para contribuir: [CONTRIBUTING](CONTRIBUTING.md).

## Privacidad

El kit guarda archivos locales y no instala servicios de sincronización. Cuando adjuntás notas a una IA o le das acceso a la carpeta, ese servicio puede procesarlas según su configuración. Compartí solo el contexto que necesite la tarea.

## English

An AI-guided Obsidian starter kit for study, work or personal projects. Unzip it and give the folder to an assistant that can read and write files. Ask it to read `00_CORE/atoms/00_vault-rules.md` first, then `AI-INSTRUCTIONS.md`. Answer one or two simple questions at a time; the assistant prepares your vault and first project. No coding or template editing is required. Open the prepared folder in Obsidian when setup is complete. Ask the assistant to resume your project using its saved context note. Documentation and templates are in Spanish. The optional installer preserves existing notes and Obsidian settings and stops on conflicts. A chat that only accepts attachments needs to return a downloadable configured copy; it cannot edit your local folder through an attachment alone.

## Licencia y créditos

[MIT](LICENSE). Trabajo derivado e independiente del repositorio [Context Engineering](https://github.com/davidkimai/Context-Engineering) de **davidkimai** (© 2025 davidkimai). Este kit no está afiliado ni respaldado por el proyecto original.
