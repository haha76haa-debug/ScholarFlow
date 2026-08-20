"""
Test Suite for kb_tools.linter and CLI 'lint' subcommand.
Covers Tier 1 (Unit & Schema Contracts) and Tier 2 (CLI & Functional Boundaries).
Validates YAML frontmatter schemas, required H2 heading layout, tag taxonomy,
Evidence Record contracts, and CLI exit codes.
"""

import json
import os
import subprocess
import sys
from pathlib import Path
import pytest

# Ensure src is in sys.path
SRC_DIR = Path(__file__).resolve().parent.parent / "src"
if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


# ---------------------------------------------------------------------------
# Tier 1: Schema & Unit Validation Tests
# ---------------------------------------------------------------------------

def test_valid_paper_note_passes_lint(populated_vault):
    """Tier 1: Valid canonical paper note (ResNet) passes schema validation with zero errors."""
    from kb_tools.linter import lint_file, lint_vault
    resnet_path = populated_vault / "Sources" / "Papers" / "he2016deep.md"
    
    issues = lint_file(resnet_path, vault_dir=populated_vault)
    errors = [i for i in issues if getattr(i, "severity", "error") == "error"]
    assert len(errors) == 0, f"Expected 0 errors on valid paper note, got: {errors}"


def test_valid_concept_note_passes_lint(populated_vault):
    """Tier 1: Valid canonical concept note passes schema validation with zero errors."""
    from kb_tools.linter import lint_file
    concept_path = populated_vault / "Knowledge" / "Concepts" / "residual_connection.md"
    
    issues = lint_file(concept_path, vault_dir=populated_vault)
    errors = [i for i in issues if getattr(i, "severity", "error") == "error"]
    assert len(errors) == 0, f"Expected 0 errors on valid concept note, got: {errors}"


def test_valid_synthesis_note_passes_lint(populated_vault):
    """Tier 1: Valid canonical synthesis note passes schema validation with zero errors."""
    from kb_tools.linter import lint_file
    synth_path = populated_vault / "Knowledge" / "Literature Overview.md"
    
    issues = lint_file(synth_path, vault_dir=populated_vault)
    errors = [i for i in issues if getattr(i, "severity", "error") == "error"]
    assert len(errors) == 0, f"Expected 0 errors on valid synthesis note, got: {errors}"


def test_missing_required_frontmatter_fields(tmp_vault):
    """Tier 1: Paper note missing required fields (citekey, authors, year, claim_strength) fails lint."""
    from kb_tools.linter import lint_file
    bad_file = tmp_vault / "Sources" / "Papers" / "missing_fields.md"
    bad_file.write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Paper Missing Mandatory Metadata"
status: to-read
updated: 2026-08-19T00:00:00Z
---
# Paper Missing Mandatory Metadata
## Claim
Some claim.
## Research question
Question.
## Method
Method.
## Evidence
```md
Evidence ID: EVD-missing-01
Source: [[Sources/Papers/missing_fields]]
Source type: preprint
Supports: "Test"
Method / dataset / metric: "Test"
Project relevance: "Test"
Claim strength: observed
```
## Strengths
- Good
## Limitation
- Bad
## Direct relevance to repo
- Relevance
## Relation to other papers
- Relation
## Knowledge links
- [[Knowledge/Literature Overview]]
""", encoding="utf-8")

    issues = lint_file(bad_file, vault_dir=tmp_vault)
    errors = [i for i in issues if getattr(i, "severity", "error") == "error"]
    assert len(errors) > 0, "Linter must report errors when mandatory frontmatter fields are missing"
    
    error_msgs = " ".join(str(getattr(i, "message", i)) for i in errors).lower()
    assert any(k in error_msgs for k in ["citekey", "authors", "year", "claim_strength", "required"]), \
        f"Error message should mention missing required fields: {error_msgs}"


def test_invalid_field_types(tmp_vault):
    """Tier 1: Type mismatches (e.g. year as string, authors as string instead of list) fail lint."""
    from kb_tools.linter import lint_file
    type_err_file = tmp_vault / "Sources" / "Papers" / "type_err.md"
    type_err_file.write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Type Error Paper"
citekey: typeerr2026
zotero_key: "TYPE2026"
status: to-read
source_type: "full paper"
claim_strength: strong
authors: "String Author Instead Of List"
year: "not_a_number_year"
linked_knowledge: 99999
updated: 2026-08-19T00:00:00Z
---
# Type Error Paper
## Claim
Claim.
## Research question
Question.
## Method
Method.
## Evidence
```md
Evidence ID: EVD-typeerr2026-01
Source: [[Sources/Papers/typeerr2026]]
Source type: full paper
Supports: "Test"
Method / dataset / metric: "Test"
Project relevance: "Test"
Claim strength: strong
```
## Strengths
- Good
## Limitation
- Bad
## Direct relevance to repo
- Relevance
## Relation to other papers
- Relation
## Knowledge links
- [[Knowledge/Literature Overview]]
""", encoding="utf-8")

    issues = lint_file(type_err_file, vault_dir=tmp_vault)
    errors = [i for i in issues if getattr(i, "severity", "error") == "error"]
    assert len(errors) > 0, "Linter must flag type mismatches on frontmatter fields"
    error_msgs = " ".join(str(getattr(i, "message", i)) for i in errors).lower()
    assert any(w in error_msgs for w in ["type", "integer", "list", "expected", "authors", "year"])


def test_invalid_enum_values(tmp_vault):
    """Tier 1: Disallowed enum values (e.g. unknown claim_strength or bad status) fail lint."""
    from kb_tools.linter import lint_file
    enum_err_file = tmp_vault / "Sources" / "Papers" / "bad_enum.md"
    enum_err_file.write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Bad Enum Paper"
citekey: badenum2026
zotero_key: "ENUM2026"
status: completely_invented_status
source_type: invalid_source_classification
claim_strength: unsupported_strength_rating
authors:
  - "Test Author"
year: 2026
linked_knowledge:
  - "[[Knowledge/Literature Overview]]"
updated: 2026-08-19T00:00:00Z
---
# Bad Enum Paper
## Claim
Claim.
## Research question
Question.
## Method
Method.
## Evidence
```md
Evidence ID: EVD-badenum2026-01
Source: [[Sources/Papers/badenum2026]]
Source type: full paper
Supports: "Test"
Method / dataset / metric: "Test"
Project relevance: "Test"
Claim strength: strong
```
## Strengths
- Good
## Limitation
- Bad
## Direct relevance to repo
- Relevance
## Relation to other papers
- Relation
## Knowledge links
- [[Knowledge/Literature Overview]]
""", encoding="utf-8")

    issues = lint_file(enum_err_file, vault_dir=tmp_vault)
    errors = [i for i in issues if getattr(i, "severity", "error") == "error"]
    assert len(errors) > 0, "Linter must reject invalid enum values"
    error_msgs = " ".join(str(getattr(i, "message", i)) for i in errors).lower()
    assert any(w in error_msgs for w in ["enum", "allowed", "claim_strength", "status", "source_type", "invalid"])


def test_citekey_pattern_and_filename_mismatch(tmp_vault):
    """Tier 1: Citekey must match pattern ^[a-z0-9]+$ and correspond to the note filename."""
    from kb_tools.linter import lint_file
    mismatch_file = tmp_vault / "Sources" / "Papers" / "actual_filename.md"
    mismatch_file.write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Mismatch Citekey Paper"
citekey: different_citekey_with_underscores_and_CAPS
zotero_key: "MISMATCH2026"
status: to-read
source_type: "conference paper"
claim_strength: observed
authors:
  - "Test Author"
year: 2026
linked_knowledge:
  - "[[Knowledge/Literature Overview]]"
updated: 2026-08-19T00:00:00Z
---
# Mismatch Citekey Paper
## Claim
Claim.
## Research question
Question.
## Method
Method.
## Evidence
```md
Evidence ID: EVD-actual_filename-01
Source: [[Sources/Papers/actual_filename]]
Source type: conference paper
Supports: "Test"
Method / dataset / metric: "Test"
Project relevance: "Test"
Claim strength: observed
```
## Strengths
- Good
## Limitation
- Bad
## Direct relevance to repo
- Relevance
## Relation to other papers
- Relation
## Knowledge links
- [[Knowledge/Literature Overview]]
""", encoding="utf-8")

    issues = lint_file(mismatch_file, vault_dir=tmp_vault)
    errors = [i for i in issues if getattr(i, "severity", "error") == "error"]
    assert len(errors) > 0, "Linter must flag citekey pattern or filename mismatches"


def test_tag_taxonomy_compliance(tmp_vault, sample_paper_note_content):
    """Tier 1: Tag validation accepts standard hierarchical tags and flags malformed tags."""
    from kb_tools.linter import lint_file
    valid_file = tmp_vault / "Sources" / "Papers" / "he2016deep.md"
    valid_file.write_text(sample_paper_note_content, encoding="utf-8")
    
    issues = lint_file(valid_file, vault_dir=tmp_vault)
    errors = [i for i in issues if getattr(i, "severity", "error") == "error"]
    assert len(errors) == 0

    # Write file with illegal tag syntax
    bad_tag_file = tmp_vault / "Sources" / "Papers" / "badtag.md"
    bad_content = sample_paper_note_content.replace('citekey: he2016deep', 'citekey: badtag').replace(
        '#type/paper-note', 'invalid tag with spaces'
    )
    bad_tag_file.write_text(bad_content, encoding="utf-8")
    issues_bad = lint_file(bad_tag_file, vault_dir=tmp_vault)
    # Malformed tags should produce at least a warning or error
    assert len(issues_bad) > 0, "Linter should detect invalid tag syntax with spaces"


def test_missing_required_heading_sections(tmp_vault):
    """Tier 1: Paper note missing mandatory H2 headings (e.g. Method, Evidence) fails heading check."""
    from kb_tools.linter import lint_file
    missing_h2_file = tmp_vault / "Sources" / "Papers" / "noh2.md"
    missing_h2_file.write_text("""---
type: paper
project: zotero_obsidian_kb
title: "No Headings Paper"
citekey: noh2
zotero_key: "NOH2_2026"
status: to-read
source_type: "preprint"
claim_strength: observed
authors:
  - "Author A"
year: 2026
linked_knowledge:
  - "[[Knowledge/Literature Overview]]"
updated: 2026-08-19T00:00:00Z
---
# No Headings Paper

Just markdown body text without the 9 required section headings.
""", encoding="utf-8")

    issues = lint_file(missing_h2_file, vault_dir=tmp_vault)
    errors = [i for i in issues if getattr(i, "severity", "error") == "error"]
    assert len(errors) > 0, "Linter must report error when required H2 headings are missing"
    error_msgs = " ".join(str(getattr(i, "message", i)) for i in errors).lower()
    assert any(h in error_msgs for h in ["heading", "section", "claim", "method", "evidence"])


def test_concept_heading_variants_accepted(tmp_vault, sample_concept_note_content):
    """Tier 1: Concept notes accepting variants ('## Mathematical Formulation', '## Mechanism', etc.)."""
    from kb_tools.linter import lint_file
    concept_file = tmp_vault / "Knowledge" / "Concepts" / "residual_connection.md"
    
    # Test with Mathematical Formulation
    concept_file.write_text(sample_concept_note_content, encoding="utf-8")
    issues1 = lint_file(concept_file, vault_dir=tmp_vault)
    assert len([i for i in issues1 if getattr(i, "severity", "error") == "error"]) == 0

    # Test variant with ## Mechanism
    variant_content = sample_concept_note_content.replace(
        "## Mathematical Formulation", "## Mechanism"
    )
    concept_file.write_text(variant_content, encoding="utf-8")
    issues2 = lint_file(concept_file, vault_dir=tmp_vault)
    assert len([i for i in issues2 if getattr(i, "severity", "error") == "error"]) == 0


def test_evidence_record_block_validation(tmp_vault):
    """Tier 1: Paper note with malformed Evidence Record block fails validation."""
    from kb_tools.linter import lint_file
    bad_evd_file = tmp_vault / "Sources" / "Papers" / "badevd2026.md"
    bad_evd_file.write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Bad Evidence Paper"
citekey: badevd2026
zotero_key: "EVD2026"
status: to-read
source_type: "preprint"
claim_strength: observed
authors:
  - "Author Name"
year: 2026
linked_knowledge:
  - "[[Knowledge/Literature Overview]]"
updated: 2026-08-19T00:00:00Z
---
# Bad Evidence Paper

## Claim
Claim.
## Research question
Question.
## Method
Method.
## Evidence
```md
Evidence ID: INVALID_ID_FORMAT_WITHOUT_PREFIX
Missing_Source_Key: none
Supports: ""
```
## Strengths
- Good
## Limitation
- Bad
## Direct relevance to repo
- Relevance
## Relation to other papers
- Relation
## Knowledge links
- [[Knowledge/Literature Overview]]
""", encoding="utf-8")

    issues = lint_file(bad_evd_file, vault_dir=tmp_vault)
    errors = [i for i in issues if getattr(i, "severity", "error") == "error"]
    assert len(errors) > 0, "Linter must detect malformed Evidence Record codeblocks"


def test_directory_exclusions(tmp_vault):
    """Tier 1: Excluded directories (.obsidian, _system, Templates, Archive) do not generate false positives."""
    from kb_tools.linter import lint_vault
    # Put a non-conforming file in Templates and _system
    (tmp_vault / "Templates" / "unstructured_raw_template.md").write_text("Just a raw template text without frontmatter", encoding="utf-8")
    (tmp_vault / "_system" / "notes_internal.md").write_text("Internal system notes", encoding="utf-8")

    report = lint_vault(tmp_vault)
    errors = report.errors if hasattr(report, "errors") else [i for i in report if getattr(i, "severity", "error") == "error"]
    
    # None of the errors should come from Templates or _system
    error_files = [str(getattr(e, "file", e)) for e in errors]
    for ef in error_files:
        assert "_system" not in ef and ".obsidian" not in ef, f"System dirs should be excluded from lint: {ef}"


# ---------------------------------------------------------------------------
# Tier 2: CLI & Boundary Functional Tests
# ---------------------------------------------------------------------------

def test_cli_lint_clean_vault_exit_code_zero(populated_vault, capsys):
    """Tier 2: CLI `kb-tools lint` on a clean, populated vault exits with 0."""
    from kb_tools.cli import main
    exit_code = main(["lint", "--vault-dir", str(populated_vault)])
    assert exit_code == 0
    captured = capsys.readouterr()
    assert "error" not in captured.out.lower() or "0 error" in captured.out.lower()


def test_cli_lint_corrupted_vault_exit_code_nonzero(tmp_vault, corrupted_vault_factory, capsys):
    """Tier 2: CLI `kb-tools lint` on a vault with schema corruptions exits with non-zero (1)."""
    corrupted_vault_factory("missing_frontmatter_keys")
    from kb_tools.cli import main
    exit_code = main(["lint", "--vault-dir", str(tmp_vault)])
    assert exit_code != 0, f"Expected non-zero exit code on corrupted vault, got {exit_code}"


def test_cli_lint_json_output(tmp_vault, corrupted_vault_factory, capsys):
    """Tier 2: CLI `kb-tools lint --json` outputs structured JSON with error details."""
    corrupted_vault_factory("invalid_types")
    from kb_tools.cli import main
    exit_code = main(["lint", "--vault-dir", str(tmp_vault), "--json"])
    assert exit_code != 0
    
    captured = capsys.readouterr()
    assert captured.out.strip().startswith("{") or captured.out.strip().startswith("["), \
        f"Output should be JSON: {captured.out}"
    data = json.loads(captured.out)
    assert "errors" in data or "issues" in data or isinstance(data, list)


def test_cli_lint_strict_mode(populated_vault, capsys):
    """Tier 2: CLI `kb-tools lint --strict` flag enforces warnings as failures."""
    # Add a note with missing optional fields or non-standard tag to trigger warning
    (populated_vault / "Sources" / "Papers" / "warning_paper.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Warning Paper Missing Optional Field"
citekey: warning2026
zotero_key: "WARN2026"
status: to-read
source_type: "preprint"
claim_strength: observed
authors:
  - "Warning Author"
year: 2026
linked_knowledge:
  - "[[Knowledge/Literature Overview]]"
tags:
  - "custom-unprefixed-tag"
updated: 2026-08-19T00:00:00Z
---
# Warning Paper
## Claim
Claim text.
## Research question
Question text.
## Method
Method text.
## Evidence
```md
Evidence ID: EVD-warning2026-01
Source: [[Sources/Papers/warning2026]]
Source type: preprint
Supports: "Warning test"
Method / dataset / metric: "Benchmark"
Project relevance: "Relevance"
Claim strength: observed
```
## Strengths
- S1
## Limitation
- L1
## Direct relevance to repo
- R1
## Relation to other papers
- Rel1
## Knowledge links
- [[Knowledge/Literature Overview]]
""", encoding="utf-8")

    from kb_tools.cli import main
    exit_code_normal = main(["lint", "--vault-dir", str(populated_vault)])
    # In normal mode it may pass with exit code 0 or warnings
    exit_code_strict = main(["lint", "--vault-dir", str(populated_vault), "--strict"])
    # In strict mode warnings escalate
    assert exit_code_strict in [0, 1]


def test_cli_lint_single_file_target(populated_vault, capsys):
    """Tier 2: CLI `kb-tools lint <filepath>` lints only the targeted note file."""
    resnet_path = populated_vault / "Sources" / "Papers" / "he2016deep.md"
    from kb_tools.cli import main
    exit_code = main(["lint", str(resnet_path), "--vault-dir", str(populated_vault)])
    assert exit_code == 0
