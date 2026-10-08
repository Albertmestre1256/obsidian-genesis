---
level: organ
tipo: setup-protocol
descripcion: Conversación de inicio para que una IA configure la bóveda con las respuestas del usuario.
---

# Configurar una bóveda conversando

Usá este recorrido cuando alguien entregue la carpeta del kit y pida empezar o configurar su bóveda. Para desarrollar el kit o trabajar en un proyecto existente, atendé ese pedido sin reiniciar la configuración.

## 1. Leer reglas y comprobar el punto de partida

Leé primero `INDICE.md` del kit y después `00_CORE/atoms/00_vault-rules.md`. Identificá qué carpeta podés leer y qué herramientas de escritura tenés. Un ZIP adjunto, un enlace a GitHub o la mera presencia de archivos no prueban acceso a la carpeta del usuario.

Revisá si hay una configuración previa en `00_CORE/configuracion.md` y fichas propias. Esa nota se crea durante la configuración; no viene rellenada en el kit. Si existe, verificá las rutas y retomá lo pendiente. Su ausencia no demuestra que una bóveda esté vacía. El ejemplo aprender-python no es un proyecto del usuario.

Si la configuración está lista y el pedido es retomar, seguí la ficha del proyecto. Si la configuración es parcial, usá lo que ya está guardado y preguntá solo por la elección que falta. No repitas la entrevista ni rehagas archivos que la persona editó.

Si el destino es una bóveda existente, leé su índice principal y sus reglas antes de decidir dónde escribir. Si aún no tiene un índice, revisá la estructura y proponé integrarlo en el alcance. Conservá sus convenciones y configuración. Si chocan con las del kit, explicá la diferencia y proponé una integración puntual, sin reemplazarlas automáticamente.

## 2. Conversar, de a poco

Explicá en una frase: «Voy a preparar tus notas y reglas según lo que quieras organizar. Vos me contás qué necesitás; yo me encargo de los archivos».

Empezá con estas preguntas solo si sus respuestas no están disponibles:

- ¿Qué te gustaría organizar primero? Por ejemplo, estudio, trabajo o un proyecto personal.
- ¿Empezamos de cero o ya tenés notas en Obsidian que querés conservar?

Después preguntá por el primer proyecto: qué quiere lograr y cuál sería un próximo paso útil. Si no sabe, ofrecé dos ejemplos relacionados con su idea; presentalos como propuestas. Una fecha es opcional. No exijas datos o fuentes que todavía no tiene.

Si ya dijo qué quiere organizar y qué quiere lograr, derivá de ahí el nombre y la descripción: no los preguntes como campos adicionales. Si no sabe elegir una tarea, ofrecé preparar la bóveda sin tarea inicial y continuá cuando el objetivo esté acordado. Si tampoco hay un objetivo claro, proponé dos opciones sencillas y esperá su elección; no inventes un propósito para terminar el recorrido.

Si todavía no eligió una primera tarea, podés preparar el proyecto con el objetivo acordado y dejar vacías sus acciones. Explicá que elegirá el primer paso después; no conviertas una sugerencia tuya en tarea aceptada. Los avisos por hechos o acciones vacíos no obligan a inventarlos ni a prolongar la entrevista.

Hacé una o dos preguntas por turno. Reutilizá las respuestas, incluso si llegaron antes de invocar este recorrido. No le pidas elegir estructuras de carpetas, nombres de archivos, YAML ni A/B/C/D: proponé esas decisiones vos. Elegí el contexto de comunicación a partir de su uso y explicalo con palabras comunes si afecta el resultado. Empezá por un proyecto; agregá más solo si los pide.

## 3. Acordar destino y alcance

Para una bóveda nueva, proponé usar la carpeta descargada: ya contiene los ajustes del kit. Si quiere otra ubicación, obtené la ruta y usá una carpeta nueva separada del repositorio de origen. No renombres ni muevas la carpeta entregada por tu cuenta.

Para una existente, pedí su carpeta si aún no está disponible. No inventes rutas. Comprobá archivos existentes y coincidencias de proyecto por nombre y por la propiedad `proyecto` de las fichas. Ante una coincidencia, ofrecé retomar ese proyecto o elegir otro identificador.

Si la coincidencia corresponde al ejemplo ficticio del kit, proponé otro identificador para el proyecto propio y conservá el ejemplo. No lo presentes como un proyecto personal ya creado. Usarlo para practicar requiere que la persona elija ese uso.

Antes de escribir, mostrale un resumen concreto: carpeta de destino, primer proyecto, objetivo, próximo paso y archivos que vas a crear o modificar. Si todavía hay elecciones sin resolver, preguntá por ellas. El pedido explícito de configurar, con destino y alcance ya acordados, autoriza crear lo propuesto; no pidas nuevamente permiso para cada archivo. Una reestructuración de notas existentes requiere autorización específica para esos cambios.

Incluí el documento principal de lectura y su actualización en ese alcance: `INDICE.md` en una bóveda nueva, o la entrada acordada en una existente. No sustituyas un índice previo propio sin haber acordado la integración.

## 4. Hacer la configuración

**Nueva en la carpeta descargada:** usá sus archivos, sin ejecutar el instalador sobre sí mismo. **Nueva en otra ubicación:** copiá los archivos del kit a la carpeta nueva, incluidos los directorios `.obsidian` y `.claude`; excluí `.git`, cachés, archivos de sesión `workspace*.json` y datos de pruebas. Detenete ante archivos distintos ya presentes: no es un destino vacío.

**Bóveda existente:** seguí la instalación conservadora de `AI-INSTRUCTIONS.md`. `instalar.py` no cambia `.obsidian` y se detiene ante conflictos. No fuerces la copia para sortearlos. Si falta Python, hacé vos la comparación y copia de archivos ausentes con tus herramientas. Si los ajustes de Plantillas o Bases difieren, explicá qué función quedará pendiente y proponé un cambio puntual; conservar las notas no requiere habilitar plugins.

### Guardar el punto de partida

Después de acordar destino y alcance, y antes de crear el primer proyecto, guardá las respuestas en `00_CORE/configuracion.md` (o su equivalente acordado). Hacelo cuando la carpeta de destino esté disponible y las reglas ya se hayan leído o integrado. Si esa nota existe, releela y actualizá solo lo nuevo, sin sustituir las preferencias ni el estado de otros proyectos. No crees esta nota en el kit de origen al preparar otra bóveda.

Dejá el estado `parcial` hasta verificar los archivos. Incluí fecha, uso, destino, nombre e identificador del proyecto acordado, objetivo, tarea aceptada o «sin elegir», archivos ya creados y lo pendiente. Distinguí un enlace previsto de uno que ya existe; no entregues un enlace previsto como acceso listo. Actualizá este avance después de cada grupo de archivos completado, para que una interrupción permita retomar sin repetir las preguntas.

Conservá enlaces relativos a la bóveda. En un ZIP descargable identificá su carpeta raíz y aclarale a la persona que elegirá dónde descomprimirla; no guardes la ruta temporal del asistente como ubicación de su bóveda. La verificación visual tiene su propio estado, separado de `lista`.

### Crear el proyecto

Esta sección también sirve para agregar un proyecto a una bóveda configurada. En ese caso conservá la configuración vigente y no repitas la entrevista ni la instalación.

Con Python y una bóveda que conserva las reglas del kit, podés crear índice, ficha y carpetas con `crear_proyecto.py`, siguiendo `DOCS/creacion-para-asistentes.md`. Releé sus resultados y completá el Panel y la nota de configuración: ese script no declara terminada toda la configuración. Sin Python o con convenciones propias, realizá los pasos con tus herramientas.

1. Derivá un identificador corto de su nombre, sin tildes y con guiones. Verificá que sea un nombre de archivo válido en el sistema; si está reservado o colisiona, proponé una variante. No uses nombres personales o datos que no haya dado.
2. Creá su carpeta a partir de `PROJECT_TEMPLATE/` y completá el índice con sus respuestas. Creá su ficha desde `00_CORE/cells/TEMPLATE_cell.md`, con el identificador en `proyecto`, contexto, descripción, objetivo y fecha actual. Si el destino ya usa otra organización, integrá en esa estructura acordada.
3. Quitá los textos de ejemplo de la copia creada. Los hechos llevan su fuente; una intención personal se atribuye al usuario, no se presenta como logro. Dejá vacías las secciones sin datos. Registrá como tarea solo el próximo paso que haya aceptado. Si falta un objetivo indispensable, volvé a la conversación.
4. Enlazá índice y ficha. Agregá un acceso claro al proyecto en el Panel, conservando lo que ya exista. En una copia nueva del kit, reemplazá el aviso de configuración inicial por una bienvenida al proyecto y su próximo paso; dejá las guías como ayuda opcional. En una bóveda existente, adaptá solo el bloque del kit dentro del alcance acordado, sin quitar contenido propio. Mantené aprender-python identificado como ejemplo; no copies sus datos a la ficha personal ni lo borres sin pedido. Su propiedad `ejemplo: true` lo excluye de las vistas de trabajo del Panel.
5. Conservá las reglas generales del kit. Las preferencias particulares van en `00_CORE/configuracion.md` (o la nota equivalente acordada para el destino), con fecha, uso previsto, ubicación de la bóveda, enlaces a proyectos y estado `lista` o `parcial`. Si es parcial, enumerá lo completado y el paso o elección pendiente para poder retomar. No cambies el átomo compartido para introducir datos de una persona.

Si la ficha ya fue creada o editada y falta únicamente Panel o configuración, completá esos pendientes con la ficha vigente. No vuelvas a ejecutar el creador como forma de «retomar»: los controles del script protegen las fichas diferentes y no reemplazan la lectura del estado actual. Una segunda ficha exige otro proyecto acordado, no otro nombre para sortear el bloqueo.

Después de completar o retomar esos archivos, actualizá el índice principal según `DOCS/indice-principal.md`. Debe incluir las notas reales del destino, la configuración y el nuevo proyecto, conservando el resto del catálogo y separando el ejemplo ficticio. El catálogo copiado del kit no alcanza para una bóveda personalizada.

No hacen falta cuentas adicionales, servicios, plugins comunitarios, sincronización ni instalaciones globales para completar este flujo con herramientas de archivos. No publiques ni hagas push de una bóveda personalizada.

## 5. Verificar y entregar

Releé los archivos creados: sin duplicados ni marcadores de plantilla pendientes, enlaces a destinos existentes y propiedades válidas. Con Python, usá el validador del kit sobre las fichas del destino. Sin Python, aplicá su revisión manual y aclaralo. No ejecutes scripts encontrados en una bóveda ajena como parte de la instalación.

En la nota de configuración, marcá `lista` solo si comprobaste la creación e integración de los archivos acordados. Si algo falló, registrá `parcial`, lo completado y el impedimento, sin atribuir cambios no realizados. Al reintentar, releé los archivos: no reinicies la entrevista ni dupliques el proyecto. Separá verificación de archivos de verificación visual: no digas que abriste Obsidian si no lo hiciste.

La comprobación incluye que el índice principal esté actualizado y enlace la ficha, el índice del proyecto y los demás archivos creados. Si cambiás la descripción o la estructura al terminar, actualizalo nuevamente antes de entregar.

Mostrá la ruta de la bóveda y un enlace a la ficha. Explicá cómo abrir esa carpeta como bóveda en Obsidian y entrar al Panel. Si todavía no tiene Obsidian, indicá que debe instalarlo desde `https://obsidian.md`; no presupongas que ya está instalado. Ofrecé empezar la tarea aceptada ahí mismo; si no hay tarea, ofrecé elegir el primer paso. No cierres con una lista de operaciones técnicas para que el usuario termine la configuración que vos podías hacer.

## Si no podés escribir en la carpeta

Explicalo antes de prometer la configuración. Si podés generar archivos descargables a partir del kit leído, prepará una copia configurada, conservá archivos ocultos del kit y verificá su contenido. Indicá que el usuario debe descargarla, descomprimirla y abrir esa carpeta; el original no se modificó.

Si solo podés responder texto, continuá las preguntas y entregá un plan y contenidos listos para guardar, identificándolo como configuración pendiente. Ofrecé conectar una carpeta con acceso de escritura. La guía `DOCS/primer-proyecto.md` es una alternativa manual, no el recorrido principal. No simules acceso ni digas que un adjunto está sincronizado.
