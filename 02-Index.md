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
> > 💡 **中文导读**：*如何规范报告与基准评估新兴场效应晶体管*
> - 🏛️ **发表刊物**：*Nature Electronics* (`2022`) · **DOI**: [10.1038/s41928-022-00798-8](https://doi.org/10.1038/s41928-022-00798-8) ｜ 👤 **作者团队**：Zhihui Cheng, Chin-Sheng Pang et al.
> - 🧬 **关联理论概念**：`Emerging FET Benchmarking` · `Contact Resistance Extraction`
> - 🎯 **核心科学论点**：建立标准化的器件参数报告清单和统一的基准评估方法论，是消除新兴二维半导体场效应晶体管领域中普遍存在的参数提取歧义（如接触电阻、载流子迁移率、亚阈值摆幅）及虚高宣传性能的关键。
> - 🏷️ **状态评级**：`✅ Summarized (已深度提炼)` ｜ **证据级别**: `Strong`

> [!quote]+ 📄 [[Sources/Papers/2021_Liu_2D-Transistors|Promises and prospects of two-dimensional transistors]]
> > 💡 **中文导读**：*二维晶体管的前景与展望*
> - 🏛️ **发表刊物**：*Nature* (`2021`) · **DOI**: [10.1038/s41586-021-03339-z](https://doi.org/10.1038/s41586-021-03339-z) ｜ 👤 **作者团队**：Yuan Liu, Xidong Duan et al.
> - 🧬 **关联理论概念**：`Two-Dimensional Transistor Scaling` · `Saturation Current Density Benchmarking`
> - 🎯 **核心科学论点**：原子级超薄的二维（2D）半导体提供了终极的静电栅控缩放极限（特征长度 $\lambda \propto \sqrt{t_b t_{ox}}$，沟道厚度 $t_b < 1\text{ nm}$），能够彻底抑制亚 10 纳米晶体管中的短沟道效应。然而，外在载流子迁移率在学术界长期被误解与滥用，**短沟道弹道极限下的开态饱和电流密度 ($I_{on}/W$)** 才是衡量 2D 逻辑晶体管性能的根本基准。
> - 🏷️ **状态评级**：`✅ Summarized (已深度提炼)` ｜ **证据级别**: `Strong`

<!-- END AUTO REGISTRY: PAPERS_CARDS -->

### 📑 文献汇总数据表 (Literature Table)

<!-- BEGIN AUTO REGISTRY: PAPERS -->

| 状态 Status | 引用键 Citekey | 论文标题 Title | 第一作者 First Author | 年份 Year | 期刊/会议 Venue | 关联概念 Concepts |
| :---: | :--- | :--- | :--- | :---: | :--- | :--- |
| `✅ Summarized` | [[Sources/Papers/2022_Cheng_FET-Benchmark|2022_Cheng_FET-Benchmark]] | **How to report and benchmark emerging field-effect transistors** | Zhihui Cheng, Chin-Sheng Pang et al. | 2022 | *Nature Electronics* | `Emerging FET Benchmarking`, `Contact Resistance Extraction` |
| `✅ Summarized` | [[Sources/Papers/2021_Liu_2D-Transistors|2021_Liu_2D-Transistors]] | **Promises and prospects of two-dimensional transistors** | Yuan Liu, Xidong Duan et al. | 2021 | *Nature* | `Two-Dimensional Transistor Scaling`, `Saturation Current Density Benchmarking` |

<!-- END AUTO REGISTRY: PAPERS -->

---

## 🧠 2. 核心知识库与原子概念 (Knowledge & Concepts)

### 🧬 原子概念理论卡片 (Concept Cards)

<!-- BEGIN AUTO REGISTRY: CONCEPTS_CARDS -->

> [!tip]+ 🧬 [[Knowledge/Concepts/contact_resistance_extraction|Contact Resistance Extraction in 2D Transistors]]
> > 💡 **中文概念**：*二维材料晶体管接触电阻提取与去嵌套方法*
> - 🏷️ **概念属性**：`concept` ｜ 📚 **理论基石来源**：[[Sources/Papers/2022_Cheng_FET-Benchmark]]
> - 🎯 **机制定义与物理洞见**：接触电阻 ($R_c$) 是指由于费米能级钉扎、肖特基势垒或隧穿间隙在金属电极与二维半导体接触界面产生的额外寄生电阻。精确提取并扣除 $R_c$ 是准确判断器件性能受限于接触界面还是受限于沟道本征输运的核心前提。
> - 状态：`🔬 Active`

> [!tip]+ 🧬 [[Knowledge/Concepts/emerging_fet_benchmarking|Emerging FET Benchmarking Guidelines]]
> > 💡 **中文概念**：*新兴低维场效应晶体管基准测试指南*
> - 🏷️ **概念属性**：`concept` ｜ 📚 **理论基石来源**：[[Sources/Papers/2022_Cheng_FET-Benchmark]]
> - 🎯 **机制定义与物理洞见**：面向新兴低维场效应晶体管（如单层 $\text{MoS}_2$、碳纳米管、二维半导体）的标准化基准测试与参数提取规范。旨在建立统一的器件参数提取与对比规则，消除学术界选择性报道的问题，实现与硅基先进 CMOS 节点的严谨客观对标。
> - 状态：`🔬 Active`

> [!tip]+ 🧬 [[Knowledge/Concepts/saturation_current_density_benchmarking|Saturation Current Density Benchmarking in Logic Transistors]]
> > 💡 **中文概念**：*逻辑晶体管开态饱和电流密度基准评估*
> - 🏷️ **概念属性**：`concept` ｜ 📚 **理论基石来源**：[[Sources/Papers/2021_Liu_2D-Transistors]]
> - 🎯 **机制定义与物理洞见**：在超短沟道纳米晶体管中，载流子输运从传统扩散漂移机制转变为准弹道注入机制。因此，低场漂移迁移率不再决定逻辑门电路的翻转延迟；在固定供电电压 ($V_{dd}$) 和规定关态漏电流 ($I_{off}$) 条件下的**单位宽度开态饱和电流密度 ($I_{on}/W$)**，才是评价逻辑晶体管性能的最核心客观基准。
> - 状态：`🔬 Active`

> [!tip]+ 🧬 [[Knowledge/Concepts/two_dimensional_transistor_scaling|Two-Dimensional Transistor Scaling and Natural Length]]
> > 💡 **中文概念**：*二维晶体管静电缩放与特征自然长度 $\lambda$*
> - 🏷️ **概念属性**：`concept` ｜ 📚 **理论基石来源**：[[Sources/Papers/2021_Liu_2D-Transistors]]
> - 🎯 **机制定义与物理洞见**：晶体管静电微缩理论指出，在不发生严重短沟道效应（漏极诱导势垒降低 DIBL、阈值电压漂移）的前提下，器件可微缩的最小物理栅长受限于特征自然长度 $\lambda$。原子级单层二维半导体（厚度 $t_b < 1\text{ nm}$ 且表面无悬挂键）能够将 $\lambda$ 压缩至物理极限，从而支持亚 5 纳米乃至 1 纳米物理栅长的晶体管微缩。
> - 状态：`🔬 Active`

<!-- END AUTO REGISTRY: CONCEPTS_CARDS -->

### 📑 概念理论汇总表 (Concepts Table)

<!-- BEGIN AUTO REGISTRY: CONCEPTS -->

| 状态 Status | 概念笔记 Note | 核心概念名称 Concept Title | 类型 Type | 核心来源 Primary Sources | 标签 Tags |
| :---: | :--- | :--- | :---: | :--- | :--- |
| `🔬 Active` | [[Knowledge/Concepts/contact_resistance_extraction|Contact Resistance Extraction in 2D Transistors]] | **Contact Resistance Extraction in 2D Transistors** | `concept` | `2022_Cheng_FET-Benchmark` | - |
| `🔬 Active` | [[Knowledge/Concepts/emerging_fet_benchmarking|Emerging FET Benchmarking Guidelines]] | **Emerging FET Benchmarking Guidelines** | `concept` | `2022_Cheng_FET-Benchmark` | - |
| `🔬 Active` | [[Knowledge/Concepts/saturation_current_density_benchmarking|Saturation Current Density Benchmarking in Logic Transistors]] | **Saturation Current Density Benchmarking in Logic Transistors** | `concept` | `2021_Liu_2D-Transistors` | - |
| `🔬 Active` | [[Knowledge/Concepts/two_dimensional_transistor_scaling|Two-Dimensional Transistor Scaling and Natural Length]] | **Two-Dimensional Transistor Scaling and Natural Length** | `concept` | `2021_Liu_2D-Transistors` | - |

<!-- END AUTO REGISTRY: CONCEPTS -->

---

## 📊 3. 领域综合研究成果 (Synthesis & Lineage)
- 📈 **全景文献综述**：[[Knowledge/Literature Overview|Literature Overview (领域文献全景综述与发展里程碑)]]
- 🌳 **研究方法学树**：[[Knowledge/Method Taxonomy|Method Taxonomy (微观建模与电学参数提取方法分类法)]]
- 🎯 **前沿瓶颈与空白**：[[Knowledge/Research Gaps|Research Gaps (开放学术挑战与优先级矩阵)]]

---

## 📝 4. 论文写作与横向对比 (`Writing/`)
- 📊 **学术对比矩阵**：[[Writing/comparison-matrix|Literature Comparison Matrix (跨文献全景横向对比矩阵)]]
