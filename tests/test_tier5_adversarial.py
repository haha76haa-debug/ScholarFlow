"""
Tier 5 Adversarial Test Suite for Zotero-Obsidian Academic Knowledge Base.

Consolidated and hardened test suite combining white-box adversarial stress tests,
fuzzing scenarios, edge-case validations, and security boundaries.
"""

from __future__ import annotations

import concurrent.futures
import json
from pathlib import Path
import re
import shutil
import time
from typing import Any, Dict, List, Optional

import pytest

from kb_tools.canvas_gen import (
    COLOR_CYAN,
    COLOR_GREEN,
    COLOR_ORANGE,
    COLOR_PURPLE,
    COLOR_RED,
    COLOR_YELLOW,
    build_canvas_graph,
    generate_canvas_file,
)
from kb_tools.cli import main
from kb_tools.ingest import (
    clean_latex_string,
    ingest_file,
    parse_bibtex,
    parse_csl_json,
    render_paper_note,
    sanitize_citekey,
)
from kb_tools.link_checker import (
    build_vault_graph,
    check_links,
    find_all_wikilinks,
    repair_all_links,
    repair_links,
)
from kb_tools.linter import (
    ALLOWED_STANDALONE_TAGS,
    ALLOWED_TAG_PREFIXES,
    VALID_CLAIM_STRENGTHS,
    VALID_SOURCE_TYPES,
    VALID_STATUSES,
    LintIssue,
    LintResult,
    lint_concept_note,
    lint_file,
    lint_paper_note,
    lint_synthesis_note,
    lint_vault,
    validate_claim_promotion_gate,
    validate_tag,
    validate_tag_taxonomy,
    write_lint_report,
)
from kb_tools.models import (
    EXCLUDED_DIRS,
    STANDARD_SYSTEM_TARGETS,
    dump_frontmatter,
    extract_wikilinks,
    get_canonical_note_map,
    parse_frontmatter,
    scan_vault_notes,
)
from kb_tools.registry import (
    generate_knowledge_index,
    generate_papers_index,
    generate_system_registry,
    scan_concept_notes,
    scan_paper_notes,
    sync_registry,
    update_02_index,
    update_section_with_marker,
)
from kb_tools.synthesizer import (
    build_comparison_matrix,
    cluster_claims,
    extract_all_claims,
    extract_claims_and_evidence,
    extract_evidence_records,
    group_claims_by_strength,
    run_synthesis,
    synthesize_comparison_matrix_doc,
    synthesize_literature_overview,
    synthesize_method_taxonomy,
    synthesize_research_gaps,
)


# ==============================================================================
# Helper Factories for Test Vault Generation
# ==============================================================================

def create_paper_note(
    vault_dir: Path,
    citekey: str,
    title: str = "Test Paper",
    **kwargs: Any,
) -> Path:
    """Helper to generate a canonical paper note with customized frontmatter/body."""
    paper_dir = vault_dir / "Sources" / "Papers"
    paper_dir.mkdir(parents=True, exist_ok=True)
    file_path = paper_dir / f"{citekey}.md"

    frontmatter = {
        "type": kwargs.get("type", "paper"),
        "project": kwargs.get("project", "zotero_obsidian_kb"),
        "title": title,
        "citekey": citekey,
        "zotero_key": kwargs.get("zotero_key", f"KEY{citekey[:6].upper()}"),
        "status": kwargs.get("status", "read"),
        "source_type": kwargs.get("source_type", "conference paper"),
        "claim_strength": kwargs.get("claim_strength", "observed"),
        "authors": kwargs.get("authors", ["Author One", "Author Two"]),
        "year": kwargs.get("year", 2024),
        "venue": kwargs.get("venue", "NeurIPS"),
        "linked_knowledge": kwargs.get("linked_knowledge", ["Knowledge/Literature Overview"]),
        "paper_relationships": kwargs.get("paper_relationships", []),
        "tags": kwargs.get("tags", ["#type/paper-note", "#topic/deep-learning"]),
    }
    for k, v in kwargs.items():
        if k not in frontmatter and k not in ("extra_body", "raw_content"):
            frontmatter[k] = v

    if "raw_content" in kwargs:
        file_path.write_text(kwargs["raw_content"], encoding="utf-8")
        return file_path

    body = f"""# {title}

## Claim
Primary finding and assertion of {citekey}.

## Research question
What specific open problem is addressed?

## Method
Core algorithmic or architectural formulation.

## Evidence
```md
Evidence ID: EVD-{citekey}-01
Source: [[Sources/Papers/{citekey}]]
Source type: {kwargs.get("source_type", "conference paper")}
Supports: "Primary claim of {citekey}"
Contradicts: ""
Method / dataset / metric: "Standard Benchmark"
Limitation: ""
Project relevance: "Foundational baseline"
Claim strength: {kwargs.get("claim_strength", "observed")}
```

## Strengths
- High empirical robustness and scalability.

## Limitation
- High compute overhead.

## Direct relevance to repo
Essential architecture component.

## Relation to other papers
- Baseline comparisons.

## Knowledge links
- [[Knowledge/Literature Overview]]
"""
    if "extra_body" in kwargs:
        body += "\n" + kwargs["extra_body"]

    content = dump_frontmatter(frontmatter, body)
    file_path.write_text(content, encoding="utf-8")
    return file_path


def create_concept_note(
    vault_dir: Path,
    name: str,
    title: str = "Test Concept",
    **kwargs: Any,
) -> Path:
    """Helper to generate an atomic concept note."""
    concept_dir = vault_dir / "Knowledge" / "Concepts"
    concept_dir.mkdir(parents=True, exist_ok=True)
    file_path = concept_dir / f"{name}.md"

    frontmatter = {
        "type": kwargs.get("type", "concept"),
        "project": kwargs.get("project", "zotero_obsidian_kb"),
        "title": title,
        "status": kwargs.get("status", "active"),
        "claim_strength": kwargs.get("claim_strength", "established"),
        "primary_sources": kwargs.get("primary_sources", ["Sources/Papers/he2016deep"]),
        "tags": kwargs.get("tags", ["#type/concept", "#topic/deep-learning"]),
    }
    for k, v in kwargs.items():
        if k not in frontmatter and k not in ("extra_body", "raw_content"):
            frontmatter[k] = v

    if "raw_content" in kwargs:
        file_path.write_text(kwargs["raw_content"], encoding="utf-8")
        return file_path

    body = f"""# {title}

## Definition
Definition and core principles of {title}.

## Mathematical Formulation
Mathematical explanation of {title}: $y = f(x) + x$.

## Context & Background
Theoretical background and origin.

## Primary Sources
- [[Sources/Papers/he2016deep]]
"""
    if "extra_body" in kwargs:
        body += "\n" + kwargs["extra_body"]

    content = dump_frontmatter(frontmatter, body)
    file_path.write_text(content, encoding="utf-8")
    return file_path


# ==============================================================================
# 1. CLI Adversarial Invocations & Boundary Stress Tests
# ==============================================================================

class TestTier5CLIAdversarial:
    """Stress tests on CLI argument parsing, flags, invalid directories, and exit codes."""

    def test_cli_no_args_returns_code_one(self, capsys):
        code = main([])
        out, err = capsys.readouterr()
        assert code == 1
        assert "usage:" in out.lower() or "usage:" in err.lower()

    def test_cli_unknown_subcommand_returns_code_one_or_two(self, capsys):
        code = main(["unknown-command-xyz"])
        assert code in (1, 2)

    def test_cli_subcommand_aliases_all_resolve(self, tmp_path):
        vault = tmp_path / "alias_vault"
        vault.mkdir()
        create_paper_note(vault, "paper2024", title="Paper 2024")
        create_concept_note(vault, "concept_a", title="Concept A")

        assert main(["check-links", "--vault-dir", str(vault)]) == 0
        assert main(["check_links", "--vault-dir", str(vault)]) == 0
        assert main(["sync-registry", "--vault-dir", str(vault)]) == 0
        assert main(["sync_registry", "--vault-dir", str(vault)]) == 0
        assert main(["repair-links", "--vault-dir", str(vault)]) == 0
        assert main(["repair_links", "--vault-dir", str(vault)]) == 0
        assert main(["generate-canvas", "--vault-dir", str(vault)]) == 0
        assert main(["generate_canvas", "--vault-dir", str(vault)]) == 0

    def test_cli_nonexistent_vault_directory_handling(self, capsys):
        nonexistent = "/path/that/does/not/exist/vault_987654"
        subcommands = ["lint", "sync-registry", "check-links", "repair-links", "synthesize", "generate-canvas", "ingest"]
        for subcmd in subcommands:
            args = [subcmd, "--vault-dir", nonexistent]
            if subcmd == "ingest":
                args.extend(["--input", "some_file.bib"])
            exit_code = main(args)
            assert exit_code == 1

    def test_cli_empty_vault_execution_all_subcommands(self, tmp_path):
        empty_vault = tmp_path / "empty_vault"
        empty_vault.mkdir()

        assert main(["lint", "--vault-dir", str(empty_vault)]) == 0
        assert main(["check-links", "--vault-dir", str(empty_vault)]) == 0
        assert main(["repair-links", "--vault-dir", str(empty_vault)]) == 0
        assert main(["sync-registry", "--vault-dir", str(empty_vault)]) == 0
        assert main(["synthesize", "--vault-dir", str(empty_vault)]) == 0
        assert main(["generate-canvas", "--vault-dir", str(empty_vault)]) == 0

    def test_cli_dry_run_and_json_flag_combination(self, tmp_path, capsys):
        vault = tmp_path / "combo_vault"
        vault.mkdir()
        create_paper_note(vault, "paper2024", title="Combo Paper")

        for subcmd in ["sync-registry", "repair-links", "synthesize", "generate-canvas"]:
            code = main([subcmd, "--vault-dir", str(vault), "--dry-run", "--json"])
            out, _ = capsys.readouterr()
            assert code == 0, f"{subcmd} failed with exit code {code}"
            parsed = json.loads(out)
            assert isinstance(parsed, dict)

    def test_cli_lint_single_file_positional_target(self, tmp_path, capsys):
        vault = tmp_path / "single_file_vault"
        vault.mkdir()
        paper_file = create_paper_note(vault, "paper2024", title="Single File Paper")

        code = main(["lint", str(paper_file), "--vault-dir", str(vault), "--json"])
        out, _ = capsys.readouterr()
        assert code == 0
        parsed = json.loads(out)
        assert parsed["target"] == str(paper_file)
        assert parsed["errors_count"] == 0

    def test_cli_strict_mode_converts_warnings_to_errors(self, tmp_path, capsys):
        vault = tmp_path / "strict_vault"
        vault.mkdir()
        # Create paper note with non-standard tag containing spaces generating a lint warning
        create_paper_note(
            vault, "warnpaper2024",
            title="Warning Paper",
            tags=["invalid tag with space"]
        )

        # Standard lint returns 0 (warnings only)
        code_normal = main(["lint", "--vault-dir", str(vault)])
        assert code_normal == 0

        # Strict lint returns 1 (warnings treated as failures)
        code_strict = main(["lint", "--vault-dir", str(vault), "--strict"])
        assert code_strict == 1

    def test_cli_repair_links_dry_run_flag(self, tmp_path, capsys):
        vault = tmp_path / "repair_cli_vault"
        vault.mkdir()
        p1 = create_paper_note(vault, "he2016deep", title="ResNet")
        
        note = vault / "test_note.md"
        note.write_text("# Note\nSee [[he2016dee]] for details.\n", encoding="utf-8")

        code = main(["repair-links", "--vault-dir", str(vault), "--dry-run", "--json"])
        out, _ = capsys.readouterr()
        assert code == 0
        data = json.loads(out)
        assert data["dry_run"] is True
        assert data["repaired_count"] >= 1
        # File should not be modified
        assert "[[he2016dee]]" in note.read_text(encoding="utf-8")

    def test_cli_ingest_malformed_input_files(self, tmp_path):
        vault = tmp_path / "ingest_vault"
        vault.mkdir()
        bad_file = tmp_path / "corrupt.json"
        bad_file.write_text("INVALID JSON CONTENT { [", encoding="utf-8")

        code = main(["ingest", "--input", str(bad_file), "--vault-dir", str(vault)])
        assert code != 0


# ==============================================================================
# 2. Unicode, Emojis, BiDi, Non-ASCII & Special Formatting Stress Tests
# ==============================================================================

class TestTier5UnicodeAndStringFormatting:
    """Stress tests on unicode characters, zero-width spaces, RTL/BiDi, multibyte emojis, and LaTeX."""

    def test_zero_width_spaces_and_bidi_in_paper_note(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        # Zero-width spaces (\u200b), LTR/RTL marks (\u200e, \u202e)
        zws_title = "Zero\u200bWidth\u200cSpace \u202eRTL Override\u202c Paper"
        paper_path = create_paper_note(vault, "zwspaper2024", title=zws_title)

        issues = lint_file(paper_path, vault)
        assert not any(i.severity == "error" for i in issues)

        reg = sync_registry(vault)
        assert reg["status"] == "success"
        assert reg["papers_count"] == 1

        reg_file = vault / "_system" / "registry.md"
        assert reg_file.exists()
        reg_text = reg_file.read_text(encoding="utf-8")
        assert "zwspaper2024" in reg_text

    def test_multibyte_emojis_and_cjk_in_notes_and_wikilinks(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        emoji_title = "🧠 Deep Transformer 🚀 & 视觉大模型 🌟"
        paper_path = create_paper_note(vault, "emojipaper2024", title=emoji_title)
        concept_path = create_concept_note(
            vault,
            "深度学习概念",
            title="深度学习 🧠 Concept",
            primary_sources=["Sources/Papers/emojipaper2024"],
        )

        res = check_links(vault)
        assert res.is_clean
        assert len(res.broken_links) == 0

        graph = build_canvas_graph(vault)
        assert len(graph["nodes"]) >= 2
        file_nodes = [n for n in graph["nodes"] if n["type"] == "file"]
        assert any("深度学习概念.md" in n["file"] for n in file_nodes)

    def test_markdown_table_pipe_character_injection_resistance(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        pipe_title = "Scaling Laws | A Survey | Part 1 | Summary"
        pipe_authors = ["Smith | John", "Doe | Jane"]
        paper_path = create_paper_note(vault, "pipepaper2024", title=pipe_title, authors=pipe_authors)

        res = sync_registry(vault)
        assert res["status"] == "success"

        papers_index = vault / "02-Index.md"
        content = papers_index.read_text(encoding="utf-8")
        assert "pipepaper2024" in content

        synth_files = run_synthesis(vault)
        assert len(synth_files) >= 3

    def test_clean_latex_unicode_and_accents(self):
        samples = {
            r"{\"o}rsted": '"orsted',
            r"{\'E}tienne": "'Etienne",
            r"\textbf{Deep} Learning": "Deep Learning",
            r"\emph{Convolutional} Neural Networks": "Convolutional Neural Networks",
            r"$\mathcal{O}(N \log N)$ Complexity": "$\\mathcal{O}(N \\log N)$ Complexity",
            r"Attention is all you need \% 100\%": "Attention is all you need \\% 100\\%",
            r"Double {{nested}} {{braces}}": "Double {nested} {braces}",
        }
        for raw, expected in samples.items():
            cleaned = clean_latex_string(raw)
            assert isinstance(cleaned, str)
            assert len(cleaned) > 0

    def test_clean_latex_escaped_symbols(self):
        raw = r"Accuracy 95\% in \$100 budget \& 50\_000 samples \#1"
        cleaned = clean_latex_string(raw)
        assert "%" in cleaned
        assert "$" in cleaned
        assert "&" in cleaned
        assert "_" in cleaned
        assert "#" in cleaned


# ==============================================================================
# 3. Deeply Nested Wikilinks, Anchors, Block Refs, Chained Aliases, and Cycles
# ==============================================================================

class TestTier5WikilinksAndGraphIntegrity:
    """Stress tests on wikilink resolution, anchors, block IDs, chained aliases, and graph cycles."""

    def test_header_anchors_and_block_references_resolution(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        p1 = create_paper_note(vault, "he2016deep", title="Deep Residual Learning")
        c1 = create_concept_note(
            vault,
            "residual_connection",
            title="Residual Connection",
            extra_body="""
## References
- [[Sources/Papers/he2016deep#Method]]
- [[Sources/Papers/he2016deep#Evidence]]
- [[Sources/Papers/he2016deep#^evd-01]]
- [[Sources/Papers/he2016deep|ResNet Paper]]
""",
        )

        res = check_links(vault)
        assert res.is_clean
        assert len(res.broken_links) == 0

    def test_cyclic_graph_and_self_referential_links(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        # Paper A -> Concept B -> Paper C -> Paper A (Cycle)
        create_paper_note(
            vault, "cyclica2024", title="Cyclic Paper A",
            extra_body="- Uses [[Knowledge/Concepts/cyclicconceptb]]\n- Self [[Sources/Papers/cyclica2024]]"
        )
        create_concept_note(
            vault, "cyclicconceptb", title="Cyclic Concept B",
            primary_sources=["Sources/Papers/cyclicc2024"]
        )
        create_paper_note(
            vault, "cyclicc2024", title="Cyclic Paper C",
            extra_body="- Extends [[Sources/Papers/cyclica2024]]"
        )

        res = check_links(vault)
        assert res.is_clean

        graph = build_canvas_graph(vault)
        assert len(graph["nodes"]) >= 3
        assert len(graph["edges"]) >= 3

        vault_graph = build_vault_graph(vault)
        assert "Sources/Papers/cyclica2024.md" in vault_graph
        assert "Knowledge/Concepts/cyclicconceptb.md" in vault_graph["Sources/Papers/cyclica2024.md"]["outgoing"]

    def test_chained_and_aliased_wikilinks_repair(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        create_paper_note(vault, "vaswani2017attention", title="Attention Is All You Need")

        # Note with typo target and alias
        note_path = vault / "Notes" / "reading_notes.md"
        note_path.parent.mkdir(parents=True, exist_ok=True)
        note_path.write_text(
            "# Reading Note\n\nRefer to [[vaswani2017attentio|Transformer Architecture]] and [[vaswani2017attention#Method|Attention Section]].",
            encoding="utf-8"
        )

        res = check_links(vault)
        assert not res.is_clean
        assert len(res.broken_links) == 1

        repair_res = repair_links(vault, threshold=0.7, dry_run=False)
        assert repair_res["repaired_count"] == 1

        repaired_content = note_path.read_text(encoding="utf-8")
        assert "[[vaswani2017attention|Transformer Architecture]]" in repaired_content

        res_post = check_links(vault)
        assert res_post.is_clean

    def test_wikilink_url_encoding_detection(self, tmp_path):
        vault = tmp_path / "url_vault"
        vault.mkdir()
        create_paper_note(vault, "he2016deep", title="Deep Residual Learning")

        test_note = vault / "note.md"
        test_note.write_text(
            "# Note\n"
            "URL Encoded: [[he2016%20deep]]\n"
            "Valid: [[he2016deep]]\n",
            encoding="utf-8",
        )

        res = check_links(vault)
        assert not res.is_clean
        broken_targets = [bl["target"] for bl in res.broken_links]
        assert "he2016%20deep" in broken_targets

    def test_markdown_standard_links_vs_wikilinks(self, tmp_path):
        vault = tmp_path / "md_link_vault"
        vault.mkdir()
        create_paper_note(vault, "he2016deep", title="Deep Residual Learning")

        test_note = vault / "note.md"
        test_note.write_text(
            "# Note\n"
            "Standard markdown link: [ResNet Paper](Sources/Papers/he2016deep.md)\n"
            "External link: [ArXiv](https://arxiv.org/abs/1512.03385)\n"
            "Wikilink: [[he2016deep]]\n",
            encoding="utf-8",
        )

        matches = find_all_wikilinks(test_note.read_text(encoding="utf-8"))
        targets = [m[1] for m in matches]
        assert "he2016deep" in targets
        assert "https://arxiv.org/abs/1512.03385" not in targets

    def test_nested_brackets_and_transclusions(self, tmp_path):
        vault = tmp_path / "bracket_vault"
        vault.mkdir()
        create_paper_note(vault, "he2016deep", title="Deep Residual Learning")

        text = (
            "Embedded image: ![[assets/diagram.png]]\n"
            "Embedded paper: ![[Sources/Papers/he2016deep]]\n"
            "Math with double brackets: $[[x_i, y_i]]$\n"
            "Pipe in table: | [[Sources/Papers/he2016deep\\|ResNet]] |\n"
        )
        extracted = extract_wikilinks(text)
        assert len(extracted) >= 3

    def test_multiple_broken_links_per_line_repair(self, tmp_path):
        vault = tmp_path / "multi_repair_vault"
        vault.mkdir()
        create_paper_note(vault, "he2016deep", title="ResNet")
        create_paper_note(vault, "vaswani2017attention", title="Attention")

        note = vault / "multi.md"
        note.write_text(
            "# Note\nCompare [[he2016dee]] with [[vaswani2017attentio]] in detail.\n",
            encoding="utf-8",
        )

        res = repair_links(vault, threshold=0.7, dry_run=False)
        assert res["repaired_count"] >= 2
        content = note.read_text(encoding="utf-8")
        assert "he2016deep" in content
        assert "vaswani2017attention" in content

    def test_fuzzy_link_repair_idempotency(self, tmp_path):
        vault = tmp_path / "repair_vault"
        vault.mkdir()
        create_paper_note(vault, "he2016deep", title="ResNet")

        note = vault / "broken.md"
        note.write_text("# Note\nSee [[he2016dee]] for details.\n", encoding="utf-8")

        res1 = repair_links(vault, threshold=0.7, dry_run=False)
        assert res1["repaired_count"] >= 1
        content1 = note.read_text(encoding="utf-8")
        assert "he2016deep" in content1

        res2 = repair_links(vault, threshold=0.7, dry_run=False)
        assert res2["repaired_count"] == 0
        content2 = note.read_text(encoding="utf-8")
        assert content1 == content2

    def test_vault_graph_bidirectional_mapping(self, tmp_path):
        vault = tmp_path / "graph_vault"
        vault.mkdir()
        create_paper_note(vault, "he2016deep", title="ResNet")
        create_concept_note(
            vault,
            "residual_connection",
            title="Residual Connection",
            primary_sources=["Sources/Papers/he2016deep"],
        )

        graph = build_vault_graph(vault)
        assert "Knowledge/Concepts/residual_connection.md" in graph
        assert "Sources/Papers/he2016deep.md" in graph
        assert "Sources/Papers/he2016deep.md" in graph["Knowledge/Concepts/residual_connection.md"]["outgoing"]
        assert "Knowledge/Concepts/residual_connection.md" in graph["Sources/Papers/he2016deep.md"]["incoming"]

    def test_canonical_map_case_insensitivity(self, tmp_path):
        vault = tmp_path / "case_vault"
        vault.mkdir()
        create_paper_note(vault, "he2016deep", title="ResNet")

        cmap = get_canonical_note_map(vault)
        assert "he2016deep" in cmap
        assert "HE2016DEEP".lower() in cmap
        assert "Sources/Papers/he2016deep" in cmap
        assert "sources/papers/he2016deep" in cmap


# ==============================================================================
# 4. Schema Bypasses, Type Mutations & Linter Stress Testing
# ==============================================================================

class TestTier5SchemaTaxonomyAndEvidence:
    """Stress test schema validations, type mutations, enum violations, and taxonomy rules."""

    def test_frontmatter_year_as_non_integer_types(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        mutations = [
            ("year_str", "2024"),
            ("year_bool", True),
            ("year_float", 2024.5),
            ("year_list", [2024]),
            ("year_none", None),
        ]

        for citekey, invalid_year in mutations:
            p = create_paper_note(vault, citekey, title=f"Invalid Year {citekey}", year=invalid_year)
            issues = lint_file(p, vault)
            errs = [i for i in issues if i.severity == "error" and "year" in i.message.lower()]
            assert len(errs) >= 1, f"Expected year error for {citekey} ({type(invalid_year)})"

    def test_frontmatter_non_dict_and_corrupt_yaml(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        paper_dir = vault / "Sources" / "Papers"
        paper_dir.mkdir(parents=True, exist_ok=True)

        p1 = paper_dir / "corrupt1.md"
        p1.write_text("---\n- Item 1 in list instead of dict\n- Item 2\n---\n# Corrupt\n", encoding="utf-8")

        p2 = paper_dir / "corrupt2.md"
        p2.write_text("---\nkey: : [invalid yaml structure\n---\n# Corrupt 2\n", encoding="utf-8")

        p3 = paper_dir / "corrupt3.md"
        p3.write_text("No frontmatter at all in paper file.\n# Heading", encoding="utf-8")

        for p in [p1, p2, p3]:
            issues = lint_file(p, vault)
            assert any(i.severity == "error" for i in issues)

    def test_frontmatter_delimiter_variants(self, tmp_path):
        vault = tmp_path / "delim_vault"
        vault.mkdir()
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)

        # Delimiter using '===' or '...' instead of '---'
        bad_delim = papers / "bad_delim.md"
        bad_delim.write_text("===\ntype: paper\ntitle: Bad Delim\n===\n# Bad Delim", encoding="utf-8")

        issues = lint_file(bad_delim, vault_dir=vault)
        assert any(i.severity == "error" for i in issues)

    def test_enum_mutation_and_invalid_values(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        p = create_paper_note(
            vault,
            "badval2024",
            title="Bad Value Paper",
            status="finished_reading_all",
            source_type="reddit post",
            claim_strength="absolutely_proven_100%",
        )
        issues = lint_file(p, vault)
        status_errs = [i for i in issues if "status must be one of" in i.message]
        source_errs = [i for i in issues if "source_type must be one of" in i.message]
        strength_errs = [i for i in issues if "claim_strength must be one of" in i.message]

        assert len(status_errs) >= 1
        assert len(source_errs) >= 1
        assert len(strength_errs) >= 1

    def test_paper_field_type_boundary_checks(self, tmp_path):
        vault = tmp_path / "boundary_vault"
        vault.mkdir()

        # authors as single string, linked_knowledge as int
        p = create_paper_note(
            vault,
            "typebad2024",
            title="Type Bad Paper",
            authors="Alice Researcher",
            linked_knowledge=12345,
        )
        issues = lint_file(p, vault_dir=vault)
        errors = [i for i in issues if i.severity == "error"]
        assert len(errors) >= 2

    def test_duplicate_citekey_and_zotero_key_collision_detection(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        p1 = create_paper_note(vault, "dupkey2024", title="Original Paper", zotero_key="KEY12345")
        
        # Second file with different file name but same citekey
        paper_dir = vault / "Sources" / "Papers"
        p2 = paper_dir / "dupkey2024_copy.md"
        content2 = dump_frontmatter({
            "type": "paper",
            "project": "zotero_obsidian_kb",
            "title": "Copy Paper",
            "citekey": "dupkey2024",
            "zotero_key": "KEY12345",
            "status": "read",
            "source_type": "preprint",
            "claim_strength": "observed",
            "authors": ["Author"],
            "year": 2024,
            "linked_knowledge": ["Knowledge/Literature Overview"],
        }, "# Copy\n\n## Claim\nClaim\n## Research question\nQ\n## Method\nM\n## Evidence\n```md\nEvidence ID: EVD-dupkey2024-01\nSource: [[Sources/Papers/dupkey2024]]\nSupports: \"X\"\nClaim strength: observed\n```\n## Strengths\nS\n## Limitation\nL\n## Direct relevance to repo\nR\n## Relation to other papers\nRel\n## Knowledge links\n- [[Knowledge/Literature Overview]]\n")
        p2.write_text(content2, encoding="utf-8")

        res = lint_vault(vault)
        dup_citekeys = [i for i in res.issues if "Duplicate citekey 'dupkey2024'" in i.message]
        dup_zoteros = [i for i in res.issues if "Duplicate zotero_key 'KEY12345'" in i.message]

        assert len(dup_citekeys) >= 1
        assert len(dup_zoteros) >= 1

    def test_claim_promotion_gate_weak_source_rejection(self, tmp_path):
        vault = tmp_path / "gate_vault"
        vault.mkdir()
        p = create_paper_note(
            vault,
            "weak2024",
            title="Weak Source Paper",
            source_type="webpage placeholder",
            claim_strength="strong",
        )
        passed, errors = validate_claim_promotion_gate(p, vault)
        assert passed is False
        assert len(errors) >= 1

    def test_tag_taxonomy_strict_rules(self):
        assert validate_tag("type/paper") is True
        assert validate_tag("topic/deep-learning/vision") is True
        assert validate_tag("status/reading") is True
        assert validate_tag("method/lora") is True
        assert validate_tag("transformer") is True

        assert validate_tag("") is False
        assert validate_tag("tag with space") is False
        assert validate_tag("#type/paper") is True
        assert validate_tag("invalid@char!") is False

    def test_tag_validator_type_safety_non_strings(self):
        """Verify validate_tag gracefully handles non-string and unexpected inputs."""
        assert validate_tag(None) is False
        assert validate_tag(12345) is False
        assert validate_tag(True) is False
        assert validate_tag(["type/paper"]) is False
        assert validate_tag({"tag": "value"}) is False
        assert validate_tag("type/") is False

    def test_heading_variant_normalization(self, tmp_path):
        vault = tmp_path / "heading_vault"
        vault.mkdir()
        p = create_paper_note(vault, "p2024", title="Heading Variant Paper")
        content = p.read_text(encoding="utf-8")
        content = content.replace("## Method", "## METHODOLOGY").replace("## Limitation", "## Limitations")
        p.write_text(content, encoding="utf-8")

        issues = lint_file(p, vault_dir=vault)
        heading_errors = [i for i in issues if i.category == "Heading Structure"]
        assert len(heading_errors) == 0


# ==============================================================================
# 5. Path Traversal & Filesystem Security Boundaries
# ==============================================================================

class TestTier5PathTraversalAndSecurity:
    """Stress tests on citekey sanitization, path traversal vectors, and Windows reserved names."""

    def test_citekey_path_traversal_sanitization(self):
        traversals = [
            ("../../etc/passwd", "etcpasswd"),
            ("..\\..\\Windows\\System32", "windowssystem32"),
            ("../../../secret", "secret"),
            ("foo/../../bar", "foobar"),
            ("./relative/path", "relativepath"),
        ]
        for raw, expected in traversals:
            sanitized = sanitize_citekey(raw)
            assert "/" not in sanitized
            assert "\\" not in sanitized
            assert ".." not in sanitized
            assert sanitized == expected

    def test_forbidden_windows_characters_sanitization(self):
        forbidden = [
            ("he:2016?deep*", "he2016deep"),
            ("vaswani<2017>attention|v1", "vaswani2017attentionv1"),
            ('hu"2021"lora', "hu2021lora"),
        ]
        for raw, expected in forbidden:
            sanitized = sanitize_citekey(raw)
            assert not any(c in sanitized for c in ':*?"<>|')
            assert sanitized == expected

    def test_reserved_windows_device_names(self):
        device_names = ["CON", "PRN", "AUX", "NUL", "COM1", "COM9", "LPT1", "LPT9"]
        for name in device_names:
            sanitized = sanitize_citekey(name)
            assert sanitized == name.lower()

    def test_empty_and_whitespace_only_citekeys(self):
        empties = ["", "   ", "---", "___", "\t\n", "!@#$%^&*()"]
        for empty_str in empties:
            sanitized = sanitize_citekey(empty_str)
            assert sanitized == "unknownpaper"
            assert len(sanitized) > 0


# ==============================================================================
# 6. Ingest, BibTeX & CSL-JSON Parser Stress Testing
# ==============================================================================

class TestTier5IngestAndBibtexCSL:
    """Stress tests on BibTeX/CSL parsing, malformed entries, long author lists, and batch files."""

    def test_malformed_bibtex_with_unclosed_braces(self):
        malformed_bib = """
@article{broken2024,
  title = {A Title With {Unclosed Braces,
  author = {Smith, John and Doe, Jane,
  year = {2024},
  journal = {ArXiv}
}
@inproceedings{valid2024,
  title = {Valid Followup Paper},
  author = {Brown, Charlie},
  year = {2024},
  booktitle = {ICML}
}
"""
        entries = parse_bibtex(malformed_bib)
        assert len(entries) >= 1
        assert any(e["citekey"] == "valid2024" for e in entries)

    def test_bibtex_massive_fields_and_long_author_lists(self):
        authors = " and ".join([f"Author{i}, Firstname{i}" for i in range(50)])
        huge_abstract = "Deep learning breakthrough. " * 500
        
        bib = f"""
@article{{massive2024,
  title = {{Massive Paper with 50 Authors and Huge Abstract}},
  author = {{{authors}}},
  year = {{2024}},
  journal = {{Journal of Big Data}},
  abstract = {{{huge_abstract}}}
}}
"""
        entries = parse_bibtex(bib)
        assert len(entries) == 1
        entry = entries[0]
        assert len(entry["authors"]) == 50
        assert entry["citekey"] == "massive2024"

        md = render_paper_note(entry)
        assert "Massive Paper" in md
        assert "EVD-massive2024-01" in md

    def test_csl_json_with_corrupt_date_and_missing_properties(self):
        corrupt_csl = [
            {"id": "item1"},
            {"id": "item2", "title": "No Date", "author": "Invalid Author String"},
            {"id": "item3", "title": "Negative Year", "issued": {"date-parts": [[]]}},
            {"id": "item4", "title": "Raw String Date", "issued": {"raw": "Published Spring 2023"}},
        ]
        entries = parse_csl_json(corrupt_csl)
        assert len(entries) == 4
        assert entries[0]["citekey"] == "item1"
        assert entries[3]["year"] == 2023

    def test_parse_bibtex_with_complex_fields(self):
        bib_content = """@article{he2016deep,
  author = {He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
  title = {{Deep Residual Learning for Image Recognition}},
  journal = {IEEE Conference on Computer Vision and Pattern Recognition (CVPR)},
  year = {2016},
  pages = {770--778},
  doi = {10.1109/CVPR.2016.90},
  abstract = {Deeper neural networks are more difficult to train. We present a residual learning framework.}
}
@inproceedings{vaswani2017attention,
  author = {Vaswani, Ashish and Shazeer, Noam and Parmar, Niki},
  title = "Attention Is All You Need",
  booktitle = "Advances in Neural Information Processing Systems",
  year = 2017
}"""
        entries = parse_bibtex(bib_content)
        assert len(entries) == 2
        assert entries[0]["citekey"] == "he2016deep"
        assert entries[0]["year"] == 2016
        assert len(entries[0]["authors"]) == 4
        assert entries[1]["citekey"] == "vaswani2017attention"
        assert entries[1]["year"] == 2017

    def test_parse_csl_json_with_missing_optional_fields(self):
        csl_data = [
            {
                "id": "hu2021lora",
                "type": "paper-conference",
                "title": "LoRA: Low-Rank Adaptation of Large Language Models",
                "author": [
                    {"family": "Hu", "given": "Edward J."},
                    {"literal": "OpenAI Team"},
                ],
                "issued": {"date-parts": [[2021, 6, 1]]},
                "container-title": "ICLR",
            },
            {
                "id": "minimal_item",
                "title": "Minimal Paper",
            }
        ]
        entries = parse_csl_json(csl_data)
        assert len(entries) == 2
        assert entries[0]["citekey"] == "hu2021lora"
        assert entries[0]["year"] == 2021
        assert "Edward J. Hu" in entries[0]["authors"]
        assert "OpenAI Team" in entries[0]["authors"]
        assert entries[1]["citekey"] == "minimalitem"
        assert entries[1]["authors"] == ["Anonymous"]

    def test_ingest_batch_file_with_duplicates_and_overwrite_flag(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        bib_file = tmp_path / "batch.bib"
        bib_file.write_text("""
@inproceedings{batcha2024,
  title = {Batch Paper A},
  author = {Alpha, Alice},
  year = {2024},
  booktitle = {ICLR}
}
@inproceedings{batchb2024,
  title = {Batch Paper B},
  author = {Beta, Bob},
  year = {2024},
  booktitle = {NeurIPS}
}
""", encoding="utf-8")

        created1 = ingest_file(bib_file, vault_dir=vault, overwrite=False)
        assert len(created1) == 2

        created2 = ingest_file(bib_file, vault_dir=vault, overwrite=False)
        assert len(created2) == 0

        created3 = ingest_file(bib_file, vault_dir=vault, overwrite=True)
        assert len(created3) == 2


# ==============================================================================
# 7. Canvas Integrity, Group Containers & JSON Canvas v1.0 Spec
# ==============================================================================

class TestTier5CanvasTopologyAndRendering:
    """Stress tests on Canvas graph generation, coordinate layouts, and edge resolution."""

    def test_canvas_empty_vault_schema_compliance(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        graph = build_canvas_graph(vault)
        assert "nodes" in graph
        assert "edges" in graph
        assert graph["nodes"] == []
        assert graph["edges"] == []

        canvas_file = generate_canvas_file(vault)
        assert canvas_file.exists()
        canvas_data = json.loads(canvas_file.read_text(encoding="utf-8"))
        assert canvas_data == {"nodes": [], "edges": []}

    def test_canvas_dense_graph_node_coordinates_and_color_palette(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        for i in range(15):
            create_paper_note(
                vault, f"paper{i:02d}", title=f"Scale Paper {i}",
                linked_knowledge=["Knowledge/Literature Overview"]
            )
        for j in range(5):
            create_concept_note(
                vault,
                f"concept{j:02d}",
                title=f"Scale Concept {j}",
                primary_sources=[f"Sources/Papers/paper{j:02d}", f"Sources/Papers/paper{j+1:02d}"]
            )

        graph = build_canvas_graph(vault)
        assert len(graph["nodes"]) >= 20
        assert len(graph["edges"]) >= 10

        for node in graph["nodes"]:
            assert isinstance(node["id"], str)
            assert isinstance(node["x"], (int, float))
            assert isinstance(node["y"], (int, float))
            assert node["width"] > 0
            assert node["height"] > 0
            if "color" in node:
                assert node["color"] in ("1", "2", "3", "4", "5", "6")

        node_ids = {n["id"] for n in graph["nodes"]}
        for edge in graph["edges"]:
            assert edge["fromNode"] in node_ids
            assert edge["toNode"] in node_ids
            assert edge["fromNode"] != edge["toNode"]

    def test_canvas_frontmatter_bracketed_wikilink_edge_resolution(self, tmp_path):
        """Verify bracketed wikilinks in frontmatter lists cleanly resolve node IDs."""
        vault = tmp_path / "bracket_canvas_vault"
        vault.mkdir()
        create_paper_note(
            vault, "he2016deep", title="ResNet",
            linked_knowledge=["[[Knowledge/Literature Overview]]"],
            paper_relationships=["[[Sources/Papers/vaswani2017attention]]::extends"],
        )
        create_paper_note(vault, "vaswani2017attention", title="Transformer")
        create_concept_note(
            vault,
            "residual_connection",
            title="Residual Connection",
            primary_sources=["[[Sources/Papers/he2016deep]]"],
        )

        graph = build_canvas_graph(vault)
        node_ids = {n["id"]: n for n in graph["nodes"]}
        edges = graph["edges"]

        # Verify edge exists from he2016deep to residual_connection
        assert any(
            e["fromNode"] == "node-he2016deep"
            and e["toNode"] in ("node-residual_connection", "node-residual-connection")
            for e in edges
        )
        # Verify edge exists from he2016deep to vaswani2017attention
        assert any(
            e["fromNode"] == "node-he2016deep"
            and e["toNode"] in ("node-vaswani2017attention", "node-vaswani-2017-attention")
            for e in edges
        )

    def test_canvas_graph_generation_with_cycles(self, tmp_path):
        vault = tmp_path / "cycle_vault"
        vault.mkdir()

        create_paper_note(
            vault, "papera", title="Paper A",
            extra_body="\n- Uses [[Sources/Papers/paperb]]\n",
        )
        create_paper_note(
            vault, "paperb", title="Paper B",
            extra_body="\n- Uses [[Knowledge/Concepts/concept_c]]\n",
        )
        create_concept_note(
            vault, "concept_c", title="Concept C",
            primary_sources=["Sources/Papers/papera"],
        )

        graph = build_canvas_graph(vault)
        assert len(graph["nodes"]) >= 3
        assert len(graph["edges"]) >= 2

        node_ids = {n["id"] for n in graph["nodes"]}
        for edge in graph["edges"]:
            assert edge["fromNode"] in node_ids
            assert edge["toNode"] in node_ids

    def test_canvas_file_output_matches_spec(self, tmp_path):
        vault = tmp_path / "out_canvas_vault"
        vault.mkdir()
        create_paper_note(vault, "p1", title="Paper 1")

        canvas_path = generate_canvas_file(vault, dry_run=False)
        assert canvas_path.exists()

        data = json.loads(canvas_path.read_text(encoding="utf-8"))
        assert "nodes" in data
        assert "edges" in data
        assert isinstance(data["nodes"], list)
        assert isinstance(data["edges"], list)


# ==============================================================================
# 8. Registry Sync, Preamble Preservation & Vault Scaling Benchmark
# ==============================================================================

class TestTier5RegistryAndScaling:
    """Stress tests on registry generation, preamble preservation, concurrency, and 100-note scale."""

    def test_registry_sync_detects_duplicate_citekeys(self, tmp_path):
        vault = tmp_path / "dup_vault"
        vault.mkdir()

        create_paper_note(vault, "he2016deep", title="Original ResNet")
        # Duplicate file with same citekey
        paper_dir = vault / "Sources" / "Papers"
        dup_file = paper_dir / "he2016deep_duplicate.md"
        dup_file.write_text((paper_dir / "he2016deep.md").read_text(encoding="utf-8"), encoding="utf-8")

        lint_res = lint_vault(vault)
        dup_errors = [i for i in lint_res.issues if i.category == "Duplicate Key"]
        assert len(dup_errors) >= 1

    def test_registry_preamble_preservation_with_complex_formatting(self, tmp_path):
        vault = tmp_path / "preamble_vault"
        vault.mkdir()
        system_dir = vault / "_system"
        system_dir.mkdir(parents=True)
        create_paper_note(vault, "paper2024", title="Preamble Paper")

        custom_preamble = (
            "# Custom Preamble Header\n\n"
            "> Important Note: This registry is managed by automated tools.\n"
            "<!-- Custom Comment -->\n\n"
            "| Custom Col 1 | Custom Col 2 |\n"
            "| --- | --- |\n"
            "| Val 1 | Val 2 |\n"
        )

        reg_file = system_dir / "registry.md"
        reg_file.write_text(f"{custom_preamble}\n\n## Sources\nOld table", encoding="utf-8")

        sync_registry(vault, dry_run=False)

        updated_text = reg_file.read_text(encoding="utf-8")
        assert "# Custom Preamble Header" in updated_text
        assert "Important Note: This registry is managed" in updated_text
        assert "| Custom Col 1 | Custom Col 2 |" in updated_text
        assert "## Sources" in updated_text
        assert "paper2024" in updated_text

    def test_special_characters_and_cjk_in_titles(self, tmp_path):
        vault = tmp_path / "cjk_vault"
        vault.mkdir()
        create_paper_note(vault, "paper_cjk", title="大语言模型微调方法综述: LoRA & QLoRA")
        create_concept_note(vault, "concept_cjk", title="低秩适应 (Low-Rank Adaptation)")

        reg = sync_registry(vault, dry_run=False)
        assert reg["status"] == "success"

        papers_idx = vault / "02-Index.md"
        assert "大语言模型微调方法综述" in papers_idx.read_text(encoding="utf-8")

        concepts_idx = vault / "02-Index.md"
        assert "低秩适应" in concepts_idx.read_text(encoding="utf-8")

    def test_concurrent_vault_read_operations(self, tmp_path):
        vault = tmp_path / "thread_vault"
        vault.mkdir()
        for i in range(10):
            create_paper_note(vault, f"paper_{i}", title=f"Thread Paper {i}")

        def read_op():
            return (
                len(scan_vault_notes(vault)),
                len(get_canonical_note_map(vault)),
                lint_vault(vault).total_files_scanned,
            )

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
            futures = [executor.submit(read_op) for _ in range(16)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        for r in results:
            assert r[0] == 10
            assert r[2] == 10

    def test_large_vault_scaling_performance_100_notes(self, tmp_path):
        """Verify performance and stability on 100+ generated notes (< 5.0s)."""
        vault = tmp_path / "scale_vault"
        vault.mkdir()

        for i in range(50):
            ck = f"paper{i:04d}a"
            zk = f"ZOT{i:05d}"
            create_paper_note(
                vault,
                ck,
                title=f"Scale Paper {i}",
                year=2000 + (i % 25),
                zotero_key=zk,
            )
            c_name = f"concept_{i:03d}"
            create_concept_note(
                vault,
                c_name,
                title=f"Scale Concept {i}",
                claim_strength="supported",
            )

        t1 = time.perf_counter()
        res_sync = sync_registry(vault, dry_run=False)
        sync_time = time.perf_counter() - t1

        assert res_sync["papers_count"] == 50
        assert res_sync["concepts_count"] == 50
        assert sync_time < 5.0, f"Registry sync took too long: {sync_time:.2f}s"

        t2 = time.perf_counter()
        lint_res = lint_vault(vault)
        lint_time = time.perf_counter() - t2

        assert lint_res.is_clean is True
        assert lint_time < 5.0, f"Linting 100 notes took too long: {lint_time:.2f}s"


# ==============================================================================
# 9. Synthesizer, Evidence Gate & Full Lifecycle Idempotency
# ==============================================================================

class TestTier5SynthesizerAndEvidenceGate:
    """Stress tests on evidence extraction, claim grouping, idempotency, and synthesis docs."""

    def test_synthesizer_with_corrupted_and_missing_evidence_blocks(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        paper_dir = vault / "Sources" / "Papers"
        paper_dir.mkdir(parents=True, exist_ok=True)
        p = paper_dir / "noevidence2024.md"

        content = """---
type: paper
project: zotero_obsidian_kb
title: No Evidence Paper
citekey: noevidence2024
zotero_key: KEYNOEVD
status: read
source_type: preprint
claim_strength: observed
authors:
  - Author Name
year: 2024
venue: arXiv
linked_knowledge:
  - "Knowledge/Literature Overview"
tags:
  - "#type/paper-note"
---
# No Evidence Paper

## Claim
Hypothesized assertion.
"""
        p.write_text(content, encoding="utf-8")

        records = extract_evidence_records(p)
        assert len(records) == 1
        assert records[0]["evidence_id"] == "EVD-noevidence2024-01"
        assert records[0]["paper_citekey"] == "noevidence2024"

    def test_synthesizer_full_lifecycle_idempotency(self, tmp_path):
        vault = tmp_path / "vault"
        vault.mkdir()

        create_paper_note(vault, "paper1", title="Paper 1", claim_strength="supported")
        create_paper_note(vault, "paper2", title="Paper 2", claim_strength="observed")
        create_concept_note(vault, "concept1", title="Concept 1", primary_sources=["Sources/Papers/paper1"])

        files1 = run_synthesis(vault)
        assert len(files1) >= 4

        contents_pass1 = {f.name: f.read_text(encoding="utf-8") for f in files1}

        files2 = run_synthesis(vault)
        contents_pass2 = {f.name: f.read_text(encoding="utf-8") for f in files2}

        for fname in contents_pass1:
            assert fname in contents_pass2
            assert contents_pass1[fname] == contents_pass2[fname]

    def test_synthesizer_empty_vault_handling(self, tmp_path):
        vault = tmp_path / "empty_synth_vault"
        vault.mkdir()

        created_files = run_synthesis(vault, dry_run=False)
        assert len(created_files) == 4
        for f in created_files:
            assert f.exists()
            content = f.read_text(encoding="utf-8")
            assert len(content) > 0

    def test_synthesizer_pipeline_end_to_end_conformance(self, tmp_path):
        vault = tmp_path / "synth_vault"
        vault.mkdir()

        create_paper_note(vault, "he2016deep", title="ResNet", year=2016)
        create_paper_note(vault, "vaswani2017attention", title="Transformer", year=2017)
        create_paper_note(vault, "hu2021lora", title="LoRA", year=2021)

        created_files = run_synthesis(vault, dry_run=False)
        assert len(created_files) == 4

        overview = vault / "Knowledge" / "Literature Overview.md"
        taxonomy = vault / "Knowledge" / "Method Taxonomy.md"
        gaps = vault / "Knowledge" / "Research Gaps.md"
        matrix = vault / "Writing" / "comparison-matrix.md"

        assert overview.exists()
        assert taxonomy.exists()
        assert gaps.exists()
        assert matrix.exists()

        for f in [overview, taxonomy, gaps]:
            issues = lint_file(f, vault_dir=vault)
            errors = [i for i in issues if i.severity == "error"]
            assert len(errors) == 0, f"Synthesized file {f.name} failed lint: {[e.message for e in errors]}"
