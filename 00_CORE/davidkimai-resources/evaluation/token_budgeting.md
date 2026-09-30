---
level: resource
tipo: token-budgeting
descripcion: Cuánto contexto darle a la IA — presupuesto orientativo de tokens por pieza
---

# Presupuesto de contexto (tokens)

Un *token* es un pedacito de texto (más o menos, 3 o 4 letras). Las IAs actuales aceptan textos muy largos, pero **darles más contexto del necesario empeora las respuestas**: se distraen, mezclan información vieja con la vigente y cuesta más. Por eso el kit carga solo lo justo.

## Cuánto ocupa cada pieza (aprox.)

| Pieza | Tokens aprox. | ¿Cuándo se carga? |
|---|---|---|
| Átomo (`00_vault-rules.md`) | ~400 | Siempre |
| Célula del proyecto | 300 a 3000 | Siempre |
| Marco de comunicación | ~900 | Solo para escribir algo para otra persona |
| Guía de redacción (A, B, C o D) | ~300 | Solo para escribir, la del contexto del texto |
| Protocolo de escritura | ~350 | Solo para escribir |

## Topes

- **Orientarse, planificar, actualizar la célula** (`/empezar`, `/cerrar`): átomo + célula → **menos de 3500 tokens**.
- **Escribir un texto** (`/redactar`): átomo + célula + marco + guía + protocolo → **menos de 5000 tokens**.
- **La célula no debería pasar de ~3000 tokens.** El validador avisa si se pasa: resumí o mové lo viejo a `_archivo`.

## Reglas
- Nunca cargar índices, otros proyectos ni guías que no correspondan a la tarea.
- Si un dato de la célula ya no es vigente, sacarlo: lo viejo confunde más de lo que ayuda.
