---
tipo: indice-proyecto
proyecto: "[completar: nombre-corto-del-proyecto]"
contexto: "[completar: A, B, C o D]"
creado:
---

# [completar: Nombre del proyecto]

> **Reglas del vault:** [[00_vault-rules]]
> **Célula del proyecto:** [[completar-nombre-corto-context]] ← cambiá este enlace por el de tu célula (en `00_CORE/cells/`)

%% Esta es la portada del proyecto: sirve para navegar. Lo que la IA necesita saber (hechos, decisiones, próximos pasos) va en la célula, no acá. %%

---

## Qué es

[completar: de qué se trata el proyecto, en 2 o 3 líneas]

---

## Dónde está cada cosa

| Carpeta | Qué va ahí |
|---|---|
| `01_FUENTES/` | Material original: PDFs, chats exportados, datos. Solo se agregan archivos, no se editan. |
| `02_SINTESIS/` | Trabajo en curso: notas, análisis, borradores. |
| `03_ENTREGABLES/` | Versiones finales, numeradas (`_v1`, `_v2`...). |
| `_archivo/` | Lo que ya no está vigente. No se borra: se archiva. |

---

## Comandos (si usás Claude Code)

```bash
/empezar <proyecto>           # arrancar la sesión con el contexto justo
/redactar <proyecto> <qué>    # escribir algo usando la célula
/cerrar <proyecto>            # guardar en la célula lo que cambió hoy
/validar                      # revisar que las células estén bien
```

> ¿Usás otra IA? Usá los prompts listos para pegar en `DOCS/usar-con-otras-ias.md`.

---

## Flujo de trabajo recomendado

1. **Empezar** — `/empezar <proyecto>`: la IA lee la célula y te dice dónde quedaste
2. **Trabajar** — material nuevo a `01_FUENTES/`, borradores en `02_SINTESIS/`
3. **Escribir** — `/redactar <proyecto> <qué>` cuando necesites producir un texto
4. **Cerrar** — `/cerrar <proyecto>`: la célula queda al día para la próxima sesión

---

## Referencias

- [[00_vault-rules]] — reglas del vault
- [[marco-comunicacion-general]] — cómo comunicar según el contexto (A, B, C, D)
- [[ai-write-protocol]] — cómo escribir con IA
- [[context-injection]] — qué contexto darle a la IA

---

*Basado en [Context Engineering](https://github.com/davidkimai/Context-Engineering) de davidkimai.*
