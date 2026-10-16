---
level: organ
tipo: setup-protocol
descripcion: Conversación de inicio para que una IA configure la bóveda con las respuestas del usuario.
---
> [!info]- Índice de esta nota (líneas)
> - Líneas 1–5: Propiedades
> - Líneas 6–18: Este índice
> - Líneas 20–23: Configurar una bóveda conversando
> - Líneas 24–29: 1. Ubicar la bóveda
> - Líneas 30–39: 2. Preguntar lo indispensable y acordar el destino
> - Líneas 40–47: 3. Preparar los archivos
> - Líneas 48–53: Guardar el punto de partida
> - Líneas 54–62: Crear el proyecto
> - Líneas 63–70: 4. Verificar y entregar
> - Líneas 71–84: Ejemplo completo de inicio
> - Líneas 85–88: Secuencia de cierre compartida
> - Líneas 89–91: Si no podés escribir en la carpeta

# Configurar una bóveda conversando

Esta es la guía principal de configuración. La persona cuenta qué necesita; la IA prepara los archivos. Consultá las referencias al ejecutar cada paso, sin convertirlas en tareas para el principiante. Desarrollar el kit o continuar un proyecto listo sigue `AI-INSTRUCTIONS.md`, sin reiniciar la entrevista.

## 1. Ubicar la bóveda

Leé `INDICE.md` completo y después `00_CORE/atoms/00_vault-rules.md`. Comprobá el acceso real de lectura y escritura; un adjunto o enlace no da acceso al original. Buscá configuración y fichas por su propiedad `proyecto`, aunque estén renombradas: si ya hay trabajo, conservá su versión y retomá solo lo pendiente.

En una bóveda existente, leé su entrada y reglas antes de elegir dónde guardar; respetá sus convenciones y acordá incompatibilidades puntuales. Si falta un índice, proponé integrarlo. No sustituyas reglas ni entrada, ni interpretes la ausencia de configuración del kit como una bóveda vacía.

## 2. Preguntar lo indispensable y acordar el destino

Preguntá solo lo que falte, de a una o dos preguntas: qué quiere organizar, si empieza de cero o conserva notas y qué quiere lograr. Reutilizá lo ya respondido. Derivá nombre, descripción y contexto sin pedir YAML, carpetas ni letras A/B/C/D. Si el objetivo es ambiguo, ofrecé dos opciones y esperá su elección; una propuesta no confirma una decisión.

CV, presentación, formación, experiencia, fecha, fuentes, hechos y primera tarea son opcionales. Con objetivo acordado y sin tarea, dejá acciones vacías: los avisos no obligan a inventar datos. Empezá por un proyecto.

Proponé la carpeta descargada para una bóveda nueva. Si quiere otra, obtené la ruta de una carpeta nueva separada; no muevas ni renombres el origen. Ante rutas ocupadas o una ficha propia coincidente, ofrecé retomar o acordar otro identificador. Si coincide con el ejemplo ficticio, conservá sus datos y proponé otro identificador; practicar con él requiere elección explícita. Pedí acceso si falta.

Mostrá destino, proyecto, objetivo, próximo paso aceptado o pendiente y archivos afectados, incluido `INDICE.md`. Resolvé elecciones pendientes antes de escribir. Ese pedido con alcance acordado autoriza el trabajo sin otra aprobación por archivo; reestructurar notas existentes requiere autorización específica.

## 3. Preparar los archivos

| Destino acordado | Preparación |
|---|---|
| Carpeta descargada | Ya contiene el kit; no ejecutes el instalador sobre sí mismo. |
| Otra carpeta nueva | Copiá el kit con `.obsidian`, `.claude` y `.opencode`; excluí Git, cachés, `.claude/worktrees`, `workspace*.json` y datos de pruebas. Detenete ante archivos diferentes presentes. |
| Bóveda existente | Usá la instalación conservadora de `AI-INSTRUCTIONS.md` o [la alternativa sin Python](../../DOCS/instalacion-manual.md). Conservá `.obsidian`; no fuerces conflictos. Acordá ajustes de Plantillas/Bases e indicá lo pendiente. |

### Guardar el punto de partida

Antes de crear el primer proyecto, guardá respuestas e inventario en `00_CORE/configuracion.md` o el equivalente acordado. Leé [Personalizar la bóveda](personalizar-vault.md): define los ítems y estados para retomar sin repetir preguntas. Si la nota es nueva, usá [la plantilla](../templates/TEMPLATE_configuracion.md), cambiá `tipo` a `configuracion`, completá fecha real y referencias. Atribuí las respuestas a su origen: lo desconocido sigue pendiente y lo saltado queda omitido. Si existe, releela y actualizá solo lo nuevo, conservando preferencias y otros proyectos.

Mantené `estado: parcial` hasta comprobar la integración. Guardá avance e impedimentos por grupo, distinguiendo enlaces previstos de comprobados. Usá referencias relativas: una ruta temporal de extracción no es la ubicación personal. Al preparar otra bóveda, conservá el kit de origen.

### Crear el proyecto

1. Derivá un identificador corto, sin tildes y con guiones; acordá una variante si está reservado u ocupado. Con Python y reglas compatibles, seguí [el creador](../../DOCS/creacion-para-asistentes.md). Si ya existe una ficha editada, trabajá desde ella: no la recrees ni eludas su protección con otro nombre.
2. Sin Python o con organización propia, creá desde `PROJECT_TEMPLATE/` y [la plantilla de ficha](../templates/TEMPLATE_cell.md); guardá la ficha en `00_CORE/cells/` y completá identificador, descripción, contexto, objetivo y fecha real. Quitá marcadores y ejemplos de la copia; hechos con fuente e intenciones atribuidas al usuario, sin presentarlas como logros. Acciones solo aceptadas; secciones sin datos vacías.
3. Enlazá ficha e índice. En una bóveda nueva (carpeta descargada u otra carpeta nueva), reemplazá el aviso inicial del Panel por bienvenida, próximo paso aceptado o pendiente y acceso al proyecto y al inventario. Conservá el ejemplo con `ejemplo: true`, separado de proyectos propios. En una bóveda existente, editá solo el bloque acordado. El creador no completa este paso.
4. Actualizá configuración y avance; preferencias personales allí, sin cambiar reglas compartidas. Mantené [mapas y nodos](../../DOCS/indice-principal.md): el catálogo debe reflejar los archivos reales del destino.

Este paso también agrega proyectos a una bóveda lista: sin reinstalar ni repetir la entrevista. Un proyecto distinto se acuerda; preguntá solo por los datos indispensables ausentes. No requiere cuentas nuevas, plugins comunitarios ni sincronización; no publiques ni hagas push de la bóveda personalizada.

## 4. Verificar y entregar

Releé archivos y enlaces: sin duplicados ni marcadores, ficha válida según [Revisar fichas](../../DOCS/usar-con-otras-ias.md#revisar-fichas), Panel adaptado y acceso al inventario. Completá el [mantenimiento y cierre](../../DOCS/mantenimiento.md#secuencia-de-cierre-compartida): autoría, rangos, mapas y registro. La IA realiza las operaciones; la persona no ejecuta comandos ni cuenta líneas. Sin Python, aplicá su alternativa manual y declarala.

Marcá `lista` solo con archivos e integración comprobados. Si falla, conservá `parcial`, lo completado y el impedimento; releelos al retomar. El inventario puede seguir abierto con la bóveda lista: ofrecé «qué falta para personalizar mi bóveda» cuando quiera completarlo.

Mostrá carpeta y acceso al proyecto. Explicá abrir esa carpeta como bóveda en Obsidian y entrar al Panel; si falta Obsidian, indicá `https://obsidian.md`. Separá comprobación de archivos de prueba visual. Ofrecé seguir la tarea aceptada o elegirla; no afirmes haber abierto Obsidian sin hacerlo.

## Ejemplo completo de inicio

Ejemplo ficticio, no datos para copiar automáticamente. Cada respuesta se usa cuando la persona la da.

> **Persona:** Quiero organizar mi estudio de astronomía. Empiezo de cero.
> **IA:** ¿Qué te gustaría conseguir?
> **Persona:** Entender las bases y guardar resúmenes. No tengo apuntes, fecha ni primera tarea; el perfil prefiero dejarlo para después.
> **IA:** Prepararé «Estudio de astronomía» en esta carpeta para entender las bases y guardar tus resúmenes. Guardaré tus respuestas, crearé el proyecto y actualizaré sus accesos, el Panel y el índice general. El perfil y la primera tarea pueden esperar. ¿Usamos esta carpeta con ese alcance?
> **Persona:** Sí, preparalo aquí.

La IA guarda primero configuración parcial e inventario, crea el proyecto, adapta el Panel y verifica el mantenimiento. Solo después informa lo comprobado: «Tu carpeta está preparada; abrila como bóveda en Obsidian y entrá al Panel. Tu perfil sigue para después». Si hay un impedimento, explica lo parcial. La prueba visual continúa pendiente hasta realizarla.

Si luego pide «Agregá un nodo para mis resúmenes y una nota vacía», seguí la guía de mapas: padre ↔ hijo, nodo ↔ nota, nodos generales conectados con entrada e índice. Al decir «seguí con mi estudio», releé configuración y ficha, conservá omisiones y proponé elegir el primer tema; no guardes una propuesta como tarea aceptada.

## Secuencia de cierre compartida

La secuencia técnica vive en [Mantenimiento](../../DOCS/mantenimiento.md#secuencia-de-cierre-compartida), compartida con el trabajo diario. Consultala antes de registrar y cerrar; no la sustituyas por el éxito del creador.

## Si no podés escribir en la carpeta

Explicá el límite antes de prometer una configuración. Si podés generar archivos, devolvé una copia configurada y comprobada del kit leído, incluidos los ocultos; indicá descargar, descomprimir y abrir esa carpeta. El original no cambió. Si solo respondés texto, entregá plan y contenidos con destinos como pendientes y ofrecé conectar la carpeta o [la alternativa manual](../../DOCS/primer-proyecto.md). No simules acceso ni sincronización.
