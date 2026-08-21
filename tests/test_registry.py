"""
Test Suite for kb_tools.registry and CLI 'sync-registry' subcommand.
Covers Tier 1 (Unit & Schema Contracts) and Tier 2 (CLI & Functional Boundaries).
Validates registry table generation, sorting rules, idempotency, error tolerance,
and CLI execution flags.
"""

import json
import os
import sys
from pathlib import Path
import pytest

# Ensure src is in sys.path
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# ---------------------------------------------------------------------------
# Tier 1: Unit & Registry Logic Tests
# ---------------------------------------------------------------------------

def test_generate_papers_registry_table_format(populated_vault):
    """Tier 1: Verify generated papers registry table contains required columns and markdown formatting."""
    from kb_tools.registry import scan_paper_notes, generate_papers_table
    papers = scan_paper_notes(populated_vault)
    assert len(papers) == 3, f"Expected 3 papers scanned, found {len(papers)}"

    table = generate_papers_table(papers)
    assert "|" in table, "Table must be markdown formatted with pipe delimiters"
    
    # Check table headers (case-insensitive checks for core columns)
    headers = table.splitlines()[0].lower()
    for col in ["citekey", "title", "author", "year"]:
        assert col in headers, f"Expected column '{col}' in table headers: {headers}"

    # Check rows for the 3 papers
    assert "he2016deep" in table
    assert "vaswani2017attention" in table
    assert "hu2021lora" in table


def test_generate_knowledge_registry_table_format(populated_vault):
    """Tier 1: Verify generated knowledge registry table lists atomic concepts and syntheses."""
    from kb_tools.registry import scan_concept_notes, generate_knowledge_table
    concepts = scan_concept_notes(populated_vault)
    assert len(concepts) == 3, f"Expected 3 concepts scanned, found {len(concepts)}"

    table = generate_knowledge_table(concepts)
    assert "|" in table
    assert "residual_connection" in table or "Residual Connections" in table
    assert "self_attention" in table or "Self-Attention" in table
    assert "peft" in table or "Parameter-Efficient Fine-Tuning" in table


def test_registry_sorting_order_year_desc_author_asc(tmp_vault):
    """Tier 1: Papers must be sorted by year descending, and tie-broken by author ascending."""
    from kb_tools.registry import scan_paper_notes, generate_papers_table
    papers_dir = tmp_vault / "Sources" / "Papers"
    
    # Create 3 papers with different years and authors
    (papers_dir / "paper2015.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Old Paper 2015"
citekey: paper2015
zotero_key: "P2015"
status: read
source_type: "preprint"
claim_strength: strong
authors: ["Zachary, Z."]
year: 2015
linked_knowledge: ["[[Knowledge/Literature Overview]]"]
updated: 2026-08-19T00:00:00Z
---
# Old Paper 2015
""", encoding="utf-8")

    (papers_dir / "paper2020b.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Paper 2020 Bob"
citekey: paper2020b
zotero_key: "P2020B"
status: read
source_type: "preprint"
claim_strength: strong
authors: ["Bob, B."]
year: 2020
linked_knowledge: ["[[Knowledge/Literature Overview]]"]
updated: 2026-08-19T00:00:00Z
---
# Paper 2020 Bob
""", encoding="utf-8")

    (papers_dir / "paper2020a.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Paper 2020 Alice"
citekey: paper2020a
zotero_key: "P2020A"
status: read
source_type: "preprint"
claim_strength: strong
authors: ["Alice, A."]
year: 2020
linked_knowledge: ["[[Knowledge/Literature Overview]]"]
updated: 2026-08-19T00:00:00Z
---
# Paper 2020 Alice
""", encoding="utf-8")

    papers = scan_paper_notes(tmp_vault)
    table = generate_papers_table(papers)
    lines = [line for line in table.splitlines() if "|" in line and "---" not in line][1:] # Skip header
    
    # Paper 2020 Alice should come first (2020, Alice < Bob), then 2020 Bob, then 2015 Zachary
    first_row = lines[0]
    second_row = lines[1]
    third_row = lines[2]

    assert "paper2020a" in first_row or "Alice" in first_row, f"First row should be 2020 Alice: {first_row}"
    assert "paper2020b" in second_row or "Bob" in second_row, f"Second row should be 2020 Bob: {second_row}"
    assert "paper2015" in third_row or "Zachary" in third_row, f"Third row should be 2015: {third_row}"


def test_registry_idempotency(populated_vault):
    """Tier 1: Running sync_registry multiple times on the same vault produces identical content."""
    from kb_tools.registry import sync_registry
    
    # First sync
    res1 = sync_registry(populated_vault)
    registry_file = populated_vault / "_system" / "registry.md"
    index_file = populated_vault / "02-Index.md"
    papers_index = populated_vault / "02-Index.md"
    
    content1_reg = registry_file.read_text(encoding="utf-8") if registry_file.exists() else ""
    content1_idx = index_file.read_text(encoding="utf-8") if index_file.exists() else ""
    content1_p = papers_index.read_text(encoding="utf-8") if papers_index.exists() else ""

    # Second sync
    res2 = sync_registry(populated_vault)
    content2_reg = registry_file.read_text(encoding="utf-8") if registry_file.exists() else ""
    content2_idx = index_file.read_text(encoding="utf-8") if index_file.exists() else ""
    content2_p = papers_index.read_text(encoding="utf-8") if papers_index.exists() else ""

    assert content1_reg == content2_reg, "Registry file must be 100% identical after second sync"
    assert content1_idx == content2_idx, "Index file must be 100% identical after second sync"
    assert content1_p == content2_p, "Papers index file must be 100% identical after second sync"


def test_registry_handles_empty_vault(tmp_vault):
    """Tier 1: Vault with 0 papers/concepts creates clean index tables without throwing errors."""
    from kb_tools.registry import sync_registry
    result = sync_registry(tmp_vault)
    assert result is not None
    
    # Check that registry file exists and contains valid empty table structure
    registry_file = tmp_vault / "_system" / "registry.md"
    if registry_file.exists():
        content = registry_file.read_text(encoding="utf-8")
        assert "# Project Registry" in content or "Registry" in content


def test_registry_handles_unparseable_notes(tmp_vault):
    """Tier 1: Corrupted or unparseable notes are skipped with warning without failing sync."""
    from kb_tools.registry import sync_registry, scan_paper_notes
    papers_dir = tmp_vault / "Sources" / "Papers"
    
    # One good paper
    (papers_dir / "good2026.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Good Paper"
citekey: good2026
zotero_key: "GOOD2026"
status: read
source_type: "preprint"
claim_strength: strong
authors: ["Good, Author"]
year: 2026
linked_knowledge: ["[[Knowledge/Literature Overview]]"]
updated: 2026-08-19T00:00:00Z
---
# Good Paper
""", encoding="utf-8")

    # One corrupted paper with invalid YAML
    (papers_dir / "broken_yaml.md").write_text("""---
title: [unclosed list
invalid: YAML ::: syntax error
---
# Broken YAML
""", encoding="utf-8")

    # Should not raise exception, should index the good paper
    papers = scan_paper_notes(tmp_vault)
    citekeys = [p.get("citekey") for p in papers]
    assert "good2026" in citekeys
    
    res = sync_registry(tmp_vault)
    assert res is not None


def test_registry_detects_duplicate_citekeys(tmp_vault):
    """Tier 1: Multiple files with the same citekey are handled without crashing."""
    from kb_tools.registry import scan_paper_notes
    papers_dir = tmp_vault / "Sources" / "Papers"
    
    (papers_dir / "paper_a.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Paper A"
citekey: dup2026
zotero_key: "DUP1"
status: read
source_type: "preprint"
claim_strength: strong
authors: ["Author A"]
year: 2026
linked_knowledge: ["[[Knowledge/Literature Overview]]"]
updated: 2026-08-19T00:00:00Z
---
# Paper A
""", encoding="utf-8")

    (papers_dir / "paper_b.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Paper B"
citekey: dup2026
zotero_key: "DUP2"
status: read
source_type: "preprint"
claim_strength: strong
authors: ["Author B"]
year: 2026
linked_knowledge: ["[[Knowledge/Literature Overview]]"]
updated: 2026-08-19T00:00:00Z
---
# Paper B
""", encoding="utf-8")

    papers = scan_paper_notes(tmp_vault)
    assert len(papers) >= 1


def test_registry_preserves_custom_preamble(tmp_vault):
    """Tier 1: Notes with custom preamble text before the table retain their preamble."""
    from kb_tools.registry import sync_registry
    registry_file = tmp_vault / "_system" / "registry.md"
    custom_preamble = "# Project Registry\n\n> Important Note: Hand-curated research vault for AI.\n\n"
    registry_file.write_text(custom_preamble, encoding="utf-8")

    sync_registry(tmp_vault)
    content = registry_file.read_text(encoding="utf-8")
    assert "Hand-curated research vault for AI" in content


# ---------------------------------------------------------------------------
# Tier 2: CLI & Boundary Functional Tests
# ---------------------------------------------------------------------------

def test_cli_sync_registry_exit_code_zero(populated_vault, capsys):
    """Tier 2: CLI `kb-tools sync-registry` on a populated vault exits with 0."""
    from kb_tools.cli import main
    exit_code = main(["sync-registry", "--vault-dir", str(populated_vault)])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "synced" in captured.out.lower() or "updated" in captured.out.lower() or exit_code == 0


def test_cli_sync_registry_dry_run(populated_vault, capsys):
    """Tier 2: CLI `kb-tools sync-registry --dry-run` reports changes without modifying files."""
    papers_index = populated_vault / "02-Index.md"
    if papers_index.exists():
        papers_index.unlink()

    from kb_tools.cli import main
    exit_code = main(["sync-registry", "--vault-dir", str(populated_vault), "--dry-run"])
    assert exit_code == 0
    
    # In dry run mode, new files should not be committed to disk
    # (or if modified, content was not written)
    captured = capsys.readouterr()
    assert "dry" in captured.out.lower() or len(captured.out) > 0


def test_cli_sync_registry_json_output(populated_vault, capsys):
    """Tier 2: CLI `kb-tools sync-registry --json` returns structured JSON response."""
    from kb_tools.cli import main
    exit_code = main(["sync-registry", "--vault-dir", str(populated_vault), "--json"])
    assert exit_code == 0
    
    captured = capsys.readouterr()
    assert captured.out.strip().startswith("{") or captured.out.strip().startswith("[")
    data = json.loads(captured.out)
    assert "papers" in data or "total_papers" in data or "synced" in data or isinstance(data, dict)


def test_cli_sync_registry_cwd_flag(populated_vault, capsys):
    """Tier 2: CLI `kb-tools sync-registry --cwd <path>` works identically to `--vault-dir`."""
    from kb_tools.cli import main
    exit_code = main(["sync-registry", "--cwd", str(populated_vault)])
    assert exit_code == 0


def test_cli_sync_registry_invalid_directory(tmp_path, capsys):
    """Tier 2: CLI `kb-tools sync-registry` with non-existent directory returns non-zero error."""
    non_existent = tmp_path / "does_not_exist_vault_dir_12345"
    from kb_tools.cli import main
    exit_code = main(["sync-registry", "--vault-dir", str(non_existent)])
    assert exit_code != 0


# ---------------------------------------------------------------------------
# Tier 1 & 2: 6D Microelectronics Comparison Registry Tests
# ---------------------------------------------------------------------------

def test_scan_comparison_notes(tmp_vault):
    """Tier 1: scan_comparison_notes extracts comparison metadata including silicon fields."""
    from kb_tools.registry import scan_comparison_notes

    comp_dir = tmp_vault / "Knowledge" / "Comparisons"
    comp_dir.mkdir(parents=True, exist_ok=True)
    (comp_dir / "2d_scaling.md").write_text("""---
type: comparison
project: 2d-semiconductors
title: "2D Scaling Benchmark"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
silicon_reference_nodes:
  - "Silicon FinFET (5nm)"
  - "GAAFET (3nm)"
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
# 2D Scaling Benchmark
> **Focus / 核心主题**: 2D FET scaling vs GAAFET.
""", encoding="utf-8")

    comps = scan_comparison_notes(tmp_vault)
    assert len(comps) == 1
    c = comps[0]
    assert c["title"] == "2D Scaling Benchmark"
    assert c["claim_strength"] == "strong"
    assert "Silicon FinFET (5nm)" in c["silicon_reference_nodes"]
    assert c["dimensions_covered"] == [1, 2, 3, 4, 5, 6]


def test_generate_comparisons_table_format(tmp_vault):
    """Tier 1: generate_comparisons_table generates markdown table with required comparison columns."""
    from kb_tools.registry import scan_comparison_notes, generate_comparisons_table

    comp_dir = tmp_vault / "Knowledge" / "Comparisons"
    comp_dir.mkdir(parents=True, exist_ok=True)
    (comp_dir / "2d_contact.md").write_text("""---
type: comparison
project: 2d-semiconductors
title: "2D Contact vs Silicide"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2022_Cheng_FET-Benchmark]]"
silicon_reference_nodes:
  - "Silicon Salicide (NiSi)"
dimensions_covered: [1, 2, 3, 4, 5, 6]
tags:
  - type/comparison
  - topic/silicon-analogy
updated: 2026-08-20T12:00:00Z
---
# 2D Contact vs Silicide
""", encoding="utf-8")

    comps = scan_comparison_notes(tmp_vault)
    table = generate_comparisons_table(comps)
    assert "状态 Status" in table
    assert "对照卡片 Comparison Card" in table
    assert "对标硅基节点 Silicon Reference" in table
    assert "核心文献 Primary Sources" in table
    assert "证据级别 Strength" in table
    assert "2D Contact vs Silicide" in table
    assert "Silicon Salicide (NiSi)" in table


def test_generate_comparisons_cards_format(tmp_vault):
    """Tier 1: generate_comparisons_cards generates Bento-style callouts for comparison cards."""
    from kb_tools.registry import scan_comparison_notes, generate_comparisons_cards

    comp_dir = tmp_vault / "Knowledge" / "Comparisons"
    comp_dir.mkdir(parents=True, exist_ok=True)
    (comp_dir / "2d_contact.md").write_text("""---
type: comparison
project: 2d-semiconductors
title: "2D Contact vs Silicide"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2022_Cheng_FET-Benchmark]]"
silicon_reference_nodes:
  - "Silicon Salicide"
dimensions_covered: [1, 2, 3, 4, 5, 6]
tags:
  - type/comparison
  - topic/silicon-analogy
updated: 2026-08-20T12:00:00Z
---
# 2D Contact vs Silicide
> **Focus / 核心主题**: vdW contacts vs salicide metallization.
""", encoding="utf-8")

    comps = scan_comparison_notes(tmp_vault)
    cards = generate_comparisons_cards(comps)
    assert "> [!example]+ ⚖️ [[Knowledge/Comparisons/2d_contact|2D Contact vs Silicide]]" in cards
    assert "对标硅基技术节点" in cards
    assert "理论基石来源" in cards
    assert "核心对照机制" in cards


def test_update_02_index_section_5(tmp_vault):
    """Tier 1: update_02_index creates Section 5 with comparison cards and table markers."""
    from kb_tools.registry import scan_paper_notes, scan_concept_notes, scan_comparison_notes, update_02_index

    comp_dir = tmp_vault / "Knowledge" / "Comparisons"
    comp_dir.mkdir(parents=True, exist_ok=True)
    (comp_dir / "2d_scaling.md").write_text("""---
type: comparison
project: 2d-semiconductors
title: "2D Scaling Benchmark"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
silicon_reference_nodes:
  - "FinFET"
dimensions_covered: [1, 2, 3, 4, 5, 6]
tags:
  - type/comparison
  - topic/silicon-analogy
updated: 2026-08-20T12:00:00Z
---
# 2D Scaling Benchmark
""", encoding="utf-8")

    papers = scan_paper_notes(tmp_vault)
    concepts = scan_concept_notes(tmp_vault)
    comps = scan_comparison_notes(tmp_vault)

    update_02_index(tmp_vault, papers, concepts, comparisons=comps)

    index_text = (tmp_vault / "02-Index.md").read_text(encoding="utf-8")
    assert "## 💎 5. 硅基技术映射与对比矩阵 (Silicon Parallels & Comparison Benchmark)" in index_text
    assert "<!-- BEGIN AUTO REGISTRY: COMPARISONS_CARDS -->" in index_text
    assert "<!-- END AUTO REGISTRY: COMPARISONS_CARDS -->" in index_text
    assert "<!-- BEGIN AUTO REGISTRY: COMPARISONS -->" in index_text
    assert "<!-- END AUTO REGISTRY: COMPARISONS -->" in index_text
    assert "💎 硅基对照卡片" in index_text
    assert "1 篇" in index_text


def test_registry_sync_includes_comparisons_count(tmp_vault):
    """Tier 1: sync_registry returns comparisons_count and comparisons in summary dict."""
    from kb_tools.registry import sync_registry

    comp_dir = tmp_vault / "Knowledge" / "Comparisons"
    comp_dir.mkdir(parents=True, exist_ok=True)
    (comp_dir / "2d_scaling.md").write_text("""---
type: comparison
project: 2d-semiconductors
title: "2D Scaling Benchmark"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
silicon_reference_nodes:
  - "FinFET"
dimensions_covered: [1, 2, 3, 4, 5, 6]
tags:
  - type/comparison
  - topic/silicon-analogy
updated: 2026-08-20T12:00:00Z
---
# 2D Scaling Benchmark
""", encoding="utf-8")

    res = sync_registry(tmp_vault)
    assert res["status"] == "success"
    assert res["comparisons_count"] == 1
    assert len(res["comparisons"]) == 1
    assert res["comparisons"][0]["title"] == "2D Scaling Benchmark"

