# 🌊 ScholarFlow (思流)

<p align="center">
  <strong>Autonomous, Self-Iterating Academic Knowledge Base & Literature Intelligence Engine</strong><br>
  <em>Inspired by Andrej Karpathy's "LLM Wiki" paradigm | Integrated with Zotero 7, Obsidian & AI / Codex Agents</em>
</p>

<p align="center">
  <a href="README_CN.md"><strong>🇨🇳 简体中文</strong></a> •
  <a href="README.md"><strong>🇺🇸 English</strong></a> •
  <a href="SCHOLARFLOW_WORKFLOW_GUIDE.md"><strong>📖 Full Guide</strong></a> •
  <a href="https://github.com/haha76haa-debug/ScholarFlow/issues"><strong>🐛 Report Bug</strong></a> •
  <a href="https://github.com/haha76haa-debug/ScholarFlow/discussions"><strong>💬 Discussions</strong></a>
</p>

<p align="center">
  <a href="https://github.com/haha76haa-debug/ScholarFlow/actions/workflows/ci.yml"><img src="https://github.com/haha76haa-debug/ScholarFlow/actions/workflows/ci.yml/badge.svg" alt="CI Status"></a>
  <img src="https://img.shields.io/badge/Python-3.10%2B-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Tests-192%2F192%20Passing-brightgreen.svg" alt="Tests">
  <img src="https://img.shields.io/badge/Obsidian-JSON%20Canvas%20v1.0-purple.svg" alt="Obsidian">
  <img src="https://img.shields.io/badge/Zotero-Better%20BibTeX%20%2B%20CSL-red.svg" alt="Zotero">
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License"></a>
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/PRs-welcome-brightgreen.svg" alt="PRs Welcome"></a>
</p>

---

## 🎯 What is ScholarFlow?

In traditional literature management, researchers often save hundreds of papers in Zotero or Obsidian where notes quickly become isolated silos. When drafting reviews, thesis proposals, or related work sections, connecting claims across papers requires tedious manual cross-checking.

**ScholarFlow** transforms your literature library into a **living, self-iterating knowledge network**:
- **Obsidian is your "Codebase"**: Notes are structured, modular atomic files.
- **LLM / AI Agent is your "Programmer"**: Reads your PDF annotations, extracts physics mechanisms, organizes method taxonomies, heals broken wikilinks, and auto-generates comprehensive comparison matrices.
- **Zotero 7 is your "Immutable Truth"**: Metadata and 6-color semantic highlights sync seamlessly into validated Evidence Records.

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

## ✨ Key Capabilities

| Capability | Description |
| :--- | :--- |
| **🧠 Karpathy LLM Wiki Architecture** | Closed-loop cycle: `Ingest ──► Decompose ──► Synthesize ──► Compare`. |
| **🛡️ Strict Claim Promotion Gate** | Claims can only graduate to established knowledge when backed by formal Evidence Records (`EVD-citekey-NN`). |
| **📊 Single Unified Master Index (`02-Index.md`)** | Real-time KPI dashboard, literature overview cards, concept tables, and synthesis navigation in one central hub. |
| **🗺️ Non-Overlapping 3-Lane Canvas** | Clean 8-arrow parallel pipeline (`Papers ──► Concepts ──► Syntheses`) in Obsidian JSON Canvas v1.0. |
| **🌐 100% Bilingual & LaTeX Support** | Paired `[EN]` / `[CN]` parallel reading with native $\LaTeX$ mathematical rendering ($\lambda \propto \sqrt{t_b t_{ox}}$, $I_{on}/W$, $R_c$). |
| **🧪 100% Test Coverage** | **192 unit and adversarial test cases** covering schema boundary checks, concurrency, and link repairs. |

---

## 🚀 Quick Start (3 Minutes)

### 1. Clone & Set Up Python Environment

```bash
# Clone the repository
git clone https://github.com/haha76haa-debug/ScholarFlow.git
cd ScholarFlow

# Create virtual environment
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On Linux/macOS:
source .venv/bin/activate

# Install dependencies in editable mode
pip install -e .
pip install pytest pyyaml
```

### 2. Run Self-Iteration Pipeline

```bash
# Execute the full automated maintenance pipeline
python Scripts/run_pipeline.py
```

### 3. Open Vault in Obsidian

1. Open **Obsidian** $	o$ Click **"Open folder as vault"**.
2. Select the `ScholarFlow` folder.
3. Press `Ctrl + G` to inspect the clean color-grouped **Graph View**.
4. Open `Maps/literature.canvas` to explore the 3-lane visual topology.

---

## 🛠️ CLI Toolsuite (`kb-tools`)

| Command | Usage | Description |
| :--- | :--- | :--- |
| **`lint`** | `kb-tools lint` | Validate YAML frontmatter against strict schema rules |
| **`sync-registry`** | `kb-tools sync-registry` | Synchronize single Master Index (`02-Index.md`) and `_system/registry.md` |
| **`repair-links`** | `kb-tools repair-links` | Scan and automatically heal broken wikilinks |
| **`synthesize`** | `kb-tools synthesize` | Generate Overview, Method Taxonomy, and Research Gaps |
| **`generate-canvas`** | `kb-tools generate-canvas` | Build non-overlapping `Maps/literature.canvas` topology |
| **`run-pipeline`** | `kb-tools run-pipeline` | Run complete end-to-end self-iteration pipeline |

---

## 📂 Vault Directory Layout

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
│   ├── Literature Overview.md    # Synthesis: Field literature overview
│   ├── Method Taxonomy.md        # Synthesis: Method classification tree
│   ├── Research Gaps.md          # Synthesis: Open challenges & bottlenecks
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

Run the comprehensive test suite:

```bash
python -m pytest -v
```

```text
============================= 192 passed in 8.10s =============================
```

---

## 🤝 Contributing

Contributions are warmly welcome! Please check out [CONTRIBUTING.md](CONTRIBUTING.md) and [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).

## 📄 License

This project is licensed under the [MIT License](LICENSE).
