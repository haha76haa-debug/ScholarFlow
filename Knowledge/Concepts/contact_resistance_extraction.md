---
type: concept
project: zotero_obsidian_kb
title: "Contact Resistance Extraction in 2D Transistors"
slug: contact_resistance_extraction
canvas_visibility: visible
status: active
claim_strength: strong
domain: semiconductor-devices
primary_sources:
  - "[[Sources/Papers/2022_Cheng_FET-Benchmark]]"
canonical_equation: 'R_{total} \cdot W = 2 R_c \cdot W + R_{sh} L_{ch}'
updated: 2026-08-19T08:08:00Z
---

# Contact Resistance Extraction in 2D Transistors
> **中文概念**：二维材料晶体管接触电阻提取与去嵌套方法

---

## Definition
- **[EN]**: Contact resistance ($R_c$) is the parasitic electrical resistance occurring at the metal-semiconductor interface of a 2D material transistor. Accurate de-embedding of $R_c$ is essential to determine whether a device is contact-limited or channel-transport-limited.
- **[CN] 概念定义**：接触电阻 ($R_c$) 是指由于费米能级钉扎、肖特基势垒或隧穿间隙在金属电极与二维半导体接触界面产生的额外寄生电阻。精确提取并扣除 $R_c$ 是准确判断器件性能受限于接触界面还是受限于沟道本征输运的核心前提。

---

## Mathematical Formulation
- **[EN] Transfer Length Method (TLM) Model**:
  $$R_{total} \cdot W = 2 R_c \cdot W + R_{sh} \cdot L_{ch}$$
  Where:
  - $R_{total}$ is the measured two-probe resistance / 实测两探针总电阻 $(\Omega)$
  - $W$ is the channel width / 沟道宽度 $(\mu\text{m})$
  - $R_c \cdot W$ is the width-normalized contact resistance / 归一化接触电阻 $(\Omega \cdot \mu\text{m})$
  - $R_{sh}$ is the 2D sheet resistance / 二维沟道方块电阻 $(\Omega / \square)$
  - $L_{ch}$ is the channel length / 沟道长度 $(\mu\text{m})$
- **[CN] 模型推导**：通过测量一系列具有相同沟道宽度 $W$ 但不同沟道长度 $L_{ch}$ 的器件总电阻，线性拟合截距即为 $2 R_c \cdot W$，斜率即为方阻 $R_{sh}$。

---

## Theoretical Grounding
- **[EN]**: In atom-thin 2D semiconductors like $\text{MoS}_2$ and $\text{WSe}_2$, the lack of out-of-plane dangling bonds and Fermi level pinning at the metal interface often creates a Schottky barrier. Proper extraction requires fixing gate overdrive ($V_{gs} - V_{th}$) and carrier density ($n_{2D}$).
- **[CN] 理论基础**：在如 $\text{MoS}_2$、$\text{WSe}_2$ 等原子级范德华半导体中，缺乏表面悬挂键及界面能带弯曲极易形成肖特基势垒。因此提取 $R_c$ 时必须在固定的栅极过驱动电压 ($V_{gs} - V_{th}$) 与确定的载流子面密度 ($n_{2D}$) 下进行。

---

## Evidence & Empirical Support
- **[EN]**: Standardized extraction protocol formulated in [[Sources/Papers/2022_Cheng_FET-Benchmark#Evidence|Cheng et al. (Nature Electronics 2022)]]. Modern 2D FET benchmarks require $R_c \cdot W < 100\ \Omega \cdot \mu\text{m}$ to approach Silicon FinFET competitive performance.
- **[CN] 实证数据**：[[Sources/Papers/2022_Cheng_FET-Benchmark#Evidence|Cheng et al. (Nature Electronics 2022)]] 确立了该标准提取流程。国际半导体技术路线图 (IRDS) 指出，二维晶体管只有实现 $R_c \cdot W < 100\ \Omega \cdot \mu\text{m}$，才具备对标先进制程硅基 FinFET / GAAFET 的竞争力。

---

## Limitations & Boundary Conditions
- **[EN]**: TLM requires uniform channel quality and identical contact interfaces across multiple devices with varying channel lengths.
- **[CN] 边界条件与局限性**：TLM 依赖于不同沟道长度器件间具有高度一致的材料质量与接触界面均匀性；若单器件差异过大，需结合 Y 函数法或四探针法校准。

---

## Cross-References
- [[Sources/Papers/2022_Cheng_FET-Benchmark]]
- [[Knowledge/Concepts/emerging_fet_benchmarking]]
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
