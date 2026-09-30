---
name: redactar
description: Escribe un texto (mail, informe, carta, propuesta...) usando el contexto del proyecto
argument-hint: <proyecto> <qué querés escribir>
---

Proyecto: $0
Pedido completo: $ARGUMENTS

1. Usá `$0` como nombre corto del proyecto; el resto del pedido indica qué escribir. Si la célula no coincide con el nombre del archivo, buscala por su propiedad `proyecto` (por ejemplo, aprender-python usa ejemplo-context.md). Si falta algo (para quién es, para qué, largo aproximado), preguntámelo antes de seguir.
2. Cargá **solo** esto:
   - `00_CORE/atoms/00_vault-rules.md`
   - `00_CORE/molecules/marco-comunicacion-general.md`
   - la célula `00_CORE/cells/<proyecto>-context.md`
   - la herramienta de redacción que corresponda: contexto A → `00_CORE/cognitive-tools/redaccion-tecnica.md`; contexto B → `00_CORE/cognitive-tools/redaccion-narrativa.md`; contexto C → `00_CORE/cognitive-tools/redaccion-persuasiva.md`; contexto D → `00_CORE/cognitive-tools/redaccion-operativa.md`.
3. Decidí el contexto (A, B, C o D) de **este texto** —puede ser distinto del contexto dominante del proyecto— y decímelo en una línea con el porqué.
4. Seguí `00_CORE/protocols/ai-write-protocol.md`. Antes de escribir el borrador, mostrame el plan (fases 1 y 2) en pocas líneas y esperá mi OK.
5. Usá solo hechos de la sección **Hechos clave** de la célula. Si el texto necesita un dato que no está, poné `[FALTA: ...]` en vez de inventarlo.
6. Proponé una ruta que no exista y guardá el borrador solo si el plan aprobado incluye esa escritura. Verificá la carpeta real del proyecto; si falta, proponé crearla. El destino habitual es `<proyecto>/02_SINTESIS/`, con un nombre como `<tipo>_<tema>_v1.md` (ejemplo: `mail_presupuesto-imprenta_v1.md`).
