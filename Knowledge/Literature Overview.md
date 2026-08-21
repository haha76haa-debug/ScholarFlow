---
type: literature-synthesis
project: zotero_obsidian_kb
title: 'Literature Overview: Foundational Architectures & Efficient Adaptation'
status: active
covered_papers:
- '[[Sources/Papers/he2016deep]]'
- '[[Sources/Papers/hu2021lora]]'
- '[[Sources/Papers/vaswani2017attention]]'
key_themes:
- deep-learning
- residual-learning
- attention-mechanisms
- peft
updated: '2026-08-21T23:15:24Z'
---

# Literature Overview: Foundational Architectures & Efficient Adaptation

## Executive Synthesis
- **[EN]**: Over the past decade, deep learning paradigms have evolved from deep residual convolutional networks (ResNet, 2016) to fully attention-based foundation architectures (Transformer, 2017), culminating in modular parameter-efficient adaptation strategies (LoRA, 2021).
- **[CN] 核心综述**：过去十年中，深度学习范式经历了从深度残差卷积网络（ResNet，2016）到全注意力基础架构（Transformer，2017），再到模块化参数高效微调策略（LoRA，2021）的系统演进。

---

## Chronological Milestones
| Year | Paper / Initiative | Key Innovation | Primary Impact |
|---|---|---|---|
| 2016 | [[Sources/Papers/he2016deep|ResNet]] | Residual shortcut connections | Enabled training 100+ layer networks |
| 2017 | [[Sources/Papers/vaswani2017attention|Transformer]] | Multi-head self-attention | Replaced recurrence; unified NLP |
| 2021 | [[Sources/Papers/hu2021lora|LoRA]] | Low-rank weight matrix adaptation | Enabled efficient fine-tuning of 100B+ LLMs |

---

## Key Paradigms
| Paradigm | Core Hypothesis | Mechanism / Formula | Key Limitations | Canonical Papers |
|---|---|---|---|---|
| Residual Learning | Layers should learn residual functions | $F(x) + x$ shortcuts | High memory footprint | [[Sources/Papers/he2016deep]] |
| Self-Attention | Token interactions replace recurrence | Scaled dot-product | $O(N^2)$ context cost | [[Sources/Papers/vaswani2017attention]] |
| Low-Rank Adaptation | Task adaptation has low intrinsic rank | $W_0 + BA$ decomposition | Tuning rank $r$ heuristic | [[Sources/Papers/hu2021lora]] |

---

## Evidence & Benchmark Matrix
| Task / Benchmark | Baseline Metric | Proposed Metric | Delta (\Delta) | Source Note |
|---|---|---|---|---|
| ImageNet Top-5 Error | 4.49% (VGG-16) | 3.57% (ResNet-152) | -0.92% (p < 0.001) | [[Sources/Papers/he2016deep#Evidence]] |
| WMT 2014 EN-DE BLEU | 26.0 (ConvS2S) | 28.4 (Transformer Big) | +2.4 BLEU | [[Sources/Papers/vaswani2017attention#Evidence]] |
| GPT-3 175B WikiSQL Acc | 73.8% (FT) | 74.0% (LoRA) | +0.2% | [[Sources/Papers/hu2021lora#Evidence]] |

---

## Cross-Paper Links
- [[Sources/Papers/he2016deep]]
- [[Sources/Papers/hu2021lora]]
- [[Sources/Papers/vaswani2017attention]]
