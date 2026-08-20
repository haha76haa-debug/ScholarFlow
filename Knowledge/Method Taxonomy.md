---
type: method-taxonomy
project: zotero_obsidian_kb
title: 'Method Taxonomy: 2D Nanoelectronics & Emerging FET Characterization'
status: active
covered_papers:
- '[[Sources/Papers/2021_Liu_2D-Transistors]]'
- '[[Sources/Papers/2022_Cheng_FET-Benchmark]]'
key_themes:
- semiconductor-methods
- scaling-theory
- contact-resistance-extraction
- mobility-extraction
updated: '2026-08-19 07:31:38+00:00'
---

# Method Taxonomy: 2D Nanoelectronics & Emerging FET Characterization

> [!abstract]+ 📌 方法体系导读 (Methodology Overview)
> - **[EN]**: Hierarchical taxonomy of physical modeling, experimental parameter extraction, and benchmarking methodologies in emerging semiconductor electronics.
> - **[CN] 方法学体系概述**：构建涵盖微观器件物理建模、宏观电学参数提取及学术报告标准化的三层方法学分类树。

---

## Taxonomy Tree
```
低维半导体与新兴场效应晶体管研究方法体系 (2D Nanoelectronics Methodologies)
├── 1. 器件物理与静电微缩建模 (Device Physics & Electrostatic Modeling)
│   ├── 1.1 静电特征自然长度解析推导: λ = √(ε_b/ε_ox · t_b · t_ox) ([[Sources/Papers/2021_Liu_2D-Transistors]])
│   └── 1.2 短沟道弹道注入模型: Ion = q · n_2D · v_inj ([[Knowledge/Concepts/saturation_current_density_benchmarking]])
├── 2. 电学参数精确提取方法 (Electrical Parameter Extraction Protocol)
│   ├── 2.1 接触电阻提取法 (Contact Resistance Extraction)
│   │   ├── 传输线模型法 (Transmission Line Method / TLM) ([[Knowledge/Concepts/contact_resistance_extraction]])
│   │   └── Y 函数法 (Y-Function Method / YFM) ([[Knowledge/Concepts/contact_resistance_extraction]])
│   └── 2.2 载流子迁移率与亚阈值摆幅校准 (Mobility & SS Extraction)
│       ├── 场效应峰值迁移率修正: μ_eff = g_m · L / (W · C_ox · V_ds) ([[Knowledge/Concepts/emerging_fet_benchmarking]])
│       └── 亚阈值摆幅真实提取判据: SS = ∂V_gs / ∂(log10 I_ds) ([[Knowledge/Concepts/emerging_fet_benchmarking]])
└── 3. 材料合成与先进工艺集成 (Materials & Lab-to-Fab Engineering)
    ├── 3.1 范德华无损伤电极转移技术 ([[Sources/Papers/2021_Liu_2D-Transistors]])
    └── 3.2 晶圆级二维单晶薄膜外延生长
```

---

## Comparative Method Matrix
| Method Family | Mathematical Operation | Primary Advantage | Primary Constraint |
|---|---|---|---|
| 传输线模型 (TLM) | $R_{tot} = 2 R_c + \frac{R_{sh}}{W} L_{ch}$ | 经典直观，可同时解离接触电阻 $R_c$ 与薄层电阻 $R_{sh}$ | 要求制造一系列具有不同沟道长度的严格一致器件阵列 |
| Y 函数法 (YFM) | $Y = \frac{I_{ds}}{\sqrt{g_m}} = \sqrt{\frac{W}{L} C_{ox} \mu_0 V_{ds}} (V_{gs} - V_{th})$ | 单个器件即可完成提取，自动消除一阶接触电阻压降影响 | 依赖理想迁移率衰减模型，受严重陷阱电荷干扰时有偏差 |
| 弹道注入模型 (Ballistic Model) | $I_{on} = q \cdot n_{2D} \cdot v_{inj} \cdot \mathcal{T}$ | 准确预测纳米晶体管物理极限，规避漂移迁移率失真 | 需精确测定能带态密度 (DOS) 与界面量子电容 $C_Q$ |

---

## Evolutionary Lineage
- **2021 年**：[[Sources/Papers/2021_Liu_2D-Transistors]] 确立了以**弹道注入速度**与**特征长度 $\lambda$** 为核心的器件物理微缩分析框架。
- **2022 年**：[[Sources/Papers/2022_Cheng_FET-Benchmark]] 针对学术界混乱的参数提取乱象，正式发布了**新兴 FET 实验基准报告清单**，统一了国际提取准则。
