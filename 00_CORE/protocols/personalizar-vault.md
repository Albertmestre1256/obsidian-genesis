---
level: organ
tipo: personalizacion-protocol
descripcion: Inventario de datos aportados, pendientes u omitidos para personalizar y completar la bóveda sin repetir la entrevista.
---
> [!info]- Índice de esta nota (líneas)
> - Líneas 1–5: Propiedades
> - Líneas 6–13: Este índice
> - Líneas 15–18: Personalizar la bóveda y retomar lo que falta
> - Líneas 19–42: Qué conocer
> - Líneas 43–66: Inventario persistente
> - Líneas 67–74: Conservar documentos aportados
> - Líneas 75–83: Preguntar, omitir y volver

# Personalizar la bóveda y retomar lo que falta

Guía común para [configurar](configurar-vault.md) o completar después el perfil. Leé primero el índice y las reglas. Usá esta lista para recordar datos; preguntá solo lo pertinente, de a una o dos preguntas. CV, escolaridad y presentación son opcionales.

## Qué conocer

Conservá estos identificadores. `boveda` es información compartida; los ítems de proyecto se registran para cada proyecto propio, sin copiar perfiles entre ellos.

| Ítem | Alcance | Necesidad | Qué registrar o preguntar |
|---|---|---|---|
| `uso` | boveda | Para iniciar | Qué quiere organizar y para qué. |
| `destino` | boveda | Para iniciar | Carpeta acordada y acceso comprobado, o entrega de copia. |
| `conservacion` | boveda | Para iniciar | Inicio de cero o notas y reglas que conservar. |
| `objetivo` | proyecto | Para iniciar | Qué quiere conseguir; derivar nombre e identificador. |
| `presentacion` | boveda | Opcional | Contexto personal o profesional pertinente; sin exigir nombre legal. |
| `documento-perfil` | boveda | Opcional | CV, documento o resumen que quiera compartir. |
| `formacion` | proyecto | Opcional | Escolaridad, carrera, cursos o bases pertinentes; sin exigir títulos. |
| `experiencia` | proyecto | Opcional | Qué sabe y qué quiere aprender. |
| `alcance` | boveda | Opcional | Un proyecto, varios o áreas de su vida. |
| `vida-util` | boveda | Opcional | Uso temporal o continuo; qué conservar al terminar proyectos. |
| `materiales` | proyecto | Opcional | Apuntes, referencias o archivos; «no tengo» resuelve el ítem. |
| `rutina` | boveda | Opcional | Cómo consultar, agregar y revisar notas. |
| `preferencias` | boveda | Opcional | Idioma, detalle, forma de trabajar y datos que no guardar o compartir. |
| `plazo` | proyecto | Opcional | Fecha o disponibilidad; «sin fecha» resuelve el ítem. |
| `primer-paso` | proyecto | Opcional | Acción que el usuario eligió para empezar; distinguirla de una sugerencia y de un pedido puntual ya atendido, que se marca hecho (`- [x]`) en «Próximas acciones» de la ficha. |

Si una tarea necesita un dato opcional, explicá por qué y preguntalo; su ausencia no invalida la configuración básica.

## Inventario persistente

Antes de crear el primer proyecto, guardá **Inventario de personalización** en `00_CORE/configuracion.md`. Esa es la única lista de estados; las fichas contienen el trabajo de cada proyecto. Enlazá detalles y fuentes existentes en lugar de copiar un CV al contexto habitual. El kit público no lleva datos personales rellenados.

La tabla usa estas columnas: **Ítem | Alcance | Estado | Dato o referencia | Origen y fecha | Para retomar**. Alcance es `boveda` o `proyecto:identificador-real`; dato es un resumen o enlace relativo; origen distingue usuario, documento, comprobación o IA, con fecha real. Para retomar indica una pregunta o comprobación. Usá `—` cuando no corresponda contenido.

Una fila por ítem y alcance, en una línea y con barras verticales escapadas. En notas nuevas, la plantilla deja la tabla en un bloque plegable «Respuestas y pendientes para retomar», debajo de los datos iniciales y del avance. Conservá el prefijo `>` de sus filas al editarla. Una tabla plana existente sigue siendo válida; no copies el inventario ni conviertas un perfil anterior solo por su presentación. Incluí todos los ítems aplicables y agregá otros solo si afectan el uso. Conservá lo sabido de respuestas parciales y señalá la duda. [La plantilla de configuración](../templates/TEMPLATE_configuracion.md) aporta esa estructura para una nota nueva; al retomar, editá la versión vigente sin sustituir sus datos ni repetir el inventario en la ficha.

| Estado | Significado |
|---|---|
| `confirmado` | Respuesta inequívoca del usuario o comprobación de archivos, atribuida a su origen. |
| `pendiente` | Sin preguntar, sin responder o ambiguo. |
| `omitido` | Elección de saltarlo; indicar «más adelante» o «prefiero no compartir». |
| `propuesto` | Sugerencia o inferencia de la IA, incluso delegada; falta adoptar ese valor. |
| `no-aplica` | El usuario indicó que no corresponde o no existe; guardar el motivo. |

Estados independientes:

- `estado: parcial/lista`: archivos e integración verificados.
- `personalizacion: abierta/completa`: abierta si quedan filas `pendiente` o `propuesto`; las omisiones explícitas permiten completa, sin exigir un perfil exhaustivo.
- `verificacion_visual`: prueba en Obsidian, independiente del inventario.

Una bóveda puede estar `lista` con personalización `abierta`. Recalculá el estado al guardar respuestas y enlazá esta sección desde el Panel, sin duplicar la tabla.

## Conservar documentos aportados

Si el usuario pide incorporar un CV, apuntes u otro documento, conservá primero el original en `01_FUENTES/` del nodo acordado. Si ya existe allí, enlazalo sin duplicarlo ni sustituirlo; una versión distinta se agrega con otro nombre, sin pisar la anterior. Respetá el alcance y los datos que pidió no guardar. Si el destino no está claro, acordalo antes de escribir.

Para un adjunto, conservá sus bytes sin alterarlos. Para texto pegado, creá una fuente con transcripción fiel y distinguí sus metadatos del contenido aportado. Después, el inventario enlaza esa fuente; la ficha guarda solo el contexto pertinente y su referencia. Un resumen no reemplaza al documento original ni convierte lo declarado en un hecho verificado. Conservá explícitamente si el material es ficticio o una propuesta de la IA.

Si solo aporta una URL y no podés leerla, guardá la referencia como contenido pendiente de capturar, sin afirmar que conservaste o analizaste el artículo. Una exportación de conversación también es un original: seguí [Mantenimiento](../../DOCS/mantenimiento.md) sin reescribir la transcripción.

## Preguntar, omitir y volver

1. Leé configuración y ficha vigentes; reutilizá respuestas y excluí ejemplos ficticios. Un «sí» ambiguo sigue pendiente.
2. «Saltá esta parte» omite solo los ítems de esa pregunta. «Rellenalo vos» permite propuestas con motivo y origen IA; nunca inventar CV, formación ni experiencia. Con los requisitos básicos resueltos, prepará la bóveda.
3. Continuar un proyecto no reinicia la personalización ni bloquea tareas independientes de los pendientes.
4. «Qué falta» consulta pendientes, propuestas y omisiones sin escribir. «Completemos mi perfil» retoma las preguntas pertinentes; las omisiones no se preguntan cada sesión y las de privacidad se completan solo si el usuario lo elige.
5. Antes de guardar, leé [Mantenimiento](../../DOCS/mantenimiento.md), releé la versión actual y cambiá solo filas respondidas y datos afectados de la ficha. Conservá preferencias y otros proyectos; comprobá referencias, fecha, origen e índice y explicá lo pendiente.

Si falta el inventario en una configuración existente, agregalo desde sus datos dentro del pedido de completarla, conservando documento y convenciones. No reinstales ni recrees proyectos. Sin escritura, entregá filas y destino como pendientes.
