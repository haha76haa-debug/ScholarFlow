"""
Test Suite for kb_tools.cli and 'run-pipeline' subcommand.
Covers Tier 1 & Tier 2 test specifications for the 5-step automated workflow:
1. Lint (--strict)
2. Sync Registry
3. Check Links
4. Synthesize
5. Generate Canvas
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


def test_cli_run_pipeline_success_on_populated_vault(populated_vault, capsys):
    """Tier 2: CLI `kb-tools run-pipeline` succeeds with code 0 on a valid populated vault."""
    from kb_tools.cli import main

    exit_code = main(["run-pipeline", "--vault-dir", str(populated_vault), "--strict"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "Step 1/5: Strict Schema & Evidence Linter" in captured.out
    assert "Step 2/5: Master Registry & Index Sync" in captured.out
    assert "Step 3/5: Wikilink Integrity & Orphan Check" in captured.out
    assert "Step 4/5: Cross-Paper Knowledge Synthesizer" in captured.out
    assert "Step 5/5: Visual JSON Canvas Builder" in captured.out
    assert "Completed Successfully" in captured.out


def test_cli_run_pipeline_alias_underscore(populated_vault):
    """Tier 2: CLI `kb-tools run_pipeline` alias executes identically to `run-pipeline`."""
    from kb_tools.cli import main

    exit_code = main(["run_pipeline", "--vault-dir", str(populated_vault), "--strict"])
    assert exit_code == 0


def test_cli_run_pipeline_dry_run(populated_vault, capsys):
    """Tier 2: CLI `kb-tools run-pipeline --dry-run` executes without error."""
    from kb_tools.cli import main

    exit_code = main(["run-pipeline", "--vault-dir", str(populated_vault), "--dry-run"])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "dry_run=True" in captured.out


def test_cli_run_pipeline_json_output(populated_vault, capsys):
    """Tier 2: CLI `kb-tools run-pipeline --json` outputs structured JSON summary with 5 steps."""
    from kb_tools.cli import main

    exit_code = main(["run-pipeline", "--vault-dir", str(populated_vault), "--json"])
    assert exit_code == 0

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert data["status"] == "success"
    assert data["pipeline_passed"] is True
    assert len(data["steps"]) == 5

    step_names = [s["name"] for s in data["steps"]]
    assert step_names == ["lint", "sync_registry", "check_links", "synthesize", "generate_canvas"]
    for s in data["steps"]:
        assert s["passed"] is True


def test_cli_run_pipeline_strict_fails_on_broken_schema(tmp_vault, capsys):
    """Tier 2: CLI `run-pipeline --strict` fails with non-zero exit code if linting fails."""
    # Write a broken paper note
    bad_note = tmp_vault / "Sources" / "Papers" / "broken.md"
    bad_note.write_text("""---
type: paper
project: 2d-semiconductors
title: "Broken Note"
updated: invalid-date
---
# Broken Note
""", encoding="utf-8")

    from kb_tools.cli import main
    exit_code = main(["run-pipeline", "--vault-dir", str(tmp_vault), "--strict"])
    assert exit_code != 0


def test_cli_run_pipeline_fails_on_broken_links(populated_vault, capsys):
    """Tier 2: CLI `run-pipeline` fails with non-zero exit code if broken wikilinks exist."""
    # Introduce a broken wikilink in an existing note
    paper_file = populated_vault / "Sources" / "Papers" / "he2016deep.md"
    content = paper_file.read_text(encoding="utf-8")
    paper_file.write_text(content + "\n- [[NonExistentNote_12345]]\n", encoding="utf-8")

    from kb_tools.cli import main
    exit_code = main(["run-pipeline", "--vault-dir", str(populated_vault)])
    assert exit_code != 0


def test_cli_run_pipeline_invalid_vault_directory(tmp_path, capsys):
    """Tier 2: CLI `run-pipeline` with non-existent directory returns error code 1."""
    non_existent = tmp_path / "non_existent_vault_dir_xyz"
    from kb_tools.cli import main

    exit_code = main(["run-pipeline", "--vault-dir", str(non_existent)])
    assert exit_code != 0


def test_cli_no_subcommand_shows_help(capsys):
    """Tier 2: CLI without arguments shows help message and exits 1."""
    from kb_tools.cli import main

    exit_code = main([])
    assert exit_code == 1
    captured = capsys.readouterr()
    assert "usage:" in captured.out.lower() or "commands" in captured.out.lower()

