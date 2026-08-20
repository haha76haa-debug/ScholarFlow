---
type: paper
project: 2d-semiconductors
title: Transistor roadmap beyond CMOS
citekey: 2021_Liu_2D-Transistors
zotero_key: JJGAEFUH
status: read
source_type: journal article
claim_strength: strong
authors:
  - Yuxiang Liu
  - Xiangfeng Duan
  - Chen Wang
year: 2021
journal: Nature
doi: 10.1038/s41586-021-03339-z
tags:
  - type/paper
  - topic/semiconductor
  - topic/2d-materials
  - method/benchmarking
  - status/synthesized
evidence_count: 3
created: 2026-03-29
updated: 2026-04-18
linked_knowledge:
  - "[[Knowledge/Literature Overview]]"
  - "[[Knowledge/Method Taxonomy]]"
  - "[[Knowledge/Research Gaps]]"
  - "[[Knowledge/Concepts/two_dimensional_transistor_scaling]]"
  - "[[Knowledge/Concepts/saturation_current_density_benchmarking]]"
  - "[[Knowledge/Concepts/emerging_fet_benchmarking]]"
  - "[[Knowledge/Concepts/contact_resistance_extraction]]"
---

# 📚 Transistor roadmap beyond CMOS / 后 CMOS 晶体管技术路线图

- **Journal / 期刊**: *Nature* (2021), Vol. 591, pp. 43–53
- **DOI**: [10.1038/s41586-021-03339-z](https://doi.org/10.1038/s41586-021-03339-z)
- **Citekey**: `2021_Liu_2D-Transistors`
- **Zotero URI**: [Open in Zotero](zotero://select/items/@2021_Liu_2D-Transistors)

---

## Claim
- **[EN]**: Monolayer two-dimensional (2D) semiconductors offer superior electrostatic control over sub-10-nm gate lengths, overcoming fundamental scaling limits of 3D silicon GAAFET architectures.
- **[CN]**: 单层二维 (2D) 半导体在 10 纳米以下物理栅长下具有无与伦比的静电调控能力，从物理底层突破了 3D 硅基环栅 (GAAFET) 架构的微缩极限。

---

## Research question
- **[EN]**: How can 2D semiconductors systematically scale below sub-1-nm technology nodes while mitigating interface contact resistance and high-k dielectric challenges?
- **[CN]**: 二维半导体如何在克服界面接触电阻与高介电常数栅介质挑战的同时，系统性微缩至亚 1 纳米技术节点？

---

## Method
- **[EN]**: Comprehensive electrostatic scaling physics modeling, ballistic transport derivation, and cross-technology literature benchmarking.
- **[CN]**: 体系化静电微缩物理建模、弹道输运理论推导与跨技术代文献标杆比对分析。

---

## Evidence
- Evidence ID: EVD-2021_Liu_2D-Transistors-01
- Source: [[Sources/Papers/2021_Liu_2D-Transistors]]
- Supports: "Monolayer 2D semiconductors suppress short-channel effects down to sub-10-nm gate lengths"
- Level: L1 (Physical Modeling & Consensus)
- Core Formula:
  $$\lambda = \sqrt{\frac{\varepsilon_b}{\varepsilon_{ox}} t_b t_{ox} + \frac{\varepsilon_b}{2 \varepsilon_{sub}} t_b t_{sub}}$$
- Detail:
  - **[EN]**: With body thickness $t_b \approx 0.65\text{ nm}$, characteristic length $\lambda < 2\text{ nm}$ enables gate lengths down to sub-5-nm without severe short-channel effects.
  - **[CN]**: 当沟道厚度 $t_b \approx 0.65\text{ nm}$ 时，特征静电长度 $\lambda < 2\text{ nm}$，使物理栅长微缩至 5 纳米以下仍无严重短沟道效应。

- Evidence ID: EVD-2021_Liu_2D-Transistors-02
- Source: [[Sources/Papers/2021_Liu_2D-Transistors]]
- Supports: "Ballistic saturation current density Ion/W is the primary benchmark metric"
- Detail:
  - **[EN]**: Saturation drive current $I_{on}/W > 1.0\text{ mA}/\mu\text{m}$ at $V_{dd} = 0.7\text{ V}$ is required to outperform silicon GAAFET nodes.
  - **[CN]**: 在 $V_{dd} = 0.7\text{ V}$ 下饱和驱动电流需满足 $I_{on}/W > 1.0\text{ mA}/\mu\text{m}$ 才能全面超越硅基 GAAFET 节点。

- Evidence ID: EVD-2021_Liu_2D-Transistors-03
- Source: [[Sources/Papers/2021_Liu_2D-Transistors]]
- Supports: "Contact resistance and equivalent oxide thickness dominate nanoscale 2D performance"
- Detail:
  - **[EN]**: Parasitic contact resistance $R_c < 100\ \Omega\cdot\mu\text{m}$ and gate dielectric $EOT < 0.6\text{ nm}$ are critical milestones.
  - **[CN]**: 寄生接触电阻 $R_c < 100\ \Omega\cdot\mu\text{m}$ 与栅介质 $EOT < 0.6\text{ nm}$ 是关键工艺里程碑。

---

## Strengths
- **Theoretical Authority / 权威推导**: Authoritative physics framework published in *Nature* (2021) / 发表在 *Nature* 上的权威物理架构。
- **Comprehensive Scope / 全局视野**: Covers channel scaling, contact physics, high-k integration, and wafer-scale synthesis / 涵盖沟道微缩、接触物理、介质集成与晶圆级合成。

---

## Limitation
- **P-Type FET Gap / P 型器件性能差距**: Complementary p-type 2D FETs lag behind n-type devices in contact resistance / 互补型 P 型 2D 器件在接触电阻上显著滞后于 N 型器件。
- **Wafer-Scale Uniformity / 晶圆级良率挑战**: Synthesis of high-mobility single-crystal monolayer films on 12-inch wafers remains challenging / 12 英寸晶圆级高迁移率单晶薄膜制备仍面临工艺挑战。

---

## Direct relevance to repo
- **[EN]**: Establishes the foundational electrostatic equation ($\lambda$) and on-current target benchmarks across the knowledge base.
- **[CN]**: 为全知识库确立了核心静电微缩方程 ($\lambda$) 与开态驱动电流标杆指标。

---

## Relation to other papers
- **[EN]**: Supplies the theoretical foundations and scaling targets evaluated by the reporting protocol in [[Sources/Papers/2022_Cheng_FET-Benchmark|Cheng et al. (Nature Electronics 2022)]].
- **[CN]**: 为 [[Sources/Papers/2022_Cheng_FET-Benchmark|Cheng et al. (Nature Electronics 2022)]] 中的评估规范提供了理论支撑与微缩目标。

---

## Knowledge links
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
- [[Knowledge/Research Gaps]]
- [[Knowledge/Concepts/two_dimensional_transistor_scaling]]
- [[Knowledge/Concepts/saturation_current_density_benchmarking]]
- [[Knowledge/Concepts/emerging_fet_benchmarking]]
- [[Knowledge/Concepts/contact_resistance_extraction]]
- [[Sources/Papers/2022_Cheng_FET-Benchmark]]
