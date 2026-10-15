> [!info]- Índice de esta nota (líneas)
> - Líneas 1–7: Este índice
> - Líneas 9–12: Si Claude no conecta con el MCP
> - Líneas 13–24: Identificar el fallo
> - Líneas 25–33: Recorrido de diagnóstico para la IA
> - Líneas 34–39: Cuándo darlo por solucionado
> - Líneas 40–44: Referencias y límites

# Si Claude no conecta con el MCP

Pasale a la IA el mensaje de error y el nombre del conector. Pedile: «Leé esta guía, identificá el problema y conservá mis notas». No necesitás entender esquemas ni corregir archivos a mano. El kit funciona con otras herramientas de archivos; MCP es una conexión opcional.

## Identificar el fallo

Esta guía recoge errores reportados en servidores de archivos y conexiones a Obsidian. Son casos de compatibilidad: no demuestran un fallo de todos los clientes Claude ni del kit. `@modelcontextprotocol/server-filesystem`, `obsidian-mcp` y un servidor HTTP de un plugin son conectores distintos.

| Mensaje o síntoma | Qué debe comprobar la IA | Solución según el diagnóstico |
|---|---|---|
| `Invalid result for tools/list`, `inputSchema.type`, `expected "object"` | Definiciones de herramientas sin un esquema de parámetros válido. | Revisar versión efectiva y dependencias del servidor; usar una versión compatible comprobada. Fijar solo una versión antigua puede conservar dependencias incompatibles. |
| `invalid outputSchema`, `unsupported dialect`, `draft-07` o `2020-12` | El dialecto del esquema devuelto y el que acepta ese cliente. | Preferir una actualización compatible. Si hace falta un adaptador, modificar solo el esquema incompatible y comprobar la conexión; no retirar todos los esquemas por defecto. |
| `Access denied`, `path outside allowed directories` o `no allowed directories` | Carpeta real y lista de carpetas autorizadas, incluidos los Roots enviados por el cliente. | Corregir la carpeta expuesta en el proyecto o conexión. No ampliar acceso a otras carpetas para evitar el error. |
| Rechazo HTTP de `$schema`, `$defs` o `prefixItems` | Plugin, transporte y esquema de la herramienta exactos. | Revisar conversión y compatibilidad de ese plugin; un adaptador stdio no corrige por sí mismo un servidor HTTP. |
| `ECONNREFUSED` | Dirección, puerto y servicio que debería escuchar. | Comprobar si Obsidian y el plugin correspondiente están abiertos, habilitados y escuchando; este error solo no prueba una incompatibilidad de esquemas. |

## Recorrido de diagnóstico para la IA

1. Anotá mensaje exacto, cliente y versión, servidor/paquete y versión efectiva, transporte y operación fallida. Conservá un respaldo antes de editar la conexión. No recopiles claves ni cuerpos privados para un reporte.
2. Para un servidor stdio, probá la negociación sin llamar a un modelo: `initialize`, `notifications/initialized` y `tools/list`, continuando páginas. Revisá cada `inputSchema`, incluido `type: object`, sus parámetros y el dialecto anunciado. Registrá si falla la conexión, el catálogo o una llamada. Una herramienta con esquema vacío no se arregla agregando solo `type` si perdió los parámetros.
3. En filesystem, consultá `list_allowed_directories`. Su [documentación](https://raw.githubusercontent.com/modelcontextprotocol/servers/main/src/filesystem/README.md) indica que los Roots válidos del cliente sustituyen las carpetas de argumentos. Preferí corregir la carpeta del cliente. Si ese cliente no permite hacerlo, un adaptador puede omitir `capabilities.roots` en `initialize` únicamente para usar la lista explícita acordada; comprobá que el servidor devuelve exactamente esas carpetas. No sirve para eludir una denegación de permisos.
4. Ante un dialecto incompatible comprobado, respaldá y prepará un adaptador local de esa conexión. Puede retirar `outputSchema` de las herramientas afectadas en respuestas `tools/list`, conservando sus nombres, parámetros y resultados, si ese cliente admite resultados sin ese esquema. Eso reduce la validación de salida; comprobá su contenido y no afirmes compatibilidad universal. No cambies etiquetas `$schema` sin convertir el esquema. Fijá la versión realmente probada, no una versión tomada de un ejemplo.
5. En un plugin HTTP, identificá la versión y su conversor antes de proponer un parche. Si admite seleccionar el dialecto requerido por el cliente, ajustalo y verificá el resultado. Cambiar `draft-2020-12` por `draft-07` en un `main.js` desconocido no es una receta general; los cambios locales del plugin pueden perderse al actualizar. Preferí la corrección del proveedor y conservá el parche verificable si fue necesario.
6. Aplicá solo dentro del alcance acordado, conservando otras conexiones. Volvé a cargar la conexión según el cliente; Claude Desktop puede requerir cerrar también su proceso de bandeja y volver a abrirlo. Si hay un adaptador Node, ejecutá el servidor con ruta y argumentos separados; evitá construir una orden de shell con rutas interpoladas. Comprobá Windows y rutas con espacios si es el entorno del usuario.

## Cuándo darlo por solucionado

La conexión negocia, entrega herramientas utilizables y permite leer una nota de prueba dentro del alcance acordado. Las carpetas autorizadas coinciden con ese alcance. Si la tarea requiere escritura, probala en una copia aislada o nota de prueba acordada y verificá el resultado; una lectura correcta no acredita escritura. Guardá diagnóstico, versiones y comprobaciones según [Mantenimiento](mantenimiento.md), con la causa todavía pendiente si no se determinó.

Si continúa impedida, explicá qué falta y conservá la configuración parcial. No reinstales el vault, borres notas ni repitas llamadas a modelos para resolver un error del catálogo. Retomá con otra herramienta de archivos autorizada o entregá una copia descargable si ese chat puede generarla, aclarando qué original no cambió.

## Referencias y límites

La [especificación de herramientas MCP](https://modelcontextprotocol.io/specification/2025-11-25/server/tools) define `inputSchema` y permite `outputSchema` opcional; el dialecto por defecto es 2020-12 y también muestra draft-07 explícito. La [especificación de Roots](https://modelcontextprotocol.io/specification/2025-11-25/client/roots) describe su negociación. La aceptación concreta depende del cliente y servidor usados.

Los síntomas y alternativas anteriores provienen de un reporte de compatibilidad aportado al proyecto y contrastado con esas referencias. Este documento no instala un conector ni acredita una reparación probada en todas las versiones de Claude. La IA verifica el caso del usuario antes de aplicar una adaptación.
