---
tipo: guia-documentos
descripcion: "各文档的内容、用途以及适合查阅的时机。"
---
> [!info]- Índice de esta nota (líneas)
> - Líneas 1–4: Propiedades
> - Líneas 5–17: Este índice
> - Líneas 19–26: 工具包文档与工具指南
> - Líneas 27–37: 本指南目录
> - Líneas 38–47: 入口
> - Líneas 48–65: 规则与项目
> - Líneas 66–85: 帮助
> - Líneas 86–99: 集成与设置
> - Líneas 100–113: Python 与测试
> - Líneas 114–124: 仓库与署名
> - Líneas 125–133: 可选资源
> - Líneas 134–146: 使用过程中创建的文件

# 工具包文档与工具指南

**主 README 及其语言版本:** [Español](../README.md) · [English](../README.en.md) · [Deutsch](../README.de.md) · [中文](../README.zh.md)

**本指南的其他语言版本:** [Español](README.md) · [English](README.en.md) · [Deutsch](README.de.md) · [中文](README.zh.md)

开始前不需要读完所有文档：按照主 README 操作，回答 AI 的问题即可。本指南帮助你了解文件或查找帮助。各语言版本使用相同的文件路径；工具包的通用指令仍为西班牙语。 本指南介绍完整仓库，应在下载的工具包文件夹中查阅。将工具包整合到另一个笔记库时，本指南与测试及开发文档留在原文件夹中；日常使用帮助仍会复制。

## 本指南目录

- [入口](#入口)
- [规则与项目](#规则与项目)
- [帮助](#帮助)
- [集成与设置](#集成与设置)
- [Python 与测试](#python-与测试)
- [仓库与署名](#仓库与署名)
- [可选资源](#可选资源)
- [使用过程中创建的文件](#使用过程中创建的文件)

## 入口

| 文档或工具 | 用途 |
|---|---|
| [`README.md`](../README.md) · [`README.en.md`](../README.en.md) · [`README.de.md`](../README.de.md) · [`README.zh.md`](../README.zh.md) | 开始步骤、项目状态和供 AI 配置使用的提示。 |
| [`LEER_PRIMERO.md`](../LEER_PRIMERO.md) | 连接面板、总索引与规则的入口笔记。 |
| [`Panel.md`](../Panel.md) | 日常访问项目和任务的面板。 |
| [`INDICE.md`](../INDICE.md) | 整个笔记库的实际目录；AI 首先读取它。 |
| [`AI-INSTRUCTIONS.md`](../AI-INSTRUCTIONS.md) · [`AGENTS.md`](../AGENTS.md) · [`CLAUDE.md`](../CLAUDE.md) | 助手入口说明如何选择流程；AGENTS 和 CLAUDE 都指向该说明。 |

## 规则与项目

| 文档或工具 | 用途 |
|---|---|
| [`00_CORE/atoms/00_vault-rules.md`](../00_CORE/atoms/00_vault-rules.md) | 关于上下文、保留原文、链接与署名的通用规则。 |
| [`00_CORE/protocols/configurar-vault.md`](../00_CORE/protocols/configurar-vault.md) | 通过问答创建笔记库，允许信息暂不完整。 |
| [`00_CORE/protocols/personalizar-vault.md`](../00_CORE/protocols/personalizar-vault.md) | 记录回答、跳过的信息和以后可补充的内容。 |
| [`00_CORE/protocols/context-injection.md`](../00_CORE/protocols/context-injection.md) | 按请求选择上下文，无需读取整个笔记库。 |
| [`00_CORE/protocols/ai-write-protocol.md`](../00_CORE/protocols/ai-write-protocol.md) | 使用足够的上下文准备、撰写和检查文本。 |
| [`00_CORE/molecules/marco-comunicacion-general.md`](../00_CORE/molecules/marco-comunicacion-general.md) | 确定沟通目的、受众和表达方式。 |
| [`00_CORE/cognitive-tools/redaccion-tecnica.md`](../00_CORE/cognitive-tools/redaccion-tecnica.md) · [`00_CORE/cognitive-tools/redaccion-narrativa.md`](../00_CORE/cognitive-tools/redaccion-narrativa.md) · [`00_CORE/cognitive-tools/redaccion-operativa.md`](../00_CORE/cognitive-tools/redaccion-operativa.md) · [`00_CORE/cognitive-tools/redaccion-persuasiva.md`](../00_CORE/cognitive-tools/redaccion-persuasiva.md) | 按任务选用技术、叙事、操作性或说服性写作指南。 |
| [`00_CORE/cells/ejemplo-context.md`](../00_CORE/cells/ejemplo-context.md) | 展示上下文笔记的虚构示例，不代表你的数据。 |
| [`00_CORE/templates/TEMPLATE_cell.md`](../00_CORE/templates/TEMPLATE_cell.md) | 项目上下文笔记模板。 |
| [`00_CORE/templates/TEMPLATE_configuracion.md`](../00_CORE/templates/TEMPLATE_configuracion.md) | 配置与可选、可继续补充的信息清单模板。 |
| [`00_CORE/templates/TEMPLATE_nodo.md`](../00_CORE/templates/TEMPLATE_nodo.md) | 笔记集合的索引模板。 |
| [`PROJECT_TEMPLATE/00 - Índice y Contexto.md`](../PROJECT_TEMPLATE/00%20-%20%C3%8Dndice%20y%20Contexto.md) | 每个新项目的关联索引基础模板。 |
| [`PROJECT_TEMPLATE/01_FUENTES/README.md`](../PROJECT_TEMPLATE/01_FUENTES/README.md) · [`PROJECT_TEMPLATE/02_SINTESIS/README.md`](../PROJECT_TEMPLATE/02_SINTESIS/README.md) · [`PROJECT_TEMPLATE/03_ENTREGABLES/README.md`](../PROJECT_TEMPLATE/03_ENTREGABLES/README.md) · [`PROJECT_TEMPLATE/_archivo/README.md`](../PROJECT_TEMPLATE/_archivo/README.md) | 说明原始资料、工作内容、成果与历史材料的存放位置。 |

## 帮助

| 文档或工具 | 用途 |
|---|---|
| [`DOCS/QUICKSTART.md`](../DOCS/QUICKSTART.md) | 快速跳转到主要开始步骤与访问指南。 |
| [`DOCS/empezar-con-ia.md`](../DOCS/empezar-con-ia.md) | 如何提供真实的文件夹访问权限，或使用附件副本。 |
| [`DOCS/opencode.md`](../DOCS/opencode.md) | 在 OpenCode 中打开工具包并使用命令。 |
| [`DOCS/chatgpt.md`](../DOCS/chatgpt.md) | ChatGPT 使用文件夹或附件的操作流程。 |
| [`DOCS/usar-con-otras-ias.md`](../DOCS/usar-con-otras-ias.md) | 用于继续项目、写作或保存进展的日常请求示例。 |
| [`DOCS/primer-proyecto.md`](../DOCS/primer-proyecto.md) | 手动创建项目的备选方法。 |
| [`DOCS/instalacion-manual.md`](../DOCS/instalacion-manual.md) | 不运行 Python 时如何整合工具包。 |
| [`DOCS/creacion-para-asistentes.md`](../DOCS/creacion-para-asistentes.md) | 供 AI 准备项目文件时使用的技术参考。 |
| [`DOCS/indice-principal.md`](../DOCS/indice-principal.md) | 维护总索引、局部索引和可扩展的链接关系。 |
| [`DOCS/mantenimiento.md`](../DOCS/mantenimiento.md) | 更新行号索引、地图与记录，并检查收尾状态。 |
| [`DOCS/obsidian.md`](../DOCS/obsidian.md) | Obsidian 中的模板、面板、Bases 与关系图谱。 |
| [`DOCS/TROUBLESHOOTING.md`](../DOCS/TROUBLESHOOTING.md) | 常见错误，以及如何诊断受阻的步骤。 |
| [`DOCS/mcp-claude.md`](../DOCS/mcp-claude.md) | 排查 Claude 中的 MCP 连接与结构定义问题。 |
| [`DOCS/prueba-con-usuarios.md`](../DOCS/prueba-con-usuarios.md) | 面向真实初学者的测试流程与判定标准。 |
| [`DOCS/publicacion.md`](../DOCS/publicacion.md) | 发布版本前需要完成的检查。 |

## 集成与设置

| 文档或工具 | 用途 |
|---|---|
| [`.claude/skills/configurar/SKILL.md`](../.claude/skills/configurar/SKILL.md) · [`.opencode/commands/configurar.md`](../.opencode/commands/configurar.md) | /configurar：开始问答或继续未完成的配置。 |
| [`.claude/skills/empezar/SKILL.md`](../.claude/skills/empezar/SKILL.md) · [`.opencode/commands/empezar.md`](../.opencode/commands/empezar.md) | /empezar：加载项目上下文并继续。 |
| [`.claude/skills/nuevo-proyecto/SKILL.md`](../.claude/skills/nuevo-proyecto/SKILL.md) · [`.opencode/commands/nuevo-proyecto.md`](../.opencode/commands/nuevo-proyecto.md) | /nuevo-proyecto：商定并添加另一个项目。 |
| [`.claude/skills/redactar/SKILL.md`](../.claude/skills/redactar/SKILL.md) · [`.opencode/commands/redactar.md`](../.opencode/commands/redactar.md) | /redactar：根据现有上下文与事实撰写内容。 |
| [`.claude/skills/validar/SKILL.md`](../.claude/skills/validar/SKILL.md) · [`.opencode/commands/validar.md`](../.opencode/commands/validar.md) | /validar：检查上下文笔记并解释错误或提醒。 |
| [`.claude/skills/cerrar/SKILL.md`](../.claude/skills/cerrar/SKILL.md) · [`.opencode/commands/cerrar.md`](../.opencode/commands/cerrar.md) | /cerrar：建议保存变更并检查已同意的更新。 |
| [`.claude/skills/vault-manager/SKILL.md`](../.claude/skills/vault-manager/SKILL.md) · [`.claude/settings.json`](../.claude/settings.json) | 笔记库使用引导与 Claude 集成设置。 |
| [`.obsidian/app.json`](../.obsidian/app.json) · [`.obsidian/core-plugins.json`](../.obsidian/core-plugins.json) · [`.obsidian/graph.json`](../.obsidian/graph.json) · [`.obsidian/templates.json`](../.obsidian/templates.json) | 新笔记库的初始设置；整合时保留已有设置。 |
| [`Proyectos.base`](../Proyectos.base) | 面板使用的项目表；它不是笔记或脚本。 |

## Python 与测试

Python 用于自动执行任务。只要 AI 能管理文件，使用工具包就不需要编程。测试文件供工具包开发者使用；安装程序不会把它们复制到安装后的笔记库。

| 文档或工具 | 用途 |
|---|---|
| [`instalar.py`](../instalar.py) | 将工具包添加到另一个笔记库，不替换已有文件。 |
| [`crear_proyecto.py`](../crear_proyecto.py) | 为已商定的项目创建上下文笔记与文件夹。 |
| [`actualizar_indice.py`](../actualizar_indice.py) | 生成或检查总索引与节点索引。 |
| [`00_CORE/schemas/validate.py`](../00_CORE/schemas/validate.py) | 检查上下文笔记与配置；使用 --cierre 核查一次操作。 |
| [`00_CORE/schemas/note_index.py`](../00_CORE/schemas/note_index.py) | 计算并检查可编辑笔记的行号范围。 |
| [`00_CORE/schemas/registrar_cambios.py`](../00_CORE/schemas/registrar_cambios.py) | 记录修改者、变更文件并保留历史。 |
| [`tests/conftest.py`](../tests/conftest.py) · [`tests/test_crear_proyecto.py`](../tests/test_crear_proyecto.py) · [`tests/test_indice.py`](../tests/test_indice.py) · [`tests/test_instalar.py`](../tests/test_instalar.py) · [`tests/test_kit.py`](../tests/test_kit.py) · [`tests/test_mantenimiento.py`](../tests/test_mantenimiento.py) · [`tests/test_nodos.py`](../tests/test_nodos.py) · [`tests/test_validate.py`](../tests/test_validate.py) | 共享测试准备，以及创建、索引、安装、打包、维护、节点和验证测试。 |

## 仓库与署名

| 文档或工具 | 用途 |
|---|---|
| [`LICENSE`](../LICENSE) | MIT 许可证及 davidkimai 与 Albert Mestre 的署名。 |
| [`CHANGELOG.md`](../CHANGELOG.md) | 按版本或日期记录工具包变更。 |
| [`CONTRIBUTING.md`](../CONTRIBUTING.md) | 如何参与贡献、寻求帮助和检查修改。 |
| [`.github/ISSUE_TEMPLATE/no-me-funciona.md`](../.github/ISSUE_TEMPLATE/no-me-funciona.md) | 使用虚构示例报告故障的简短模板。 |
| [`.github/workflows/tests.yml`](../.github/workflows/tests.yml) | GitHub Actions 远程测试定义。 |
| [`.gitignore`](../.gitignore) | Git 应忽略的本地文件。 |

## 可选资源

| 文档或工具 | 用途 |
|---|---|
| [`00_CORE/davidkimai-resources/README.md`](../00_CORE/davidkimai-resources/README.md) | 源自原始项目的改编资源入口，可选阅读。 |
| [`00_CORE/davidkimai-resources/protocols/01_extract_information.md`](../00_CORE/davidkimai-resources/protocols/01_extract_information.md) | 从来源中提取信息，不编造缺失内容。 |
| [`00_CORE/davidkimai-resources/evaluation/token_budgeting.md`](../00_CORE/davidkimai-resources/evaluation/token_budgeting.md) | 选择足够的上下文，避免加载无关材料。 |
| [`00_CORE/davidkimai-resources/field-theory/field_dynamics.md`](../00_CORE/davidkimai-resources/field-theory/field_dynamics.md) | 用于关联与维护上下文的可选概念模型。 |

## 使用过程中创建的文件

这些文件并未在工具包中预先填入个人信息，而是由 AI 根据你的回答创建。下面的项目名称仅用于说明路径，不需要手动创建这些文件。

| 文档或工具 | 用途 |
|---|---|
| `00_CORE/configuracion.md` | 保存回答、跳过的信息与配置状态，便于继续时不再重复提问。 |
| `00_CORE/cells/ID-context.md` | 每个项目的上下文笔记：目标、事实、决定与下一步行动。 |
| `ID/00 - Índice - ID.md` | 项目自己的索引，连接笔记与子节点；独立节点也有自己的索引。 |
| `ID/01_FUENTES/ · ID/02_SINTESIS/ · ID/03_ENTREGABLES/ · ID/_archivo/` | 按照约定范围保存原始资料、进行中的工作、成果和历史材料。 |
| `00_CORE/logs/registro-cambios.md · 00_CORE/logs/historial/` | 注明修改者的变更记录；五天后更新记录时，旧记录会完整归档。 |

总索引维护实际文件清单。本指南解释文件用途，不替代规则，也不要求每次对话都加载所有文档。
