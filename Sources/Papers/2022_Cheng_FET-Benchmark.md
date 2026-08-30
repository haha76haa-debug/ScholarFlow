---
type: paper
project: zotero_obsidian_kb
title: "How to report and benchmark emerging field-effect transistors"
citekey: 2022_Cheng_FET-Benchmark
zotero_key: "CHENG2022FET"
canvas_visibility: visible
status: summarized
source_type: "journal article"
claim_strength: strong
authors:
  - "Zhihui Cheng"
  - "Chin-Sheng Pang"
  - "Peiqi Wang"
  - "Son T. Le"
  - "Yanqing Wu"
  - "Davood Shahrjerdi"
  - "Iuliana Radu"
  - "Max C. Lemme"
  - "Lian-Mao Peng"
  - "Xiangfeng Duan"
  - "Zhihong Chen"
  - "Joerg Appenzeller"
  - "Steven J. Koester"
  - "Eric Pop"
  - "Aaron D. Franklin"
  - "Curt A. Richter"
year: 2022
venue: "Nature Electronics"
doi: "10.1038/s41928-022-00798-8"
url: "https://doi.org/10.1038/s41928-022-00798-8"
keywords:
  - 2d-materials
  - field-effect-transistors
  - mos2
  - benchmarking
  - contact-resistance
  - nanoelectronics
tags:
  - type/paper
  - topic/semiconductor
  - topic/2d-materials
  - topic/silicon-analogy
  - method/benchmarking
  - status/synthesized
concepts:
  - "Emerging FET Benchmarking"
  - "Contact Resistance Extraction"
methods:
  - "Standardized FET Reporting Checklist"
  - "Transfer Length Method TLM Normalization"
  - "Subthreshold Swing Extraction Protocol"
subfield: semiconductor-devices
related_papers: []
linked_knowledge:
  - "Knowledge/Literature Overview"
  - "Knowledge/Method Taxonomy"
  - "Knowledge/Research Gaps"
  - "Knowledge/Concepts/fet_mosfet_fundamentals"
  - "Knowledge/Concepts/emerging_fet_benchmarking"
  - "Knowledge/Concepts/contact_resistance_extraction"
  - "Knowledge/Concepts/channel_mobility_and_dibl"
  - "Knowledge/Concepts/transconductance_gm_in_fet"
  - "Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide"
  - "Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet"
updated: 2026-08-30T10:55:00Z
---

# How to report and benchmark emerging field-effect transistors
> **中文译名**：如何规范报告与基准评估新兴场效应晶体管

---

## Claim
- **[EN]**: A standardized parameter reporting checklist and uniform benchmarking methodology are essential to eliminate pervasive ambiguities, inconsistent parameter extractions (e.g., contact resistance, mobility, subthreshold swing), and overclaimed performance in emerging 2D semiconductor field-effect transistors.
- **[CN] 核心主张**：建立标准化的器件参数报告清单和统一的基准评估方法论，是消除新兴二维半导体场效应晶体管领域中普遍存在的参数提取歧义（如接触电阻、载流子迁移率、亚阈值摆幅）及虚高宣传性能的关键。

> [!quote] 原文引用 (p. 416)
> "Inconsistent reporting and extraction methods across laboratories have led to confusing benchmarks and misleading comparisons with mainstream silicon technology. Here we provide guidelines and a checklist for reporting and benchmarking FET device parameters, with the aim of facilitating a fair comparison between different devices."

---

## Research question
- **[EN]**: How can the interdisciplinary nanoelectronics research community rigorously report, extract, and compare interdependent device metrics (contact resistance $R_c$, carrier mobility $\mu$, subthreshold swing $SS$, on/off ratio $I_{on}/I_{off}$, and drive current $I_d$) across novel channel materials (e.g., monolayer $\text{MoS}_2$, carbon nanotubes) to enable fair benchmarking against Silicon CMOS standards?
- **[CN] 核心科学问题**：跨物理、材料与微电子的多学科纳米器件研究团队，如何才能严谨、自洽地报告并提取高度耦合的器件参数（接触电阻 $R_c$、载流子迁移率 $\mu$、亚阈值摆幅 $SS$、开关比 $I_{on}/I_{off}$ 与开态驱动电流 $I_d$），从而在新材料（如单层 $\text{MoS}_2$、碳纳米管）与硅基先进 CMOS 之间实现客观公正的横向对比与潜力评估？

---

## Method
- **[EN] Standardized Reporting & Benchmark Protocols**:
  1. **Reporting Checklist**: Defined a mandatory set of device geometry ($L_{ch}, W$), measurement conditions, contact configurations, dielectric equivalent oxide thickness ($\text{EOT}$), gate leakage, and temperature.

> [!quote] 原文引用 — Reporting Checklist (p. 418)
> "To ensure reproducibility, authors should report the device geometry (channel length $L_{ch}$ and width $W$), contact metal stack, equivalent oxide thickness (EOT), gate leakage current $I_g$, temperature, and measurement sweep rate, as well as whether the reported mobility has been corrected for contact resistance."

  2. **Extraction Rigor**: Enforced Transfer Length Method (TLM) or Y-function under specified gate overdrive for contact resistance $R_c$; distinguished field-effect mobility $\mu_{FE}$ from intrinsic effective mobility $\mu_{eff}$; reported both $SS_{min}$ and decade-averaged $SS_{60}$.

> [!quote] 原文引用 — TLM R² Criterion (p. 419)
> "We recommend using at least four different channel lengths and requiring a coefficient of determination $R^2 > 0.99$ for the linear fit to ensure reliable extraction of contact resistance. Two-probe measurements systematically underestimate contact resistance and should not be used as the sole extraction method."

  3. **Canonical Benchmark Envelopes**: Established standardized 2D scatter plots ($I_{on}$ vs. $I_{off}$, $R_c \cdot W$ vs. carrier density $n_{2D}$) across globally published literature.

> [!quote] 原文引用 — Benchmark Envelopes (p. 420)
> "Standardized $I_{on}$–$I_{off}$ scatter plots across all reported 2D FET devices provide a canonical benchmark envelope, enabling direct comparison of novel device reports against the state-of-the-art performance space and IRDS technology targets."

- **[CN] 规范化方法体系**：
  1. **器件报告清单 (Checklist)**：制定必须详尽披露的参数规范，包括沟道长宽 ($L_{ch}, W$)、接触金属叠层、介质等效氧化层厚度 ($\text{EOT}$)、栅极漏电流及测量扫描速率。
  2. **严谨提取规范**：规范使用传输线模型 (TLM) 或 Y 函数在固定栅过驱动电压下提取接触电阻 $R_c$；明确区分外在场效应迁移率 $\mu_{FE}$ 与扣除接触电阻后的本征有效迁移率 $\mu_{eff}$；同时报告最小亚阈值摆幅 $SS_{min}$ 与跨越数个量级的平均摆幅。
  3. **标准基准散点图**：构建统一的性能包络对比图（如 $I_{on}$-$I_{off}$ 曲线、接触电阻随二维载流子浓度 $n_{2D}$ 演化曲线）。


---

## Evidence
```md
Evidence ID: EVD-2022_Cheng_FET-Benchmark-01
Source: [[Sources/Papers/2022_Cheng_FET-Benchmark]]
Source type: journal article
Supports: "Establishes community consensus guidelines and unified benchmark plots for 2D FETs based on comprehensive monolayer MoS2 device surveys / 建立基于单层MoS2器件调研的二维FET国际统一基准规范"
Contradicts: "Common practice of reporting peak extrinsic mobility or subthreshold swing without accounting for contact resistance or gate hysteresis / 忽视接触电阻和栅迟滞直接报告峰值迁移率的片面做法"
Method / dataset / metric: "Monolayer MoS2 FET literature survey / Contact resistance Rc (Ω·μm), Subthreshold swing SS (mV/dec), On-current Ion (μA/μm)"
Limitation: "Guidelines focus primarily on single-device DC electrical metrics rather than complex multi-stage digital circuit benchmarking / 主要针对单器件直流电学特性，未涵盖多级数字电路或高频射频噪声特性"
Project relevance: "Foundational baseline for assessing 2D material device quality, contact engineering, and benchmark validity / 二维材料晶体管质量、接触工程与基准测试的根本性规范文献"
Claim strength: strong
```

```md
Evidence ID: EVD-2022_Cheng_FET-Benchmark-02
Source: [[Sources/Papers/2022_Cheng_FET-Benchmark]]
Source type: journal article
Supports: "Multi-channel TLM with R^2 > 0.99 linear fitting is the mandatory extraction standard to avoid two-probe underestimation of contact resistance / 必须使用 R² > 0.99 的多长度传输线法提取接触电阻以避免两探针低估"
Method / dataset / metric: "TLM across ≥4 channel lengths, contact resistance Rc·W (Ω·μm), R² goodness-of-fit ≥ 0.99"
Project relevance: "Establishes the specific R² ≥ 0.99 criterion and benchmark target Rc·W < 100 Ω·μm required for IRDS competitive performance / 确立 R² ≥ 0.99 判据与 IRDS 竞争目标 Rc·W < 100 Ω·μm"
Claim strength: strong
```

```md
Evidence ID: EVD-2022_Cheng_FET-Benchmark-03
Source: [[Sources/Papers/2022_Cheng_FET-Benchmark]]
Source type: journal article
Supports: "Electrostatic integrity must be preserved alongside low contact resistance for true 2D transistor scaling benefits at Vdd = 0.7 V benchmark conditions / 在 Vdd = 0.7 V 基准条件下电场完整性与低接触电阻必须协同优化"
Method / dataset / metric: "Benchmark conditions: Vdd = 0.7 V, Ion/W > 1.0 mA/μm, Rc·W < 100 Ω·μm against IRDS sub-2nm node targets"
Project relevance: "Ensures that IRDS sub-2nm node target of Ion/W > 1.0 mA/μm at Vdd = 0.7 V is correctly compared with 2D device reports / 确保与 IRDS 亚 2nm 节点目标 Ion/W > 1.0 mA/μm @ Vdd = 0.7 V 的正确基准对标"
Claim strength: strong
```

---

## Strengths
- **Theoretical & Academic Consensus / 理论高度与国际共识**:
  - Co-authored by leading global institutions (NIST, Duke, Stanford, IMEC, RWTH Aachen, PKU).
  - 由全球顶级半导体机构与高校顶尖学者联合署名，具备极高的行业公信力。

> [!quote] 原文引用 — Community Consensus (p. 416)
> "This Perspective is co-authored by researchers from major institutions and provides community-wide guidelines that represent a consensus on the need to standardize the reporting and benchmarking of emerging FET technologies."

- **Empirical Rigor / 实证严密性**:
  - Systematically surveys decades of monolayer $\text{MoS}_2$ transistors to expose common extraction pitfalls.
  - 系统调研了全球发表的单层 $\text{MoS}_2$ 晶体管数据，清晰指出了业界常见的测量误区与伪峰值。

> [!quote] 原文引用 — Mobility Overestimation Survey (p. 417)
> "A survey of published MoS₂ FET data reveals that field-effect mobility values extracted without proper subtraction of contact resistance are systematically overestimated, often by more than an order of magnitude, leading to an artificially optimistic picture of 2D material performance."

- **Actionable Usability / 实用与指导价值**:
  - Provides plug-and-play tables, checklists, and figure styles for experimentalists.
  - 为实验人员提供了可直接套用的标准化表格、自查清单与对比作图模版。

> [!quote] 原文引用 — Checklist Value (p. 418)
> "The checklist provided here is intended to serve as a practical tool for authors, reviewers, and editors to assess whether the key parameters necessary for a fair comparison have been reported."


---

## Limitation
- **DC-Centric Focus / 局限于直流特性**:
  - Primarily addresses DC transfer and output curves; high-frequency RF performance, device-to-device variability, and bias temperature instability (BTI) are briefly discussed.
  - 核心内容集中在直流转移与输出特性，对射频高频性能、器件间均一性偏差及长期偏压温度不稳定性 (BTI) 的讨论相对有限。

> [!quote] 原文引用 — DC Scope Limitation (p. 421)
> "Our proposed benchmarking framework primarily addresses DC electrical characterization. High-frequency performance metrics such as $f_T$ and $f_{max}$, as well as device-to-device variability and reliability metrics including bias temperature instability (BTI), require additional characterization protocols beyond the scope of this work."

- **Circuit-Level Gap / 缺乏芯片级考量**:
  - Does not extend to parasitic interconnect capacitance in multi-gate standard logic cells.
  - 尚未直接延伸到标准逻辑单元库中的互连寄生电容与复杂时序延迟建模。

> [!quote] 原文引用 — Circuit-Level Gap (p. 421)
> "Extension of these guidelines to multi-stage logic circuit benchmarking, including parasitic capacitances of interconnects, fan-out loading, and propagation delay, represents an important future direction for the community."


---

## Direct relevance to repo
- **[EN]**: Serves as the authoritative benchmark baseline and parameter taxonomy standard for all subsequent 2D semiconductor and nanoelectronic papers ingested into this repository.
- **[CN] 本知识库直接应用价值**：作为本知识库中所有半导体器件、二维材料晶体管后续文献评估的黄金标准与方法学分类树根节点。

---

## Relation to other papers
- **[EN]**: Foundational consensus standard guiding experimental extraction and benchmark reporting in all subsequent low-dimensional device research.
- **[CN] 与其他文献的关系**：作为奠基性标准论文，指导后续所有低维场效应晶体管文献在提取接触电阻、有效迁移率与开关特性时的严谨性判别。

---

## Silicon Analogy & Microelectronics Mapping
- **[EN]**:
  - **Standardized Benchmarking vs. Silicon ITRS/IRDS**: The Cheng et al. framework mirrors the IRDS roadmap's mandatory reporting of $I_{on}/W$, $SS$, $EOT$, and $R_c$ for silicon nodes, enabling rigorous cross-technology comparison between 2D FETs and sub-3nm Si GAAFET/CFET nodes.
  - **TLM Contact Extraction vs. Silicon Salicide**: Silicon contact resistance is typically extracted using 4-probe kelvin structures on silicide (NiSi/TiSi). The TLM protocol standardized in this paper provides the equivalent metric for 2D devices, enabling direct $R_c \cdot W$ benchmarking.
  - **CMOS-Compatible Reporting Discipline**: The checklist mandates EOT reporting for gate dielectrics — directly analogous to the silicon process of record (POR) EOT specifications at leading-edge nodes (sub-0.8 nm at 3nm node).
- **[CN] 硅基微电子映射与技术对照**:
  - **标准化基准规范 vs. 硅基 ITRS/IRDS 路线图**：本文建立的规范框架与 IRDS 对先进硅基节点 $I_{on}/W$、$SS$、$EOT$、$R_c$ 的强制披露要求完全对标，实现了二维 FET 与亚 3nm 硅基 GAAFET/CFET 节点的严格跨技术比对。
  - **TLM 接触提取 vs. 硅基自对准硅化物 (Salicide)**：硅基接触电阻通常通过 4 探针 Kelvin 结构对 NiSi/TiSi 进行提取。本文规范化的 TLM 协议为二维器件提供了等效度量，实现直接的 $R_c \cdot W$ 基准对比。
  - **CMOS 工艺兼容报告规范**：清单强制要求报告栅介质 EOT，与先进硅基制程 (sub-0.8 nm at 3nm node) 的 EOT 规范要求完全一致。
- **Mapped Comparisons / 关联对照卡片**:
  - [[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide|2D vdW & Semi-Metal Contacts vs. Silicon Silicide Metallization]]
  - [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet|2D Electrostatic Scaling vs. Silicon FinFET, GAAFET & CFET]]

---

## Knowledge links
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
- [[Knowledge/Research Gaps]]
- [[Knowledge/Concepts/emerging_fet_benchmarking]]
- [[Knowledge/Concepts/contact_resistance_extraction]]
- [[Knowledge/Concepts/channel_mobility_and_dibl]]
- [[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide]]
- [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet]]

---

## Key Annotations & Highlights
> [!quote]+ Motivation & Background (p. 416) / 研究动机与背景
> **[EN]**: Emerging field-effect transistors (FETs) based on low-dimensional materials have attracted tremendous interest for future logic applications. However, inconsistent reporting and extraction methods across laboratories have led to confusing benchmarks and misleading comparisons with mainstream silicon technology.
> 
> **[CN]**: 基于低维材料的新兴场效应晶体管在未来逻辑器件中展现出巨大前景。然而，由于不同实验室间报道标准与参数提取方法的不一致，导致了基准对比混乱以及与主流硅技术的误导性对比。
>
> [Open in Nature Electronics](https://doi.org/10.1038/s41928-022-00798-8)

> [!tip]+ Core Method: The Reporting Checklist (p. 418) / 核心方法：参数自查清单
> **[EN]**: To ensure reproducibility, authors must report: channel length ($L_{ch}$), channel width ($W$), contact metal stack, dielectric equivalent oxide thickness ($\text{EOT}$), gate leakage ($I_g$), measurement sweep rate, and whether mobility was corrected for contact resistance ($R_c$).
> 
> **[CN]**: 为确保实验可重复性，作者必须完整报告：沟道长度 ($L_{ch}$)、沟道宽度 ($W$)、接触金属层结构、栅介质等效氧化层厚度 ($\text{EOT}$)、栅极漏电流 ($I_g$)、电压扫描速度，以及迁移率是否已经经过接触电阻 ($R_c$) 的去嵌套校准。
>
> [Open in Nature Electronics](https://doi.org/10.1038/s41928-022-00798-8)

> [!warning]+ Limitation & Pitfalls (p. 420) / 常见误区与局限性
> **[EN]**: Reporting field-effect mobility $\mu_{FE}$ extracted at high gate overdrive without subtracting contact resistance can overestimate or underestimate intrinsic transport properties by orders of magnitude.
> 
> **[CN]**: 在高栅极过驱动电压下提取场效应迁移率 $\mu_{FE}$ 时，如果不扣除接触电阻的影响，可能会使材料的本征输运性质被高估或低估数个数量级。
>
> [Open in Nature Electronics](https://doi.org/10.1038/s41928-022-00798-8)
