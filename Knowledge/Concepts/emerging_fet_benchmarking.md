---
type: concept
project: zotero_obsidian_kb
title: "Emerging FET Benchmarking Guidelines"
slug: emerging_fet_benchmarking
canvas_visibility: visible
status: active
claim_strength: strong
domain: semiconductor-devices
primary_sources:
  - "[[Sources/Papers/2022_Cheng_FET-Benchmark]]"
canonical_equation: 'SS = \frac{\partial V_{gs}}{\partial (\log_{10} I_d)}'
updated: 2026-08-19T08:08:00Z
---

# Emerging FET Benchmarking Guidelines
> **中文概念**：新兴低维场效应晶体管基准测试指南

---

## Definition
- **[EN]**: A standardized benchmarking framework for emerging low-dimensional field-effect transistors (FETs, such as monolayer $\text{MoS}_2$, carbon nanotubes, and 2D semiconductors). It establishes uniform extraction rules and comparison metrics to prevent selective reporting and ensure meaningful performance benchmarking against Silicon CMOS standards.
- **[CN] 概念定义**：面向新兴低维场效应晶体管（如单层 $\text{MoS}_2$、碳纳米管、二维半导体）的标准化基准测试与参数提取规范。旨在建立统一的器件参数提取与对比规则，消除学术界选择性报道的问题，实现与硅基先进 CMOS 节点的严谨客观对标。

---

## Mathematical Formulation
- **[EN] Core Metric Formulations**:
  1. **Subthreshold Swing ($SS$) / 亚阈值摆幅**:
  $$SS = \left( \frac{\partial \log_{10} I_d}{\partial V_{gs}} \right)^{-1} = \frac{k_B T}{q} \ln(10) \left( 1 + \frac{C_{it} + C_d}{C_{ox}} \right)$$
  2. **On/Off Current Ratio / 开关电流比**:
  $$\text{Ratio} = \frac{I_{on} (V_{gs} = V_{dd}, V_{ds} = V_{dd})}{I_{off} (V_{gs} = V_{off}, V_{ds} = V_{dd})}$$
  3. **Effective Drive Current Normalization / 归一化开态电流**:
  $$I_{on} / W \quad (\mu\text{A}/\mu\text{m})$$
- **[CN] 关键公式解析**：
  - 亚阈值摆幅 $SS$ 反映栅控能力，室温玻尔兹曼极限为 $60\text{ mV/dec}$；
  - 必须在统一的供电电压 $V_{dd}$ 条件下比对开态电流密度与开关比。

---

## Theoretical Grounding
- **[EN]**: Device performance in low-dimensional FETs is strongly dominated by extrinsic parasitics (such as contact resistance $R_c$, gate dielectric trap density $D_{it}$, and series resistance). Without standardizing reporting conditions, extrinsic device measurements can distort intrinsic transport physics.
- **[CN] 理论基础**：在原子级超薄的低维材料体系中，器件实测性能极大程度受到金属-半导体接触电阻 ($R_c$)、栅介质界面陷阱 ($D_{it}$) 等寄生效应的主导。如果不进行规范化解耦，外在寄生损耗将严重掩盖材料本征的物理输运极限。

---

## Evidence & Empirical Support
- **[EN]**: Demonstrated across monolayer $\text{MoS}_2$ FET benchmarks in [[Sources/Papers/2022_Cheng_FET-Benchmark#Evidence|Cheng et al. (Nature Electronics 2022)]]. Canonical $I_{on}$-$I_{off}$ envelopes demonstrate that contact-de-embedded metrics align closely with theoretical ballistic limits.
- **[CN] 实证支持**：经 [[Sources/Papers/2022_Cheng_FET-Benchmark#Evidence|Cheng et al. (Nature Electronics 2022)]] 对全球数百组单层 $\text{MoS}_2$ 器件实测数据调研验证。在统一标准下扣除接触电阻后，本征饱和电流与理论弹道输运预测高度一致。

---

## Limitations & Boundary Conditions
- **[EN]**: Primary guidelines target DC characteristics; high-speed AC switching dynamics require separate parasitic capacitance calibration.
- **[CN] 边界条件与局限性**：当前规范主要针对静态直流特性；涉及射频截止频率与瞬态逻辑反演特性的评估需结合高频寄生电容单独标定。

---

## Cross-References
- [[Sources/Papers/2022_Cheng_FET-Benchmark]]
- [[Knowledge/Concepts/contact_resistance_extraction]]
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
