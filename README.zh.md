> **主要致谢：[davidkimai](https://github.com/davidkimai)。** 本工具包基于其作品 [Context Engineering](https://github.com/davidkimai/Context-Engineering)。Obsidian Genesis 改编了这项工作，借助 AI 来创建和整理 Obsidian 仓库（vault）。

> [!info]- Índice de esta nota (líneas)
> - Líneas 1–1: Atribución
> - Líneas 3–19: Este índice
> - Líneas 21–22: Introducción
> - Líneas 23–28: Obsidian Genesis：由 AI 为你配置的仓库
> - Líneas 29–40: 术语说明
> - Líneas 41–59: 三步开始
> - Líneas 60–68: 你将得到
> - Líneas 69–76: 日常使用
> - Líneas 77–97: 指南
> - Líneas 98–113: 文件夹里有什么
> - Líneas 114–119: 项目状态
> - Líneas 120–123: 隐私
> - Líneas 124–127: 许可证
> - Líneas 128–131: 社区与支持
> - Líneas 132–135: 支持本项目
> - Líneas 136–138: 关于开发

**语言：** [Español](README.md) · [English](README.en.md) · [Deutsch](README.de.md) · 中文

# Obsidian Genesis：由 AI 为你配置的仓库

Obsidian Genesis 是一个免费工具包，让你在不了解 [Obsidian](https://obsidian.md) 如何运作的情况下也能开始使用它。把这个文件夹交给一个能读写文件的 AI，回答几个简单的问题，AI 就会搭建你的仓库：你的第一个项目、一个入口面板，以及一个它会持续更新的索引。你不需要会编程。

它适用于学习、工作或任何个人项目。工具包使用西班牙语：你可以用自己的语言和助手交流，但工具包的笔记和指南目前仍为西班牙语。本 README 和文档指南也提供西班牙语、英语和德语版本。

## 术语说明

| 术语 | 含义 |
|---|---|
| 仓库（vault） | 用 Obsidian 打开的笔记文件夹。 |
| 项目卡片 | 记录项目目标、已核实的事实和下一步行动的笔记。 |
| 面板（Panel） | 首页：你的项目和待办任务。 |
| 总索引 | `INDICE.md`，所有文件的地图。AI 会首先阅读并保持其最新。 |
| 节点 | 带有自己索引的主题文件夹，例如“课程摘要”。 |

AI 按照工具包的规则和指南工作：写入前先询问，说明每样内容会保存在哪里，并在完成后检查文件。

## 三步开始

1. **下载并解压**仓库：Code → Download ZIP。
2. **在一个能读写文件的 AI 中打开该文件夹。** 选择包含本 README 和 `AI-INSTRUCTIONS.md` 的那个文件夹。
3. **粘贴以下消息并回答它的问题：**

   > 我希望你用这个工具包配置我的 Obsidian 仓库。请先阅读 `INDICE.md`，然后阅读 `00_CORE/atoms/00_vault-rules.md` 和 `AI-INSTRUCTIONS.md`。我不了解 Obsidian：请用简单的问题引导我，每次一两个，并根据我的回答处理文件。在写入之前，请告诉我你会把所有内容保存在哪里、会创建什么。请保持主索引为最新。如果你没有权限做这些，请告诉我。

| 你使用的工具 | 如何打开工具包 |
|---|---|
| Claude Code | 打开文件夹，使用上面的消息或 `/configurar`。 |
| OpenCode | 打开文件夹，使用上面的消息或 `/configurar`。[指南](DOCS/opencode.md)。 |
| ChatGPT | 带文件工具的本地文件夹，或附加的副本。[指南](DOCS/chatgpt.md)。 |
| 其他 AI | 让它访问该文件夹，并使用同样的消息。 |

AI 会询问你想整理什么、要保留哪些笔记以及目标是什么。你可以回答“我还不知道”或“我没有截止日期”：第一个任务可以以后再选。如果你附加 ZIP 文件而不是提供文件夹访问权限，[快速入门](DOCS/QUICKSTART.md)说明了你可能收到什么。

如果你已经有一个仓库，本工具包不会调整它：请在新文件夹中使用本工具包。调整现有仓库将是一个单独的仓库，目前尚未提供。

## 你将得到

- 一个可以作为仓库打开的文件夹，包含你的第一个项目及其项目卡片。
- **面板**（`Panel.md`）用于进入你的项目和任务；**Leer primero**（`LEER_PRIMERO.md`，“请先阅读”）把面板与总索引连接起来。
- 简洁视图：文件列表显示你的笔记，隐藏工具包的技术文件。从侧边栏图标打开 Obsidian 的**关系图谱**，可以看到笔记之间的连接。
- 一份可选、默认折叠的**个性化清单**：你已回答的、待定的以及你选择跳过的内容。你可以随时说 **“个性化我的仓库还缺什么”** 来完善它。[工作原理](00_CORE/protocols/personalizar-vault.md)。

打开方法：从 [obsidian.md](https://obsidian.md) 安装 Obsidian，将准备好的文件夹作为仓库打开，然后进入 `Panel.md`。AI 会检查文件；在 Obsidian 中的显示效果由你来确认。

## 日常使用

- **继续：** 说 **“继续 [项目]”** 或使用 `/empezar`。AI 会阅读索引、规则和项目卡片，并继续待办事项。
- **其他请求：** 另一个项目、草稿、审阅或保存当天的收尾。[现成的请求](DOCS/usar-con-otras-ias.md)。
- **整理更多内容：** 说 **“添加一个节点，用于我的课程摘要”**。AI 会创建它的索引并连接到总地图。[节点如何运作](DOCS/indice-principal.md)。

Claude Code 和 OpenCode 包含 `/configurar`、`/empezar`、`/nuevo-proyecto`、`/redactar`、`/validar` 和 `/cerrar`；在 Claude 中，创建另一个项目和收尾需要手动调用。权限取决于所用的助手。使用附件时，请始终分享最新的笔记：它们不会自动同步。

## 指南

除文档指南外，以下指南均为西班牙语。

| 如果你想…… | 请阅读 |
|---|---|
| 了解把文件夹交给 AI 的方式 | [快速入门](DOCS/QUICKSTART.md) |
| 使用 ChatGPT | [ChatGPT 入门](DOCS/chatgpt.md) |
| 使用 OpenCode | [OpenCode 入门](DOCS/opencode.md) |
| 解决 Claude 与 Obsidian 的连接问题（MCP） | [Claude 无法连接 MCP 时](DOCS/mcp-claude.md) |
| 了解日常请求 | [与 AI 协作](DOCS/usar-con-otras-ias.md) |
| 不用 AI 创建项目 | [手动创建第一个项目](DOCS/primer-proyecto.md) |
| 了解面板、模板和简洁视图 | [模板和面板](DOCS/obsidian.md) |
| 添加节点并了解总地图 | [总地图和节点索引](DOCS/indice-principal.md) |
| 了解变更如何记录和检查 | [维护](DOCS/mantenimiento.md) |
| 使用五个可选 skill | [可选 skill](DOCS/skills-portables.md) |
| 解决问题 | [故障排除](DOCS/TROUBLESHOOTING.md) |
| 查看工具包每个文件的作用 | [文档与工具指南](DOCS/README.zh.md) |

**面向助手和工具包开发：** [AI 入口](AI-INSTRUCTIONS.md) · [仓库规则](00_CORE/atoms/00_vault-rules.md) · [配置流程](00_CORE/protocols/configurar-vault.md) · [项目创建器](DOCS/creacion-para-asistentes.md) · [如何贡献](CONTRIBUTING.md) · [用户测试](DOCS/prueba-con-usuarios.md) · [发布](DOCS/publicacion.md) · [更新日志](CHANGELOG.md)。

## 文件夹里有什么

| 位置 | 用途 |
|---|---|
| `Panel.md` | 访问项目和任务 |
| `LEER_PRIMERO.md` | 面向使用者的入口笔记，也是各总节点的连接 |
| `INDICE.md` | 文件和项目目录；AI 首先阅读 |
| `00_CORE/` | 规则、项目卡片、模板和工具 |
| `PROJECT_TEMPLATE/` | 项目文件夹：资料、草稿、成果和归档 |
| `skills/` | 五个可选 skill |
| `DOCS/` | 指南 |

示例 `aprender-python` 是虚构的，与你的项目分开。你的数据来自你的回答；不知道的内容可以留空。

Python 3.8 或更高版本可以借助标准库自动完成创建、验证和索引。没有 Python 时，AI 会使用其文件工具。

## 项目状态

第一个版本（v0.1.0）的候选版；尚不稳定。对话式配置及可继续的个人资料、项目创建器、相互连接的节点和索引、变更记录和验证均已可用。自动测试在 Windows、macOS 和 Ubuntu 上使用 Python 3.8 和 3.13 通过；这并不能证明工具包易于使用。

已用 Claude Code 检查配置和继续工作。仍待完成：OpenCode 的新会话独立恢复、ChatGPT 网页版、五名初学者的测试，以及 Obsidian 中最终的视觉检查。详情见[更新日志](CHANGELOG.md)（西班牙语）。

## 隐私

工具包将文件保存在本地，不安装同步功能。AI 会根据其服务和设置处理你分享的内容：只提供必要的上下文。

## 许可证

[MIT](LICENSE)，署名 davidkimai 和 Albert Mestre。这是 Context Engineering 的独立改编版本，与原项目无隶属关系。

## 社区与支持

如有问题、想法或使用经验，可以参加[社区讨论](https://github.com/Albertmestre1256/obsidian-genesis/discussions)。如果遇到故障，请通过[问题报告](https://github.com/Albertmestre1256/obsidian-genesis/issues)使用“No me funciona”模板，并提供使用虚构数据的简短示例。[如何贡献](CONTRIBUTING.md)（西班牙语）。

## 支持本项目

Obsidian Genesis 是免费的，并将一直免费。如果它对你有帮助，可以通过 [Patreon](https://www.patreon.com/obsidiangenesis) 支持本项目。捐助用于投入时间完善初学者指南、开展真人测试、维护翻译和提供支持。捐助完全自愿：不会解锁任何功能，整个工具包始终公开。

## 关于开发

Albert Mestre 在 **OpenCode、Claude 和 Codex（OpenAI）** 的重要协助下开发这一改编版本。这些 AI 工具帮助构建了代码的重要部分，并支持文档编写和测试，因此在此列为项目的贡献工具。各项提议都会经过审阅，结果在整合前都会经过验证；使用 AI 不能取代与真人的测试，也不能单凭这一点证明工具包易于使用。
