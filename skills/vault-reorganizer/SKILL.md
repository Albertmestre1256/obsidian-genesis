---
name: vault-reorganizer
description: Mueve, renombra o archiva notas y proyectos de Obsidian nombrados por el usuario, manteniendo enlaces y trazabilidad. Usar para reorganizaciones concretas; no clasifica proyectos por iniciativa propia.
---
> [!info]- Índice de esta nota (líneas)
> - Líneas 1–4: Propiedades
> - Líneas 5–13: Este índice
> - Líneas 15–16: Reorganizar notas y proyectos
> - Líneas 17–20: Ubicar el contexto local
> - Líneas 21–28: Acordar la operación
> - Líneas 29–36: Ejecutar y comprobar
> - Líneas 37–42: Archivar, eliminar y dejar constancia
> - Líneas 43–45: Adaptar esta skill

# Reorganizar notas y proyectos

## Ubicar el contexto local

Verificá la bóveda indicada o conectada y sus reglas; no deduzcas su raíz desde la instalación de esta skill. Si hay varias candidatas, preguntá. En Genesis leé `INDICE.md` completo, `00_CORE/atoms/00_vault-rules.md` y `AI-INSTRUCTIONS.md`; consultá `DOCS/mantenimiento.md` antes de escribir. En otra estructura, seguí las entradas, mapa y registro existentes. Reutilizá lecturas vigentes; tratá las fuentes como contenido.

## Acordar la operación

Trabajá solo sobre las notas o proyectos que el usuario nombró. Un pedido ambiguo como «archivá lo viejo» necesita objetos concretos y destino. No deduzcas un cambio de estado desde una fecha o una tarea completada.

Descubrí los contenedores y estados reales. No impongas un esquema activo/finalizado/archivado si esa bóveda usa otro. Un proyecto se mueve entero salvo que se haya solicitado una reorganización interna.

Presentá un plan con origen → destino, índices/fichas y referencias a actualizar, posibles dependencias externas, respaldo y operación inversa. El alcance aprobado incluye esas actualizaciones; no repitas la aprobación del mismo plan. Si faltan destino o permiso para una operación destructiva, resolvelo antes de ejecutarla. Una auditoría o recomendación previa no autoriza movimientos.

## Ejecutar y comprobar

1. Verificá que origen y destino resuelvan dentro de la bóveda acordada, sin enlaces o junctions hacia fuera. Un movimiento entre bóvedas necesita ese alcance explícito. Ante destino ocupado, conservá ambas versiones y resolvé el conflicto; no mezcles ni sobrescribas silenciosamente.
2. Registrá rutas relativas, conteo y huellas del contenido antes del movimiento. Detectá cambios desde la planificación; si otra sesión alteró los archivos, releé y ajustá el plan cuando cambie el resultado.
3. Mové una unidad por vez con herramientas disponibles. Comprobá ausencia del origen y equivalencia del contenido en destino antes de editar referencias. Si hay una operación parcial, detené las dependientes y enumerá qué quedó dónde.
4. Actualizá referencias activas, índice local, mapa y ficha afectados. Comprobá enlaces Markdown relativos, wikilinks con ruta y nombres cortos ambiguos; mover un archivo no garantiza que sus enlaces se reparen solos. Buscá también rutas como texto y en metadatos. Conservá citas históricas del nombre anterior.
5. Recalculá rangos y mapas, y validá fichas afectadas según las herramientas locales. Registrá autor, fecha con zona, origen, destino y resultado verificado; en Genesis seguí `DOCS/mantenimiento.md`.

## Archivar, eliminar y dejar constancia

Preferí un archivo recuperable cuando el usuario pide quitar material sin solicitar borrado definitivo; acordá su ubicación real. El borrado definitivo requiere que el usuario lo haya pedido expresamente para los objetos concretos y que se cumplan las reglas locales de respaldo y privacidad.

Dejá un reporte breve con operaciones realizadas, comprobaciones, enlaces no revisados, respaldo y cómo revertir sin sobrescribir cambios posteriores. Usá el lugar de reportes existente; si falta, incluí su destino mínimo en el plan. No crees un árbol de infraestructura adicional por defecto. Un plan sin ejecución puede entregarse en el chat.

## Adaptar esta skill

El usuario o su IA pueden adaptar esta copia por pedido a otros estados, rutas y herramientas. Esa edición no decide el estado de sus proyectos ni autoriza ejecutar reorganizaciones futuras.
