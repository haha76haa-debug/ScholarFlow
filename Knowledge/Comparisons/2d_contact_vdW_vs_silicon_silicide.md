---
type: comparison
project: 2d-semiconductors
title: 2D vdW & Semi-Metal Contacts vs. Silicon Silicide Metallization
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
  - "[[Sources/Papers/2022_Cheng_FET-Benchmark]]"
silicon_reference_nodes:
  - "Silicon FinFET (7nm/5nm)"
  - "GAAFET Nanosheet (3nm/2nm)"
  - "Angstrom A14/A10 Node"
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
  - method/contact-engineering
  - status/promoted
aliases:
  - 2D Contact vs Silicon Silicide
  - 范德华/半金属接触与硅化物金属化对比
  - vdW Contacts vs Salicide
created: 2026-03-29
updated: 2026-04-18
---

# ⚖️ 2D vdW & Semi-Metal Contacts vs. Silicon Silicide Metallization / 2D 范德华与半金属接触 vs. 硅基自对准硅化物金属化

> **Focus / 核心主题**: Microelectronics engineering comparison between 2D van der Waals/semi-metal low-damage contacts and industrial Silicon self-aligned silicide (Salicide) source/drain metallization.

---

## Executive Overview & Silicon Analogy
- **[EN] Executive Summary**:
  - In silicon CMOS technology, source/drain contact resistance is minimized down to $R_c \approx 15-25\ \Omega\cdot\mu\text{m}$ ($\rho_c \approx 10^{-9}\ \Omega\cdot\text{cm}^2$) using degenerate ion-implantation doping ($N_D > 10^{20}\text{ cm}^{-3}$) followed by self-aligned silicide (Salicide: $\text{NiSi}$, $\text{NiPtSi}$, $\text{TiSi}_2$) formation. This process relies on high-temperature annealing ($900^\circ\text{C}-1050^\circ\text{C}$) to activate dopants and form low-barrier metallurgical junctions.
  - In contrast, 2D transition metal dichalcogenides (TMDs) such as monolayer $\text{MoS}_2$ and $\text{WS}_2$ possess an atomically thin, dangling-bond-free lattice ($t_b \approx 0.65\text{ nm}$) that is destroyed by conventional high-energy ion implantation or high-energy sputtering. Direct evaporation of 3D metals induces severe Fermi-Level Pinning (FLP) with pinning factor $S \approx 0.1$, trapping the Fermi level near the conduction band edge or midgap and imposing large Schottky barrier heights ($\Phi_B > 0.3\text{ eV}$).
  - The paradigm shift for 2D contact engineering is the adoption of van der Waals (vdW) transferred electrodes and semi-metal contacts (such as zero-gap bismuth $\text{Bi}(0001)$ and antimony $\text{Sb}(0112)$). Semi-metal contacts hybridize with the 2D conduction band while suppressing Metal-Induced Gap States (MIGS), achieving an unpinned interface ($S \approx 0.9-1.0$), zero Schottky barrier ($\Phi_{B,n} \approx 0\text{ eV}$), and ultra-low contact resistance $R_c \approx 25-123\ \Omega\cdot\mu\text{m}$, approaching the quantum limit at room temperature without high-temperature damage.
- **[CN] 硅基微电子技术映射与对照总述**:
  - 在传统硅基 CMOS 工艺中，源漏欧姆接触主要依靠高剂量重离子注入掺杂 ($N_D > 10^{20}\text{ cm}^{-3}$) 结合自对准硅化物（Salicide: $\text{NiSi}$, $\text{NiPtSi}$, $\text{TiSi}_2$）反应生成低势垒冶金接触，将接触电阻降低至 $R_c \approx 15-25\ \Omega\cdot\mu\text{m}$（比接触电阻率 $\rho_c \approx 10^{-9}\ \Omega\cdot\text{cm}^2$）。然而该工艺严重依赖前道 $900^\circ\text{C}-1050^\circ\text{C}$ 的高温退火激活。
  - 二维半导体（如单层 $\text{MoS}_2$、$\text{WS}_2$）由于晶格厚度仅为原子级 ($t_b \approx 0.65\text{ nm}$) 且表面无悬挂键，极易被高能离子注入与高能电子束蒸镀破坏。传统三维金属沉积会导致严重的金属诱导间隙态 (MIGS) 与费米能级钉扎效应 (FLP, $S \approx 0.1$)，形成巨大的肖特基势垒 ($\Phi_B > 0.3\text{ eV}$)，使接触电阻飙升至 $10^3-10^5\ \Omega\cdot\mu\text{m}$。
  - 二维接触工程的核心突破在于引入范德华转移电极与半金属（如铋 $\text{Bi}(0001)$、锑 $\text{Sb}(0112)$）能带杂化接触。半金属具有极低的态密度且与二维半导体导带波函数发生轨道杂化，彻底抑制了 MIGS，使钉扎因子恢复至接近理想 Schottky-Mott 极限 ($S \approx 0.9-1.0$)，实现近零肖特基势垒 ($\Phi_{B,n} \approx 0\text{ eV}$) 与 $R_c \approx 25-123\ \Omega\cdot\mu\text{m}$ 的超低接触电阻，无需高温退火即可实现接近量子极限的欧姆接触。

---

## 1. Physical Scaling & Electrostatic Control
- **[EN] Contact Length ($L_c$) Scaling & Transfer Length ($L_T$)**:
  - The total contact resistance normalized to channel width ($W$) is modeled via transmission line theory:
    $$R_c \cdot W = \frac{\rho_c}{L_T} \coth\left(\frac{L_c}{L_T}\right) = \sqrt{\rho_c R_{sh}} \coth\left(\frac{L_c}{L_T}\right)$$
    where the characteristic transfer length $L_T$ is defined as:
    $$L_T = \sqrt{\frac{\rho_c}{R_{sh}}}$$
    with $\rho_c$ being the specific contact resistivity ($\Omega\cdot\text{cm}^2$) and $R_{sh}$ being the channel sheet resistance under the contact ($\Omega/\square$).
  - **Scaling Regimes**:
    1. **Long Contact Regime ($L_c \ge 2.5 L_T$)**: $\coth(L_c/L_T) \to 1$, yielding the lower bound $R_c W \approx \sqrt{\rho_c R_{sh}}$. Current injection occurs primarily within the initial transfer length $L_T$ from the channel edge (current crowding).
    2. **Short Contact Regime ($L_c < L_T$)**: $\coth(L_c/L_T) \approx L_T / L_c$, collapsing contact resistance to $R_c W \approx \frac{\rho_c}{L_c}$. In sub-2nm nodes where contacted poly pitch (CPP) requires $L_c \le 10-12\text{ nm}$, contact resistivity must satisfy $\rho_c \le 10^{-9}\ \Omega\cdot\text{cm}^2$ to prevent catastrophic contact resistance inflation.
  - **Edge Contacts vs. Top vdW Contacts vs. Silicon Raised Source/Drain (RSD)**:
    - *Silicon RSD*: Relies on epitaxially grown raised SiGe/Si source/drain facets to expand the effective physical contact area $A_{eff}$, reducing local current density before reaching the silicide interface.
    - *2D Top vdW Contacts*: Current enters vertically across the vdW gap with area $A = W \cdot L_c$. Because the 2D layer is atomically thin, there is no bulk spreading resistance, but current transfer is limited by interfacial tunneling probability.
    - *2D Edge (1D) Contacts*: Etched 1D edge contacts provide direct covalent bonding with 2D dangling bonds at flake edges, minimizing $L_c$ footprint to the atomic edge ($t_b \approx 0.65\text{ nm}$), though fabrication uniformity and atomic roughness remain critical bottlenecks.
- **[CN] 接触长度微缩与传输长度物理**:
  - 接触电阻随接触长度 $L_c$ 的缩减行为严格遵循传输线模型：当 $L_c \ge 2.5 L_T$ 时，电流汇聚在接触边缘 $L_T$ 范围内，此时 $R_c W \approx \sqrt{\rho_c R_{sh}}$；当 $L_c < L_T$ 时，由于几何尺寸不足以充分注入载流子，接触电阻急剧恶化为 $R_c W \approx \rho_c / L_c$。
  - 在 sub-2nm / A14 节点中，接触长度必须微缩至 $L_c \le 10-12\text{ nm}$，要求二维器件比接触电阻率必须压低至 $\rho_c \le 10^{-9}\ \Omega\cdot\text{cm}^2$。相比硅基通过外延凸起源漏 (Raised Source/Drain, RSD) 扩大接触面积，二维顶接触受范德华界面隧穿限制，而一维边缘接触具备极小的几何占位与共价成键潜力。

---

## 2. Ohmic Contact & Metallization Engineering
- **[EN] Fermi-Level Pinning (FLP), MIGS, and Schottky Barrier Formulation**:
  - **Schottky Barrier Height & Bardeen vs. Schottky-Mott Regimes**:
    $$\Phi_{B,n} = S (\Phi_M - \chi_{2D}) + (1 - S) \left(\frac{E_g}{q} - \Phi_{CNL}\right)$$
    where $\Phi_M$ is the metal work function, $\chi_{2D}$ is the 2D electron affinity, $\Phi_{CNL}$ is the charge neutrality level, and $S$ is the Fermi-level pinning factor:
    $$S = \frac{d\Phi_{B,n}}{d\Phi_M} = \frac{1}{1 + \frac{q^2 D_{it} \delta}{\varepsilon_{it}}}$$
    - For 3D metal / 3D semiconductor junctions: High interface state density $D_{it} > 10^{14}\text{ eV}^{-1}\text{cm}^{-2}$ leads to $S \to 0$ (Bardeen Limit), heavily pinning $E_F$ to $\Phi_{CNL}$ regardless of metal work function.
    - For 2D / Semi-metal Interfaces ($\text{Bi}(0001), \text{Sb}(0112)$): Due to the zero or semi-metallic band overlap and anisotropic Fermi surface, Metal-Induced Gap States (MIGS) decaying into the 2D channel ($q_z = \sqrt{2m^*(E_g - E)}/\hbar$) are strongly suppressed, driving $D_{it} \to 0$ and $S \to 1$ (Schottky-Mott Rule).
  - **Specific Contact Resistivity $\rho_c$ via Thermionic Field Emission (TFE)**:
    $$\rho_c = \left[\frac{A^* \pi q T}{k_B \sin(\pi c_1 k_B T)} \exp\left(-\frac{q\Phi_B}{E_{00}}\right)\right]^{-1}$$
    where characteristic energy $E_{00}$ is defined as:
    $$E_{00} = \frac{q\hbar}{2}\sqrt{\frac{N_D}{m^* \varepsilon_s}}$$
    - *Silicon Salicide*: Leverages massive ion implantation ($N_D > 10^{20}\text{ cm}^{-3}$) to increase $E_{00} > 0.1\text{ eV}$, driving ultrathin Schottky barriers and pure Field Emission (FE tunneling).
    - *2D Semi-Metal Contacts*: Vanishes $\Phi_B \to 0\text{ eV}$ directly, eliminating the need for degenerate electrostatic or chemical doping to achieve $\rho_c \approx 1.1 \times 10^{-9}\ \Omega\cdot\text{cm}^2$.
- **[CN] 费米能级钉扎、MIGS 与肖特基势垒调控机制**:
  - 肖特基势垒高度由钉扎因子 $S = \frac{1}{1 + q^2 D_{it}\delta/\varepsilon_{it}}$ 决定。硅基金属接触受限于高密度界面态 ($S \approx 0.1$)，必须依靠 $N_D > 10^{20}\text{ cm}^{-3}$ 的重掺杂使特征能量 $E_{00}$ 大幅增加，依靠极窄势垒下的场发射 (FE) 隧穿降低接触电阻。
  - 二维半导体通过半金属铋 $\text{Bi}(0001)$ 或锑 $\text{Sb}(0112)$ 能带杂化，从物理上消除间隙态密度 $D_{it}$，使 $S \to 1.0$，直接实现 $\Phi_{B,n} \approx 0\text{ eV}$ 的近理想欧姆接触，无需依赖高能离子注入即可达到 $\rho_c \approx 10^{-9}\ \Omega\cdot\text{cm}^2$。

---

## 3. Gate Dielectric & EOT Scaling
- **[EN] Contact-Dielectric Interplay & Fringe Capacitance**:
  - In nanoscale FETs, the source/drain contact electrode is in close proximity to the gate dielectric stack, generating outer fringe capacitance ($C_{of}$) and inner fringe capacitance ($C_{if}$):
    $$C_{total} = C_{gate-channel} + 2 (C_{of} + C_{if})$$
  - **2D Contact Edge Dielectric Environment**:
    - High-k dielectrics ($\text{HfO}_2$, $\text{ZrO}_2$, $\varepsilon_r \approx 20-25$) deposited near the contact region introduce significant fringe capacitance, which degrades high-frequency cut-off frequency $f_T = \frac{g_m}{2\pi C_{total}}$.
    - Van der Waals dielectrics (e.g., multilayer $\text{h-BN}$, $\varepsilon_r \approx 3.5$) or low-k spacers ($\text{SiOCN}$, $\varepsilon_r \approx 4.0$) are necessary adjacent to semi-metal contacts to suppress parasitic gate-to-drain capacitance ($C_{gd}$) while maintaining Equivalent Oxide Thickness $EOT < 0.6\text{ nm}$ directly under the gate.
  - **Dielectric-Induced Doping**: High-k capping over the contact access region can induce electrostatic charge transfer (n-type doping in $\text{MoS}_2$), reducing extension sheet resistance $R_{ext}$ and lowering total parasitic series resistance.
- **[CN] 栅介质与接触界面电容/静电协同微缩**:
  - 接触电极与高-k 栅介质（$\text{HfO}_2/\text{ZrO}_2$）在纳米间距下的交叠会诱发巨大的边缘寄生电容 ($C_{of}, C_{if}$)，严重恶化器件截止频率 $f_T$。因此在维持栅下 $EOT < 0.6\text{ nm}$ 的同时，必须在接触侧墙区域引入低介电常数间隔层（如 $\text{h-BN}$ 或 $\text{SiOCN}$）。
  - 利用高-k 介质对接触延伸区进行介质电荷调制诱导掺杂，可大幅降低源漏延伸区方阻 $R_{ext}$。

---

## 4. CMOS Integration & Thermal Budget
- **[EN] Thermal Budget & Complementary CMOS Polarity**:
  - **Thermal Budget Constraint**:
    - *Silicon FEOL Salicide*: Requires $T > 900^\circ\text{C}$ for dopant activation (RTP/spike annealing) and $450^\circ\text{C}-550^\circ\text{C}$ for silicide formation ($\text{Ni} + \text{Si} \to \text{NiSi}$). This high thermal budget is strictly confined to Front-End-of-Line (FEOL) and cannot be applied on top of Cu/low-k metal interconnects.
    - *2D vdW / Semi-Metal Metallization*: Evaporation of Bi ($T_{melt} = 271.4^\circ\text{C}$) or low-energy vdW transfer operates at $T \le 200^\circ\text{C}-250^\circ\text{C}$. This low thermal budget allows Monolithic 3D (M3D) Back-End-of-Line (BEOL) logic stacking directly over multi-layer Cu interconnects without melting dielectric layers or inducing copper electromigration.
  - **Complementary CMOS Contact Asymmetry**:
    - *N-type Contact*: Bismuth ($\text{Bi}$) and Antimony ($\text{Sb}$) yield outstanding n-type contact on $\text{MoS}_2$ ($R_c < 100\ \Omega\cdot\mu\text{m}$).
    - *P-type Contact*: Achieving symmetric low-resistance p-type contacts on monolayer $\text{WSe}_2$ or $\text{MoTe}_2$ requires high-work-function metals (e.g., Pt, Pd, $\text{RuO}_2$) or transferred 2D metallic contacts ($\text{NbS}_2$, $\text{TaS}_2$). Fermi-level pinning near the valence band remains more pronounced, representing a key research bottleneck for complementary 2D CMOS logic.
- **[CN] CMOS 量产兼容性与热预算分析**:
  - **热预算优势**：硅基自对准硅化物与离子注入需要前道 $900^\circ\text{C}-1050^\circ\text{C}$ 高温退火，无法在后道金属互连层上方加工。而二维半金属铋（熔点 $271.4^\circ\text{C}$）与范德华电极制备温度全程低于 $250^\circ\text{C}$，完全兼容后道 (BEOL) 单片三维 (M3D) 多层逻辑堆叠热预算 ($< 400^\circ\text{C}$)。
  - **互补极性不对称瓶颈**：N 型 $\text{MoS}_2$ 采用 Bi/Sb 可获得极低接触电阻，但 P 型 $\text{WSe}_2$ 依赖高功函数金属（Pt/Pd/$\text{RuO}_2$）或 2D 金属（$\text{NbS}_2$），目前其接触电阻仍明显高于 N 型器件，是制约 2D 互补逻辑电路的核心技术瓶颈。

---

## 5. IRDS Technology Roadmap Alignment
- **[EN] Alignment with IEEE IRDS Scaling Targets**:
  - The International Roadmap for Devices and Systems (IRDS) specifies aggressive contact milestones for sub-2nm, A14 (1.4nm), A10 (1.0nm), and CFET technology nodes:

| IRDS Parameter Benchmark | IRDS 2nm / A14 Target | IRDS A10 / sub-1nm Target | 2D Semi-Metal Contact Status | Silicon Salicide (NiSi/NiPtSi) |
|---|---|---|---|---|
| **Contact Resistance ($R_c$)** | $\le 40\ \Omega\cdot\mu\text{m}$ | $\le 25\ \Omega\cdot\mu\text{m}$ | **$25-42\ \Omega\cdot\mu\text{m}$** (Bi-MoS2, Lab) | **$18-28\ \Omega\cdot\mu\text{m}$** (Fab Baseline) |
| **Specific Contact Resistivity ($\rho_c$)** | $\le 1.5 \times 10^{-9}\ \Omega\cdot\text{cm}^2$ | $\le 8.0 \times 10^{-10}\ \Omega\cdot\text{cm}^2$ | **$1.1 \times 10^{-9}\ \Omega\cdot\text{cm}^2$** | **$1.0 \times 10^{-9}\ \Omega\cdot\text{cm}^2$** |
| **Contact Physical Length ($L_c$)** | $\le 15\text{ nm}$ | $\le 10\text{ nm}$ | Demonstrations down to $12\text{ nm}$ | $10-15\text{ nm}$ in production GAAFET |
| **Contacted Poly Pitch (CPP)** | $\le 45\text{ nm}$ | $\le 36\text{ nm}$ | Requires lithography optimization | $42-45\text{ nm}$ in 2nm nodes |
| **Max Processing Temperature** | $< 450^\circ\text{C}$ (BEOL) | $< 400^\circ\text{C}$ (BEOL) | **$< 250^\circ\text{C}$ (Compliant)** | $> 900^\circ\text{C}$ (FEOL Only) |

- **[CN] IRDS 国际半导体技术路线图对标**:
  - 国际器件与系统路线图 (IRDS) 明确要求在 A14/A10 及 sub-1nm 节点中，寄生接触电阻必须严格压低至 $R_c \le 25-40\ \Omega\cdot\mu\text{m}$，比接触电阻率达到 $\rho_c \le 10^{-9}\ \Omega\cdot\text{cm}^2$。
  - 目前实验室半金属 Bi 接触 $\text{MoS}_2$ 已经达到 $R_c = 25-42\ \Omega\cdot\mu\text{m}$ 与 $\rho_c = 1.1 \times 10^{-9}\ \Omega\cdot\text{cm}^2$，在单项指标上已完全达到 IRDS A14 节点严苛门槛，且具备硅基所不具备的 $< 250^\circ\text{C}$ 低温后道制造优势。

---

## 6. Electrical Benchmark & Compact Modeling Matrix
- **[EN] Parameter Comparison & Compact Modeling Equations**:
  - **Comprehensive Parameter Matrix**:

| Engineering Metric | Monolayer 2D vdW / Semi-Metal | Silicon Salicide (NiSi / GAAFET) | Status & Physical Assessment |
|---|---|---|---|
| **Contact Resistance ($R_c$)** | $25-123\ \Omega\cdot\mu\text{m}$ | $15-25\ \Omega\cdot\mu\text{m}$ | Approaching silicon fab parity |
| **Specific Resistivity ($\rho_c$)** | $1.1 \times 10^{-9}\ \Omega\cdot\text{cm}^2$ | $1.0 \times 10^{-9}\ \Omega\cdot\text{cm}^2$ | Matches IRDS sub-2nm targets |
| **Schottky Barrier Height ($\Phi_B$)** | $\approx 0.0-0.05\text{ eV}$ (Ohmic) | $0.15-0.35\text{ eV}$ (Thinned by doping) | 2D avoids high doping requirement |
| **Fermi-Level Pinning Factor ($S$)** | $0.85-0.98$ (Unpinned) | $0.05-0.15$ (Strongly pinned) | 2D semi-metal suppresses MIGS |
| **Interface State Density ($D_{it}$)** | $< 10^{11}\text{ eV}^{-1}\text{cm}^{-2}$ | $> 10^{13}\text{ eV}^{-1}\text{cm}^{-2}$ (Native) | vdW interface is pristine |
| **Thermal Processing Window** | $25^\circ\text{C}-250^\circ\text{C}$ | $900^\circ\text{C}-1050^\circ\text{C}$ | 2D enables BEOL monolithic 3D |
| **Drive Current Degradation from $R_c$** | $\approx 10-15\%$ | $\approx 12-20\%$ in sub-2nm nodes | Series resistance dominates logic delay |

  - **Compact Modeling Formulation**:
    - *BSIM-CMG Silicide Resistance Network*:
      $$R_{source} = R_{contact} + R_{extension} + R_{spreading}$$
      where $R_{contact} = \frac{\rho_c}{A_{eff}} + \frac{R_{sh,salicide} L_c}{3 W}$.
    - *2D Landauer-Büttiker Multi-Valley Injection Model*:
      $$I_{ds} = \frac{2 q}{h} M_{modes} \int \mathcal{T}(E) [f_{FD}(E - E_{F,S}) - f_{FD}(E - E_{F,D})] dE$$
      where transmission $\mathcal{T}(E) = \frac{\mathcal{T}_{channel}(E) \cdot \mathcal{T}_{contact}(E)}{1 - [1 - \mathcal{T}_{channel}(E)][1 - \mathcal{T}_{contact}(E)]}$, explicitly coupling contact transmission coefficient $\mathcal{T}_{contact}$ with multi-subband channel injection.
- **[CN] 电学参数基准与紧凑模型矩阵**:
  - 在工业级 SPICE 紧凑模型中，硅基 BSIM-CMG 采用三维扩散与扩展电阻网络；而二维器件紧凑模型必须基于 Landauer-Büttiker 弹道/准弹道多子带输运架构，将接触透射几率 $\mathcal{T}_{contact}$ 与量子电容 $C_Q$ 严密耦合。

---

## References & Evidence Anchors
- **Primary Literature Sources**:
  - [[Sources/Papers/2021_Liu_2D-Transistors|Liu et al. (Nature 2021)]]: "Transistor roadmap beyond CMOS" (DOI: [10.1038/s41586-021-03339-z](https://doi.org/10.1038/s41586-021-03339-z))
  - [[Sources/Papers/2022_Cheng_FET-Benchmark|Cheng et al. (Nature Electronics 2022)]]: "How to report and benchmark emerging field-effect transistors" (DOI: [10.1038/s41928-022-00798-8](https://doi.org/10.1038/s41928-022-00798-8))
- **Evidence Records**:
  - `EVD-2021_Liu_2D-Transistors-02`: Saturation drive current density and contact resistance scaling criteria.
  - `EVD-2021_Liu_2D-Transistors-03`: Parasitic contact resistance $R_c < 100\ \Omega\cdot\mu\text{m}$ milestone and dielectric interface engineering.
  - `EVD-2022_Cheng_FET-Benchmark-01`: Standardized $I_{on}/W$ reporting and contact resistance isolation.
  - `EVD-2022_Cheng_FET-Benchmark-02`: Multi-channel TLM linear regression ($R^2 > 0.99$) extraction methodology.
- **Related Concept Notes**:
  - [[Knowledge/Concepts/contact_resistance_extraction|Contact Resistance Extraction & TLM Methodology]]
  - [[Knowledge/Concepts/emerging_fet_benchmarking|Emerging FET Benchmarking Protocols]]
  - [[Knowledge/Concepts/saturation_current_density_benchmarking|Saturation Current Density Benchmarking]]
  - [[Knowledge/Concepts/two_dimensional_transistor_scaling|Two-Dimensional Transistor Scaling Physics]]
- **Syntheses & Indexes**:
  - [[Knowledge/Literature Overview]]
  - [[Knowledge/Method Taxonomy]]
  - [[Knowledge/Research Gaps]]
  - [[Writing/comparison-matrix]]

