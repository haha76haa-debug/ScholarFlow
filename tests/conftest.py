"""
Shared Pytest Fixtures and Helpers for Zotero-Obsidian Academic Knowledge Base Tests.
Provides standard vault scaffolding, populated fixtures, corrupted vault generators,
and markdown / frontmatter parsing utilities.
"""

import copy
import json
import os
import re
import shutil
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
import pytest
import yaml

# Ensure src directory is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# ---------------------------------------------------------------------------
# Sample Note Content Strings (Authoritative Mock Data)
# ---------------------------------------------------------------------------

SAMPLE_PAPER_RESNET = """---
type: paper
project: zotero_obsidian_kb
title: "Deep Residual Learning for Image Recognition"
citekey: he2016deep
zotero_key: "HE2016DEEP"
canvas_visibility: visible
status: read
source_type: "conference paper"
claim_strength: strong
authors:
  - "He, Kaiming"
  - "Zhang, Xiangyu"
  - "Ren, Shaoqing"
  - "Sun, Jian"
year: 2016
venue: "CVPR"
doi: "10.1109/CVPR.2016.90"
url: "https://arxiv.org/abs/1512.03385"
keywords:
  - deep-learning
  - residual-learning
  - computer-vision
concepts:
  - "Residual Connections"
methods:
  - "Residual Learning Framework"
subfield: "Computer Vision"
related_papers: []
linked_knowledge:
  - "[[Knowledge/Concepts/residual_connection]]"
  - "[[Knowledge/Literature Overview]]"
argument_claims:
  - "Residual connections alleviate the degradation problem in very deep networks."
argument_methods:
  - "Identity shortcut mapping: F(x) + x"
argument_gaps:
  - "Theoretical understanding of feature representation across residual layers remains incomplete."
paper_relationships:
  - "Sources/Papers/vaswani2017attention::precedes"
tags:
  - "#type/paper-note"
  - "#topic/deep-learning"
  - "#status/read"
  - "#method/residual-learning"
updated: 2026-08-19T00:00:00Z
---

# Deep Residual Learning for Image Recognition

## Claim
Deep residual networks make it possible to train substantially deeper neural networks (up to 152 layers) by reformulating layers as learning residual functions with reference to layer inputs.

## Research question
How can we overcome the degradation problem where deeper neural networks exhibit higher training and test error without vanishing/exploding gradients?

## Method
Introduce identity shortcut connections that perform parameter-free identity mapping $F(x) + x$, allowing gradients to flow directly through the skip paths during backpropagation.

## Evidence
```md
Evidence ID: EVD-he2016deep-01
Source: [[Sources/Papers/he2016deep]]
Source type: conference paper
Supports: "Residual networks reduce top-5 error on ImageNet to 3.57% with 152 layers"
Contradicts: ""
Method / dataset / metric: ImageNet classification benchmark, top-5 error rate 3.57%
Limitation: Does not resolve memory footprint scaling linearly with layer count
Project relevance: Foundational mechanism for deep architectural backbones
Claim strength: strong
```

## Strengths
- **Theoretical**: Directly resolves optimization degradation without adding parameters.
- **Empirical**: Won 1st place in ILSVRC 2015 with 3.57% top-5 error.
- **Methodological**: Modular residual building block easily stackable.

## Limitation
- **Boundary Condition**: Extremely deep residual networks require careful batch normalization placement.
- **Computational Cost**: Memory consumption scales with network depth during training.
- **Unaddressed Edge Case**: Behavior under extreme width vs depth tradeoffs not fully explored.

## Direct relevance to repo
- Establishes the foundational concept note [[Knowledge/Concepts/residual_connection]].

## Relation to other papers
- Precedes [[Sources/Papers/vaswani2017attention]] which uses residual connections around multi-head attention.

## Knowledge links
- [[Knowledge/Concepts/residual_connection]]
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]

## Key Annotations & Highlights
> [!quote]+ Core Hypothesis (p. 2)
> Instead of hoping each few stacked layers directly fit a desired underlying mapping, we explicitly let these layers fit a residual mapping.
>
> [Zotero Link](zotero://open-pdf/0_he2016/2)
"""

SAMPLE_PAPER_TRANSFORMER = """---
type: paper
project: zotero_obsidian_kb
title: "Attention Is All You Need"
citekey: vaswani2017attention
zotero_key: "VASWANI2017"
canvas_visibility: visible
status: read
source_type: "conference paper"
claim_strength: strong
authors:
  - "Vaswani, Ashish"
  - "Shazeer, Noam"
  - "Parmar, Niki"
  - "Uszkoreit, Jakob"
  - "Jones, Llion"
  - "Gomez, Aidan N."
  - "Kaiser, Lukasz"
  - "Polosukhin, Illia"
year: 2017
venue: "NeurIPS"
doi: "10.5555/3295222.3295349"
url: "https://arxiv.org/abs/1706.03762"
keywords:
  - transformer
  - attention-mechanism
  - nlp
concepts:
  - "Self-Attention Mechanism"
  - "Residual Connections"
methods:
  - "Scaled Dot-Product Attention"
  - "Multi-Head Attention"
subfield: "Natural Language Processing"
related_papers:
  - "Sources/Papers/he2016deep"
linked_knowledge:
  - "[[Knowledge/Concepts/self_attention]]"
  - "[[Knowledge/Concepts/residual_connection]]"
  - "[[Knowledge/Literature Overview]]"
argument_claims:
  - "Recurrent and convolutional operations can be entirely replaced with attention mechanisms."
argument_methods:
  - "Scaled dot-product multi-head attention with positional encodings."
argument_gaps:
  - "Quadratic compute and memory complexity O(N^2) relative to sequence length."
paper_relationships:
  - "Sources/Papers/he2016deep::extends"
  - "Sources/Papers/hu2021lora::precedes"
tags:
  - "#type/paper-note"
  - "#topic/deep-learning"
  - "#status/read"
  - "#method/attention"
updated: 2026-08-19T00:00:00Z
---

# Attention Is All You Need

## Claim
The Transformer sequence-to-sequence architecture dispenses entirely with recurrence and convolutions, relying solely on multi-head self-attention mechanisms.

## Research question
Can sequence transduction models achieve state-of-the-art translation quality with significantly higher parallelizability and reduced training time?

## Method
Multi-head scaled dot-product attention combined with sinusoidal positional encodings, layer normalization, and residual connections.

## Evidence
```md
Evidence ID: EVD-vaswani2017attention-01
Source: [[Sources/Papers/vaswani2017attention]]
Source type: conference paper
Supports: "Achieves 28.4 BLEU on WMT 2014 English-to-German, establishing new state-of-the-art"
Contradicts: ""
Method / dataset / metric: WMT 2014 EN-DE and EN-FR translation benchmarks, BLEU score
Limitation: O(N^2) memory footprint for long sequences
Project relevance: Core architecture of modern foundation models
Claim strength: strong
```

## Strengths
- **Theoretical**: Constant number of sequential operations O(1) for path lengths between symbols.
- **Empirical**: 28.4 BLEU score with 3.5 days of training on 8 P100 GPUs.
- **Methodological**: Multi-head mechanism allows attending to information at different representation subspaces.

## Limitation
- **Boundary Condition**: Quadratic computational and memory complexity with respect to context window length.
- **Computational Cost**: Heavy key-value memory overhead during auto-regressive generation.
- **Unaddressed Edge Case**: Lack of inherent inductive bias for local temporal or spatial proximity.

## Direct relevance to repo
- Seeds [[Knowledge/Concepts/self_attention]] and links to [[Knowledge/Concepts/residual_connection]].

## Relation to other papers
- Extends [[Sources/Papers/he2016deep]] by embedding residual connections around sub-layers.
- Precedes [[Sources/Papers/hu2021lora]] parameter-efficient fine-tuning for transformers.

## Knowledge links
- [[Knowledge/Concepts/self_attention]]
- [[Knowledge/Concepts/residual_connection]]
- [[Knowledge/Literature Overview]]

## Key Annotations & Highlights
> [!quote]+ Architecture Proposal (p. 3)
> The Transformer is the first transduction model relying entirely on self-attention to compute representations of its input and output without using sequence-aligned RNNs or convolution.
>
> [Zotero Link](zotero://open-pdf/0_vaswani2017/3)
"""

SAMPLE_PAPER_LORA = """---
type: paper
project: zotero_obsidian_kb
title: "LoRA: Low-Rank Adaptation of Large Language Models"
citekey: hu2021lora
zotero_key: "HU2021LORA"
canvas_visibility: visible
status: read
source_type: "conference paper"
claim_strength: strong
authors:
  - "Hu, Edward J."
  - "Shen, Yelong"
  - "Wallis, Phillip"
  - "Zeyuan, Allen-Zhu"
  - "Li, Yuanzhi"
  - "Wang, Shean"
  - "Wang, Lu"
  - "Chen, Weizhu"
year: 2021
venue: "ICLR"
doi: "10.48550/arXiv.2106.09685"
url: "https://arxiv.org/abs/2106.09685"
keywords:
  - parameter-efficient-fine-tuning
  - peft
  - lora
  - llm
concepts:
  - "Parameter-Efficient Fine-Tuning"
  - "Low-Rank Adaptation"
methods:
  - "Low-Rank Matrix Decomposition"
subfield: "Natural Language Processing"
related_papers:
  - "Sources/Papers/vaswani2017attention"
linked_knowledge:
  - "[[Knowledge/Concepts/peft]]"
  - "[[Knowledge/Literature Overview]]"
argument_claims:
  - "Weight updates during adaptation have a low intrinsic dimension."
argument_methods:
  - "Decomposing weight delta into product of low-rank matrices W = W_0 + B * A."
argument_gaps:
  - "Determining the optimal target rank r across diverse downstream tasks remains heuristic."
paper_relationships:
  - "Sources/Papers/vaswani2017attention::extends"
tags:
  - "#type/paper-note"
  - "#topic/deep-learning"
  - "#status/read"
  - "#method/peft"
updated: 2026-08-19T00:00:00Z
---

# LoRA: Low-Rank Adaptation of Large Language Models

## Claim
Freezing the pretrained model weights and injecting trainable rank decomposition matrices into each Transformer layer reduces trainable parameters by 10,000x without inference latency.

## Research question
How can we adapt multi-billion parameter foundation models to specific downstream tasks without fine-tuning all model parameters or introducing inference latency?

## Method
Parameterize the weight update $\Delta W \in \mathbb{R}^{d \times k}$ as $\Delta W = B \cdot A$, where $B \in \mathbb{R}^{d \times r}$, $A \in \mathbb{R}^{r \times k}$ with rank $r \ll \min(d, k)$.

## Evidence
```md
Evidence ID: EVD-hu2021lora-01
Source: [[Sources/Papers/hu2021lora]]
Source type: conference paper
Supports: "Matches or exceeds full fine-tuning performance on GPT-3 175B with 10,000x fewer trainable parameters"
Contradicts: ""
Method / dataset / metric: GLUE benchmark, WikiSQL, SAMSum; accuracy and ROUGE scores
Limitation: Rank hyperparameter r must be empirically tuned
Project relevance: Primary fine-tuning method for efficient LLM customization
Claim strength: strong
```

## Strengths
- **Theoretical**: Exploits low intrinsic dimensionality of model adaptation manifolds.
- **Empirical**: Reduces GPU memory consumption by 3x and trainable parameters by 10,000x on GPT-3 175B.
- **Methodological**: Zero additional inference latency by merging $W = W_0 + BA$ during deployment.

## Limitation
- **Boundary Condition**: Merging multiple concurrent LoRA adapters for batched inference with heterogeneous tasks is non-trivial.
- **Computational Cost**: Slower training throughput than full fine-tuning per backward pass due to extra matrix multiplications.
- **Unaddressed Edge Case**: Low-rank assumption may fail when adapting to radically out-of-distribution domains.

## Direct relevance to repo
- Forms [[Knowledge/Concepts/peft]] concept and updates [[Knowledge/Literature Overview]].

## Relation to other papers
- Extends [[Sources/Papers/vaswani2017attention]] Transformer layers with efficient low-rank adaptation.

## Knowledge links
- [[Knowledge/Concepts/peft]]
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]

## Key Annotations & Highlights
> [!quote]+ Low-Rank Formulation (p. 2)
> We hypothesize that the change in weights during model adaptation also has a low intrinsic rank/dimension.
>
> [Zotero Link](zotero://open-pdf/0_hu2021/2)
"""

SAMPLE_CONCEPT_RESIDUAL = """---
type: concept
project: zotero_obsidian_kb
title: "Residual Connections"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/he2016deep]]"
related_concepts:
  - "[[Knowledge/Concepts/self_attention]]"
linked_syntheses:
  - "[[Knowledge/Method Taxonomy]]"
  - "[[Knowledge/Literature Overview]]"
tags:
  - "#type/concept"
  - "#topic/deep-learning"
  - "#method/residual-learning"
updated: 2026-08-19T00:00:00Z
---

# Residual Connections

## Definition
A structural architectural motif in neural networks where the input to a set of layers is added directly to their output via an identity mapping shortcut, enabling smooth gradient propagation during deep backpropagation.

## Mathematical Formulation
$$ y = \mathcal{F}(x, \{W_i\}) + x $$
where $x$ and $y$ are input and output vectors, and $\mathcal{F}$ represents the residual mapping to be learned.

## Primary Source Evidence
- Originates from [[Sources/Papers/he2016deep]] (Section 3.1).
- **Empirical Validation**: Solved the vanishing gradient problem on networks exceeding 1000 layers.

## Strengths & Advantages
- **Optimization**: Creates unimodal loss landscapes with unbroken gradient highways.
- **Modularity**: Integrates seamlessly with convolutional, recurrent, and transformer sub-layers.
- **Zero Overhead**: Standard identity shortcuts require zero extra parameters or FLOPs.

## Known Limitations & Failure Modes
- **Representation Redundancy**: Some residual layers perform marginal representation refinement.
- **Signal Explosion**: Unnormalized residual pathways without LayerNorm/BatchNorm can lead to signal amplification.

## Related Concepts & Evolution
- Preceded by Highway Networks.
- Adopted by [[Knowledge/Concepts/self_attention]] in Transformers ([[Sources/Papers/vaswani2017attention]]).

## References
- [[Sources/Papers/he2016deep|He et al. (2016) Deep Residual Learning for Image Recognition]]
"""

SAMPLE_CONCEPT_ATTENTION = """---
type: concept
project: zotero_obsidian_kb
title: "Self-Attention Mechanism"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/vaswani2017attention]]"
related_concepts:
  - "[[Knowledge/Concepts/residual_connection]]"
linked_syntheses:
  - "[[Knowledge/Method Taxonomy]]"
  - "[[Knowledge/Literature Overview]]"
tags:
  - "#type/concept"
  - "#topic/deep-learning"
  - "#method/attention"
updated: 2026-08-19T00:00:00Z
---

# Self-Attention Mechanism

## Definition
An attention mechanism relating different positions of a single sequence in order to compute a contextualized representation of the sequence.

## Mathematical Formulation
$$ \text{Attention}(Q, K, V) = \text{softmax}\left(\frac{QK^T}{\sqrt{d_k}}\right)V $$

## Primary Source Evidence
- Detailed in [[Sources/Papers/vaswani2017attention]] (Section 3.2).
- **Empirical Validation**: State-of-the-art machine translation with superior training efficiency.

## Strengths & Advantages
- **Global Context**: Dynamic all-to-all token interaction in $O(1)$ path length.
- **Parallelization**: Eliminates sequential recurrence bottlenecks.

## Known Limitations & Failure Modes
- **Quadratic Complexity**: Computes $O(N^2)$ dot-products for sequence length $N$.
- **KV Cache Memory**: Inference requires retaining activation memory buffers.

## Related Concepts & Evolution
- Built on Bahdanau additive attention.
- Enhanced by [[Knowledge/Concepts/residual_connection]] around sub-blocks.

## References
- [[Sources/Papers/vaswani2017attention|Vaswani et al. (2017) Attention Is All You Need]]
"""

SAMPLE_CONCEPT_PEFT = """---
type: concept
project: zotero_obsidian_kb
title: "Parameter-Efficient Fine-Tuning"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/hu2021lora]]"
related_concepts:
  - "[[Knowledge/Concepts/self_attention]]"
linked_syntheses:
  - "[[Knowledge/Method Taxonomy]]"
  - "[[Knowledge/Literature Overview]]"
tags:
  - "#type/concept"
  - "#topic/deep-learning"
  - "#method/peft"
updated: 2026-08-19T00:00:00Z
---

# Parameter-Efficient Fine-Tuning

## Definition
A family of adaptation techniques for large foundation models that freeze the majority of pretrained weights and only update or introduce a small subset of parameters.

## Mathematical Formulation
$$ W = W_0 + \Delta W = W_0 + \frac{\alpha}{r} (B \cdot A) $$

## Primary Source Evidence
- Pioneered in low-rank form by [[Sources/Papers/hu2021lora]].
- **Empirical Validation**: Matches full fine-tuning on 175B parameter models with 0.01% trainable parameters.

## Strengths & Advantages
- **Storage Efficiency**: Small adapter checkpoints (< 100MB vs tens of GBs).
- **Inference Invariance**: Zero deployment latency after weight folding.

## Known Limitations & Failure Modes
- **Capacity Limits**: May struggle on extreme domain shift tasks compared to full fine-tuning.

## Related Concepts & Evolution
- Complements Prompt Tuning, Prefix Tuning, and Adapter Modules.

## References
- [[Sources/Papers/hu2021lora|Hu et al. (2021) LoRA: Low-Rank Adaptation of Large Language Models]]
"""

SAMPLE_SYNTHESIS_OVERVIEW = """---
type: literature-synthesis
project: zotero_obsidian_kb
title: "Literature Overview"
status: active
covered_papers:
  - "[[Sources/Papers/he2016deep]]"
  - "[[Sources/Papers/vaswani2017attention]]"
  - "[[Sources/Papers/hu2021lora]]"
key_themes:
  - deep-learning
  - attention-mechanisms
  - peft
updated: 2026-08-19T00:00:00Z
---

# Literature Overview

## Executive Synthesis
Over the past decade, deep learning paradigms have evolved from deep residual convolutional networks (ResNet, 2016) to fully attention-based foundation architectures (Transformer, 2017), culminating in modular parameter-efficient adaptation strategies (LoRA, 2021).

## Chronological Milestones
| Year | Paper | Key Innovation | Primary Impact |
|---|---|---|---|
| 2016 | [[Sources/Papers/he2016deep\|ResNet]] | Residual shortcut connections | Enabled training 100+ layer networks |
| 2017 | [[Sources/Papers/vaswani2017attention\|Transformer]] | Multi-head self-attention | Replaced recurrence; unified NLP |
| 2021 | [[Sources/Papers/hu2021lora\|LoRA]] | Low-rank weight matrix adaptation | Enabled efficient fine-tuning of 100B+ LLMs |

## Key Paradigms
| Paradigm | Core Hypothesis | Mechanism | Key Limitations | Canonical Papers |
|---|---|---|---|---|
| Residual Learning | Layers should learn residual functions | $F(x) + x$ shortcuts | High memory footprint | [[Sources/Papers/he2016deep]] |
| Self-Attention | Token interactions replace recurrence | Scaled dot-product | $O(N^2)$ context cost | [[Sources/Papers/vaswani2017attention]] |
| Low-Rank Adaptation | Task adaptation has low intrinsic rank | $W_0 + BA$ decomposition | Tuning rank $r$ heuristic | [[Sources/Papers/hu2021lora]] |

## Evidence & Benchmark Matrix
| Task / Benchmark | Baseline Metric | Proposed Metric | Delta ($\Delta$) | Source Note |
|---|---|---|---|---|
| ImageNet Top-5 Error | 4.49% (VGG-16) | 3.57% (ResNet-152) | -0.92% (p < 0.001) | [[Sources/Papers/he2016deep#Evidence]] |
| WMT 2014 EN-DE BLEU | 26.0 (ConvS2S) | 28.4 (Transformer Big) | +2.4 BLEU | [[Sources/Papers/vaswani2017attention#Evidence]] |
| GPT-3 175B WikiSQL Acc | 73.8% (FT) | 74.0% (LoRA) | +0.2% | [[Sources/Papers/hu2021lora#Evidence]] |

## Cross-Paper Links
- [[Sources/Papers/he2016deep]]
- [[Sources/Papers/vaswani2017attention]]
- [[Sources/Papers/hu2021lora]]
"""

SAMPLE_BIBTEX_CONTENT = """@inproceedings{he2016deep,
  title={Deep residual learning for image recognition},
  author={He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
  booktitle={Proceedings of the IEEE conference on computer vision and pattern recognition},
  pages={770--778},
  year={2016},
  doi={10.1109/CVPR.2016.90}
}

@inproceedings{vaswani2017attention,
  title={Attention is all you need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and Kaiser, Lukasz and Polosukhin, Illia},
  booktitle={Advances in neural information processing systems},
  volume={30},
  pages={5998--6008},
  year={2017}
}

@inproceedings{hu2021lora,
  title={LoRA: Low-Rank Adaptation of Large Language Models},
  author={Hu, Edward J and Shen, Yelong and Wallis, Phillip and Allen-Zhu, Zeyuan and Li, Yuanzhi and Wang, Shean and Wang, Lu and Chen, Weizhu},
  booktitle={International Conference on Learning Representations},
  year={2022},
  url={https://openreview.net/forum?id=nZeVKeeFYf9}
}
"""

SAMPLE_CSL_JSON_CONTENT = """[
  {
    "id": "he2016deep",
    "type": "paper-conference",
    "title": "Deep residual learning for image recognition",
    "author": [
      {"family": "He", "given": "Kaiming"},
      {"family": "Zhang", "given": "Xiangyu"},
      {"family": "Ren", "given": "Shaoqing"},
      {"family": "Sun", "given": "Jian"}
    ],
    "issued": {"date-parts": [[2016]]},
    "container-title": "IEEE Conference on Computer Vision and Pattern Recognition",
    "DOI": "10.1109/CVPR.2016.90"
  },
  {
    "id": "vaswani2017attention",
    "type": "paper-conference",
    "title": "Attention is all you need",
    "author": [
      {"family": "Vaswani", "given": "Ashish"},
      {"family": "Shazeer", "given": "Noam"}
    ],
    "issued": {"date-parts": [[2017]]},
    "container-title": "NeurIPS"
  }
]"""


# ---------------------------------------------------------------------------
# Helper / Parser Utilities
# ---------------------------------------------------------------------------

def parse_frontmatter(content_or_path: Union[str, Path]) -> Tuple[Dict[str, Any], str]:
    """
    Parses YAML frontmatter and body from markdown text or file path.
    Returns (frontmatter_dict, markdown_body).
    """
    if isinstance(content_or_path, Path):
        text = content_or_path.read_text(encoding="utf-8")
    else:
        text = str(content_or_path)

    if not text.startswith("---"):
        return {}, text

    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text

    fm_raw = parts[1]
    body = parts[2].lstrip("\r\n")

    try:
        data = yaml.safe_load(fm_raw)
        return (data if isinstance(data, dict) else {}), body
    except Exception:
        return {}, body


def extract_wikilinks(content: str) -> List[Dict[str, str]]:
    """
    Extracts all [[...]] wikilinks from a string.
    Returns a list of dicts with keys: 'raw', 'target', 'alias', 'anchor'.
    """
    results = []
    pattern = r"\[\[(.*?)\]\]"
    for match in re.finditer(pattern, content):
        raw = match.group(1)
        # Parse alias: target|alias
        if "|" in raw:
            target_part, alias = raw.split("|", 1)
        else:
            target_part, alias = raw, ""

        # Parse anchor: target#anchor
        if "#" in target_part:
            target, anchor = target_part.split("#", 1)
        else:
            target, anchor = target_part, ""

        results.append({
            "raw": match.group(0),
            "target": target.strip(),
            "alias": alias.strip(),
            "anchor": anchor.strip(),
            "full_target": target_part.strip(),
        })
    return results


def extract_markdown_headings(content: str) -> List[Dict[str, Any]]:
    """
    Extracts all markdown headings (# Heading, ## Heading, etc.).
    Returns list of dicts: {'level': int, 'text': str, 'raw': str}.
    """
    headings = []
    for line in content.splitlines():
        match = re.match(r"^(#{1,6})\s+(.+)$", line.strip())
        if match:
            level = len(match.group(1))
            text = match.group(2).strip()
            headings.append({
                "level": level,
                "text": text,
                "raw": line.strip()
            })
    return headings


def validate_markdown_heading_structure(content: str, required_headings: List[str]) -> bool:
    """
    Validates whether all required headings exist in the content in the required order.
    """
    extracted = [h["text"] for h in extract_markdown_headings(content)]
    last_idx = -1
    for req in required_headings:
        # Strip leading # if provided
        clean_req = re.sub(r"^#+\s*", "", req).strip()
        try:
            found_idx = next(i for i, h in enumerate(extracted) if clean_req.lower() in h.lower() and i > last_idx)
            last_idx = found_idx
        except StopIteration:
            return False
    return True


# ---------------------------------------------------------------------------
# Pytest Fixtures
# ---------------------------------------------------------------------------

@pytest.fixture
def sample_paper_note_content():
    """Returns authoritative ResNet sample paper note content."""
    return SAMPLE_PAPER_RESNET


@pytest.fixture
def sample_transformer_paper_content():
    """Returns authoritative Transformer sample paper note content."""
    return SAMPLE_PAPER_TRANSFORMER


@pytest.fixture
def sample_lora_paper_content():
    """Returns authoritative LoRA sample paper note content."""
    return SAMPLE_PAPER_LORA


@pytest.fixture
def sample_concept_note_content():
    """Returns authoritative Residual Connection sample concept note content."""
    return SAMPLE_CONCEPT_RESIDUAL


@pytest.fixture
def sample_self_attention_concept_content():
    """Returns authoritative Self-Attention sample concept note content."""
    return SAMPLE_CONCEPT_ATTENTION


@pytest.fixture
def sample_peft_concept_content():
    """Returns authoritative PEFT sample concept note content."""
    return SAMPLE_CONCEPT_PEFT


@pytest.fixture
def sample_synthesis_note_content():
    """Returns authoritative Literature Overview synthesis note content."""
    return SAMPLE_SYNTHESIS_OVERVIEW


@pytest.fixture
def sample_bibtex_str():
    """Returns authoritative sample BibTeX string."""
    return SAMPLE_BIBTEX_CONTENT


@pytest.fixture
def sample_csl_json_str():
    """Returns authoritative sample CSL-JSON string."""
    return SAMPLE_CSL_JSON_CONTENT


@pytest.fixture
def tmp_vault(tmp_path):
    """
    Generates a clean temporary Obsidian vault directory structure conforming to R1:
    - Sources/Papers, Sources/Web, Sources/Docs
    - Knowledge/Concepts, Knowledge/
    - Writing, Daily, Maps, Templates, _system/schemas, .obsidian
    Populates schema contracts and core templates.
    """
    vault = tmp_path / "test_vault"
    vault.mkdir(parents=True, exist_ok=True)

    # Required directories
    dirs = [
        "Sources/Papers",
        "Sources/Web",
        "Sources/Docs",
        "Knowledge/Concepts",
        "Writing",
        "Daily",
        "Maps",
        "Templates",
        "_system/schemas",
        ".obsidian",
    ]
    for d in dirs:
        (vault / d).mkdir(parents=True, exist_ok=True)

    # Copy or create schema files
    real_schemas = PROJECT_ROOT / "_system" / "schemas"
    if real_schemas.exists():
        for schema_file in real_schemas.glob("*.yaml"):
            shutil.copy(schema_file, vault / "_system" / "schemas" / schema_file.name)
    else:
        # Fallback dummy schemas if running before M1
        (vault / "_system" / "schemas" / "paper_schema.yaml").write_text("schema_name: paper_schema\n", encoding="utf-8")
        (vault / "_system" / "schemas" / "concept_schema.yaml").write_text("schema_name: concept_schema\n", encoding="utf-8")
        (vault / "_system" / "schemas" / "synthesis_schema.yaml").write_text("schema_name: synthesis_schema\n", encoding="utf-8")

    # Copy or create templates
    real_templates = PROJECT_ROOT / "Templates"
    if real_templates.exists():
        for tpl in real_templates.glob("*.md"):
            shutil.copy(tpl, vault / "Templates" / tpl.name)

    # Copy or create .obsidian configurations
    real_obsidian = PROJECT_ROOT / ".obsidian"
    if real_obsidian.exists():
        for conf in real_obsidian.glob("*.json"):
            shutil.copy(conf, vault / ".obsidian" / conf.name)
    else:
        (vault / ".obsidian" / "types.json").write_text('{"types": {}}', encoding="utf-8")

    # Initialize root index and hub files
    (vault / "00-Hub.md").write_text("# Knowledge Base Hub\n", encoding="utf-8")
    (vault / "01-Plan.md").write_text("# Active Research Plan\n", encoding="utf-8")
    (vault / "02-Index.md").write_text("# Vault Navigation Index\n\n## 1. Knowledge Namespace\n\n## 2. Sources Namespace\n", encoding="utf-8")
    (vault / "_system" / "registry.md").write_text("# Project Registry\n\n## Sources\n\n## Concepts\n\n## Syntheses\n", encoding="utf-8")

    return vault


@pytest.fixture
def populated_vault(tmp_vault):
    """
    Returns a tmp_vault populated with the 3 real canonical papers (ResNet, Transformer, LoRA),
    3 atomic concept notes, and 1 literature synthesis note.
    """
    papers_dir = tmp_vault / "Sources" / "Papers"
    concepts_dir = tmp_vault / "Knowledge" / "Concepts"
    knowledge_dir = tmp_vault / "Knowledge"

    # Papers
    (papers_dir / "he2016deep.md").write_text(SAMPLE_PAPER_RESNET, encoding="utf-8")
    (papers_dir / "vaswani2017attention.md").write_text(SAMPLE_PAPER_TRANSFORMER, encoding="utf-8")
    (papers_dir / "hu2021lora.md").write_text(SAMPLE_PAPER_LORA, encoding="utf-8")

    # Concepts
    (concepts_dir / "residual_connection.md").write_text(SAMPLE_CONCEPT_RESIDUAL, encoding="utf-8")
    (concepts_dir / "self_attention.md").write_text(SAMPLE_CONCEPT_ATTENTION, encoding="utf-8")
    (concepts_dir / "peft.md").write_text(SAMPLE_CONCEPT_PEFT, encoding="utf-8")

    # Synthesis
    (knowledge_dir / "Literature Overview.md").write_text(SAMPLE_SYNTHESIS_OVERVIEW, encoding="utf-8")

    return tmp_vault


@pytest.fixture
def corrupted_vault_factory(tmp_vault):
    """
    Factory fixture to generate corrupted vault variants for testing fault tolerance,
    schema validation, linter diagnostics, and link repair.
    """
    def _create_corrupted_vault(corruption_type: str, **kwargs) -> Path:
        vault = Path(tmp_vault)
        papers_dir = vault / "Sources" / "Papers"
        concepts_dir = vault / "Knowledge" / "Concepts"
        knowledge_dir = vault / "Knowledge"

        if corruption_type == "broken_links":
            # Populate valid base then add notes with non-existent links
            (papers_dir / "he2016deep.md").write_text(SAMPLE_PAPER_RESNET, encoding="utf-8")
            (concepts_dir / "broken_concept.md").write_text("""---
type: concept
project: zotero_obsidian_kb
title: "Broken Concept Note"
status: active
claim_strength: speculative
primary_sources:
  - "[[Sources/Papers/nonexistent_paper_2099]]"
tags:
  - "#type/concept"
updated: 2026-08-19T00:00:00Z
---
# Broken Concept
Refers to [[NonExistentConceptNote]] and [[Sources/Papers/ghost_paper#Evidence]].
""", encoding="utf-8")

        elif corruption_type == "missing_frontmatter_keys":
            # Paper note missing required fields: citekey, authors, year, claim_strength
            (papers_dir / "bad_paper.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Paper Missing Keys"
status: to-read
updated: 2026-08-19T00:00:00Z
---
# Bad Paper
## Claim
No evidence or citekey.
""", encoding="utf-8")

        elif corruption_type == "invalid_types":
            # Year is string, authors is single string instead of list, linked_knowledge is int
            (papers_dir / "type_mismatch.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Type Mismatch Paper"
citekey: typemismatch2026
zotero_key: "TYPE2026"
status: to-read
source_type: "full paper"
claim_strength: strong
authors: "Single Author As String Instead Of List"
year: "twenty-sixteen"
linked_knowledge: 12345
updated: 2026-08-19T00:00:00Z
---
# Type Mismatch Paper
""", encoding="utf-8")

        elif corruption_type == "invalid_enums":
            # Invalid claim_strength, invalid status, invalid type
            (papers_dir / "enum_mismatch.md").write_text("""---
type: blog-post
project: zotero_obsidian_kb
title: "Enum Mismatch Paper"
citekey: enum2026
zotero_key: "ENUM2026"
status: finished_reading
source_type: "online forum"
claim_strength: unsupported_unknown_enum
authors:
  - "Test Author"
year: 2026
linked_knowledge:
  - "[[Knowledge/Literature Overview]]"
updated: 2026-08-19T00:00:00Z
---
# Enum Mismatch Paper
""", encoding="utf-8")

        elif corruption_type == "missing_headings":
            # Paper note missing required sections (e.g. ## Method, ## Evidence)
            (papers_dir / "missing_headings.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Missing Headings Paper"
citekey: missing2026
zotero_key: "MISSING2026"
status: read
source_type: "preprint"
claim_strength: observed
authors:
  - "Incomplete Author"
year: 2026
linked_knowledge:
  - "[[Knowledge/Literature Overview]]"
tags:
  - "#type/paper-note"
updated: 2026-08-19T00:00:00Z
---
# Missing Headings Paper

## Claim
Only has claim heading and nothing else.
""", encoding="utf-8")

        elif corruption_type == "duplicate_citekeys":
            # Two different files claiming the same citekey
            (papers_dir / "paper_alpha.md").write_text(SAMPLE_PAPER_RESNET, encoding="utf-8")
            dup_content = SAMPLE_PAPER_RESNET.replace('title: "Deep Residual Learning for Image Recognition"', 'title: "Duplicate ResNet Title"')
            (papers_dir / "paper_beta.md").write_text(dup_content, encoding="utf-8")

        elif corruption_type == "invalid_tags":
            (papers_dir / "bad_tags.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Bad Tags Paper"
citekey: badtags2026
zotero_key: "TAGS2026"
status: read
source_type: "preprint"
claim_strength: observed
authors:
  - "Author One"
year: 2026
linked_knowledge:
  - "[[Knowledge/Literature Overview]]"
tags:
  - "not_a_valid_tag_format"
  - "##doublesharp"
updated: 2026-08-19T00:00:00Z
---
# Bad Tags Paper
## Claim
Content.
## Research question
Question.
## Method
Method.
## Evidence
```md
Evidence ID: EVD-badtags2026-01
Source: [[Sources/Papers/badtags2026]]
Source type: preprint
Supports: "Test"
Method / dataset / metric: "Test"
Project relevance: "Test"
Claim strength: observed
```
## Strengths
- Good
## Limitation
- Bad
## Direct relevance to repo
- Relevance
## Relation to other papers
- Relation
## Knowledge links
- [[Knowledge/Literature Overview]]
""", encoding="utf-8")

        return vault

    return _create_corrupted_vault
