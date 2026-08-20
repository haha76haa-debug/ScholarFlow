---
type: paper
project: 2d-semiconductors
title: How to report and benchmark emerging field-effect transistors
citekey: 2022_Cheng_FET-Benchmark
zotero_key: 3A75B4X9
status: read
source_type: journal article
claim_strength: strong
authors:
  - Rui Cheng
  - Lanlan Feng
  - Xiangfeng Duan
year: 2022
journal: Nature Electronics
doi: 10.1038/s41928-022-00798-8
tags:
  - type/paper
  - topic/semiconductor
  - topic/benchmarking
  - method/standardization
  - status/synthesized
evidence_count: 3
created: 2026-03-29
updated: 2026-04-18
linked_knowledge:
  - "[[Knowledge/Literature Overview]]"
  - "[[Knowledge/Method Taxonomy]]"
  - "[[Knowledge/Research Gaps]]"
  - "[[Knowledge/Concepts/emerging_fet_benchmarking]]"
  - "[[Knowledge/Concepts/contact_resistance_extraction]]"
  - "[[Knowledge/Concepts/saturation_current_density_benchmarking]]"
  - "[[Knowledge/Concepts/two_dimensional_transistor_scaling]]"
---

# 📚 How to report and benchmark emerging field-effect transistors / 新兴场效应晶体管规范评估与标杆测试指南

- **Journal / 期刊**: *Nature Electronics* (2022), Vol. 5, pp. 467–476
- **DOI**: [10.1038/s41928-022-00798-8](https://doi.org/10.1038/s41928-022-00798-8)
- **Citekey**: `2022_Cheng_FET-Benchmark`
- **Zotero URI**: [Open in Zotero](zotero://select/items/@2022_Cheng_FET-Benchmark)

---

## Claim
- **[EN]**: Standardized normalization of drive current to channel width ($I_{on}/W$) at specified $V_{dd}$ and multi-channel TLM contact resistance extraction are required to prevent metric distortion in emerging transistors.
- **[CN]**: 必须在规定工作电压 $V_{dd}$ 下按沟道宽度归一化开态驱动电流 ($I_{on}/W$) 并使用多沟道 TLM 提取接触电阻，以彻底杜绝新兴晶体管性能评估中的指标虚标与失真。

---

## Research question
- **[EN]**: How can the research community eliminate common benchmarking pitfalls (e.g., overestimated mobility and geometry mismatch) when evaluating emerging field-effect transistors?
- **[CN]**: 科研界如何消除新兴场效应晶体管评估中普遍存在的标杆测试陷阱（如迁移率高估与几何尺寸错配）？

---

## Method
- **[EN]**: Development of standard reporting protocols, Transfer Length Method (TLM) linear regression bounds, and multi-parameter benchmark correlation matrices.
- **[CN]**: 制定标准化测试评估协议、传输长度法 (TLM) 线性拟合检验准则与多参数关联对比矩阵。

---

## Evidence
- Evidence ID: EVD-2022_Cheng_FET-Benchmark-01
- Source: [[Sources/Papers/2022_Cheng_FET-Benchmark]]
- Supports: "Saturation current density Ion/W is the universal benchmark metric"
- Detail:
  - **[EN]**: $I_{on}/W$ evaluated at $V_{ds} = V_{dd}$ and $V_{gs} - V_{th} = V_{dd}$ with $I_{on}/I_{off} \ge 10^4$ provides the true metric for logic gate delay.
  - **[CN]**: 在 $V_{ds} = V_{dd}$ 且 $V_{gs} - V_{th} = V_{dd}$（开关比 $\ge 10^4$）条件下提取的 $I_{on}/W$ 反映了真实的逻辑门延迟能力。

- Evidence ID: EVD-2022_Cheng_FET-Benchmark-02
- Source: [[Sources/Papers/2022_Cheng_FET-Benchmark]]
- Supports: "Multi-channel TLM with R2 > 0.99 is the mandatory extraction standard"
- Formula / 核心公式:
  $$R_{tot} = 2 R_c + \frac{R_{sh}}{W} L_{ch}$$
- Detail:
  - **[EN]**: Linear regression across multiple channel lengths ($R^2 > 0.99$) is strictly required to decouple contact resistance $R_c$ from channel sheet resistance $R_{sh}$.
  - **[CN]**: 必须通过多沟道长度线性拟合 ($R^2 > 0.99$) 解耦接触电阻 $R_c$ 与沟道方块电阻 $R_{sh}$。

- Evidence ID: EVD-2022_Cheng_FET-Benchmark-03
- Source: [[Sources/Papers/2022_Cheng_FET-Benchmark]]
- Supports: "Field-effect mobility is unreliable for short-channel ballistic devices"
- Detail:
  - **[EN]**: Contact resistance voltage drops suppress extrinsic transconductance $g_m$, invalidating field-effect mobility equations in scaled nanodevices.
  - **[CN]**: 接触电阻分压压降会抑制外在跨导 $g_m$，使传统场效应迁移率公式在纳米微缩器件中失效。

---

## Strengths
- **Standardization Authority / 规范权威性**: Published in *Nature Electronics* (2022) as the definitive reporting checklist / 发表在 *Nature Electronics* 上的权威评估指南。
- **Actionable Protocol / 可落地协议**: Clear guidelines for $R_c$, $EOT$, and normalized current density benchmarking / 为接触电阻、等效氧化层厚度与归一化电流密度提供了具体标准。

---

## Limitation
- **Interface Variability / 界面离散性**: Contact resistance $R_c$ exhibits sample-to-sample variations across mechanically exfoliated versus synthesized flakes / 机械剥离与人工合成样品的接触电阻仍存在离散性。
- **Sub-0.5nm EOT Instrumentation / 亚纳米介质表征**: Accurate $C-V$ measurements at sub-0.5 nm $EOT$ require specialized high-frequency instrumentation / 亚 0.5 纳米 $EOT$ 下的电容表征依赖高频测试设备。

---

## Direct relevance to repo
- **[EN]**: Serves as the primary methodological standard for data extraction and benchmark matrices throughout the knowledge base.
- **[CN]**: 作为整个知识库数据提取与标杆对比矩阵的核心方法论规范。

---

## Relation to other papers
- **[EN]**: Evaluates and provides benchmark rigor for the scaling claims in [[Sources/Papers/2021_Liu_2D-Transistors|Liu et al. (Nature 2021)]].
- **[CN]**: 为 [[Sources/Papers/2021_Liu_2D-Transistors|Liu et al. (Nature 2021)]] 中的微缩主张提供了严谨的标杆测试与数据校准体系。

---

## Knowledge links
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
- [[Knowledge/Research Gaps]]
- [[Knowledge/Concepts/emerging_fet_benchmarking]]
- [[Knowledge/Concepts/contact_resistance_extraction]]
- [[Knowledge/Concepts/saturation_current_density_benchmarking]]
- [[Knowledge/Concepts/two_dimensional_transistor_scaling]]
- [[Sources/Papers/2021_Liu_2D-Transistors]]
