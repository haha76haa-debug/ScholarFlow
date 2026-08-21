import pytest
from pathlib import Path

_VAULT_ROOT = Path(__file__).resolve().parent.parent
if not (_VAULT_ROOT / 'Knowledge' / 'Comparisons' / '2d_contact_vdW_vs_silicon_silicide.md').exists() and not (_VAULT_ROOT / 'Sources' / 'Papers' / '2021_Liu_2D-Transistors.md').exists():
    pytest.skip('Private domain-specific 2D research notes not present in open-source framework vault', allow_module_level=True)

import pytest
from pathlib import Path


"""
Adversarial Stress-Testing Suite for Milestone 4 (M4: Toolchain & Registry Updates).
Executed by Challenger 2 to find failure modes, verify edge cases, and ensure robustness.

Covers:
1. Synthesizer:
   - 0 comparison cards
   - Corrupted/malformed cards (invalid YAML, non-dict, non-list, unicode/binary fuzz, missing headings)
   - Mixed vaults (some papers with silicon analogies, some without)
   - Empty or unstructured Silicon Analogy sections
   - LaTeX formula escaping and markdown table integrity
   - Idempotency across 5+ successive synthesis runs
2. Registry & 02-Index:
   - 02-Index marker stability and balance
   - Section 5 generation (Bento cards & table)
   - Empty vault index generation (0 papers, 0 concepts, 0 comparisons)
   - Large vault scaling index generation
   - Bento-style callout rendering syntax with missing optional fields
   - Pipe character escaping in titles, authors, and reference nodes
   - Idempotency across 5+ successive sync_registry runs
3. 4-Lane Canvas Compatibility:
   - Geometric layout verification (Lane X coordinates, widths, heights)
   - Non-overlapping bounding boxes within lanes
   - Group container boundary conformance
   - Hidden notes filtering (canvas_visibility: hidden)
   - Orphan nodes and circular references handling
   - JSON string escaping for complex body text
   - Edge reference resolution and Obsidian JSON Canvas v1.0 schema compliance
4. Live Vault Conformance:
   - Master pipeline execution on current repository state with 0 errors/warnings/broken links.
"""

import copy
import json
import os
import re
import sys
from pathlib import Path
import pytest

# Ensure src is in sys.path
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kb_tools.synthesizer import (
    extract_comparison_cards,
    extract_paper_silicon_analogy,
    synthesize_comparison_matrix_doc,
    synthesize_literature_overview,
    synthesize_method_taxonomy,
    synthesize_research_gaps,
    run_synthesis,
    synthesize_all,
)
from kb_tools.registry import (
    scan_comparison_notes,
    scan_paper_notes,
    scan_concept_notes,
    generate_comparisons_cards,
    generate_comparisons_table,
    generate_papers_table,
    generate_knowledge_table,
    update_02_index,
    sync_registry,
)
from kb_tools.canvas_gen import (
    build_canvas_graph,
    generate_canvas_file,
    COLOR_SILICON,
    COLOR_ORANGE,
    COLOR_PURPLE,
    COLOR_CYAN,
    COLOR_RED,
)
from kb_tools.cli import main as cli_main
from kb_tools.linter import lint_vault


def _split_markdown_table_row(row_str: str) -> list[str]:
    """Helper to split markdown table cells preserving wikilinks and escaped pipes."""
    s = row_str.strip()
    if not (s.startswith("|") and s.endswith("|")):
        return []
    inner = s[1:-1]
    
    # Protect wikilinks [[...]] and escaped pipes \|
    protected = []
    def _repl_link(m):
        idx = len(protected)
        protected.append(m.group(0))
        return f"__LINK_{idx}__"
    
    masked = re.sub(r"\[\[[^\]]+\]\]", _repl_link, inner)
    masked = masked.replace(r"\|", "__ESCAPED_PIPE__")
    
    raw_cells = masked.split("|")
    cells = []
    for cell in raw_cells:
        c = cell.strip()
        c = c.replace("__ESCAPED_PIPE__", "|")
        for idx, orig in enumerate(protected):
            c = c.replace(f"__LINK_{idx}__", orig)
        cells.append(c)
    return cells


@pytest.fixture
def clean_vault(tmp_path):
    """Fixture creating a fresh minimal vault with all required folders."""
    vault = tmp_path / "test_vault"
    for d in [
        "Sources/Papers",
        "Knowledge/Concepts",
        "Knowledge/Comparisons",
        "Writing",
        "Maps",
        "_system/schemas",
    ]:
        (vault / d).mkdir(parents=True, exist_ok=True)
    return vault


@pytest.fixture
def populated_vault(clean_vault):
    """Fixture with standard sample paper, concept, and comparison notes."""
    # Paper 1
    p1 = clean_vault / "Sources" / "Papers" / "2021_Liu_2D-Transistors.md"
    p1.write_text("""---
type: paper
project: 2d-semiconductors
title: "2D Semiconductor FETs Scaling"
citekey: "2021_Liu_2D-Transistors"
status: read
year: 2021
authors:
  - "Liu et al."
venue: "Nature"
concepts:
  - "Knowledge/Concepts/monolayer_channel"
updated: 2026-08-20T12:00:00Z
---
# 2D Semiconductor FETs Scaling

## Claim
[CN]: 单层原子级体厚抑制短沟道效应。

## Silicon Analogy & Microelectronics Mapping
- **Electrostatic Scaling vs GAAFET**: $\\lambda < 1.5\\text{ nm}$ enables sub-5nm scaling vs. Silicon GAAFET.
- **Mapped Comparisons**:
  - [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet|2D Scaling vs GAAFET]]
""", encoding="utf-8")

    # Concept 1
    c1 = clean_vault / "Knowledge" / "Concepts" / "monolayer_channel.md"
    c1.write_text("""---
type: concept
project: 2d-semiconductors
title: "Monolayer Channel Physics"
status: active
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
updated: 2026-08-20T12:00:00Z
---
# Monolayer Channel Physics
概念定义：原子级超薄沟道物理特性。
""", encoding="utf-8")

    # Comparison 1
    comp1 = clean_vault / "Knowledge" / "Comparisons" / "2d_electrostatic_scaling_vs_silicon_gaafet.md"
    comp1.write_text("""---
type: comparison
project: 2d-semiconductors
title: "2D Electrostatic Scaling vs Silicon GAAFET"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
silicon_reference_nodes:
  - "GAAFET"
  - "CFET"
dimensions_covered:
  - 1
  - 2
  - 3
  - 4
  - 5
  - 6
tags:
  - type/comparison
  - topic/silicon-analogy
updated: 2026-08-20T12:00:00Z
---
# 2D Electrostatic Scaling vs Silicon GAAFET
## Executive Overview & Silicon Analogy
## 1. Physical Scaling & Electrostatic Control
## 2. Ohmic Contact & Metallization Engineering
## 3. Gate Dielectric & EOT Scaling
## 4. CMOS Integration & Thermal Budget
## 5. IRDS Technology Roadmap Alignment
## 6. Electrical Benchmark & Compact Modeling Matrix
## References & Evidence Anchors
""", encoding="utf-8")

    return clean_vault


class TestSynthesizerAdversarial:
    """Adversarial stress-testing of synthesizer.py."""

    def test_synthesis_on_zero_comparison_cards(self, clean_vault):
        """Stress: Synthesizer must complete cleanly when Knowledge/Comparisons is empty or missing."""
        cards = extract_comparison_cards(clean_vault)
        assert cards == []

        doc = synthesize_comparison_matrix_doc(clean_vault)
        assert isinstance(doc, str)
        assert "# Literature Comparison Matrix" in doc
        assert "6-Dimensional Microelectronics Benchmark Matrix" not in doc

        result = run_synthesis(clean_vault)
        assert len(result) == 4
        for p in result:
            assert p.exists()

    def test_synthesis_when_comparisons_dir_deleted(self, clean_vault):
        """Stress: Synthesizer must handle non-existent Knowledge/Comparisons directory."""
        comp_dir = clean_vault / "Knowledge" / "Comparisons"
        if comp_dir.exists():
            comp_dir.rmdir()
        assert not comp_dir.exists()

        cards = extract_comparison_cards(clean_vault)
        assert cards == []

        result = run_synthesis(clean_vault)
        assert len(result) == 4

    def test_synthesis_with_corrupted_cards(self, clean_vault):
        """Stress: Synthesizer must tolerate invalid YAML, non-dict frontmatter, binary/unicode fuzz."""
        comp_dir = clean_vault / "Knowledge" / "Comparisons"
        comp_dir.mkdir(parents=True, exist_ok=True)

        # 1. Invalid YAML syntax
        (comp_dir / "corrupted_yaml.md").write_text("""---
title: "Corrupted YAML
unclosed quote: [1, 2
---
# Heading
""", encoding="utf-8")

        # 2. Non-dict frontmatter (YAML list)
        (comp_dir / "list_frontmatter.md").write_text("""---
- item 1
- item 2
---
# Heading
""", encoding="utf-8")

        # 3. Non-dict frontmatter (YAML integer)
        (comp_dir / "int_frontmatter.md").write_text("""---
12345
---
# Heading
""", encoding="utf-8")

        # 4. Completely empty file
        (comp_dir / "empty.md").write_text("", encoding="utf-8")

        # 5. Non-markdown / weird headings
        (comp_dir / "strange_headings.md").write_text("""---
type: comparison
title: "Strange Headings"
dimensions_covered: ["not-an-int", None, {}]
---
### Subheading without H1 or H2
Random text without structure.
""", encoding="utf-8")

        # 6. Unicode and control characters fuzz
        (comp_dir / "unicode_fuzz.md").write_text("""---
type: comparison
title: "Fuzz \u0000 \u200B \uFEFF \U0001F9E0"
silicon_technology: "FinFET | GAAFET \x01\x02"
---
# Fuzz Card \u202E\u202D
""", encoding="utf-8")

        cards = extract_comparison_cards(clean_vault)
        assert isinstance(cards, list)
        doc = synthesize_comparison_matrix_doc(clean_vault)
        assert isinstance(doc, str)
        assert "# Literature Comparison Matrix" in doc

        res = run_synthesis(clean_vault)
        assert len(res) == 4

    def test_mixed_vault_with_and_without_silicon_analogies(self, clean_vault):
        """Stress: Vault where paper A has silicon analogy, paper B has empty section, paper C has none."""
        p_dir = clean_vault / "Sources" / "Papers"
        
        # Paper A: Complete analogy
        (p_dir / "paper_a.md").write_text("""---
type: paper
title: "Paper A"
citekey: paper_a
status: read
updated: 2026-08-20T12:00:00Z
---
# Paper A
## Silicon Analogy & Microelectronics Mapping
- **Scaling**: Sub-10nm advantage over FinFET.
- **Mapped Comparisons**:
  - [[Knowledge/Comparisons/comp_a|Comp A]]
""", encoding="utf-8")

        # Paper B: Empty Silicon Analogy section
        (p_dir / "paper_b.md").write_text("""---
type: paper
title: "Paper B"
citekey: paper_b
status: read
updated: 2026-08-20T12:00:00Z
---
# Paper B
## Silicon Analogy & Microelectronics Mapping
""", encoding="utf-8")

        # Paper C: No Silicon Analogy section at all
        (p_dir / "paper_c.md").write_text("""---
type: paper
title: "Paper C"
citekey: paper_c
status: read
updated: 2026-08-20T12:00:00Z
---
# Paper C
## Claim
Core claim of Paper C.
""", encoding="utf-8")

        # Check parsing
        res_a = extract_paper_silicon_analogy(p_dir / "paper_a.md")
        assert res_a["has_silicon_analogy"] is True
        assert len(res_a["mapped_comparisons"]) == 1

        res_b = extract_paper_silicon_analogy(p_dir / "paper_b.md")
        assert res_b["has_silicon_analogy"] is True
        assert res_b["mapped_comparisons"] == []

        res_c = extract_paper_silicon_analogy(p_dir / "paper_c.md")
        assert res_c["has_silicon_analogy"] is False

        # Matrix synthesis should render seamlessly with 8 columns
        doc = synthesize_comparison_matrix_doc(clean_vault)
        for line in doc.splitlines():
            if line.startswith("|") and line.endswith("|"):
                cells = _split_markdown_table_row(line)
                if not cells or "---" in cells[0]:
                    continue
                assert len(cells) == 8, f"Row column count mismatch: {line}"

    def test_latex_formula_escaping_in_tables(self, populated_vault):
        """Stress: LaTeX formulas with pipes, backslashes, superscripts must not break markdown table structure."""
        p = populated_vault / "Sources" / "Papers" / "2021_Liu_2D-Transistors.md"
        p.write_text("""---
type: paper
project: 2d-semiconductors
title: "2D Transistors with Math | $P(A|B)$ and $\\lambda < 1.5\\text{ nm}$"
citekey: "2021_Liu_2D-Transistors"
status: read
year: 2021
authors:
  - "Liu | Author 2"
venue: "Nature Electronics"
concepts:
  - "Knowledge/Concepts/monolayer_channel"
updated: 2026-08-20T12:00:00Z
---
# 2D Transistors with Math

## Claim
[CN]: 范德华接触势垒高度 $R_c \\approx 25\\ \\Omega\\cdot\\mu\\text{m}$ 且 $\\Delta V_{th} < 10\\text{ mV}$。

## Silicon Analogy & Microelectronics Mapping
- **Scaling vs GAAFET**: Model $|\\vec{E}| \\ge 10^6\\text{ V/cm}$ and $I_{on}/W > 1.5\\text{ mA}/\\mu\\text{m}$.
- **Mapped Comparisons**:
  - [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet|2D Scaling vs GAAFET]]
""", encoding="utf-8")

        doc = synthesize_comparison_matrix_doc(populated_vault)

        lines = doc.splitlines()
        for line in lines:
            if line.startswith("|") and line.endswith("|"):
                cells = _split_markdown_table_row(line)
                if not cells or "---" in cells[0]:
                    continue
                assert len(cells) in (5, 8), f"Malformed table row with {len(cells)} cols: {line}"

    def test_synthesis_successive_idempotency(self, populated_vault):
        """Stress: 5 successive synthesis runs must be 100% idempotent without bit drift or timestamp changes."""
        res1 = run_synthesis(populated_vault)
        assert len(res1) == 4

        matrix_path = populated_vault / "Writing" / "comparison-matrix.md"
        overview_path = populated_vault / "Knowledge" / "Literature Overview.md"
        taxonomy_path = populated_vault / "Knowledge" / "Method Taxonomy.md"
        gaps_path = populated_vault / "Knowledge" / "Research Gaps.md"

        content_matrix_1 = matrix_path.read_text(encoding="utf-8")
        content_overview_1 = overview_path.read_text(encoding="utf-8")
        content_taxonomy_1 = taxonomy_path.read_text(encoding="utf-8")
        content_gaps_1 = gaps_path.read_text(encoding="utf-8")

        for i in range(2, 6):
            res_i = run_synthesis(populated_vault)
            assert len(res_i) == 4

            assert matrix_path.read_text(encoding="utf-8") == content_matrix_1, f"Matrix drift on run {i}"
            assert overview_path.read_text(encoding="utf-8") == content_overview_1, f"Overview drift on run {i}"
            assert taxonomy_path.read_text(encoding="utf-8") == content_taxonomy_1, f"Taxonomy drift on run {i}"
            assert gaps_path.read_text(encoding="utf-8") == content_gaps_1, f"Gaps drift on run {i}"


class TestRegistryAndIndexAdversarial:
    """Adversarial stress-testing of registry.py and 02-Index.md."""

    def test_02_index_marker_stability_and_balance(self, populated_vault):
        """Stress: Verify that all auto-registry marker pairs exist, are balanced, and don't duplicate."""
        sync_registry(populated_vault)
        index_file = populated_vault / "02-Index.md"
        assert index_file.exists()

        content = index_file.read_text(encoding="utf-8")

        marker_pairs = [
            ("<!-- BEGIN AUTO REGISTRY: PAPERS_CARDS -->", "<!-- END AUTO REGISTRY: PAPERS_CARDS -->"),
            ("<!-- BEGIN AUTO REGISTRY: PAPERS -->", "<!-- END AUTO REGISTRY: PAPERS -->"),
            ("<!-- BEGIN AUTO REGISTRY: CONCEPTS_CARDS -->", "<!-- END AUTO REGISTRY: CONCEPTS_CARDS -->"),
            ("<!-- BEGIN AUTO REGISTRY: CONCEPTS -->", "<!-- END AUTO REGISTRY: CONCEPTS -->"),
            ("<!-- BEGIN AUTO REGISTRY: COMPARISONS_CARDS -->", "<!-- END AUTO REGISTRY: COMPARISONS_CARDS -->"),
            ("<!-- BEGIN AUTO REGISTRY: COMPARISONS -->", "<!-- END AUTO REGISTRY: COMPARISONS -->"),
        ]

        for begin_m, end_m in marker_pairs:
            begin_count = content.count(begin_m)
            end_count = content.count(end_m)
            assert begin_count == 1, f"Expected exactly 1 '{begin_m}', got {begin_count}"
            assert end_count == 1, f"Expected exactly 1 '{end_m}', got {end_count}"
            assert content.find(begin_m) < content.find(end_m), f"Marker order inverted for {begin_m}"

    def test_section_5_generation(self, populated_vault):
        """Stress: Section 5 must generate valid Bento cards and Comparison table."""
        sync_registry(populated_vault)
        index_content = (populated_vault / "02-Index.md").read_text(encoding="utf-8")

        # Check section 5 heading
        assert "## 💎 5. 硅基技术映射与对比矩阵 (Silicon Parallels & Comparison Benchmark)" in index_content
        # Check Bento callouts under Section 5
        assert "> [!example]+ ⚖️ [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet|2D Electrostatic Scaling vs Silicon GAAFET]]" in index_content
        assert "🏛️ **对标硅基技术节点**" in index_content
        assert "📚 **理论基石来源**" in index_content
        assert "🎯 **核心对照机制**" in index_content
        assert "🏷️ **状态评级**" in index_content
        # Check table
        assert "| 状态 Status | 对照卡片 Comparison Card | 对标硅基节点 Silicon Reference | 核心文献 Primary Sources | 证据级别 Strength |" in index_content
        assert "[[Writing/comparison-matrix|Literature Comparison Matrix (跨文献与硅基对标全景矩阵)]]" in index_content

    def test_empty_vault_index_generation(self, clean_vault):
        """Stress: sync_registry on completely empty vault should generate clean placeholders without breaking markers."""
        sync_registry(clean_vault)
        index_content = (clean_vault / "02-Index.md").read_text(encoding="utf-8")

        assert "0 篇" in index_content
        assert "0 个" in index_content
        assert "<!-- BEGIN AUTO REGISTRY: COMPARISONS_CARDS -->" in index_content
        assert "*暂无硅基对比卡片 / No comparison cards recorded yet.*" in index_content
        assert "<!-- BEGIN AUTO REGISTRY: COMPARISONS -->" in index_content
        assert "*暂无硅基对比矩阵 / No comparison table recorded yet.*" in index_content

    def test_bento_cards_missing_optional_fields(self, clean_vault):
        """Stress: Comparison cards missing primary_sources, silicon_reference_nodes, cn_title must render valid fallback Bento cards."""
        comp_dir = clean_vault / "Knowledge" / "Comparisons"
        comp_dir.mkdir(parents=True, exist_ok=True)
        (comp_dir / "minimal_comp.md").write_text("""---
type: comparison
title: "Minimal Comparison"
status: draft
claim_strength: speculative
updated: 2026-08-20T12:00:00Z
---
# Minimal Comparison
""", encoding="utf-8")

        comps = scan_comparison_notes(clean_vault)
        cards_output = generate_comparisons_cards(comps)
        table_output = generate_comparisons_table(comps)

        assert "> [!example]+ ⚖️ [[Knowledge/Comparisons/minimal_comp|Minimal Comparison]]" in cards_output
        assert "🏷️ **状态评级**：`🔬 Draft` ｜ **证据级别**: `Speculative`" in cards_output
        assert "- 🏛️ **对标硅基技术节点**：-" in cards_output
        assert "- 📚 **理论基石来源**：-" in cards_output

        assert "| `🔬 Draft` | [[Knowledge/Comparisons/minimal_comp|Minimal Comparison]] | - | - | `Speculative` |" in table_output

    def test_pipe_escaping_in_titles_and_authors(self, clean_vault):
        """Stress: Pipes (|) in paper/concept/comparison titles, authors, and nodes must be escaped in tables."""
        comp_dir = clean_vault / "Knowledge" / "Comparisons"
        comp_dir.mkdir(parents=True, exist_ok=True)
        (comp_dir / "pipe_test.md").write_text("""---
type: comparison
project: test
title: "Comparison with | Pipe in Title | Extra"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/test_paper]]"
silicon_reference_nodes:
  - "Node 1 | A14"
  - "Node 2 | A10"
dimensions_covered: [1, 2, 3, 4, 5, 6]
tags: [type/comparison, topic/silicon-analogy]
updated: 2026-08-20T12:00:00Z
---
# Comparison with Pipe
## Executive Overview & Silicon Analogy
## 1. Physical Scaling & Electrostatic Control
## 2. Ohmic Contact & Metallization Engineering
## 3. Gate Dielectric & EOT Scaling
## 4. CMOS Integration & Thermal Budget
## 5. IRDS Technology Roadmap Alignment
## 6. Electrical Benchmark & Compact Modeling Matrix
## References & Evidence Anchors
""", encoding="utf-8")

        comps = scan_comparison_notes(clean_vault)
        table_output = generate_comparisons_table(comps)

        lines = table_output.splitlines()
        for line in lines:
            if line.startswith("|") and line.endswith("|"):
                cells = _split_markdown_table_row(line)
                if not cells or "---" in cells[0]:
                    continue
                assert len(cells) == 5, f"Table row has broken pipe alignment: {line} -> cells: {cells}"

    def test_registry_successive_sync_idempotency(self, populated_vault):
        """Stress: 5 successive sync_registry runs must produce identical 02-Index.md and registry.md."""
        sync_registry(populated_vault)

        index_1 = (populated_vault / "02-Index.md").read_text(encoding="utf-8")
        reg_1 = (populated_vault / "_system" / "registry.md").read_text(encoding="utf-8")

        for i in range(2, 6):
            sync_registry(populated_vault)
            index_i = (populated_vault / "02-Index.md").read_text(encoding="utf-8")
            reg_i = (populated_vault / "_system" / "registry.md").read_text(encoding="utf-8")

            assert index_i == index_1, f"02-Index.md drift on sync {i}"
            assert reg_i == reg_1, f"_system/registry.md drift on sync {i}"


class TestCanvas4LaneAdversarial:
    """Adversarial stress-testing of 4-lane canvas generation."""

    def test_canvas_geometry_and_non_overlapping_layout(self, populated_vault):
        """Stress: Verify 4 lanes at X=0, 680, 1360, 2040 with non-overlapping bounding boxes."""
        canvas_path = generate_canvas_file(populated_vault)
        assert canvas_path.exists()

        data = json.loads(canvas_path.read_text(encoding="utf-8"))
        assert "nodes" in data
        assert "edges" in data

        file_nodes = [n for n in data["nodes"] if n.get("type") == "file"]
        group_nodes = [n for n in data["nodes"] if n.get("type") == "group"]

        expected_lane_xs = {0, 680, 1360, 2040}
        actual_lane_xs = {n["x"] for n in file_nodes}
        assert actual_lane_xs.issubset(expected_lane_xs)

        comp_nodes = [n for n in file_nodes if n["x"] == 1360]
        assert len(comp_nodes) >= 1
        for cn in comp_nodes:
            assert cn["width"] == 460
            assert cn["height"] == 340
            assert cn["color"] == COLOR_SILICON

        for lane_x in expected_lane_xs:
            lane_file_nodes = [n for n in file_nodes if n["x"] == lane_x]
            sorted_nodes = sorted(lane_file_nodes, key=lambda n: n["y"])
            for i in range(len(sorted_nodes) - 1):
                n1 = sorted_nodes[i]
                n2 = sorted_nodes[i + 1]
                assert n1["y"] + n1["height"] <= n2["y"], f"Overlap detected between {n1['file']} and {n2['file']} in lane X={lane_x}"

        expected_group_xs = {-40, 640, 1320, 2000}
        for g in group_nodes:
            assert g["x"] in expected_group_xs
            assert g["width"] == 540

        node_ids = {n["id"] for n in data["nodes"]}
        for edge in data["edges"]:
            assert edge["fromNode"] in node_ids, f"Edge fromNode {edge['fromNode']} not in nodes"
            assert edge["toNode"] in node_ids, f"Edge toNode {edge['toNode']} not in nodes"
            assert edge["fromSide"] in {"left", "right", "top", "bottom"}
            assert edge["toSide"] in {"left", "right", "top", "bottom"}
            assert edge["toEnd"] == "arrow"

    def test_canvas_hidden_node_exclusion(self, clean_vault):
        """Stress: Notes with canvas_visibility: hidden must be excluded from canvas nodes and edges."""
        p = clean_vault / "Sources" / "Papers" / "hidden_paper.md"
        p.write_text("""---
type: paper
title: "Hidden Paper"
citekey: hidden_paper
canvas_visibility: hidden
updated: 2026-08-20T12:00:00Z
---
# Hidden
""", encoding="utf-8")

        p2 = clean_vault / "Sources" / "Papers" / "visible_paper.md"
        p2.write_text("""---
type: paper
title: "Visible Paper"
citekey: visible_paper
updated: 2026-08-20T12:00:00Z
---
# Visible
""", encoding="utf-8")

        canvas_path = generate_canvas_file(clean_vault)
        data = json.loads(canvas_path.read_text(encoding="utf-8"))

        file_paths = [n.get("file") for n in data["nodes"] if n.get("type") == "file"]
        assert "Sources/Papers/hidden_paper.md" not in file_paths
        assert "Sources/Papers/visible_paper.md" in file_paths

    def test_canvas_streamline_with_dense_vault(self, clean_vault):
        """Stress: Generate canvas with 10 papers, 10 concepts, 10 comparisons, 3 syntheses without overlapping."""
        for i in range(10):
            p = clean_vault / "Sources" / "Papers" / f"paper_{i:02d}.md"
            p.write_text(f"""---
type: paper
project: test
title: "Paper {i}"
citekey: paper_{i:02d}
status: read
concepts: ["Knowledge/Concepts/concept_{i:02d}"]
updated: 2026-08-20T12:00:00Z
---
# Paper {i}
""", encoding="utf-8")

        for i in range(10):
            c = clean_vault / "Knowledge" / "Concepts" / f"concept_{i:02d}.md"
            c.write_text(f"""---
type: concept
project: test
title: "Concept {i}"
primary_sources: ["[[Sources/Papers/paper_{i:02d}]]"]
updated: 2026-08-20T12:00:00Z
---
# Concept {i}
""", encoding="utf-8")

        for i in range(10):
            comp = clean_vault / "Knowledge" / "Comparisons" / f"comparison_{i:02d}.md"
            comp.write_text(f"""---
type: comparison
project: test
title: "Comparison {i}"
primary_sources: ["[[Sources/Papers/paper_{i:02d}]]"]
silicon_reference_nodes: ["Node {i}"]
dimensions_covered: [1, 2, 3, 4, 5, 6]
tags: [type/comparison, topic/silicon-analogy]
updated: 2026-08-20T12:00:00Z
---
# Comparison {i}
""", encoding="utf-8")

        (clean_vault / "Knowledge" / "Literature Overview.md").write_text("""---
type: literature-synthesis
title: "Literature Overview"
updated: 2026-08-20T12:00:00Z
---
# Overview
""", encoding="utf-8")
        (clean_vault / "Knowledge" / "Method Taxonomy.md").write_text("""---
type: method-taxonomy
title: "Method Taxonomy"
updated: 2026-08-20T12:00:00Z
---
# Taxonomy
""", encoding="utf-8")
        (clean_vault / "Knowledge" / "Research Gaps.md").write_text("""---
type: research-gaps
title: "Research Gaps"
updated: 2026-08-20T12:00:00Z
---
# Gaps
""", encoding="utf-8")

        canvas_path = generate_canvas_file(clean_vault)
        data = json.loads(canvas_path.read_text(encoding="utf-8"))

        file_nodes = [n for n in data["nodes"] if n.get("type") == "file"]
        assert len(file_nodes) == 33  # 10 + 10 + 10 + 3

        for col_x in [0, 680, 1360, 2040]:
            nodes_in_col = sorted([n for n in file_nodes if n["x"] == col_x], key=lambda n: n["y"])
            for j in range(len(nodes_in_col) - 1):
                a = nodes_in_col[j]
                b = nodes_in_col[j + 1]
                assert a["y"] + a["height"] <= b["y"], f"Collision in column {col_x}: {a['file']} overlaps {b['file']}"


class TestLiveRepoEndToEndVerification:
    """Empirical verification on the actual live repository."""

    def test_live_vault_pipeline_run(self):
        """Verify kb-tools run-pipeline executes on actual repo with exit code 0."""
        repo_root = Path(__file__).resolve().parent.parent
        exit_code = cli_main(["run-pipeline", "--vault-dir", str(repo_root), "--strict"])
        assert exit_code == 0, "Master pipeline run-pipeline failed on live repository"

    def test_live_02_index_has_section_5_and_markers(self):
        """Verify 02-Index.md in live repo contains Section 5 and all required markers."""
        repo_root = Path(__file__).resolve().parent.parent
        index_file = repo_root / "02-Index.md"
        assert index_file.exists()

        content = index_file.read_text(encoding="utf-8")
        assert "## 💎 5. 硅基技术映射与对比矩阵 (Silicon Parallels & Comparison Benchmark)" in content
        assert "<!-- BEGIN AUTO REGISTRY: COMPARISONS_CARDS -->" in content
        assert "<!-- END AUTO REGISTRY: COMPARISONS_CARDS -->" in content
        assert "<!-- BEGIN AUTO REGISTRY: COMPARISONS -->" in content
        assert "<!-- END AUTO REGISTRY: COMPARISONS -->" in content
        assert "[[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide" in content
        assert "[[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet" in content

    def test_live_literature_canvas_is_valid_4_lane(self):
        """Verify Maps/literature.canvas in live repo conforms to 4-lane layout with cyan comparisons."""
        repo_root = Path(__file__).resolve().parent.parent
        canvas_file = repo_root / "Maps" / "literature.canvas"
        assert canvas_file.exists()

        data = json.loads(canvas_file.read_text(encoding="utf-8"))
        nodes = data["nodes"]
        file_nodes = [n for n in nodes if n.get("type") == "file"]

        lane_xs = {n["x"] for n in file_nodes}
        assert 1360 in lane_xs, "Lane 3 (X=1360) missing from literature.canvas"

        comp_nodes = [n for n in file_nodes if n["x"] == 1360]
        assert len(comp_nodes) == 2, f"Expected 2 comparison nodes in Lane 3, found {len(comp_nodes)}"
        for cn in comp_nodes:
            assert cn["color"] == COLOR_SILICON
            assert "Knowledge/Comparisons" in cn["file"]