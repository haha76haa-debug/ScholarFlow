---
type: concept
project: 2d-semiconductors
title: Contact Resistance Extraction in Emerging Transistors
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2022_Cheng_FET-Benchmark]]"
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
tags:
  - type/concept
  - topic/semiconductor
  - method/extraction
  - status/promoted
aliases:
  - TLM
  - Contact Resistance Extraction
  - 接触电阻提取
created: 2026-03-29
updated: 2026-04-18
---

# 🧬 Contact Resistance Extraction / 新兴晶体管接触电阻提取方法学

## Definition
- **[EN]**: Contact resistance ($R_c$) represents the parasitic electrical resistance at the metal-semiconductor interface in field-effect transistors. In scaled sub-10-nm devices, $R_c$ often dominates total device resistance ($R_{tot}$), limiting drive current and switching speed.
- **[CN]**: 接触电阻 ($R_c$) 代表场效应晶体管中金属-半导体界面处的寄生电阻。在亚 10 纳米器件中，$R_c$ 往往占据总电阻 ($R_{tot}$) 的主要部分，成为制约器件驱动电流与开关速度的核心瓶颈。

```
                  ┌─────────────────┐       ┌─────────────────┐
                  │ Source (金属源极)│       │ Drain (金属漏极) │
                  └────────┬────────┘       └────────┬────────┘
                           │ (Rc)                    │ (Rc)
     ══════════════════════╪═════════════════════════╪══════════════════════
     Monolayer 2D Channel  │       Rch = Rsh * L/W   │
     ═══════════════════════════════════════════════════════════════════════
```

---

## Mathematical Extraction Model

The standard Transfer Length Method (TLM) models total resistance as a linear function of channel length ($L_{ch}$):

$$R_{tot} = 2 R_c + \frac{R_{sh}}{W} L_{ch}$$

- $R_{tot}$: Total measured two-probe resistance (总测量电阻)
- $R_c$: Single-contact parasitic resistance (单端接触电阻)
- $R_{sh}$: Sheet resistance of the channel (沟道方块电阻)
- $W$: Channel width (沟道宽度)
- $L_{ch}$: Channel length across test structures (不同测试结构沟道长度)

By plotting $R_{tot}$ versus $L_{ch}$ across at least 4 distinct channel lengths, the y-intercept at $L_{ch} = 0$ yields $2 R_c$, with linear goodness-of-fit criterion $R^2 > 0.99$.

---

## Supporting Evidence
- `EVD-2022_Cheng_FET-Benchmark-02`: Multi-channel TLM with $R^2 > 0.99$ linear fitting is the mandatory extraction standard to avoid two-probe underestimation.
- `EVD-2021_Liu_2D-Transistors-03`: Identifies Fermi-level pinning and van der Waals gap states as primary physical sources of elevated $R_c$ in monolayer $\text{MoS}_2$ and $\text{WSe}_2$.

---

## Related Knowledge & Papers
- [[Sources/Papers/2022_Cheng_FET-Benchmark|Cheng et al. (Nature Electronics 2022)]]
- [[Sources/Papers/2021_Liu_2D-Transistors|Liu et al. (Nature 2021)]]
- [[Knowledge/Concepts/emerging_fet_benchmarking]]
- [[Knowledge/Concepts/saturation_current_density_benchmarking]]
- [[Knowledge/Method Taxonomy]]
