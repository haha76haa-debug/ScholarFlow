# Zotero Integration Nunjucks Template

This template is configured in the **Obsidian Zotero Integration** community plugin (or used by the automated `kb_tools ingest` CLI module).

---

## Template Source Code

```jinja2
---
type: paper
project: {{projectSlug | default("zotero_obsidian_kb")}}
title: "{{title | replace('"', '\\"')}}"
citekey: "{{citekey | default(citationKey)}}"
zotero_key: "{{key | default(zoteroKey)}}"
canvas_visibility: visible
status: to-read
source_type: {{ "preprint" if publicationTitle == "arXiv" or itemType == "preprint" else ("book" if itemType == "book" else ("conference paper" if itemType == "conferencePaper" else ("journal article" if itemType == "journalArticle" else "full paper"))) }}
claim_strength: observed
authors:
{%- for author in authors %}
  - "{{author.family}}, {{author.given}}"
{%- endfor %}
year: {{year | default(date | truncate(4, true, ""))}}
venue: "{{publicationTitle | default(conferenceName) | default(journal) | default('Preprint')}}"
doi: "{{doi}}"
url: "{{url | default('https://doi.org/' + doi if doi else '')}}"
keywords:
{%- for t in tags %}
  - "{{t.tag}}"
{%- endfor %}
concepts: []
methods: []
subfield: "{{subfield | default('general')}}"
related_papers: []
linked_knowledge:
  - "Knowledge/Literature Overview"
argument_claims: []
argument_methods: []
argument_gaps: []
paper_relationships: []
updated: {{ "now" | date("YYYY-MM-DDTHH:mm:ssZ") }}
---

# {{title}}

## Claim
*Primary assertion, theoretical hypothesis, or principal empirical finding.*

## Research question
*What specific research problem or bottleneck does this paper investigate?*

## Method
*Core architecture, algorithmic mechanism, formulation, or experimental setup.*

## Evidence
```md
Evidence ID: EVD-{{citekey | default(citationKey)}}-01
Source: [[Sources/Papers/{{citekey | default(citationKey)}}]]
Source type: full paper
Supports: "Primary claim of {{citekey | default(citationKey)}}"
Contradicts: ""
Method / dataset / metric: ""
Limitation: ""
Project relevance: ""
Claim strength: observed
```

## Strengths
- 

## Limitation
- 

## Direct relevance to repo
- 

## Relation to other papers
- 

## Knowledge links
- [[Knowledge/Literature Overview]]

## Key Annotations & Highlights
{%- if annotations and annotations.length > 0 %}
{%- for annotation in annotations %}
{%- if annotation.color == "#ffd400" or annotation.color == "yellow" %}
> [!quote]+ Background / Motivation (p. {{annotation.pageLabel | default(annotation.page)}})
> {{annotation.annotatedText}}
{%- if annotation.comment %}
>
> **Note**: {{annotation.comment}}
{%- endif %}
> [Open in Zotero]({{annotation.attachmentURI | default(annotation.desktopURI)}})

{%- elif annotation.color == "#5fb236" or annotation.color == "green" %}
> [!tip]+ Method & Implementation (p. {{annotation.pageLabel | default(annotation.page)}})
> {{annotation.annotatedText}}
{%- if annotation.comment %}
>
> **Note**: {{annotation.comment}}
{%- endif %}
> [Open in Zotero]({{annotation.attachmentURI | default(annotation.desktopURI)}})

{%- elif annotation.color == "#a28ae5" or annotation.color == "purple" %}
> [!note]+ Core Contribution & Claim (p. {{annotation.pageLabel | default(annotation.page)}})
> {{annotation.annotatedText}}
{%- if annotation.comment %}
>
> **Note**: {{annotation.comment}}
{%- endif %}
> [Open in Zotero]({{annotation.attachmentURI | default(annotation.desktopURI)}})

{%- elif annotation.color == "#ff6666" or annotation.color == "red" %}
> [!warning]+ Limitation & Constraint (p. {{annotation.pageLabel | default(annotation.page)}})
> {{annotation.annotatedText}}
{%- if annotation.comment %}
>
> **Note**: {{annotation.comment}}
{%- endif %}
> [Open in Zotero]({{annotation.attachmentURI | default(annotation.desktopURI)}})

{%- elif annotation.color == "#2ea8e5" or annotation.color == "blue" %}
> [!info]+ Important Reference & Benchmark (p. {{annotation.pageLabel | default(annotation.page)}})
> {{annotation.annotatedText}}
{%- if annotation.comment %}
>
> **Note**: {{annotation.comment}}
{%- endif %}
> [Open in Zotero]({{annotation.attachmentURI | default(annotation.desktopURI)}})

{%- else %}
> [!quote]+ General Highlight (p. {{annotation.pageLabel | default(annotation.page)}})
> {{annotation.annotatedText}}
{%- if annotation.comment %}
>
> **Note**: {{annotation.comment}}
{%- endif %}
> [Open in Zotero]({{annotation.attachmentURI | default(annotation.desktopURI)}})

{%- endif %}
{%- endfor %}
{%- else %}
*No annotations extracted yet.*
{%- endif %}
```
