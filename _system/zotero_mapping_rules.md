# Zotero Mapping Rules & Extraction Specifications

This document defines the authoritative transformation specifications from **Zotero / Better BibTeX / CSL-JSON** into canonical Obsidian vault notes.

---

## 1. Better BibTeX Citekey Formula & Normalization

### 1.1 Citation Key Formula
```text
[auth:lower][year][veryshorttitle:lower]
```

### 1.2 Component Definitions
1. **`auth`**:
   - Family name of the first author.
   - Non-ASCII characters transliterated to ASCII (e.g., `Müller` -> `muller`, `Bengio` -> `bengio`, `LeCun` -> `lecun`).
   - Punctuation, apostrophes, and spaces stripped.
   - Converted to lowercase.
2. **`year`**:
   - 4-digit publication year (e.g., `2016`, `2017`, `2021`).
   - If missing from record, fallback via regex `re.search(r'\d{4}', date_field)` or default to `unknown`.
3. **`veryshorttitle`**:
   - First significant word of the title in lowercase.
   - Strip leading/trailing punctuation.
   - Exclude English stop words: `a`, `an`, `the`, `on`, `for`, `in`, `of`, `with`, `and`, `to`, `at`, `from`, `by`, `is`, `are`, `about`.

### 1.3 Collision Disambiguation
If a generated citekey collides with an existing note:
- Append alphabetical suffixes: `he2016deepa`, `he2016deepb`, etc.

### 1.4 Canonical Examples
- He, Zhang, Ren, Sun (2016) *"Deep Residual Learning for Image Recognition"* $\to$ `he2016deep`
- Vaswani et al. (2017) *"Attention Is All You Need"* $\to$ `vaswani2017attention`
- Hu et al. (2021) *"LoRA: Low-Rank Adaptation of Large Language Models"* $\to$ `hu2021lora`
- Devlin et al. (2018) *"BERT: Pre-training of Deep Bidirectional Transformers"* $\to$ `devlin2018bert`

---

## 2. Zotero Item Type to Obsidian Type Matrix

| Zotero Item Type | Obsidian Note `type` | Obsidian `source_type` | Default Status | Target Directory | Promotion Gate Allowed? |
|---|---|---|---|---|---|
| `journalArticle` | `paper` | `journal article` | `to-read` | `Sources/Papers/` | **Yes** (if Evidence Record present) |
| `conferencePaper`| `paper` | `conference paper` | `to-read` | `Sources/Papers/` | **Yes** (if Evidence Record present) |
| `preprint`       | `paper` | `preprint` | `to-read` | `Sources/Papers/` | **Yes** (with preprint caveat) |
| `report`         | `paper` | `report` | `to-read` | `Sources/Papers/` | **Yes** (if verified) |
| `book`           | `paper` | `book` | `to-read` | `Sources/Papers/` | **Yes** |
| `bookSection`    | `paper` | `book chapter` | `to-read` | `Sources/Papers/` | **Yes** |
| `thesis`         | `paper` | `thesis` | `to-read` | `Sources/Papers/` | **Yes** |
| `webpage`        | `web` | `webpage placeholder` | `to-read` | `Sources/Web/` | **No** (Weak source) |
| `blogPost`       | `web` | `blog post` | `to-read` | `Sources/Web/` | **No** (Weak source) |
| `dataset`        | `data` | `dataset` | `active` | `Sources/Data/` | **Yes** (as data evidence) |
| `document`       | `doc` | `doc` | `active` | `Sources/Docs/` | **Yes** (as specification) |
| `interview`      | `doc` | `interview` | `active` | `Sources/Interviews/`| **No** (Qualitative background) |

---

## 3. PDF Annotation Semantic Color Taxonomy

When extracting annotations from Zotero PDF attachments, map colors to semantic Obsidian callouts and note sections:

| Color Name | Hex Code | Callout Type | Semantic Meaning | Destination Section in Note |
|---|---|---|---|---|
| **Yellow** | `#ffd400` | `> [!quote]+ Background / Motivation` | Background, research motivation, problem statement | `## Research question` / Context |
| **Green** | `#5fb236` | `> [!tip]+ Method & Implementation` | Architecture, algorithm, mathematical formulation, training setup | `## Method` |
| **Purple** | `#a28ae5` | `> [!note]+ Core Contribution & Claim` | Core contribution, key empirical finding, theoretical claim | `## Claim` / `## Evidence` |
| **Red** | `#ff6666` | `> [!warning]+ Limitation & Constraint` | Identified bottleneck, limitation, negative result, failure mode | `## Limitation` |
| **Blue** | `#2ea8e5` | `> [!info]+ Important Reference & Benchmark` | Baseline comparison, dataset, benchmark reference, related work | `## Relation to other papers` |
| **Gray** | `#aaaaaa` | `> [!quote]+ General Highlight` | General interesting snippet or quote | `## Key Annotations & Highlights` |

---

## 4. Evidence Record Contract Specification

Every empirical finding extracted from a paper must be structured as an Evidence Record:

```md
Evidence ID: EVD-<citekey>-<NN>
Source: [[Sources/Papers/he2016deep]]
Source type: full paper | preprint | conference paper | journal article
Supports: "<Concise assertion supported by the data>"
Contradicts: "<Prior assumption or conflicting finding contradicted, or empty>"
Method / dataset / metric: "<Evaluation protocol, dataset name, baseline vs result>"
Limitation: "<Stated boundary condition or compute limit>"
Project relevance: "<Actionable takeaway for this repository>"
Claim strength: speculative | observed | supported | strong
```

### Claim Promotion Gate:
- **Eligible**: Claims with valid `Evidence ID`, `source_type != webpage placeholder`, and empirical anchor.
- **Ineligible**: Abstract-only claims, unanchored opinions, speculative claims without evidence.
