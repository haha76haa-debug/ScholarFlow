# Vault Schema & Contract Documentation

This document defines the authoritative architecture, data contracts, and validation rules governing the **Zotero-Obsidian Academic Knowledge Base System**.

---

## 1. Directory Structure

```text
zotero_obsidian_kb/
├── 00-Hub.md                      # Cockpit landing page & active inquiries
├── 01-Plan.md                     # Active research state & priority queue
├── 02-Index.md                    # Curated Master Index (MOC)
├── Sources/                       # Primary ingested source artifacts
│   ├── Papers/                    # Canonical paper notes (Zotero-sourced)
│   ├── Web/                       # Web articles & blogs
│   ├── Docs/                      # Technical documentation & whitepapers
│   ├── Data/                      # Dataset descriptions & benchmark metadata
│   ├── Interviews/                # Seminar notes & expert transcripts
│   └── Notes/                     # Uncategorized raw notes
├── Knowledge/                     # Distilled cross-paper knowledge network
│   ├── Concepts/                  # Atomic concepts, theorems & mechanisms
│   ├── Literature Overview.md     # Cross-paper domain synthesis & timeline
│   ├── Method Taxonomy.md         # Hierarchical classification of methods
│   └── Research Gaps.md           # Catalog of open research bottlenecks
├── Writing/                       # Research writing, drafts, and outlines
│   ├── Drafts/                    # Manuscript drafts & sections
│   └── Outlines/                  # Publication outlines
├── Daily/                         # Daily reading logs (YYYY-MM-DD.md)
├── Maps/                          # Visual JSON Canvas files (*.canvas)
│   └── literature.canvas          # Visual literature knowledge graph
├── Templates/                     # Canonical note templates
├── Scripts/                       # Automation CLI tool scripts
├── Archive/                       # Archived and deprecated notes
├── _system/                       # System schemas, registries, and reports
│   ├── schemas/                   # Machine-readable YAML contracts
│   │   ├── paper_schema.yaml
│   │   ├── concept_schema.yaml
│   │   └── synthesis_schema.yaml
│   ├── registry.md                # Single source of truth table registry
│   └── schema.md                  # This specification document
└── .obsidian/                     # Obsidian vault configuration
```

---

## 2. Note Types & Frontmatter Contracts

### 2.1 Paper Notes (`Sources/Papers/<citekey>.md`)
- **Required Frontmatter Keys**:
  - `type: paper`
  - `project`: string
  - `title`: string
  - `citekey`: string (matching filename `<citekey>.md`)
  - `zotero_key`: string
  - `status`: `unread` | `reading` | `read` | `to-review` | `archived`
  - `source_type`: `full paper` | `preprint` | `conference paper` | `journal article` | `abstract-only` | `webpage placeholder` | `book` | `thesis` | `report`
  - `claim_strength`: `speculative` | `observed` | `supported` | `strong`
  - `authors`: list of strings
  - `year`: integer
  - `linked_knowledge`: list of strings
  - `updated`: ISO 8601 UTC timestamp
- **Required H2 Headings**:
  1. `## Claim`
  2. `## Research question`
  3. `## Method`
  4. `## Evidence`
  5. `## Strengths`
  6. `## Limitation`
  7. `## Direct relevance to repo`
  8. `## Relation to other papers`
  9. `## Knowledge links`

### 2.2 Concept Notes (`Knowledge/Concepts/<slug>.md`)
- **Required Frontmatter Keys**:
  - `type: concept`
  - `project`: string
  - `title`: string
  - `status`: `active` | `draft` | `deprecated` | `archived`
  - `claim_strength`: `speculative` | `observed` | `supported` | `strong`
  - `primary_sources`: list of strings (wikilinks to `Sources/Papers/`)
  - `tags`: list of strings
  - `updated`: ISO 8601 UTC timestamp
- **Required H2 Headings**:
  1. `## Definition`
  2. `## Mathematical Formulation` (or `## Mechanism`)
  3. `## Primary Source Evidence`
  4. `## Strengths & Advantages`
  5. `## Known Limitations & Failure Modes`
  6. `## Related Concepts & Evolution`
  7. `## References`

### 2.3 Synthesis Notes (`Knowledge/<slug>.md`)
- **Required Frontmatter Keys**:
  - `type: literature-synthesis` (or `method-taxonomy`, `research-gaps`)
  - `project`: string
  - `title`: string
  - `status`: `active` | `draft` | `archived`
  - `covered_papers`: list of strings (wikilinks to `Sources/Papers/`)
  - `key_themes`: list of strings
  - `updated`: ISO 8601 UTC timestamp

---

## 3. Evidence Record Contract

Every empirical paper note must contain an Evidence Record formatted as follows:

````markdown
```md
Evidence ID: EVD-<citekey>-<NN>
Source: [[Sources/Papers/he2016deep]]
Source type: full paper
Supports: "Core assertion statement"
Contradicts: "Contradicting assumptions if any"
Method / dataset / metric: "Dataset name, baseline, score"
Limitation: "Identified boundary condition"
Project relevance: "Direct applicability to vault"
Claim strength: observed
```
````

---

## 4. Claim Promotion Gate

To prevent LLM hallucination and ensure vault rigor:
1. **Evidence Anchor Requirement**: A claim may only be promoted to `Knowledge/Concepts/` or `Knowledge/` if it references a valid `Evidence ID`.
2. **Source Modality Constraint**: Only `full paper`, `conference paper`, `journal article`, or verified `preprint` sources can promote claims. Sources marked `webpage placeholder` or `abstract-only` cannot promote claims.
3. **Epistemic Phrasing**:
   - `speculative`: "may suggest", "hypothesized"
   - `observed`: "indicates / demonstrates on dataset X"
   - `supported`: "establishes empirically across multiple benchmarks"
   - `strong`: "proves mathematically or universally validated"

---

## 5. Visual Topology (Obsidian Canvas v1.0)

Visual knowledge graphs in `Maps/*.canvas` conform to JSON Canvas v1.0:
- **Node Colors**:
  - `1` (Red): Research Gaps & Limitations
  - `2` (Orange): Paper Source Notes
  - `3` (Yellow): Methods & Algorithms
  - `4` (Green): Validated Claims & Benchmarks
  - `5` (Cyan): Syntheses & Overviews
  - `6` (Purple): Foundational Concepts & Mechanisms
- **Edge Semantics**: `supports`, `uses`, `extends`, `contradicts`, `motivates`, `summarizes`, `relates`.
