"""
Reading Q&A & Peripheral Insights Ingestion Engine for ScholarFlow.
Distills conversation deep-dives into 6-module atomic concept cards and updates literature notes.
"""

from __future__ import annotations

import datetime
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from kb_tools.models import dump_frontmatter, parse_frontmatter


@dataclass
class QAInsight:
    paper_citekey: str
    concept_slug: str
    title: str
    cn_title: str
    question: str
    excerpt: str = ""
    mechanism_en: str = ""
    mechanism_cn: str = ""
    mathematical_formula: str = ""
    silicon_analogy: str = ""
    metrology: str = ""
    limitations: str = ""
    claim_strength: str = "strong"
    tags: List[str] = field(default_factory=lambda: ["#type/concept", "#origin/reading-qa"])
    related_concepts: List[str] = field(default_factory=list)
    date_str: str = ""


def format_qa_concept_markdown(qa: QAInsight, project_slug: str = "zotero_obsidian_kb") -> str:
    """Generate canonical 6-module markdown content for a Q&A atomic concept note."""
    now_iso = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    # Clean tags
    clean_tags = []
    for t in qa.tags:
        clean_tag = t.strip()
        if not clean_tag.startswith("#"):
            clean_tag = f"#{clean_tag}"
        clean_tags.append(clean_tag)

    if "#type/concept" not in clean_tags:
        clean_tags.insert(0, "#type/concept")
    if "#origin/reading-qa" not in clean_tags:
        clean_tags.append("#origin/reading-qa")

    # Frontmatter
    frontmatter = {
        "type": "concept",
        "project": project_slug,
        "title": qa.title,
        "status": "active",
        "claim_strength": qa.claim_strength,
        "primary_sources": [f"[[Sources/Papers/{qa.paper_citekey}]]"],
        "tags": clean_tags,
        "updated": now_iso,
    }

    if qa.related_concepts:
        frontmatter["related_concepts"] = [
            c if c.startswith("[[") else f"[[Knowledge/Concepts/{c}]]"
            for c in qa.related_concepts
        ]

    # Sections
    cn_header = f"\n> **中文概念**：*{qa.cn_title}*" if qa.cn_title else ""
    excerpt_block = f"\n> [!quote] 文献原句摘录 (Excerpt)\n> {qa.excerpt.strip()}\n" if qa.excerpt else ""

    formula_block = ""
    if qa.mathematical_formula:
        clean_formula = qa.mathematical_formula.strip()
        if not clean_formula.startswith("$$"):
            clean_formula = f"$$\n{clean_formula}\n$$"
        formula_block = f"\n- **数学/物理方程 (Mathematical Formulation)**:\n  {clean_formula}\n"

    related_wikilinks = "\n".join([
        f"- {c if c.startswith('[[') else f'[[Knowledge/Concepts/{c}]]'}"
        for c in qa.related_concepts
    ]) if qa.related_concepts else "- [[Knowledge/Literature Overview]]\n- [[Knowledge/Method Taxonomy]]"

    mech_en = qa.mechanism_en.strip() if qa.mechanism_en else "Detailed theoretical formulation and physical transport mechanisms."
    mech_cn = qa.mechanism_cn.strip() if qa.mechanism_cn else "深入微观物理与能带/输运理论解析。"
    silicon = qa.silicon_analogy.strip() if qa.silicon_analogy else "与传统硅基先进制程相关技术方案与工程挑战的对比分析。"
    metro = qa.metrology.strip() if qa.metrology else "电学、光学或结构显微表征测试方法。"
    limits = qa.limitations.strip() if qa.limitations else "当前工艺与物理微缩下的主要局限性。"

    body = f"""# {qa.title}{cn_header}

---

## 1. 问题背景与文献原句 (Originating Context & Excerpt)
- **文献出处**：[[Sources/Papers/{qa.paper_citekey}]]
- **精读疑问**：{qa.question.strip()}
{excerpt_block}
---

## 2. 物理机制与微观原理解析 (Physical Mechanism & Working Principles)
- **[EN]**: {mech_en}
- **[CN] 物理机制与核心内涵**: {mech_cn}
{formula_block}
---

## 3. 传统硅基技术对照 (Silicon Microelectronics Analogy)
- **硅基对照与工程映射**: {silicon}

---

## 4. 关键实验与提取方法 (Experimental Metrology & Characterization)
- **测试与表征手段**: {metro}

---

## 5. 局限性与开放挑战 (Limitations & Future Challenges)
- **适用边界与瓶颈**: {limits}

---

## 6. 双向链接与参考文献 (Bidirectional Links & References)
- [[Sources/Papers/{qa.paper_citekey}]]
{related_wikilinks}
"""

    return dump_frontmatter(frontmatter, body)


def append_qa_to_paper_note(vault_dir: Path, qa: QAInsight) -> Path:
    """Update literature note with a ## Reading Q&A & Deep Dives entry and link knowledge."""
    vault_path = Path(vault_dir).resolve()
    paper_file = vault_path / "Sources" / "Papers" / f"{qa.paper_citekey}.md"
    if not paper_file.exists():
        raise FileNotFoundError(f"Paper note not found: {paper_file}")

    content = paper_file.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    # 1. Update Frontmatter concepts & linked_knowledge
    linked_knowledge = fm.get("linked_knowledge", [])
    if not isinstance(linked_knowledge, list):
        linked_knowledge = [linked_knowledge] if linked_knowledge else []
    concept_target = f"[[Knowledge/Concepts/{qa.concept_slug}]]"
    if concept_target not in linked_knowledge:
        linked_knowledge.append(concept_target)
    fm["linked_knowledge"] = linked_knowledge

    concepts_list = fm.get("concepts", [])
    if not isinstance(concepts_list, list):
        concepts_list = [concepts_list] if concepts_list else []
    if qa.title not in concepts_list:
        concepts_list.append(qa.title)
    fm["concepts"] = concepts_list

    # 2. Prepare Q&A Section entry
    date_stamp = qa.date_str or datetime.datetime.now().strftime("%Y-%m-%d")
    cn_answer_short = (qa.mechanism_cn.split("。")[0] + "。") if qa.mechanism_cn else "已完成底层物理机制与微电子技术对照分析。"
    qa_entry = f"""> [!question]+ 💬 精读深度问答记录 ({date_stamp})
> **问**：{qa.question.strip()}
> **答**：{cn_answer_short}
> ──► 💡 **已沉淀原子概念卡片**：[[Knowledge/Concepts/{qa.concept_slug}|{qa.title}]]
"""

    qa_heading = "## Reading Q&A & Deep Dives"
    if qa_heading.lower() in body.lower():
        pattern = re.compile(rf"({re.escape(qa_heading)}[^\n]*\n)", re.IGNORECASE)
        body = pattern.sub(rf"\1\n{qa_entry}\n", body, count=1)
    else:
        insert_marker_patterns = [
            r"(## Silicon Analogy[^\n]*\n)",
            r"(## Knowledge links[^\n]*\n)",
            r"(## Direct relevance to repo[^\n]*\n)",
            r"(## References[^\n]*\n)",
        ]
        inserted = False
        for p in insert_marker_patterns:
            rx = re.compile(p, re.IGNORECASE)
            if rx.search(body):
                body = rx.sub(rf"{qa_heading}\n{qa_entry}\n---\n\n\1", body, count=1)
                inserted = True
                break
        if not inserted:
            body = f"{body.rstrip()}\n\n---\n\n{qa_heading}\n{qa_entry}\n"

    updated_content = dump_frontmatter(fm, body)
    paper_file.write_text(updated_content, encoding="utf-8")
    return paper_file


def ingest_qa_concept(vault_dir: Path, qa: QAInsight, project_slug: str = "zotero_obsidian_kb") -> Tuple[Path, Path]:
    """
    Ingest a Q&A deep dive into the vault:
    1. Writes Knowledge/Concepts/<slug>.md
    2. Updates Sources/Papers/<citekey>.md
    Returns tuple of (concept_note_path, paper_note_path).
    """
    vault_path = Path(vault_dir).resolve()
    concepts_dir = vault_path / "Knowledge" / "Concepts"
    concepts_dir.mkdir(parents=True, exist_ok=True)

    concept_file = concepts_dir / f"{qa.concept_slug}.md"
    concept_content = format_qa_concept_markdown(qa, project_slug=project_slug)
    concept_file.write_text(concept_content, encoding="utf-8")

    paper_file = append_qa_to_paper_note(vault_path, qa)
    return concept_file, paper_file
