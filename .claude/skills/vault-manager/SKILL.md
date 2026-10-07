---
name: vault-manager
description: Orienta la configuración y el trabajo diario en una bóveda de Obsidian con este kit, eligiendo el recorrido de inicio, proyecto, escritura o cierre. No usar para desarrollar o revisar el propio kit.
---

# Vault Manager

Este vault guarda el contexto de cada proyecto en una **célula** (`00_CORE/cells/<proyecto>-context.md`): una nota corta de Obsidian con lo que es verdad y está vigente. La IA trabaja leyendo solo lo necesario, en vez de todo el vault.

## Qué pide el usuario → qué hacer

| Si el usuario dice algo como... | Orientación disponible |
|---|---|
| "quiero trabajar en X", "sigamos con X" | `.claude/skills/empezar/SKILL.md` |
| "tengo un proyecto nuevo", "armemos un proyecto" | `.claude/skills/nuevo-proyecto/SKILL.md` |
| "escribime / redactá / armá un mail, informe, carta..." | `.claude/skills/redactar/SKILL.md` |
| "¿está todo bien?", "revisá las células" | `.claude/skills/validar/SKILL.md` |
| "terminamos", "guardá lo de hoy", "actualizá la célula" | `.claude/skills/cerrar/SKILL.md` |
| "no sé por dónde empezar", "¿cómo funciona esto?" | Leé `00_CORE/protocols/configurar-vault.md` e iniciá la conversación guiada, sin enviarlo a copiar plantillas manualmente |

La configuración inicial usa `00_CORE/protocols/configurar-vault.md` y puede crear el primer proyecto dentro del alcance acordado. Para agregar proyectos después, usá la ruta de nuevo-proyecto. No inicies la configuración cuando se pida desarrollar el kit.

## Reglas que valen siempre

- Leer primero `00_CORE/atoms/00_vault-rules.md`.
- Cargar el mínimo contexto posible (ver `00_CORE/protocols/context-injection.md`). Nunca mezclar proyectos.
- `01_FUENTES/` no se edita: solo se agregan archivos. Los borradores van a `02_SINTESIS/`; las versiones finales, a `03_ENTREGABLES/`.
- No inventar hechos. Si falta un dato, preguntarlo o marcarlo `[FALTA: ...]`.
- Después de modificar una célula, correr `python 00_CORE/schemas/validate.py` si hay Python. Si falta, usar la revisión manual de `.claude/skills/validar/SKILL.md` y aclararlo.
- Los bloques entre `%%` son ayuda para el usuario: ignorarlos al leer una célula.
- Hablar en lenguaje simple: el usuario puede no saber cómo funciona Obsidian ni qué son las propiedades de una nota.

## Mapa del vault

- `00_CORE/atoms/` — reglas del vault
- `00_CORE/molecules/` — marco de comunicación (contextos A, B, C, D)
- `00_CORE/cells/` — una célula por proyecto (+ plantilla y ejemplo)
- `00_CORE/protocols/` — cómo escribir con IA y cómo cargar contexto
- `00_CORE/cognitive-tools/` — guías de redacción, una por contexto (A, B, C, D)
- `00_CORE/schemas/validate.py` — revisa las células
- `<proyecto>/01_FUENTES/`, `02_SINTESIS/`, `03_ENTREGABLES/` — material de cada proyecto

Para crear o cerrar proyectos, indicá al usuario que invoque `/nuevo-proyecto` o `/cerrar`: esas skills son manuales. No las actives indirectamente ni escribas por una frase ambigua.
