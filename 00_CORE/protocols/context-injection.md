---
level: organ
tipo: context-injection-protocol
descripcion: Elegir el contexto mínimo según la tarea y ampliar solo cuando haga falta.
---
> [!info] Índice de esta nota (líneas)
> - Líneas 1–5: Propiedades
> - Líneas 6–12: Este índice
> - Líneas 14–27: Qué darle a la IA
> - Líneas 28–35: Guías de escritura, cuando hagan falta
> - Líneas 36–39: Si falta contexto
> - Líneas 40–44: Mantener la ficha útil

# Qué darle a la IA

Leé primero `INDICE.md`, después `00_CORE/atoms/00_vault-rules.md` y la ficha del proyecto en `00_CORE/cells/`. Buscala por su propiedad `proyecto`; el ejemplo aprender-python está en `ejemplo-context.md`. El índice principal se lee en cada inicio; el índice específico de un proyecto se carga cuando la tarea lo necesita.

Si el pedido trata de un nodo, seguí la sección 7 de las reglas: índice local primero, ficha del proyecto padre si existe y solo las notas pertinentes. Una colección independiente no exige crear un proyecto.

| Tarea | Qué sumar |
|---|---|
| Retomar, planificar o cerrar | Nada más, salvo información necesaria que falte en la ficha |
| Ubicar un archivo o crear carpetas | Índice y estructura real de ese proyecto |
| Comprobar una afirmación o analizar material | Las fuentes concretas relacionadas con la pregunta |
| Escribir un mensaje breve | Destinatario, objetivo y datos necesarios; pueden estar en el pedido |
| Preparar un informe, carta o propuesta con estructura | Marco, protocolo y una guía de redacción, indicados abajo |

## Guías de escritura, cuando hagan falta

- `00_CORE/molecules/marco-comunicacion-general.md`: elegir destinatario, intención y estructura.
- `00_CORE/protocols/ai-write-protocol.md`: preparar y revisar un texto elaborado.
- Una guía en `00_CORE/cognitive-tools/`: A → `redaccion-tecnica.md`, B → `redaccion-narrativa.md`, C → `redaccion-persuasiva.md`, D → `redaccion-operativa.md`.

El tipo de texto puede diferir del contexto habitual del proyecto. Elegí por la tarea sin pedir al principiante que conozca las letras. No cargues las cuatro guías.

## Si falta contexto

Pedí el archivo o dato concreto que falta. No interpretes la ausencia de un adjunto como ausencia del archivo en la bóveda. En un chat sin acceso a archivos, ofrecé trabajar con lo disponible e indicá qué no se puede verificar.

## Mantener la ficha útil

Conservá hechos vigentes, decisiones y próximas acciones. Los detalles largos van en notas enlazadas. Proponé archivar lo anterior antes de moverlo; no lo borres para cumplir un tamaño arbitrario.

Si necesitás ajustar el tamaño del contexto, consultá `00_CORE/davidkimai-resources/evaluation/token_budgeting.md`. La cantidad depende de la tarea y del modelo; no omitas evidencia necesaria para cumplir un tamaño arbitrario.
