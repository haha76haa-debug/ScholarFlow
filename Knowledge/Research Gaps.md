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
- dielectric-eot-scaling
- contact-length-scaling
- monolithic-3d
updated: '2026-08-19 07:31:38+00:00'
---

# Research Gaps: 2D Transistor Bottlenecks & Unresolved Challenges

> [!abstract]+ 📌 开放瓶颈导读 (Bottlenecks Overview)
> - **[EN]**: Catalog of unresolved physical limits, fabrication hurdles, and benchmarking discrepancies across emerging semiconductors.
> - **[CN] 核心挑战概述**：系统归纳当前器件从实验室走向工业制造所面临的未解物理瓶颈、工艺挑战与测试标准差异。

---

## Gap Catalog

### GAP-01: 互补逻辑所必需的 P 型二维晶体管性能严重滞后 (P-Type 2D FET Performance Gap & CMOS Balance)
- **[EN]**: While n-type $\text{MoS}_2$ FETs consistently achieve outstanding saturation currents ($I_{on}/W > 1.0\text{ mA}/\mu\text{m}$) and low contact resistances ($R_c < 100\ \Omega\cdot\mu\text{m}$), complementary p-type materials (such as $\text{WSe}_2$, $\text{MoTe}_2$, black phosphorus) suffer from severe Fermi-level pinning near the conduction band or midgap, leading to high Schottky barrier heights ($\Phi_{B,p} > 0.4\text{ eV}$), unstable air doping, and drive currents that are 5-10× lower than N-type counterparts.
- **[CN] 瓶颈描述**：在构建超低静态功耗的 CMOS 互补逻辑电路中，对称匹配的高性能 P 型器件不可或缺。虽然 N 型 $\text{MoS}_2$ 晶体管开态电流已突破 $1.0\text{ mA}/\mu\text{m}$，但主流 P 型二维半导体（如 $\text{WSe}_2$、$\text{MoTe}_2$）因金属费米能级深钉扎导致价带接触势垒过高（$\Phi_{B,p} > 0.4\text{ eV}$），且缺乏高浓度稳定的 P 型掺杂工艺，导致 P 型驱动电流与开关速度落后 N 型近一个数量级。
- **Source Context**: [[Sources/Papers/2021_Liu_2D-Transistors]]
- **Evidence Anchor**: `EVD-2021_Liu_2D-Transistors-01`
- **Open Challenges**: 研发与工业 CMOS 兼容的高功函数无损伤电极、表面电荷转移掺杂钝化层，实现在同一 12 英寸晶圆上单片共集成平衡对称的 N/P 型 2D FETs。

### GAP-02: 实验参数提取不规范与外在寄生虚高指标宣传 (Unstandardized Parameter Extraction & Extrinsic Overestimation)
- **[EN]**: Widespread non-standardized reporting across academic literature—such as using two-probe measurements without contact de-embedding, extracting field-effect mobility $\mu_{FE}$ at extreme unphysical gate overdrives, and omitting gate dielectric leakage $I_g$ or sweep-rate-dependent hysteresis—creates severe reporting discrepancies and artificially exaggerated claims.
- **[CN] 瓶颈描述**：低维电子学领域长期缺乏统一的参数报告与测量标准。部分文献在两探针测试下未扣除接触寄生压降便直接报告峰值场效应迁移率 $\mu_{FE}$，或在极高栅压过驱动/严重迟滞下选择性报告最小亚阈值摆幅 $SS_{min}$，导致实验室公布的优异指标无法真实反映芯片逻辑级性能，阻碍了与硅基先进 CMOS 的客观对标。
- **Source Context**: [[Sources/Papers/2022_Cheng_FET-Benchmark]]
- **Evidence Anchor**: `EVD-2022_Cheng_FET-Benchmark-01`
- **Open Challenges**: 全面推广 Cheng et al. 制定的标准化参数自查清单 (Checklist)，强制要求多沟道 TLM 线性拟合 ($R^2 \ge 0.99$) 与统一供电电压 ($V_{dd} = 0.7\text{ V}$) 基准散点包络对标。

### GAP-03: 晶圆级超均匀单晶二维半导体外延生长与无损伤转移 (Wafer-Scale Monolayer Single-Crystal Epitaxy & Uniformity)
- **[EN]**: Transitioning from laboratory-scale exfoliated micro-flakes to 12-inch foundry manufacturing requires wafer-scale continuous monolayer films with uniform thickness, ultra-low intrinsic point defect density ($<10^{11}\text{ cm}^{-2}$), zero grain boundaries, and high mobility retention across the entire wafer surface.
- **[CN] 瓶颈描述**：机械剥离微米级薄片无法满足工业集成电路量产需求。现有晶圆级化学气相沉积（CVD）或金属有机物化学气相沉积（MOCVD）生长的多晶薄膜中，晶界散射、硫空位点缺陷（密度 $>10^{13}\text{ cm}^{-2}$）与厚度波动会导致晶体管器件间阈值电压与驱动电流离散度剧烈失控。
- **Source Context**: [[Sources/Papers/2021_Liu_2D-Transistors]]
- **Evidence Anchor**: `EVD-2021_Liu_2D-Transistors-01`
- **Open Challenges**: 突破 12 英寸蓝宝石/绝缘体上单晶外延定向生长技术，实现无聚合物残留的超洁净、无损伤原子层干法转移或低温直接原位绝缘衬底外延。

### GAP-04: 原子级超薄高质量栅介质沉积与 EOT < 0.6nm 微缩瓶颈 (Sub-0.6nm EOT High-k Dielectric Integration)
- **[EN]**: Due to the pristine, dangling-bond-free van der Waals surface of 2D semiconductors, conventional atomic layer deposition (ALD) precursors ($\text{HfCl}_4$, $\text{TMA}$) suffer from non-uniform island nucleation, leading to pinholes and severe gate leakage. Ozone or plasma surface treatments induce lattice damage and degrade channel mobility.
- **[CN] 瓶颈描述**：单层二维半导体表面缺乏活性悬挂键，常规原子层沉积（ALD）前驱体难以在其表面均匀吸附成核，易形成岛状孤岛导致栅氧化层严重针孔漏电。若采用等离子体或强氧化剂预处理活化，则会破坏原子晶格完整性引发严重界面态（$D_{it} > 10^{13}\text{ eV}^{-1}\text{cm}^{-2}$）与迁移率崩塌。
- **Source Context**: [[Sources/Papers/2021_Liu_2D-Transistors]]
- **Evidence Anchor**: `EVD-2021_Liu_2D-Transistors-03`
- **Open Challenges**: 开发单分子层无损伤氧化种层（Seeding Layer）、超薄单晶二维范德华氟化物（如 $\text{CaF}_2$、$\text{Bi}_2\text{SeO}_5$）及低温高-$k$ 介质共形集成工艺，实现等效氧化层厚度 $EOT < 0.6\text{ nm}$ 且栅漏电 $<1\text{ pA}/\mu\text{m}$。

### GAP-05: 接触长度 ($L_c < 10\text{ nm}$) 极限微缩下的量子隧穿与接触电阻恶化 (Contact Length Scaling & Current Crowding)
- **[EN]**: Under the contacted poly pitch (CPP) scaling rules of sub-2nm/A14 nodes, the source/drain contact length must shrink to $L_c \le 10-12\text{ nm}$. When $L_c$ drops below the transfer length $L_T = \sqrt{\rho_c / R_{sh}}$, contact resistance degrades severely ($R_c W \propto \rho_c / L_c$), necessitating specific contact resistivity $\rho_c \le 10^{-9}\ \Omega\cdot\text{cm}^2$.
- **[CN] 瓶颈描述**：在 sub-2nm 与埃米级先进制程节点中，标准逻辑单元的接触多晶硅栅间距（CPP）要求源漏接触电极长度必须压缩至 $L_c \le 10-12\text{ nm}$。当接触尺寸小于特征传输长度 $L_T$ 时，电流拥挤效应导致接触电阻急剧发散恶化（$R_c W \propto \rho_c / L_c$），要求比接触电阻率必须压低至 $\rho_c \le 10^{-9}\ \Omega\cdot\text{cm}^2$。
- **Source Context**: [[Sources/Papers/2022_Cheng_FET-Benchmark]]
- **Evidence Anchor**: `EVD-2022_Cheng_FET-Benchmark-02`
- **Open Challenges**: 探索一维共价边缘接触、三维环绕接触及半金属合金界面原子重构，在 $L_c < 10\text{ nm}$ 物理极限下保持超低界面隧穿势垒。

### GAP-06: 单片三维 (Monolithic 3D) 后道集成中的层间互连与界面散热瓶颈 (BEOL Monolithic 3D Interconnects & Thermal Dissipation)
- **[EN]**: Monolithic 3D stacking of 2D logic layers in Back-End-of-Line (BEOL) interconnects eliminates long-distance RC wiring delay. However, the poor out-of-plane thermal conductivity of 2D van der Waals interfaces ($\kappa_{\perp} < 1-2\text{ W/m}\cdot\text{K}$) and interlayer dielectric traps trap heat, exacerbating self-heating and localized thermal breakdown.
- **[CN] 瓶颈描述**：利用二维器件 $<400^\circ\text{C}$ 低温制程在芯片后道金属布线层（BEOL）上方单片垂直堆叠多层 2D 逻辑与高密度存储，是突破内存墙与互连延迟的革命性方案。然而范德华层间垂直热导率极低（$\kappa_{\perp} < 1-2\text{ W/m}\cdot\text{K}$），多层堆叠下大电流密度运行会引发极严重的自发热效应（Self-Heating Effect），导致器件温升加剧与早期介质击穿。
- **Source Context**: [[Sources/Papers/2021_Liu_2D-Transistors]]
- **Evidence Anchor**: `EVD-2021_Liu_2D-Transistors-02`
- **Open Challenges**: 研发嵌入式金刚石/石墨烯纳米散热衬底、高垂直导热各向异性界面绝缘材料及三维协同热仿真 PDK 紧凑模型。

---

## Unresolved Theoretical Questions
- **费米能级钉扎物理根因与动态解除机理**：金属-2D 半导体界面范德华相互作用与轨道杂化如何定量改变金属诱导间隙态 (MIGS) 的空间衰减长度与能态密度分布？
- **超薄 2D 沟道中弹道声子散射与量子电容极限**：在亚 5nm 极限物理栅长下，纵向强电场与量子受限态如何协同制约载流子注入初速度 ($v_{inj}$) 与最大导通电流上限？
- **界面电荷捕获动力学与偏压温度不稳定性 (BTI)**：超薄高-$k$ 介质/2D 半导体界面的慢速陷阱与快速界面态在长时间电应力下的退化规律与可靠性物理模型。
- **接触边缘电流拥挤与极限尺寸下的量子界面隧穿**：在接触长度 $L_c < 5	ext{ nm}$ 极限下，顶接触 (Top Contact) 垂直隧穿与边缘接触 (Edge Contact) 水平注入的量子波函数重叠演化与电阻下限。
- **单片三维集成中微观各向异性热输运与声子声子失配**：原子层范德华界面声子边界散射如何定量影响高密度堆叠逻辑芯片的局部热点 (Hotspot) 耗散？

---

## Priority Matrix for Future Investigation
| Gap ID | Impact | Feasibility | Target Timeline | Canonical Source |
|---|---|---|---|---|
| **GAP-01** (P-Type 2D FET) | High | Medium | P1 (1-2 年) | [[Sources/Papers/2021_Liu_2D-Transistors]] |
| **GAP-02** (Standardized Benchmark) | High | High | P1 (即刻) | [[Sources/Papers/2022_Cheng_FET-Benchmark]] |
| **GAP-03** (Wafer-Scale CVD Epitaxy) | High | Medium | P1 (2-3 年) | [[Sources/Papers/2021_Liu_2D-Transistors]] |
| **GAP-04** (Sub-0.6nm EOT Dielectric) | High | Medium | P1 (1-3 年) | [[Sources/Papers/2021_Liu_2D-Transistors]] |
| **GAP-05** (Contact Length Scaling) | High | High | P2 (3-5 年) | [[Sources/Papers/2022_Cheng_FET-Benchmark]] |
| **GAP-06** (Monolithic 3D Thermal) | Medium | High | P2 (3-5 年) | [[Sources/Papers/2021_Liu_2D-Transistors]] |
---

## Strategic Technology Roadmap & Engineering Mitigation Path
> [!tip]+ 🎯 二维半导体器件迈向先进制程量产的三阶段演进路线图 (Strategic Roadmap)

```
2D Semiconductor Industrialization Roadmap (二维半导体产业化演进路线)
├── 阶段一: 实验室物理极限与标准化验证 (1-2 年 / 2026-2027)
│   ├── 全面落实 Cheng et al. 标准化报告 Checklist 与多沟道 TLM 参数提取
│   ├── 攻克高性能 P 型器件接触工程 (Rc < 100 Ω·μm, Ion/W > 500 μA/μm)
│   └── 确立无损伤种子层超薄 High-k ALD 介质沉积工艺 (EOT < 0.8 nm)
├── 阶段二: 晶圆级工艺攻关与后道单片三维集成 (3-5 年 / 2028-2030)
│   ├── 突破 12 英寸晶圆级单晶单层 CVD 外延与超洁净无损干法转移
│   ├── 实现 N/P 对称单片 2D CFET 逻辑单元与标准逻辑库 (Standard Cell)
│   └── 完成 BEOL 后道低温单片三维逻辑堆叠与存储器共集成验证
└── 阶段三: 埃米级节点产业化商业导入 (5-10 年 / 2031-2035+)
    ├── 对标国际路线图 IRDS 2037 / sub-1nm 节点，实现 A14/A10 商业量产
    ├── 接触长度极限微缩至 Lc ≤ 10 nm 且保持 Rc < 40 Ω·μm
    └── 建立完整的二维半导体 EDA PDK 设计工具链与紧凑物理模型 (Compact Modeling)
```
