---
type: method-taxonomy
project: zotero_obsidian_kb
title: 'Method Taxonomy: Deep Learning Architectures & Adaptation'
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

# Method Taxonomy: Deep Learning Architectures & Adaptation

> [!abstract]+ 📌 方法体系导读 (Methodology Overview)
> - **[EN]**: Hierarchical taxonomy of physical modeling, experimental parameter extraction, and benchmarking methodologies in emerging semiconductor electronics.
> - **[CN] 方法学体系概述**：构建涵盖微观器件物理建模、宏观电学参数提取及学术报告标准化的三层方法学分类树。

---

## Taxonomy Tree
```
Deep Learning Methods & Architectures (深度学习方法学分类树)
├── 1. Backbone Architectures & Optimization
│   ├── 1.1 Convolutional & Residual Networks
│   │   └── Residual Shortcut Mapping: F(x) + x ([[Sources/Papers/he2016deep]])
│   └── 1.2 Attention & Sequence Models
│       ├── Scaled Dot-Product Attention ([[Sources/Papers/vaswani2017attention]])
│       └── Multi-Head Attention Mechanism ([[Sources/Papers/vaswani2017attention]])
└── 2. Efficient Fine-Tuning & Adaptation
    ├── 2.1 Low-Rank Decomposition
    │   └── Low-Rank Matrix Factorization: W + BA ([[Sources/Papers/hu2021lora]])
    └── 2.2 Parameter-Efficient Fine-Tuning (PEFT)
```

---

## Comparative Method Matrix
| Method Family | Mathematical Operation | Primary Advantage | Primary Constraint |
|---|---|---|---|
| Residual Connection | $y = \mathcal{F}(x, \{W_i\}) + x$ | Gradients backpropagate directly | Memory footprint scales with depth |
| Multi-Head Attention | $\text{Concat}(head_1, \dots, head_h)W^O$ | Captures joint subspace representations | Quadratic complexity in sequence length |
| Low-Rank Adaptation | $h = W_0 x + \frac{\alpha}{r} B A x$ | Zero additional inference latency | Requires rank heuristic selection |

---

## Evolutionary Lineage
- **2015-2016**: Residual Connections ([[Sources/Papers/he2016deep]]) overcome vanishing gradients in CNNs.
- **2017**: Self-Attention & Transformers ([[Sources/Papers/vaswani2017attention]]) replace recurrence with parallel token routing.
- **2021**: Low-Rank Adaptation ([[Sources/Papers/hu2021lora]]) enables targeted rank decomposition for large foundational checkpoints.
