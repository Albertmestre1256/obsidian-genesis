# Empezar con OpenCode

OpenCode puede configurar tu bóveda desde la carpeta descargada. El kit ya trae la entrada `AGENTS.md` y el comando `/configurar`; no necesitás escribir código ni modificar su configuración global.

## Abrir y configurar

1. Descomprimí el kit y abrí en OpenCode la carpeta que contiene `README.md`, `INDICE.md` y `AGENTS.md`. Si usás la terminal, abrila en esa carpeta y ejecutá `opencode`.
2. Escribí **`/configurar`**. También podés agregar tu idea, por ejemplo `/configurar quiero organizar mi estudio`.
3. Respondé las preguntas. El asistente debe mostrarte dónde guardará la bóveda y qué creará, conservar tus notas y preparar el primer proyecto.

Si tu versión no muestra el comando, pegá el [mensaje de inicio del README](../README.md). El comando es un acceso al mismo protocolo, no un requisito para usar el kit.

Elegí un modo que permita editar archivos cuando vayas a configurar; si estás en un modo de planificación, el asistente puede preparar la propuesta y necesitar cambiar de modo para guardarla. Los permisos y el proveedor de IA son los que tengas en OpenCode. El kit no cambia tu modelo ni instala servicios.

## Qué recibir

La carpeta preparada, la ficha de tu proyecto, un acceso desde `Panel.md`, la configuración guardada y `INDICE.md` actualizado. Abrí esa carpeta como bóveda en Obsidian y entrá al Panel. Si todavía no lo instalaste, podés hacerlo desde [obsidian.md](https://obsidian.md).

Para una bóveda existente, indicá su carpeta como destino y permití leerla antes de integrar el kit. Se conservan sus reglas y ajustes; cualquier cambio a notas existentes se acuerda por separado.

## Retomar

Decí «seguí con la configuración» si quedó parcial, o «seguí con [proyecto]» cuando esté lista. Para redactar, crear otro proyecto o guardar el cierre, usá los [pedidos de uso diario](usar-con-otras-ias.md). El asistente debe leer lo guardado, incluso si renombraste una ficha.

## Cómo se integra

`AGENTS.md` señala el orden de lectura. `.opencode/commands/configurar.md` remite al protocolo común; no duplica la entrevista ni necesita cargar las skills de Claude. El instalador también agrega estos archivos a bóvedas existentes, conservando cualquier comando previo del mismo nombre.

Referencia oficial: [reglas](https://opencode.ai/docs/rules/) y [comandos](https://opencode.ai/docs/commands/). El formato está preparado según esas convenciones; la prueba de invocación en OpenCode real se registra por separado de la verificación de archivos.
