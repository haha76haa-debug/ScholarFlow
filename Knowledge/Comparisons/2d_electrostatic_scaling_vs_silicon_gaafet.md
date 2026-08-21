---
type: comparison
project: 2d-semiconductors
title: 2D Electrostatic Scaling vs. Silicon FinFET, GAAFET & CFET
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
  - "[[Sources/Papers/2022_Cheng_FET-Benchmark]]"
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
  - method/electrostatic-scaling
  - status/promoted
aliases:
  - 2D Electrostatic Scaling vs Silicon GAAFET
  - 二维半导体静电微缩与硅基环栅对比
  - 2D FET vs GAAFET Scaling
created: 2026-03-29
updated: 2026-04-18
---

# ⚖️ 2D Electrostatic Scaling vs. Silicon FinFET, GAAFET & CFET / 2D 静电微缩机制 vs. 硅基 FinFET、GAAFET 纳米片与互补晶体管 CFET

> **Focus / 核心主题**: Microelectronics engineering comparison between atomically thin 2D semiconductor channels ($t_b \approx 0.65\text{ nm}$) and silicon 3D FinFET, Gate-All-Around (GAAFET) Nanosheet, and Complementary FET (CFET) architectures.

---

## Executive Overview & Silicon Analogy
- **[EN] Executive Summary**:
  - As industrial silicon CMOS scales through FinFET (16nm-5nm) and Gate-All-Around Nanosheet (GAAFET, 3nm-2nm) architectures, electrostatic control is maintained by wrapping the gate dielectric and metal around the silicon body. However, as the silicon nanosheet thickness is thinned below $t_{si} < 3\text{ nm}$, quantum confinement causes bandgap expansion, and surface roughness scattering ($\mu_{sr} \propto t_{si}^6$) severely collapses carrier mobility. Consequently, Silicon GAAFET faces a fundamental physical gate length scaling floor at $L_g \approx 12\text{ nm}$.
  - Transition metal dichalcogenides (TMDs, such as monolayer $\text{MoS}_2$, $\text{WS}_2$, $\text{WSe}_2$) possess an atomically uniform crystal structure with body thickness $t_b \approx 0.65\text{ nm}$ and an absence of out-of-plane dangling bonds. This pristine atomic thickness shortens the electrostatic scale length to $\lambda < 1.5\text{ nm}$, completely suppressing short-channel effects (SCE) and drain-induced barrier lowering (DIBL $< 40\text{ mV/V}$) down to physical gate lengths of sub-5-nm.
  - Furthermore, the planar 2D geometry enables natural Complementary FET (CFET) vertical stacking without requiring complex selective chemical etching of sacrificial silicon-germanium ($\text{SiGe}$) superlattice layers, making 2D FETs the premier channel candidates for Angstrom-era (A14, A10, sub-1nm) logic nodes.
- **[CN] 硅基微电子技术映射与对照总述**:
  - 传统硅基 CMOS 从 FinFET（16nm-5nm）演进至纳米片环栅 GAAFET（3nm-2nm），通过全包围栅极增强静电控制。然而当硅纳米片厚度微缩至 $t_{si} < 3\text{ nm}$ 时，量子限域效应导致能带展宽与有效质量变化，更致命的是表面粗糙度散射导致迁移率呈 6 次方暴跌 ($\mu_{sr} \propto t_{si}^6$)。这构成了硅基 GAAFET 在物理栅长 $L_g \approx 12\text{ nm}$ 的微缩红线。
  - 二维过渡金属硫族化合物（TMDs，如单层 $\text{MoS}_2$、$\text{WS}_2$、$\text{WSe}_2$）具备天然原子级均一厚度 ($t_b \approx 0.65\text{ nm}$) 且表面完全无悬挂键。其超薄体将自然特征静电长度压缩至 $\lambda < 1.5\text{ nm}$，即使在 $L_g < 5\text{ nm}$ 的极限短沟道下依然能完美抑制短沟道效应 (SCE) 与漏致势垒降低效应 (DIBL $< 40\text{ mV/V}$)，亚阈值摆幅逼近玻尔兹曼热力学极限 ($SS \approx 60\text{ mV/dec}$)。
  - 此外，二维材料天然的范德华层状结构极易实现垂直互补晶体管 (CFET) 单片集成，彻底摆脱了硅基纳米片制造中繁复的 $\text{Si}/\text{SiGe}$ 超晶格选择性外延与化学腐蚀工艺，是后摩尔时代埃米级（A14, A10, sub-1nm）逻辑芯片的核心沟道演进方向。

---

## 1. Physical Scaling & Electrostatic Control
- **[EN] Characteristic Scale Length ($\lambda$) & Short-Channel Scaling Equations**:
  - The electrostatic integrity of a field-effect transistor is governed by the natural characteristic scale length $\lambda$. To suppress short-channel effects (SCE) such as threshold voltage roll-off and drain-induced barrier lowering (DIBL), the physical gate length must satisfy the scaling criterion:
    $$L_g \ge (3 \sim 4) \lambda$$
  - **Natural Scale Length Formulations**:
    - *Single-Gate (SG) Planar Architecture*:
      $$\lambda_{SG} = \sqrt{\frac{\varepsilon_b}{\varepsilon_{ox}} t_b t_{ox} + \frac{\varepsilon_b}{2\varepsilon_{sub}} t_b t_{sub}}$$
    - *Double-Gate (DG) Architecture*:
      $$\lambda_{DG} = \sqrt{\frac{\varepsilon_b}{2\varepsilon_{ox}} t_b t_{ox} \left(1 + \frac{\varepsilon_{ox} t_b}{4\varepsilon_b t_{ox}}\right)} \approx \sqrt{\frac{\varepsilon_b}{2\varepsilon_{ox}} t_b t_{ox}}$$
    - *Gate-All-Around (GAA) Cylindrical / Nanosheet Architecture*:
      $$\lambda_{GAA} = \sqrt{\frac{\varepsilon_b}{4\varepsilon_{ox}} t_b t_{ox} \left(1 + \frac{\varepsilon_{ox} t_b}{2\varepsilon_b t_{ox}}\right)} \approx \sqrt{\frac{\varepsilon_b}{4\varepsilon_{ox}} t_b t_{ox}}$$
    where $\varepsilon_b$ is the channel dielectric constant ($\approx 4-7$ for TMDs, $\approx 11.7$ for Si), $\varepsilon_{ox}$ is the gate dielectric constant ($\approx 25$ for $\text{HfO}_2$), $t_b$ is the channel body thickness, and $t_{ox}$ is the physical oxide thickness ($t_{ox} = EOT \cdot \varepsilon_{ox} / \varepsilon_{\text{SiO}_2}$).
  - **Quantitative Scaling Comparison**:
    - *Silicon GAAFET Nanosheet*: $t_{si} \approx 5.0\text{ nm}$, $EOT \approx 0.7\text{ nm}$, $\varepsilon_{si} = 11.7 \implies \lambda_{GAA,Si} \approx 2.85\text{ nm} \implies L_{g,min} \approx 11.4\text{ nm}$.
    - *Monolayer 2D Double-Gate FET*: $t_b = 0.65\text{ nm}$, $EOT \approx 0.6\text{ nm}$, $\varepsilon_{2D} \approx 5.5 \implies \lambda_{DG,2D} \approx 1.05\text{ nm} \implies L_{g,min} \approx 3.2-4.2\text{ nm}$.
  - **Subthreshold Swing ($SS$) and DIBL Formulations**:
    $$SS = \ln(10) \frac{k_B T}{q} \left(1 + \frac{C_{dep} + C_{it}}{C_{ox}}\right) \approx 60\text{ mV/dec} \times \left(1 + \frac{\varepsilon_b t_{ox}}{\varepsilon_{ox} t_b} + \frac{q D_{it}}{C_{ox}}\right)$$
    $$\text{DIBL} = \frac{\Delta V_{th}}{\Delta V_{ds}} \approx 0.80 \frac{\varepsilon_b}{\varepsilon_{ox}} \exp\left(-\frac{\pi L_g}{2\lambda}\right)$$
  - **Quantum Confinement & Mobility Degradation at Sub-3nm**:
    In silicon, thinning the body to $t_{si} < 3\text{ nm}$ splits conduction subbands, shifting $E_g$ by $\Delta E_g \approx \frac{\hbar^2 \pi^2}{2 m^* t_{si}^2}$, while atomic step variations ($\delta t_{si} \approx 1$ monolayer) induce severe interface roughness scattering that degrades mobility as $\mu \propto t_{si}^6$. In contrast, monolayer 2D crystals maintain atomic thickness uniformity across entire wafer domains with zero dangling bonds, preserving high intrinsic room-temperature mobility ($\mu_{int} \approx 50-150\text{ cm}^2/\text{V}\cdot\text{s}$).
- **[CN] 静电特征长度与极限微缩方程对比**:
  - 静电微缩由特征长度 $\lambda$ 决定，要求物理栅长满足 $L_g \ge 3\lambda$。
  - 硅基 GAA 纳米片由于受限于 $t_{si} \approx 5\text{ nm}$，其特征长度 $\lambda \approx 2.85\text{ nm}$，限制了其物理栅长难以突破 11-12 纳米。
  - 单层二维材料厚度仅为 $0.65\text{ nm}$，介电常数较低 ($\varepsilon_b \approx 5.5$)，使 $\lambda_{DG}$ 大幅压低至 $1.05\text{ nm}$，理论上允许物理栅长微缩至 3-4 纳米。
  - 硅在 $t_{si} < 3\text{ nm}$ 时因表面原子级粗糙散射导致迁移率呈 6 次方暴跌 ($\mu \propto t_{si}^6$)，而单层二维材料天然原子级平整无悬挂键，彻底消除了体厚度波动引起的散射机制。

---

## 2. Ohmic Contact & Metallization Engineering
- **[EN] Series Resistance Impact on Electrostatic Scaling**:
  - The intrinsic electrostatic benefits of 2D sub-5nm channels cannot be realized without ultra-low parasitic source/drain series resistance $R_{sd} = 2 R_c$.
  - The extrinsic transconductance $g_{m,ext}$ is degraded by contact resistance according to:
    $$g_{m,ext} = \frac{g_{m,int}}{1 + g_{m,int} R_s + g_{ds,int}(R_s + R_d)}$$
  - The actual voltage drop across the intrinsic channel is reduced to $V_{ds,eff} = V_{ds} - I_{ds}(R_s + R_d)$. When $R_c > 200\ \Omega\cdot\mu\text{m}$, more than $50\%$ of the supply voltage $V_{dd}$ drops across the contacts in the on-state, obscuring the intrinsic ballistic drive current advantage ($I_{on}/W$).
  - Integration of semi-metal contacts ($\text{Bi}(0001)$ or $\text{Sb}(0112)$) reduces $R_c < 50\ \Omega\cdot\mu\text{m}$, allowing the intrinsic ballistic velocity injection $v_{inj} \approx (1.0-1.8) \times 10^7\text{ cm/s}$ to translate directly into record extrinsic drive currents ($I_{on}/W > 1.0\text{ mA}/\mu\text{m}$).
- **[CN] 寄生串联电阻对静电微缩的制约**:
  - 极短沟道下的内在静电优势必须依赖极低的接触寄生电阻 $R_c$。当接触电阻过大时，外在跨导 $g_{m,ext}$ 与有效驱动电压 $V_{ds,eff}$ 将严重受损。半金属接触将 $R_c$ 压低至 $50\ \Omega\cdot\mu\text{m}$ 以下，确保了 2D 晶体管高载流子注入速度转换为实际电学开态电流。

---

## 3. Gate Dielectric & EOT Scaling
- **[EN] Equivalent Oxide Thickness ($EOT$) & Low-$D_{it}$ Interface Integration**:
  - **Sub-0.5nm EOT Requirement**:
    To maintain $SS < 65\text{ mV/dec}$ at $L_g \le 10\text{ nm}$, gate dielectric stacks must scale to $EOT \le 0.6\text{ nm}$, where:
    $$EOT = t_{high-k} \cdot \left(\frac{\varepsilon_{\text{SiO}_2}}{\varepsilon_{high-k}}\right) = t_{high-k} \cdot \left(\frac{3.9}{\varepsilon_{high-k}}\right)$$
  - **2D ALD Nucleation Challenge vs. Silicon Native Oxide**:
    - *Silicon*: Native oxidation forms an atomically smooth $\text{SiO}_2$ interface, upon which Atomic Layer Deposition (ALD) of $\text{HfO}_2$ achieves near-perfect chemisorption with interface trap density $D_{it} < 10^{10}\text{ eV}^{-1}\text{cm}^{-2}$.
    - *2D Semiconductors*: Monolayer TMDs have pristine, chemically inert surfaces devoid of dangling bonds or hydroxyl groups (-OH), causing ALD precursors (such as TDMA-Hf or TMA) to island and form pinholes.
  - **Engineered Dielectric Solutions**:
    1. *Low-Damage Seed Layers*: Ultra-thin evaporated oxidized metal buffers (e.g., $0.5\text{ nm}$ $\text{AlO}_x$ or $\text{Y}_2\text{O}_3$).
    2. *Native 2D Oxides*: Single-crystal native oxide transformation (e.g., $\text{Bi}_2\text{SeO}_5$ or $\text{MoS}_2 \to \text{MoO}_3$).
    3. *Single-Crystal Layered Dielectrics*: Epitaxial hexagonal boron nitride ($\text{h-BN}$, $\varepsilon_r \approx 3.5$) or calcium fluoride ($\text{CaF}_2$, $\varepsilon_r \approx 8.43$) providing defect-free vdW dielectric interfaces with $D_{it} < 10^{11}\text{ eV}^{-1}\text{cm}^{-2}$.
- **[CN] 栅介质成核与等效氧化层厚度 ($EOT$) 微缩**:
  - 在 $L_g \le 10\text{ nm}$ 下维持陡峭亚阈值摆幅必须要求 $EOT \le 0.6\text{ nm}$。
  - 硅基具有优异的原生氧化层 ($\text{SiO}_2$) 作为高-k ALD 沉积缓冲层，界面缺陷态极低 ($D_{it} < 10^{10}\text{ eV}^{-1}\text{cm}^{-2}$)。
  - 二维材料因表面无悬挂键导致前驱体难以化学吸附，容易产生岛状聚集与针孔。目前通过超薄预氧化种子层（$\text{AlO}_x/\text{Y}_2\text{O}_3$）、单晶二维原生氧化物（$\text{Bi}_2\text{SeO}_5$）以及层状单晶介质（$\text{h-BN}/\text{CaF}_2$），已实现 $EOT < 0.6\text{ nm}$ 与 $D_{it} < 10^{11}\text{ eV}^{-1}\text{cm}^{-2}$ 的突破。

---

## 4. CMOS Integration & Thermal Budget
- **[EN] Complementary FET (CFET) Architecture & Monolithic 3D Integration**:
  - **CFET Architecture Comparison**:
    - *Silicon 3D CFET*: Stacks an n-FET nanosheet directly on top of a p-FET nanosheet. Fabricating silicon CFET requires complex multi-layer epitaxial superlattices ($\text{Si}/\text{SiGe}/\text{Si}/\text{SiGe}$), selective isotropic lateral etching of $\text{SiGe}$ with $>150:1$ selectivity, and differential gate work-function metal patterning in ultra-narrow aspect ratio vertical cavities ($< 20\text{ nm}$ vertical spacing).
    - *2D Monolithic CFET*: Naturally stacks an n-type monolayer ($\text{MoS}_2$) above a p-type monolayer ($\text{WSe}_2$) separated by a thin inter-device dielectric ($\text{Al}_2\text{O}_3$ or $\text{h-BN}$) using sequential transfer or low-temperature Chemical Vapor Deposition (CVD). No sacrificial lattice etching is required.
  - **Thermal Budget & BEOL Logic Stacking**:
    - Silicon FEOL requires $900^\circ\text{C}-1050^\circ\text{C}$ dopant activation, which damages underlying metal interconnections.
    - 2D transistor fabrication processes operate at temperatures below $T < 350^\circ\text{C}-400^\circ\text{C}$, fully compatible with Back-End-of-Line (BEOL) logic-on-logic and logic-on-memory 3D integration.
- **[CN] 互补晶体管 (CFET) 架构与单片 3D 集成对比**:
  - 硅基 3D CFET 需通过复杂的 $\text{Si}/\text{SiGe}$ 多层超晶格选择性横向腐蚀与深沟槽功函数金属填充，制造良率面临巨大挑战。
  - 二维材料凭借天然原子层状解理特性，可直接实现 N 型 $\text{MoS}_2$ 与 P 型 $\text{WSe}_2$ 的垂直层叠，无需牺牲层腐蚀。且全流程工艺温度 $< 400^\circ\text{C}$，可无缝集成于后道金属布线上方实现单片三维集成。

---

## 5. IRDS Technology Roadmap Alignment
- **[EN] IEEE IRDS Roadmapping for Beyond-Silicon Scaling**:
  - Benchmarking against IRDS Logic Technology Nodes (2028-2034 horizons):

| Roadmap Specification | IRDS 2.0nm Node (2028) | IRDS A14 Node (2031) | IRDS A10 Node (2034) | 2D Monolayer FET Benchmark |
|---|---|---|---|---|
| **Physical Gate Length ($L_g$)** | $12\text{ nm}$ | $10\text{ nm}$ | $8\text{ nm}$ | **$1-10\text{ nm}$ demonstrated** |
| **Contacted Poly Pitch (CPP)** | $45\text{ nm}$ | $38\text{ nm}$ | $30\text{ nm}$ | Scalable with E-beam/EUV |
| **Subthreshold Swing ($SS$)** | $\le 68\text{ mV/dec}$ | $\le 65\text{ mV/dec}$ | $\le 62\text{ mV/dec}$ | **$60-65\text{ mV/dec}$ (near-limit)** |
| **DIBL** | $\le 55\text{ mV/V}$ | $\le 45\text{ mV/V}$ | $\le 35\text{ mV/V}$ | **$< 30\text{ mV/V}$** |
| **On-State Drive ($I_{on}/W$)** | $1.35\text{ mA}/\mu\text{m}$ | $1.50\text{ mA}/\mu\text{m}$ | $1.65\text{ mA}/\mu\text{m}$ | **$1.0-1.5\text{ mA}/\mu\text{m}$ ($V_{dd}=0.7\text{V}$)** |
| **Supply Voltage ($V_{dd}$)** | $0.70\text{ V}$ | $0.65\text{ V}$ | $0.60\text{ V}$ | Fully functional at $0.5-0.7\text{ V}$ |

- **[CN] IRDS 国际半导体路线图对标**:
  - 在 IRDS A14 及 A10（埃米）节点中，硅基 GAAFET 在 $L_g \le 10\text{ nm}$ 时静电完整性急剧恶化。
  - 二维单层晶体管在 $L_g \le 10\text{ nm}$ 下依旧能保持 $SS \le 65\text{ mV/dec}$ 与 DIBL $< 30\text{ mV/V}$，在驱动电流上已跨越 $1.0\text{ mA}/\mu\text{m}$ 门槛，完全契合 IRDS 对埃米时代逻辑芯片的核心规范。

---

## 6. Electrical Benchmark & Compact Modeling Matrix
- **[EN] Comprehensive Parameter Matrix & Compact Modeling Formulations**:
  - **Full Device Benchmarking Matrix**:

| Performance Metric | Monolayer 2D TMD FET | Silicon FinFET (5nm) | Silicon GAA Nanosheet (2nm) | Industrial Advantage |
|---|---|---|---|---|
| **Body Thickness ($t_b$)** | $0.65\text{ nm}$ | $6-8\text{ nm}$ (Fin width) | $4-5\text{ nm}$ (Sheet thickness) | 2D: $\approx 7\times$ thinner channel |
| **Scale Length ($\lambda$)** | $\approx 1.05\text{ nm}$ | $\approx 4.2\text{ nm}$ | $\approx 2.85\text{ nm}$ | 2D: $< 40\%$ of silicon scale length |
| **Subthreshold Swing ($SS$)** | $60-66\text{ mV/dec}$ | $68-75\text{ mV/dec}$ | $64-70\text{ mV/dec}$ | 2D approaches theoretical Boltzmann limit |
| **DIBL** | $< 35\text{ mV/V}$ | $50-70\text{ mV/V}$ | $40-55\text{ mV/V}$ | 2D suppresses short-channel punchthrough |
| **Effective Mobility ($\mu_{eff}$)** | $40-100\text{ cm}^2/\text{V}\cdot\text{s}$ | $150-250\text{ cm}^2/\text{V}\cdot\text{s}$ | $80-140\text{ cm}^2/\text{V}\cdot\text{s}$ | Silicon higher in bulk, but drops at $t_{si}<3\text{nm}$ |
| **Ballistic Ratio ($I_{ballistic}$)** | $60-80\%$ (at $L_g < 10\text{nm}$) | $40-55\%$ | $50-60\%$ | 2D: High injection velocity in short channel |
| **Gate Leakage Density ($J_g$)** | $< 10^{-4}\text{ A/cm}^2$ | $< 10^{-2}\text{ A/cm}^2$ | $< 10^{-2}\text{ A/cm}^2$ | 2D eliminates pinholes with vdW stacks |

  - **Compact Modeling Formulation Differences**:
    - *BSIM-CMG Model (Silicon Multi-Gate / GAAFET)*:
      Based on 3D Poisson-drift-diffusion theory and continuous surface potential formulation:
      $$I_{ds} = \mu_{eff} \frac{W}{L_g} Q_{inv,avg} V_{ds,eff} \left[1 + \theta (V_{gs} - V_{th})\right]^{-1}$$
      incorporating velocity saturation ($v_{sat} \approx 1 \times 10^7\text{ cm/s}$), mobility degradation models, and 3D quantum mechanical corrections ($\Delta V_{th,QM}$).
    - *2D Landauer-Büttiker Multi-Subband Transport Model*:
      $$I_{ds} = \frac{2 q}{h} \sum_{i} \int_{E_i}^{\infty} \mathcal{T}_i(E) [f_{FD}(E - E_{F,S}) - f_{FD}(E - E_{F,D})] dE$$
      where quantum capacitance $C_Q$ is intrinsically coupled to the 2D density of states ($D_{2D} = \frac{g_v g_s m^*}{2\pi \hbar^2}$):
      $$C_Q = q^2 \frac{\partial n_{2D}}{\partial \psi_s} = q^2 D_{2D} \left[1 + \exp\left(\frac{E_C - E_F}{k_B T}\right)\right]^{-1}$$
      Total gate capacitance is governed by series combination:
      $$\frac{1}{C_{gate}} = \frac{1}{C_{ox}} + \frac{1}{C_Q} + \frac{1}{C_{it}}$$
      Because $C_Q$ in 2D is comparable to $C_{ox}$ at sub-0.5nm EOT, quantum capacitance limits channel charge accumulation, a crucial effect not captured by classical bulk BSIM models.
- **[CN] 电学参数基准与紧凑模型矩阵**:
  - 硅基 BSIM-CMG 紧凑模型建立在连续表面势与漂移-扩散输运理论之上；
  - 2D 晶体管紧凑模型必须基于 Landauer-Büttiker 弹道多能带输运方程，显式将量子电容 $C_Q = q^2 D_{2D}$ 与绝缘层几何电容 $C_{ox}$ 串联计入全栅电容体系，准确表征量子电容效应引起的沟道电荷饱和行为。

---

## References & Evidence Anchors
- **Primary Literature Sources**:
  - [[Sources/Papers/2021_Liu_2D-Transistors|Liu et al. (Nature 2021)]]: "Transistor roadmap beyond CMOS" (DOI: [10.1038/s41586-021-03339-z](https://doi.org/10.1038/s41586-021-03339-z))
  - [[Sources/Papers/2022_Cheng_FET-Benchmark|Cheng et al. (Nature Electronics 2022)]]: "How to report and benchmark emerging field-effect transistors" (DOI: [10.1038/s41928-022-00798-8](https://doi.org/10.1038/s41928-022-00798-8))
- **Evidence Records**:
  - `EVD-2021_Liu_2D-Transistors-01`: Electrostatic characteristic length formula $\lambda = \sqrt{\frac{\varepsilon_b}{\varepsilon_{ox}} t_b t_{ox} + \frac{\varepsilon_b}{2\varepsilon_{sub}} t_b t_{sub}}$ and SCE suppression.
  - `EVD-2021_Liu_2D-Transistors-02`: Ballistic saturation current density $I_{on}/W > 1.0\text{ mA}/\mu\text{m}$ at $V_{dd} = 0.7\text{ V}$.
  - `EVD-2022_Cheng_FET-Benchmark-01`: Saturation current density normalization protocol under matched overdrive voltage.
  - `EVD-2022_Cheng_FET-Benchmark-03`: Extrinsic transconductance degradation and field-effect mobility invalidation in short-channel devices.
- **Related Concept Notes**:
  - [[Knowledge/Concepts/two_dimensional_transistor_scaling|Two-Dimensional Transistor Scaling Physics]]
  - [[Knowledge/Concepts/emerging_fet_benchmarking|Emerging FET Benchmarking Protocols]]
  - [[Knowledge/Concepts/saturation_current_density_benchmarking|Saturation Current Density Benchmarking]]
  - [[Knowledge/Concepts/contact_resistance_extraction|Contact Resistance Extraction & TLM Methodology]]
- **Syntheses & Indexes**:
  - [[Knowledge/Literature Overview]]
  - [[Knowledge/Method Taxonomy]]
  - [[Knowledge/Research Gaps]]
  - [[Writing/comparison-matrix]]

