"""
Unit, Schema, and Integration Tests for ScholarFlow Q&A Deep Dive Ingestion Engine.
Verifies atomic concept note generation, paper note Q&A section appending,
linter validation, tag taxonomy, and end-to-end pipeline synchronization.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

from kb_tools.linter import lint_file, lint_vault
from kb_tools.models import parse_frontmatter
from kb_tools.qa_ingest import (
    QAInsight,
    append_qa_to_paper_note,
    format_qa_concept_markdown,
    ingest_qa_concept,
)
from kb_tools.registry import sync_all_registries
from kb_tools.synthesizer import run_synthesis


@pytest.fixture
def mock_paper_vault(tmp_path: Path) -> Path:
    """Create an isolated minimal vault with 1 paper note for testing QA ingestion."""
    vault = tmp_path / "qa_vault"
    vault.mkdir(parents=True, exist_ok=True)
    (vault / "Sources" / "Papers").mkdir(parents=True, exist_ok=True)
    (vault / "Knowledge" / "Concepts").mkdir(parents=True, exist_ok=True)
    (vault / "Knowledge" / "Comparisons").mkdir(parents=True, exist_ok=True)
    (vault / "Writing").mkdir(parents=True, exist_ok=True)
    (vault / "Maps").mkdir(parents=True, exist_ok=True)
    (vault / "_system").mkdir(parents=True, exist_ok=True)

    paper_file = vault / "Sources" / "Papers" / "2021_Test_Paper.md"
    paper_file.write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Physics and Prospects of 2D Nanoelectronics"
citekey: 2021_Test_Paper
zotero_key: "TEST2021"
canvas_visibility: visible
status: read
source_type: "journal article"
claim_strength: strong
authors:
  - "TestAuthor, Alice"
year: 2021
venue: "Nature Electronics"
concepts:
  - "Initial Concept"
linked_knowledge:
  - "[[Knowledge/Literature Overview]]"
tags:
  - "#type/paper-note"
  - "#topic/2d-materials"
updated: 2026-08-24T00:00:00Z
---

# Physics and Prospects of 2D Nanoelectronics

## Claim
2D semiconductors provide sub-nanometer electrostatic channel scaling.

## Research question
How do contact barriers scale down to sub-10nm dimensions?

## Method
Experimental fabrication and parameter extraction.

## Evidence
```md
Evidence ID: EVD-2021_Test_Paper-01
Source: [[Sources/Papers/2021_Test_Paper]]
Supports: "2D semiconductors offer ultimate sub-5nm channel gate control."
Method / dataset / metric: Transfer characteristics
Limitation: Contact resistance high
Claim strength: strong
```

## Strengths
Pristine atomic surface.

## Limitation
Fermi-level pinning.

## Direct relevance to repo
Core reference.

## Relation to other papers
Foundational work.

## Knowledge links
- [[Knowledge/Literature Overview]]
""", encoding="utf-8")

    return vault


def test_format_qa_concept_markdown_structure():
    """Verify format_qa_concept_markdown outputs 6 required modules and valid frontmatter."""
    qa = QAInsight(
        paper_citekey="2021_Liu_2D-Transistors",
        concept_slug="interface_state_density_and_fermi_pinning",
        title="Interface State Density & Fermi-Level Pinning",
        cn_title="界面态密度与费米能级钉扎机理",
        question="为什么金属沉积在二维半导体表面会导致费米能级钉扎？",
        excerpt="The metal deposition process induces metal-induced gap states (MIGS)...",
        mechanism_en="Wavefunctions of metallic states penetrate the van der Waals gap...",
        mechanism_cn="金属波函数穿透范德华间隙进入禁带形成虚态分布，钉扎费米能级于电荷中性能级附近。",
        mathematical_formula=r"S = \frac{d\Phi_B}{d\Phi_M} = \frac{1}{1 + \frac{q^2 D_{it} \delta}{\varepsilon_{it}}}",
        silicon_analogy="硅基通过离子注入掺杂与NiSi硅化物解决接触问题，二维材料通过半金属杂化解决。",
        metrology="高频/准静态C-V测试与变温输运测试提取Dit与肖特基势垒。",
        limitations="半金属合金热蒸镀均一性与亚10nm接触微缩限制。",
        tags=["#type/concept", "#origin/reading-qa", "#topic/semiconductor-physics"],
        related_concepts=["contact_resistance_extraction"],
    )

    md = format_qa_concept_markdown(qa)
    fm, body = parse_frontmatter(md)

    assert fm["type"] == "concept"
    assert fm["title"] == "Interface State Density & Fermi-Level Pinning"
    assert "[[Sources/Papers/2021_Liu_2D-Transistors]]" in fm["primary_sources"]
    assert "#origin/reading-qa" in fm["tags"]

    assert "## 1. 问题背景与文献原句 (Originating Context & Excerpt)" in body
    assert "## 2. 物理机制与微观原理解析 (Physical Mechanism & Working Principles)" in body
    assert "## 3. 传统硅基技术对照 (Silicon Microelectronics Analogy)" in body
    assert "## 4. 关键实验与提取方法 (Experimental Metrology & Characterization)" in body
    assert "## 5. 局限性与开放挑战 (Limitations & Future Challenges)" in body
    assert "## 6. 双向链接与参考文献 (Bidirectional Links & References)" in body
    assert r"S = \frac{d\Phi_B}{d\Phi_M}" in body


def test_ingest_qa_concept_end_to_end(mock_paper_vault: Path):
    """Verify ingest_qa_concept writes concept note and updates paper note with Q&A callout."""
    qa = QAInsight(
        paper_citekey="2021_Test_Paper",
        concept_slug="test_fermi_pinning_mechanism",
        title="Test Fermi Pinning Mechanism",
        cn_title="测试费米能级钉扎机理",
        question="How does pinning factor S scale with Dit?",
        excerpt="The pinning factor S approaches 0 for strong pinning.",
        mechanism_en="MIGS density determines the barrier height modification.",
        mechanism_cn="MIGS态密度决定了肖特基势垒高度与金属功函数解耦程度。",
        mathematical_formula=r"S = rac{1}{1 + rac{q^2 D_{it} \delta}{arepsilon_{it}}}",
        silicon_analogy="Compared to silicide contacts in bulk Silicon CMOS.",
        metrology="Extracted from temperature-dependent IV characteristics.",
        limitations="Limited by defect-free vdW interface requirements.",
        tags=["#type/concept", "#origin/reading-qa", "#topic/semiconductor-physics"],
    )

    concept_path, paper_path = ingest_qa_concept(mock_paper_vault, qa)

    assert concept_path.exists()
    assert paper_path.exists()

    # Verify Concept Note passes Linter
    issues = lint_file(concept_path, vault_dir=mock_paper_vault)
    errors = [i for i in issues if i.severity == "error"]
    assert len(errors) == 0, f"Concept note lint errors: {errors}"

    # Verify Paper Note was updated with Q&A section and frontmatter
    paper_content = paper_path.read_text(encoding="utf-8")
    paper_fm, paper_body = parse_frontmatter(paper_content)

    assert "[[Knowledge/Concepts/test_fermi_pinning_mechanism]]" in paper_fm.get("linked_knowledge", [])
    assert "Test Fermi Pinning Mechanism" in paper_fm.get("concepts", [])
    assert "## Reading Q&A & Deep Dives" in paper_body
    assert "How does pinning factor S scale with Dit?" in paper_body
    assert "[[Knowledge/Concepts/test_fermi_pinning_mechanism|Test Fermi Pinning Mechanism]]" in paper_body


def test_append_qa_multiple_times_idempotency(mock_paper_vault: Path):
    """Verify appending multiple Q&As to the same paper maintains clean structure."""
    qa1 = QAInsight(
        paper_citekey="2021_Test_Paper",
        concept_slug="qa_concept_one",
        title="QA Concept One",
        cn_title="问答概念一",
        question="Question 1?",
        mechanism_cn="回答 1 内容。",
    )
    qa2 = QAInsight(
        paper_citekey="2021_Test_Paper",
        concept_slug="qa_concept_two",
        title="QA Concept Two",
        cn_title="问答概念二",
        question="Question 2?",
        mechanism_cn="回答 2 内容。",
    )

    ingest_qa_concept(mock_paper_vault, qa1)
    ingest_qa_concept(mock_paper_vault, qa2)

    paper_path = mock_paper_vault / "Sources" / "Papers" / "2021_Test_Paper.md"
    content = paper_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)

    assert len([k for k in fm["linked_knowledge"] if "qa_concept" in k]) == 2
    assert body.count("## Reading Q&A & Deep Dives") == 1
    assert "Question 1?" in body
    assert "Question 2?" in body
