---
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
