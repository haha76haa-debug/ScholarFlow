---
type: comparison
project: 2d-semiconductors
title: "{{title}}"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/{{primary_source_citekey}}]]"
silicon_reference_nodes:
  - "Silicon FinFET (5nm)"
  - "Silicon GAAFET Nanosheet (3nm/2nm)"
  - "Complementary FET (CFET / A14-A10)"
dimensions_covered:
  - 1
  - 2
  - 3
  - 4
  - 5
  - 6
tags:
  - type/comparison
  - topic/semiconductor
  - topic/silicon-analogy
  - topic/microelectronics
  - status/promoted
aliases:
  - "{{title}}"
  - "{{chinese_title}}"
created: "{{date}}"
updated: "{{date}}T{{time}}Z"
---

# ⚖️ {{title}} / {{chinese_title}}

> **Focus / 核心主题**: *(Brief description of the microelectronics engineering comparison between 2D semiconductors and silicon technologies)*

---

## Executive Overview & Silicon Analogy
- **[EN] Executive Summary**:
  - *Core physical difference between 2D nanomaterial approach and conventional bulk/3D silicon CMOS.*
  - *Key architectural benefits, bottlenecks, and scaling implications.*
- **[CN] 硅基微电子技术映射与对照总述**:
  - *(系统性对比二维半导体与硅基集成电路在材料物理、器件结构与工艺集成上的本质差异与互补特性)*

---

## 1. Physical Scaling & Electrostatic Control
- **[EN] Scaling Physics & Dimensionality**:
  - Scale length equation:
    $$\lambda = \sqrt{\frac{\varepsilon_b}{\varepsilon_{ox}} t_b t_{ox} + \frac{\varepsilon_b}{2\varepsilon_{sub}} t_b t_{sub}}$$
  - Comparison of electrostatic gate control, short-channel effects (SCE), subthreshold swing ($SS$), and drain-induced barrier lowering (DIBL).
- **[CN] 物理微缩与静电完整性对比**:
  - *(二维超薄体抑制短沟道效应机制 vs 硅基三维环栅/纳米片结构在极限微缩下的量子限域与表面粗糙散射)*

---

## 2. Ohmic Contact & Metallization Engineering
- **[EN] Contact Physics & Interface Metallization**:
  - Contact resistance extraction and transfer length formulation:
    $$R_c \cdot W = \frac{\rho_c}{L_T} \coth\left(\frac{L_c}{L_T}\right), \quad L_T = \sqrt{\frac{\rho_c}{R_{sh}}}$$
  - Schottky barrier height pinning factor $S = \frac{d\Phi_B}{d\Phi_M}$ and Metal-Induced Gap States (MIGS) suppression.
- **[CN] 欧姆接触与金属化界面工程**:
  - *(二维半导体范德华/半金属无钉扎接触 vs 硅基自对准硅化物 Salicide 欧姆接触工艺机制与界面态密度调控)*

---

## 3. Gate Dielectric & EOT Scaling
- **[EN] Dielectric Nucleation & Interface Traps**:
  - High-k integration on dangling-bond-free 2D channels vs thermal $\text{SiO}_2 / \text{HfO}_2$ on silicon.
  - Equivalent oxide thickness ($EOT$) scaling and interface state density ($D_{it}$) requirements.
- **[CN] 栅介质沉积与等效氧化层厚度微缩**:
  - *(原子级洁净无悬挂键表面的高-k ALD 种子层成核技术 vs 硅基原生氧化层界面的极低缺陷密度对比)*

---

## 4. CMOS Integration & Thermal Budget
- **[EN] Manufacturing Process & Thermal Budget Compatibility**:
  - Back-End-of-Line (BEOL) Monolithic 3D (M3D) stacking thermal budget ($T < 400^\circ\text{C}$).
  - Front-End-of-Line (FEOL) high-temperature dopant activation annealing in silicon ($T > 900^\circ\text{C}$).
  - Complementary n-FET / p-FET threshold voltage matching and co-integration.
- **[CN] CMOS 量产兼容性与热预算分析**:
  - *(二维器件低温后道单片 3D 集成潜力 vs 传统硅基前道高温离子注入退火工艺与互补极性集成挑战)*

---

## 5. IRDS Technology Roadmap Alignment
- **[EN] IEEE IRDS Technology Targets & Milestones**:
  - Alignment against sub-2nm, A14, A10, and sub-1nm node specifications:
    - Physical gate length $L_g \le 12\text{ nm}$
    - Contacted Poly Pitch $CPP \le 40\text{ nm}$
    - Contact resistance $R_c \le 50\ \Omega\cdot\mu\text{m}$
    - On-state current density $I_{on}/W \ge 1.0-1.5\text{ mA}/\mu\text{m}$
- **[CN] IRDS 国际半导体技术路线图对标**:
  - *(量化对标国际器件与系统路线图在亚 1 纳米与埃米时代的几何尺寸、寄生电阻与驱动电流门槛)*

---

## 6. Electrical Benchmark & Compact Modeling Matrix
- **[EN] Key Metrics & Compact Modeling Equations**:
  - Comparative Parameter Table:

| Metric / Parameter | 2D Semiconductor Target | Silicon Reference Node (GAAFET/CFET) | Engineering Gap / Assessment |
|---|---|---|---|
| **Channel Thickness ($t_{ch}$)** | Monolayer ($0.65\text{ nm}$) | $t_{si} \approx 5\text{ nm}$ Nanosheet | 2D superior in SCE resistance |
| **Contact Resistance ($R_c$)** | $< 100\ \Omega\cdot\mu\text{m}$ | $15-30\ \Omega\cdot\mu\text{m}$ (NiSi) | Silicon currently superior |
| **Subthreshold Swing ($SS$)** | $< 65\text{ mV/dec}$ | $65-72\text{ mV/dec}$ | 2D approaches Boltzmann limit |
| **Drive Current ($I_{on}/W$)** | $> 1.0\text{ mA}/\mu\text{m}$ ($V_{dd}=0.7\text{V}$) | $1.2-1.8\text{ mA}/\mu\text{m}$ | Rapidly converging with semi-metal contacts |

  - Compact Modeling Formulation:
    - BSIM-CMG multi-gate 3D Poisson drift-diffusion vs 2D Landauer-Büttiker ballistic multi-subband transport.
- **[CN] 电学参数基准与紧凑模型矩阵**:
  - *(紧凑模型参数提取方法、寄生电容/电阻网络与工业级 SPICE 模型对接分析)*

---

## References & Evidence Anchors
- **Primary Literature Sources**:
  - [[Sources/Papers/{{primary_source_citekey}}]]
- **Evidence Records**:
  - `EVD-{{primary_source_citekey}}-01`
- **Related Concept Notes**:
  - [[Knowledge/Concepts/two_dimensional_transistor_scaling]]
  - [[Knowledge/Concepts/contact_resistance_extraction]]
  - [[Knowledge/Concepts/emerging_fet_benchmarking]]
  - [[Knowledge/Concepts/saturation_current_density_benchmarking]]
- **Syntheses & Indexes**:
  - [[Knowledge/Literature Overview]]
  - [[Knowledge/Method Taxonomy]]
  - [[Writing/comparison-matrix]]

