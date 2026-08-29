# AGENT.md — Autonomous Academic Knowledge Base Operating Constitution

This document defines the authoritative operating protocols, architecture, interface contracts, and lifecycle workflows for Autonomous AI Agents (Codex, Antigravity, LLMs) operating within the **Zotero-Obsidian Academic Knowledge Base System**.

---

## 1. System Overview & Vault Architecture

The Academic Knowledge Base implements a dual-tier epistemic architecture integrating **Zotero** (immutable reference master & PDF annotations) and **Obsidian** (networked concept graph, claim-level synthesis, and manuscript drafting), backed by Python CLI automation tools (`kb_tools`).

```text
zotero_obsidian_kb/
├── 00-Hub.md                      # Cockpit landing page, mission, and navigation MOC
├── 01-Plan.md                     # Active research plan, state variables & backlog
├── 02-Index.md                    # Curated Master Map of Content (MOC)
├── Sources/                       # Primary ingested source artifacts
│   ├── Papers/                    # Canonical paper notes (Sources/Papers/<citekey>.md)
│   ├── Web/                       # Web sources & online articles (Sources/Web/<slug>.md)
│   ├── Docs/                      # Technical manuals & specifications (Sources/Docs/<slug>.md)
│   ├── Data/                      # Dataset descriptions & benchmark metadata (Sources/Data/<slug>.md)
│   ├── Interviews/                # Seminar transcripts & expert notes (Sources/Interviews/<slug>.md)
│   └── Notes/                     # Uncategorized raw notes (Sources/Notes/<slug>.md)
├── Knowledge/                     # Distilled cross-paper knowledge network
│   ├── Concepts/                  # Atomic concepts, theorems & mechanisms (Knowledge/Concepts/<slug>.md)
│   ├── Literature Overview.md     # Cross-paper domain synthesis & chronological timeline
│   ├── Method Taxonomy.md         # Hierarchical classification & comparative complexity matrix
│   └── Research Gaps.md           # Catalog of open research bottlenecks & failure modes
├── Writing/                       # Research writing, drafts, and outlines
│   ├── Drafts/                    # Manuscript drafts & review chapters
│   └── Outlines/                  # Publication outlines & thesis structures
├── Daily/                         # Daily reading logs & ingestion journals (Daily/YYYY-MM-DD.md)
├── Maps/                          # Visual JSON Canvas v1.0 topologies
│   └── literature.canvas          # Auto-maintained literature knowledge network canvas
├── Templates/                     # Canonical note templates
│   ├── paper_template.md
│   ├── concept_template.md
│   ├── synthesis_template.md
│   ├── reading_log_template.md
│   ├── web_source_template.md
│   └── collection_inventory_template.md
├── Scripts/                       # Automation CLI scripts
├── Archive/                       # Archived & deprecated notes
├── _system/                       # System schemas, registries, and reports
│   ├── schemas/                   # Strict schema contract definitions (*.yaml)
│   │   ├── paper_schema.yaml
│   │   ├── concept_schema.yaml
│   │   └── synthesis_schema.yaml
│   ├── registry.md                # Central single source of truth table registry
│   ├── schema.md                  # Human-readable specification documentation
│   ├── zotero_template.njk        # Nunjucks template for Zotero Integration plugin
│   └── zotero_mapping_rules.md    # Citekey formula, item types & color taxonomy
└── .obsidian/                     # Obsidian vault configuration (app.json, types.json, etc.)
```

---

## 2. Agent Operating Principles & Workflow Lifecycle

### Phase 1: Ingestion Protocol
1. **Metadata & Annotation Intake**:
   - Extract bibliographic fields and semantic annotations from BibTeX, CSL-JSON, or Zotero exports.
   - Generate canonical Better BibTeX citekey via formula: `[auth:lower][year][veryshorttitle:lower]`.
2. **Canonical Note Creation**:
   - Create `Sources/Papers/<citekey>.md` strictly adhering to `_system/schemas/paper_schema.yaml`.
   - Populate required frontmatter (`type: paper`, `citekey`, `zotero_key`, `status: to-read`, `source_type`, `claim_strength: observed`, `authors`, `year`, `linked_knowledge`, `updated`).
   - Populate all 9 required H2 headings: `## Claim`, `## Research question`, `## Method`, `## Evidence`, `## Strengths`, `## Limitation`, `## Direct relevance to repo`, `## Relation to other papers`, `## Knowledge links`.
3. **Evidence Record Extraction**:
   - Structure empirical data into an Evidence Record block under `## Evidence` (`Evidence ID: EVD-<citekey>-01`, `Supports`, `Method / dataset / metric`, `Project relevance`, `Claim strength`).
4. **Registry & Navigation Synchronization**:
   - Register note in `_system/registry.md` under `## Sources` with stable ID `paper-XXX`.
   - Index note in `02-Index.md` under `## 2. Sources Namespace`.
   - Log activity and promotable items in today's `Daily/YYYY-MM-DD.md`.

### Phase 2: Linking & Synthesis Protocol (Claim Promotion Gate)
1. **Claim Promotion Gate Verification**:
   - Before promoting an assertion from a paper to `Knowledge/Concepts/` or `Knowledge/`:
     - **Anchor Check**: Must reference a valid `Evidence ID` (`EVD-<citekey>-NN`).
     - **Modality Check**: Source must be `full paper`, `conference paper`, `journal article`, or verified `preprint` (Reject `webpage placeholder` or `abstract-only`).
     - **Strength Alignment**: Phrasing must strictly match `claim_strength` (`speculative` $\to$ "may suggest", `observed` $\to$ "indicates on dataset X", `supported` $\to$ "establishes empirically", `strong` $\to$ "proves mathematically").
2. **Atomic Concept Promotion**:
   - Create or update atomic concept note in `Knowledge/Concepts/<slug>.md` complying with `_system/schemas/concept_schema.yaml`.
   - Include formal `## Definition`, `## Mathematical Formulation` (or `## Mechanism`), `## Primary Source Evidence`, `## Strengths & Advantages`, `## Known Limitations & Failure Modes`, `## Related Concepts & Evolution`, and `## References`.
3. **Cross-Paper Synthesis Update**:
   - Update `Knowledge/Literature Overview.md` (chronological evolution & benchmark comparison).
   - Update `Knowledge/Method Taxonomy.md` (hierarchical categorization & asymptotic complexity).
   - Update `Knowledge/Research Gaps.md` (unresolved bottlenecks & boundary limits).
4. **Bidirectional Graph Wiring**:
   - Ensure paper notes link to concepts/syntheses via `linked_knowledge` and `## Knowledge links`.
   - Ensure concept/synthesis notes link back to primary source paper notes.

### Phase 3: Autonomous Maintenance Protocol
1. **Lint Validation**: Execute `python -m kb_tools lint` to verify YAML frontmatter, required headings, and schema compliance.
2. **Registry Parity**: Execute `python -m kb_tools sync_registry` to ensure every active note is registered and indexed.
3. **Link Integrity**: Execute `python -m kb_tools check_links --repair` to detect and repair broken or dangling wikilinks.
4. **Visual Topology Regeneration**: Execute `python -m kb_tools generate_canvas` to update `Maps/literature.canvas`.

### Phase 4: Multi-Modal Visual & Zero-Barrier Ingestion Protocol
1. **Triad Multi-Modal Standard**: Every paper note and concept note must include (a) a Hero Visual (3D cross-section or energy band diagram), (b) a layer-by-layer parameter breakdown, and (c) Mermaid vector flowcharts for processes. Never use ASCII art.
2. **Zero-Barrier Q&A Ingestion**: When user poses a free-form question about a paper, immediately provide Feynman-level explanation, auto-draft atomic concept note, request confirmation, then ingest upon approval ("存入").
3. **Paper Evidence Citation Standard（原文引用锚定规范）**: Every key claim, quantitative conclusion, or method description in paper notes (`Sources/Papers/*.md`) MUST be followed by the corresponding verbatim original text in an Obsidian callout block:
   ```
   > [!quote] 原文引用 (p. XX / Section X.X)
   > "...exact original sentence from the paper..."
   ```
   - Citation block placed **after** the Chinese/English summary, **before** the next bullet
   - Page number or section reference mandatory for traceability
   - Apply to concept notes (`Knowledge/Concepts/*.md`) whenever citing specific paper evidence
   - Backfill existing notes incrementally when content is revisited, not all at once

---

## 3. CLI Maintenance Tool Suite Command Signatures

| Command | Signature | Description |
|---|---|---|
| **Lint Vault** | `python -m kb_tools lint [--cwd <path>] [--strict]` | Validates schema contracts, frontmatter, required headings, and Evidence Records. |
| **Sync Registry** | `python -m kb_tools sync_registry [--cwd <path>]` | Synchronizes `_system/registry.md` and `02-Index.md` with filesystem notes. |
| **Check & Repair Links** | `python -m kb_tools check_links [--cwd <path>] [--repair]` | Scans for broken wikilinks, detects case/folder mismatches, and repairs targets. |
| **Synthesize Topics** | `python -m kb_tools synthesize [--cwd <path>] [--topic <name>]` | Aggregates cross-paper claims, methods, and evidence matrices into synthesis notes. |
| **Generate Canvas** | `python -m kb_tools generate_canvas [--cwd <path>] [--output <path>]` | Builds deterministic JSON Canvas v1.0 visual graph (`Maps/literature.canvas`). |
| **Ingest Source** | `python -m kb_tools ingest --format [bibtex\|csl-json\|zotero-api] --input <path_or_key>` | Ingests metadata and annotations, generating schema-compliant Paper Notes. |

---

## 4. Linking & Wikilink Rules

1. **Vault-Internal Note Links**:
   - Use standard Obsidian wikilinks: `[[Sources/Papers/vaswani2017attention]]`.
   - Use aliases when helpful: `[[Sources/Papers/vaswani2017attention|Vaswani et al. (2017)]]`.
   - Use folder-qualified paths to prevent ambiguity: `[[Sources/Papers/he2016deep]]` vs `[[Knowledge/Concepts/residual_connection]]`.
2. **Section & Block Anchors**:
   - Heading links: `[[Sources/Papers/vaswani2017attention#Evidence|Vaswani et al. Evidence]]`.
   - Block links: `[[Sources/Papers/vaswani2017attention#^evd-01]]`.
3. **External Resources**:
   - Use standard Markdown hyperlinks: `[arXiv:1706.03762](https://arxiv.org/abs/1706.03762)`.
   - Use Zotero deep-link URIs for annotations: `[Open in Zotero](zotero://open-pdf/0_xxx/1)`.
4. **Typed Paper Relationships**:
   - Format in paper YAML `paper_relationships`:
     - `"Sources/Papers/bahdanau2014neural::extends"`
     - `"Sources/Papers/devlin2018bert::precedes"`
     - `"Sources/Papers/other2020work::complements"`
     - `"Sources/Papers/other2021work::contradicts"`
     - `"Knowledge/Concepts/self_attention::uses"`

---

## 5. Query Conventions for LLM Agents

1. **Context Discovery Hierarchy**:
   - Step 1: Read `00-Hub.md` and `01-Plan.md` to identify active research questions and current state.
   - Step 2: Query `_system/registry.md` to resolve note IDs, paths, and statuses.
   - Step 3: Check `02-Index.md` for thematic clusters.
   - Step 4: Access specific canonical notes in `Sources/Papers/` or `Knowledge/Concepts/`.
2. **Property-Based Retrieval**:
   - Filter papers by frontmatter attributes: `status: read`, `subfield: <topic>`, `claim_strength: strong`, `methods: [...]`.
3. **Avoid Full Vault Scans**:
   - Do not grep the entire vault when a registry lookup or index consultation provides the exact note path.

---

---

## 6. Bilingual (Chinese-English) Format Standard / 全库中英文对照规范

All literature notes, concept abstractions, syntheses, and templates in this repository MUST strictly follow a paired **Chinese-English bilingual standard**:

1. **Literature Notes (`Sources/Papers/`)**:
   - Title must include Chinese translated title (`> **中文译名**：...`).
   - Core structural sections (`Claim`, `Research question`, `Method`, `Strengths`, `Limitation`, `Direct relevance`) must provide both English scientific articulation (`- **[EN]**: ...`) and precise academic Chinese translation (`- **[CN]**: ...`).
   - High-priority PDF annotations (`Key Annotations & Highlights`) must include the original English extract accompanied by an accurate Chinese translation and research note.

2. **Concept Notes (`Knowledge/Concepts/`)**:
   - `Definition`, `Mathematical Formulation`, `Theoretical Grounding`, `Evidence & Empirical Support`, and `Limitations` must be rendered in parallel English and Chinese blocks.

3. **Domain Syntheses & Overviews (`Knowledge/`)**:
   - Comparative matrices, methodology taxonomy trees, and research gap catalogs must provide bilingual explanations and column headers.

4. **Agent Generation Mandate**:
   - Whenever an AI Agent (Codex, Antigravity, Claude, LLM) creates or modifies notes in this vault, it MUST automatically generate both English and Chinese paired content. Single-language notes are considered non-conformant.

---

## 7. Anti-Patterns & Strict Prohibitions

- ❌ **No Root Pollution**: Never create note files in the root folder (only `00-Hub.md`, `01-Plan.md`, and `02-Index.md` are permitted).
- ❌ **No Orphan Notes**: Every canonical note must be registered in `_system/registry.md` and indexed in `02-Index.md`.
- ❌ **No Unanchored Synthesis**: Knowledge and concept notes must cite primary source paper notes with explicit anchors.
- ❌ **No Unvetted Claim Promotion**: Never promote ungrounded claims, abstract-only summaries, or `webpage placeholder` sources into `Knowledge/`.
- ❌ **No Duplicate Notes**: Do not duplicate existing notes for the same paper (update in-place by `citekey` or `zotero_key`).
- ❌ **No Parallel Registries**: `_system/registry.md` is the only project registry.
- ❌ **No Dense All-to-All Canvas Topologies**: Visual canvas graphs must follow sparse argument-tree geometry (`Paper -> Claim -> Method -> Gap`).

---

## 8. Autonomous Maintenance & Daily Promotion Loop

1. **Daily Log Triage**:
   - Scan `Daily/` logs for pending items in `> [!tip] Promotable Items`.
   - Promote verified concept candidates to `Knowledge/Concepts/<slug>.md`.
2. **Plan Progression**:
   - Review completed milestones and update `## Current Research State` in `01-Plan.md`.
3. **Automated Tool Execution**:
   - Run `kb_tools lint` $\to$ `kb_tools sync_registry` $\to$ `kb_tools check_links` $\to$ `kb_tools generate_canvas`.
   - Ensure zero errors in `_system/lint-report.md`.
