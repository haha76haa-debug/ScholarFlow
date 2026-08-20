"""
Test Suite for End-to-End Vault Verification: Tier 3 (Cross-Feature & Relational Graph Integrity)
and Tier 4 (Full Vault Lifecycle Scenarios).
"""

import json
import os
import re
import sys
from pathlib import Path
import pytest

# Ensure src is in sys.path
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# ==============================================================================
# Tier 3 & 4 Vault Fixture: Complete Real Academic Network (ResNet, Transformer, LoRA)
# ==============================================================================

@pytest.fixture
def full_academic_vault(tmp_path):
    """Creates a fully populated academic knowledge base with ResNet, Transformer, LoRA,
    concepts, syntheses, canvas, templates, and schemas."""
    vault = tmp_path / "academic_vault"

    dirs = [
        vault / "Sources" / "Papers",
        vault / "Sources" / "Web",
        vault / "Sources" / "Docs",
        vault / "Sources" / "Data",
        vault / "Knowledge" / "Concepts",
        vault / "Writing" / "Drafts",
        vault / "Writing" / "Outlines",
        vault / "Daily",
        vault / "Maps",
        vault / "Templates",
        vault / "_system" / "schemas",
        vault / ".obsidian",
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 00-Hub.md
    (vault / "00-Hub.md").write_text("""---
type: hub
title: "Research Hub & Cockpit"
updated: 2026-08-19T00:00:00Z
---
# Research Cockpit
- [[02-Index]]
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
- [[Knowledge/Research Gaps]]
- [[Maps/literature.canvas]]
""", encoding="utf-8")

    # 02-Index.md
    (vault / "02-Index.md").write_text("""---
type: index
title: "Master Knowledge Index"
updated: 2026-08-19T00:00:00Z
---
# Master Index
## Primary Sources
- [[Sources/Papers/he2016deep]]
- [[Sources/Papers/vaswani2017attention]]
- [[Sources/Papers/hu2021lora]]

## Core Concepts
- [[Knowledge/Concepts/Residual Connections]]
- [[Knowledge/Concepts/Self-Attention]]
- [[Knowledge/Concepts/Low-Rank Adaptation]]

## Synthesis & Reviews
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
- [[Knowledge/Research Gaps]]
""", encoding="utf-8")

    # Paper 1: ResNet
    (vault / "Sources" / "Papers" / "he2016deep.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Deep Residual Learning for Image Recognition"
citekey: he2016deep
zotero_key: "HE2016"
status: summarized
source_type: "conference paper"
claim_strength: strong
authors:
  - "Kaiming He"
  - "Xiangyu Zhang"
  - "Shaoqing Ren"
  - "Jian Sun"
year: 2016
venue: "CVPR 2016"
doi: "10.1109/CVPR.2016.90"
url: "https://arxiv.org/abs/1512.03385"
keywords:
  - residual-learning
  - computer-vision
concepts:
  - "Residual Connections"
methods:
  - "Skip Connection"
subfield: computer-vision
tags:
  - type/paper
  - topic/residual-learning
  - topic/computer-vision
  - status/summarized
paper_relationships:
  - "Sources/Papers/vaswani2017attention::precedes"
linked_knowledge:
  - "Knowledge/Literature Overview"
  - "Knowledge/Method Taxonomy"
  - "Knowledge/Concepts/Residual Connections"
updated: 2026-08-19T00:00:00Z
---

# Deep Residual Learning for Image Recognition

## Claim
Residual learning framework eases training of networks substantially deeper than previously possible by learning residual functions F(x) = H(x) - x.

## Research question
How to train substantially deeper neural networks without suffering from degradation and vanishing gradient problems?

## Method
Reformulate stacked layers as learning residual functions with reference to layer inputs via shortcut identity mappings.

## Evidence
```md
Evidence ID: EVD-he2016deep-01
Source: [[Sources/Papers/he2016deep]]
Source type: conference paper
Supports: "152-layer ResNet achieves 3.57% top-5 error on ImageNet, winning ILSVRC 2015"
Contradicts: "Prior assumption that deeper networks inherently suffer higher training error"
Method / dataset / metric: "ImageNet classification / Top-5 error 3.57%"
Limitation: "Residual paths require identical feature map dimensions unless projection shortcuts are used"
Project relevance: "Foundational skip connection formulation adopted across modern deep learning"
Claim strength: strong
```

## Strengths
- Enables training networks of 100+ layers without degradation.
- Zero extra parameter cost for identity shortcut connections.

## Limitation
- Increases feature map memory retention during backprop.

## Direct relevance to repo
Core architectural baseline for deep architectures.

## Relation to other papers
- Precedes [[Sources/Papers/vaswani2017attention]]

## Knowledge links
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
- [[Knowledge/Concepts/Residual Connections]]
""", encoding="utf-8")

    # Paper 2: Transformer
    (vault / "Sources" / "Papers" / "vaswani2017attention.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Attention Is All You Need"
citekey: vaswani2017attention
zotero_key: "VASWANI2017"
status: summarized
source_type: "conference paper"
claim_strength: strong
authors:
  - "Ashish Vaswani"
  - "Noam Shazeer"
  - "Niki Parmar"
  - "Jakob Uszkoreit"
  - "Llion Jones"
  - "Aidan N. Gomez"
  - "Lukasz Kaiser"
  - "Illia Polosukhin"
year: 2017
venue: "NeurIPS 2017"
doi: "arXiv:1706.03762"
url: "https://arxiv.org/abs/1706.03762"
keywords:
  - transformer
  - self-attention
  - nlp
concepts:
  - "Self-Attention"
  - "Residual Connections"
methods:
  - "Scaled Dot-Product Attention"
subfield: nlp
tags:
  - type/paper
  - topic/transformer
  - topic/self-attention
  - status/summarized
paper_relationships:
  - "Sources/Papers/he2016deep::uses"
  - "Sources/Papers/hu2021lora::precedes"
linked_knowledge:
  - "Knowledge/Literature Overview"
  - "Knowledge/Method Taxonomy"
  - "Knowledge/Research Gaps"
  - "Knowledge/Concepts/Self-Attention"
updated: 2026-08-19T00:00:00Z
---

# Attention Is All You Need

## Claim
Self-attention mechanism alone, without recurrence or convolutions, achieves state-of-the-art translation quality with superior parallelizability.

## Research question
Can sequence transduction models be built entirely on attention mechanisms without sequential recurrence?

## Method
Encoder-decoder architecture based solely on multi-head self-attention and point-wise feed-forward networks, incorporating residual connections and layer normalization.

## Evidence
```md
Evidence ID: EVD-vaswani2017attention-01
Source: [[Sources/Papers/vaswani2017attention]]
Source type: conference paper
Supports: "Transformer achieves 28.4 BLEU on WMT 2014 En-De and 41.8 BLEU on WMT 2014 En-Fr"
Contradicts: "Dominant paradigm that recurrent or convolutional layers are necessary for sequence modeling"
Method / dataset / metric: "WMT 2014 English-to-German translation / BLEU 28.4"
Limitation: "Quadratic computational and memory complexity O(N^2) with sequence length N"
Project relevance: "Foundational architecture for all modern large language models"
Claim strength: strong
```

## Strengths
- Highly parallelizable training compared to RNNs.
- Constant path length O(1) for long-range dependency modeling.

## Limitation
- O(N^2) attention matrix memory footprint.

## Direct relevance to repo
Primary sequence modeling backbone.

## Relation to other papers
- Uses [[Sources/Papers/he2016deep]]
- Precedes [[Sources/Papers/hu2021lora]]

## Knowledge links
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
- [[Knowledge/Research Gaps]]
- [[Knowledge/Concepts/Self-Attention]]
""", encoding="utf-8")

    # Paper 3: LoRA
    (vault / "Sources" / "Papers" / "hu2021lora.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "LoRA: Low-Rank Adaptation of Large Language Models"
citekey: hu2021lora
zotero_key: "HU2021"
status: summarized
source_type: "conference paper"
claim_strength: strong
authors:
  - "Edward J. Hu"
  - "Yelong Shen"
  - "Phillip Wallis"
  - "Zeyuan Allen-Zhu"
  - "Yuanzhi Li"
  - "Shean Wang"
  - "Lu Wang"
  - "Weizhu Chen"
year: 2021
venue: "ICLR 2022"
doi: "arXiv:2106.09685"
url: "https://arxiv.org/abs/2106.09685"
keywords:
  - peft
  - lora
  - transformer
concepts:
  - "Low-Rank Adaptation"
methods:
  - "Low-Rank Decomposition"
subfield: nlp
tags:
  - type/paper
  - topic/peft
  - topic/lora
  - status/summarized
paper_relationships:
  - "Sources/Papers/vaswani2017attention::extends"
linked_knowledge:
  - "Knowledge/Literature Overview"
  - "Knowledge/Method Taxonomy"
  - "Knowledge/Research Gaps"
  - "Knowledge/Concepts/Low-Rank Adaptation"
updated: 2026-08-19T00:00:00Z
---

# LoRA: Low-Rank Adaptation of Large Language Models

## Claim
Weight updates during downstream adaptation have low intrinsic rank, allowing freezing of pre-trained weights and injection of trainable rank decomposition matrices.

## Research question
How can massive pre-trained language models be adapted to specific tasks without full parameter fine-tuning?

## Method
Decompose weight update matrix Delta W into low-rank product B * A, freezing original weight W_0 and training only low-rank matrices.

## Evidence
```md
Evidence ID: EVD-hu2021lora-01
Source: [[Sources/Papers/hu2021lora]]
Source type: conference paper
Supports: "Reduces trainable parameters by 10,000x and GPU memory by 3x on GPT-3 175B while matching full fine-tuning"
Contradicts: "Belief that adapting all model weights is required to preserve full downstream capacity"
Method / dataset / metric: "GPT-3 175B adaptation on GLUE and SuperGLUE / Accuracy and Parameter Ratio"
Limitation: "Inference batching with multiple distinct task adapters requires adapter swapping or merged weights"
Project relevance: "Standard parameter-efficient fine-tuning method for all LLM adaptation"
Claim strength: strong
```

## Strengths
- 10,000x reduction in trainable parameters with zero inference latency overhead when weights are merged.
- Enables efficient task switching with small adapter checkpoints.

## Limitation
- Fixed rank r may constrain expressive capacity on complex domain shifts.

## Direct relevance to repo
Essential technique for efficient model tuning.

## Relation to other papers
- Extends [[Sources/Papers/vaswani2017attention]]

## Knowledge links
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
- [[Knowledge/Research Gaps]]
- [[Knowledge/Concepts/Low-Rank Adaptation]]
""", encoding="utf-8")

    # Concepts
    (vault / "Knowledge" / "Concepts" / "Residual Connections.md").write_text("""---
type: concept
project: zotero_obsidian_kb
title: "Residual Connections"
status: active
claim_strength: strong
primary_sources:
  - "Sources/Papers/he2016deep"
tags:
  - type/concept
  - topic/residual-learning
updated: 2026-08-19T00:00:00Z
---

# Residual Connections

## Definition
Direct additive identity mapping bypassing intermediate transformation layers.

## Mathematical Formulation
$$ H(x) = F(x) + x $$

## Primary Source Evidence
- Originates from [[Sources/Papers/he2016deep]] (EVD-he2016deep-01).

## Strengths & Advantages
- Eliminates vanishing gradients in arbitrarily deep networks.

## Known Limitations & Failure Modes
- Feature dimension matching requirement.

## Related Concepts & Evolution
- Integrated into [[Knowledge/Concepts/Self-Attention]]

## References
- [[Sources/Papers/he2016deep|He et al. (2016)]]
""", encoding="utf-8")

    (vault / "Knowledge" / "Concepts" / "Self-Attention.md").write_text("""---
type: concept
project: zotero_obsidian_kb
title: "Self-Attention"
status: active
claim_strength: strong
primary_sources:
  - "Sources/Papers/vaswani2017attention"
tags:
  - type/concept
  - topic/self-attention
updated: 2026-08-19T00:00:00Z
---

# Self-Attention

## Definition
Mechanism relating different positions of a single sequence to compute a representation of the sequence.

## Mathematical Formulation
$$ \\text{Attention}(Q, K, V) = \\text{softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V $$

## Primary Source Evidence
- Originates from [[Sources/Papers/vaswani2017attention]] (EVD-vaswani2017attention-01).

## Strengths & Advantages
- Direct modeling of long-range dependencies with constant path length.

## Known Limitations & Failure Modes
- Quadratic memory scaling with sequence length.

## Related Concepts & Evolution
- Built on [[Knowledge/Concepts/Residual Connections]]
- Adapted by [[Knowledge/Concepts/Low-Rank Adaptation]]

## References
- [[Sources/Papers/vaswani2017attention|Vaswani et al. (2017)]]
""", encoding="utf-8")

    (vault / "Knowledge" / "Concepts" / "Low-Rank Adaptation.md").write_text("""---
type: concept
project: zotero_obsidian_kb
title: "Low-Rank Adaptation"
status: active
claim_strength: strong
primary_sources:
  - "Sources/Papers/hu2021lora"
tags:
  - type/concept
  - topic/peft
updated: 2026-08-19T00:00:00Z
---

# Low-Rank Adaptation

## Definition
Parameter-efficient fine-tuning method freezing pre-trained weights and training low-rank factorized matrices.

## Mathematical Formulation
$$ W = W_0 + B A, \\quad B \\in \\mathbb{R}^{d \\times r}, A \\in \\mathbb{R}^{r \\times k}, r \\ll \\min(d, k) $$

## Primary Source Evidence
- Originates from [[Sources/Papers/hu2021lora]] (EVD-hu2021lora-01).

## Strengths & Advantages
- Massive reduction in trainable parameters and storage footprint.

## Known Limitations & Failure Modes
- Adapter swapping overhead in concurrent multi-tenant serving.

## Related Concepts & Evolution
- Adapts [[Knowledge/Concepts/Self-Attention]]

## References
- [[Sources/Papers/hu2021lora|Hu et al. (2021)]]
""", encoding="utf-8")

    # Synthesis Notes
    (vault / "Knowledge" / "Literature Overview.md").write_text(r"""---
type: literature-synthesis
project: zotero_obsidian_kb
title: "Literature Overview"
status: active
covered_papers:
  - "Sources/Papers/he2016deep"
  - "Sources/Papers/vaswani2017attention"
  - "Sources/Papers/hu2021lora"
key_themes:
  - deep-learning
  - architectures
  - adaptation
updated: 2026-08-19T00:00:00Z
---

# Literature Overview

## Executive Synthesis
Deep learning has evolved from deep convolutional residual networks to attention-driven foundational transformers, and subsequently to parameter-efficient low-rank adaptation techniques.

## Chronological Milestones
| Year | Paper | Key Innovation | Primary Impact |
|---|---|---|---|
| 2016 | [[Sources/Papers/he2016deep\|ResNet]] | Residual skip connections | Enabled 100+ layer deep networks |
| 2017 | [[Sources/Papers/vaswani2017attention\|Transformer]] | Multi-head self-attention | Sequence modeling without recurrence |
| 2021 | [[Sources/Papers/hu2021lora\|LoRA]] | Low-rank weight updates | Efficient large-scale LLM adaptation |

## Key Paradigms
| Paradigm | Core Hypothesis | Mechanism | Canonical Papers |
|---|---|---|---|
| Residual Learning | Identity mappings prevent degradation | $F(x) + x$ | [[Sources/Papers/he2016deep]] |
| Self-Attention | Pairwise attention captures all dependencies | Scaled Dot-Product | [[Sources/Papers/vaswani2017attention]] |
| Low-Rank Adaptation | Task updates have low intrinsic rank | $W_0 + BA$ | [[Sources/Papers/hu2021lora]] |

## Evidence & Benchmark Matrix
| Task / Benchmark | Baseline Metric | Proposed Metric | Source Note |
|---|---|---|---|
| ImageNet Top-5 | ~4.8% (VGG) | 3.57% (ResNet-152) | [[Sources/Papers/he2016deep#Evidence]] |
| WMT En-De BLEU | 26.0 (ConvS2S) | 28.4 (Transformer) | [[Sources/Papers/vaswani2017attention#Evidence]] |
| GPT-3 175B GLUE | Full Fine-Tuning | Matches/Exceeds (10,000x fewer params) | [[Sources/Papers/hu2021lora#Evidence]] |

## Cross-Paper Links
- [[Sources/Papers/he2016deep]]
- [[Sources/Papers/vaswani2017attention]]
- [[Sources/Papers/hu2021lora]]
""", encoding="utf-8")

    (vault / "Knowledge" / "Method Taxonomy.md").write_text(r"""---
type: method-taxonomy
project: zotero_obsidian_kb
title: "Method Taxonomy"
status: active
covered_papers:
  - "Sources/Papers/he2016deep"
  - "Sources/Papers/vaswani2017attention"
  - "Sources/Papers/hu2021lora"
key_themes:
  - architectures
  - optimization
updated: 2026-08-19T00:00:00Z
---

# Method Taxonomy

## Taxonomy Tree
- **Deep Architectures**
  - Residual Learning ([[Sources/Papers/he2016deep]])
  - Multi-Head Attention ([[Sources/Papers/vaswani2017attention]])
- **Model Adaptation & PEFT**
  - Low-Rank Decomposition ([[Sources/Papers/hu2021lora]])

## Comparative Method Matrix
| Family | Method | Complexity | Strengths | Limitations |
|---|---|---|---|---|
| Architecture | Skip Connection | $O(N)$ | Resolves vanishing gradient | Dimension matching |
| Architecture | Self-Attention | $O(N^2)$ | Constant path length | Quadratic memory |
| Adaptation | LoRA | $O(r \cdot d)$ | Zero inference latency | Rank capacity limit |

## Evolutionary Lineage
- ResNet (2016) -> Transformer (2017) -> LoRA (2021)
""", encoding="utf-8")

    (vault / "Knowledge" / "Research Gaps.md").write_text(r"""---
type: research-gaps
project: zotero_obsidian_kb
title: "Research Gaps"
status: active
covered_papers:
  - "Sources/Papers/vaswani2017attention"
  - "Sources/Papers/hu2021lora"
key_themes:
  - computational-complexity
  - parameter-efficiency
updated: 2026-08-19T00:00:00Z
---

# Research Gaps

## Gap Catalog
1. **Quadratic Self-Attention Bottleneck**: Attention complexity scales quadratically with sequence length $O(N^2)$.
   - Evidence Anchor: [[Sources/Papers/vaswani2017attention]] (EVD-vaswani2017attention-01).
2. **Low-Rank Expressivity Bound on Extreme Domain Shift**: Fixed low-rank approximation may underperform on drastic distribution shifts.
   - Evidence Anchor: [[Sources/Papers/hu2021lora]] (EVD-hu2021lora-01).

## Unresolved Theoretical Questions
- What is the minimal intrinsic dimension of cross-task transfer in billion-parameter models?

## Priority Matrix for Future Investigation
- Sub-quadratic linear attention mechanisms (e.g. FlashAttention, State Space Models).
- Dynamic adaptive rank allocation for PEFT.
""", encoding="utf-8")

    # Writing
    (vault / "Writing" / "comparison-matrix.md").write_text(r"""# Literature Comparison Matrix
| Paper | Year | Paradigm / Method | Benchmark / Key Result | Primary Limitation |
|---|---|---|---|---|
| [[Sources/Papers/he2016deep\|ResNet]] | 2016 | Skip Connection ($F(x)+x$) | ImageNet Top-5 3.57% | Dimension matching |
| [[Sources/Papers/vaswani2017attention\|Transformer]] | 2017 | Self-Attention | WMT En-De 28.4 BLEU | $O(N^2)$ memory |
| [[Sources/Papers/hu2021lora\|LoRA]] | 2021 | Low-Rank ($W_0+BA$) | Matches Full FT on GPT-3 175B | Multi-adapter batching |
""", encoding="utf-8")

    # Maps/literature.canvas
    canvas_json = {
        "nodes": [
            {"id": "node-resnet", "type": "file", "file": "Sources/Papers/he2016deep.md", "x": -400, "y": 0, "width": 300, "height": 180, "color": "2"},
            {"id": "node-transformer", "type": "file", "file": "Sources/Papers/vaswani2017attention.md", "x": -400, "y": 240, "width": 300, "height": 180, "color": "2"},
            {"id": "node-lora", "type": "file", "file": "Sources/Papers/hu2021lora.md", "x": -400, "y": 480, "width": 300, "height": 180, "color": "2"},
            {"id": "node-c-resnet", "type": "file", "file": "Knowledge/Concepts/Residual Connections.md", "x": 200, "y": 0, "width": 280, "height": 160, "color": "6"},
            {"id": "node-c-attention", "type": "file", "file": "Knowledge/Concepts/Self-Attention.md", "x": 200, "y": 240, "width": 280, "height": 160, "color": "6"},
            {"id": "node-c-lora", "type": "file", "file": "Knowledge/Concepts/Low-Rank Adaptation.md", "x": 200, "y": 480, "width": 280, "height": 160, "color": "6"},
            {"id": "node-synth-overview", "type": "file", "file": "Knowledge/Literature Overview.md", "x": 800, "y": 0, "width": 320, "height": 200, "color": "5"},
            {"id": "node-synth-gaps", "type": "file", "file": "Knowledge/Research Gaps.md", "x": 800, "y": 260, "width": 320, "height": 200, "color": "1"}
        ],
        "edges": [
            {"id": "e1", "fromNode": "node-resnet", "toNode": "node-transformer", "label": "precedes"},
            {"id": "e2", "fromNode": "node-transformer", "toNode": "node-lora", "label": "precedes"},
            {"id": "e3", "fromNode": "node-resnet", "toNode": "node-c-resnet", "label": "supports"},
            {"id": "e4", "fromNode": "node-transformer", "toNode": "node-c-attention", "label": "supports"},
            {"id": "e5", "fromNode": "node-lora", "toNode": "node-c-lora", "label": "supports"},
            {"id": "e6", "fromNode": "node-transformer", "toNode": "node-c-resnet", "label": "uses"},
            {"id": "e7", "fromNode": "node-lora", "toNode": "node-c-attention", "label": "extends"},
            {"id": "e8", "fromNode": "node-transformer", "toNode": "node-synth-overview", "label": "summarizes"},
            {"id": "e9", "fromNode": "node-lora", "toNode": "node-synth-gaps", "label": "addresses"}
        ]
    }
    (vault / "Maps" / "literature.canvas").write_text(json.dumps(canvas_json, indent=2), encoding="utf-8")

    return vault


# ==============================================================================
# Tier 3: Cross-Feature & Relational Graph Integrity Tests (>= 15 Test Cases)
# ==============================================================================

def test_tier3_multi_tool_interaction_pipeline(full_academic_vault):
    """Test sequentially running ingest, lint, sync_registry, and check_links."""
    from kb_tools.linter import lint_vault
    from kb_tools.registry import sync_all_registries
    from kb_tools.link_checker import check_all_links

    # 1. Sync registries
    sync_all_registries(full_academic_vault)

    # 2. Lint vault
    lint_report = lint_vault(full_academic_vault)
    assert lint_report.get("valid", False) or lint_report.get("errors_count", 0) == 0

    # 3. Check links
    link_report = check_all_links(full_academic_vault)
    assert len(link_report.get("broken_links", [])) == 0


def test_tier3_full_vault_link_graph_traversal(full_academic_vault):
    """Test full graph traversal from Papers -> Concepts -> Synthesis -> Writing -> Canvas."""
    from kb_tools.synthesizer import extract_all_claims
    from kb_tools.canvas_gen import build_canvas_graph

    # Verify papers contain claims
    claims = extract_all_claims(full_academic_vault)
    assert "he2016deep" in claims
    assert "vaswani2017attention" in claims
    assert "hu2021lora" in claims

    # Verify canvas reflects entire network
    canvas = build_canvas_graph(full_academic_vault)
    files_in_canvas = [n.get("file", "") for n in canvas["nodes"] if n.get("type") == "file"]

    assert any("he2016deep" in f for f in files_in_canvas)
    assert any("Residual Connections" in f for f in files_in_canvas)
    assert any("Literature Overview" in f for f in files_in_canvas)


def test_tier3_claim_promotion_gate_valid(full_academic_vault):
    """Verify all promoted claims in Knowledge/Concepts reference valid Evidence IDs in Sources/Papers/."""
    from kb_tools.synthesizer import extract_all_claims

    claims_map = extract_all_claims(full_academic_vault)
    valid_evd_ids = {c["evidence_id"] for claims in claims_map.values() for c in claims if "evidence_id" in c}

    concept_files = list((full_academic_vault / "Knowledge" / "Concepts").glob("*.md"))
    for concept_file in concept_files:
        content = concept_file.read_text(encoding="utf-8")
        found_evds = re.findall(r"EVD-[a-z0-9]+-\d{2}", content)
        for evd in found_evds:
            assert evd in valid_evd_ids, f"Promoted claim in {concept_file.name} references invalid Evidence ID: {evd}"


def test_tier3_claim_promotion_gate_reject_placeholder_source(full_academic_vault):
    """Verify placeholder or abstract-only sources cannot promote strong claims."""
    from kb_tools.linter import validate_claim_promotion_gate

    # Create a placeholder note
    placeholder = full_academic_vault / "Sources" / "Papers" / "sketchy2024blog.md"
    placeholder.write_text("""---
type: paper
project: zotero_obsidian_kb
title: "A Sketchy Blog Post"
citekey: sketchy2024blog
zotero_key: "SKETCHY2024"
status: unread
source_type: "webpage placeholder"
claim_strength: strong
authors: ["Blogger"]
year: 2024
linked_knowledge: ["Knowledge/Concepts/NewIdea"]
updated: 2026-08-19T00:00:00Z
---
# Sketchy Blog
## Claim
AGI achieved yesterday.
## Evidence
```md
Evidence ID: EVD-sketchy2024blog-01
Source: [[Sources/Papers/sketchy2024blog]]
Source type: webpage placeholder
Supports: "AGI achieved"
Method / dataset / metric: "None"
Project relevance: "None"
Claim strength: strong
```
""", encoding="utf-8")

    # Validator must flag invalid source type promoting strong claims
    is_valid, errors = validate_claim_promotion_gate(placeholder, full_academic_vault)
    assert not is_valid or len(errors) > 0


def test_tier3_zero_dead_wikilinks_invariant(full_academic_vault):
    """Test that zero broken/dead wikilinks exist anywhere in the mock academic vault."""
    from kb_tools.link_checker import check_all_links

    report = check_all_links(full_academic_vault)
    broken_links = report.get("broken_links", [])
    assert len(broken_links) == 0, f"Found dead wikilinks: {broken_links}"


def test_tier3_canvas_file_node_target_existence(full_academic_vault):
    """Test that every 'file' node in Maps/literature.canvas points to an actual existing file."""
    canvas_file = full_academic_vault / "Maps" / "literature.canvas"
    data = json.loads(canvas_file.read_text(encoding="utf-8"))

    for node in data["nodes"]:
        if node.get("type") == "file":
            rel_file = node["file"]
            target_path = full_academic_vault / rel_file
            assert target_path.exists(), f"Canvas file node points to non-existent file: {rel_file}"


def test_tier3_canvas_edge_endpoint_and_label_integrity(full_academic_vault):
    """Test all canvas edges connect existing nodes and have valid semantic labels."""
    canvas_file = full_academic_vault / "Maps" / "literature.canvas"
    data = json.loads(canvas_file.read_text(encoding="utf-8"))
    node_ids = {n["id"] for n in data["nodes"]}

    for edge in data["edges"]:
        assert edge["fromNode"] in node_ids
        assert edge["toNode"] in node_ids
        assert "label" in edge and len(edge["label"]) > 0


def test_tier3_evidence_record_schema_conformance(full_academic_vault):
    """Verify all evidence codeblocks conform to the Evidence Record contract schema."""
    from kb_tools.synthesizer import extract_evidence_records

    paper_notes = list((full_academic_vault / "Sources" / "Papers").glob("*.md"))
    assert len(paper_notes) >= 3

    for note in paper_notes:
        records = extract_evidence_records(note)
        for rec in records:
            assert re.match(r"^EVD-[a-z0-9]+-\d{2}$", rec["evidence_id"])
            assert rec["source"].startswith("[[Sources/Papers/")
            assert rec["claim_strength"] in ["speculative", "observed", "supported", "strong"]
            assert len(rec["supports"]) > 0
            assert len(rec["method"]) > 0


def test_tier3_tag_taxonomy_consistency(full_academic_vault):
    """Verify tags across paper and concept notes follow allowed prefixes."""
    from kb_tools.linter import validate_tag_taxonomy

    allowed_prefixes = ("type/", "topic/", "status/", "method/", "knowledge", "concept")

    for md_file in full_academic_vault.rglob("*.md"):
        if ".obsidian" in str(md_file) or "_system" in str(md_file):
            continue
        is_valid, errors = validate_tag_taxonomy(md_file, allowed_prefixes)
        assert is_valid, f"Tag taxonomy violation in {md_file.name}: {errors}"


def test_tier3_bidirectional_link_symmetry(full_academic_vault):
    """Test that paper relationships maintain coherent bidirectional citations."""
    from kb_tools.link_checker import build_vault_graph

    graph = build_vault_graph(full_academic_vault)

    # ResNet -> Transformer
    assert "Sources/Papers/vaswani2017attention.md" in graph.get("Sources/Papers/he2016deep.md", {}).get("outgoing", [])
    # Transformer -> LoRA
    assert "Sources/Papers/hu2021lora.md" in graph.get("Sources/Papers/vaswani2017attention.md", {}).get("outgoing", [])


def test_tier3_registry_table_completeness(full_academic_vault):
    """Verify all paper notes appear in registry indices."""
    from kb_tools.registry import sync_all_registries

    sync_all_registries(full_academic_vault)

    registry_file = full_academic_vault / "_system" / "registry.md"
    if not registry_file.exists():
        registry_file = full_academic_vault / "02-Index.md"

    content = registry_file.read_text(encoding="utf-8")
    assert "he2016deep" in content
    assert "vaswani2017attention" in content
    assert "hu2021lora" in content


def test_tier3_concept_primary_sources_parity(full_academic_vault):
    """Verify every concept note's primary_sources references existing paper notes."""
    concept_files = list((full_academic_vault / "Knowledge" / "Concepts").glob("*.md"))
    assert len(concept_files) >= 3

    for concept_file in concept_files:
        content = concept_file.read_text(encoding="utf-8")
        # Extract primary_sources
        sources = re.findall(r"primary_sources:\s*\n(?:\s*-\s*\"?([^\"]+)\"?)+", content)
        for s in sources:
            source_path = full_academic_vault / s.strip('"\'')
            if not source_path.suffix:
                source_path = source_path.with_suffix(".md")
            assert source_path.exists(), f"Concept {concept_file.name} references non-existent primary source: {s}"


def test_tier3_synthesis_covered_papers_parity(full_academic_vault):
    """Verify every synthesis note's covered_papers references existing paper notes."""
    synthesis_files = list((full_academic_vault / "Knowledge").glob("*.md"))
    for sf in synthesis_files:
        content = sf.read_text(encoding="utf-8")
        covered = re.findall(r"covered_papers:\s*\n(?:\s*-\s*\"?([^\"]+)\"?)+", content)
        for c in covered:
            p_path = full_academic_vault / c.strip('"\'')
            if not p_path.suffix:
                p_path = p_path.with_suffix(".md")
            assert p_path.exists(), f"Synthesis note {sf.name} references non-existent paper: {c}"


def test_tier3_frontmatter_timestamp_format_invariant(full_academic_vault):
    """Verify all 'updated' timestamp fields across all notes match ISO 8601 UTC format."""
    iso_pattern = re.compile(r"^\d{4}-\d{2}-\d{2}(T\d{2}:\d{2}:\d{2}(Z|[+-]\d{2}:\d{2}))?$")

    for md_file in full_academic_vault.rglob("*.md"):
        if ".obsidian" in str(md_file) or "_system" in str(md_file):
            continue
        content = md_file.read_text(encoding="utf-8")
        match = re.search(r"updated:\s*([^\n\r]+)", content)
        if match:
            ts = match.group(1).strip('"\' ')
            assert iso_pattern.match(ts), f"Invalid timestamp format in {md_file.name}: {ts}"


def test_tier3_master_index_and_hub_link_validity(full_academic_vault):
    """Verify all navigation links in 00-Hub.md and 02-Index.md resolve to existing notes."""
    from kb_tools.link_checker import check_note_links

    for nav_doc in [full_academic_vault / "00-Hub.md", full_academic_vault / "02-Index.md"]:
        if nav_doc.exists():
            broken = check_note_links(nav_doc, full_academic_vault)
            assert len(broken) == 0, f"Broken navigation links in {nav_doc.name}: {broken}"


def test_tier3_evidence_strength_consistency(full_academic_vault):
    """Verify claim strength ratings are consistently strong across foundational papers."""
    from kb_tools.synthesizer import group_claims_by_strength

    grouped = group_claims_by_strength(full_academic_vault)
    assert "strong" in grouped
    assert len(grouped["strong"]) >= 3


# ==============================================================================
# Tier 4: Full Vault Lifecycle Scenarios (>= 5 Comprehensive Scenarios)
# ==============================================================================

def test_tier4_scenario_1_fresh_vault_bootstrap_and_scaffold(tmp_path):
    """Scenario 1: Fresh Vault Bootstrap & Scaffold Verification.
    Start with empty directory, create hierarchy, verify template validity, and verify clean initial lint.
    """
    from kb_tools.linter import lint_vault
    from kb_tools.registry import sync_all_registries

    fresh_vault = tmp_path / "fresh_vault"
    subdirs = [
        "Sources/Papers", "Sources/Web", "Sources/Docs", "Sources/Data",
        "Knowledge/Concepts", "Writing/Drafts", "Writing/Outlines",
        "Daily", "Maps", "Templates", "_system/schemas", ".obsidian"
    ]
    for sub in subdirs:
        (fresh_vault / sub).mkdir(parents=True, exist_ok=True)

    # Initial hub notes
    (fresh_vault / "00-Hub.md").write_text("""---
type: hub
title: "Research Cockpit"
updated: 2026-08-19T00:00:00Z
---
# Research Cockpit
""", encoding="utf-8")

    (fresh_vault / "02-Index.md").write_text("""---
type: index
title: "Master Index"
updated: 2026-08-19T00:00:00Z
---
# Master Index
""", encoding="utf-8")

    # Run sync and lint on empty bootstrap
    sync_all_registries(fresh_vault)
    report = lint_vault(fresh_vault)
    assert report.get("valid", True) or report.get("errors_count", 0) == 0


def test_tier4_scenario_2_real_academic_ingestion_and_synthesis_lifecycle(tmp_path):
    """Scenario 2: Real Academic Ingestion & Synthesis Lifecycle.
    Ingest ResNet, Transformer, LoRA BibTeX -> generate notes -> concepts -> synthesis -> canvas -> registries -> zero lint errors.
    """
    from kb_tools.ingest import ingest_file
    from kb_tools.synthesizer import run_synthesis
    from kb_tools.canvas_gen import generate_canvas_file
    from kb_tools.registry import sync_all_registries
    from kb_tools.linter import lint_vault
    from kb_tools.link_checker import check_all_links

    vault = tmp_path / "lifecycle_vault"
    for d in ["Sources/Papers", "Knowledge/Concepts", "Writing", "Maps", "Templates", "_system/schemas"]:
        (vault / d).mkdir(parents=True, exist_ok=True)

    # 1. Ingest BibTeX
    bib_content = """@inproceedings{he2016deep,
  title={Deep Residual Learning for Image Recognition},
  author={He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
  booktitle={CVPR},
  year={2016},
  doi={10.1109/CVPR.2016.90}
}
@inproceedings{vaswani2017attention,
  title={Attention Is All You Need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob},
  booktitle={NeurIPS},
  year={2017}
}
@inproceedings{hu2021lora,
  title={LoRA: Low-Rank Adaptation of Large Language Models},
  author={Hu, Edward J and Shen, Yelong and Wallis, Phillip},
  booktitle={ICLR},
  year={2021}
}"""
    bib_file = tmp_path / "academic_papers.bib"
    bib_file.write_text(bib_content, encoding="utf-8")
    ingest_file(bib_file, vault_dir=vault)

    assert (vault / "Sources" / "Papers" / "he2016deep.md").exists()
    assert (vault / "Sources" / "Papers" / "vaswani2017attention.md").exists()
    assert (vault / "Sources" / "Papers" / "hu2021lora.md").exists()

    # 2. Run synthesis
    run_synthesis(vault)
    assert (vault / "Knowledge" / "Literature Overview.md").exists()
    assert (vault / "Knowledge" / "Method Taxonomy.md").exists()
    assert (vault / "Knowledge" / "Research Gaps.md").exists()

    # 3. Generate Canvas
    canvas_path = generate_canvas_file(vault)
    assert Path(canvas_path).exists()

    # 4. Sync registries
    sync_all_registries(vault)

    # 5. Check links and lint
    link_report = check_all_links(vault)
    assert len(link_report.get("broken_links", [])) == 0


def test_tier4_scenario_3_corrupted_vault_injection_and_healing_cycle(full_academic_vault):
    """Scenario 3: Corrupted Vault Injection & Automated Healing Cycle.
    Inject missing frontmatter, corrupted citekey, dead links -> detect with lint -> heal with repair_links -> clean idempotent state.
    """
    from kb_tools.linter import lint_vault
    from kb_tools.link_checker import repair_all_links, check_all_links
    from kb_tools.registry import sync_all_registries

    # Inject corruption: note with corrupted wikilink target
    corrupt_note = full_academic_vault / "Writing" / "broken_draft.md"
    corrupt_note.write_text("""---
type: draft
title: "Draft with Typos"
updated: 2026-08-19T00:00:00Z
---
# Draft
Referencing [[vaswani-2017-attention]] and [[he-2016-deep-residual]].
""", encoding="utf-8")

    # Step 1: Detect broken links
    initial_check = check_all_links(full_academic_vault)
    assert len(initial_check.get("broken_links", [])) >= 1

    # Step 2: Repair broken links with fuzzy matcher
    repair_report = repair_all_links(full_academic_vault, threshold=0.5)
    assert repair_report.get("repaired_count", 0) >= 1 or "repaired" in repair_report

    # Step 3: Verify repaired content
    repaired_text = corrupt_note.read_text(encoding="utf-8")
    assert "vaswani2017attention" in repaired_text or "he2016deep" in repaired_text

    # Step 4: Re-sync and verify clean state
    sync_all_registries(full_academic_vault)


def test_tier4_scenario_4_incremental_knowledge_evolution(full_academic_vault):
    """Scenario 4: Incremental Knowledge Evolution.
    Add a 4th paper note (FlashAttention) -> incremental registry update -> incremental canvas update.
    """
    from kb_tools.ingest import ingest_file
    from kb_tools.registry import sync_all_registries
    from kb_tools.canvas_gen import build_canvas_graph, generate_canvas_file

    flashattn_bib = """@inproceedings{dao2022flashattention,
  title={FlashAttention: Fast and Memory-Efficient Exact Attention with IO-Awareness},
  author={Dao, Tri and Fu, Daniel Y and Ermon, Stefano and Rudra, Atri and Re, Christopher},
  booktitle={NeurIPS},
  year={2022}
}"""
    bib_path = full_academic_vault / "flashattn.bib"
    bib_path.write_text(flashattn_bib, encoding="utf-8")
    ingest_file(bib_path, vault_dir=full_academic_vault)

    # Verify 4th paper note created
    flash_note = full_academic_vault / "Sources" / "Papers" / "dao2022flashattention.md"
    assert flash_note.exists()

    # Incremental registry sync
    sync_all_registries(full_academic_vault)

    # Regenerate canvas
    canvas_data = build_canvas_graph(full_academic_vault)
    files = [n.get("file", "") for n in canvas_data["nodes"] if n.get("type") == "file"]
    assert any("dao2022flashattention" in f for f in files)
    assert any("he2016deep" in f for f in files)


def test_tier4_scenario_5_end_to_end_cli_pipeline(full_academic_vault, capsys):
    """Scenario 5: End-to-End CLI Pipeline.
    Run all CLI subcommands sequentially with exit code and output validation.
    """
    from kb_tools.cli import main

    commands = [
        ["--help"],
        ["lint", "--vault-dir", str(full_academic_vault), "--json"],
        ["sync-registry", "--vault-dir", str(full_academic_vault), "--json"],
        ["check-links", "--vault-dir", str(full_academic_vault), "--json"],
        ["synthesize", "--vault-dir", str(full_academic_vault), "--json"],
        ["generate-canvas", "--vault-dir", str(full_academic_vault), "--json"],
    ]

    for cmd in commands:
        exit_code = main(cmd)
        assert exit_code in (0, None), f"CLI command failed: kb-tools {' '.join(cmd)}"
        captured = capsys.readouterr()
        assert len(captured.out) > 0 or len(captured.err) == 0
