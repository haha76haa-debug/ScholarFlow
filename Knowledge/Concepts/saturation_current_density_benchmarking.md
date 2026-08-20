---
type: concept
project: 2d-semiconductors
title: Saturation Current Density Benchmarking
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
  - "[[Sources/Papers/2022_Cheng_FET-Benchmark]]"
tags:
  - type/concept
  - topic/semiconductor
  - topic/benchmarking
  - status/promoted
aliases:
  - Saturation Current Density
  - Ion/W
  - 饱和电流密度标杆评估
created: 2026-03-29
updated: 2026-04-18
---

# 🧬 Saturation Current Density Benchmarking / 饱和电流密度标杆评估准则

## Definition
- **[EN]**: Saturation current density ($I_{sat}/W$ or $I_{on}/W$) is the maximum on-state current flowing through a transistor channel normalized by channel width ($W$) under high drain bias ($V_{ds} = V_{dd}$) and full gate overdrive ($V_{gs} - V_{th} = V_{dd}$).
- **[CN]**: 饱和电流密度 ($I_{sat}/W$ 或 $I_{on}/W$) 是晶体管在高漏极偏压 ($V_{ds} = V_{dd}$) 与充分栅极过驱动 ($V_{gs} - V_{th} = V_{dd}$) 状态下，按沟道宽度归一化的最大开态驱动电流。

```
                       $I_{on}/W$ 决定逻辑门延迟 $\tau = \frac{C_L V_{dd}}{I_{on}}$
```

---

## Mechanism & Ballistic Transport Model

In short-channel ballistic nanotransistors, saturation current is governed by the carrier injection velocity ($v_{inj}$) rather than diffusive low-field mobility:

$$I_{sat}/W = q \cdot n_{2D} \cdot v_{inj}$$

- $q$: Elementary charge (元电荷)
- $n_{2D}$: 2D carrier density in channel (沟道二维载流子面密度)
- $v_{inj}$: Thermal injection / saturation velocity (载流子热注入速度 / 饱和速度)

---

## Supporting Evidence
- `EVD-2022_Cheng_FET-Benchmark-01`: Standardizes width normalization and voltage matching for emerging logic transistors.
- `EVD-2021_Liu_2D-Transistors-02`: Demonstrates that ballistic injection velocity dictates on-current performance at sub-10-nm physical gate lengths.

---

## Related Knowledge & Papers
- [[Sources/Papers/2021_Liu_2D-Transistors|Liu et al. (Nature 2021)]]
- [[Sources/Papers/2022_Cheng_FET-Benchmark|Cheng et al. (Nature Electronics 2022)]]
- [[Knowledge/Concepts/two_dimensional_transistor_scaling]]
- [[Knowledge/Concepts/emerging_fet_benchmarking]]
- [[Writing/comparison-matrix]]
