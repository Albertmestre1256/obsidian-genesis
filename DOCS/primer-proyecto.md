# Tu primer proyecto a mano

Esta es la alternativa manual. El recorrido principal consiste en [darle la carpeta a una IA para que la configure con tus respuestas](empezar-con-ia.md).

Una **bóveda** es la carpeta donde Obsidian guarda tus notas. Una **ficha de proyecto** responde: qué quiero hacer, qué sé y qué sigue. En algunos archivos se llama «célula»: es lo mismo.

Al terminar tendrás una ficha propia y una primera tarea. Podés hacerlo sin IA ni Python. No hace falta aprender programación.

## 1. Elegí algo pequeño

Por ejemplo, organizar una mudanza, estudiar un tema o preparar un viaje. Usá un proyecto tuyo; aprender-python es un ejemplo ficticio.

Elegí un nombre corto, como `mi-primer-proyecto`. Usá minúsculas y guiones en lugar de espacios. Revisá las fichas de `00_CORE/cells/`: si ese nombre ya aparece en la propiedad `proyecto`, abrí esa ficha para continuar. Para uno distinto, elegí otro nombre.

## 2. Creá una ficha vacía

En el listado de archivos de Obsidian, desplegá `00_CORE` y después `cells`. Creá una nota nueva dentro de `cells` y llamala `mi-primer-proyecto-context`. Obsidian guarda la nota como archivo `.md`; no necesitás escribir esa extensión en el título.

El final `-context` permite que el Panel encuentre tu ficha. Si ese archivo ya existe, abrilo o elegí otro nombre; no reemplaces su contenido.

## 3. Insertá la plantilla

Con la nota vacía abierta, abrí la paleta de comandos (`Ctrl + P` en Windows/Linux o `Cmd + P` en Mac), buscá **Plantillas: Insertar plantilla** y elegí **TEMPLATE_cell**.

La plantilla agrega las propiedades y secciones; la fecha se completa al insertarla. Hacelo una sola vez. Si no aparece el comando o la plantilla, seguí [Configurar Plantillas](obsidian.md) y volvé a este paso.

## 4. Completá la ficha

En las propiedades de arriba, reemplazá los textos entre corchetes:

| Campo | Qué poner |
|---|---|
| `tipo` | Dejá `celula` |
| `proyecto` | El nombre corto que elegiste, por ejemplo `mi-primer-proyecto` |
| `descripcion` | Una frase sobre lo que vas a hacer |
| `objetivo` | Qué resultado querés conseguir; agregá una fecha si ya la decidiste |
| `contexto` | A para trabajo técnico; B para relatos o cartas personales; C para propuestas; D para organizar y coordinar |
| `actualizado` | La fecha que completó la plantilla |

Si empezás organizando tareas, podés usar D y cambiarlo más adelante.

Debajo de las propiedades:

- **Hechos clave:** anotá lo que ya sabés y de dónde sale. Una decisión personal puede citarse como `(fuente: mi decisión de hoy)`; un dato externo necesita su documento o referencia. Si no tenés datos todavía, dejá la sección vacía. Quitá el texto de ejemplo de tu copia.
- **Próximas acciones:** reemplazá la tarea de ejemplo por algo que puedas hacer a continuación. Por ejemplo, `- [ ] Anotar los tres temas que quiero estudiar`.
- **Decisiones y Preguntas abiertas:** completalas si las necesitás; pueden quedar vacías.

## 5. Comprobá que podés retomarlo

Abrí otra nota y volvé a tu ficha desde `00_CORE/cells/`. ¿Podés entender qué querés hacer y cuál es el próximo paso? Si sí, ya tenés lo necesario para empezar.

Abrí [Panel](../Panel.md): tu ficha debería aparecer en la tabla y tu tarea en las acciones pendientes. Si la tabla no aparece, podés seguir abriendo la ficha desde el listado de archivos; consultá [la ayuda del panel](obsidian.md) cuando quieras resolverlo.

## 6. Usá una IA si te sirve

Adjuntá al chat las reglas (`00_CORE/atoms/00_vault-rules.md`) y tu ficha, desde la carpeta de tu bóveda. Pegá:

> Leé las reglas y mi ficha. Explicame en lenguaje simple dónde estoy y proponé un próximo paso pequeño. Usá solo mis datos; si falta algo necesario, preguntámelo. Por ahora respondé en el chat, sin modificar archivos.

Al terminar, pedile que proponga qué actualizar. Revisalo y copiá los cambios a tu ficha en Obsidian. La próxima vez adjuntá esa versión: el chat no actualiza tu carpeta por recibir un archivo.

## Cuando el proyecto crezca

Mientras solo tengas la ficha, podés trabajar desde ella. Cuando tengas documentos o borradores, copiá `PROJECT_TEMPLATE/` desde el explorador de archivos de tu sistema, poné a la copia el nombre corto del proyecto y completá su índice. No reemplaces una carpeta existente.

La carpeta del proyecto va al lado de `00_CORE/`. Guardá originales en `01_FUENTES/`, notas y borradores en `02_SINTESIS/`, versiones finales en `03_ENTREGABLES/`. En el índice, cambiá el enlace de ejemplo por el nombre de tu ficha: `[[mi-primer-proyecto-context]]`.

Seguí con [los pedidos para trabajar con una IA](usar-con-otras-ias.md) cuando necesites redactar o guardar avances. Las configuraciones avanzadas son opcionales.

Referencia del comando y la fecha automática: [Plantillas de Obsidian](https://obsidian.md/help/plugins/templates). Esta guía aún está pendiente de la prueba visual y con principiantes.
