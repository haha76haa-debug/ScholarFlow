---
type: literature-synthesis
project: zotero_obsidian_kb
title: 'Literature Overview: 2D Semiconductors & Emerging FET Benchmarking'
status: active
covered_papers:
- '[[Sources/Papers/2021_Liu_2D-Transistors]]'
- '[[Sources/Papers/2022_Cheng_FET-Benchmark]]'
key_themes:
- 2d-materials
- semiconductor-physics
- fet-benchmarking
- contact-resistance
- sub-10nm-scaling
- silicon-analogy
- microelectronics
updated: '2026-08-19 07:31:38+00:00'
---

# Literature Overview: 2D Semiconductors & Emerging FET Benchmarking

## Executive Synthesis
- **[EN]**: As conventional bulk and 3D Silicon transistors (FinFET and GAAFET nanosheets) approach atomic thickness and electrostatic scaling limits (with minimum channel thickness $t_{si} \ge 3-5\text{ nm}$ and physical gate length scaling floor $L_g \ge 12\text{ nm}$), atomically thin two-dimensional (2D) transition metal dichalcogenides (TMDs, e.g., monolayer $\text{MoS}_2$, $\text{WS}_2$, $\text{WSe}_2$) offer the ultimate electrostatic scaling potential. With pristine dangling-bond-free surfaces and sub-nanometer body thickness ($t_b \approx 0.65\text{ nm}$), 2D channels compress the characteristic electrostatic natural length to $\lambda < 1.5\text{ nm}$, fundamentally eliminating short-channel effects (SCE) and drain-induced barrier lowering (DIBL) down to physical gate lengths below $5\text{ nm}$.

Historically, academic literature heavily relied on extrinsic low-field field-effect mobility ($\mu_{FE}$) measured in long-channel devices as the primary figure of merit. However, in nanoscale ballistic logic transistors, drive currents are dictated by the thermal injection velocity ($v_{inj} \approx 10^7\text{ cm/s}$) and quantum capacitance ($C_Q$) rather than low-field drift mobility. Consequently, normalized saturation current density ($I_{sat}/W$ or $I_{on}/W$) at a fixed supply voltage ($V_{dd} = 0.7\text{ V}$) under standardized contact de-embedding has emerged as the true benchmark metric. Breakthroughs in van der Waals (vdW) transferred electrodes and semimetal (e.g., zero-gap $\text{Bi}(0001)$, $\text{Sb}(0112)$) contacts have eliminated metal-induced gap states (MIGS) and Fermi-level pinning, driving contact resistance down to $R_c < 100\ \Omega\cdot\mu\text{m}$ (approaching the quantum limit $\approx 25\ \Omega\cdot\mu\text{m}$). Coupled with low-temperature ($<400^\circ\text{C}$) process compatibility, 2D semiconductors enable Back-End-of-Line (BEOL) monolithic 3D integration and 2D Complementary FET (CFET) architectures, establishing a viable pathway for Angstrom (A14/A10) node logic chips.
- **[CN] 核心综述**：随着传统硅基三维晶体管（FinFET 与 GAAFET 纳米片）在体厚度减薄（$t_{si} \ge 3-5\text{ nm}$）与静电微缩（物理栅长瓶颈 $L_g \ge 12\text{ nm}$）方面逼近物理极限，原子级单层二维半导体（如单层 $\text{MoS}_2$、$\text{WS}_2$、$\text{WSe}_2$）凭借天然无悬挂键的理想晶格表面与亚纳米体厚度（$t_b \approx 0.65\text{ nm}$），将晶体管静电特征自然长度压缩至 $\lambda < 1.5\text{ nm}$，能够在亚 5 纳米乃至 1 纳米物理栅长下彻底消除短沟道效应（SCE）与漏致势垒降低效应（DIBL）。

在器件表征方法学上，学术界早期过度依赖长沟道器件测得的低场场效应迁移率（$\mu_{FE}$），而忽视了纳米尺度下由强纵向电场主导的准弹道输运物理。在先进制程逻辑器件中，决定电路门延迟的核心参数是由载流子热注入初速度（$v_{inj} \approx 10^7\text{ cm/s}$）与量子电容决定的**单位宽度开态饱和电流密度（$I_{on}/W$）**。通过引入范德华转移电极与半金属（如零带隙铋 $\text{Bi}(0001)$、锑 $\text{Sb}(0112)$）能带杂化接触，有效消除了金属诱导间隙态（MIGS）与费米能级钉扎效应，将接触电阻降低至 $R_c < 100\ \Omega\cdot\mu\text{m}$，逼近量子理论极限（$\approx 25\ \Omega\cdot\mu\text{m}$）。结合 $<400^\circ\text{C}$ 的低温制程优势，二维材料为后道（BEOL）单片三维集成与 2D CFET 互补逻辑架构提供了超越硅基物理极限的全新技术路径。

---

## Chronological Milestones
| Year | Paper / Initiative | Key Innovation | Primary Impact |
|---|---|---|---|
| 2021 | [[Sources/Papers/2021_Liu_2D-Transistors|2021_Liu_2D-Transistors]] | 二维晶体管静电缩放理论 ($\lambda < 1.5\text{ nm}$) 与饱和电流密度基准 | 确立亚 10nm 逻辑器件物理极限与开态饱和电流评价标准，破除学术界过度依赖长沟道迁移率的传统误区 |
| 2021 | Shen et al. (Nature 2021) | 铋 $\text{Bi}(0001)$ 半金属能带杂化零肖特基势垒接触 ($R_c < 123\ \Omega\cdot\mu\text{m}$) | 彻底抑制金属诱导间隙态 (MIGS)，使费米能级钉扎因子恢复至 $S \approx 0.96$，突破欧姆接触瓶颈 |
| 2022 | [[Sources/Papers/2022_Cheng_FET-Benchmark|2022_Cheng_FET-Benchmark]] | 新兴 FET 国际标准化报告清单 (Checklist) 与多沟道 TLM 提取规范 | 规范学术界电学参数提取协议 ($R^2 \ge 0.99$)，消除外推误差与选择性报道，统一全球基准散点图 |
| 2023-2026 | Monolithic 3D & 2D CFET Integration | 400°C 低温后道制程与单片三维互补逻辑堆叠技术 (BEOL M3D) | 实现 N/P 对称互补逻辑单元与垂直堆叠 CFET，对标国际路线图 IRDS 2037 / sub-1nm 节点 |

---

## Key Paradigms
| Paradigm | Core Hypothesis | Mechanism / Formula | Key Limitations | Canonical Papers |
|---|---|---|---|---|
| **1. 二维静电微缩极限 (2D Electrostatic Scaling)** | 单层原子级体厚 ($t_b < 1\text{ nm}$) 彻底消除亚表面漏电通路，自然长度 $\lambda < 1.5\text{ nm}$，支撑 $L_g < 5\text{ nm}$。 | $\lambda = \sqrt{\frac{\varepsilon_b}{\varepsilon_{ox}} t_b t_{ox} + \frac{\varepsilon_b}{2\varepsilon_{sub}} t_b t_{sub}}$ | $L_{ch} < 3\text{ nm}$ 时受限于直接源漏量子隧穿漏电 | [[Sources/Papers/2021_Liu_2D-Transistors]] |
| **2. 短沟道弹道注入基准 (Ballistic Injection Limit)** | 纳米逻辑晶体管性能由势垒顶端载流子注入速度与量子电容决定，而非长沟道低场漂移迁移率。 | $I_{on} = q \cdot n_{2D} \cdot v_{inj} \cdot \mathcal{T}$ | 实际开态电流发挥严重受制于金属接触寄生压降与自发热效应 | [[Sources/Papers/2021_Liu_2D-Transistors]] |
| **3. 范德华与半金属低阻接触 (vdW & Semimetal Contacts)** | 消除金属-半导体界面悬挂键损伤与 MIGS 态密度，钉扎因子恢复至 $S \approx 0.9-1.0$，实现近零肖特基势垒。 | $\Phi_{B,n} = S(\Phi_M - \chi_{2D}) + (1-S)(E_g/q - \Phi_{CNL})$ | 工业级晶圆制造中的大面积沉积均一性与接触长度 $L_c < 10\text{ nm}$ 微缩限制 | [[Sources/Papers/2022_Cheng_FET-Benchmark]] |
| **4. 超薄 High-$\kappa$ 介质外延 (High-k Dielectric Integration)** | 克服 2D 表面无悬挂键成核困难，通过超薄氧化种层或 vdW 氟化物实现 $EOT < 0.6\text{ nm}$ 且维持极低界面态。 | $EOT = t_{high-k} \cdot (\varepsilon_{SiO_2} / \varepsilon_{high-k})$ | 界面电荷陷阱诱发栅迟滞与偏压温度不稳定性 (BTI) | [[Sources/Papers/2021_Liu_2D-Transistors]] |
| **5. 低温后道单片三维集成 (BEOL Monolithic 3D)** | 全流程热预算 $<400^\circ\text{C}$，突破硅基前道高温退火限制，可直接在互连金属层上方堆叠多层逻辑与存储。 | 热预算兼容性: $T_{process} \le 350-400^\circ\text{C}$ | 层间垂直互连通孔 (Via) 寄生电阻与大功率多层晶体管散热瓶颈 | [[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide]] |
| **6. 新兴 FET 标准化表征准则 (Standardized Benchmarking)** | 强制披露全套几何参数与测试条件，强制多沟道 TLM 线性拟合 ($R^2 \ge 0.99$)，扣除接触寄生后评估本征指标。 | $R_{tot} \cdot W = 2 R_c \cdot W + R_{sh} \cdot L_{ch}$ | 依赖多器件一致性；单器件需采用 Y 函数法与四探针法交叉校验 | [[Sources/Papers/2022_Cheng_FET-Benchmark]] |

---

## Evidence & Benchmark Matrix
| Task / Benchmark | Baseline Metric | Proposed Metric | Delta (\Delta) | Source Note |
|---|---|---|---|---|
| 亚 10nm 晶体管栅控 | 硅基 FinFET 面临严重短沟道漏电 | 单层 2D 沟道保持 $SS \approx 65\text{ mV/dec}$，$\lambda < 1.5\text{ nm}$ | 证明超薄体具有终极抗短沟道效应能力 | [[Sources/Papers/2021_Liu_2D-Transistors#Evidence]] |
| 短沟道开态饱和电流密度 | 早期文献过度宣传长沟道迁移率 | 弹道注入驱动电流突破 $I_{on}/W > 1.0\text{ mA}/\mu\text{m}$ ($V_{dd}=0.7\text{ V}$) | 确立纳米逻辑芯片级时钟翻转延迟评价标准 | [[Sources/Papers/2021_Liu_2D-Transistors#Evidence]] |
| 接触电阻物理机理与 FLP | 传统 3D 金属沉积导致 $S \approx 0.1$ 强钉扎 | 揭示费米能级钉扎与 vdW 间隙态为 $R_c$ 偏高根因 | 为半金属与范德华接触工程提供理论指导 | [[Sources/Papers/2021_Liu_2D-Transistors#Evidence]] |
| 2D FET 全球文献基准散点图 | 缺乏统一标准导致文献虚高宣传 | 统计全球数百篇单层 $\text{MoS}_2$ 数据，构建 $I_{on}$-$I_{off}$ 与 $R_c$-$n_{2D}$ 包络 | 消除选择性报道，建立国际学术界对标共识 | [[Sources/Papers/2022_Cheng_FET-Benchmark#Evidence]] |
| 接触电阻提取严谨性 | 两探针测量忽略沟道电阻导致数据失真 | 规范采用多长度 TLM ($R^2 \ge 0.99$) 或 Y 函数法精确解离 | 排除实验中人为低估接触电阻的提取伪峰 | [[Sources/Papers/2022_Cheng_FET-Benchmark#Evidence]] |
| 跨技术节点基准电压对标 | 任意偏压测试无法横向比较 | 统一在 $V_{dd} = 0.7\text{ V}$ 条件下对标 IRDS sub-2nm 目标 ($R_c < 100\ \Omega\cdot\mu\text{m}$) | 建立与先进硅基 GAAFET/CFET 节点的严谨横向对标 | [[Sources/Papers/2022_Cheng_FET-Benchmark#Evidence]] |
---

## Silicon CMOS Technology Parallels & Roadmap Mapping
> [!info]+ 📊 硅基微电子技术映射与路线图对标总览 (Silicon Parallels Overview)
> 本知识库建立了二维半导体物理与传统硅基先进制程工艺（FinFET、GAAFET、CFET 与自对准硅化物 Salicide）的深度对照体系：

| Engineering Dimension | 2D Semiconductor Physics | Silicon CMOS Benchmark | Mapped Comparison Card |
|---|---|---|---|
| **1. 物理微缩与静电控制** | 原子级单层体厚 ($t_b \approx 0.65\text{ nm}$)，$\lambda < 1.5\text{ nm}$，支撑 $L_g < 5\text{ nm}$ 物理微缩。 | 纳米片体厚 $t_{si} \ge 3-5\text{ nm}$，量子限域与表面粗糙散射限制物理栅长 $L_g \ge 12\text{ nm}$。 | [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet|2D Scaling vs GAAFET]] |
| **2. 欧姆接触与金属化** | 范德华转移电极与半金属 (Bi/Sb) 能带杂化，消除 MIGS，实现近零势垒与 $R_c < 100\ \Omega\cdot\mu\text{m}$。 | 离子注入掺杂结合自对准硅化物 (NiSi Salicide)，依赖 $>900^\circ\text{C}$ 高温退火激活。 | [[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide|2D Contacts vs Salicide]] |
| **3. 栅介质与 EOT 微缩** | 表面无悬挂键导致 ALD 成核困难，需引入超薄氧化种层或单晶氟化物介质实现 $EOT < 0.6\text{ nm}$。 | 热氧化 $\text{SiO}_2$ 与共形 ALD $\text{HfO}_2$，界面态极低 ($D_{it} < 10^{11}\text{ eV}^{-1}\text{cm}^{-2}$)。 | [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet|2D Scaling vs GAAFET]] |
| **4. CMOS 集成与热预算** | 低温工艺 ($<400^\circ\text{C}$)，天生适用于后道 (BEOL) 单片三维堆叠与互补 2D CFET 集成。 | 前道高温掺杂导致 3D 顺序集成热预算极其紧张，依赖复杂超晶格刻蚀。 | [[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide|2D Contacts vs Salicide]] |
| **5. 国际路线图对标** | $I_{on}/W > 1.0-1.5\text{ mA}/\mu\text{m}$ ($V_{dd}=0.7\text{ V}$)，$SS \le 65\text{ mV/dec}$，对标 IRDS 2037 目标。 | GAAFET 驱动电流高但面临关态漏电失控与短沟道功耗恶化。 | [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet|2D Scaling vs GAAFET]] |
| **6. 紧凑模型与电路仿真** | 弹道输运 + 量子电容 ($C_Q$) + 能带杂化模型，需准确去嵌套接触寄生。 | 漂移-扩散 + 迁移率退化模型 (BSIM-CMG 产业标准紧凑模型)。 | [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet|2D Scaling vs GAAFET]], [[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide|2D Contacts vs Salicide]] |

---

## Cross-Paper Links
- [[Sources/Papers/2021_Liu_2D-Transistors]]
- [[Sources/Papers/2022_Cheng_FET-Benchmark]]
- [[Knowledge/Concepts/two_dimensional_transistor_scaling|Two-Dimensional Transistor Scaling]]
- [[Knowledge/Concepts/saturation_current_density_benchmarking|Saturation Current Density Benchmarking]]
- [[Knowledge/Concepts/emerging_fet_benchmarking|Emerging FET Benchmarking]]
- [[Knowledge/Concepts/contact_resistance_extraction|Contact Resistance Extraction]]
- [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet|2D Electrostatic Scaling vs. Silicon FinFET, GAAFET & CFET]]
- [[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide|2D vdW & Semi-Metal Contacts vs. Silicon Silicide Metallization]]
