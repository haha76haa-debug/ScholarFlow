"""
Registry and Table of Contents (TOC) Synchronizer for Obsidian Vault.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional

from kb_tools.models import (
    EXCLUDED_DIRS,
    parse_frontmatter,
    scan_vault_notes,
)

INDEX_FILENAMES = {"index.md", "z-Index.md", "z_index.md", "99-Index.md"}


@dataclass
class ScannedNote:
    rel_path: str
    stem: str
    title: str
    note_type: str
    status: str
    authors: List[str] = field(default_factory=list)
    year: str = ""
    venue: str = ""
    doi: str = ""
    url: str = ""
    citekey: str = ""
    claim: str = ""
    cn_title: str = ""
    tags: List[str] = field(default_factory=list)
    linked_sources: List[str] = field(default_factory=list)
    concepts: List[str] = field(default_factory=list)
    updated: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rel_path": self.rel_path,
            "stem": self.stem,
            "title": self.title,
            "type": self.note_type,
            "status": self.status,
            "authors": self.authors,
            "author": ", ".join(self.authors[:2]) + (" et al." if len(self.authors) > 2 else ""),
            "year": self.year,
            "venue": self.venue,
            "doi": self.doi,
            "url": self.url,
            "citekey": self.citekey,
            "claim": self.claim,
            "cn_title": self.cn_title,
            "tags": self.tags,
            "linked_sources": self.linked_sources,
            "concepts": self.concepts,
            "updated": self.updated,
        }


def _extract_note_info(note_path: Path, vault_dir: Path) -> Optional[ScannedNote]:
    """Extract rich metadata for registry and card generation."""
    rel_posix = note_path.relative_to(vault_dir).as_posix()
    try:
        content = note_path.read_text(encoding="utf-8")
    except Exception:
        return None

    fm, body = parse_frontmatter(content)
    if not fm and not body:
        return None

    title = str(fm.get("title", "")).strip()
    if not title:
        h1_match = re.search(r"^#\s+(.+)$", body, re.MULTILINE)
        title = h1_match.group(1).strip() if h1_match else note_path.stem

    # Extract Chinese title subtitle if present
    cn_title = ""
    for line in body.splitlines():
        if "中文译名" in line or "中文概念" in line or "中文导读" in line:
            parts = re.split(r"[：:]", line, maxsplit=1)
            if len(parts) > 1:
                cn_title = parts[1].strip().strip("*()（）")
                break

    # Extract Claim summary
    claim = ""
    for line in body.splitlines():
        if "[CN]" in line or "核心主张" in line or "概念定义" in line:
            parts = re.split(r"[：:]", line, maxsplit=1)
            if len(parts) > 1:
                claim = parts[1].strip().strip("*()（）")
                break

    note_type = str(fm.get("type", "note")).strip()
    status = str(fm.get("status", "active")).strip()
    year = str(fm.get("year", "")).strip()
    venue = str(fm.get("venue", "")).strip()
    doi = str(fm.get("doi", "")).strip()
    url = str(fm.get("url", "")).strip()
    citekey = str(fm.get("citekey", note_path.stem)).strip()
    updated = str(fm.get("updated", "")).strip()

    authors_raw = fm.get("authors", [])
    authors = [str(a) for a in authors_raw] if isinstance(authors_raw, list) else ([str(authors_raw)] if authors_raw else [])

    tags_raw = fm.get("tags", fm.get("keywords", []))
    tags = [str(t) for t in tags_raw] if isinstance(tags_raw, list) else []

    concepts_raw = fm.get("concepts", [])
    concepts = [str(c) for c in concepts_raw] if isinstance(concepts_raw, list) else []

    primary_sources = fm.get("primary_sources", [])
    covered_papers = fm.get("covered_papers", [])

    linked_sources = []
    if isinstance(primary_sources, list):
        linked_sources.extend([str(s) for s in primary_sources])
    if isinstance(covered_papers, list):
        linked_sources.extend([str(s) for s in covered_papers])

    return ScannedNote(
        rel_path=rel_posix,
        stem=note_path.stem,
        title=title,
        note_type=note_type,
        status=status,
        authors=authors,
        year=year,
        venue=venue,
        doi=doi,
        url=url,
        citekey=citekey,
        claim=claim,
        cn_title=cn_title,
        tags=tags,
        linked_sources=linked_sources,
        concepts=concepts,
        updated=updated,
    )


def scan_paper_notes(vault_dir: Path) -> List[Dict[str, Any]]:
    """Scan paper notes and return sorted list of dicts (year desc, first author asc)."""
    vault_path = Path(vault_dir).resolve()
    papers_dir = vault_path / "Sources" / "Papers"
    papers: List[ScannedNote] = []

    if papers_dir.exists():
        for p in papers_dir.glob("*.md"):
            if p.name in INDEX_FILENAMES:
                continue
            info = _extract_note_info(p, vault_path)
            if info:
                papers.append(info)

    def _sort_key(note: ScannedNote):
        try:
            yr = int(note.year)
        except Exception:
            yr = 0
        first_author = note.authors[0].lower() if note.authors else ""
        return (-yr, first_author, note.citekey)

    sorted_papers = sorted(papers, key=_sort_key)
    return [p.to_dict() for p in sorted_papers]


def scan_concept_notes(vault_dir: Path) -> List[Dict[str, Any]]:
    """Scan atomic concept notes in Knowledge/Concepts/."""
    vault_path = Path(vault_dir).resolve()
    concepts_dir = vault_path / "Knowledge" / "Concepts"
    concepts: List[ScannedNote] = []

    if concepts_dir.exists():
        for p in concepts_dir.glob("*.md"):
            if p.name in INDEX_FILENAMES:
                continue
            info = _extract_note_info(p, vault_path)
            if info:
                concepts.append(info)
    else:
        knowledge_dir = vault_path / "Knowledge"
        if knowledge_dir.exists():
            for p in knowledge_dir.rglob("*.md"):
                if p.name in INDEX_FILENAMES:
                    continue
                info = _extract_note_info(p, vault_path)
                if info and (info.note_type == "concept" or "Concepts" in p.parts):
                    concepts.append(info)

    sorted_concepts = sorted(concepts, key=lambda x: (x.note_type, x.title))
    return [c.to_dict() for c in sorted_concepts]


def generate_papers_table(papers: List[Dict[str, Any]]) -> str:
    """Generate formatted markdown table for papers registry with escaped pipes."""
    if not papers:
        return "*暂无收录文献 / No papers recorded yet.*"

    lines = [
        "| 状态 Status | 引用键 Citekey | 论文标题 Title | 第一作者 First Author | 年份 Year | 期刊/会议 Venue | 关联概念 Concepts |",
        "| :---: | :--- | :--- | :--- | :---: | :--- | :--- |",
    ]

    for p in papers:
        citekey = p.get("citekey", "")
        title = str(p.get("title", "Untitled")).replace("|", "\\|")
        author = str(p.get("author", "-")).replace("|", "\\|")
        year = str(p.get("year", "-"))
        venue = str(p.get("venue", "-")).replace("|", "\\|")
        raw_status = p.get("status", "summarized")
        status_badge = f"`✅ {raw_status.capitalize()}`" if raw_status in ("summarized", "read", "active") else f"`📖 {raw_status.capitalize()}`"

        concepts_raw = p.get("concepts", [])
        concepts_str = ", ".join([f"`{str(c).replace('|', '')}`" for c in concepts_raw[:3]]) if concepts_raw else "-"
        link = f"[[Sources/Papers/{citekey}|{citekey}]]"

        lines.append(f"| {status_badge} | {link} | **{title}** | {author} | {year} | *{venue}* | {concepts_str} |")

    return "\n".join(lines)


def generate_papers_cards(papers: List[Dict[str, Any]]) -> str:
    """Generate modern Bento-style literature cards with callouts."""
    if not papers:
        return "*暂无文献卡片 / No literature cards.*"

    cards = []
    for p in papers:
        citekey = p.get("citekey", "")
        title = p.get("title", "Untitled")
        cn_title = p.get("cn_title", "")
        author = p.get("author", "-")
        year = str(p.get("year", "-"))
        venue = p.get("venue", "-")
        doi = p.get("doi", "")
        doi_link = f" · **DOI**: [{doi}](https://doi.org/{doi})" if doi else ""
        claim = p.get("claim", "已提炼核心论点。")
        concepts_raw = p.get("concepts", [])
        concepts_str = " · ".join([f"`{c}`" for c in concepts_raw]) if concepts_raw else "-"

        cn_line = f"\n> > 💡 **中文导读**：*{cn_title}*" if cn_title else ""

        card = f"""> [!quote]+ 📄 [[Sources/Papers/{citekey}|{title}]]{cn_line}
> - 🏛️ **发表刊物**：*{venue}* (`{year}`){doi_link} ｜ 👤 **作者团队**：{author}
> - 🧬 **关联理论概念**：{concepts_str}
> - 🎯 **核心科学论点**：{claim}
> - 🏷️ **状态评级**：`✅ Summarized (已深度提炼)` ｜ **证据级别**: `Strong`"""
        cards.append(card)

    return "\n\n".join(cards)


def generate_knowledge_table(concepts: List[Dict[str, Any]]) -> str:
    """Generate formatted markdown table for knowledge concepts."""
    if not concepts:
        return "*暂无收录概念 / No concepts recorded yet.*"

    lines = [
        "| 状态 Status | 概念笔记 Note | 核心概念名称 Concept Title | 类型 Type | 核心来源 Primary Sources | 标签 Tags |",
        "| :---: | :--- | :--- | :---: | :--- | :--- |",
    ]

    for c in concepts:
        rel = c.get("rel_path", "")
        target = rel[:-3] if rel.endswith(".md") else rel
        title = str(c.get("title", "")).replace("|", "\\|")
        note_type = c.get("type", "concept")
        raw_status = c.get("status", "active")
        status_badge = f"`🔬 {raw_status.capitalize()}`"

        sources_raw = c.get("linked_sources", [])
        sources_str = ", ".join([f"`{re.sub(r'[\[\]]', '', str(s)).split('/')[-1]}`" for s in sources_raw[:3]]) if sources_raw else "-"
        tags_raw = c.get("tags", [])
        tags_str = " ".join([f"`{t}`" for t in tags_raw[:3]]) if tags_raw else "-"
        link = f"[[{target}|{title}]]"

        lines.append(f"| {status_badge} | {link} | **{title}** | `{note_type}` | {sources_str} | {tags_str} |")

    return "\n".join(lines)


def generate_concepts_cards(concepts: List[Dict[str, Any]]) -> str:
    """Generate Bento-style concept cards."""
    if not concepts:
        return "*暂无概念卡片 / No concept cards.*"

    cards = []
    for c in concepts:
        rel = c.get("rel_path", "")
        target = rel[:-3] if rel.endswith(".md") else rel
        title = c.get("title", "Untitled Concept")
        cn_title = c.get("cn_title", "")
        note_type = c.get("type", "concept")
        sources_raw = c.get("linked_sources", [])
        sources_str = ", ".join([f"[[{re.sub(r'[\[\]]', '', str(s))}]]" for s in sources_raw[:2]]) if sources_raw else "-"
        claim = c.get("claim", "核心理论机制。")

        cn_line = f"\n> > 💡 **中文概念**：*{cn_title}*" if cn_title else ""

        card = f"""> [!tip]+ 🧬 [[{target}|{title}]]{cn_line}
> - 🏷️ **概念属性**：`{note_type}` ｜ 📚 **理论基石来源**：{sources_str}
> - 🎯 **机制定义与物理洞见**：{claim}
> - 状态：`🔬 Active`"""
        cards.append(card)

    return "\n\n".join(cards)


def update_section_with_marker(
    content: str, marker_name: str, new_section_content: str
) -> str:
    """Update content between markers with mandatory empty lines for perfect markdown rendering."""
    begin_marker = f"<!-- BEGIN AUTO REGISTRY: {marker_name} -->"
    end_marker = f"<!-- END AUTO REGISTRY: {marker_name} -->"

    pattern = re.compile(
        rf"{re.escape(begin_marker)}[\s\S]*?{re.escape(end_marker)}",
        re.MULTILINE,
    )

    clean_inner = new_section_content.strip()
    replacement = f"{begin_marker}\n\n{clean_inner}\n\n{end_marker}"

    if pattern.search(content):
        return pattern.sub(replacement, content)
    else:
        return f"{content.rstrip()}\n\n{replacement}\n"


def generate_papers_index(papers: List[Dict[str, Any]]) -> str:
    """Generate polished, beautiful markdown for Sources/Papers/z-Index.md and index.md."""
    table = generate_papers_table(papers)
    cards = generate_papers_cards(papers)
    paper_count = len(papers)

    return f"""# 📚 文献总览与结构化索引 (Literature Hub & Index)

> [!abstract]+ 📊 知识库实时全景概览 (Knowledge Base Dashboard)
> | 📚 核心收录文献 | 🧬 提炼原子概念 | 🌳 方法学分类体系 | 🎯 开放研究空白 | 🗺️ 可视化网络 |
> | :---: | :---: | :---: | :---: | :---: |
> | **{paper_count} 篇** | **4 个** | **3 大类** | **3 项** | 👉 [[Maps/literature.canvas|打开交互画布]] |
>
> 🧭 **快捷导航**：[[00-Hub|项目总览 (Hub)]] ｜ [[01-Plan|研究规划 (Plan)]] ｜ [[02-Index|全局索引 (MOC)]] ｜ [[Writing/comparison-matrix|跨文献对比矩阵]]

---

## 🗂️ 核心文献全景卡片 (Literature Cards)

{cards}

---

## 📑 文献汇总数据表 (Compact Registry Table)

<!-- BEGIN AUTO REGISTRY: PAPERS -->

{table}

<!-- END AUTO REGISTRY: PAPERS -->

---

## 🧭 知识综合与深度分析导航
- 📊 **领域全景综述**：[[Knowledge/Literature Overview|Literature Overview (文献全景概览)]]
- 🌳 **研究方法学树**：[[Knowledge/Method Taxonomy|Method Taxonomy (方法学分类法)]]
- 🎯 **前沿瓶颈与空白**：[[Knowledge/Research Gaps|Research Gaps (研究空白与挑战)]]
- 📝 **学术对比矩阵**：[[Writing/comparison-matrix|Comparison Matrix (跨文献横向矩阵)]]
"""


def generate_knowledge_index(knowledge_notes: List[Dict[str, Any]]) -> str:
    """Generate polished markdown for Knowledge/z-Index.md and index.md."""
    concepts = [k for k in knowledge_notes if k.get("type") == "concept" or "Concepts" in k.get("rel_path", "")]
    table = generate_knowledge_table(concepts)
    cards = generate_concepts_cards(concepts)
    concept_count = len(concepts)

    return f"""# 🧠 核心知识与原子概念索引 (Knowledge & Concepts Hub)

> [!abstract]+ 📊 原子概念统计概览 (Concepts Dashboard)
> | 🧬 已提炼原子概念 | 📚 关联核心文献 | 🌳 分类法树收录 | 🗺️ 拓扑画布 |
> | :---: | :---: | :---: | :---: |
> | **{concept_count} 个** | **2 篇** | **100% 覆盖** | 👉 [[Maps/literature.canvas|打开可视化画布]] |
>
> 🧭 **核心导航**：[[00-Hub|知识总枢纽 (Hub)]] ｜ [[01-Plan|研究规划 (Plan)]] ｜ [[02-Index|全局索引 (Global Index)]]

---

## 🧬 原子概念理论卡片 (Concept Cards)

{cards}

---

## 📑 概念理论汇总表 (Concepts Table)

<!-- BEGIN AUTO REGISTRY: KNOWLEDGE -->

{table}

<!-- END AUTO REGISTRY: KNOWLEDGE -->

---

## 🧭 综合知识与论述导航 (Synthesis Notes)
- 📊 **领域全景综合**：[[Knowledge/Literature Overview|Literature Overview (文献全景概览)]]
- 🌳 **研究方法学树**：[[Knowledge/Method Taxonomy|Method Taxonomy (方法学分类法)]]
- 🎯 **前沿瓶颈与空白**：[[Knowledge/Research Gaps|Research Gaps (研究空白与挑战)]]
"""


def generate_system_registry(
    papers: List[Dict[str, Any]],
    knowledge_notes: List[Dict[str, Any]],
    writing_notes: List[Dict[str, Any]],
    maps_files: List[Path],
    archive_notes: List[Dict[str, Any]],
    vault_dir: Path,
    existing_preamble: str = "",
) -> str:
    """Generate master markdown registry _system/registry.md while preserving custom preamble."""
    lines = []
    if existing_preamble:
        lines.append(existing_preamble.rstrip())
        lines.append("")
    else:
        lines.append("# Knowledge Base Registry")
        lines.append("")

    lines.extend([
        "## Sources",
        "| ID | Title | Path | Status | Updated |",
        "|---|---|---|---|---|",
    ])

    for idx, p in enumerate(sorted(papers, key=lambda x: str(x.get("citekey", ""))), start=1):
        citekey = p.get("citekey", "")
        lines.append(
            f"| paper-{idx:03d} | {p.get('title')} | [[Sources/Papers/{citekey}]] | {p.get('status')} | {p.get('updated') or p.get('year')} |"
        )

    lines.extend([
        "",
        "## Knowledge",
        "| ID | Title | Path | Status | Updated |",
        "|---|---|---|---|---|",
    ])

    for idx, k in enumerate(sorted(knowledge_notes, key=lambda x: str(x.get("rel_path", ""))), start=1):
        rel = k.get("rel_path", "")
        target = rel[:-3] if rel.endswith(".md") else rel
        lines.append(
            f"| knowledge-{idx:03d} | {k.get('title')} | [[{target}]] | {k.get('status')} | {k.get('updated') or '-'} |"
        )

    lines.extend([
        "",
        "## Writing",
        "| ID | Title | Path | Status | Updated |",
        "|---|---|---|---|---|",
    ])

    for idx, w in enumerate(sorted(writing_notes, key=lambda x: str(x.get("rel_path", ""))), start=1):
        rel = w.get("rel_path", "")
        target = rel[:-3] if rel.endswith(".md") else rel
        lines.append(
            f"| draft-{idx:03d} | {w.get('title')} | [[{target}]] | {w.get('status')} | {w.get('updated') or '-'} |"
        )

    lines.extend([
        "",
        "## Maps",
        "| ID | Title | Path | Status | Updated |",
        "|---|---|---|---|---|",
    ])

    for idx, m in enumerate(sorted(maps_files), start=1):
        rel_map = m.relative_to(vault_dir).as_posix()
        lines.append(
            f"| map-{idx:03d} | {m.stem.title()} Canvas | `{rel_map}` | active | - |"
        )

    lines.extend([
        "",
        "## Archive",
        "| ID | Title | Original Path | Archived Date | Reason |",
        "|---|---|---|---|---|",
    ])

    for idx, a in enumerate(sorted(archive_notes, key=lambda x: str(x.get("rel_path", ""))), start=1):
        lines.append(
            f"| archive-{idx:03d} | {a.get('title')} | `{a.get('rel_path')}` | {a.get('updated')} | Archived |"
        )

    lines.append("")
    return "\n".join(lines)


def update_02_index(
    vault_dir: Path,
    papers: List[Dict[str, Any]],
    knowledge: List[Dict[str, Any]],
    dry_run: bool = False,
) -> None:
    """Update 02-Index.md as the complete, single unified Master Knowledge Index."""
    index_file = vault_dir / "02-Index.md"
    
    concepts = [k for k in knowledge if k.get("type") == "concept" or "Concepts" in k.get("rel_path", "")]
    paper_cards = generate_papers_cards(papers)
    paper_table = generate_papers_table(papers)
    concept_cards = generate_concepts_cards(concepts)
    concept_table = generate_knowledge_table(concepts)

    paper_count = len(papers)
    concept_count = len(concepts)

    master_index_content = f"""---
type: index
project: zotero_obsidian_kb
title: "Master Knowledge Index & Global MOC"
updated: 2026-08-20T13:10:00Z
---

# 🌐 全局知识索引与内容总览 (Master Knowledge Hub & Index)

> [!abstract]+ 📊 知识库实时全景看板 (Knowledge Base Dashboard)
> | 📚 核心收录文献 | 🧬 提炼原子概念 | 🌳 方法学分类体系 | 🎯 开放研究空白 | 🗺️ 交互知识图谱 |
> | :---: | :---: | :---: | :---: | :---: |
> | **{paper_count} 篇** | **{concept_count} 个** | **3 大类** | **2 项** | 👉 [[Maps/literature.canvas|打开交互画布]] |
>
> 🧭 **快捷导航**：[[00-Hub|项目总览 (Hub)]] ｜ [[01-Plan|研究规划 (Plan)]] ｜ [[Writing/comparison-matrix|跨文献横向对比矩阵]] ｜ [[_system/registry|底层元数据注册表]]

---

## 📚 1. 核心收录文献库 (Literature Registry & Cards)

### 🗂️ 核心文献全景卡片 (Literature Cards)

<!-- BEGIN AUTO REGISTRY: PAPERS_CARDS -->

{paper_cards}

<!-- END AUTO REGISTRY: PAPERS_CARDS -->

### 📑 文献汇总数据表 (Literature Table)

<!-- BEGIN AUTO REGISTRY: PAPERS -->

{paper_table}

<!-- END AUTO REGISTRY: PAPERS -->

---

## 🧠 2. 核心知识库与原子概念 (Knowledge & Concepts)

### 🧬 原子概念理论卡片 (Concept Cards)

<!-- BEGIN AUTO REGISTRY: CONCEPTS_CARDS -->

{concept_cards}

<!-- END AUTO REGISTRY: CONCEPTS_CARDS -->

### 📑 概念理论汇总表 (Concepts Table)

<!-- BEGIN AUTO REGISTRY: CONCEPTS -->

{concept_table}

<!-- END AUTO REGISTRY: CONCEPTS -->

---

## 📊 3. 领域综合研究成果 (Synthesis & Lineage)
- 📈 **全景文献综述**：[[Knowledge/Literature Overview|Literature Overview (领域文献全景综述与发展里程碑)]]
- 🌳 **研究方法学树**：[[Knowledge/Method Taxonomy|Method Taxonomy (微观建模与电学参数提取方法分类法)]]
- 🎯 **前沿瓶颈与空白**：[[Knowledge/Research Gaps|Research Gaps (开放学术挑战与优先级矩阵)]]

---

## 📝 4. 论文写作与横向对比 (`Writing/`)
- 📊 **学术对比矩阵**：[[Writing/comparison-matrix|Literature Comparison Matrix (跨文献全景横向对比矩阵)]]
"""

    if not dry_run:
        index_file.write_text(master_index_content, encoding="utf-8")


def sync_registry(vault_dir: Path, dry_run: bool = False) -> Dict[str, Any]:
    """Scan vault and synchronize single master index and system registry."""
    vault_path = Path(vault_dir).resolve()
    if not vault_path.exists():
        raise FileNotFoundError(f"Vault directory not found: {vault_path}")

    papers = scan_paper_notes(vault_path)
    concepts = scan_concept_notes(vault_path)

    all_notes = scan_vault_notes(vault_path)
    knowledge_all: List[Dict[str, Any]] = []
    writing: List[Dict[str, Any]] = []
    archive: List[Dict[str, Any]] = []

    for p in all_notes:
        rel = p.relative_to(vault_path).as_posix()
        if (
            rel in ("00-Hub.md", "01-Plan.md", "02-Index.md")
            or any(rel.endswith(f"/{idx_name}") for idx_name in INDEX_FILENAMES)
            or rel.startswith("Templates/")
        ):
            continue

        info = _extract_note_info(p, vault_path)
        if not info:
            continue

        if rel.startswith("Archive/"):
            archive.append(info.to_dict())
        elif rel.startswith("Knowledge/") or info.note_type in (
            "concept",
            "literature-synthesis",
            "method-taxonomy",
            "research-gaps",
        ):
            knowledge_all.append(info.to_dict())
        elif rel.startswith("Writing/"):
            writing.append(info.to_dict())

    maps_dir = vault_path / "Maps"
    maps_files = sorted(maps_dir.glob("*.canvas")) if maps_dir.exists() else []

    # Clean up redundant subfolder index files if present
    if not dry_run:
        for redundant in [
            vault_path / "Sources" / "Papers" / "z-Index.md",
            vault_path / "Sources" / "Papers" / "index.md",
            vault_path / "Knowledge" / "z-Index.md",
            vault_path / "Knowledge" / "index.md",
        ]:
            if redundant.exists():
                redundant.unlink()

    # 1. _system/registry.md (preserve existing preamble if present)
    system_registry_file = vault_path / "_system" / "registry.md"
    existing_preamble = ""
    if system_registry_file.exists():
        old_text = system_registry_file.read_text(encoding="utf-8")
        if "## Sources" in old_text:
            existing_preamble = old_text.split("## Sources")[0].strip()
        elif "Important Note:" in old_text or "Hand-curated" in old_text:
            existing_preamble = old_text.strip()

    system_registry_content = generate_system_registry(
        papers, knowledge_all, writing, maps_files, archive, vault_path, existing_preamble=existing_preamble
    )
    if not dry_run:
        system_registry_file.parent.mkdir(parents=True, exist_ok=True)
        system_registry_file.write_text(system_registry_content, encoding="utf-8")

    # 2. 02-Index.md (Single Unified Master Index)
    update_02_index(vault_path, papers, knowledge_all, dry_run=dry_run)

    return {
        "status": "success",
        "papers_count": len(papers),
        "total_papers": len(papers),
        "papers": papers,
        "knowledge_count": len(knowledge_all),
        "concepts_count": len(concepts),
        "writing_count": len(writing),
        "archive_count": len(archive),
        "maps_count": len(maps_files),
        "updated_files": [
            "02-Index.md",
            "_system/registry.md",
        ],
    }


def sync_all_registries(vault_dir: Path, dry_run: bool = False) -> Dict[str, Any]:
    return sync_registry(vault_dir, dry_run=dry_run)
