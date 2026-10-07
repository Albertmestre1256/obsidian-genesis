---
tipo: celula
proyecto: "[completar: nombre-corto-del-proyecto]"
descripcion: "[completar: qué es este proyecto, en 1 a 3 oraciones]"
objetivo: "[completar: qué querés lograr; la fecha del objetivo es opcional]"
contexto: "[completar: A, B, C o D]"
actualizado: "{{date:YYYY-MM-DD}}"
---

# Célula del proyecto

%%
CÓMO USAR ESTA PLANTILLA
Elegí UNA de estas formas de crear la ficha:
- Con Plantillas: creá una nota VACÍA en esta carpeta, con nombre nombre-de-tu-proyecto-context.md. Usá Plantillas → Insertar plantilla y elegí TEMPLATE_cell. La propiedad actualizado se completa con la fecha.
- A mano: duplicá esta plantilla y renombrá la copia nombre-de-tu-proyecto-context.md. Reemplazá {{date:YYYY-MM-DD}} por la fecha de hoy (AAAA-MM-DD). No uses Insertar plantilla sobre esa copia: duplicaría el contenido.

En ambos casos, el nombre tiene que terminar en -context.md. Completá las propiedades y reemplazá cada [completar: ...].
Si tenés Python, revisala con: python 00_CORE/schemas/validate.py

Qué va en "contexto" (una sola letra):
  A = técnico     → informes, código, documentación (precisión y evidencia)
  B = narrativo   → cartas, ensayos, relatos personales
  C = persuasivo  → propuestas, pitch, ventas
  D = operativo   → mails, coordinación, organización del día a día

Regla de oro: acá va solo lo que es VERDAD y está VIGENTE.
Lo viejo se borra o se mueve a la carpeta _archivo del proyecto.
Estos bloques de ayuda (los que abren y cierran con dos signos de porcentaje) no se ven en modo lectura; la IA y el validador los ignoran, y podés borrarlos.
¿Querés ver una célula completa? Abrí ejemplo-context.md
%%

## Hechos clave

%% Cosas verdaderas que la IA puede usar, una por línea, cada una con de dónde sale: (fuente: ...).
Si todavía no tenés fuente, dejá (fuente: ) vacío: el validador te va a avisar para que no lo trates como comprobado. %%

- [completar: algo concreto y verdadero sobre el proyecto] (fuente: [completar: dónde se puede comprobar])

## Decisiones

%% Opcional. Lo que ya decidiste, para que la IA no te proponga lo que descartaste.
Formato: - AAAA-MM-DD: qué se decidió — porque razón %%

## Próximas acciones

%% Una tarea por línea: - [ ] pendiente, - [x] hecha. Si está en curso, agregá (en curso) al final.
En Obsidian podés marcar las tareas haciendo clic en el cuadradito. %%

- [ ] [completar: próximo paso concreto]

## Preguntas abiertas

%% Opcional. Lo que todavía no sabés. %%
