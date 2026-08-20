---
type: concept
project: 2d-semiconductors
title: Two-Dimensional Transistor Scaling Physics
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
  - "[[Sources/Papers/2022_Cheng_FET-Benchmark]]"
tags:
  - type/concept
  - topic/semiconductor
  - topic/2d-materials
  - status/promoted
aliases:
  - 2D Transistor Scaling
  - Characteristic Length
  - 二维晶体管微缩物理
created: 2026-03-29
updated: 2026-04-18
---

# 🧬 Two-Dimensional Transistor Scaling Physics / 二维晶体管微缩物理机制

## Definition
- **[EN]**: Explains how atomically thin 2D semiconductors (such as monolayer $\text{MoS}_2$, $\text{WS}_2$, $\text{WSe}_2$) overcome short-channel effects (SCE) and drain-induced barrier lowering (DIBL) at extreme physical gate lengths ($L_g < 10\text{ nm}$) due to their pristine surfaces and atomic body thickness ($t_b < 1\text{ nm}$).
- **[CN]**: 阐明原子级厚度的二维半导体（如单层 $\text{MoS}_2$、$\text{WS}_2$、$\text{WSe}_2$）如何凭借无悬挂键的理想表面与亚纳米体厚度 ($t_b < 1\text{ nm}$)，在极限物理栅长 ($L_g < 10\text{ nm}$) 下彻底抑制短沟道效应 (SCE) 与漏致势垒降低效应 (DIBL)。

---

## Mathematical Formulation & Scaling Physics

$$\lambda = \sqrt{\frac{\varepsilon_b}{\varepsilon_{ox}} t_b t_{ox} + \frac{\varepsilon_b}{2 \varepsilon_{sub}} t_b t_{sub}}$$

- $\lambda$: Electrostatic characteristic length (特征静电长度，器件必须满足 $L_g \ge 3\lambda$ 以避免漏电失控)
- $\varepsilon_b, \varepsilon_{ox}, \varepsilon_{sub}$: Dielectric constants of channel, gate oxide, and substrate (沟道、栅氧化层与衬底的介电常数)
- $t_b, t_{ox}, t_{sub}$: Physical thicknesses of channel, oxide, and substrate (沟道厚度、氧化层厚度与衬底耗尽厚度)

Because monolayer 2D crystals reach $t_b = 0.65\text{ nm}$ while maintaining high carrier transport without surface dangling bonds, $\lambda$ drops below $2\text{ nm}$, enabling physical gate length scaling down to sub-5-nm.

---

## Supporting Evidence
- `EVD-2021_Liu_2D-Transistors-01`: Theoretical derivation and electrostatic simulation proving SCE immunity in atomically thin 2D channels down to sub-10-nm gate lengths.
- `EVD-2022_Cheng_FET-Benchmark-03`: Highlights that electrostatic integrity must be preserved alongside low contact resistance for true scaling benefits.

---

## Related Knowledge & Papers
- [[Sources/Papers/2021_Liu_2D-Transistors|Liu et al. (Nature 2021)]]
- [[Sources/Papers/2022_Cheng_FET-Benchmark|Cheng et al. (Nature Electronics 2022)]]
- [[Knowledge/Concepts/saturation_current_density_benchmarking]]
- [[Knowledge/Concepts/emerging_fet_benchmarking]]
- [[Knowledge/Literature Overview]]
