> [!info]- Índice de esta nota (líneas)
> - Líneas 1–18: Este índice
> - Líneas 20–23: Solución de problemas
> - Líneas 24–27: La IA no puede guardar en mi carpeta
> - Líneas 28–31: Vuelve a preguntarme lo que ya respondí
> - Líneas 32–35: Todavía no tengo fecha, fuentes ni primera tarea
> - Líneas 36–45: El cierre revisa otra bóveda
> - Líneas 46–49: Python no está disponible
> - Líneas 50–55: Aparece un bloqueo
> - Líneas 56–59: El creador informa un proyecto existente
> - Líneas 60–65: No aparece el Panel o la fecha automática
> - Líneas 66–69: Claude Code no reconoce un comando
> - Líneas 70–73: Claude no conecta al MCP o rechaza sus herramientas
> - Líneas 74–77: OpenCode no muestra los comandos del kit
> - Líneas 78–81: OpenCode muestra un error del proveedor o modelo
> - Líneas 82–85: ChatGPT ve los adjuntos pero no mi carpeta
> - Líneas 86–106: Mensajes del validador
> - Líneas 107–109: La IA no encuentra una nota nueva

# Solución de problemas

Si una IA está configurando tu bóveda, pasale el problema y pedile que revise los archivos: no necesitás corregirlos a mano. Las indicaciones de formato de abajo también sirven para quien elija el recorrido manual.

## La IA no puede guardar en mi carpeta

Comprobá que tenga acceso de escritura a la carpeta correcta. Un adjunto no concede ese acceso. Si puede generar archivos, pedile una copia configurada para descargar; si solo responde texto, quedará pendiente guardarlo. Ver [Empezar con una IA](QUICKSTART.md).

## Vuelve a preguntarme lo que ya respondí

Pedile que relea `00_CORE/configuracion.md` y la ficha de tu proyecto. Si la configuración quedó parcial, debe retomar solo lo pendiente. Si estaba lista, «seguí» continúa el proyecto.

## Todavía no tengo fecha, fuentes ni primera tarea

Podés comenzar con un objetivo. Las secciones sin datos quedan vacías y sus avisos no bloquean la configuración. La fecha de actualización refleja cuándo cambió la ficha; no es un plazo del proyecto.

## El cierre revisa otra bóveda

La salida «Bóveda revisada» indica la carpeta comprobada, tanto si el cierre pasa como si encuentra errores. Sin una ruta explícita, usa la bóveda donde está el script; cambiar la carpeta actual no cambia ese destino. Pedile a la IA que use la ruta actual de tu bóveda y la contraste con la salida:

```sh
python "ruta-del-kit/00_CORE/schemas/validate.py" "ruta-de-la-bóveda" --cierre --operacion ID
```

También admite su carpeta `00_CORE/cells`. Si moviste o volviste a extraer el ZIP, actualizá la ruta; no reemplaces las notas ni registres otra operación solo por haber revisado otra carpeta.

## Python no está disponible

El kit funciona con herramientas de archivos y revisión manual. Python solo automatiza creación, validación e índice. Si necesitás usarlo, el comando puede llamarse `python3` o `py` en lugar de `python`.

## Aparece un bloqueo

Mientras escriben, las herramientas del kit crean un archivo de bloqueo (`.<nota>.kit-lock` junto a la nota, o `00_CORE/logs/.registro-cambios.lock` para el registro) y lo retiran al terminar, aunque la operación falle. El archivo indica el proceso (`pid`) y la hora de inicio. Si una operación se cortó (corte de luz, cierre forzado, error del asistente), puede quedar y las escrituras siguientes se detienen con un mensaje que muestra su ruta y antigüedad. Un bloqueo de menos de 10 minutos suele indicar otra operación en curso: esperá y reintentá.

Si persiste y ninguna IA ni proceso está trabajando en la bóveda, el bloqueo quedó huérfano. Para comprobarlo, cerrá las sesiones de IA abiertas sobre la bóveda y buscá ese `pid` en el Administrador de tareas (Windows, pestaña Detalles) o con `ps -p <pid>` (macOS y Linux): si no aparece, la operación terminó; si aparece como Python, esperá a que termine; si es otro programa, el sistema reutilizó ese número y la operación también terminó. Si el archivo está vacío o no indica `pid`, guiate por su antigüedad. Después borrá solo ese archivo, releé las notas afectadas para confirmar que están completas y reintentá. Una IA no lo borra sin confirmación de la persona, y el kit no retira bloqueos por su cuenta: otra herramienta podría estar usándolos.

## El creador informa un proyecto existente

Puede haber una carpeta ocupada o una ficha con el mismo identificador, aunque el archivo tenga otro nombre. Retomá el proyecto propio o elegí otro identificador. `aprender-python` pertenece al ejemplo ficticio: no adoptes sus datos como propios. Si una creación se interrumpió, conservá los archivos completos y releelos antes de reintentar.

## No aparece el Panel o la fecha automática

Seguí [Plantillas y panel](obsidian.md). Insertá la plantilla solo en una nota vacía; al duplicarla a mano, reemplazá `{{date:YYYY-MM-DD}}` por una fecha real.

El ejemplo ficticio se abre desde la ayuda del Panel; está excluido de sus proyectos y tareas. Si todavía no creaste un proyecto propio, esas vistas pueden estar vacías.

## Claude Code no reconoce un comando

Abrilo en la raíz de la bóveda. Las skills están en `.claude/skills/`; si acabás de agregarlas, reiniciá la sesión. Conservá y compará cualquier comando previo del mismo nombre. Los permisos para leer o escribir dependen de tu configuración; el kit no los concede por sí mismo.

## Claude no conecta al MCP o rechaza sus herramientas

Pasale a la IA el error y pedile que siga [el diagnóstico de MCP en Claude](mcp-claude.md). Cubre `tools/list`, esquemas de entrada/salida incompatibles, carpetas fuera del alcance y conexión HTTP. La IA comprueba el conector y sus versiones antes de adaptar la conexión; no reinstala tu bóveda ni da por hecha una reparación solo por reiniciar.

## OpenCode no muestra los comandos del kit

Abrí la carpeta que contiene `AGENTS.md` y comprobá que esté `.opencode/commands/configurar.md`. Si acabás de agregar los comandos, abrí una sesión nueva. Podés iniciar con el mensaje del README y continuar con los [pedidos en lenguaje común](usar-con-otras-ias.md); la [guía de OpenCode](opencode.md) muestra ambos accesos. No reemplaces tus instrucciones con `/init` para intentar resolverlo.

## OpenCode muestra un error del proveedor o modelo

Si `/configurar` aparece pero la IA no responde, separá ese problema de los archivos del kit. Revisá la conexión y disponibilidad del modelo desde OpenCode según su [guía de proveedores](https://opencode.ai/docs/providers/). Un error de autenticación, límite de uso o 403 no se arregla recreando la bóveda, borrando tus notas o reinstalando el kit. Conservá lo ya guardado y retomá cuando el proveedor responda.

## ChatGPT ve los adjuntos pero no mi carpeta

Un Proyecto de ChatGPT con archivos subidos trabaja sobre esas copias. Para guardar en la bóveda local, necesitás adjuntar la carpeta a un proyecto local con herramientas de escritura. También podés pedir una copia descargable si el chat puede generarla. Seguí la [guía de ChatGPT](chatgpt.md) y usá la versión vigente de tus notas al retomar.

## Mensajes del validador

El validador es la referencia de formato. Con una IA, pedile que explique los mensajes y proponga cambios concretos antes de aplicarlos. Para edición manual:

| Mensaje o problema | Qué revisar |
|---|---|
| No hay fichas | Creá un proyecto con la IA o seguí la [guía manual](primer-proyecto.md). No es un error de instalación. |
| No encuentra propiedades | La nota empieza con `---`, propiedades y otro `---`. |
| Propiedad faltante, repetida o vacía | Compará con `TEMPLATE_cell.md` y conservá una sola versión de cada campo. |
| Comillas o dos puntos | Usá texto en una línea; por ejemplo, `descripcion: "Meta: ordenar apuntes"`. El lector admite propiedades planas y listas simples, no todo YAML. |
| Contexto no reconocido | A: técnico; B: narrativo; C: persuasivo; D: operativo. La IA elige según el uso. |
| Fecha incorrecta | Una fecha real con formato AAAA-MM-DD. |
| Sección faltante | Deben estar `## Hechos clave` y `## Próximas acciones`, aunque no tengan viñetas todavía. |
| Acción sin casilla | `- [ ] tarea pendiente` o `- [x] tarea hecha`, con texto. |
| Hecho sin fuente | Agregá `(fuente: referencia)`; mientras falte, el dato no está comprobado. |
| Decisión sin fecha | `- AAAA-MM-DD: decisión — motivo`. |
| Texto de plantilla pendiente | Reemplazá o quitá `[completar: ...]` en tu copia; no inventes datos. |
| Ficha larga | Resumí o enlazá notas de detalle. Proponé el archivo de información anterior antes de moverla. |

Los avisos no son errores. Formato correcto tampoco significa fuentes verificadas ni funcionamiento visual comprobado en Obsidian.

## La IA no encuentra una nota nueva

Pedile que lea `INDICE.md`, contraste el catálogo con la carpeta real y lo actualice según [la guía del índice](indice-principal.md). Si hay un índice propio incompatible o falta escritura, debe explicar el pendiente y conservar tus notas. Un adjunto antiguo no demuestra que esa nota no exista.
