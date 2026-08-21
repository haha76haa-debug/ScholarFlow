# 🌊 ScholarFlow (思流)

<p align="center">
  <strong>基于 Zotero 7 + Obsidian + AI Agent（Codex / Claude）的自迭代学术知识库与科研智能引擎</strong><br>
  <em>借鉴 Andrej Karpathy “LLM Wiki” 范式 | 打造文献摄取、原子概念提炼、全景综述生成与图谱可视化的学术生产力闭环</em>
</p>

<p align="center">
  <a href="README_CN.md"><strong>🇨🇳 简体中文</strong></a> •
  <a href="README.md"><strong>🇺🇸 English</strong></a> •
  <a href="SCHOLARFLOW_WORKFLOW_GUIDE.md"><strong>📖 深度实操全景指南</strong></a> •
  <a href="https://github.com/haha76haa-debug/ScholarFlow/issues"><strong>🐛 报告问题</strong></a> •
  <a href="https://github.com/haha76haa-debug/ScholarFlow/discussions"><strong>💬 社区讨论</strong></a>
</p>

<p align="center">
  <a href="https://github.com/haha76haa-debug/ScholarFlow/actions/workflows/ci.yml"><img src="https://github.com/haha76haa-debug/ScholarFlow/actions/workflows/ci.yml/badge.svg" alt="CI Status"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Tests-192%2F192%20Passing-brightgreen.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Obsidian-JSON%20Canvas%20v1.0-purple.svg" alt="Obsidian">
  <img src="https://img.shields.io/badge/Zotero-Better%20BibTeX%20%2B%20CSL-red.svg" alt="Zotero">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-%E6%AC%A2%E8%BF%8E%E8%B4%A1%E7%8C%AE-brightgreen.svg" alt="PRs Welcome"></a>
</p>

---

## 🎯 为什么需要 ScholarFlow？

传统文献管理中，科研人员常面临三大痛点：
1. **只存不读，读完就忘**：Zotero 划了一堆高亮，两周后无法快速调取核心论点；
2. **文献孤岛，缺乏复利**：单篇笔记彼此割裂，撰写开题报告、综述或相关工作时无法串联；
3. **AI 总结浮于表面**：市面上的 AI 摘要工具仅输出粗糙大纲，无法提炼严谨的物理机制、参数提取方法与真实证据链。

**ScholarFlow（思流）** 的核心思想是将文献库视作一个**能够自生长的动态知识软件工程**：
- **Obsidian 是“代码库 (Codebase)”**：每一篇文献笔记都是模块化、结构化的知识文件。
- **AI Agent (Codex/Claude) 是“程序员 (Programmer)”**：自动阅读批注、提炼原子概念、梳理方法演进、修补断链并自动生成对比矩阵。
- **Zotero 7 是“不可变事实源头 (Single Source of Truth)”**：元数据与 6 色语义 PDF 划线批注自动提取为标准证据记录 (`EVD-citekey-NN`)。

```
                               ┌────────────────────────────────────────┐
                               │         Zotero 7 (不可变事实源)         │
                               │  - Better BibTeX 自动生成标准 Citekey   │
                               │  - 6 色语义 PDF 批注（问题/方法/贡献等） │
                               └──────────────────┬─────────────────────┘
                                                  │ (Zotero Integration / CSL-JSON / BibTeX)
                                                  ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Obsidian 学术结构化知识库 (Vault)                                                                     │
│                                                                                                       │
│  ┌────────────────────────┐     ┌────────────────────────┐     ┌───────────────────────────────────┐  │
│  │ Sources/Papers/        │────▶│ Knowledge/Concepts/    │────▶│ Writing/                          │  │
│  │ (单篇文献精读与证据链)   │     │ (原子理论概念与机制)   │     │ (全景横向对比矩阵与论文草稿)        │  │
│  └───────────┬────────────┘     └───────────┬────────────┘     └───────────────────────────────────┘  │
│              │                              │                                                         │
│              ▼                              ▼                                                         │
│  ┌───────────────────────────────────────────────────────┐     ┌───────────────────────────────────┐  │
│  │ Knowledge/ (全景文献综述、方法分类法体系、前沿研究空白)   │     │ Maps/literature.canvas            │  │
│  └───────────────────────────────────────────────────────┘     │ (3 泳道 Obsidian JSON Canvas 画布)│  │
│                                                                └───────────────────────────────────┘  │
└─────────────────────────────────────────────────┬─────────────────────────────────────────────────────┘
                                                  ▲
                                                  │ (格式校验、注册表同步、双链自愈、多篇文献全景合成)
┌─────────────────────────────────────────────────┴─────────────────────────────────────────────────────┐
│ Python 自动化工具箱 (`kb_tools`) & AI Agent 自迭代协议准则 (`CLAUDE.md` / `AGENT.md`)                 │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## ✨ 核心特色功能

### 1. 🧠 Karpathy “LLM Wiki” 学术全闭环
实现从 `文献摄取 ──► 概念拆解 ──► 全景综合 ──► 矩阵对比` 的自生长链路，随着阅读量增加，知识库自动自愈与演化。

### 2. 🛡️ 严谨的观点晋级门槛 (Claim Promotion Gate)
未经严格同行评审验证的占位符笔记无法晋级为确凿理论，所有核心结论必须绑定 `EVD-citekey-NN` 证据编号，彻底杜绝大模型学术幻觉。

### 3. 📊 全局唯一总索引 ([`02-Index.md`](02-Index.md))
告别文件夹内到处都是 index 的混乱设计。唯一总索引直接聚合 **实时 KPI 看板**、**文献全景卡片**、**概念总表**与**综合成果直达链接**。

### 4. 🗺️ 3 泳道极简 Canvas 拓扑图 ([`Maps/literature.canvas`](Maps/literature.canvas))
精心重构的 8 条水平直连箭头呈现 `文献 ──► 理论 ──► 产出` 流水线，卡片尺寸扩增至 `460×340px`，免缩放直接阅读双语摘要与公式，告别杂乱蜘蛛网。

### 5. 🌐 100% 中英双语对照与原生 LaTeX 公式支持
严格保证 `[EN]` / `[CN]` 平行对照，完整保留并精准渲染微观物理与半导体复杂公式（如特征长度 $\lambda = \sqrt{rac{arepsilon_b}{arepsilon_{ox}} t_b t_{ox}}$、饱和电流密度 $I_{on}/W$、接触电阻 $R_c$ 等）。

### 6. 🧪 192 项全量自动化测试保障
覆盖 YAML 边界异常、并发读写、断链模糊自愈、拓扑环路与证据门禁，测试通过率 100%。

---

## 🚀 3 分钟快速上手

### 步骤 1：克隆仓库与安装环境

```bash
# 克隆仓库
git clone https://github.com/haha76haa-debug/ScholarFlow.git
cd ScholarFlow

# 创建并激活 Python 虚拟环境
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 安装 kb-tools 核心工具箱
pip install -e .
pip install pytest pyyaml
```

### 步骤 2：一键运行自迭代维护管线

```bash
python Scripts/run_pipeline.py
```

### 步骤 3：在 Obsidian 中打开并体验

1. 打开 **Obsidian** $	o$ 点击左下角 **“打开文件夹作为库”**。
2. 选择本项目的 `ScholarFlow` 文件夹。
3. 按下 `Ctrl + G` 打开**色彩分类关系图谱**（蓝=文献、绿=概念、黄=综述、紫=写作）。
4. 双击打开 `Maps/literature.canvas` 即可体验清晰的 3 泳道知识流水线画布。

---

## 🛠️ Python 自动化工具箱 (`kb-tools`) 命令指南

| 指令 | 完整命令 | 功能说明 |
| :--- | :--- | :--- |
| **`lint`** | `kb-tools lint` | 校验全库笔记的 YAML Frontmatter 与元数据契约 |
| **`sync-registry`** | `kb-tools sync-registry` | 自动更新全局唯一总索引 (`02-Index.md`) 与元数据注册表 |
| **`repair-links`** | `kb-tools repair-links` | 全局扫描并自动修补断链与孤岛文档 |
| **`synthesize`** | `kb-tools synthesize` | 跨文献动态合成领域全景综述、方法分类法与前沿空白 |
| **`generate-canvas`** | `kb-tools generate-canvas` | 自动生成非重叠的 3 泳道 `Maps/literature.canvas` 图谱 |
| **`run-pipeline`** | `kb-tools run-pipeline` | 一键执行端到端全量自迭代与验证维护 |

---

## 📂 知识库标准目录结构

```text
ScholarFlow/
├── 00-Hub.md                     # 项目全局总览中枢
├── 01-Plan.md                    # 当前研究规划与待读文献队列
├── 02-Index.md                   # 🌟【全库唯一合并总索引】(实时看板+文献卡片+概念总表)
├── Sources/
│   └── Papers/                   # 📚 纯净文献笔记库 (示例演示文献)
│       ├── he2016deep.md         # ResNet 深度残差学习 (CVPR 2016)
│       ├── vaswani2017attention.md # Transformer 自注意力架构 (NeurIPS 2017)
│       └── hu2021lora.md         # LoRA 低秩自适应微调 (ICLR 2022)
├── Knowledge/
│   ├── Literature Overview.md    # 📊 综合成果：领域文献全景综述与发展里程碑
│   ├── Method Taxonomy.md        # 🌳 综合成果：研究方法学三层分类体系
│   ├── Research Gaps.md          # 🎯 综合成果：开放学术挑战与优先级矩阵
│   └── Concepts/                 # 🧬 原子理论概念卡片
│       ├── residual_connection.md
│       ├── self_attention.md
│       └── parameter_efficient_fine_tuning.md
├── Writing/
│   └── comparison-matrix.md      # 📝 跨文献全景横向对比矩阵
├── Maps/
│   └── literature.canvas         # 🗺️ 3 泳道 JSON Canvas 可视化拓扑图谱
├── Templates/                    # 📋 Zotero 导入模板与标准笔记模板
├── Scripts/                      # ⚡ 一键执行与自迭代脚本
├── src/kb_tools/                 # 🐍 Python 自动化 CLI 核心源码
├── tests/                        # 🧪 192 项 pytest 单元与对抗性测试用例
└── SCHOLARFLOW_WORKFLOW_GUIDE.md # 📖 深度图文实操全景指南
```

---

## 🧪 自动化测试验证

运行完整的 192 项测试用例：

```bash
python -m pytest -v
```

```text
============================= 192 passed in 8.10s =============================
```

---

## 🤝 参与贡献与社区交流

欢迎提交 Issue 与 Pull Request！在提交前请阅读 [CONTRIBUTING.md](CONTRIBUTING.md) 与 [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md)。

## 📄 开源许可证

本项目基于 [MIT 许可证](LICENSE) 开源。
