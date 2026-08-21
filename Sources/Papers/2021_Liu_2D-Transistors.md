---
type: paper
project: zotero_obsidian_kb
title: "Promises and prospects of two-dimensional transistors"
citekey: 2021_Liu_2D-Transistors
zotero_key: "KF992J3I"
canvas_visibility: visible
status: summarized
source_type: "journal article"
claim_strength: strong
authors:
  - "Yuan Liu"
  - "Xidong Duan"
  - "Hyeon-Jin Shin"
  - "Seongjun Park"
  - "Yu Huang"
  - "Xiangfeng Duan"
year: 2021
venue: "Nature"
doi: "10.1038/s41586-021-03339-z"
url: "https://doi.org/10.1038/s41586-021-03339-z"
keywords:
  - 2d-materials
  - field-effect-transistors
  - sub-10-nm-scaling
  - saturation-current
  - contact-engineering
  - moores-law
tags:
  - type/paper
  - topic/semiconductor
  - topic/2d-materials
  - topic/silicon-analogy
  - method/benchmarking
  - status/synthesized
concepts:
  - "Two-Dimensional Transistor Scaling"
  - "Saturation Current Density Benchmarking"
methods:
  - "Electrostatic Scaling Characteristic Length Analysis"
  - "Short-Channel Ballistic Injection Model"
  - "Van der Waals Contact Integration"
subfield: semiconductor-devices
related_papers:
  - "Sources/Papers/2022_Cheng_FET-Benchmark"
linked_knowledge:
  - "Knowledge/Literature Overview"
  - "Knowledge/Method Taxonomy"
  - "Knowledge/Research Gaps"
  - "Knowledge/Concepts/two_dimensional_transistor_scaling"
  - "Knowledge/Concepts/saturation_current_density_benchmarking"
  - "Knowledge/Concepts/emerging_fet_benchmarking"
  - "Knowledge/Concepts/contact_resistance_extraction"
  - "Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet"
  - "Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide"
updated: 2026-08-21T08:48:00Z
---


# Promises and prospects of two-dimensional transistors
> **中文译名**：二维晶体管的前景与展望

---

## Claim
- **[EN]**: Atomically thin two-dimensional (2D) semiconductors offer the ultimate electrostatic scaling limit ($\lambda \propto \sqrt{t_b t_{ox}}$ with $t_b < 1\text{ nm}$) to overcome short-channel effects in sub-10-nm transistors. However, extrinsic carrier mobility is widely misinterpreted as the sole figure of merit; **saturation on-current density ($I_{on}/W$) in the short-channel ballistic limit** must serve as the true benchmark for logic computing.
- **[CN] 核心主张**：原子级超薄的二维（2D）半导体提供了终极的静电栅控缩放极限（特征长度 $\lambda \propto \sqrt{t_b t_{ox}}$，沟道厚度 $t_b < 1\text{ nm}$），能够彻底抑制亚 10 纳米晶体管中的短沟道效应。然而，外在载流子迁移率在学术界长期被误解与滥用，**短沟道弹道极限下的开态饱和电流密度 ($I_{on}/W$)** 才是衡量 2D 逻辑晶体管性能的根本基准。

---

## Research question
- **[EN]**: As silicon transistors approach atomic limits and short-channel degradation at sub-10-nm physical gate lengths, what fundamental physics and material-device integration hurdles (channels, contacts, high-$\kappa$ gate dielectrics, substrates, and lab-to-fab translation) dictate the true technological viability of 2D transistors for next-generation logic chips?
- **[CN] 核心科学问题**：随着硅基晶体管在亚 10 纳米物理栅长下逼近物理极限与短沟道退化，哪些根本性的器件物理机制与材料集成瓶颈（二维原子沟道、金属-半导体低阻接触、超薄高介电常数栅介质、晶圆级外延衬底以及实验室到先进制程量产的 Lab-to-Fab 转化）决定了二维晶体管在下一代计算芯片中的真实竞争力？

---

## Method
- **[EN] Electrostatic Scaling & Comprehensive Device Architecture Framework**:
  1. **Electrostatic Characteristic Length ($\lambda$)**: Derived the scaling boundary $\lambda = \sqrt{\frac{\varepsilon_b}{\varepsilon_{ox}} t_b t_{ox} + \frac{\varepsilon_b}{2 \varepsilon_{sub}} t_b t_{sub}}$, demonstrating that shrinking body thickness $t_b < 1\text{ nm}$ without surface dangling bonds enables physical gate lengths down to sub-5-nm.
  2. **Short-Channel Ballistic Carrier Injection**: Modeled top-of-the-barrier carrier velocity ($v_{inj}$) and demonstrated that drive current is dictated by quantum capacitance and injection velocity rather than long-channel drift mobility.
  3. **Interface & Contact Engineering**: Evaluated van der Waals (vdW) gap contacts, semimetal (Bi/Sb) zero-Schottky-barrier contacts, and 2D/high-$\kappa$ dielectric integration strategies.
- **[CN] 规范化方法与器件物理体系**：
  1. **静电特征缩放长度 ($\lambda$) 物理推导**：推导了 $\lambda = \sqrt{\frac{\varepsilon_b}{\varepsilon_{ox}} t_b t_{ox}}$，证明无表面悬挂键的单层原子厚度 ($t_b < 1\text{ nm}$) 能够将晶体管物理栅长推进至亚 5 纳米乃至 1 纳米极限。
  2. **短沟道弹道注入模型**：建立势垒顶端载流子注入速度 ($v_{inj}$) 模型，证明短沟道下开态电流由注入速度与量子电容决定，而非长沟道漂移迁移率。
  3. **界面与接触工程路线**：系统评述范德华 (vdW) 钝化接触、半金属 (Bi/Sb) 肖特基势垒消除技术及二维超薄 High-$\kappa$ 介质外延方案。

---

## Evidence
```md
Evidence ID: EVD-2021_Liu_2D-Transistors-01
Source: [[Sources/Papers/2021_Liu_2D-Transistors]]
Source type: journal article
Supports: "Demonstrates that sub-1nm 2D semiconductor channels can retain ideal subthreshold swing (<65 mV/dec) and high saturation current density (>1 mA/μm) at sub-10nm gate lengths / 证明亚1nm原子级二维沟道在亚10nm栅长下仍能保持理想亚阈值摆幅和超高饱和电流密度"
Contradicts: "Prior reliance on long-channel field-effect mobility as the primary benchmark for logic performance / 破除仅依赖长沟道迁移率评估先进制程逻辑性能的传统误区"
Method / dataset / metric: "Nature literature review / Electrostatic length λ (nm), Saturation current Ion (mA/μm), Contact resistance Rc (Ω·μm)"
Limitation: "Identifies remaining critical challenges in wafer-scale uniform CVD single-crystal growth, scalable p-type FET performance, and thermal dissipation in 2D stacked architectures"
Project relevance: "Master review defining the design principles and scaling limits for 2D semiconductor transistors in this knowledge base"
Claim strength: strong
```

```md
Evidence ID: EVD-2021_Liu_2D-Transistors-02
Source: [[Sources/Papers/2021_Liu_2D-Transistors]]
Source type: journal article
Supports: "Ballistic saturation current density Ion/W > 1.0 mA/μm at Vdd = 0.7 V is the primary benchmark metric for 2D transistor competitiveness with silicon GAAFET / 弹道饱和电流密度 Ion/W > 1.0 mA/μm 是二维晶体管对标 GAAFET 的核心指标"
Method / dataset / metric: "Ballistic injection velocity model, n_2D carrier density, IRDS sub-2nm node target: Ion/W > 1.0 mA/μm at Vdd = 0.7 V"
Project relevance: "Establishes the Ion/W benchmark for comparison against IRDS A14/A10 and CFET technology nodes / 确立与 IRDS A14/A10、CFET 节点对标的 Ion/W 基准"
Claim strength: strong
```

```md
Evidence ID: EVD-2021_Liu_2D-Transistors-03
Source: [[Sources/Papers/2021_Liu_2D-Transistors]]
Source type: journal article
Supports: "Contact resistance Rc < 100 Ω·μm and gate dielectric EOT < 0.6 nm are critical milestones; Fermi-level pinning and van der Waals gap states are primary sources of elevated Rc in MoS2 and WSe2 / 接触电阻 Rc < 100 Ω·μm 与栅介质 EOT < 0.6 nm 是 2D 器件的关键工艺里程碑"
Method / dataset / metric: "Contact resistance extraction: Rc·W (Ω·μm) via TLM; EOT from C-V; Fermi-level pinning factor S measured from barrier height vs metal work function"
Project relevance: "Identifies Fermi-level pinning and vdW gap states as physics-root-cause of Rc challenges, directly linking to comparison notes"
Claim strength: strong
```

---

## Strengths
- **Theoretical Authority / 权威性与物理洞见**:
  - Published as an authoritative review in *Nature* (2021) by leading pioneering teams from UCLA and Hunan University.
  - 由国际著名纳米电子学先驱段镶锋教授团队领衔发表于 *Nature*，深刻重塑了二维电子学领域的基准评价体系。
- **Comprehensive Architecture Scope / 架构全景覆盖**:
  - Systematically dissects the 4 critical pillars: Channel material, Contact interfaces, Dielectric oxides, and Substrate integration.
  - 全面解构了二维器件走向芯片级的四大支柱：沟道材料、接触电极、栅介质与衬底外延。
- **Constructive Roadmapping / 前瞻性技术路线图**:
  - Outlines actionable experimental targets for 2D devices to compete with sub-2nm GAAFET technology nodes.
  - 明确给出了二维晶体管对标亚 2 纳米 GAAFET 制程节点的关键物理指标量化目标。

---

## Limitation
- **P-Type FET Performance Gap / P 型器件性能滞后**:
  - High-performance n-type $\text{MoS}_2$ is extensively developed, but complementary p-type FETs ($\text{WSe}_2$, black phosphorus) still face higher contact barriers and doping instability.
  - 互补逻辑所必需的高性能 P 型器件（如 $\text{WSe}_2$）在接触电阻与掺杂稳定性上显著落后于 N 型 $\text{MoS}_2$。
- **Lab-to-Fab Scaling Bottlenecks / 工业制造量产鸿沟**:
  - Wafer-scale (12-inch) single-crystal monolayer synthesis with ultra-low defect density remains challenging.
  - 12 英寸晶圆级单晶单层生长、无损伤介质沉积及热耗散管理仍存在工程工艺挑战。

---

## Direct relevance to repo
- **[EN]**: Establishes the core physical scaling equation ($\lambda$) and on-current metric benchmarks for all semiconductor device modeling and experimental notes in this repository.
- **[CN] 本知识库直接应用价值**：确立了本知识库中所有半导体物理与低维电子学文献的物理特征长度 ($\lambda$) 缩放方程与开态饱和电流基准核心指标。

---

## Relation to other papers
- **[EN]**: Provides the foundational theoretical motivation and device physics underpinning the benchmark standards in [[Sources/Papers/2022_Cheng_FET-Benchmark|Cheng et al. (Nature Electronics 2022)]].
- **[CN] 与其他文献的关联**：为 [[Sources/Papers/2022_Cheng_FET-Benchmark|Cheng et al. (Nature Electronics 2022)]] 中确立的实验基准与参数提取清单提供了最核心的器件缩放物理依据与理论支撑。

---

## Silicon Analogy & Microelectronics Mapping
- **[EN]**:
  - **Electrostatic Scaling vs. Silicon GAAFET**: Atomically thin 2D channels ($t_b \approx 0.65\text{ nm}$) reduce the electrostatic characteristic length to $\lambda < 1.5\text{ nm}$, breaking through the short-channel scaling floor ($L_g \approx 12\text{ nm}$) of 3D Silicon GAAFET nanosheets ($t_{si} \approx 5\text{ nm}$).
  - **Ohmic Contact vs. Silicide**: While Silicon achieves low contact resistance ($R_c < 20\ \Omega\cdot\mu\text{m}$) via degenerate ion doping and self-aligned silicides (NiSi), 2D semiconductors eliminate Fermi-level pinning via van der Waals or semi-metal (Bi/Sb) interfaces without high-energy lattice damage.
  - **Monolithic 3D Integration**: Low-temperature processing ($<400^\circ\text{C}$) enables Back-End-of-Line (BEOL) monolithic 3D stacking, bypassing the severe thermal budget constraints ($>900^\circ\text{C}$) of Silicon Front-End-of-Line (FEOL).
- **[CN] 硅基微电子映射与技术对照**:
  - **静电微缩机制 vs. 硅基环栅 (GAAFET)**：单层原子级厚度 ($t_b \approx 0.65\text{ nm}$) 使静电特征长度降至 $\lambda < 1.5\text{ nm}$，突破了硅基纳米片 ($t_{si} \approx 5\text{ nm}$) 因表面粗糙散射和量子限域效应而面临的 12 纳米物理栅长极限。
  - **接触工程 vs. 硅化物 (Salicide)**：传统硅基依靠离子注入退火与自对准硅化物实现极低接触电阻，而二维晶体管依靠范德华无损伤电极与半金属 (Bi/Sb) 能带杂化消除费米能级钉扎。
  - **单片三维集成与热预算**：二维器件低温制备流程 ($<400^\circ\text{C}$) 完美适配后道 (BEOL) 多层单片集成，克服了硅基前道高温掺杂退火对金属布线的热破坏。
- **Mapped Comparisons / 关联对照卡片**:
  - [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet|2D Electrostatic Scaling vs. Silicon FinFET, GAAFET & CFET]]
  - [[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide|2D vdW & Semi-Metal Contacts vs. Silicon Silicide Metallization]]

---

## Knowledge links
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
- [[Knowledge/Research Gaps]]
- [[Knowledge/Concepts/two_dimensional_transistor_scaling]]
- [[Knowledge/Concepts/saturation_current_density_benchmarking]]
- [[Knowledge/Concepts/emerging_fet_benchmarking]]
- [[Knowledge/Concepts/contact_resistance_extraction]]
- [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet]]
- [[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide]]

---

## Key Annotations & Highlights
> [!quote]+ Motivation & Background (p. 43) / 研究背景与动机
> **[EN]**: Atomically thin channels facilitate continued transistor scaling... A FET is an electronic switch in which the conductance of a semiconductor channel between the source and drain electrodes can be switched on and off by a third electrode (gate) that is electrostatically coupled through a thin dielectric layer.
> 
> **[CN]**: 原子级超薄沟道能够助力晶体管的持续微缩... 场效应晶体管（FET）是一种电子开关，其源漏电极之间的半导体沟道导电能力由通过薄介质层静电耦合的栅极开启或关断。
>
> [Open in Zotero](zotero://open-pdf/library/items/JJGAEFUH?page=43&annotation=K5VF3DXU)

> [!tip]+ Core Physics: Characteristic Length $\lambda$ (p. 43-44) / 核心物理：晶体管特征缩放长度
> **[EN]**: $\lambda$ is the transistor characteristic length that ultimately dictates the transistor size:
> $$\lambda = \sqrt{\frac{\varepsilon_b}{\varepsilon_{ox}} t_b t_{ox} + \frac{\varepsilon_b}{2 \varepsilon_{sub}} t_b t_{sub}}$$
> In particular, 2D semiconductors feature a dangling-bond-free surface and little mobility variation with decreasing $t_b$. Retaining high electronic performance at the ultimate $t_b$ limit ($<1\text{ nm}$) enables transistors with sub-10-nm gate length while maintaining sufficiently small subthreshold swing and low leakage.
> 
> **[CN]**: $\lambda$ 是最终决定晶体管最小物理尺寸的特征长度。特别地，二维半导体具有无悬挂键的原子级平整表面，且在体厚度 $t_b$ 降低至极限（$<1\text{ nm}$）时仍能保持优异电学输运，从而在亚 10 纳米栅长下仍能维持极小的亚阈值摆幅与超低漏电流。
>
> [Open in Zotero](zotero://open-pdf/library/items/JJGAEFUH?page=43&annotation=YI2ATJBJ)

> [!warning]+ Limitation & Pitfalls (p. 43) / 关键误区剖析
> **[EN]**: Widely used device parameters (such as carrier mobility and contact resistance) are often misestimated or misinterpreted. In short-channel logic transistors, saturation drive current density $I_{sat}/W$ governed by ballistic carrier velocity is the decisive metric.
> 
> **[CN]**: 广泛使用的器件参数（如场效应迁移率和接触电阻）经常被误估或曲解。在短沟道数字逻辑晶体管中，由弹道载流子注入速度决定的饱和驱动电流密度才是决定性指标。
>
> [Open in Zotero](zotero://open-pdf/library/items/JJGAEFUH?page=43&annotation=3HUEJLI2)
