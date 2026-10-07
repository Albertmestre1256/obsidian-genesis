---
name: redactar
description: Escribe un texto para un proyecto con los datos necesarios y una revisión proporcional a la tarea
argument-hint: <proyecto> <qué querés escribir>
---

Proyecto: $0
Pedido completo: $ARGUMENTS

1. Leé primero `00_CORE/atoms/00_vault-rules.md` y después la ficha del proyecto. Usá `$0` como nombre corto; buscá también por la propiedad `proyecto` (aprender-python usa ejemplo-context.md). Ante varias coincidencias, preguntá cuál corresponde.
2. Identificá destinatario, objetivo y restricciones a partir del pedido y la ficha. Preguntá solo por datos que cambien el resultado. Si falta un dato que puede quedar pendiente, marcá `[FALTA: ...]`.
3. Para un mensaje breve, redactá directamente en el chat y revisá claridad y hechos. Para un informe, carta o propuesta que necesite estructura, cargá las guías de `00_CORE/protocols/context-injection.md`, presentá un plan corto y esperá su aprobación, salvo que ya se haya aprobado ese alcance. Elegí el tipo de comunicación por la tarea; no exijas que el usuario conozca A/B/C/D.
4. Usá hechos de la ficha y fuentes pertinentes disponibles. No presentes una inferencia como hecho, una intención como logro ni una propuesta como decisión.
5. Si se pidió guardar el borrador, comprobá la carpeta del proyecto y proponé una ruta libre, normalmente en `02_SINTESIS/`, con versión (`mail_coordinacion_v1.md`). Guardá solo con autorización para esa escritura; conservá archivos anteriores. Si no tenés acceso, entregá el texto y su ruta sugerida. Redactar no autoriza enviar ni publicar el texto.
