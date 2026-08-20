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
updated: '2026-08-19 07:31:38+00:00'
---

# Literature Overview: 2D Semiconductors & Emerging FET Benchmarking

## Executive Synthesis
- **[EN]**: Systematic literature synthesis across nanoscale semiconductor physics, 2D field-effect transistors, and standardized electrical benchmarking protocols for sub-10nm logic nodes.
- **[CN] 核心综述**：系统梳理低维半导体物理、二维场效应晶体管（2D FETs）微缩理论以及新兴器件标准化电学基准测试规范，构建从底层物理极限探索到标准化器件表征的完整学术脉络。

## Chronological Milestones
| Year | Paper | Key Innovation | Primary Impact |
|---|---|---|---|
| 2021 | [[Sources/Papers/2021_Liu_2D-Transistors|2021_Liu_2D-Transistors]] | 二维晶体管静电缩放理论 ($\lambda < 1.5\text{ nm}$) 与饱和电流密度基准 | 确立亚 10nm 逻辑器件物理极限与开态饱和电流评价标准 |
| 2022 | [[Sources/Papers/2022_Cheng_FET-Benchmark|2022_Cheng_FET-Benchmark]] | 新兴 FET 标准化报告清单与接触电阻提取规范 | 规范学术界参数提取协议，消除虚高宣传误差 |

## Key Paradigms
| Paradigm | Core Hypothesis | Mechanism | Key Limitations | Canonical Papers |
|---|---|---|---|---|
| 二维静电微缩极限 (2D Electrostatic Scaling) | 原子层厚度 $t_b < 1\text{ nm}$ 可消除短沟道效应并支持亚 5nm 栅长 | $\lambda = \sqrt{\frac{\varepsilon_b}{\varepsilon_{ox}} t_b t_{ox}}$ | $L_{ch} < 3\text{ nm}$ 时受限于直接源漏量子隧穿 | [[Sources/Papers/2021_Liu_2D-Transistors]] |
| 短沟道弹道注入基准 (Ballistic Injection Limit) | 纳米逻辑晶体管性能由弹道注入速度决定而非低场漂移迁移率 | $I_{on} = q \cdot n_{2D} \cdot v_{inj}$ | 实际开态电流严重受制于金属接触电阻 $R_c$ | [[Sources/Papers/2021_Liu_2D-Transistors]] |
| 无损伤低阻接触工程 (van der Waals Contact) | 消除金属-半导体费米能级钉扎可实现接近量子极限的极低接触电阻 | $R_c \to \frac{\pi \hbar}{2 q^2 k_F} \approx 25\ \Omega\cdot\mu\text{m}$ | 工业级晶圆制造工艺兼容性与热稳定性 | [[Sources/Papers/2022_Cheng_FET-Benchmark]] |

## Evidence & Benchmark Matrix
| Task / Benchmark | Baseline Metric | Proposed Metric | Delta (\Delta) | Source Note |
|---|---|---|---|---|
| 亚 10nm 晶体管栅控 | 硅基 FinFET 面临严重短沟道漏电 | 单层 2D 沟道保持 $SS \approx 65\text{ mV/dec}$ | 证明超薄体具有终极抗短沟道效应能力 | [[Sources/Papers/2021_Liu_2D-Transistors#Evidence]] |
| 接触电阻 $R_c$ 真实表征 | 忽略沟道压降导致虚高低阻数据 | 采用多沟道 TLM 或 Y 函数法精确解离 | 排除实验接触电阻被低估或错误报告 | [[Sources/Papers/2022_Cheng_FET-Benchmark#Evidence]] |

## Cross-Paper Links
- [[Sources/Papers/2021_Liu_2D-Transistors]]
- [[Sources/Papers/2022_Cheng_FET-Benchmark]]
