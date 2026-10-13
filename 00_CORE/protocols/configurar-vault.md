---
level: organ
tipo: setup-protocol
descripcion: Conversación de inicio para que una IA configure la bóveda con las respuestas del usuario.
---
> [!info] Índice de esta nota (líneas)
> - Líneas 1–5: Propiedades
> - Líneas 6–18: Este índice
> - Líneas 20–23: Configurar una bóveda conversando
> - Líneas 24–31: 1. Leer y comprobar el punto de partida
> - Líneas 32–45: 2. Conversar, de a poco
> - Líneas 46–53: 3. Acordar destino y alcance
> - Líneas 54–61: 4. Hacer la configuración
> - Líneas 62–71: Guardar el punto de partida
> - Líneas 72–87: Crear el proyecto
> - Líneas 88–95: 5. Verificar, entregar y cerrar
> - Líneas 96–107: Secuencia de cierre compartida
> - Líneas 108–112: Si no podés escribir en la carpeta

# Configurar una bóveda conversando

Usá este recorrido para iniciar o adaptar una bóveda. Desarrollar el kit o continuar un proyecto configurado sigue `AI-INSTRUCTIONS.md`, sin reiniciar la entrevista.

## 1. Leer y comprobar el punto de partida

Leé `INDICE.md` completo y después `00_CORE/atoms/00_vault-rules.md`. Comprobá qué carpeta podés leer y escribir: adjuntos, enlaces y archivos visibles no prueban acceso al original.

Revisá configuración y fichas vigentes según `AI-INSTRUCTIONS.md`; conservá lo creado y retomá solo lo pendiente. Antes de escribir, leé [Personalizar la bóveda](personalizar-vault.md) para el inventario y datos omitidos, y [Mantenimiento](../../DOCS/mantenimiento.md) para guardar y verificar esa operación. Completar el perfil puede hacerse con una bóveda lista.

En una bóveda existente, leé su índice y reglas antes de elegir dónde escribir. Si no tiene índice, revisá su estructura y proponé integrarlo. Respetá sus convenciones y acordá cualquier incompatibilidad puntual; no sustituyas sus reglas o entrada.

## 2. Conversar, de a poco

Explicá: «Vos me contás qué necesitás organizar; yo preparo las notas y reglas».

Preguntá solo lo que falte, de a una o dos preguntas por turno:

- Qué quiere organizar y si empieza de cero o conserva notas existentes.
- Qué quiere lograr con el primer proyecto y, si sabe, cuál es el próximo paso.

Reutilizá respuestas anteriores. Derivá nombre, descripción y contexto de comunicación; no pidas campos YAML, estructuras de carpetas ni letras A/B/C/D. Si falta un objetivo, ofrecé dos opciones relacionadas y esperá su elección. Las propuestas siguen siendo propuestas hasta aceptarlas.

Fecha, fuentes, hechos y primera tarea son opcionales. Con objetivo acordado y sin tarea, prepará la bóveda y dejá acciones vacías; los avisos del validador no obligan a inventar datos. Empezá por un proyecto y agregá otros cuando los pida.


## 3. Acordar destino y alcance

Para una bóveda nueva, proponé la carpeta descargada. Para otra ubicación, obtené la ruta y usá una carpeta nueva separada del origen; no muevas ni renombres la entregada por tu cuenta. Para una existente, pedí acceso a su carpeta si falta.

Comprobá rutas ocupadas y coincidencias por la propiedad `proyecto`, aunque la ficha esté renombrada. Ante una coincidencia propia, ofrecé retomar o elegir otro identificador. Ante el ejemplo ficticio, conservá sus datos y proponé otro identificador; practicar con él requiere elección explícita.

Mostrá destino, proyecto, objetivo, próximo paso aceptado o pendiente y archivos a crear o modificar, incluido el índice principal. Resolvé elecciones pendientes. El pedido de configurar con destino y alcance acordados autoriza ese trabajo sin otro permiso por archivo. Reestructurar notas existentes requiere autorización específica.

## 4. Hacer la configuración

| Destino | Cómo preparar los archivos |
|---|---|
| Carpeta descargada | Ya tiene el kit; no ejecutes el instalador sobre sí mismo. |
| Otra carpeta nueva | Copiá el kit, incluidos `.obsidian`, `.claude` y `.opencode`. Excluí Git, cachés, checkouts de `.claude/worktrees`, sesiones `workspace*.json` y datos de pruebas. Detenete ante archivos diferentes presentes. |
| Bóveda existente | Seguí la instalación conservadora de `AI-INSTRUCTIONS.md`. No fuerces conflictos ni reemplaces `.obsidian`. Sin Python, compará y agregá archivos ausentes según `DOCS/instalacion-manual.md`. Acordá ajustes puntuales de Plantillas o Bases; indicá funciones pendientes. |

### Guardar el punto de partida

Con destino disponible y reglas leídas o integradas, guardá las respuestas **antes de crear el primer proyecto** en `00_CORE/configuracion.md` o equivalente acordado. Si existe, releela y actualizá solo lo nuevo, conservando preferencias y otros proyectos. Al preparar otra bóveda, no personalices el kit de origen.

Si todavía no existe, usá [la plantilla de configuración](../templates/TEMPLATE_configuracion.md): en la copia, cambiá `tipo` a `configuracion`, completá la fecha real y adaptá los marcadores y enlaces al proyecto y destino acordados. Guardá lo respondido con su origen; lo desconocido sigue pendiente y lo saltado se marca omitido. La plantilla no autoriza reemplazar una configuración existente.

Conservá estado `parcial` hasta verificar la integración. Actualizá el avance de archivos tras cada grupo para retomar interrupciones, distinguiendo enlaces previstos de comprobados.

Usá referencias relativas; para un ZIP identificá su carpeta raíz, sin guardar rutas temporales como ubicación personal. La persona elige dónde descomprimirlo.

### Crear el proyecto

Esta sección también agrega proyectos a una bóveda lista: conservá su configuración, sin repetir entrevista ni instalación. Preguntá únicamente por el objetivo o datos indispensables todavía ausentes.

Con Python y reglas compatibles, usá `crear_proyecto.py` según `DOCS/creacion-para-asistentes.md`. Produce ficha, índice y carpetas; releé su resultado y completá Panel y configuración. Sin Python o con organización propia, hacé esos pasos con herramientas de archivos:

1. Derivá un identificador corto válido, sin tildes y con guiones; ante nombre reservado o coincidencia, acordá una variante.
2. Creá la carpeta desde `PROJECT_TEMPLATE/` y la ficha desde `00_CORE/cells/TEMPLATE_cell.md`, adaptándolas al destino acordado. Completá identificador, descripción, contexto, objetivo y fecha real.
3. Quitá ejemplos y marcadores de la copia. Hechos con fuente; intenciones atribuidas al usuario, sin presentarlas como logros. Acciones solo aceptadas; dejá vacías las secciones sin datos.
4. Enlazá ficha e índice y agregá acceso en el Panel, además del inventario en la configuración. En copia nueva, reemplazá el aviso inicial por bienvenida y próximo paso; en existente, adaptá solo el bloque acordado. Conservá el ejemplo con `ejemplo: true`, separado de proyectos propios.
5. Actualizá configuración, inventario y avance; las preferencias personales van allí, no en las reglas compartidas.

Si la ficha ya existe o fue editada, completá los pendientes desde esa versión. No ejecutes el creador para recrearla ni uses otro nombre para eludir su protección. Un proyecto distinto requiere haberlo acordado.

Mantené `INDICE.md` según `DOCS/indice-principal.md`: notas reales del destino, configuración y nuevo proyecto. El catálogo copiado del kit no basta. Este recorrido con herramientas de archivos no requiere cuentas nuevas, plugins comunitarios ni sincronización. No publiques ni hagas push de la bóveda personalizada.

## 5. Verificar, entregar y cerrar

Releé lo creado: sin duplicados ni marcadores, enlaces existentes, Panel integrado y ficha válida según «Revisar fichas» de `DOCS/usar-con-otras-ias.md`. Sin Python, declaralo revisión manual. Completá `DOCS/mantenimiento.md`, que verifica rangos, registra operaciones y mantiene los mapas; el principiante no hace esos pasos.

Marcá `lista` solo con los archivos e integración comprobados. Ante fallo, conservá `parcial`, lo completado y el impedimento; releé ese estado al retomar. El inventario sigue su propia guía: puede quedar abierto con la bóveda lista. Ofrecé «qué falta para personalizar mi bóveda» para completarlo después.

Mostrá carpeta y acceso a la ficha. Explicá cómo abrir esa carpeta como bóveda y entrar al Panel; si falta Obsidian, indicá `https://obsidian.md`. Separá comprobación de archivos de prueba visual: no afirmes haber abierto Obsidian sin hacerlo. Ofrecé empezar la tarea aceptada o elegirla; completá vos las operaciones técnicas dentro del alcance disponible.

### Secuencia de cierre compartida

Para cerrar una sesión de trabajo (referencia: `DOCS/mantenimiento.md`):

1. **Chequeo parcial**: ejecutá `python 00_CORE/schemas/validate.py --cierre --operacion <ID-parcial>` con el ID de la operación que registró los avances actuales. Esta validación no escribe nada; solo confirma configuración, mapas, rangos y registro.
2. **Estado final `lista`**: si la bóveda pasa a `estado: lista`, actualizá `00_CORE/configuracion.md` (cambiar `estado` y `fecha`).
3. **Mantenimiento de rangos y mapas**: corré `python 00_CORE/schemas/note_index.py apply --vault <raíz>` y `python actualizar_indice.py <raíz>` para refrescar índices de líneas y mapas.
4. **Registrar edición final**: registrá ese cambio de configuración como **nueva operación real** (nuevo ID, `verificado: true`, fecha actual con zona). No reutilicés el ID del chequeo parcial.
5. **Refrescar y volver a chequear**: corré `actualizar_indice.py` otra vez (el registro ya existe) y luego `validate.py --cierre --operacion <ID-final>` con el nuevo ID. El chequeo anterior no sirve para la edición final.

La IA gestiona los IDs y pasos técnicos; la persona no los proporciona. Índices manuales o logs incompatibles generan error explícito de «revisión manual pendiente», sin reescritura ni aprobación automática.

## Si no podés escribir en la carpeta

Explicá el límite antes de prometer una configuración. Si podés generar archivos, devolvé una copia configurada y verificada del kit leído, incluidos sus archivos ocultos. Indicá descargar, descomprimir y abrir esa carpeta; el original no cambió.

Si solo respondés texto, entregá plan y contenidos con destinos como configuración pendiente. Ofrecé conectar una carpeta; `DOCS/primer-proyecto.md` es alternativa manual. No simules acceso ni sincronización de adjuntos.
