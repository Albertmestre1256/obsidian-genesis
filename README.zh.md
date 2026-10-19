> **主要致谢：[davidkimai](https://github.com/davidkimai)。** 本工具包基于其作品 [Context Engineering](https://github.com/davidkimai/Context-Engineering)。Obsidian Genesis 改编了这项工作，借助 AI 来创建和整理 Obsidian 仓库（vault）。
> [!info]- Índice de esta nota (líneas)
> - Líneas 1–1: Atribución
> - Líneas 2–16: Este índice
> - Líneas 18–19: Introducción
> - Líneas 20–27: Obsidian Genesis：由 AI 为你配置的仓库
> - Líneas 28–51: 项目状态 — 2026 年 10 月 19 日
> - Líneas 52–72: 三步开始
> - Líneas 73–78: 附件或已有仓库
> - Líneas 79–86: 继续
> - Líneas 87–101: 包含内容
> - Líneas 102–112: 可选帮助
> - Líneas 113–116: 隐私
> - Líneas 117–120: 许可证
> - Líneas 121–124: 社区与支持
> - Líneas 125–127: 关于开发

**语言：** [Español](README.md) · [English](README.en.md) · [Deutsch](README.de.md) · 中文

# Obsidian Genesis：由 AI 为你配置的仓库

下载工具包，把文件夹交给一个 AI，然后回答它的问题。助手会按照工具包的规则准备你的笔记和第一个项目。你不需要会编程，也不需要了解 Obsidian。

**仓库（vault）** 是一个用 [Obsidian](https://obsidian.md) 打开的笔记文件夹。工具包使用西班牙语，适用于学习、工作或任何个人项目。你可以用自己的语言和助手交流；工具包的笔记和指南目前仍为西班牙语。

入口笔记 [Leer primero](LEER_PRIMERO.md)（“请先阅读”）连接面板（Panel）和总索引。在新仓库中，工具包会启用 Obsidian 的**关系图谱**：从侧边栏图标打开它来浏览相互连接的笔记，或在某个项目的索引中使用局部关系图谱。

## 项目状态 — 2026 年 10 月 19 日

**代码已发布到 `Pruebas` 分支（`10b99b5`）；尚不是稳定版本。** 重点仍然是通过简单的问题来创建仓库，不要求使用者编程或维护索引。

| 已实现 | 作用 |
|---|---|
| 对话式配置 | 在创建第一个项目之前保存回答，并继续未完成的部分。 |
| 可选、可继续的个人资料 | 维护唯一一份可折叠的清单；保留被跳过的信息，只补充使用者选择的内容。 |
| 相互连接的节点和索引 | 每个集合都链接其上级、下级和笔记；总节点链接地图和 Leer primero。新项目拥有以自身名称命名的索引。 |
| 维护与收尾 | 标识助手，记录变更并保留历史，检查项目卡片、面板、个人资料、地图、行范围以及初始项目的一致性。 |
| 支持多种 AI | 提供 Claude Code、OpenCode、ChatGPT 及其他具备文件工具的助手的指南；也有手动方式可选。 |

项目创建器在保存项目前会再次检查状态，并区分事先阻止的情况与部分失败；每个文件都在不覆盖已有文件的前提下创建。

简洁视图减少新文件夹的文件列表和关系图谱中的杂项；现有仓库也可选择启用，并保留备份。原有设置和自定义搜索会保留；如果工具包的过滤条件尚未应用，会明确提示。

安装器的本地检查中，**40 项测试通过，1 项在 Python 3.13 下跳过**。[代码提交 `10b99b5` 的远程测试矩阵](https://github.com/Albertmestre1256/obsidian-genesis/actions/runs/39100123756)在 Windows、macOS 和 Ubuntu 上使用 Python 3.8 和 3.13，**6/6 项均成功**。这些是技术结果，不能证明工具包易于使用。

已用 Claude Code 检查配置和继续工作。OpenCode/Big Pickle 的手动试验展示了同一会话内的持续使用，未证明新会话中的独立恢复。一个新的 Codex 对话继续处理了较早的副本，并保留了被跳过的信息；过程中使用了外部上下文和工具。这些并非与真正初学者进行的测试，也不能验证所有当前变更的界面表现。

仍待完成：OpenCode 的新会话独立恢复、ChatGPT 网页版的专项验证、五名初学者的测试（至少四人无需帮助），以及 Obsidian 中最终正式的视觉检查。

社区讨论现已开放；赞助渠道仍待确定。README 与文档指南提供西班牙语、英语、德语和中文版本；工具包的通用操作说明仍使用西班牙语。全面调整和优化现有仓库将是后续阶段。[更新日志](CHANGELOG.md) · [如何贡献](CONTRIBUTING.md)（均为西班牙语）。

## 三步开始

1. **下载并解压**仓库：Code → Download ZIP。
2. **在一个能读写文件的 AI 中打开该文件夹。** 选择包含本 README 和 `AI-INSTRUCTIONS.md` 的那个文件夹。
3. **粘贴以下消息并回答它的问题：**

   > 我希望你用这个工具包配置我的 Obsidian 仓库。请先阅读 `INDICE.md`，然后阅读 `00_CORE/atoms/00_vault-rules.md` 和 `AI-INSTRUCTIONS.md`。我不了解 Obsidian：请用简单的问题引导我，每次一两个，并根据我的回答处理文件。在写入之前，请告诉我你会把所有内容保存在哪里、会创建什么。请保持主索引为最新。如果你没有权限做这些，请告诉我。

| 你使用的工具 | 如何打开工具包 |
|---|---|
| OpenCode | 打开文件夹，使用上面的消息或 `/configurar`。[指南](DOCS/opencode.md)。 |
| ChatGPT | 带文件工具的本地文件夹，或附加的副本。[指南](DOCS/chatgpt.md)。 |
| Claude Code | 打开文件夹，使用上面的消息或 `/configurar`。 |
| 其他 AI | 让它访问该文件夹，并使用同样的消息。 |

AI 会询问你想整理什么、要保留哪些笔记以及目标是什么。你可以回答“我还不知道”或“我没有截止日期”；第一个任务可以以后再选。

它还会维护一份**个性化清单**：你已回答的、待定的以及你选择跳过的内容。在新笔记中，它折叠在项目及其进展下方；需要查看时再展开。自我介绍、简历、教育背景、日常安排以及仓库的使用期限都是可选的。你可以先从基本内容开始，之后再说 **“个性化我的仓库还缺什么”** 或 **“我们来完善我的个人资料”**。[工作原理](00_CORE/protocols/personalizar-vault.md)。

**你将得到：** 一个准备好的文件夹、项目卡片、用于访问的面板，以及如何在 Obsidian 中打开它的说明。AI 会检查文件；视觉检查在 Obsidian 中进行。如果你还没有安装 Obsidian，请从 [obsidian.md](https://obsidian.md) 安装，将准备好的文件夹作为仓库打开，然后进入 `Panel.md`。

## 附件或已有仓库

附加的 ZIP 文件并不能让 AI 访问你的电脑。如果聊天能生成文件，它可以返回一份配置好的副本供你下载。如果它只能回复文字，保存工作就仍待完成。[访问指南](DOCS/QUICKSTART.md)说明了各种选择。

如果你已经有一个仓库，目前的整合方式是保守的：AI 会读取它的规则、比较冲突，并保留笔记和设置。自动重组或优化整个现有仓库尚未实现；这就是上面提到的后续阶段。

## 继续

说 **“继续 [项目]”**。AI 会先阅读索引，然后阅读规则和当前的项目卡片，并继续待办事项。你可以要求创建另一个项目、起草、审阅或保存收尾：[日常请求](DOCS/usar-con-otras-ias.md)。

如需整理更多内容，可以说 **“添加一个节点，用于我的课程摘要”**。每个节点都有一个包含链接和摘要的索引；总地图连接所有节点，AI 在添加笔记时会维护它们。已有的索引会被保留；重命名索引或重组笔记需要事先约定范围。[指南](DOCS/indice-principal.md)。

Claude Code 和 OpenCode 包含 `/configurar`、`/empezar`、`/nuevo-proyecto`、`/redactar`、`/validar` 和 `/cerrar`。在 Claude 中，创建另一个项目和收尾需要手动调用。权限取决于所用的助手。使用附件时，请始终分享最新的笔记：它们不会同步。

## 包含内容

各文件的用途与查阅时机，请参阅[文档与工具指南](DOCS/README.zh.md)。

| 位置 | 用途 |
|---|---|
| `INDICE.md` | 首先阅读：文件和项目的完整目录 |
| `LEER_PRIMERO.md` | 面向使用者的入口笔记，也是各总节点的核心连接 |
| `Panel.md` | 访问项目和任务 |
| `00_CORE/` | 规则、项目卡片、指南和工具 |
| `PROJECT_TEMPLATE/` | 用于资料、草稿、成果和历史的文件夹 |
| `DOCS/` | 可选帮助 |

示例 `aprender-python` 是虚构的，与你自己的项目分开。你的数据根据你的回答填写；没有信息的部分可以留空。

## 可选帮助

以下指南为西班牙语：

- [手动创建项目](DOCS/primer-proyecto.md)。
- [不使用 Python 整合工具包](DOCS/instalacion-manual.md)。
- [模板和面板](DOCS/obsidian.md)。
- [故障排除](DOCS/TROUBLESHOOTING.md)。

Python 3.8 或更高版本可以借助标准库自动完成安装、创建、验证和索引。AI 也可以使用其文件工具完成配置。参与贡献：[CONTRIBUTING](CONTRIBUTING.md)。

## 隐私

工具包将文件保存在本地，不安装同步功能。AI 会根据其服务和设置处理你分享的内容：只提供必要的上下文。

## 许可证

[MIT](LICENSE)，署名 davidkimai 和 Albert Mestre。这是 Context Engineering 的独立改编版本，与原项目无隶属关系。

## 社区与支持

如有问题、想法或使用经验，可以参加[社区讨论](https://github.com/Albertmestre1256/obsidian-genesis/discussions)。如果遇到故障，请通过[问题报告](https://github.com/Albertmestre1256/obsidian-genesis/issues)使用“No me funciona”模板，并提供使用虚构数据的简短示例。[如何贡献](CONTRIBUTING.md)（西班牙语）。

## 关于开发

Albert Mestre 在 **OpenCode、Claude 和 Codex（OpenAI）** 的重要协助下开发这一改编版本。这些 AI 工具帮助构建了代码的重要部分，并支持文档编写和测试，因此在此列为项目的贡献工具。各项提议都会经过审阅，结果在整合前都会经过验证；使用 AI 不能取代与真人的测试，也不能单凭这一点证明工具包易于使用。
