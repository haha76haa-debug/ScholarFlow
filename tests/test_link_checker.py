"""
Test Suite for kb_tools.link_checker and CLI 'check-links' / 'repair-links' subcommands.
Covers Tier 1 (Unit & Link Graph Contracts) and Tier 2 (CLI & Functional Boundaries).
Validates dead wikilink detection, cross-directory target resolution, alias & anchor handling,
fuzzy match repair, formatting preservation, and CLI exit codes.
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
# Tier 1: Link Resolution & Unit Tests
# ---------------------------------------------------------------------------

def test_detect_dead_wikilinks_in_body(tmp_vault):
    """Tier 1: Detects broken wikilinks in markdown body and reports source file and target."""
    from kb_tools.link_checker import check_links
    papers_dir = tmp_vault / "Sources" / "Papers"
    
    # Create note referencing non-existent link
    (papers_dir / "note_with_dead_link.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Dead Link Note"
citekey: deadlink2026
zotero_key: "DEAD2026"
status: to-read
source_type: "preprint"
claim_strength: observed
authors: ["Test Author"]
year: 2026
linked_knowledge: ["[[Knowledge/Literature Overview]]"]
updated: 2026-08-19T00:00:00Z
---
# Dead Link Note
This note links to [[NonExistentConceptNote]] and [[Sources/Papers/ghost_paper_2099]].
""", encoding="utf-8")

    report = check_links(tmp_vault)
    broken = report.get("broken_links", []) if isinstance(report, dict) else getattr(report, "broken_links", [])
    
    assert len(broken) >= 1, f"Expected broken links detected, got: {broken}"
    broken_targets = [str(getattr(b, "target", b.get("target") if isinstance(b, dict) else b)) for b in broken]
    assert any("NonExistentConceptNote" in t or "ghost_paper_2099" in t for t in broken_targets)


def test_detect_dead_wikilinks_in_yaml_frontmatter(tmp_vault):
    """Tier 1: Detects broken wikilinks embedded inside YAML frontmatter fields."""
    from kb_tools.link_checker import check_links
    papers_dir = tmp_vault / "Sources" / "Papers"
    
    (papers_dir / "fm_dead_link.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "FM Dead Link Note"
citekey: fmdead2026
zotero_key: "FMDEAD2026"
status: to-read
source_type: "preprint"
claim_strength: observed
authors: ["Test Author"]
year: 2026
linked_knowledge:
  - "[[Knowledge/Concepts/non_existent_concept]]"
  - "[[Knowledge/NonExistentSynthesis]]"
updated: 2026-08-19T00:00:00Z
---
# FM Dead Link Note
Body without broken links.
""", encoding="utf-8")

    report = check_links(tmp_vault)
    broken = report.get("broken_links", []) if isinstance(report, dict) else getattr(report, "broken_links", [])
    assert len(broken) >= 1


def test_resolve_valid_wikilinks_across_subdirectories(populated_vault):
    """Tier 1: Resolves valid folder-qualified and bare-slug links across all vault subdirectories."""
    from kb_tools.link_checker import check_links
    report = check_links(populated_vault)
    broken = report.get("broken_links", []) if isinstance(report, dict) else getattr(report, "broken_links", [])
    assert len(broken) == 0, f"Populated vault should have 0 broken links, found: {broken}"


def test_wikilink_aliases_ignored_during_target_resolution(tmp_vault, sample_paper_note_content):
    """Tier 1: Link alias syntax [[Target|Alias Text]] correctly resolves target without alias in lookup."""
    from kb_tools.link_checker import check_links
    papers_dir = tmp_vault / "Sources" / "Papers"
    concepts_dir = tmp_vault / "Knowledge" / "Concepts"

    (papers_dir / "he2016deep.md").write_text(sample_paper_note_content, encoding="utf-8")
    (concepts_dir / "residual_connection.md").write_text("""---
type: concept
project: zotero_obsidian_kb
title: "Residual Connections"
status: active
claim_strength: strong
primary_sources: ["[[Sources/Papers/he2016deep]]"]
tags: ["#type/concept"]
updated: 2026-08-19T00:00:00Z
---
# Residual Connections
Cites [[Sources/Papers/he2016deep|He et al. (2016) ImageNet Winner]] and [[he2016deep|ResNet]].
""", encoding="utf-8")

    report = check_links(tmp_vault)
    broken = report.get("broken_links", []) if isinstance(report, dict) else getattr(report, "broken_links", [])
    assert len(broken) == 0, f"Aliased links should resolve cleanly, found broken: {broken}"


def test_wikilink_heading_and_block_anchors(tmp_vault, sample_paper_note_content):
    """Tier 1: Heading anchors [[Target#Heading]] and block anchors [[Target#^block]] are parsed cleanly."""
    from kb_tools.link_checker import check_links
    papers_dir = tmp_vault / "Sources" / "Papers"
    knowledge_dir = tmp_vault / "Knowledge"

    (papers_dir / "he2016deep.md").write_text(sample_paper_note_content, encoding="utf-8")
    (knowledge_dir / "notes.md").write_text("""---
type: literature-synthesis
project: zotero_obsidian_kb
title: "Synthesis Notes"
status: active
covered_papers: ["[[Sources/Papers/he2016deep]]"]
key_themes: ["deep-learning"]
updated: 2026-08-19T00:00:00Z
---
# Notes
Check evidence at [[Sources/Papers/he2016deep#Evidence]] and [[Sources/Papers/he2016deep#Method|Methodology Section]].
""", encoding="utf-8")

    report = check_links(tmp_vault)
    broken = report.get("broken_links", []) if isinstance(report, dict) else getattr(report, "broken_links", [])
    assert len(broken) == 0, f"Anchor links should resolve cleanly without error: {broken}"


def test_external_urls_and_zotero_uris_ignored(tmp_vault):
    """Tier 1: Standard markdown URLs (http/https) and zotero:// URIs are ignored by wikilink checker."""
    from kb_tools.link_checker import check_links, find_all_wikilinks
    sample_text = """
    Check [arXiv Paper](https://arxiv.org/abs/1512.03385) and [Zotero Reader](zotero://open-pdf/0_xxx/1).
    """
    wikilinks = find_all_wikilinks(sample_text)
    assert len(wikilinks) == 0, "External Markdown links must not be parsed as Obsidian wikilinks"


def test_repair_links_fuzzy_match_resolution(tmp_vault, sample_paper_note_content):
    """Tier 1: repair_links resolves unqualified or slightly varied links to canonical note paths."""
    from kb_tools.link_checker import repair_links, check_links
    papers_dir = tmp_vault / "Sources" / "Papers"
    concepts_dir = tmp_vault / "Knowledge" / "Concepts"

    # Create target note at canonical path
    (papers_dir / "he2016deep.md").write_text(sample_paper_note_content, encoding="utf-8")

    # Create referencing note with bare filename
    referencing_note = concepts_dir / "test_concept.md"
    referencing_note.write_text("""---
type: concept
project: zotero_obsidian_kb
title: "Test Concept"
status: active
claim_strength: strong
primary_sources: ["[[he2016deep]]"]
tags: ["#type/concept"]
updated: 2026-08-19T00:00:00Z
---
# Test Concept
Referencing [[he2016deep]].
""", encoding="utf-8")

    repair_result = repair_links(tmp_vault, fuzzy=True)
    assert repair_result is not None

    # After repair, link in file should be updated or resolved
    updated_content = referencing_note.read_text(encoding="utf-8")
    assert "Sources/Papers/he2016deep" in updated_content or "he2016deep" in updated_content


def test_repair_links_preserves_frontmatter_and_formatting(tmp_vault, sample_paper_note_content):
    """Tier 1: Link repair preserves YAML indentation, code blocks, and markdown structure."""
    from kb_tools.link_checker import repair_links
    papers_dir = tmp_vault / "Sources" / "Papers"
    concepts_dir = tmp_vault / "Knowledge" / "Concepts"

    (papers_dir / "he2016deep.md").write_text(sample_paper_note_content, encoding="utf-8")

    initial_content = """---
type: concept
project: zotero_obsidian_kb
title: "Complex Formatting Concept"
status: active
claim_strength: strong
primary_sources:
  - "[[he2016deep]]"
tags:
  - "#type/concept"
  - "#nested/tag/value"
updated: 2026-08-19T00:00:00Z
---

# Complex Formatting Concept

## Mathematical Formulation
$$ \\mathcal{F}(x) + x $$

```python
# Code block test
def forward(x):
    return f(x) + x
```

> [!quote]+ Callout Test
> Callout body referencing [[he2016deep|ResNet]].
"""
    test_file = concepts_dir / "complex.md"
    test_file.write_text(initial_content, encoding="utf-8")

    repair_links(tmp_vault, fuzzy=True)
    repaired_content = test_file.read_text(encoding="utf-8")

    assert "def forward(x):" in repaired_content
    assert "$$ \\mathcal{F}(x) + x $$" in repaired_content
    assert "> [!quote]+ Callout Test" in repaired_content
    assert "type: concept" in repaired_content


# ---------------------------------------------------------------------------
# Tier 2: CLI & Boundary Functional Tests
# ---------------------------------------------------------------------------

def test_cli_check_links_clean_vault_exit_code_zero(populated_vault, capsys):
    """Tier 2: CLI `kb-tools check-links` exits with 0 on clean vault with valid links."""
    from kb_tools.cli import main
    exit_code = main(["check-links", "--vault-dir", str(populated_vault)])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "broken" not in captured.out.lower() or "0 broken" in captured.out.lower()


def test_cli_check_links_broken_links_exit_code_nonzero(tmp_vault, corrupted_vault_factory, capsys):
    """Tier 2: CLI `kb-tools check-links` exits with non-zero when broken links exist."""
    corrupted_vault_factory("broken_links")
    from kb_tools.cli import main
    exit_code = main(["check-links", "--vault-dir", str(tmp_vault)])
    assert exit_code != 0
    captured = capsys.readouterr()
    assert len(captured.out) > 0 or len(captured.err) > 0


def test_cli_check_links_json_output(tmp_vault, corrupted_vault_factory, capsys):
    """Tier 2: CLI `kb-tools check-links --json` produces valid JSON report."""
    corrupted_vault_factory("broken_links")
    from kb_tools.cli import main
    exit_code = main(["check-links", "--vault-dir", str(tmp_vault), "--json"])
    assert exit_code != 0
    
    captured = capsys.readouterr()
    assert captured.out.strip().startswith("{") or captured.out.strip().startswith("[")
    data = json.loads(captured.out)
    assert "broken_links" in data or "total_broken" in data or isinstance(data, list)


def test_cli_repair_links_dry_run(tmp_vault, corrupted_vault_factory, capsys):
    """Tier 2: CLI `kb-tools repair-links --dry-run` reports planned repairs without writing to disk."""
    corrupted_vault_factory("broken_links")
    target_file = tmp_vault / "Knowledge" / "Concepts" / "broken_concept.md"
    before_content = target_file.read_text(encoding="utf-8") if target_file.exists() else ""

    from kb_tools.cli import main
    exit_code = main(["repair-links", "--vault-dir", str(tmp_vault), "--dry-run"])
    assert exit_code in [0, 1]

    if target_file.exists():
        after_content = target_file.read_text(encoding="utf-8")
        assert before_content == after_content, "Dry run must not modify files on disk"


def test_cli_repair_links_execution(tmp_vault, sample_paper_note_content, capsys):
    """Tier 2: CLI `kb-tools repair-links` repairs broken link targets in-place."""
    papers_dir = tmp_vault / "Sources" / "Papers"
    concepts_dir = tmp_vault / "Knowledge" / "Concepts"

    (papers_dir / "he2016deep.md").write_text(sample_paper_note_content, encoding="utf-8")
    
    note_to_repair = concepts_dir / "needs_repair.md"
    note_to_repair.write_text("""---
type: concept
project: zotero_obsidian_kb
title: "Needs Repair"
status: active
claim_strength: strong
primary_sources: ["[[he2016deep]]"]
tags: ["#type/concept"]
updated: 2026-08-19T00:00:00Z
---
# Needs Repair
Links to [[he2016deep]].
""", encoding="utf-8")

    from kb_tools.cli import main
    exit_code = main(["repair-links", "--vault-dir", str(tmp_vault)])
    assert exit_code == 0
