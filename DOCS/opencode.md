> [!info] Índice de esta nota (líneas)
> - Líneas 1–7: Este índice
> - Líneas 9–12: Empezar con OpenCode
> - Líneas 13–24: Abrir y configurar
> - Líneas 25–30: Qué recibir
> - Líneas 31–46: Retomar
> - Líneas 47–51: Cómo se integra

# Empezar con OpenCode

OpenCode puede configurar tu bóveda desde la carpeta descargada. El kit ya trae la entrada `AGENTS.md` y el comando `/configurar`; no necesitás escribir código ni modificar su configuración global.

## Abrir y configurar

1. Descomprimí el kit y abrí en OpenCode la carpeta que contiene `README.md`, `INDICE.md` y `AGENTS.md`. Si usás la terminal, abrila en esa carpeta y ejecutá `opencode`.
2. Escribí **`/configurar`**. También podés agregar tu idea, por ejemplo `/configurar quiero organizar mi estudio`.
3. Respondé las preguntas. El asistente debe mostrarte dónde guardará la bóveda y qué creará, conservar tus notas y preparar el primer proyecto.

Si tu versión no muestra el comando, pegá el [mensaje de inicio del README](../README.md). El comando es un acceso al mismo protocolo, no un requisito para usar el kit.

Elegí un modo que permita editar archivos cuando vayas a configurar; si estás en un modo de planificación, el asistente puede preparar la propuesta y necesitar cambiar de modo para guardarla. Los permisos y el proveedor de IA son los que tengas en OpenCode. El kit no cambia tu modelo ni instala servicios.

Si OpenCode todavía no responde porque falta conectar un proveedor o el modelo devuelve un error, resolvé ese acceso en OpenCode antes de configurar la bóveda. Su [guía de conexión](https://opencode.ai/docs/providers/) explica las opciones. El kit ya trae `AGENTS.md`: podés comenzar directamente con `/configurar`, sin ejecutar `/init` para generar otras instrucciones.

## Qué recibir

La carpeta preparada, la ficha de tu proyecto, un acceso desde `Panel.md`, la configuración guardada y `INDICE.md` actualizado. Abrí esa carpeta como bóveda en Obsidian y entrá al Panel. Si todavía no lo instalaste, podés hacerlo desde [obsidian.md](https://obsidian.md).

Para una bóveda existente, indicá su carpeta como destino y permití leerla antes de integrar el kit. Se conservan sus reglas y ajustes; cualquier cambio a notas existentes se acuerda por separado.

## Retomar

Decí «seguí con la configuración» si quedó parcial, o «seguí con [proyecto]» cuando esté lista. Para redactar, crear otro proyecto o guardar el cierre, usá los [pedidos de uso diario](usar-con-otras-ias.md). El asistente debe leer lo guardado, incluso si renombraste una ficha.

También tenés estos accesos. Reemplazá los ejemplos por tu proyecto; podés decir lo mismo en lenguaje común.

| Querés | Pedido en OpenCode |
|---|---|
| Retomar el estudio | `/empezar estudio` |
| Agregar un proyecto | `/nuevo-proyecto aprender huerta` |
| Preparar un texto | `/redactar un correo para mi grupo de estudio` |
| Revisar las fichas | `/validar` |
| Guardar el avance | `/cerrar estudio` |

Si el proyecto no está claro, el asistente debe preguntarte cuál. `/validar` revisa sin cambiar tus fichas; `/cerrar` propone lo nuevo y guarda el plan aprobado. No hace falta aprender todos los comandos para usar la bóveda.

## Cómo se integra

`AGENTS.md` señala el orden de lectura. Los seis archivos de `.opencode/commands/` remiten al protocolo de configuración o a los pedidos de uso diario; no duplican sus procedimientos ni necesitan cargar las skills de Claude. El instalador también agrega estos archivos a bóvedas existentes, conservando cualquier comando previo del mismo nombre.

Referencia oficial: [reglas](https://opencode.ai/docs/rules/) y [comandos](https://opencode.ai/docs/commands/). El formato está preparado según esas convenciones; la prueba de invocación en OpenCode real se registra por separado de la verificación de archivos.
