---
type: research-gaps
project: zotero_obsidian_kb
title: 'Research Gaps: Architectural Bottlenecks & Open Questions'
status: active
covered_papers:
- '[[Sources/Papers/he2016deep]]'
- '[[Sources/Papers/hu2021lora]]'
- '[[Sources/Papers/vaswani2017attention]]'
key_themes:
- research-gaps
- quadratic-complexity
- lora-rank-selection
updated: '2026-08-21T23:15:24Z'
---

# Research Gaps: Architectural Bottlenecks & Open Questions

> [!abstract]+ 📌 开放瓶颈导读 (Bottlenecks Overview)
> - **[EN]**: Catalog of unresolved physical limits, fabrication hurdles, and benchmarking discrepancies across emerging semiconductors.
> - **[CN] 核心挑战概述**：系统归纳当前器件从实验室走向工业制造所面临的未解物理瓶颈、工艺挑战与测试标准差异。

---

## Gap Catalog

### GAP-01: Quadratic Scaling of Standard Self-Attention
- **Description**: Standard full self-attention exhibits $O(N^2)$ computational and memory complexity with respect to sequence length $N$.
- **Source Context**: [[Sources/Papers/vaswani2017attention]]
- **Evidence Anchor**: EVD-vaswani2017attention-01
- **Current State**: Addressed by FlashAttention, linear attention variants, and state-space models.
- **Open Challenges**: Retaining full associative recall while achieving sub-quadratic throughput on commodity hardware.

### GAP-02: Rank Selection Heuristics in Low-Rank Adaptation
- **Description**: Finding optimal rank $r$ and target modules across heterogeneous LLM layers remains predominantly empirical.
- **Source Context**: [[Sources/Papers/hu2021lora]]
- **Evidence Anchor**: EVD-hu2021lora-01
- **Current State**: Addressed by AdaLoRA and dynamic pruning algorithms.
- **Open Challenges**: Automated layer-specific rank allocation under strict parameter budgets.

---

## Unresolved Theoretical Questions
- Mathematical characterization of expressivity loss when decomposing full rank gradient updates into rank $r \ll d$.
- Exact convergence guarantees for shortcut connections in overparameterized Transformer blocks.

---

## Priority Matrix for Future Investigation
| Gap ID | Impact | Feasibility | Target Timeline | Canonical Source |
|---|---|---|---|---|
| GAP-01 | High | Medium | P1 | [[Sources/Papers/vaswani2017attention]] |
| GAP-02 | High | High | P1 | [[Sources/Papers/hu2021lora]] |
