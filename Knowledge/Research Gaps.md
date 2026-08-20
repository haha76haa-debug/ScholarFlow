---
type: research-gaps
project: zotero_obsidian_kb
title: 'Research Gaps: 2D Transistor Bottlenecks & Unresolved Challenges'
status: active
covered_papers:
- '[[Sources/Papers/2021_Liu_2D-Transistors]]'
- '[[Sources/Papers/2022_Cheng_FET-Benchmark]]'
key_themes:
- research-gaps
- p-type-2d-fet
- wafer-scale-integration
- unstandardized-benchmarking
updated: '2026-08-19 07:31:38+00:00'
---

# Research Gaps: 2D Transistor Bottlenecks & Unresolved Challenges

> [!abstract]+ 📌 开放瓶颈导读 (Bottlenecks Overview)
> - **[EN]**: Catalog of unresolved physical limits, fabrication hurdles, and benchmarking discrepancies across emerging semiconductors.
> - **[CN] 核心挑战概述**：系统归纳当前器件从实验室走向工业制造所面临的未解物理瓶颈、工艺挑战与测试标准差异。

---

## Gap Catalog

### GAP-01: 互补逻辑所必需的 P 型二维晶体管性能严重滞后 (P-Type 2D FET Performance Gap)
- **[EN]**: While n-type $\text{MoS}_2$ FETs achieve outstanding drive currents ($>1\text{ mA}/\mu\text{m}$), complementary p-type materials (e.g. $\text{WSe}_2$) suffer from high Schottky contact barriers and threshold voltage instability.
- **[CN] 瓶颈描述**：虽然 N 型 $\text{MoS}_2$ 器件开态电流已突破 $1\text{ mA}/\mu\text{m}$，但构建低功耗 CMOS 互补逻辑所必需的 P 型器件由于严重费米能级钉扎和高接触势垒，性能显著落后。
- **Source Context**: [[Sources/Papers/2021_Liu_2D-Transistors]]
- **Evidence Anchor**: EVD-2021_Liu_2D-Transistors-01
- **Open Challenges**: 在同一晶圆上单片集成对称平衡的高性能 N 型与 P 型 2D 晶体管。

### GAP-02: 实验参数提取不规范与虚高指标宣传 (Unstandardized Parameter Extraction & Overestimation)
- **[EN]**: Non-standardized extraction methodologies for contact resistance $R_c$ and extrinsic mobility introduce discrepancies and exaggerated claims.
- **[CN] 瓶颈描述**：接触电阻外推误差与不规范的场效应迁移率提取导致文献中存在器件性能虚高问题。
- **Source Context**: [[Sources/Papers/2022_Cheng_FET-Benchmark]]
- **Evidence Anchor**: EVD-2022_Cheng_FET-Benchmark-01
- **Open Challenges**: 建立跨实验室的国际统一测试标准与自动化参数提取开源校验平台。

---

## Unresolved Theoretical Questions
- 范德华异质结界面态电荷捕获动力学及其对亚阈值摆幅超陡峭开关特性的物理制约。
- 原子级超薄沟道中声子散射与量子电容受限下的弹道饱和电流输运极限精确建模。

---

## Priority Matrix for Future Investigation
| Gap ID | Impact | Feasibility | Priority | Canonical Source |
|---|---|---|---|---|
| GAP-01 | High | Medium | P1 | [[Sources/Papers/2021_Liu_2D-Transistors]] |
| GAP-02 | High | High | P1 | [[Sources/Papers/2022_Cheng_FET-Benchmark]] |
