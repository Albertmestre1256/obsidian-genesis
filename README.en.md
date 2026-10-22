> **Main credit to [davidkimai](https://github.com/davidkimai):** this kit is based on their work [Context Engineering](https://github.com/davidkimai/Context-Engineering). Obsidian Genesis adapts that work to start and organize Obsidian vaults with the help of an AI.

> [!info]- Índice de esta nota (líneas)
> - Líneas 1–1: Atribución
> - Líneas 3–19: Este índice
> - Líneas 21–22: Introducción
> - Líneas 23–28: Obsidian Genesis: your vault, set up by an AI
> - Líneas 29–40: What each thing is
> - Líneas 41–59: Get started in three steps
> - Líneas 60–68: What you get
> - Líneas 69–76: Everyday use
> - Líneas 77–97: Guides
> - Líneas 98–113: What is in the folder
> - Líneas 114–119: Project status
> - Líneas 120–123: Privacy
> - Líneas 124–127: License
> - Líneas 128–131: Community and support
> - Líneas 132–135: Support the project
> - Líneas 136–138: About the development

**Language:** [Español](README.md) · English · [Deutsch](README.de.md) · [中文](README.zh.md)

# Obsidian Genesis: your vault, set up by an AI

Obsidian Genesis is a free kit to start using [Obsidian](https://obsidian.md) without knowing how it works. You give this folder to an AI that can read and write files, answer a few simple questions, and the AI builds your vault: your first project, a panel to get in and an index it keeps up to date. You don't need to program.

It works for study, work or any personal project. The kit is in Spanish: you can write to the assistant in your own language, but the kit's notes and guides stay in Spanish for now. This README and the document guide are also available in Spanish, German and Chinese.

## What each thing is

| Term | What it is |
|---|---|
| Vault | The folder of notes you open with Obsidian. |
| Project card | A note with a project's goal, verified facts and next actions. |
| Panel | The home page: your projects and pending tasks. |
| General index | `INDICE.md`, the map of every file. The AI reads it first and keeps it up to date. |
| Node | A topic folder with its own index, for example "Course summaries". |

The AI works with the kit's rules and guides: it asks before writing, explains where it will save each thing and checks the files when it finishes.

## Get started in three steps

1. **Download and unzip** the repository: Code → Download ZIP.
2. **Open the folder in an AI that can read and write files.** Choose the one that contains this README and `AI-INSTRUCTIONS.md`.
3. **Paste this message and answer its questions:**

   > I want you to set up my Obsidian vault with this kit. First read `INDICE.md`, then `00_CORE/atoms/00_vault-rules.md` and `AI-INSTRUCTIONS.md`. I don't know Obsidian: guide me with simple questions, one or two at a time, and take care of the files based on my answers. Before writing, explain where you will save everything and what you will create. Keep the main index up to date. If you don't have access to do it, tell me.

| You use | How to open the kit |
|---|---|
| Claude Code | Open the folder and use the message above or `/configurar`. |
| OpenCode | Open the folder and use the message above or `/configurar`. [Guide](DOCS/opencode.md). |
| ChatGPT | Local folder with file tools, or an attached copy. [Guide](DOCS/chatgpt.md). |
| Another AI | Give it access to the folder and use the same message. |

The AI asks what you want to organize, which notes to keep and what the goal is. You can answer "I don't know yet" or "I have no deadline": the first task can be chosen later. If you attach a ZIP instead of giving access to the folder, the [quick start](DOCS/QUICKSTART.md) explains what you can get back.

If you already have a vault, the kit does not adapt it: use it in a new folder. Adapting existing vaults will be a separate repository, not available yet.

## What you get

- A folder ready to open as a vault, with your first project and its card.
- The **Panel** (`Panel.md`) to reach your projects and tasks, and **Leer primero** (`LEER_PRIMERO.md`, "Read first"), which connects the Panel with the general index.
- A simple view: the file explorer shows your notes and hides the kit's technical files. Obsidian's **Graph view**, from its sidebar icon, shows how they connect.
- An optional, collapsed **personalization inventory**: what you answered, what is pending and what you chose to skip. You can complete it whenever you like with **"what is missing to personalize my vault"**. [How it works](00_CORE/protocols/personalizar-vault.md).

To open it, install Obsidian from [obsidian.md](https://obsidian.md), open the prepared folder as a vault and go to `Panel.md`. The AI checks the files; you check how it looks in Obsidian.

## Everyday use

- **Resume:** say **"Continue with [project]"** or use `/empezar`. The AI reads the index, the rules and the project card, and picks up what is pending.
- **Other requests:** another project, a draft, a review or saving the day's closing. [Ready-to-use requests](DOCS/usar-con-otras-ias.md).
- **Organize more content:** ask **"Add a node for summaries of my courses"**. The AI creates its index and connects it to the general map. [How nodes work](DOCS/indice-principal.md).

Claude Code and OpenCode include `/configurar`, `/empezar`, `/nuevo-proyecto`, `/redactar`, `/validar` and `/cerrar`; in Claude, creating another project and closing are invoked manually. Permissions depend on the assistant. If you work with attachments, always share the current notes: they don't sync on their own.

## Guides

The guides are in Spanish, except the document guide.

| If you want to… | Read |
|---|---|
| See the ways to give the folder to an AI | [Quick start](DOCS/QUICKSTART.md) |
| Use ChatGPT | [Getting started with ChatGPT](DOCS/chatgpt.md) |
| Use OpenCode | [Getting started with OpenCode](DOCS/opencode.md) |
| Fix Claude's connection to Obsidian (MCP) | [If Claude does not connect to the MCP](DOCS/mcp-claude.md) |
| Learn the everyday requests | [Working with an AI](DOCS/usar-con-otras-ias.md) |
| Create a project without an AI | [Your first project by hand](DOCS/primer-proyecto.md) |
| Understand the Panel, templates and simple view | [Templates and panel](DOCS/obsidian.md) |
| Add nodes and understand the general map | [General map and node indexes](DOCS/indice-principal.md) |
| See how changes are recorded and checked | [Maintenance](DOCS/mantenimiento.md) |
| Use the five optional skills | [Optional skills](DOCS/skills-portables.md) |
| Solve a problem | [Troubleshooting](DOCS/TROUBLESHOOTING.md) |
| See what each kit file does | [Guide to documents and tools](DOCS/README.en.md) |

**For assistants and kit development:** [entry for the AI](AI-INSTRUCTIONS.md) · [vault rules](00_CORE/atoms/00_vault-rules.md) · [setup protocol](00_CORE/protocols/configurar-vault.md) · [project creator](DOCS/creacion-para-asistentes.md) · [how to contribute](CONTRIBUTING.md) · [user testing](DOCS/prueba-con-usuarios.md) · [publishing](DOCS/publicacion.md) · [changelog](CHANGELOG.md).

## What is in the folder

| Place | What for |
|---|---|
| `Panel.md` | Access to projects and tasks |
| `LEER_PRIMERO.md` | Entry note for the person and connection of the general nodes |
| `INDICE.md` | Catalog of files and projects; the AI's first read |
| `00_CORE/` | Rules, project cards, templates and tools |
| `PROJECT_TEMPLATE/` | A project's folders: sources, drafts, deliverables and archive |
| `skills/` | Five optional skills |
| `DOCS/` | Guides |

The `aprender-python` example is fictional and kept apart from your projects. Your data comes from your answers; whatever you don't know can stay empty.

Python 3.8 or later automates creation, validation and the index with the standard library. Without Python, the AI uses its file tools.

## Project status

Version 1.0, the first publishable release. Conversational setup with a resumable profile, the project creator, connected nodes and indexes, change recording and validation all work. Automated tests pass on Windows, macOS and Ubuntu with Python 3.8 and 3.13; that does not show the kit is easy to use.

Setup and resumption were checked with Claude Code, and setup with ChatGPT web. Still pending: resumption in ChatGPT web and OpenCode, a test with five beginners and the final visual review in Obsidian. Details are in the [changelog](CHANGELOG.md) (in Spanish).

## Privacy

The kit stores local files and does not install synchronization. The AI processes what you share according to its service and settings: give it only the context it needs.

## License

[MIT](LICENSE), with credits to davidkimai and Albert Mestre. Independent adaptation of Context Engineering, not affiliated with the original project.

## Community and support

For questions, ideas and experiences, use the [community discussions](https://github.com/Albertmestre1256/obsidian-genesis/discussions). If something fails, open a [bug report](https://github.com/Albertmestre1256/obsidian-genesis/issues) using the “No me funciona” template and a small example with fictional data. [How to contribute](CONTRIBUTING.md) (in Spanish).

## Support the project

Obsidian Genesis is free and will stay free. If you find it useful, you can support it on [Patreon](https://www.patreon.com/obsidiangenesis). Contributions help fund time for beginner guides, testing with real people, translations and support. They are optional: they do not unlock features, and the whole kit remains public.

## About the development

Albert Mestre develops this adaptation with substantial contributions from **OpenCode, Claude and Codex (OpenAI)**, which helped build an important part of the code and supported documentation and testing. They are credited here as contributing AI tools. Proposals are reviewed and results are verified before they are integrated; using AI does not replace tests with people and does not by itself show that the kit is easy to use.
