> **Crédito principal a [davidkimai](https://github.com/davidkimai):** este kit se basa en su trabajo [Context Engineering](https://github.com/davidkimai/Context-Engineering). Obsidian Genesis adapta ese trabajo para iniciar y organizar bóvedas de Obsidian con ayuda de una IA.
> [!info]- Índice de esta nota (líneas)
> - Líneas 1–1: Atribución
> - Líneas 2–15: Este índice
> - Líneas 17–18: Introducción
> - Líneas 19–26: Obsidian Genesis: tu bóveda, configurada por una IA
> - Líneas 27–48: Estado del proyecto — 16/10/2026
> - Líneas 49–69: Empezar en tres pasos
> - Líneas 70–75: Adjuntos o bóveda existente
> - Líneas 76–83: Continuar
> - Líneas 84–96: Qué contiene
> - Líneas 97–105: Ayuda opcional
> - Líneas 106–109: Privacidad
> - Líneas 110–113: Licencia
> - Líneas 114–116: Sobre el desarrollo

**Idioma:** Español · [English](README.en.md) · [Deutsch](README.de.md) · [中文](README.zh.md)

# Obsidian Genesis: tu bóveda, configurada por una IA

Descargá el kit, dale la carpeta a una IA y respondé sus preguntas. El asistente prepara tus notas y tu primer proyecto usando las reglas del kit. No necesitás programar ni conocer Obsidian.

Una **bóveda** es una carpeta de notas que abrís con [Obsidian](https://obsidian.md). El kit está en español y sirve para estudio, trabajo o cualquier proyecto personal.

La entrada [Leer primero](LEER_PRIMERO.md) conecta el Panel y el índice general. En una bóveda nueva, el kit activa la **Vista de gráfico** de Obsidian: abrila desde su icono lateral para explorar las notas conectadas, o usá el gráfico local desde el índice de un proyecto.

## Estado del proyecto — 16/10/2026

**Candidato local en validación; todavía no es una release estable.** El foco sigue siendo iniciar una bóveda con preguntas simples, sin pedirle a la persona que programe ni mantenga los índices.

| Ya implementado | Qué permite |
|---|---|
| Configuración conversacional | Guardar respuestas antes del primer proyecto y retomar lo que quedó pendiente. |
| Perfil opcional y reanudable | Mantener un único inventario plegable; conservar datos omitidos y completar solo lo que la persona elija. |
| Nodos e índices conectados | Cada colección enlaza su padre, hijos y notas; los nodos generales enlazan el mapa y Leer primero. Los proyectos nuevos tienen índices con nombres propios. |
| Mantenimiento y cierre | Identificar al asistente, registrar cambios con historial conservado y comprobar fichas, Panel, perfil, mapas, rangos y coherencia del proyecto inicial. |
| Accesos para distintas IA | Guías para Claude Code, OpenCode, ChatGPT y otros asistentes con herramientas de archivos; alternativa manual disponible. |

El creador vuelve a comprobar el estado antes de guardar un proyecto y distingue los bloqueos previos de los fallos parciales; cada archivo se crea sin reemplazar uno existente.

El cierre muestra qué carpeta revisó; la guía usa su ruta explícita para distinguir la copia descargada de tu bóveda.

Las últimas pruebas automáticas locales dieron **509 correctas y 1 omitida en cada versión, Python 3.8 y 3.13, en Windows**. En dos conversaciones de prueba con Claude Code y personas ficticias, la IA configuró la bóveda, pasó el cierre comprobado y, al retomar, siguió sin repetir preguntas; en una de ellas lo hizo desde una conversación nueva. Esas pruebas llevaron a dos ajustes, que todavía no se probaron en una conversación: el Panel ya no guarda una copia fija del próximo paso (queda en la ficha del proyecto) y los scripts ya no dejan carpetas técnicas `__pycache__` dentro de la bóveda. No son pruebas con principiantes reales.

Faltan conversaciones completas en OpenCode y ChatGPT, pruebas con principiantes y las comprobaciones visuales restantes de Obsidian. Algunas interacciones ya se observaron en copias anteriores; eso no valida la presentación de todos los cambios actuales. Los cambios locales y la matriz remota de GitHub Actions siguen pendientes de publicación autorizada.

También quedan por preparar Discussions y patrocinio. El README está en español, inglés, alemán y chino; las guías e instrucciones del kit siguen en español. La adaptación y optimización de bóvedas existentes será una fase posterior. [Historial de cambios](CHANGELOG.md) · [Cómo contribuir](CONTRIBUTING.md).

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

También guarda un **inventario de personalización**: lo respondido, lo pendiente y lo que elegiste saltar. En notas nuevas está plegado debajo del proyecto y su avance; se abre cuando querés revisarlo. Presentación, CV, formación, rutina y duración de la bóveda son opcionales. Podés empezar con lo básico y decir después **«qué falta para personalizar mi bóveda»** o **«completemos mi perfil»**. [Cómo funciona](00_CORE/protocols/personalizar-vault.md).

**Recibís:** carpeta preparada, ficha del proyecto, Panel para acceder y explicación para abrirla en Obsidian. La IA verifica los archivos; la prueba visual se hace en Obsidian. Si aún no lo tenés, instalalo desde [obsidian.md](https://obsidian.md), abrí la carpeta preparada como bóveda y entrá a `Panel.md`.

## Adjuntos o bóveda existente

Un ZIP adjunto no da acceso a tu computadora. Si el chat genera archivos, puede devolverte una copia configurada para descargar. Si solo responde texto, queda pendiente guardarlo. La [guía de acceso](DOCS/empezar-con-ia.md) explica las opciones.

Si ya tenés una bóveda, la integración actual es conservadora: la IA lee sus reglas, compara conflictos y conserva notas y ajustes. Reorganizar u optimizar automáticamente toda una bóveda existente todavía no está implementado; es la fase posterior mencionada arriba.

## Continuar

Decí **«Seguí con [proyecto]»**. La IA lee primero el índice, después las reglas y la ficha vigente, y retoma lo pendiente. Podés pedir otro proyecto, un borrador, una revisión o guardar el cierre: [pedidos de uso diario](DOCS/usar-con-otras-ias.md).

Para organizar más contenido, pedí **«Agregá un nodo para resúmenes de mis materias»**. Cada nodo tiene un índice con enlaces y resúmenes; el mapa general conecta todos los nodos y la IA los mantiene al agregar notas. Los índices previos se conservan; cambiar su nombre o reorganizar notas requiere un alcance acordado. [Guía](DOCS/indice-principal.md).

Claude Code y OpenCode incluyen `/configurar`, `/empezar`, `/nuevo-proyecto`, `/redactar`, `/validar` y `/cerrar`. En Claude, crear otro proyecto y cerrar son de invocación manual. Los permisos dependen del asistente. Con adjuntos, compartí siempre las notas vigentes: no están sincronizadas.

## Qué contiene

| Lugar | Uso |
|---|---|
| `INDICE.md` | Primera lectura: catálogo completo de archivos y proyectos |
| `LEER_PRIMERO.md` | Entrada para la persona y conexión central de los nodos generales |
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

## Licencia

[MIT](LICENSE), con los créditos de davidkimai y Albert Mestre. Adaptación independiente de Context Engineering, sin afiliación al proyecto original.

## Sobre el desarrollo

Albert Mestre desarrolla esta adaptación con ayuda de asistentes de IA para programación, documentación y pruebas. Las propuestas se revisan y los resultados se verifican antes de integrarlos; el uso de IA no sustituye las pruebas con personas ni acredita por sí solo que el kit sea fácil de usar.
