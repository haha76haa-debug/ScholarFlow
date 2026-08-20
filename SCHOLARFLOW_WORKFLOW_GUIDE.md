# 《ScholarFlow: 基于 Zotero + Obsidian + LLM 的自迭代学术知识库实操指南》
> 💡 **参考体系**：本知识库基于 **Andrej Karpathy “LLM Wiki” 架构** 与抖音博主 **ScholarFlow【Obsidian联动Codex打造“自迭代”生长知识库】** 的核心理念精心构建，实现了“文献摄取 -> 证据抽取 -> 知识网络自生长 -> 成果输出与自动化维护”的全闭环。

---

## 目录
1. [系统核心理念与架构总览](#1-系统核心理念与架构总览)
2. [为什么是“自迭代生长”知识库？](#2-为什么是自迭代生长知识库)
3. [Zotero 保姆级配置与 PDF 批注流](#3-zotero-保姆级配置与-pdf-批注流)
4. [Obsidian 知识库目录结构与规范](#4-obsidian-知识库目录结构与规范)
5. [Codex / AI Agent 联动自迭代实操](#5-codex--ai-agent-联动自迭代实操)
6. [Python 自动化工具集 (`kb_tools`) 速查](#6-python-自动化工具集-kb_tools-速查)
7. [内置文献与图谱演示（开箱即用）](#7-内置文献与图谱演示开箱即用)

---

## 1. 系统核心理念与架构总览

在传统文献管理中，用户往往只是把文献“存”在 Zotero 或 Obsidian 中，笔记变成了一座座孤岛，难以随着阅读量的增加而产生复利。

**本系统的核心思想**：
- **Obsidian 是“代码库 (Codebase)”**：每一篇笔记都是模块化、结构化的知识文件。
- **Codex / LLM 是“程序员 (Programmer)”**：AI 负责阅读你的批注、提炼原子概念、梳理方法演进、修补断链并自动更新索引。
- **Zotero 是“不可变数据源 (Single Source of Truth)”**：文献元数据与 PDF 划线批注在 Zotero 中沉淀，通过结构化模板同步到 Obsidian。

```
┌────────────────────────────────────────────────────────┐
│                   Zotero (事实源头)                     │
│  - Better BibTeX 自动生成标准 Citekey (如 he2016deep)     │
│  - 6色语义 PDF 批注（问题/方法/贡献/局限/数据/讨论）        │
└───────────────────────────┬────────────────────────────┘
                            │ (Zotero Integration / BibTeX Ingest)
                            ▼
┌────────────────────────────────────────────────────────┐
│             Obsidian 结构化知识库 (Vault)                │
│                                                        │
│  ┌──────────────────┐    ┌──────────────────────────┐  │
│  │ Sources/Papers/  │───▶│ Knowledge/Concepts/      │  │
│  │ (单篇文献笔记)    │    │ (提炼出的原子概念/机制)    │  │
│  └─────────┬────────┘    └────────────┬─────────────┘  │
│            │                          │                │
│            ▼                          ▼                │
│  ┌──────────────────────────────────────────────────┐  │
│  │ Knowledge/ (综述演进、方法分类法、开放研究空白)   │  │
│  └──────────────────────────────────────────────────┘  │
│            │                                           │
│            ▼                                           │
│  ┌──────────────────────────┐    ┌──────────────────┐  │
│  │ Writing/ (对比矩阵与草稿) │    │ Maps/ (Canvas图谱)│ │
│  └──────────────────────────┘    └──────────────────┘  │
└───────────────────────────┬────────────────────────────┘
                            ▲
                            │ 自动维护、断链检查、图谱生成
┌───────────────────────────┴────────────────────────────┐
│   Codex / AI 准则 (CLAUDE.md / AGENT.md) + Python CLI   │
└────────────────────────────────────────────────────────┘
```

---

## 2. 为什么是“自迭代生长”知识库？

传统的知识库随着笔记增多，整理成本指数上升；而“自迭代生长”具备以下三大机制：

1. **证据与知识分离（Evidence vs Synthesis）**：
   - 绝不在单篇文献笔记里堆砌长篇大论。单篇论文笔记只提取结构化 **Evidence Record（证据卡片）**。
   - 跨论文的归纳总结全部自动升华到 `Knowledge/` 目录中。
2. **观点晋级门禁（Claim Promotion Gate）**：
   - AI 在提炼知识时，必须带上对应的证据编号（如 `EVD-he2016deep-01`），禁止“无源幻觉”。
   - 强结论（Strong Claim）必须源自完整论文或顶级会议，网页草稿仅作为推测性观点（Speculative）。
3. **自动化自愈与索引更新（Automated Maintenance）**：
   - 每次摄取新论文后，运行自动化工具或由 AI 执行自检，自动更新全局注册表、索引导航以及双链 Canvas 画布。

---

## 3. Zotero 保姆级配置与 PDF 批注流

### 3.1 安装 Better BibTeX 插件
1. 在 Zotero 中安装 **Better BibTeX (BBT)** 插件。
2. 打开 Zotero **首选项** -> **Better BibTeX** -> **Citation keys**。
3. 设置 **Citation key formula** 为：
   ```text
   [auth:lower][year][veryshorttitle:lower]
   ```
   *例如：Kaiming He (2016) 的 ResNet 论文将自动生成唯一 Citekey：`he2016deep`。*

### 3.2 6 色语义 PDF 划线标注规范
在 Zotero 内置 PDF 阅读器中划线时，请使用以下 6 种标准颜色，系统导入时会自动分类并赋予语义：

| 标注颜色 | 含义与语义分类 | 提取目标位置 | 说明 |
|---|---|---|---|
| 🟡 **黄色 (Yellow)** | **研究背景与问题 (Context)** | `## Research question` | 论文试图解决什么痛点、核心动机 |
| 🟢 **绿色 (Green)** | **方法架构与实现 (Method)** | `## Method` | 核心公式、网络结构、算法步骤 |
| 🟣 **紫色 (Purple)** | **核心创新与结论 (Claim)** | `## Claim` / `## Evidence` | 论文的主要创新点、理论突破 |
| 🔴 **红色 (Red)** | **局限性与不足 (Limitation)** | `## Limitation` / `## Research Gaps` | 实验边界、算力瓶颈、失败案例 |
| 🔵 **蓝色 (Blue)** | **实验数据与基准 (Benchmark)**| `## Evidence` | 准确率、指标提升、数据集对比 |
| ⚪ **灰色 (Gray)** | **延伸讨论与引用 (Discussion)**| `## Key Annotations` | 启发性思考、重要参考文献 |

### 3.3 Obsidian Zotero Integration 插件配置
1. 在 Obsidian **社区插件** 中搜索并安装 **Zotero Integration**。
2. 打开插件设置 -> **Add Import Format**：
   - **Name**: `Academic Paper Note`
   - **Output path**: `Sources/Papers/{{citekey}}.md`
   - **Template**: 直接使用本知识库内置模板 `Templates/zotero_integration_nunjucks.md`（或 `_system/zotero_template.njk`）。
3. 在 Obsidian 中按下 `Ctrl+P`（Mac 为 `Cmd+P`），输入并运行 `Zotero Integration: Create Literature Note`，选中 Zotero 中的论文，即可一键生成完全合规的标准论文笔记！

---

## 4. Obsidian 知识库目录结构与规范

知识库根目录下仅保留 3 个核心导航入口，所有内容严格模块化：

| 目录 / 文件 | 作用与定位 |
|---|---|
| **`00-Hub.md`** | **项目总览中枢**：定义研究使命、当前核心议题、快速导航入口。 |
| **`01-Plan.md`** | **研究规划面板**：当前研究状态、进行中的假设、待读文献队列。 |
| **`02-Index.md`** | **主索引导航 (MOC)**：人工与自动同步的全局目录索引。 |
| **`Sources/Papers/`** | **文献笔记库**：每篇论文一个独立 Markdown 文件，包含 Frontmatter 与 Evidence Record。 |
| **`Knowledge/Concepts/`**| **原子概念库**：由 AI 从多篇论文中提炼的通用概念（如 `residual_connection`、`self_attention`、`peft`）。 |
| **`Knowledge/`** | **领域综合成果**：包含 `Literature Overview.md`（综述）、`Method Taxonomy.md`（分类法）、`Research Gaps.md`（研究空白）。 |
| **`Writing/`** | **学术写作与产出**：包含 `comparison-matrix.md`（全景对比矩阵）、`Drafts/`（论文初稿）、`Outlines/`（大纲）。 |
| **`Daily/`** | **每日阅读日志**：按日期记录每天阅读的文献与提炼出的 Promotable 候选概念。 |
| **`Maps/literature.canvas`**| **可视化图谱**：符合 Obsidian 原生规范的 JSON Canvas 关系画布。 |
| **`_system/`** | **系统架构与配置**：包含 YAML 校验契约（Schemas）、全局注册表（`registry.md`）、Lint 检查报告。 |

---

## 5. Codex / AI Agent 联动自迭代实操

当你在 Obsidian 中配合 **Codex CLI**、**Claude Code** 或第三方 AI 插件（如 Codex Panel、Agent Client、Smart Connections）时，可以直接基于预置的 `CLAUDE.md` 和 `AGENT.md` 执行自迭代。

### 常用自迭代 Prompt 模版：

#### 场景 1：新读完一篇论文，请求 AI 摄取与提炼
```text
我刚在 Sources/Papers/ 下新增了论文笔记（例如 vaswani2017attention.md）。
请按照 CLAUDE.md 的 Phase 1 & 2 准则：
1. 检查并补全 Evidence Record。
2. 提取出其中的关键概念，在 Knowledge/Concepts/ 中创建或更新原子概念笔记。
3. 将论文的主要贡献和局限性同步到 Knowledge/ 下的 Literature Overview 和 Research Gaps。
4. 运行 kb_tools 自动化工具同步索引和 Canvas 图谱。
```

#### 场景 2：定期自动重构与知识库巡检（ScholarFlow工作流核心）
```text
请对当前知识库执行每日/每周自迭代巡检：
1. 运行 python -m kb_tools lint --strict 检查所有笔记格式与证据锚点。
2. 检查是否有未建立双链的孤岛笔记（Orphan Notes），并为它们与已有概念建立关联。
3. 重新聚合 Knowledge/Method Taxonomy.md 中的分类法树状结构。
4. 更新 Maps/literature.canvas 可视化网络。
```

#### 场景 3：辅助论文写作（从知识库提取对比矩阵与 Related Work）
```text
我想撰写关于“大模型轻量化微调技术”的文献综述章节。
请基于 Sources/Papers/ 和 Knowledge/ 中的 Evidence Records：
1. 更新 Writing/comparison-matrix.md 对比表格。
2. 在 Writing/Drafts/ 下生成一段 800 字的结构化 Related Work 初稿，并明确标注每句话引用的文献与 Evidence ID。
```

---

## 6. Python 自动化工具集 (`kb_tools`) 速查

知识库内置了高度健壮的 Python 自动化工具集，位于 `src/kb_tools/`，无需复杂外部依赖。

### 6.1 一键运行完整自迭代流水线
在 Windows 终端（PowerShell 或 CMD）中运行：
```powershell
# 运行一键维护脚本（自动完成 Lint、同步索引、修复链接、提炼知识、生成Canvas）
python Scripts/run_pipeline.py
```
*(或者直接双击运行 `Scripts/run_pipeline.bat`)*

### 6.2 独立 CLI 命令速查

| 操作需求 | 执行命令 | 说明 |
|---|---|---|
| **格式与规范检查** | `python -m kb_tools lint --strict` | 校验 YAML Frontmatter、必填 H2 标题与证据卡片 |
| **注册表与索引同步** | `python -m kb_tools sync-registry` | 自动扫描全库并更新 `_system/registry.md` 与 `02-Index.md` |
| **断链与孤岛检测** | `python -m kb_tools check-links` | 扫描死链并提示孤立笔记 |
| **智能修复断链** | `python -m kb_tools repair-links` | 模糊匹配自动修复因重命名导致的失效双链 |
| **跨文献知识提炼** | `python -m kb_tools synthesize` | 汇总所有 Evidence 生成综述、分类法与研究空白 |
| **生成 Canvas 可视化画布** | `python -m kb_tools generate-canvas` | 生成可交互的 `Maps/literature.canvas` |
| **直接导入 BibTeX 文件** | `python -m kb_tools ingest --format bibtex --input papers.bib` | 从 BibTeX 文件批量生成标准论文笔记 |

### 6.3 运行内置自动化测试套件
```powershell
python -m pytest tests/
```
*（当前内置 192 项单元测试与端到端对抗测试，保证知识库运行绝对稳定！）*

---

## 7. 内置文献与图谱演示（开箱即用）

为了让您能够立即上手体验，知识库已经预置了 3 篇经典的 AI/深度学习里程碑论文作为完整示范：

1. **`Sources/Papers/he2016deep.md`**：ResNet 深度残差学习（CVPR 2016）
2. **`Sources/Papers/vaswani2017attention.md`**：Transformer 自注意力机制（NeurIPS 2017）
3. **`Sources/Papers/hu2021lora.md`**：LoRA 低秩适应微调（ICLR 2022）

同时已自动生成：
- 4 个原子概念：`residual_connection.md`、`self_attention.md`、`transformer_architecture.md`、`peft.md`
- 3 份领域综合成果：`Literature Overview.md`、`Method Taxonomy.md`、`Research Gaps.md`
- 1 份全景对比矩阵：`Writing/comparison-matrix.md`
- 1 份完整交互画布：`Maps/literature.canvas`（可以直接在 Obsidian 中打开并拖拽缩放查看文献关系网！）

---

🎉 **祝您在 Zotero + Obsidian + Codex 的学术自迭代探索中收获满满的知识复利！**
