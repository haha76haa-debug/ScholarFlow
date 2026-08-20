# 🌊 ScholarFlow (思流)

> **Autonomous, Self-Iterating Academic Knowledge Base & Literature Intelligence Engine**  
> *Inspired by Andrej Karpathy's "LLM Wiki" paradigm | Integrated with Zotero 7, Obsidian & LLM / Codex Agents*

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-192%2F192%20Passing-brightgreen.svg)](tests/)
[![CI](https://github.com/scholarflow/scholarflow/actions/workflows/ci.yml/badge.svg)](https://github.com/)
[![Obsidian](https://img.shields.io/badge/Obsidian-JSON%20Canvas%20v1.0-purple.svg)](https://jsoncanvas.org/)
[![Zotero](https://img.shields.io/badge/Zotero-Better%20BibTeX%20%2B%20CSL-red.svg)](https://retorque.re/zotero-better-bibtex/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](CONTRIBUTING.md)

[English Documentation](#-english-overview) | [中文说明文档](#-中文使用说明) | [实操全景指南](SCHOLARFLOW_WORKFLOW_GUIDE.md)

---

## 📖 English Overview

**ScholarFlow** is a production-grade, self-iterating academic research knowledge base system. It turns raw scientific literature and PDF annotations from **Zotero** into a living, interconnected, and self-growing knowledge network inside **Obsidian**, governed by strict evidentiary rules, autonomous AI agent protocols (**`CLAUDE.md`**, **`AGENT.md`**), and a comprehensive Python automation toolsuite (**`kb-tools`**).

### ✨ Key Features

1. **🧠 Karpathy "LLM Wiki" Architecture for Academia**:
   - Automated lifecycle: `Ingest (文献摄取) ──► Decompose (概念拆解) ──► Synthesize (全景综合) ──► Compare (矩阵对比)`.
2. **🛡️ Claim Promotion Gate & Evidence Integrity**:
   - Enforces strict verification: claims can only graduate to established knowledge when backed by formal Evidence Records (`EVD-citekey-NN`) from peer-reviewed publications.
3. **⚡ Built-in Python CLI Toolsuite (`kb-tools`)**:
   - `kb-tools lint`: Strict YAML frontmatter and schema validator.
   - `kb-tools sync-registry`: Single Master Index (`02-Index.md`) and metadata registry auto-sync.
   - `kb-tools repair-links`: Bi-directional link healer and orphan detector.
   - `kb-tools synthesize`: Dynamic generation of Literature Overviews, Method Taxonomies, and Research Gaps.
   - `kb-tools generate-canvas`: Non-crossing 3-lane Obsidian JSON Canvas v1.0 visual topology generator.
4. **🌐 100% Bilingual Invariant & Native LaTeX Support**:
   - Paired `[EN]` / `[CN]` parallel reading with zero-loss LaTeX math rendering ($\lambda = \sqrt{rac{arepsilon_b}{arepsilon_{ox}} t_b t_{ox}}$, $I_{on}/W$, $R_c$).
5. **🧪 100% Test Coverage**:
   - **192 unit and adversarial test cases** covering schema edge cases, concurrent operations, and graph integrity.

---

## 🏛️ System Architecture

```
                               ┌────────────────────────────────────────┐
                               │       Zotero 7 (Immutable Source)      │
                               │  - Better BibTeX Standard Citekeys     │
                               │  - 6-Color Semantic PDF Highlights     │
                               └──────────────────┬─────────────────────┘
                                                  │ (Zotero Integration / CSL-JSON / BibTeX)
                                                  ▼
┌───────────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Obsidian Academic Knowledge Base Vault                                                                │
│                                                                                                       │
│  ┌────────────────────────┐     ┌────────────────────────┐     ┌───────────────────────────────────┐  │
│  │ Sources/Papers/        │────▶│ Knowledge/Concepts/    │────▶│ Writing/                          │  │
│  │ (Literature Notes)     │     │ (Atomic Concepts, Math)│     │ (Comparison Matrices, Drafts)     │  │
│  └───────────┬────────────┘     └───────────┬────────────┘     └───────────────────────────────────┘  │
│              │                              │                                                         │
│              ▼                              ▼                                                         │
│  ┌───────────────────────────────────────────────────────┐     ┌───────────────────────────────────┐  │
│  │ Knowledge/ (Literature Overview, Taxonomy, Gaps)      │     │ Maps/literature.canvas            │  │
│  └───────────────────────────────────────────────────────┘     │ (Obsidian JSON Canvas v1.0 Graph) │  │
│                                                                └───────────────────────────────────┘  │
└─────────────────────────────────────────────────┬─────────────────────────────────────────────────────┘
                                                  ▲
                                                  │ (Auto Lint, Sync, Synthesize, Canvas Gen)
┌─────────────────────────────────────────────────┴─────────────────────────────────────────────────────┐
│ Python Automation Toolsuite (`kb_tools`) & AI Agent Governance Protocols (`CLAUDE.md` / `AGENT.md`)   │
└───────────────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 🚀 Quick Start (3 Minutes)

### 1. Clone & Install Dependencies

```bash
# Clone the repository
git clone https://github.com/<your-username>/ScholarFlow.git
cd ScholarFlow

# Create and activate virtual environment
python -m venv .venv
# Windows:
.venv\Scriptsctivate
# Linux/macOS:
source .venv/bin/activate

# Install kb-tools in editable mode
pip install -e .
pip install pytest pyyaml
```

### 2. Run Self-Iteration Pipeline

```bash
# Execute the full automated maintenance pipeline
python Scripts/run_pipeline.py
```

### 3. Open Vault in Obsidian

1. Open **Obsidian** -> Click **"Open folder as vault"**.
2. Select the `ScholarFlow` repository folder.
3. Press `Ctrl + G` to inspect the clean color-grouped **Graph View**.
4. Open `Maps/literature.canvas` to explore the 3-lane visual research topology.

---

## 🛠️ CLI Toolsuite (`kb-tools`) Reference

| Command | Description |
| :--- | :--- |
| `kb-tools lint` | Validate vault frontmatter against strict YAML schemas |
| `kb-tools sync-registry` | Synchronize single Master Index (`02-Index.md`) and `_system/registry.md` |
| `kb-tools repair-links` | Scan and automatically heal broken wikilinks |
| `kb-tools synthesize` | Generate bilingual Overview, Taxonomy, and Gaps notes |
| `kb-tools generate-canvas` | Build non-overlapping `Maps/literature.canvas` topology |
| `kb-tools run-pipeline` | Run complete end-to-end self-iteration pipeline |

---

## 🇨🇳 中文使用说明

**ScholarFlow（思流）** 是一套基于 **Zotero 7 + Obsidian + AI Agent（Codex / Claude）** 的全自迭代学术知识库系统。借鉴了 Andrej Karpathy 的 “LLM Wiki” 范式，致力于解决科研人员文献读完就忘、笔记彼此孤立、缺乏体系化沉淀的痛点。

### 🌟 核心特色

- 📚 **Zotero 原生打通**：通过 Better BibTeX 自动生成规范 Citekey，6 色语义高亮批注一键提取为标准 Evidence Record。
- 🧬 **原子概念提炼**：自动将文献方法与物理机制沉淀为 `Knowledge/Concepts/` 独立概念卡片。
- 📊 **全局唯一总索引 (`02-Index.md`)**：聚合 KPI 统计看板、文献全景卡片、概念总表与综合成果导航，告别混乱。
- 🗺️ **3 泳道 Canvas 画布**：8 条单向水平箭头呈现 `文献 ──► 理论 ──► 产出` 极简流水线，告别杂乱连线。
- 🧪 **192 项全量自动化测试**：工业级代码与数据自洽性保障。

### 📖 详细实操全景指南
请参阅完整图文指南：[**`SCHOLARFLOW_WORKFLOW_GUIDE.md`**](SCHOLARFLOW_WORKFLOW_GUIDE.md)

---

## 📂 Vault Directory Structure

```text
ScholarFlow/
├── 00-Hub.md                     # Central navigation hub
├── 01-Plan.md                    # Research roadmap & reading queue
├── 02-Index.md                   # 🌟 Single Master Knowledge Index (MOC)
├── Sources/
│   └── Papers/                   # 📚 Pure literature notes
│       ├── 2021_Liu_2D-Transistors.md
│       └── 2022_Cheng_FET-Benchmark.md
├── Knowledge/
│   ├── Literature Overview.md    # Synthesis: Literature overview
│   ├── Method Taxonomy.md        # Synthesis: Method taxonomy tree
│   ├── Research Gaps.md          # Synthesis: Open challenges
│   └── Concepts/                 # 🧬 Atomic concept & physics cards
│       ├── contact_resistance_extraction.md
│       ├── emerging_fet_benchmarking.md
│       ├── saturation_current_density_benchmarking.md
│       └── two_dimensional_transistor_scaling.md
├── Writing/
│   └── comparison-matrix.md      # 📝 Cross-paper comparison matrix
├── Maps/
│   └── literature.canvas         # 🗺️ 3-Lane JSON Canvas visual topology
├── Templates/                    # 📋 Standard markdown & Zotero templates
├── Scripts/                      # ⚡ One-click pipeline & maintenance scripts
├── src/kb_tools/                 # 🐍 Python CLI core engine
├── tests/                        # 🧪 192 pytest unit & adversarial test cases
└── SCHOLARFLOW_WORKFLOW_GUIDE.md # 📖 Comprehensive operational handbook
```

---

## 🧪 Testing & Verification

Run the comprehensive 192-test suite:

```bash
python -m pytest -v
```

All 192 tests pass in < 10 seconds.

---

## 🤝 Contributing

Contributions are welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md) before submitting pull requests.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
