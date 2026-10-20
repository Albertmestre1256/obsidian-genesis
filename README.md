> **Crédito principal a [davidkimai](https://github.com/davidkimai):** este kit se basa en su trabajo [Context Engineering](https://github.com/davidkimai/Context-Engineering). Obsidian Genesis adapta ese trabajo para iniciar y organizar bóvedas de Obsidian con ayuda de una IA.
> [!info]- Índice de esta nota (líneas)
> - Líneas 1–1: Atribución
> - Líneas 2–17: Este índice
> - Líneas 19–20: Introducción
> - Líneas 21–28: Obsidian Genesis: tu bóveda, configurada por una IA
> - Líneas 29–52: Estado del proyecto — 20/10/2026
> - Líneas 53–73: Empezar en tres pasos
> - Líneas 74–79: Adjuntos o bóveda existente
> - Líneas 80–87: Continuar
> - Líneas 88–102: Qué contiene
> - Líneas 103–111: Ayuda opcional
> - Líneas 112–115: Privacidad
> - Líneas 116–119: Licencia
> - Líneas 120–123: Comunidad y soporte
> - Líneas 124–127: Sobre el desarrollo
> - Líneas 128–130: Apoyar el proyecto

**Idioma:** Español · [English](README.en.md) · [Deutsch](README.de.md) · [中文](README.zh.md)

# Obsidian Genesis: tu bóveda, configurada por una IA

Descargá el kit, dale la carpeta a una IA y respondé sus preguntas. El asistente prepara tus notas y tu primer proyecto usando las reglas del kit. No necesitás programar ni conocer Obsidian.

Una **bóveda** es una carpeta de notas que abrís con [Obsidian](https://obsidian.md). El kit está en español y sirve para estudio, trabajo o cualquier proyecto personal.

La entrada [Leer primero](LEER_PRIMERO.md) conecta el Panel y el índice general. En una bóveda nueva, el kit activa la **Vista de gráfico** de Obsidian: abrila desde su icono lateral para explorar las notas conectadas, o usá el gráfico local desde el índice de un proyecto.

## Estado del proyecto — 20/10/2026

**Código publicado en `main` (`c69c38a`); todavía no es una release estable.** El foco sigue siendo iniciar una bóveda con preguntas simples, sin pedirle a la persona que programe ni mantenga los índices.

| Ya implementado | Qué permite |
|---|---|
| Configuración conversacional | Guardar respuestas antes del primer proyecto y retomar lo que quedó pendiente. |
| Perfil opcional y reanudable | Mantener un único inventario plegable; conservar datos omitidos y completar solo lo que la persona elija. |
| Nodos e índices conectados | Cada colección enlaza su padre, hijos y notas; los nodos generales enlazan el mapa y Leer primero. Los proyectos nuevos tienen índices con nombres propios. |
| Mantenimiento y cierre | Identificar al asistente, registrar cambios con historial conservado y comprobar fichas, Panel, perfil, mapas, rangos y coherencia del proyecto inicial. |
| Accesos para distintas IA | Guías para Claude Code, OpenCode, ChatGPT y otros asistentes con herramientas de archivos; alternativa manual disponible. |

El creador vuelve a comprobar el estado antes de guardar un proyecto y distingue los bloqueos previos de los fallos parciales; cada archivo se crea sin reemplazar uno existente.

La vista simple despeja el explorador y el gráfico en carpetas nuevas y puede activarse opcionalmente en bóvedas existentes con respaldo. Conserva preferencias y búsqueda propia; informa si el filtro del kit queda pendiente.

La [matriz remota del código `c69c38a`](https://github.com/Albertmestre1256/obsidian-genesis/actions/runs/39375866749) terminó **6/6 correcta** en Windows, macOS y Ubuntu con Python 3.8 y 3.13. Son resultados técnicos; no acreditan facilidad de uso.

Se comprobaron configuración y reanudación con Claude Code. El ensayo manual OpenCode/Big Pickle mostró uso continuado en una misma sesión, sin acreditar reanudación independiente. Un chat nuevo de Codex retomó una copia anterior y conservó las omisiones, con contexto y herramientas externos. No son pruebas con principiantes reales ni validan la interfaz de todos los cambios actuales.

Faltan la reanudación independiente en OpenCode, la cobertura específica de ChatGPT web, una prueba con cinco principiantes (al menos cuatro sin ayuda) y la revisión visual formal final en Obsidian.

Las discusiones de la comunidad están disponibles y podés apoyar el proyecto en [Patreon](https://www.patreon.com/obsidiangenesis). El README y la guía de documentos están en español, inglés, alemán y chino; las instrucciones comunes del kit siguen en español. La adaptación y optimización general de bóvedas existentes será una fase posterior. [Historial de cambios](CHANGELOG.md) · [Cómo contribuir](CONTRIBUTING.md).

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

Un ZIP adjunto no da acceso a tu computadora. Si el chat genera archivos, puede devolverte una copia configurada para descargar. Si solo responde texto, queda pendiente guardarlo. La [guía de acceso](DOCS/QUICKSTART.md) explica las opciones.

Si ya tenés una bóveda, la integración actual es conservadora: la IA lee sus reglas, compara conflictos y conserva notas y ajustes. Reorganizar u optimizar automáticamente toda una bóveda existente todavía no está implementado; es la fase posterior mencionada arriba.

## Continuar

Decí **«Seguí con [proyecto]»**. La IA lee primero el índice, después las reglas y la ficha vigente, y retoma lo pendiente. Podés pedir otro proyecto, un borrador, una revisión o guardar el cierre: [pedidos de uso diario](DOCS/usar-con-otras-ias.md).

Para organizar más contenido, pedí **«Agregá un nodo para resúmenes de mis materias»**. Cada nodo tiene un índice con enlaces y resúmenes; el mapa general conecta todos los nodos y la IA los mantiene al agregar notas. Los índices previos se conservan; cambiar su nombre o reorganizar notas requiere un alcance acordado. [Guía](DOCS/indice-principal.md).

Claude Code y OpenCode incluyen `/configurar`, `/empezar`, `/nuevo-proyecto`, `/redactar`, `/validar` y `/cerrar`. En Claude, crear otro proyecto y cerrar son de invocación manual. Los permisos dependen del asistente. Con adjuntos, compartí siempre las notas vigentes: no están sincronizadas.

## Qué contiene

Para conocer la función de cada archivo y cuándo consultarlo, abrí la [guía de documentos y herramientas](DOCS/README.md).

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

## Comunidad y soporte

Para dudas, ideas y experiencias, usá las [discusiones de la comunidad](https://github.com/Albertmestre1256/obsidian-genesis/discussions). Si algo falla, abrí un [reporte de error](https://github.com/Albertmestre1256/obsidian-genesis/issues) con la plantilla «No me funciona» y un ejemplo ficticio pequeño. [Cómo contribuir](CONTRIBUTING.md).

## Sobre el desarrollo

Albert Mestre desarrolla esta adaptación con contribuciones importantes de **OpenCode, Claude y Codex (OpenAI)**, que ayudaron a construir una parte sustancial del código y apoyaron la documentación y las pruebas. Se los reconoce aquí como herramientas de IA contribuidoras al proyecto. Las propuestas se revisan y los resultados se verifican antes de integrarlos; el uso de IA no sustituye las pruebas con personas ni acredita por sí solo que el kit sea fácil de usar.

## Apoyar el proyecto

Obsidian Genesis es gratuito y lo seguirá siendo. Si te resulta útil, podés apoyarlo en [Patreon](https://www.patreon.com/obsidiangenesis). Los aportes ayudan a dedicar tiempo a guías para principiantes, pruebas con personas reales, traducciones y soporte. Son opcionales: no desbloquean funciones y todo el kit sigue siendo público.
