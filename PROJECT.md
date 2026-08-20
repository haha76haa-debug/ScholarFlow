# Project: Zotero-Obsidian Academic Knowledge Base System

## Architecture
A dual-tier academic knowledge base integrating Zotero (source of truth & PDF annotations) and Obsidian (knowledge graph, networked thought, synthesis, and writing), backed by Python CLI automation tools (`kb_tools`) and autonomous agent operating protocols (`CLAUDE.md`, `AGENT.md`).

```
                               ┌────────────────────────────────┐
                               │     Zotero (Primary Source)    │
                               │  - Better BibTeX Citekeys      │
                               │  - Semantic PDF Annotations    │
                               └───────────────┬────────────────┘
                                               │ (Zotero Integration / CSL / BibTeX)
                                               ▼
┌─────────────────────────────────────────────────────────────────────────────────────────────────┐
│ Obsidian Academic Knowledge Base Vault                                                          │
│                                                                                                 │
│  ┌──────────────────────┐   ┌──────────────────────┐   ┌─────────────────────────────────────┐  │
│  │ Sources/Papers/      │──▶│ Knowledge/Concepts/  │──▶│ Writing/                            │  │
│  │ (Paper Notes, Claims)│   │ (Atomic Concepts)    │   │ (Synthesized drafts, reviews)       │  │
│  └──────────┬───────────┘   └──────────┬───────────┘   └─────────────────────────────────────┘  │
│             │                          │                                                        │
│             ▼                          ▼                                                        │
│  ┌─────────────────────────────────────────────────┐   ┌─────────────────────────────────────┐  │
│  │ Knowledge/ (Synthesis & Comparison Matrices)    │   │ Maps/literature.canvas              │  │
│  └─────────────────────────────────────────────────┘   │ (JSON Canvas v1.0 Visual Topology)  │  │
│                                                        └─────────────────────────────────────┘  │
└──────────────────────────────────────────────┬──────────────────────────────────────────────────┘
                                               ▲
                                               │ (Linter, Registry, Link Checker, Canvas, Synth)
┌──────────────────────────────────────────────┴──────────────────────────────────────────────────┐
│ Python Automation CLI Suite (`kb_tools`) & Agent Self-Iteration Protocols (`CLAUDE.md`/`AGENT.md`)│
└─────────────────────────────────────────────────────────────────────────────────────────────────┘
```

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Vault Directory Scaffolding | Standard namespace partitions (`Sources/`, `Knowledge/`, `Writing/`, `Daily/`, `Maps/`, `Templates/`, `Scripts/`, `_system/`, `.obsidian/`) | M1 | Survey (Explorer 1) |
| 2 | Frontmatter Contracts & Schemas | Strict YAML schemas for Paper Notes, Concept Notes, Synthesis Notes, Reading Logs | M1 | Survey (Explorer 1) |
| 3 | Core Obsidian Note Templates | Production Markdown templates with Jinja/Nunjucks-compatible placeholders and callouts | M1 | Survey (Explorer 1) |
| 4 | JSON Canvas v1.0 Specification | Formal JSON schema for `.canvas` visual graph representation with 6-color semantics and directional relations | M1 | Survey (Explorer 1) |
| 5 | Zotero Integration Plugin Template | Nunjucks template for Obsidian Zotero Integration plugin with semantic color highlighting | M2 | Survey (Explorer 2) |
| 6 | Better BibTeX & CSL Mapping Rules | Normalization rules for citekeys (`[auth:lower][year][veryshorttitle:lower]`), item types, and BibTeX fields | M2 | Survey (Explorer 2) |
| 7 | PDF Annotation Color Taxonomy | 6-color semantic schema (#ffd400 Context, #5fb236 Method, #a28ae5 Contribution, #ff6666 Limitation, #2ea8e5 Reference, #aaaaaa Misc) | M2 | Survey (Explorer 2) |
| 8 | Evidence Record Contract | Structured contract for empirical findings (`Evidence ID`, `Source`, `Supports`, `Contradicts`, `Method`, `Limitation`) | M2 | Survey (Explorer 2) |
| 9 | Agent Self-Iteration Protocol (`CLAUDE.md` & `AGENT.md`) | Ingestion, claim promotion gate, query conventions, linking taxonomy, and anti-patterns | M3 | Survey (Explorer 2) |
| 10 | Python Package Architecture (`kb_tools`) | CLI tools package structure, pyproject.toml, entrypoints `kb-tools` and `python -m kb_tools` | M4 | Survey (Explorer 3) |
| 11 | CLI Subcommand `lint` | Schema validation, YAML frontmatter checker, tag taxonomy enforcement, heading structure checker | M4 | Survey (Explorer 3) |
| 12 | CLI Subcommand `sync_registry` | Automated scanning and table-of-contents generation in `Sources/Papers/index.md` and `Knowledge/index.md` | M4 | Survey (Explorer 3) |
| 13 | CLI Subcommand `check_links` & `repair_links` | Dead/broken wikilink detection, fuzzy matching, and automatic repair | M4 | Survey (Explorer 3) |
| 14 | CLI Subcommand `synthesize` | Cross-paper topic clustering, claim alignment, and comparison matrix generation | M4 | Survey (Explorer 3) |
| 15 | CLI Subcommand `generate_canvas` | Automated JSON Canvas v1.0 graph generation from note relationships and frontmatter | M4 | Survey (Explorer 3) |
| 16 | CLI Subcommand `ingest` | Automated ingestion from BibTeX / CSL-JSON into compliant Paper Notes | M4 | Survey (Explorer 3) |
| 17 | Tool Unit Test Suite | Comprehensive pytest suite verifying all CLI modules, edge cases, and exit codes | M4 | Survey (Explorer 3) |
| 18 | Real Paper 1: ResNet (`he2016deep`) | Complete paper note, claims, evidence, annotations, and concept links | M5 | Survey (Explorer 3) |
| 19 | Real Paper 2: Transformer (`vaswani2017attention`) | Complete paper note, claims, evidence, annotations, and concept links | M5 | Survey (Explorer 3) |
| 20 | Real Paper 3: LoRA (`hu2021lora`) | Complete paper note, claims, evidence, annotations, and concept links | M5 | Survey (Explorer 3) |
| 21 | Cross-Paper Concept & Synthesis Notes | Atomic concepts (`residual_connection`, `self_attention`, `peft`) and literature synthesis note | M5 | Survey (Explorer 3) |
| 22 | Visual Literature Canvas (`literature.canvas`) | Valid Obsidian JSON Canvas v1.0 mapping the 3 papers, concepts, and relationships | M5 | Survey (Explorer 1, 3) |
| 23 | Comprehensive `README.md` User Guide | Complete user guide covering architecture, Zotero setup, CLI usage, agent workflows | M5 | Survey (Explorer 1, 2, 3) |
| 24 | E2E Testing Suite (Tiers 1-4) | Comprehensive requirement-driven opaque-box verification test suite | M6 / E2E Track | Survey (Explorer 3) |
| 25 | Tier 5 Adversarial Coverage Hardening | White-box adversarial testing, fuzzing, and robustness hardening | M6 (Phase 2) | Orchestrator Protocol |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Obsidian Skeleton, Schemas & Templates | Vault directories, schema contract definitions (`_system/schemas/`), Obsidian templates (`Templates/`) | None | DONE |
| M2 | Zotero Integration & Ingestion Specs | Zotero Integration Nunjucks template, annotation color taxonomy, CSL/BibTeX mapping specs | M1 | DONE |
| M3 | Agent Operating Protocols | `CLAUDE.md` and `AGENT.md` autonomous maintenance protocols, claim promotion gate, query rules | M1, M2 | DONE |
| M4 | Python Maintenance CLI Suite (`kb_tools`) | `kb_tools` package implementation (`lint`, `sync_registry`, `check_links`, `repair_links`, `synthesize`, `generate_canvas`, `ingest`), pytest unit tests | M1, M2, M3 | DONE |
| M5 | Real Paper Network, Canvas & User Guide | 3 Real academic paper notes, linked concept notes, literature synthesis, `Maps/literature.canvas`, `README.md` | M1, M2, M3, M4 | DONE |
| M6 | E2E Full Pass Verification & Hardening | Pass 100% E2E test suite (Tiers 1-4) + Tier 5 Adversarial Coverage Hardening with Challenger/Auditor | M1-M5, TEST_READY | DONE |

## Interface Contracts
### Obsidian Vault ↔ `kb_tools` Linter / Sync / Canvas
- **Paper Notes Path**: `Sources/Papers/<citekey>.md`
- **Concept Notes Path**: `Knowledge/Concepts/<slug>.md`
- **Synthesis Notes Path**: `Knowledge/<slug>.md`
- **Canvas Path**: `Maps/literature.canvas`
- **Frontmatter Required Fields (Paper Note)**:
  - `type`: `paper-note`
  - `citekey`: string (matching filename `<citekey>.md`)
  - `title`: string
  - `authors`: list of strings
  - `year`: integer
  - `item_type`: string (e.g. `journalArticle`, `conferencePaper`, `preprint`)
  - `tags`: list of strings starting with `#` or raw tag name
  - `claim_strength`: enum [`preliminary`, `validated`, `robust`, `consensus`, `disputed`]
  - `linked_knowledge`: list of `\[\[wikilink\]\]` strings
- **Frontmatter Required Fields (Concept Note)**:
  - `type`: `concept`
  - `title`: string
  - `tags`: list of strings
  - `claim_strength`: enum [`preliminary`, `validated`, `robust`, `consensus`, `disputed`]
  - `primary_sources`: list of `\[\[wikilink\]\]` strings
- **Canvas Format**: JSON Canvas v1.0 (`nodes`: list of node objects with `id`, `type`, `x`, `y`, `width`, `height`; `edges`: list of edge objects with `id`, `fromNode`, `toNode`, `label`, `color`).

## Verification Summary
- **Pytest Suite**: 192/192 passed across 9 test modules (100% pass rate in 9.59s).
- **Live Vault Lint**: `kb-tools lint --strict` -> 26 notes scanned, 0 errors, 0 warnings.
- **Link Resolution**: `kb-tools check-links` -> 228 links resolved, 0 dead links.
- **Registry Synchronization**: `kb-tools sync-registry` -> Clean idempotency.
- **Visual Canvas**: `Maps/literature.canvas` valid JSON Canvas v1.0.
- **Auditor Verdict**: **CLEAN** (Zero dummy code, genuine end-to-end integration).
