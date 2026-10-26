> [!info]- Índice de esta nota (líneas)
> - Líneas 1–10: Este índice
> - Líneas 12–15: Empezar con OpenCode
> - Líneas 16–27: Abrir y configurar
> - Líneas 28–33: Qué recibir
> - Líneas 34–49: Retomar
> - Líneas 50–55: Carga automática opcional
> - Líneas 56–63: Filtrar el índice de líneas
> - Líneas 64–73: Consulta con archivos autorizados
> - Líneas 74–78: Cómo se integra

# Empezar con OpenCode

OpenCode puede configurar tu bóveda desde la carpeta descargada. El kit ya trae la entrada `AGENTS.md` y el comando `/configurar`; no necesitás escribir código ni modificar su configuración global.

## Abrir y configurar

1. Descomprimí el kit y abrí en OpenCode la carpeta que contiene `INDICE.md` y `AGENTS.md`. Si usás la terminal, abrila en esa carpeta y ejecutá `opencode`.
2. Escribí **`/configurar`**. También podés agregar tu idea, por ejemplo `/configurar quiero organizar mi estudio`.
3. Respondé las preguntas. El asistente debe mostrarte dónde guardará la bóveda y qué creará, conservar tus notas y preparar el primer proyecto.

Si tu versión no muestra el comando, usá el pedido del [inicio rápido](QUICKSTART.md). El comando es un acceso al mismo protocolo, no un requisito para usar el kit.

Elegí un modo que permita editar archivos cuando vayas a configurar; si estás en un modo de planificación, el asistente puede preparar la propuesta y necesitar cambiar de modo para guardarla. Los permisos y el proveedor de IA son los que tengas en OpenCode. El kit no cambia tu modelo ni instala servicios.

Si OpenCode todavía no responde porque falta conectar un proveedor o el modelo devuelve un error, resolvé ese acceso en OpenCode antes de configurar la bóveda. Su [guía de conexión](https://opencode.ai/docs/providers/) explica las opciones. El kit ya trae `AGENTS.md`: podés comenzar directamente con `/configurar`, sin ejecutar `/init` para generar otras instrucciones.

## Qué recibir

La carpeta preparada, la ficha de tu proyecto, un acceso desde `Panel.md`, la configuración guardada y `INDICE.md` actualizado. Abrí esa carpeta como bóveda en Obsidian y entrá al Panel. Si todavía no lo instalaste, podés hacerlo desde [obsidian.md](https://obsidian.md).

Este kit prepara bóvedas nuevas: indicá una carpeta nueva como destino. No lo uses para adaptar una bóveda existente.

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

## Carga automática opcional

El perfil [opencode.example.json](../opencode.example.json) precarga el índice general, las reglas y la entrada para la IA. Para usarlo, copialo como `opencode.json` en la raíz de la bóveda. Si ya tenés una configuración, incorporá solo las rutas que falten en `instructions` y la integración de `plugin`; conservá el modelo, los permisos y el resto de tus ajustes. No hace falta cambiar la configuración global.

El nombre de ejemplo evita activarlo por accidente. La carga aumenta el contexto inicial y no garantiza ahorro: evita pedir otra lectura de un documento ya disponible, pero las fichas y los protocolos siguen cargándose según la tarea. Comprobá las tres rutas y su carga efectiva: OpenCode puede omitir archivos inexistentes. Si el contenido falta, está recortado, cambió o salió del contexto, el asistente debe recuperarlo. Sin este perfil, conserva la lectura por herramientas.

## Filtrar el índice de líneas

El perfil anterior carga [opencode_context.mjs](../00_CORE/schemas/opencode_context.mjs), una integración local sin dependencias externas. Quita del contexto enviado al modelo únicamente el bloque generado «Índice de esta nota (líneas)», tanto en las instrucciones precargadas como en las lecturas completas de Markdown. Conserva YAML, títulos, contenido, otros avisos y los archivos originales. El índice general de documentos sigue disponible.

Las lecturas mantienen sus números de línea originales. Si se pide `offset` o `limit`, el filtro conserva también el bloque de rangos: permite consultarlo para navegar. Un bloque incompleto o distinto del formato generado se conserva. El filtro reduce caracteres; el ahorro de tokens depende del modelo y debe medirse con su proveedor.

La integración usa hooks experimentales comprobados con OpenCode **1.19.4** en Windows. El modo `--pure` desactiva plugins, incluido este filtro. Otras versiones necesitan su propia comprobación; no se presume compatibilidad con la sintaxis de permisos de V2. No necesitás instalar Node para usarla en OpenCode; las pruebas del repositorio usan Node 24.

## Consulta con archivos autorizados

[opencode.consulta.example.json](../opencode.consulta.example.json) ofrece un segundo perfil opcional: deniega por defecto y habilita solo `read` para los archivos enumerados en `readPaths`. Incluye una ficha ficticia para probar. Antes de activarlo, acordá qué archivos reales necesitás y adaptá esa única lista con rutas relativas explícitas, separadas por `/`, sin comodines. Incluí `AGENTS.md` y cada documento de `instructions`. Abrí OpenCode desde la raíz de la bóveda y copiá el perfil como `opencode.json`, conservando tus ajustes de modelo y proveedor si ya existen.

El agente `consulta` puede leer esos archivos; no puede escribir, ejecutar comandos, buscar con `grep` o `glob`, acceder a la web ni delegar en subagentes. Por eso este perfil no sirve para `/configurar` ni para guardar un `/cerrar`. Una denegación no autoriza ampliar la lista o cambiar de perfil: ese cambio necesita una decisión de la persona.

La integración aplica los permisos al proyecto y a los agentes configurados, verifica la ruta antes de cada lectura y rechaza enlaces y junctions. También comprueba las instrucciones declaradas y su procedencia antes de enviarlas al modelo. Una precarga no autorizada hace fallar la consulta.

Este control actúa sobre las herramientas y el contexto del agente. No es un aislamiento del sistema operativo: OpenCode puede abrir archivos de configuración durante el arranque, otros plugins tienen su propia autoridad y una modificación concurrente del sistema de archivos puede superar una comprobación previa. Usá un entorno aislado cuando necesites una frontera de seguridad más fuerte. Los permisos limitan las acciones posibles; no garantizan la exactitud de las respuestas.

## Cómo se integra

`AGENTS.md` señala el orden de lectura y cuándo reutilizar documentos ya disponibles. Los seis archivos de `.opencode/commands/` remiten a esa entrada y al protocolo de configuración o a los pedidos de uso diario; no ordenan releer el índice por cada comando ni necesitan cargar las skills de Claude.

Referencia oficial: [reglas](https://opencode.ai/docs/rules/), [comandos](https://opencode.ai/docs/commands/), [plugins](https://opencode.ai/docs/plugins/) y [permisos](https://opencode.ai/docs/permissions/). Las pruebas con OpenCode real y las capturas del proveedor local se registran fuera del kit; la suite del repositorio verifica el filtro y las restricciones sin usar una API externa.
