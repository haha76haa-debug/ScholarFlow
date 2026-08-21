---
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
