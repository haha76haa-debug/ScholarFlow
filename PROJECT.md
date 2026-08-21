# Project: ScholarFlow Silicon Parallels Extension

## Architecture
ScholarFlow is a high-rigor research knowledge base bridging 2D semiconductor materials science and industrial silicon microelectronics. It combines an Obsidian markdown vault with an automated Python toolchain (`kb_tools`) and a multi-tier pytest verification suite.

### Data Flow & Component Hierarchy
```
Sources/Papers (Literature Notes)
       │
       ├──► Knowledge/Concepts (Atomic Physics & Theory)
       │           │
       │           └──► Knowledge/Comparisons (6D Microelectronics Benchmark Cards)
       │                      │
       ▼                      ▼
Knowledge/Syntheses & Writing (Overview, Taxonomy, Gaps, Comparison Matrix)
       │
       ├──► Maps/literature.canvas (4-Lane Horizontal Straight Streamline Visual Canvas)
       └──► 02-Index.md & _system/registry.md (Master Indexes & Registries)
```

---

## Feature Inventory
| # | Feature | Description | Milestone | Source |
|---|---------|-------------|-----------|--------|
| 1 | Comparison Schema & Template | `_system/schemas/comparison_schema.yaml` and `Templates/comparison_template.md` defining 6-dimensional comparison card contracts. | M1 | Survey / Follow-up Request §R1 |
| 2 | 6D Microelectronics Comparison Cards | Masterclass comparison cards in `Knowledge/Comparisons/` (`2d_contact_vdW_vs_silicon_silicide.md`, `2d_electrostatic_scaling_vs_silicon_gaafet.md`) covering all 6 engineering dimensions. | M1 | Survey / Follow-up Request §R1 |
| 3 | Literature Note Silicon Analogy Sections | `## Silicon Analogy & Microelectronics Mapping` sections in `Sources/Papers/` (`2021_Liu_2D-Transistors.md`, `2022_Cheng_FET-Benchmark.md`) with EN/CN text and bidirectional links. | M2 | Survey / Follow-up Request §R2 |
| 4 | 4-Lane Canvas Generation | 4-lane horizontal straight streamline layout in `src/kb_tools/canvas_gen.py` (Col 1: Papers, Col 2: Concepts, Col 3: Comparisons Cyan `#0891b2`, Col 4: Syntheses/Writing). | M3 | Survey / Follow-up Request §R3 |
| 5 | Obsidian Graph View Color Configuration | `.obsidian/graph.json` configuration adding color group for `path:Knowledge/Comparisons` with Cyan `#0891b2` (RGB 561586). | M3 | Survey / Follow-up Request §R3 |
| 6 | Linter Comparison Validation & Tags | `src/kb_tools/linter.py` validation for comparison note schema, 6-D headings, and updated taxonomy tags. | M4 | Survey / Follow-up Request §R4 |
| 7 | Synthesizer Silicon Matrix Generation | `src/kb_tools/synthesizer.py` populating Silicon Benchmark / Analog columns in `Writing/comparison-matrix.md`. | M4 | Survey / Follow-up Request §R4 |
| 8 | Registry & 02-Index Synchronization | `src/kb_tools/registry.py` updating `02-Index.md` with Section 5 (Silicon Parallels) and syncing `_system/registry.md`. | M4 | Survey / Follow-up Request §R4 |
| 9 | CLI Pipeline Subcommand | `src/kb_tools/cli.py` adding `run-pipeline` / `run_pipeline` subcommand executing all 5 workflow steps. | M4 | Survey / Follow-up Request §R4 |
| 10 | Comprehensive Pytest Suite Expansion | 195+ passing unit and regression tests in `tests/` covering comparison linting, 4-lane canvas, silicon synthesizer, CLI, and end-to-end flows. | M5 | Survey / Follow-up Request §R5 |
| 11 | Pipeline Verification & Zero-Defect Signoff | Full execution of `kb-tools run-pipeline` with 0 errors, 0 warnings, and 0 broken links. | M5 | Survey / Follow-up Request §R5 |

---

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|--------|
| M1 | Comparison Schema & 6D Cards | `_system/schemas/comparison_schema.yaml`, `Templates/comparison_template.md`, and 2+ 6D comparison cards in `Knowledge/Comparisons/` | none | DONE |
| M2 | Literature Note Mapping | `Sources/Papers/` updates with `## Silicon Analogy & Microelectronics Mapping` and bidirectional wikilinks | M1 | DONE |
| M3 | 4-Lane Canvas & Graph Config | `src/kb_tools/canvas_gen.py` 4-lane layout, `Maps/literature.canvas`, and `.obsidian/graph.json` | M1, M2 | IN_PROGRESS |
| M4 | Toolchain & Registry Updates | `src/kb_tools/linter.py`, `synthesizer.py`, `registry.py`, `cli.py`, `Writing/comparison-matrix.md`, `02-Index.md` | M1, M2, M3 | PLANNED |
| M5 | E2E Testing & Pipeline Verification | Full pytest test suite (195+ tests, 100% passing), `kb-tools run-pipeline` zero error verification | M1, M2, M3, M4 | PLANNED |

---

## Interface Contracts
### Comparison Notes ↔ Linter / Synthesizer / Registry
- **File location**: `Knowledge/Comparisons/<slug>.md`
- **Frontmatter**:
  - `type`: `comparison` (or `silicon-comparison`)
  - `title`: string
  - `project`: string
  - `status`: `active` | `draft` | `deprecated`
  - `claim_strength`: `speculative` | `observed` | `supported` | `strong`
  - `primary_sources`: list of wikilinks `[[Sources/Papers/2021_Liu_2D-Transistors]]`
  - `silicon_technology` / `silicon_reference_nodes`: string / list of strings
- **Required H2 Headings**:
  1. `## Executive Overview & Silicon Analogy`
  2. `## 1. Physical Scaling & Electrostatic Control`
  3. `## 2. Ohmic Contact & Metallization Engineering`
  4. `## 3. Gate Dielectric & EOT Scaling`
  5. `## 4. CMOS Integration & Thermal Budget`
  6. `## 5. IRDS Technology Roadmap Alignment`
  7. `## 6. Electrical Benchmark & Compact Modeling Matrix`
  8. `## References & Evidence Anchors`

### Canvas Generation Coordinates
- **Col 1 (Papers)**: X = 0, Width = 460
- **Col 2 (Concepts)**: X = 680, Width = 460
- **Col 3 (Silicon Comparisons)**: X = 1360, Width = 460, Color: Cyan `#0891b2`
- **Col 4 (Syntheses & Writing)**: X = 2040, Width = 460
- **Group Containers**: 4 column groups matching column X boundaries with width 540 and height calculated dynamically.

### CLI Pipeline Protocol
- Command: `kb-tools run-pipeline [--vault-dir .] [--strict] [--dry-run] [--json]`
- Sequence: Lint (`--strict`) -> Sync Registry -> Check Links -> Synthesize -> Generate Canvas
- Exit code: 0 on complete pass, 1 on any error or strict warning.

---

## Code Layout
```
zotero_obsidian_kb/
├── .obsidian/
│   └── graph.json                     # Graph view color configuration
├── _system/
│   ├── schemas/
│   │   ├── paper_schema.yaml
│   │   ├── concept_schema.yaml
│   │   ├── synthesis_schema.yaml
│   │   └── comparison_schema.yaml     # M1: Comparison note schema contract
│   ├── registry.md                    # Authoritative vault registry
│   └── schema.md
├── Templates/
│   ├── paper_template.md
│   ├── concept_template.md
│   ├── synthesis_template.md
│   └── comparison_template.md         # M1: Comparison note template
├── Sources/
│   └── Papers/
│       ├── 2021_Liu_2D-Transistors.md # M2: Updated with Silicon Analogy
│       └── 2022_Cheng_FET-Benchmark.md # M2: Updated with Silicon Analogy
├── Knowledge/
│   ├── Concepts/                      # Atomic concept notes
│   ├── Comparisons/                   # M1: 6D microelectronics comparison cards
│   │   ├── 2d_contact_vdW_vs_silicon_silicide.md
│   │   └── 2d_electrostatic_scaling_vs_silicon_gaafet.md
│   ├── Literature Overview.md
│   ├── Method Taxonomy.md
│   └── Research Gaps.md
├── Writing/
│   └── comparison-matrix.md           # M4: Updated with Silicon Benchmark column
├── Maps/
│   └── literature.canvas              # M3: 4-lane visual canvas
├── 02-Index.md                        # M4: Updated with Section 5
├── src/
│   └── kb_tools/
│       ├── canvas_gen.py              # M3: 4-lane canvas generation logic
│       ├── linter.py                  # M4: Comparison note linting & tags
│       ├── synthesizer.py             # M4: Silicon comparison matrix synthesis
│       ├── registry.py                # M4: 02-Index & registry sync
│       ├── cli.py                     # M4: run-pipeline subcommand
│       ├── models.py
│       └── link_checker.py
├── Scripts/
│   └── run_pipeline.py                # Master runner script
└── tests/
    ├── conftest.py                    # Test fixtures
    ├── test_linter.py                 # M5: Comparison lint tests
    ├── test_canvas_gen.py             # M5: 4-lane canvas tests
    ├── test_synthesizer.py            # M5: Silicon matrix tests
    ├── test_registry.py               # M5: Registry & index tests
    ├── test_cli.py                    # M5: CLI pipeline tests
    ├── test_link_checker.py           # M5: Bidirectional link tests
    ├── test_e2e.py                    # M5: End-to-end integration tests
    ├── test_adversarial_challenge.py
    └── test_tier5_adversarial.py
```
