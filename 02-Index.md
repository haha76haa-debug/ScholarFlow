---
type: index
project: zotero_obsidian_kb
title: "Master Knowledge Index & Global MOC"
updated: 2026-08-20T13:10:00Z
---

# 🌐 全局知识索引与内容总览 (Master Knowledge Hub & Index)

> [!abstract]+ 📊 知识库实时全景看板 (Knowledge Base Dashboard)
> | 📚 核心收录文献 | 🧬 提炼原子概念 | 🌳 方法学分类体系 | 🎯 开放研究空白 | 🗺️ 交互知识图谱 |
> | :---: | :---: | :---: | :---: | :---: |
> | **2 篇** | **4 个** | **3 大类** | **2 项** | 👉 [[Maps/literature.canvas|打开交互画布]] |
>
> 🧭 **快捷导航**：[[00-Hub|项目总览 (Hub)]] ｜ [[01-Plan|研究规划 (Plan)]] ｜ [[Writing/comparison-matrix|跨文献横向对比矩阵]] ｜ [[_system/registry|底层元数据注册表]]

---

## 📚 1. 核心收录文献库 (Literature Registry & Cards)

### 🗂️ 核心文献全景卡片 (Literature Cards)

<!-- BEGIN AUTO REGISTRY: PAPERS_CARDS -->

> [!quote]+ 📄 [[Sources/Papers/2022_Cheng_FET-Benchmark|How to report and benchmark emerging field-effect transistors]]
> - 🏛️ **发表刊物**：** (`2022`) · **DOI**: [10.1038/s41928-022-00798-8](https://doi.org/10.1038/s41928-022-00798-8) ｜ 👤 **作者团队**：Rui Cheng, Lanlan Feng et al.
> - 🧬 **关联理论概念**：-
> - 🎯 **核心科学论点**：必须在规定工作电压 $V_{dd}$ 下按沟道宽度归一化开态驱动电流 ($I_{on}/W$) 并使用多沟道 TLM 提取接触电阻，以彻底杜绝新兴晶体管性能评估中的指标虚标与失真。
> - 🏷️ **状态评级**：`✅ Summarized (已深度提炼)` ｜ **证据级别**: `Strong`

> [!quote]+ 📄 [[Sources/Papers/2021_Liu_2D-Transistors|Transistor roadmap beyond CMOS]]
> - 🏛️ **发表刊物**：** (`2021`) · **DOI**: [10.1038/s41586-021-03339-z](https://doi.org/10.1038/s41586-021-03339-z) ｜ 👤 **作者团队**：Yuxiang Liu, Xiangfeng Duan et al.
> - 🧬 **关联理论概念**：-
> - 🎯 **核心科学论点**：单层二维 (2D) 半导体在 10 纳米以下物理栅长下具有无与伦比的静电调控能力，从物理底层突破了 3D 硅基环栅 (GAAFET) 架构的微缩极限。
> - 🏷️ **状态评级**：`✅ Summarized (已深度提炼)` ｜ **证据级别**: `Strong`

<!-- END AUTO REGISTRY: PAPERS_CARDS -->

### 📑 文献汇总数据表 (Literature Table)

<!-- BEGIN AUTO REGISTRY: PAPERS -->

| 状态 Status | 引用键 Citekey | 论文标题 Title | 第一作者 First Author | 年份 Year | 期刊/会议 Venue | 关联概念 Concepts |
| :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| `✅ Read` | [[Sources/Papers/2022_Cheng_FET-Benchmark|2022_Cheng_FET-Benchmark]] | **How to report and benchmark emerging field-effect transistors** | Rui Cheng, Lanlan Feng et al. | 2022 | ** | - |
| `✅ Read` | [[Sources/Papers/2021_Liu_2D-Transistors|2021_Liu_2D-Transistors]] | **Transistor roadmap beyond CMOS** | Yuxiang Liu, Xiangfeng Duan et al. | 2021 | ** | - |

<!-- END AUTO REGISTRY: PAPERS -->

---

## 🧠 2. 核心知识库与原子概念 (Knowledge & Concepts)

### 🧬 原子概念理论卡片 (Concept Cards)

<!-- BEGIN AUTO REGISTRY: CONCEPTS_CARDS -->

> [!tip]+ 🧬 [[Knowledge/Concepts/contact_resistance_extraction|Contact Resistance Extraction in Emerging Transistors]]
> - 🏷️ **概念属性**：`concept` ｜ 📚 **理论基石来源**：[[Sources/Papers/2022_Cheng_FET-Benchmark]], [[Sources/Papers/2021_Liu_2D-Transistors]]
> - 🎯 **机制定义与物理洞见**：接触电阻 ($R_c$) 代表场效应晶体管中金属-半导体界面处的寄生电阻。在亚 10 纳米器件中，$R_c$ 往往占据总电阻 ($R_{tot}$) 的主要部分，成为制约器件驱动电流与开关速度的核心瓶颈。
> - 状态：`🔬 Active`

> [!tip]+ 🧬 [[Knowledge/Concepts/emerging_fet_benchmarking|Emerging Field-Effect Transistor Benchmarking]]
> - 🏷️ **概念属性**：`concept` ｜ 📚 **理论基石来源**：[[Sources/Papers/2022_Cheng_FET-Benchmark]], [[Sources/Papers/2021_Liu_2D-Transistors]]
> - 🎯 **机制定义与物理洞见**：一套用于严格评估和横向对比非硅逻辑晶体管（二维半导体、碳纳米管、半导体纳米线）与国际半导体路线图 (IRDS) 产业标准的规范化标杆测试方法学。
> - 状态：`🔬 Active`

> [!tip]+ 🧬 [[Knowledge/Concepts/saturation_current_density_benchmarking|Saturation Current Density Benchmarking]]
> - 🏷️ **概念属性**：`concept` ｜ 📚 **理论基石来源**：[[Sources/Papers/2021_Liu_2D-Transistors]], [[Sources/Papers/2022_Cheng_FET-Benchmark]]
> - 🎯 **机制定义与物理洞见**：饱和电流密度 ($I_{sat}/W$ 或 $I_{on}/W$) 是晶体管在高漏极偏压 ($V_{ds} = V_{dd}$) 与充分栅极过驱动 ($V_{gs} - V_{th} = V_{dd}$) 状态下，按沟道宽度归一化的最大开态驱动电流。
> - 状态：`🔬 Active`

> [!tip]+ 🧬 [[Knowledge/Concepts/two_dimensional_transistor_scaling|Two-Dimensional Transistor Scaling Physics]]
> - 🏷️ **概念属性**：`concept` ｜ 📚 **理论基石来源**：[[Sources/Papers/2021_Liu_2D-Transistors]], [[Sources/Papers/2022_Cheng_FET-Benchmark]]
> - 🎯 **机制定义与物理洞见**：阐明原子级厚度的二维半导体（如单层 $\text{MoS}_2$、$\text{WS}_2$、$\text{WSe}_2$）如何凭借无悬挂键的理想表面与亚纳米体厚度 ($t_b < 1\text{ nm}$)，在极限物理栅长 ($L_g < 10\text{ nm}$) 下彻底抑制短沟道效应 (SCE) 与漏致势垒降低效应 (DIBL)。
> - 状态：`🔬 Active`

<!-- END AUTO REGISTRY: CONCEPTS_CARDS -->

### 📑 概念理论汇总表 (Concepts Table)

<!-- BEGIN AUTO REGISTRY: CONCEPTS -->

| 状态 Status | 概念笔记 Note | 核心概念名称 Concept Title | 类型 Type | 核心来源 Primary Sources | 标签 Tags |
| :---: | :--- | :--- | :---: | :--- | :--- |
| `🔬 Active` | [[Knowledge/Concepts/contact_resistance_extraction|Contact Resistance Extraction in Emerging Transistors]] | **Contact Resistance Extraction in Emerging Transistors** | `concept` | `2022_Cheng_FET-Benchmark`, `2021_Liu_2D-Transistors` | `type/concept` `topic/semiconductor` `method/extraction` |
| `🔬 Active` | [[Knowledge/Concepts/emerging_fet_benchmarking|Emerging Field-Effect Transistor Benchmarking]] | **Emerging Field-Effect Transistor Benchmarking** | `concept` | `2022_Cheng_FET-Benchmark`, `2021_Liu_2D-Transistors` | `type/concept` `topic/semiconductor` `topic/benchmarking` |
| `🔬 Active` | [[Knowledge/Concepts/saturation_current_density_benchmarking|Saturation Current Density Benchmarking]] | **Saturation Current Density Benchmarking** | `concept` | `2021_Liu_2D-Transistors`, `2022_Cheng_FET-Benchmark` | `type/concept` `topic/semiconductor` `topic/benchmarking` |
| `🔬 Active` | [[Knowledge/Concepts/two_dimensional_transistor_scaling|Two-Dimensional Transistor Scaling Physics]] | **Two-Dimensional Transistor Scaling Physics** | `concept` | `2021_Liu_2D-Transistors`, `2022_Cheng_FET-Benchmark` | `type/concept` `topic/semiconductor` `topic/2d-materials` |

<!-- END AUTO REGISTRY: CONCEPTS -->

---

## 📊 3. 领域综合研究成果 (Synthesis & Lineage)
- 📈 **全景文献综述**：[[Knowledge/Literature Overview|Literature Overview (领域文献全景综述与发展里程碑)]]
- 🌳 **研究方法学树**：[[Knowledge/Method Taxonomy|Method Taxonomy (微观建模与电学参数提取方法分类法)]]
- 🎯 **前沿瓶颈与空白**：[[Knowledge/Research Gaps|Research Gaps (开放学术挑战与优先级矩阵)]]

---

## 📝 4. 论文写作与横向对比 (`Writing/`)
- 📊 **学术对比矩阵**：[[Writing/comparison-matrix|Literature Comparison Matrix (跨文献全景横向对比矩阵)]]
