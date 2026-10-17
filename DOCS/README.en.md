---
tipo: guia-documentos
descripcion: "What each kit document contains, what it does and when to consult it."
---
> [!info]- Índice de esta nota (líneas)
> - Líneas 1–4: Propiedades
> - Líneas 5–17: Este índice
> - Líneas 19–26: Guide to the kit documents and tools
> - Líneas 27–37: Contents of this guide
> - Líneas 38–47: Entry points
> - Líneas 48–65: Rules and projects
> - Líneas 66–85: Help
> - Líneas 86–99: Integrations and settings
> - Líneas 100–113: Python and tests
> - Líneas 114–124: Repository and credits
> - Líneas 125–133: Optional resources
> - Líneas 134–146: Files created during use

# Guide to the kit documents and tools

**Main README and its languages:** [Español](../README.md) · [English](../README.en.md) · [Deutsch](../README.de.md) · [中文](../README.zh.md)

**This guide in other languages:** [Español](README.md) · [English](README.en.md) · [Deutsch](README.de.md) · [中文](README.zh.md)

You do not need to read everything to begin: follow the main README and answer your AI’s questions. Use this guide to understand the files or find help. File paths are the same in every language; the kit’s shared instructions remain in Spanish. This guide describes the complete repository and is read in the downloaded kit folder. When integrating the kit into another vault, it stays here with the tests and development documentation; usage help is copied.

## Contents of this guide

- [Entry points](#entry-points)
- [Rules and projects](#rules-and-projects)
- [Help](#help)
- [Integrations and settings](#integrations-and-settings)
- [Python and tests](#python-and-tests)
- [Repository and credits](#repository-and-credits)
- [Optional resources](#optional-resources)
- [Files created during use](#files-created-during-use)

## Entry points

| Document or tool | Purpose |
|---|---|
| [`README.md`](../README.md) · [`README.en.md`](../README.en.md) · [`README.de.md`](../README.de.md) · [`README.zh.md`](../README.zh.md) | Start, project status and setup prompt for an AI. |
| [`LEER_PRIMERO.md`](../LEER_PRIMERO.md) | Entry note connecting the Panel, map and rules. |
| [`Panel.md`](../Panel.md) | Daily access to projects and tasks. |
| [`INDICE.md`](../INDICE.md) | Actual vault-wide catalog; the AI reads it first. |
| [`AI-INSTRUCTIONS.md`](../AI-INSTRUCTIONS.md) · [`AGENTS.md`](../AGENTS.md) · [`CLAUDE.md`](../CLAUDE.md) | The assistant entry selects the workflow; AGENTS and CLAUDE point to it. |

## Rules and projects

| Document or tool | Purpose |
|---|---|
| [`00_CORE/atoms/00_vault-rules.md`](../00_CORE/atoms/00_vault-rules.md) | Shared rules for context, preservation, links and authorship. |
| [`00_CORE/protocols/configurar-vault.md`](../00_CORE/protocols/configurar-vault.md) | Setup interview and vault creation with incomplete details. |
| [`00_CORE/protocols/personalizar-vault.md`](../00_CORE/protocols/personalizar-vault.md) | Inventory of answers, omissions and details that can be completed later. |
| [`00_CORE/protocols/context-injection.md`](../00_CORE/protocols/context-injection.md) | What context to load for a request, without reading the whole vault. |
| [`00_CORE/protocols/ai-write-protocol.md`](../00_CORE/protocols/ai-write-protocol.md) | Prepare, draft and review text with sufficient context. |
| [`00_CORE/molecules/marco-comunicacion-general.md`](../00_CORE/molecules/marco-comunicacion-general.md) | Choose the purpose, audience and communication style. |
| [`00_CORE/cognitive-tools/redaccion-tecnica.md`](../00_CORE/cognitive-tools/redaccion-tecnica.md) · [`00_CORE/cognitive-tools/redaccion-narrativa.md`](../00_CORE/cognitive-tools/redaccion-narrativa.md) · [`00_CORE/cognitive-tools/redaccion-operativa.md`](../00_CORE/cognitive-tools/redaccion-operativa.md) · [`00_CORE/cognitive-tools/redaccion-persuasiva.md`](../00_CORE/cognitive-tools/redaccion-persuasiva.md) | Technical, narrative, operational and persuasive writing guides, as needed. |
| [`00_CORE/cells/ejemplo-context.md`](../00_CORE/cells/ejemplo-context.md) | Fictional example of a context note; it is not your data. |
| [`00_CORE/templates/TEMPLATE_cell.md`](../00_CORE/templates/TEMPLATE_cell.md) | Project context note template. |
| [`00_CORE/templates/TEMPLATE_configuracion.md`](../00_CORE/templates/TEMPLATE_configuracion.md) | Template for setup and an optional, resumable profile inventory. |
| [`00_CORE/templates/TEMPLATE_nodo.md`](../00_CORE/templates/TEMPLATE_nodo.md) | Index template for a collection of notes. |
| [`PROJECT_TEMPLATE/00 - Índice y Contexto.md`](../PROJECT_TEMPLATE/00%20-%20%C3%8Dndice%20y%20Contexto.md) | Basis for the linked index of each new project. |
| [`PROJECT_TEMPLATE/01_FUENTES/README.md`](../PROJECT_TEMPLATE/01_FUENTES/README.md) · [`PROJECT_TEMPLATE/02_SINTESIS/README.md`](../PROJECT_TEMPLATE/02_SINTESIS/README.md) · [`PROJECT_TEMPLATE/03_ENTREGABLES/README.md`](../PROJECT_TEMPLATE/03_ENTREGABLES/README.md) · [`PROJECT_TEMPLATE/_archivo/README.md`](../PROJECT_TEMPLATE/_archivo/README.md) | Explain where originals, work, outputs and history belong. |

## Help

| Document or tool | Purpose |
|---|---|
| [`DOCS/QUICKSTART.md`](../DOCS/QUICKSTART.md) | Shortcut to the main start and access guides. |
| [`DOCS/empezar-con-ia.md`](../DOCS/empezar-con-ia.md) | Give real folder access or work with an attached copy. |
| [`DOCS/opencode.md`](../DOCS/opencode.md) | Open the kit and use its commands in OpenCode. |
| [`DOCS/chatgpt.md`](../DOCS/chatgpt.md) | ChatGPT workflows with a folder or attachments. |
| [`DOCS/usar-con-otras-ias.md`](../DOCS/usar-con-otras-ias.md) | Everyday requests to resume, draft or save progress. |
| [`DOCS/primer-proyecto.md`](../DOCS/primer-proyecto.md) | Create a project manually as an alternative. |
| [`DOCS/instalacion-manual.md`](../DOCS/instalacion-manual.md) | Integrate the kit without running Python. |
| [`DOCS/creacion-para-asistentes.md`](../DOCS/creacion-para-asistentes.md) | Technical reference for an AI preparing project files. |
| [`DOCS/indice-principal.md`](../DOCS/indice-principal.md) | Maintain the map, local indexes and scalable links. |
| [`DOCS/mantenimiento.md`](../DOCS/mantenimiento.md) | Update line ranges, maps and logs, and verify closure. |
| [`DOCS/obsidian.md`](../DOCS/obsidian.md) | Templates, Panel, Bases and graph inside Obsidian. |
| [`DOCS/TROUBLESHOOTING.md`](../DOCS/TROUBLESHOOTING.md) | Common errors and how to diagnose a blocked step. |
| [`DOCS/mcp-claude.md`](../DOCS/mcp-claude.md) | Troubleshoot MCP connections and schemas in Claude. |
| [`DOCS/prueba-con-usuarios.md`](../DOCS/prueba-con-usuarios.md) | Script and criteria for testing with real beginners. |
| [`DOCS/publicacion.md`](../DOCS/publicacion.md) | Checks required before publishing a version. |

## Integrations and settings

| Document or tool | Purpose |
|---|---|
| [`.claude/skills/configurar/SKILL.md`](../.claude/skills/configurar/SKILL.md) · [`.opencode/commands/configurar.md`](../.opencode/commands/configurar.md) | /configurar: start the interview or resume incomplete setup. |
| [`.claude/skills/empezar/SKILL.md`](../.claude/skills/empezar/SKILL.md) · [`.opencode/commands/empezar.md`](../.opencode/commands/empezar.md) | /empezar: load project context and continue. |
| [`.claude/skills/nuevo-proyecto/SKILL.md`](../.claude/skills/nuevo-proyecto/SKILL.md) · [`.opencode/commands/nuevo-proyecto.md`](../.opencode/commands/nuevo-proyecto.md) | /nuevo-proyecto: agree on and add another project. |
| [`.claude/skills/redactar/SKILL.md`](../.claude/skills/redactar/SKILL.md) · [`.opencode/commands/redactar.md`](../.opencode/commands/redactar.md) | /redactar: write using available context and facts. |
| [`.claude/skills/validar/SKILL.md`](../.claude/skills/validar/SKILL.md) · [`.opencode/commands/validar.md`](../.opencode/commands/validar.md) | /validar: check context notes and explain errors or warnings. |
| [`.claude/skills/cerrar/SKILL.md`](../.claude/skills/cerrar/SKILL.md) · [`.opencode/commands/cerrar.md`](../.opencode/commands/cerrar.md) | /cerrar: propose saving changes and verify approved updates. |
| [`.claude/skills/vault-manager/SKILL.md`](../.claude/skills/vault-manager/SKILL.md) · [`.claude/settings.json`](../.claude/settings.json) | Vault usage guidance and Claude integration settings. |
| [`.obsidian/app.json`](../.obsidian/app.json) · [`.obsidian/core-plugins.json`](../.obsidian/core-plugins.json) · [`.obsidian/graph.json`](../.obsidian/graph.json) · [`.obsidian/templates.json`](../.obsidian/templates.json) · [`.obsidian/appearance.json`](../.obsidian/appearance.json) · [`.obsidian/snippets/genesis-vista-simple.css`](../.obsidian/snippets/genesis-vista-simple.css) | Initial settings and enabled simple view for a new vault; preserve existing settings when integrating. |
| [`Proyectos.base`](../Proyectos.base) | Project table used by the Panel; not a note or script. |

## Python and tests

Python automates tasks; you do not need to program to use the kit with an AI that can manage files. Tests are for kit developers, and the installer does not copy them into an installed vault.

| Document or tool | Purpose |
|---|---|
| [`instalar.py`](../instalar.py) | Add the kit to another vault without replacing existing files. |
| [`crear_proyecto.py`](../crear_proyecto.py) | Create the context note and folders of an agreed project. |
| [`actualizar_indice.py`](../actualizar_indice.py) | Generate or check the general index and node indexes. |
| [`00_CORE/schemas/validate.py`](../00_CORE/schemas/validate.py) | Check context notes and setup; with --cierre, verify an operation. |
| [`00_CORE/schemas/note_index.py`](../00_CORE/schemas/note_index.py) | Compute and check line ranges in editable notes. |
| [`00_CORE/schemas/registrar_cambios.py`](../00_CORE/schemas/registrar_cambios.py) | Record authorship, changed files and preserved history. |
| [`tests/conftest.py`](../tests/conftest.py) · [`tests/test_crear_proyecto.py`](../tests/test_crear_proyecto.py) · [`tests/test_indice.py`](../tests/test_indice.py) · [`tests/test_instalar.py`](../tests/test_instalar.py) · [`tests/test_kit.py`](../tests/test_kit.py) · [`tests/test_mantenimiento.py`](../tests/test_mantenimiento.py) · [`tests/test_nodos.py`](../tests/test_nodos.py) · [`tests/test_validate.py`](../tests/test_validate.py) | Shared fixtures and tests for creation, indexes, installation, packaging, maintenance, nodes and validation. |

## Repository and credits

| Document or tool | Purpose |
|---|---|
| [`LICENSE`](../LICENSE) | MIT license and attribution to davidkimai and Albert Mestre. |
| [`CHANGELOG.md`](../CHANGELOG.md) | Kit changes by version or date. |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | How to contribute, ask for help and check changes. |
| [`.github/ISSUE_TEMPLATE/no-me-funciona.md`](../.github/ISSUE_TEMPLATE/no-me-funciona.md) | Short template for reporting a failure with fictional sample data. |
| [`.github/workflows/tests.yml`](../.github/workflows/tests.yml) | Definition of remote GitHub Actions tests. |
| [`.gitignore`](../.gitignore) | Local files Git should ignore. |

## Optional resources

| Document or tool | Purpose |
|---|---|
| [`00_CORE/davidkimai-resources/README.md`](../00_CORE/davidkimai-resources/README.md) | Entry to resources adapted from the original work; optional reading. |
| [`00_CORE/davidkimai-resources/protocols/01_extract_information.md`](../00_CORE/davidkimai-resources/protocols/01_extract_information.md) | Extract information from a source without inventing missing details. |
| [`00_CORE/davidkimai-resources/evaluation/token_budgeting.md`](../00_CORE/davidkimai-resources/evaluation/token_budgeting.md) | Choose enough context without loading irrelevant material. |
| [`00_CORE/davidkimai-resources/field-theory/field_dynamics.md`](../00_CORE/davidkimai-resources/field-theory/field_dynamics.md) | Optional conceptual model for connecting and maintaining context. |

## Files created during use

These files do not ship with personal data: the AI creates them from your answers. Project names below are example paths, not files you need to create by hand. In example paths, `{ID}` or `ID` stands for the chosen project identifier; it is not a literal name.

| Document or tool | Purpose |
|---|---|
| `00_CORE/configuracion.md` | Answers, skipped details and setup status; supports resuming without repeating questions. |
| `00_CORE/cells/{ID}-context.md` | Each project’s context note: goal, facts, decisions and next actions. |
| `ID/00 - Índice - ID.md` | The project’s own index, connecting its notes and child nodes. An independent node also has an index. |
| `ID/01_FUENTES/ · ID/02_SINTESIS/ · ID/03_ENTREGABLES/ · ID/_archivo/` | Original material, work in progress, outputs and historical material within the agreed scope. |
| `00_CORE/logs/registro-cambios.md · 00_CORE/logs/historial/` | Identified change log; renewal after five days preserves the previous log in the archive. |

The general index maintains the actual inventory. This guide explains purposes; it does not replace the rules or require loading every document into each conversation.
