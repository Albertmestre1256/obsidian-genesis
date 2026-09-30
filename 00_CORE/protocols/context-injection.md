---
level: organ
tipo: context-injection-protocol
descripcion: Qué contexto darle a la IA en cada tarea — solo lo necesario
---

# Protocolo de Inyección de Contexto

## Regla de oro
Darle a la IA **solo lo que necesita para esta tarea**. Más contexto no es mejor: la distrae y la hace mezclar información vieja con la vigente.

## Qué cargar según la tarea

**Para orientarse, planificar o actualizar la célula** (`/empezar`, `/cerrar`):
1. `00_CORE/atoms/00_vault-rules.md` — reglas del vault
2. `00_CORE/cells/<proyecto>-context.md` — célula del proyecto

**Para escribir algo que va a leer otra persona** (`/redactar`), además:
3. `00_CORE/molecules/marco-comunicacion-general.md` — marco de comunicación
4. La guía de redacción del contexto del texto, en `00_CORE/cognitive-tools/`: A → `redaccion-tecnica.md` · B → `redaccion-narrativa.md` · C → `redaccion-persuasiva.md` · D → `redaccion-operativa.md`
5. `00_CORE/protocols/ai-write-protocol.md` — pasos para escribir

## Qué NO cargar (salvo que el usuario lo pida)
- Índices de proyecto: sirven para navegar, no para trabajar
- Otros proyectos: mezclan información
- Guías de redacción de otros contextos
- Conversaciones anteriores, salvo que haga falta continuidad

## Presupuesto
- Orientarse: menos de 3500 tokens. Escribir: menos de 5000 tokens.
- Detalle en `00_CORE/davidkimai-resources/evaluation/token_budgeting.md`.

## Mantener la célula liviana
- Lo que ya no es vigente se saca de la célula (o se mueve a `_archivo`).
- Una sesión nueva nunca debería arrancar con información vieja.
