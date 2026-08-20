---
type: concept
project: 2d-semiconductors
title: Emerging Field-Effect Transistor Benchmarking
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2022_Cheng_FET-Benchmark]]"
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
tags:
  - type/concept
  - topic/semiconductor
  - topic/benchmarking
  - status/promoted
aliases:
  - FET Benchmarking
  - Emerging FET Benchmarking
  - 新兴晶体管标杆测试
created: 2026-03-29
updated: 2026-04-18
---

# 🧬 Emerging Field-Effect Transistor Benchmarking / 新兴场效应晶体管标杆测试规范

## Definition
- **[EN]**: A standardized benchmarking methodology to rigorously evaluate and compare non-silicon logic transistors (2D semiconductors, carbon nanotubes, semiconductor nanowires) against IRDS/ITRS industry standards.
- **[CN]**: 一套用于严格评估和横向对比非硅逻辑晶体管（二维半导体、碳纳米管、半导体纳米线）与国际半导体路线图 (IRDS) 产业标准的规范化标杆测试方法学。

---

## Mathematical Formulation & Criteria

| 指标名称 / Metric | 标准测试条件 / Protocol | 物理意义 / Physical Meaning |
| :--- | :--- | :--- |
| **$I_{on}/W$** | $V_{ds} = V_{dd},\ V_{gs}-V_{th}=V_{dd}$ | 饱和开态驱动电流密度（衡量逻辑门充放电速度） |
| **$I_{on}/I_{off}$** | Over operating voltage window | 开关比（保证逻辑状态鲁棒性与静态漏电抑制，需 $\ge 10^4$） |
| **$SS$ (Subthreshold Swing)** | Minimum & Average over 3 decades | 亚阈值摆幅（衡量栅电极对沟道势垒的静电调控效率） |
| **$R_c$ (Contact Resistance)** | TLM extraction at high carrier density | 接触电阻（衡量界面载流子注入效率） |
| **$EOT$ (Equivalent Oxide Thickness)**| From measured gate capacitance | 栅介质等效氧化层厚度 |

---

## Supporting Evidence
- `EVD-2022_Cheng_FET-Benchmark-01`: Normalization of drive current to channel width at matched supply voltage ($V_{dd}$) is required for honest cross-technology comparison.
- `EVD-2021_Liu_2D-Transistors-02`: Compares 2D channel saturation current targets ($I_{on}/W > 1.0\text{ mA}/\mu\text{m}$) with sub-2nm silicon GAAFET roadmap nodes.

---

## Related Knowledge & Papers
- [[Sources/Papers/2022_Cheng_FET-Benchmark|Cheng et al. (Nature Electronics 2022)]]
- [[Sources/Papers/2021_Liu_2D-Transistors|Liu et al. (Nature 2021)]]
- [[Knowledge/Concepts/saturation_current_density_benchmarking]]
- [[Knowledge/Concepts/contact_resistance_extraction]]
- [[Knowledge/Literature Overview]]
