---
type: concept
project: zotero_obsidian_kb
title: "Saturation Current Density Benchmarking in Logic Transistors"
slug: saturation_current_density_benchmarking
canvas_visibility: visible
status: active
claim_strength: strong
domain: semiconductor-devices
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
canonical_equation: 'I_{on} = q n_{2D} v_{inj}'
updated: 2026-08-19T08:50:00Z
---

# Saturation Current Density Benchmarking in Logic Transistors
> **中文概念**：逻辑晶体管开态饱和电流密度基准评估

---

## Definition
- **[EN]**: In ultra-short-channel nanoscale transistors, carrier transport transitions from diffusive drift to quasi-ballistic injection. Consequently, low-field drift mobility ceases to dictate switching speed; the **saturation on-current density per unit width ($I_{on}/W$)** at a fixed supply voltage ($V_{dd}$) and specified off-current ($I_{off}$) represents the sole decisive figure of merit for logic circuit delay.
- **[CN] 概念定义**：在超短沟道纳米晶体管中，载流子输运从传统扩散漂移机制转变为准弹道注入机制。因此，低场漂移迁移率不再决定逻辑门电路的翻转延迟；在固定供电电压 ($V_{dd}$) 和规定关态漏电流 ($I_{off}$) 条件下的**单位宽度开态饱和电流密度 ($I_{on}/W$)**，才是评价逻辑晶体管性能的最核心客观基准。

---

## Mathematical Formulation
- **[EN] Ballistic Injection Current Equation**:
  $$I_{on} = q \cdot n_{2D} \cdot v_{inj} \cdot \mathcal{T}$$
  Where:
  - $q$ is the elementary electron charge / 基本电荷量 $(1.6 \times 10^{-19}\text{ C})$
  - $n_{2D}$ is the 2D sheet carrier density at the top of the barrier / 势垒顶端载流子面密度 $(\text{cm}^{-2})$
  - $v_{inj}$ is the thermal/ballistic carrier injection velocity / 载流子注入初速度 $(\approx 10^7\text{ cm/s})$
  - $\mathcal{T}$ is the ballistic transmission coefficient / 弹道透射系数 $(0 < \mathcal{T} \le 1)$
- **[CN] 物理推导**：
  - 提高 $I_{on}/W$ 的核心路径是提升顶端载流子面密度 $n_{2D}$（依赖减小 EOT 与降低接触电阻 $R_c$）以及选择高注入速度 $v_{inj}$（与能带有效质量 $m^*$ 相关）的材料。

---

## Theoretical Grounding
- **[EN]**: Historical literature often prioritized peak field-effect mobility $\mu_{FE}$ measured in long-channel devices. However, long-channel mobility fails to predict nanoscale digital performance where high lateral electric fields cause severe velocity saturation and quasi-ballistic injection.
- **[CN] 理论基础**：学术界早期常将长沟道器件测得的峰值场效应迁移率 $\mu_{FE}$ 作为宣传亮点。然而在先进制程纳米尺度下，强纵向电场导致载流子速度迅速饱和，器件完全受限于弹道注入速度与接触压降，长沟道迁移率与最终芯片时钟频率严重脱节。

---

## Evidence & Empirical Support
- **[EN]**: [[Sources/Papers/2021_Liu_2D-Transistors#Evidence|Liu et al. (Nature 2021)]] benchmarks demonstrated that 2D $\text{MoS}_2$ FETs with low contact resistance achieve $I_{on} > 1\text{ mA}/\mu\text{m}$ at $V_{ds} = 1\text{ V}$, meeting the IRDS targets for future silicon-equivalent logic nodes.
- **[CN] 实证支持**：[[Sources/Papers/2021_Liu_2D-Transistors#Evidence|Liu et al. (Nature 2021)]] 总结指出，优化接触电阻后的单层 $\text{MoS}_2$ 晶体管在 $V_{ds} = 1\text{ V}$ 下实测开态电流已突破 $1\text{ mA}/\mu\text{m}$，完全满足国际器件与系统路线图 (IRDS) 对未来先进逻辑节点的指标要求。

---

## Limitations & Boundary Conditions
- **[EN]**: Achieving near-ballistic $I_{on}$ in practice is heavily throttled by metal-semiconductor contact resistance ($R_c$) and self-heating degradation under high current densities.
- **[CN] 适用边界与局限性**：高开态电流密度的实际发挥严重受制于金属接触电阻 ($R_c$) 以及大电流密度下的自发热效应 (Self-Heating Effect)。

---

## Cross-References
- [[Sources/Papers/2021_Liu_2D-Transistors]]
- [[Sources/Papers/2022_Cheng_FET-Benchmark]]
- [[Knowledge/Concepts/two_dimensional_transistor_scaling]]
- [[Knowledge/Concepts/contact_resistance_extraction]]
- [[Knowledge/Concepts/emerging_fet_benchmarking]]
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
