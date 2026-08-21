---
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
$$ W = W_0 + \Delta W = W_0 + rac{lpha}{r} (B \cdot A) $$

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
