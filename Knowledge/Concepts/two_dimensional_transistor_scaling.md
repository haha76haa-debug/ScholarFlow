---
type: concept
project: zotero_obsidian_kb
title: "Two-Dimensional Transistor Scaling and Natural Length"
slug: two_dimensional_transistor_scaling
canvas_visibility: visible
status: active
claim_strength: strong
domain: semiconductor-devices
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
canonical_equation: '\lambda = \sqrt{\frac{\varepsilon_b}{\varepsilon_{ox}} t_b t_{ox}}'
updated: 2026-08-19T08:50:00Z
---

# Two-Dimensional Transistor Scaling and Natural Length
> **中文概念**：二维晶体管静电缩放与特征自然长度 $\lambda$

---

## Definition
- **[EN]**: The transistor electrostatic scaling theory dictates that the minimum channel length ($L_{ch}$) achievable without severe short-channel effects (drain-induced barrier lowering, threshold voltage roll-off) is bounded by the characteristic natural length $\lambda$. Atomically thin 2D semiconductors ($t_b < 1\text{ nm}$) minimize $\lambda$ to enable sub-5-nm physical gate lengths.
- **[CN] 概念定义**：晶体管静电微缩理论指出，在不发生严重短沟道效应（漏极诱导势垒降低 DIBL、阈值电压漂移）的前提下，器件可微缩的最小物理栅长受限于特征自然长度 $\lambda$。原子级单层二维半导体（厚度 $t_b < 1\text{ nm}$ 且表面无悬挂键）能够将 $\lambda$ 压缩至物理极限，从而支持亚 5 纳米乃至 1 纳米物理栅长的晶体管微缩。

---

## Mathematical Formulation
- **[EN] Electrostatic Scaling Length Equations**:
  $$\lambda = \sqrt{\frac{\varepsilon_b}{\varepsilon_{ox}} t_b t_{ox} + \frac{\varepsilon_b}{2\varepsilon_{sub}} t_b t_{sub}}$$
  In a double-gate or gate-all-around (GAA) structure with high-$\kappa$ dielectric ($\varepsilon_{ox} \gg \varepsilon_b$):
  $$\lambda \approx \sqrt{\frac{\varepsilon_b}{2\varepsilon_{ox}} t_b t_{ox}}$$
  To maintain excellent gate control ($SS < 70\text{ mV/dec}$), the channel length must satisfy:
  $$L_{ch} \ge 3 \cdot \lambda$$
- **[CN] 公式解析与缩放判据**：
  - $t_b$ 为半导体沟道体厚度，$\varepsilon_b$ 为沟道介电常数；
  - $t_{ox}$ 为栅氧化层厚度，$\varepsilon_{ox}$ 为栅介质介电常数；
  - 经典静电微缩判据要求物理栅长 $L_{ch} \ge 3\lambda$，单层 2D 材料可使 $\lambda < 1.5\text{ nm}$，支撑 $L_{ch} < 5\text{ nm}$。

---

## Theoretical Grounding
- **[EN]**: Unlike conventional 3D semiconductors (Silicon, Germanium, III-V) whose carrier mobility degrades precipitously when thinned below $3\text{ nm}$ due to surface roughness and dangling bond scattering, pristine van der Waals 2D semiconductors maintain high mobility down to single-layer thickness ($0.65\text{ nm}$).
- **[CN] 理论基础**：传统三维半导体（硅、锗、III-V族）在体厚度减薄至 $3\text{ nm}$ 以下时，严重的表面粗糙度散射与悬挂键诱发的界面缺陷态会导致迁移率急剧崩溃。而原子级范德华二维半导体天然具备平整无悬挂键表面，在单原子层厚度 ($0.65\text{ nm}$) 下仍能保持优异的载流子输运。

---

## Evidence & Empirical Support
- **[EN]**: Formulated and validated by [[Sources/Papers/2021_Liu_2D-Transistors#Evidence|Liu et al. (Nature 2021)]], demonstrating that monolayer $\text{MoS}_2$ and $\text{WSe}_2$ transistors retain subthreshold swings of $\approx 65\text{ mV/dec}$ at $L_{ch} < 10\text{ nm}$.
- **[CN] 实证支持**：由 [[Sources/Papers/2021_Liu_2D-Transistors#Evidence|Liu et al. (Nature 2021)]] 建立并论证。实测表明，单层 $\text{MoS}_2$ 与 $\text{WSe}_2$ 晶体管在栅长微缩至 $10\text{ nm}$ 以下时仍能保持接近极限的 $\approx 65\text{ mV/dec}$ 亚阈值摆幅。

---

## Limitations & Boundary Conditions
- **[EN]**: As $L_{ch}$ shrinks below $3\text{ nm}$, quantum direct source-to-drain tunneling becomes the dominant leakage mechanism rather than classical electrostatic short-channel effects.
- **[CN] 边界条件与局限性**：当物理栅长微缩至 $3\text{ nm}$ 以下时，源漏之间的量子直接隧穿将取代经典静电效应成为主要的关态漏电机制。

---

## Cross-References
- [[Sources/Papers/2021_Liu_2D-Transistors]]
- [[Sources/Papers/2022_Cheng_FET-Benchmark]]
- [[Knowledge/Concepts/saturation_current_density_benchmarking]]
- [[Knowledge/Concepts/emerging_fet_benchmarking]]
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
