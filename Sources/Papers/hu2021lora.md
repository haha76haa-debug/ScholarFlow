---
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
Parameterize the weight update $\Delta W \in \mathbb{R}^{d 	imes k}$ as $\Delta W = B \cdot A$, where $B \in \mathbb{R}^{d 	imes r}$, $A \in \mathbb{R}^{r 	imes k}$ with rank $r \ll \min(d, k)$.

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
