"""
Zotero-Obsidian Academic Knowledge Base - Clean Vault Initializer
Backs up sample papers and concepts into .demo_backup/ and resets the vault to a pristine blank slate.
"""
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# Ensure UTF-8 output encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    vault_root = Path(__file__).resolve().parent.parent
    archive_demo = vault_root / ".demo_backup"
    if archive_demo.exists():
        shutil.rmtree(archive_demo)
    archive_demo.mkdir(parents=True, exist_ok=True)

    print("=" * 70)
    print("[*] Switching to Clean Blank Slate (纯净空白起步模式)")
    print(f"[>] Vault Root: {vault_root}")
    print("=" * 70)

    # 1. Backup demo papers
    papers_dir = vault_root / "Sources" / "Papers"
    demo_papers_dir = archive_demo / "Papers"
    demo_papers_dir.mkdir(parents=True, exist_ok=True)
    if papers_dir.exists():
        for p in papers_dir.glob("*.md"):
            if p.name != "index.md":
                shutil.copy2(p, demo_papers_dir / p.name)
                p.unlink()
                print(f"  [-] Archived paper note: {p.name}")

    # Reset Sources/Papers/index.md
    clean_papers_index = """---
type: index
project: zotero_obsidian_kb
updated: """ + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """
---

# Sources / Papers Index

This directory contains individual literature notes extracted from Zotero.

## Ingested Papers (0)
*No papers ingested yet. Use Zotero Integration plugin (Ctrl+P -> Create Literature Note) or add BibTeX files to start!*
"""
    (papers_dir / "index.md").write_text(clean_papers_index, encoding="utf-8")

    # 2. Backup demo concepts
    concepts_dir = vault_root / "Knowledge" / "Concepts"
    demo_concepts_dir = archive_demo / "Concepts"
    demo_concepts_dir.mkdir(parents=True, exist_ok=True)
    if concepts_dir.exists():
        for c in concepts_dir.glob("*.md"):
            shutil.copy2(c, demo_concepts_dir / c.name)
            c.unlink()
            print(f"  [-] Archived concept note: {c.name}")

    # 3. Backup & reset synthesis notes
    for synth_name in ["Literature Overview.md", "Method Taxonomy.md", "Research Gaps.md", "index.md"]:
        src_synth = vault_root / "Knowledge" / synth_name
        if src_synth.exists():
            shutil.copy2(src_synth, archive_demo / synth_name)

    clean_overview = """---
type: literature-synthesis
project: zotero_obsidian_kb
title: "Literature Overview: Active Research Domain"
status: active
covered_papers: []
key_themes: []
updated: """ + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """
---

# Literature Overview: Active Research Domain

## Executive Synthesis
*No literature ingested yet. Ingest paper notes in Sources/Papers/ to automatically synthesize your domain overview.*

## Chronological Milestones
| Year | Paper | Key Innovation | Primary Impact |
|---|---|---|---|
| - | *Waiting for first paper* | - | - |

## Evidence & Benchmark Matrix
| Task / Benchmark | Baseline Metric | Proposed Metric | Delta | Source Note |
|---|---|---|---|---|
| - | - | - | - | - |
"""
    (vault_root / "Knowledge" / "Literature Overview.md").write_text(clean_overview, encoding="utf-8")

    clean_taxonomy = """---
type: method-taxonomy
project: zotero_obsidian_kb
title: "Method Taxonomy: Domain Methodologies"
status: active
covered_papers: []
key_themes: []
updated: """ + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """
---

# Method Taxonomy: Domain Methodologies

## Taxonomy Tree
```
Research Methods & Architecture Taxonomy
└── Pending Ingestion (Waiting for your literature notes)
```

## Comparative Method Matrix
| Method Family | Mathematical Operation | Primary Advantage | Primary Constraint |
|---|---|---|---|
| - | - | - | - |
"""
    (vault_root / "Knowledge" / "Method Taxonomy.md").write_text(clean_taxonomy, encoding="utf-8")

    clean_gaps = """---
type: research-gaps
project: zotero_obsidian_kb
title: "Research Gaps: Open Problems & Theoretical Bottlenecks"
status: active
covered_papers: []
key_themes: []
updated: """ + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """
---

# Research Gaps: Open Problems & Theoretical Bottlenecks

## Gap Catalog
*Identified open challenges, bottlenecks, and limitations from ingested literature will be compiled here.*

## Priority Matrix for Future Investigation
| Gap ID | Description | Impact | Feasibility | Priority | Canonical Source |
|---|---|---|---|---|---|
| GAP-00 | Initial setup - waiting for literature ingestion | Low | High | P3 | - |
"""
    (vault_root / "Knowledge" / "Research Gaps.md").write_text(clean_gaps, encoding="utf-8")

    clean_knowledge_index = """---
type: index
project: zotero_obsidian_kb
updated: """ + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """
---

# Knowledge Namespace Index

## Syntheses & Overviews
- [[Knowledge/Literature Overview|Literature Overview]]
- [[Knowledge/Method Taxonomy|Method Taxonomy]]
- [[Knowledge/Research Gaps|Research Gaps]]

## Atomic Concepts (0)
*No atomic concepts created yet. As you read papers, AI will help extract and promote concepts into Knowledge/Concepts/.*
"""
    (vault_root / "Knowledge" / "index.md").write_text(clean_knowledge_index, encoding="utf-8")

    # 4. Backup & reset comparison matrix
    matrix_file = vault_root / "Writing" / "comparison-matrix.md"
    if matrix_file.exists():
        shutil.copy2(matrix_file, archive_demo / "comparison-matrix.md")
    clean_matrix = """# Literature Comparison Matrix

| Paper | Title | Year | Core Claim | Method / Benchmark | Claim Strength | Primary Limitation |
|---|---|---|---|---|---|---|
| - | *No papers ingested yet* | - | - | - | - | - |
"""
    matrix_file.write_text(clean_matrix, encoding="utf-8")

    # 5. Backup & reset Canvas
    canvas_file = vault_root / "Maps" / "literature.canvas"
    if canvas_file.exists():
        shutil.copy2(canvas_file, archive_demo / "literature.canvas")
    
    clean_canvas_data = {
        "nodes": [
            {
                "id": "welcome-node",
                "type": "text",
                "text": "### 欢迎使用自迭代文献知识库\n\n当前知识库处于纯净初始状态。\n\n1. 在 Zotero 中选中文献并划线批注。\n2. 在 Obsidian 中按 `Ctrl+P` 运行 `Zotero Integration: Create Literature Note`。\n3. 运行 `Scripts/run_pipeline.bat` 即可自动生成知识网络！",
                "x": 0,
                "y": 0,
                "width": 420,
                "height": 220,
                "color": "6"
            }
        ],
        "edges": []
    }
    canvas_file.write_text(json.dumps(clean_canvas_data, indent=2, ensure_ascii=False), encoding="utf-8")

    # 6. Update 00-Hub.md and 01-Plan.md
    clean_hub = """---
type: hub
project: zotero_obsidian_kb
updated: """ + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """
---

# Academic Knowledge Base Hub

欢迎使用 **Zotero + Obsidian + Codex 学术自迭代知识库**（当前为纯净空白起步状态）。

## 快速上手
1. 📖 查看实操指南：[[SCHOLARFLOW_WORKFLOW_GUIDE|《ScholarFlow 自迭代学术知识库实操指南》]]
2. 📥 导入您的第一篇文献到 `Sources/Papers/`
3. ⚡ 运行维护工具：双击运行 `Scripts/run_pipeline.bat`

## 导航中心 (MOC)
- [[02-Index|主索引导航 (02-Index)]]
- [[01-Plan|当前研究规划与待读清单 (01-Plan)]]
- [[Knowledge/Literature Overview|领域文献综述]]
- [[Knowledge/Method Taxonomy|方法分类法]]
- [[Knowledge/Research Gaps|开放研究空白]]
- `Maps/literature.canvas` — 交互式知识图谱画布
"""
    (vault_root / "00-Hub.md").write_text(clean_hub, encoding="utf-8")

    clean_plan = """---
type: plan
project: zotero_obsidian_kb
updated: """ + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """
---

# Active Research Plan & Reading Queue

## 当前研究状态 (Current Research State)
- **知识库状态**：纯净空白起步状态（示例已安全归档至 `.demo_backup/`）。
- **当前核心研究议题**：待确立（根据您近期关注的学术方向填写）。

## 待读文献队列 (To-Read Queue)
- [ ] 文献 1：*(添加您的第一篇待读论文)*
- [ ] 文献 2：*(添加您的第二篇待读论文)*

## 活跃研究假设 (Active Hypotheses)
1. 假设 1：*(记录您正在探索的科学问题或实验设想)*
"""
    (vault_root / "01-Plan.md").write_text(clean_plan, encoding="utf-8")

    # 7. Update registry.md and 02-Index.md
    clean_registry = """---
type: registry
project: zotero_obsidian_kb
updated: """ + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """
---

# Master Knowledge Base Registry

This registry is the authoritative single source of truth tracking all notes in the vault.

## Sources

| ID | Title | Citekey / Slug | Type | Status | Path | Updated |
|---|---|---|---|---|---|---|
| - | *No papers ingested yet* | - | - | - | - | - |

## Knowledge & Concepts

| ID | Title | Slug | Type | Status | Path | Updated |
|---|---|---|---|---|---|---|
| synth-01 | Literature Overview | literature-overview | literature-synthesis | active | [[Knowledge/Literature Overview]] | """ + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """ |
| synth-02 | Method Taxonomy | method-taxonomy | method-taxonomy | active | [[Knowledge/Method Taxonomy]] | """ + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """ |
| synth-03 | Research Gaps | research-gaps | research-gaps | active | [[Knowledge/Research Gaps]] | """ + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """ |
"""
    (vault_root / "_system" / "registry.md").write_text(clean_registry, encoding="utf-8")

    clean_index = """---
type: index
project: zotero_obsidian_kb
updated: """ + datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ") + """
---

# Master Knowledge Base Index (MOC)

## 1. 核心导航入口
- [[00-Hub|00-Hub: 项目总览中枢]]
- [[01-Plan|01-Plan: 研究规划与待读队列]]
- [[SCHOLARFLOW_WORKFLOW_GUIDE|《ScholarFlow 自迭代学术知识库实操指南》]]
- [[_system/registry|知识库全局注册表]]

---

## 2. 原始文献库 (`Sources/Papers/`)
*(暂无已读文献，请使用 Zotero Integration 插件导入或直接添加笔记)*

---

## 3. 提炼知识库 (`Knowledge/`)

### 领域综合成果
- [[Knowledge/Literature Overview|领域文献综述]]
- [[Knowledge/Method Taxonomy|方法分类法]]
- [[Knowledge/Research Gaps|开放研究空白]]

### 原子概念与机制 (`Knowledge/Concepts/`)
*(等待从新文献中提炼)*

---

## 4. 可视化图谱 (`Maps/`)
- `Maps/literature.canvas` — 交互式知识拓扑图谱

---

## 5. 论文写作 (`Writing/`)
- [[Writing/comparison-matrix|全景文献对比矩阵]]
"""
    (vault_root / "02-Index.md").write_text(clean_index, encoding="utf-8")

    # Clean any old Archive/demo_examples if exists
    old_archive = vault_root / "Archive" / "demo_examples"
    if old_archive.exists():
        shutil.rmtree(old_archive)

    print("\n[+] Reset complete! Vault is now 100% clean and ready for your own papers.")
    print("[i] All demo examples have been safely preserved in: .demo_backup/")
    print("[i] You can restore demo examples at any time by running: python Scripts/restore_demo.py")
    print("=" * 70)

if __name__ == "__main__":
    main()
