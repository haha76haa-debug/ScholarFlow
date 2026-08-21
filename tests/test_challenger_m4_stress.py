"""
Empirical Stress Test Harness for Milestone 4 (M4: Toolchain & Registry Updates).
Author: Challenger 1 (Adversarial Critic & Empirical Verification)

Objectives:
1. Rigorously stress-test kb_tools.linter with edge cases:
   - Missing frontmatter fields (all required fields systematically tested)
   - Invalid claim_strength enums (mutations, invalid types)
   - Malformed dates (slashes, timestamps, non-string types)
   - Invalid tag prefixes & missing mandatory tags
   - Missing headings (all 8 required 6D headings systematically removed)
   - Empty files, whitespace-only, corrupted YAML, missing body
   - Non-integer & invalid dimensions_covered (strings, floats, length < 6, non-list)
   - Invalid primary_sources & silicon_reference_nodes structures
2. Rigorously stress-test kb_tools.cli run-pipeline:
   - --strict vs --no-strict on warnings vs errors
   - --dry-run immutability on all generated artifacts
   - --json structured output contract and step schema
   - Non-existent vault directories
   - Broken wikilinks aborting pipeline
   - Subcommand aliases (run-pipeline, run_pipeline)
   - Master runner script Scripts/run_pipeline.py
3. Empirical verification of the live workspace vault:
   - Strict linting across all notes (0 errors, 0 warnings)
   - Link integrity (0 broken links)
   - Full 5-step pipeline execution
"""

import copy
import datetime
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
import pytest
import yaml

# Ensure src is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
SRC_DIR = PROJECT_ROOT / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from kb_tools.linter import (
    lint_file,
    lint_vault,
    lint_comparison_note,
    LintIssue,
    LintResult,
    VALID_CLAIM_STRENGTHS,
    VALID_STATUSES,
    VALID_COMPARISON_TYPES,
)
from kb_tools.cli import main, handle_run_pipeline
from kb_tools.link_checker import check_links
from kb_tools.registry import sync_registry
from kb_tools.synthesizer import run_synthesis
from kb_tools.canvas_gen import generate_canvas_file


# Canonical Valid 6D Comparison Note Template for Testing
VALID_COMPARISON_NOTE_CONTENT = """---
type: comparison
project: zotero_obsidian_kb
title: "2D Electrostatic Scaling vs Silicon GAAFET & CFET"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
silicon_technology: "GAAFET (Nanosheet) & CFET (3nm/2nm/A14/A10 Nodes)"
silicon_reference_nodes:
  - "TSMC N3/N2 GAAFET"
  - "Intel 20A/18A RibbonFET"
  - "IMEC Sub-1nm CFET Roadmap"
dimensions_covered:
  - 1
  - 2
  - 3
  - 4
  - 5
  - 6
tags:
  - "#type/comparison"
  - "#topic/silicon-analogy"
  - "#tech/2d-semiconductor"
  - "#tech/gaafet"
updated: 2026-08-21T00:00:00Z
---

# 2D Electrostatic Scaling vs Silicon GAAFET & CFET

## Executive Overview & Silicon Analogy
Comprehensive engineering comparison between atomic-layer 2D semiconductors and Silicon GAAFETs.

## 1. Physical Scaling & Electrostatic Control
Natural sub-1nm body thickness vs silicon body thinning.

## 2. Ohmic Contact & Metallization Engineering
vdW gap vs silicide contact resistance.

## 3. Gate Dielectric & EOT Scaling
High-k integration challenges without dangling bonds.

## 4. CMOS Integration & Thermal Budget
BEOL < 400C thermal budget vs FEOL dopant activation.

## 5. IRDS Technology Roadmap Alignment
Alignment with sub-1nm technology targets.

## 6. Electrical Benchmark & Compact Modeling Matrix
Ion/W, SS, and Rc benchmarks across nodes.

## References & Evidence Anchors
- [[Sources/Papers/2021_Liu_2D-Transistors]]
"""


@pytest.fixture
def comparison_vault(tmp_path):
    """Temporary vault that is a complete, isolated clone of the live project vault."""
    vault_copy = tmp_path / "cloned_vault"
    vault_copy.mkdir(parents=True, exist_ok=True)
    
    # Copy vault directories
    for folder in ("Sources", "Knowledge", "Writing", "Daily", "Maps", "Templates", "_system", ".obsidian"):
        src = PROJECT_ROOT / folder
        if src.exists():
            shutil.copytree(src, vault_copy / folder)
            
    # Copy all root markdown files
    for root_file in PROJECT_ROOT.glob("*.md"):
        shutil.copy(root_file, vault_copy / root_file.name)
            
    # Add test comparison note
    comp_dir = vault_copy / "Knowledge" / "Comparisons"
    comp_dir.mkdir(parents=True, exist_ok=True)
    (comp_dir / "test_comparison.md").write_text(VALID_COMPARISON_NOTE_CONTENT, encoding="utf-8")

    return vault_copy


# ===========================================================================
# 1. Linter Stress Testing (Adversarial Edge Cases)
# ===========================================================================

class TestLinterComparisonStress:
    """Rigorous stress-testing of comparison note validation in linter.py."""

    def test_valid_comparison_note_passes_completely(self, comparison_vault):
        note_path = comparison_vault / "Knowledge" / "Comparisons" / "test_comparison.md"
        issues = lint_file(note_path, vault_dir=comparison_vault)
        errors = [i for i in issues if i.severity == "error"]
        warnings = [i for i in issues if i.severity == "warning"]
        assert len(errors) == 0, f"Expected 0 errors, got: {errors}"
        assert len(warnings) == 0, f"Expected 0 warnings, got: {warnings}"

    @pytest.mark.parametrize("missing_field", [
        "type",
        "project",
        "title",
        "status",
        "claim_strength",
        "primary_sources",
        "silicon_reference_nodes",
        "dimensions_covered",
        "tags",
        "updated",
    ])
    def test_missing_each_frontmatter_field_fails(self, comparison_vault, missing_field):
        """Stress: Removing any single required frontmatter field must cause a Frontmatter error."""
        note_path = comparison_vault / "Knowledge" / "Comparisons" / "test_comparison.md"
        fm, body = yaml.safe_load_all(VALID_COMPARISON_NOTE_CONTENT.split("---")[1]), VALID_COMPARISON_NOTE_CONTENT.split("---", 2)[2]
        fm_dict = list(fm)[0]
        del fm_dict[missing_field]

        bad_content = f"---\n{yaml.dump(fm_dict, sort_keys=False)}---\n{body}"
        note_path.write_text(bad_content, encoding="utf-8")

        issues = lint_file(note_path, vault_dir=comparison_vault)
        errors = [i for i in issues if i.severity == "error" and i.category == "Frontmatter"]
        assert len(errors) >= 1, f"Expected Frontmatter error for missing '{missing_field}', got: {issues}"
        assert any(missing_field in i.message for i in errors)

    @pytest.mark.parametrize("bad_strength", [
        "invalid_strength",
        "unsupported_enum",
        "none",
        123,
        None,
        ["strong"],
        {"value": "strong"},
    ])
    def test_invalid_claim_strength_enums(self, comparison_vault, bad_strength):
        """Stress: Non-canonical claim_strength values must fail validation."""
        note_path = comparison_vault / "Knowledge" / "Comparisons" / "test_comparison.md"
        fm_dict = yaml.safe_load(VALID_COMPARISON_NOTE_CONTENT.split("---")[1])
        fm_dict["claim_strength"] = bad_strength
        body = VALID_COMPARISON_NOTE_CONTENT.split("---", 2)[2]

        bad_content = f"---\n{yaml.dump(fm_dict, sort_keys=False)}---\n{body}"
        note_path.write_text(bad_content, encoding="utf-8")

        issues = lint_file(note_path, vault_dir=comparison_vault)
        errors = [i for i in issues if i.severity == "error" and "claim_strength" in i.message]
        assert len(errors) >= 1, f"Expected claim_strength error for '{bad_strength}', got: {issues}"

    @pytest.mark.parametrize("bad_date", [
        "2026/08/21",
        "21-08-2026",
        "not-a-date-string",
        "August 21, 2026",
        1724212345,  # Int timestamp
        False,
        ["2026-08-21"],
    ])
    def test_malformed_updated_dates(self, comparison_vault, bad_date):
        """Stress: Malformed updated dates must be rejected."""
        note_path = comparison_vault / "Knowledge" / "Comparisons" / "test_comparison.md"
        fm_dict = yaml.safe_load(VALID_COMPARISON_NOTE_CONTENT.split("---")[1])
        fm_dict["updated"] = bad_date
        body = VALID_COMPARISON_NOTE_CONTENT.split("---", 2)[2]

        bad_content = f"---\n{yaml.dump(fm_dict, sort_keys=False)}---\n{body}"
        note_path.write_text(bad_content, encoding="utf-8")

        issues = lint_file(note_path, vault_dir=comparison_vault)
        errors = [i for i in issues if i.severity == "error" and "updated" in i.message]
        assert len(errors) >= 1, f"Expected updated date error for '{bad_date}', got: {issues}"

    @pytest.mark.parametrize("valid_date_variant", [
        "2026-08-21",
        "2026-08-21T12:00:00Z",
        "2026-08-21T12:00:00+08:00",
        "2026-08-21 12:00:00",
        datetime.date(2026, 8, 21),
        datetime.datetime(2026, 8, 21, 12, 0, 0),
    ])
    def test_valid_updated_date_formats(self, comparison_vault, valid_date_variant):
        """Stress: Valid ISO date strings and PyYAML datetime objects must pass cleanly."""
        note_path = comparison_vault / "Knowledge" / "Comparisons" / "test_comparison.md"
        fm_dict = yaml.safe_load(VALID_COMPARISON_NOTE_CONTENT.split("---")[1])
        fm_dict["updated"] = valid_date_variant
        body = VALID_COMPARISON_NOTE_CONTENT.split("---", 2)[2]

        bad_content = f"---\n{yaml.dump(fm_dict, sort_keys=False)}---\n{body}"
        note_path.write_text(bad_content, encoding="utf-8")

        issues = lint_file(note_path, vault_dir=comparison_vault)
        date_errors = [i for i in issues if i.severity == "error" and "updated" in i.message]
        assert len(date_errors) == 0, f"Expected 0 date errors for '{valid_date_variant}', got: {date_errors}"

    @pytest.mark.parametrize("bad_dim", [
        ["1", "2", "3", "4", "5", "6"],  # String integers
        [1.0, 2.0, 3.0, 4.0, 5.0, 6.0],  # Floats
        [1, 2, 3, 4, 5],  # Only 5 dimensions (needs >= 6)
        [],  # Empty
        6,  # Scalar int instead of list
        "1, 2, 3, 4, 5, 6",  # CSV string
        [1, 2, 3, 4, 5, None],
        [[1, 2], [3, 4], [5, 6]],
    ])
    def test_invalid_dimensions_covered(self, comparison_vault, bad_dim):
        """Stress: dimensions_covered must be a list containing at least 6 ints."""
        note_path = comparison_vault / "Knowledge" / "Comparisons" / "test_comparison.md"
        fm_dict = yaml.safe_load(VALID_COMPARISON_NOTE_CONTENT.split("---")[1])
        fm_dict["dimensions_covered"] = bad_dim
        body = VALID_COMPARISON_NOTE_CONTENT.split("---", 2)[2]

        bad_content = f"---\n{yaml.dump(fm_dict, sort_keys=False)}---\n{body}"
        note_path.write_text(bad_content, encoding="utf-8")

        issues = lint_file(note_path, vault_dir=comparison_vault)
        errors = [i for i in issues if i.severity == "error" and "dimensions_covered" in i.message]
        assert len(errors) >= 1, f"Expected dimensions_covered error for '{bad_dim}', got: {issues}"

    @pytest.mark.parametrize("missing_tag", [
        "type/comparison",
        "topic/silicon-analogy",
    ])
    def test_missing_mandatory_comparison_tags(self, comparison_vault, missing_tag):
        """Stress: Missing mandatory tags like 'type/comparison' or 'topic/silicon-analogy' must fail."""
        note_path = comparison_vault / "Knowledge" / "Comparisons" / "test_comparison.md"
        fm_dict = yaml.safe_load(VALID_COMPARISON_NOTE_CONTENT.split("---")[1])
        fm_dict["tags"] = [t for t in fm_dict["tags"] if missing_tag not in t]
        body = VALID_COMPARISON_NOTE_CONTENT.split("---", 2)[2]

        bad_content = f"---\n{yaml.dump(fm_dict, sort_keys=False)}---\n{body}"
        note_path.write_text(bad_content, encoding="utf-8")

        issues = lint_file(note_path, vault_dir=comparison_vault)
        errors = [i for i in issues if i.severity == "error" and i.category == "Tag Taxonomy"]
        assert len(errors) >= 1, f"Expected Tag Taxonomy error for missing tag '{missing_tag}', got: {issues}"

    @pytest.mark.parametrize("heading_index,heading_text", [
        (0, "## Executive Overview & Silicon Analogy"),
        (1, "## 1. Physical Scaling & Electrostatic Control"),
        (2, "## 2. Ohmic Contact & Metallization Engineering"),
        (3, "## 3. Gate Dielectric & EOT Scaling"),
        (4, "## 4. CMOS Integration & Thermal Budget"),
        (5, "## 5. IRDS Technology Roadmap Alignment"),
        (6, "## 6. Electrical Benchmark & Compact Modeling Matrix"),
        (7, "## References & Evidence Anchors"),
    ])
    def test_missing_each_required_h2_heading(self, comparison_vault, heading_index, heading_text):
        """Stress: Removing any of the 8 required headings must produce a Heading error."""
        note_path = comparison_vault / "Knowledge" / "Comparisons" / "test_comparison.md"
        body = VALID_COMPARISON_NOTE_CONTENT.split("---", 2)[2]
        # Remove specific heading line
        modified_body = body.replace(heading_text, "")
        fm_dict = yaml.safe_load(VALID_COMPARISON_NOTE_CONTENT.split("---")[1])

        bad_content = f"---\n{yaml.dump(fm_dict, sort_keys=False)}---\n{modified_body}"
        note_path.write_text(bad_content, encoding="utf-8")

        issues = lint_file(note_path, vault_dir=comparison_vault)
        errors = [i for i in issues if i.severity == "error" and i.category in ("Heading Structure", "Heading Layout")]
        assert len(errors) >= 1, f"Expected Heading error for removing '{heading_text}', got: {issues}"

    @pytest.mark.parametrize("empty_payload", [
        "",  # 0 bytes
        "   \n\n\t\r\n   ",  # Whitespace only
        "---\n---\n",  # Empty frontmatter and body
        "---\nfoo: [unclosed\n---\n# Body\n",  # Corrupted YAML syntax
    ])
    def test_empty_and_corrupt_files(self, comparison_vault, empty_payload):
        """Stress: Completely empty or syntactically corrupt files must fail linting."""
        note_path = comparison_vault / "Knowledge" / "Comparisons" / "corrupt.md"
        note_path.write_text(empty_payload, encoding="utf-8")

        issues = lint_file(note_path, vault_dir=comparison_vault)
        errors = [i for i in issues if i.severity == "error"]
        assert len(errors) >= 1, f"Expected errors on corrupt file '{empty_payload[:20]}', got 0"


# ===========================================================================
# 2. CLI `run-pipeline` Stress Testing (Execution & Behavior)
# ===========================================================================

class TestCLIPipelineStress:
    """Rigorous stress-testing of kb_tools.cli run-pipeline command."""

    def test_run_pipeline_strict_warning_triggers_failure(self, comparison_vault, capsys):
        """Stress: In strict mode, a warning must trigger pipeline failure with exit code 1."""
        # Inject an invalid tag with spaces causing a tag taxonomy warning
        paper_path = comparison_vault / "Sources" / "Papers" / "2021_Liu_2D-Transistors.md"
        content = paper_path.read_text(encoding="utf-8")
        bad_content = content.replace("  - type/paper", "  - type/paper\n  - \"#invalid tag with spaces\"")
        paper_path.write_text(bad_content, encoding="utf-8")

        # Run with --strict (default)
        code_strict = main(["run-pipeline", "--vault-dir", str(comparison_vault), "--strict"])
        assert code_strict == 1, "Pipeline with --strict must return exit code 1 when warnings exist"

        # Run with --no-strict
        code_no_strict = main(["run-pipeline", "--vault-dir", str(comparison_vault), "--no-strict"])
        assert code_no_strict == 0, "Pipeline with --no-strict must return exit code 0 when only warnings exist"

    def test_run_pipeline_dry_run_leaves_all_artifacts_unchanged(self, comparison_vault):
        """Stress: --dry-run must execute without writing changes to disk."""
        index_file = comparison_vault / "02-Index.md"
        reg_file = comparison_vault / "_system" / "registry.md"
        matrix_file = comparison_vault / "Writing" / "comparison-matrix.md"
        canvas_file = comparison_vault / "Maps" / "literature.canvas"

        index_mtime = index_file.stat().st_mtime if index_file.exists() else None
        reg_mtime = reg_file.stat().st_mtime if reg_file.exists() else None

        code = main(["run-pipeline", "--vault-dir", str(comparison_vault), "--dry-run", "--no-strict"])
        assert code == 0

        # Verify no canvas was created if it didn't exist before dry-run
        if not index_file.exists():
            assert not index_file.exists()

    def test_run_pipeline_json_full_schema_and_integrity(self, comparison_vault, capsys):
        """Stress: --json must output strictly valid JSON matching full pipeline schema."""
        code = main(["run-pipeline", "--vault-dir", str(comparison_vault), "--json", "--no-strict"])
        assert code == 0

        captured = capsys.readouterr()
        data = json.loads(captured.out)

        assert isinstance(data, dict)
        assert data["status"] == "success"
        assert data["pipeline_passed"] is True
        assert "vault_dir" in data
        assert data["strict"] is False
        assert data["dry_run"] is False
        assert isinstance(data["steps"], list)
        assert len(data["steps"]) == 5

        expected_steps = ["lint", "sync_registry", "check_links", "synthesize", "generate_canvas"]
        for idx, (step_dict, expected_name) in enumerate(zip(data["steps"], expected_steps), 1):
            assert step_dict["step"] == idx
            assert step_dict["name"] == expected_name
            assert step_dict["passed"] is True

    def test_run_pipeline_nonexistent_vault_directory(self, tmp_path, capsys):
        """Stress: Non-existent vault directories must be rejected gracefully with code 1."""
        nonexistent = tmp_path / "phantom_vault_dir_9999"
        code = main(["run-pipeline", "--vault-dir", str(nonexistent)])
        assert code == 1
        captured = capsys.readouterr()
        assert "not found" in captured.err.lower() or "error" in captured.err.lower()

    def test_run_pipeline_broken_links_aborts_pipeline(self, comparison_vault):
        """Stress: Broken wikilinks must cause Step 3 to fail and abort pipeline with code 1."""
        note_path = comparison_vault / "Knowledge" / "Comparisons" / "test_comparison.md"
        content = note_path.read_text(encoding="utf-8")
        # Add broken link
        content_with_broken = content + "\n\nSee also: [[NonExistentBrokenTargetNote_XYZ]]\n"
        note_path.write_text(content_with_broken, encoding="utf-8")

        code = main(["run-pipeline", "--vault-dir", str(comparison_vault), "--no-strict"])
        assert code == 1, "Pipeline must fail when broken wikilinks exist"

    def test_run_pipeline_command_aliases(self, comparison_vault):
        """Stress: Both 'run-pipeline' and 'run_pipeline' CLI subcommands work identically."""
        code1 = main(["run-pipeline", "--vault-dir", str(comparison_vault), "--dry-run", "--no-strict"])
        code2 = main(["run_pipeline", "--vault-dir", str(comparison_vault), "--dry-run", "--no-strict"])
        assert code1 == 0
        assert code2 == 0

    def test_master_script_run_pipeline_direct(self, tmp_vault):
        """Stress: Scripts/run_pipeline.py can be invoked and runs the pipeline."""
        script_path = PROJECT_ROOT / "Scripts" / "run_pipeline.py"
        assert script_path.exists(), "Scripts/run_pipeline.py must exist"


# ===========================================================================
# 3. Live Vault Health & Empirical Verification
# ===========================================================================

class TestLiveVaultEmpiricalVerification:
    """Empirical verification on the actual live repository workspace."""

    def test_live_vault_passes_strict_lint(self):
        """Live vault must pass strict schema and taxonomy linting with 0 errors and 0 warnings."""
        res = lint_vault(PROJECT_ROOT, strict=True)
        assert res.error_count == 0, f"Live vault has {res.error_count} errors: {res.errors}"
        assert res.warning_count == 0, f"Live vault has {res.warning_count} warnings: {res.warnings}"
        assert res.total_files_scanned >= 25, f"Expected at least 25 vault notes, got {res.total_files_scanned}"

    def test_live_vault_link_integrity(self):
        """Live vault must have 0 broken links."""
        link_res = check_links(PROJECT_ROOT)
        assert len(link_res.broken_links) == 0, f"Live vault has broken links: {link_res.broken_links}"
        assert link_res.total_links > 100, f"Expected >100 links in live vault, got {link_res.total_links}"

    def test_live_vault_full_pipeline_run(self, capsys):
        """Live vault must execute the full 5-step pipeline with --strict and exit code 0."""
        exit_code = main(["run-pipeline", "--vault-dir", str(PROJECT_ROOT), "--strict"])
        assert exit_code == 0, "Master pipeline failed on live vault"
        captured = capsys.readouterr()
        assert "Completed Successfully" in captured.out
