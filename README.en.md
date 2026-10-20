> **Main credit to [davidkimai](https://github.com/davidkimai):** this kit is based on their work [Context Engineering](https://github.com/davidkimai/Context-Engineering). Obsidian Genesis adapts that work to start and organize Obsidian vaults with the help of an AI.
> [!info]- Índice de esta nota (líneas)
> - Líneas 1–1: Atribución
> - Líneas 2–17: Este índice
> - Líneas 19–20: Introducción
> - Líneas 21–28: Obsidian Genesis: your vault, set up by an AI
> - Líneas 29–52: Project status — October 19, 2026
> - Líneas 53–73: Get started in three steps
> - Líneas 74–79: Attachments or an existing vault
> - Líneas 80–87: Continue
> - Líneas 88–102: What it contains
> - Líneas 103–113: Optional help
> - Líneas 114–117: Privacy
> - Líneas 118–121: License
> - Líneas 122–125: Community and support
> - Líneas 126–129: About the development
> - Líneas 130–132: Support the project

**Language:** [Español](README.md) · English · [Deutsch](README.de.md) · [中文](README.zh.md)

# Obsidian Genesis: your vault, set up by an AI

Download the kit, give the folder to an AI and answer its questions. The assistant prepares your notes and your first project following the kit's rules. You don't need to program or know Obsidian.

A **vault** is a folder of notes that you open with [Obsidian](https://obsidian.md). The kit is in Spanish and works for study, work or any personal project. You can write to the assistant in your own language; the kit's notes and guides stay in Spanish for now.

The entry note [Leer primero](LEER_PRIMERO.md) ("Read first") connects the Panel and the general index. In a new vault, the kit enables Obsidian's **Graph view**: open it from its sidebar icon to explore the connected notes, or use the local graph from a project's index.

## Project status — October 19, 2026

**Code published on `Pruebas` (`10b99b5`); not a stable release yet.** The focus is still to start a vault through simple questions, without asking the person to program or maintain the indexes.

| Already implemented | What it allows |
|---|---|
| Conversational setup | Save answers before the first project and resume whatever was left pending. |
| Optional, resumable profile | Keep a single collapsible inventory; preserve skipped data and complete only what the person chooses. |
| Connected nodes and indexes | Each collection links its parent, children and notes; general nodes link the map and Leer primero. New projects get indexes with their own names. |
| Maintenance and closing | Identify the assistant, record changes with preserved history and check project cards, Panel, profile, maps, line ranges and the consistency of the initial project. |
| Access for different AIs | Guides for Claude Code, OpenCode, ChatGPT and other assistants with file tools; a manual alternative is available. |

The project creator checks the state again before saving a project and tells blocking conditions apart from partial failures; each file is created without replacing an existing one.

The simple view reduces clutter in the file explorer and graph for new folders and can be enabled optionally in existing vaults with backups. It preserves preferences and custom searches, reporting when the kit filter remains pending.

The installer passed **40 local tests, with 1 skipped on Python 3.13**. The [remote matrix for code commit `10b99b5`](https://github.com/Albertmestre1256/obsidian-genesis/actions/runs/39100123756) finished **6/6 successfully** on Windows, macOS and Ubuntu with Python 3.8 and 3.13. These are technical results; they do not establish ease of use.

Setup and resumption were checked with Claude Code. The manual OpenCode/Big Pickle trial demonstrated continued use within one session, without establishing independent resumption. A new Codex chat resumed an earlier copy and preserved skipped information, with external context and tools. These are not tests with real beginners and do not validate the interface for all current changes.

Still pending: independent resumption in OpenCode, specific coverage of ChatGPT web, a test with five beginners (at least four without help) and the final formal visual review in Obsidian.

Community discussions are available, and you can support the project on [Patreon](https://www.patreon.com/obsidiangenesis). The README and document guide are available in Spanish, English, German and Chinese; shared kit instructions remain in Spanish. General adaptation and optimization of existing vaults will be a later phase. [Changelog](CHANGELOG.md) · [How to contribute](CONTRIBUTING.md) (both in Spanish).

## Get started in three steps

1. **Download and unzip** the repository: Code → Download ZIP.
2. **Open the folder in an AI that can read and write files.** Choose the one that contains this README and `AI-INSTRUCTIONS.md`.
3. **Paste this message and answer its questions:**

   > I want you to set up my Obsidian vault with this kit. First read `INDICE.md`, then `00_CORE/atoms/00_vault-rules.md` and `AI-INSTRUCTIONS.md`. I don't know Obsidian: guide me with simple questions, one or two at a time, and take care of the files based on my answers. Before writing, explain where you will save everything and what you will create. Keep the main index up to date. If you don't have access to do it, tell me.

| You use | How to open the kit |
|---|---|
| OpenCode | Open the folder and use the message above or `/configurar`. [Guide](DOCS/opencode.md). |
| ChatGPT | Local folder with file tools, or an attached copy. [Guide](DOCS/chatgpt.md). |
| Claude Code | Open the folder and use the message above or `/configurar`. |
| Another AI | Give it access to the folder and use the same message. |

The AI asks what you want to organize, which notes to keep and what the goal is. You can answer "I don't know yet" or "I have no deadline"; the first task can be chosen later.

It also keeps a **personalization inventory**: what you answered, what is pending and what you chose to skip. In new notes it is collapsed below the project and its progress; you can expand it when you want to review it. Introduction, CV, education, routine and how long you will use the vault are optional. You can start with the basics and later say **"what is missing to personalize my vault"** or **"let's complete my profile"**. [How it works](00_CORE/protocols/personalizar-vault.md).

**You get:** a prepared folder, the project card, a Panel to access it and an explanation of how to open it in Obsidian. The AI checks the files; the visual check happens in Obsidian. If you don't have it yet, install it from [obsidian.md](https://obsidian.md), open the prepared folder as a vault and go to `Panel.md`.

## Attachments or an existing vault

An attached ZIP does not give access to your computer. If the chat can generate files, it can return a configured copy for you to download. If it only answers with text, saving it remains pending. The [access guide](DOCS/QUICKSTART.md) explains the options.

If you already have a vault, the current integration is conservative: the AI reads its rules, compares conflicts and keeps notes and settings. Automatically reorganizing or optimizing a whole existing vault is not implemented yet; it is the later phase mentioned above.

## Continue

Say **"Continue with [project]"**. The AI first reads the index, then the rules and the current project card, and resumes what is pending. You can ask for another project, a draft, a review or to save the closing: [everyday requests](DOCS/usar-con-otras-ias.md).

To organize more content, ask **"Add a node for summaries of my courses"**. Each node has an index with links and summaries; the general map connects all nodes and the AI maintains them when adding notes. Existing indexes are kept; renaming them or reorganizing notes requires an agreed scope. [Guide](DOCS/indice-principal.md).

Claude Code and OpenCode include `/configurar`, `/empezar`, `/nuevo-proyecto`, `/redactar`, `/validar` and `/cerrar`. In Claude, creating another project and closing are invoked manually. Permissions depend on the assistant. With attachments, always share the current notes: they are not synchronized.

## What it contains

To understand what each file does and when to use it, open the [guide to documents and tools](DOCS/README.en.md).

| Place | Use |
|---|---|
| `INDICE.md` | First read: complete catalog of files and projects |
| `LEER_PRIMERO.md` | Entry note for the person and central connection of the general nodes |
| `Panel.md` | Access to projects and tasks |
| `00_CORE/` | Rules, project cards, guides and tools |
| `PROJECT_TEMPLATE/` | Folders for sources, drafts, deliverables and history |
| `DOCS/` | Optional help |

The `aprender-python` example is fictional and kept apart from your own projects. Your data is filled in from your answers; sections without information can stay empty.

## Optional help

These guides are in Spanish:

- [Create a project by hand](DOCS/primer-proyecto.md).
- [Integrate the kit without Python](DOCS/instalacion-manual.md).
- [Templates and panel](DOCS/obsidian.md).
- [Troubleshooting](DOCS/TROUBLESHOOTING.md).

Python 3.8 or later automates installation, creation, validation and the index with the standard library. The AI can also set things up using its file tools. To contribute: [CONTRIBUTING](CONTRIBUTING.md).

## Privacy

The kit stores local files and does not install synchronization. The AI processes what you share according to its service and settings: give it only the context it needs.

## License

[MIT](LICENSE), with credits to davidkimai and Albert Mestre. Independent adaptation of Context Engineering, not affiliated with the original project.

## Community and support

For questions, ideas and experiences, use the [community discussions](https://github.com/Albertmestre1256/obsidian-genesis/discussions). If something fails, open a [bug report](https://github.com/Albertmestre1256/obsidian-genesis/issues) using the “No me funciona” template and a small example with fictional data. [How to contribute](CONTRIBUTING.md) (in Spanish).

## About the development

Albert Mestre develops this adaptation with substantial contributions from **OpenCode, Claude and Codex (OpenAI)**, which helped build an important part of the code and supported documentation and testing. They are credited here as contributing AI tools. Proposals are reviewed and results are verified before they are integrated; using AI does not replace tests with people and does not by itself show that the kit is easy to use.

## Support the project

Obsidian Genesis is free and will stay free. If you find it useful, you can support it on [Patreon](https://www.patreon.com/obsidiangenesis). Contributions help fund time for beginner guides, testing with real people, translations and support. They are optional: they do not unlock features, and the whole kit remains public.
