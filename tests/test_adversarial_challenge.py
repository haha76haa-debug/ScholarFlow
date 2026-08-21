"""
Adversarial Stress-Testing and Empirical Challenge Suite for Academic Knowledge Base System.
Authored by Challenger 1 (teamwork_preview_challenger).
"""

import json
import os
import shutil
import sys
from pathlib import Path
import pytest
import yaml

from kb_tools.cli import main
from kb_tools.linter import lint_vault, lint_file
from kb_tools.link_checker import check_links, repair_links
from kb_tools.ingest import ingest_file, parse_bibtex, parse_csl_json
from kb_tools.registry import sync_registry
from kb_tools.synthesizer import run_synthesis
from kb_tools.canvas_gen import build_canvas_graph, generate_canvas_file


def make_valid_paper_note(citekey="valid2024", title="Valid Paper Title"):
    return f"""---
type: paper
project: zotero_obsidian_kb
title: "{title}"
citekey: {citekey}
zotero_key: "KEY{citekey.upper()}"
status: read
source_type: "conference paper"
claim_strength: strong
authors:
  - "Author, One"
year: 2024
linked_knowledge:
  - "[[Knowledge/Literature Overview]]"
updated: "2026-08-19T00:00:00Z"
tags:
  - "#type/paper-note"
---
# {title}

## Claim
A valid claim assertion.

## Research question
What is the core question?

## Method
Core methodology description.

## Evidence
```evidence
Evidence ID: EVD-{citekey}-01
Source: [[Sources/Papers/{citekey}]]
Source type: conference paper
Supports: [[Knowledge/Literature Overview]]
Method / dataset / metric: Benchmark evaluation
Project relevance: Essential reference
Claim strength: strong
```

## Strengths
High empirical rigor.

## Limitation
Evaluated only on English datasets.

## Direct relevance to repo
Directly guides implementation.

## Relation to other papers
- Extends previous work.

## Knowledge links
- [[Knowledge/Literature Overview]]
"""


class TestMalformedYamlAndFrontmatter:
    """Adversarial testing of YAML parsing, malformed frontmatter, missing keys, invalid types."""

    def test_unclosed_quotes_and_syntax_error_in_frontmatter(self, tmp_path):
        vault = tmp_path / "vault"
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)
        
        corrupted_note = papers / "bad2024yaml.md"
        corrupted_note.write_text("""---
title: "Unclosed quote title
citekey: bad2024yaml
type: paper
---
# Corrupted Note
Body
""", encoding="utf-8")
        
        res = lint_vault(vault)
        assert not res.is_clean
        assert any(i.severity == "error" for i in res.issues)
        assert any("yaml" in i.message.lower() or "frontmatter" in i.message.lower() for i in res.issues)

    def test_missing_mandatory_keys_in_paper_note(self, tmp_path):
        vault = tmp_path / "vault"
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)
        
        note = papers / "incomplete2024.md"
        note.write_text("""---
type: paper
citekey: incomplete2024
title: "Incomplete Paper"
---
# Incomplete
""", encoding="utf-8")
        
        res = lint_vault(vault)
        assert not res.is_clean
        messages = [i.message for i in res.issues]
        assert any("authors" in m for m in messages)
        assert any("year" in m for m in messages)
        assert any("claim_strength" in m for m in messages)

    def test_invalid_types_and_enum_values(self, tmp_path):
        vault = tmp_path / "vault"
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)
        
        note = papers / "wrongtypes2024.md"
        note.write_text("""---
type: paper
citekey: wrongtypes2024
title: "Wrong Types"
authors: "Not a list"
year: "twenty twenty four"
claim_strength: "super-ultra-strong"
---
# Title
""", encoding="utf-8")
        
        res = lint_vault(vault)
        assert not res.is_clean
        messages = [i.message for i in res.issues]
        assert any("authors" in m or "list" in m for m in messages)
        assert any("year" in m or "integer" in m for m in messages)
        assert any("claim_strength" in m or "enum" in m or "Invalid" in m for m in messages)

    def test_filename_vs_citekey_mismatch(self, tmp_path):
        vault = tmp_path / "vault"
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)
        
        note = papers / "filecitekey.md"
        note.write_text("""---
type: paper
project: zotero_obsidian_kb
citekey: differentcitekey
zotero_key: "DIFF2024"
status: read
source_type: "conference paper"
title: "Mismatch"
authors: ["Author One"]
year: 2024
claim_strength: strong
linked_knowledge: ["[[Knowledge/Literature Overview]]"]
updated: "2026-08-19T00:00:00Z"
---
# Title
""", encoding="utf-8")
        
        res = lint_vault(vault)
        assert not res.is_clean
        messages = [i.message for i in res.issues]
        assert any("does not match file stem" in m or "match" in m.lower() for m in messages)

    def test_completely_empty_or_missing_frontmatter(self, tmp_path):
        vault = tmp_path / "vault"
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)
        
        note = papers / "nofrontmatter2024.md"
        note.write_text("# Raw Markdown Without Frontmatter\nJust text.\n", encoding="utf-8")
        
        res = lint_vault(vault)
        assert not res.is_clean
        assert any("frontmatter" in i.message.lower() for i in res.issues)


class TestBrokenWikilinksAndFuzzyAutoRepair:
    """Adversarial testing of link checking and fuzzy repair."""

    def test_detect_dead_wikilinks_and_orphans(self, tmp_path):
        vault = tmp_path / "vault"
        papers = vault / "Sources" / "Papers"
        concepts = vault / "Knowledge" / "Concepts"
        papers.mkdir(parents=True)
        concepts.mkdir(parents=True)

        (papers / "he2016deep.md").write_text("""---
type: paper
citekey: he2016deep
title: "ResNet"
authors: ["He"]
year: 2016
claim_strength: strong
---
Link to non-existent note: [[Sources/Papers/nonexistent_paper]]
Link to non-existent concept: [[Knowledge/Concepts/ghost_concept]]
""", encoding="utf-8")

        res = check_links(vault)
        assert not res.is_clean
        assert len(res.broken_links) >= 2
        targets = [b.target for b in res.broken_links]
        assert any("nonexistent_paper" in t for t in targets)
        assert any("ghost_concept" in t for t in targets)

    def test_fuzzy_link_repair_single_and_multiple_typos(self, tmp_path):
        vault = tmp_path / "vault"
        papers = vault / "Sources" / "Papers"
        concepts = vault / "Knowledge" / "Concepts"
        papers.mkdir(parents=True)
        concepts.mkdir(parents=True)

        (papers / "he2016deep.md").write_text("""---
type: paper
citekey: he2016deep
title: "ResNet"
authors: ["He"]
year: 2016
claim_strength: strong
---
# ResNet
""", encoding="utf-8")

        (concepts / "residual_connection.md").write_text("""---
type: concept
title: "Residual Connection"
claim_strength: strong
primary_sources: ["[[Sources/Papers/he2016deep]]"]
---
# Residual Connection
""", encoding="utf-8")

        test_note = vault / "Knowledge" / "Overview.md"
        test_note.parent.mkdir(parents=True, exist_ok=True)
        test_note.write_text("""---
type: literature-synthesis
title: "Overview"
covered_papers: ["[[Sources/Papers/he2016deep]]"]
---
We refer to [[he2016dep]] and concept [[residual_connections]].
""", encoding="utf-8")

        dry_res = repair_links(vault, threshold=0.7, dry_run=True)
        assert dry_res["repaired_count"] >= 1
        assert "[[he2016dep]]" in test_note.read_text(encoding="utf-8")

        live_res = repair_links(vault, threshold=0.7, dry_run=False)
        assert live_res["repaired_count"] >= 1
        repaired_text = test_note.read_text(encoding="utf-8")
        assert "[[he2016dep]]" not in repaired_text
        assert "he2016deep" in repaired_text

    def test_anchors_and_piped_aliases_handled_safely(self, tmp_path):
        vault = tmp_path / "vault"
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)

        (papers / "vaswani2017attention.md").write_text("""---
type: paper
citekey: vaswani2017attention
title: "Attention Is All You Need"
authors: ["Vaswani"]
year: 2017
claim_strength: strong
---
# Attention Is All You Need
## Architecture
Section details.
""", encoding="utf-8")

        linking_note = papers / "linking_note.md"
        linking_note.write_text("""---
type: paper
citekey: linking_note
title: "Linking Note"
authors: ["Author"]
year: 2024
claim_strength: strong
---
Check [[vaswani2017attention#Architecture|The Transformer Architecture]].
""", encoding="utf-8")

        res = check_links(vault)
        assert not any(b.source_file.endswith("linking_note.md") and "vaswani2017attention" in b.target for b in res.broken_links)

    def test_external_urls_and_zotero_uris_ignored(self, tmp_path):
        vault = tmp_path / "vault"
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)

        note = papers / "externallinks2024.md"
        note.write_text("""---
type: paper
citekey: externallinks2024
title: "External Links"
authors: ["Author"]
year: 2024
claim_strength: strong
url: "https://arxiv.org/abs/1706.03762"
---
See [ArXiv](https://arxiv.org/abs/1706.03762) and [Zotero](zotero://select/items/12345).
""", encoding="utf-8")

        res = check_links(vault)
        broken_for_note = [b for b in res.broken_links if b.source_file.endswith("externallinks2024.md")]
        assert len(broken_for_note) == 0

    def test_circular_wikilink_references_no_infinite_loop(self, tmp_path):
        vault = tmp_path / "vault"
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)

        (papers / "notea.md").write_text("""---
type: paper
citekey: notea
title: "Note A"
authors: ["A"]
year: 2024
claim_strength: strong
---
See [[Sources/Papers/noteb]]
""", encoding="utf-8")

        (papers / "noteb.md").write_text("""---
type: paper
citekey: noteb
title: "Note B"
authors: ["B"]
year: 2024
claim_strength: strong
---
See [[Sources/Papers/notec]]
""", encoding="utf-8")

        (papers / "notec.md").write_text("""---
type: paper
citekey: notec
title: "Note C"
authors: ["C"]
year: 2024
claim_strength: strong
---
See [[Sources/Papers/notea]]
""", encoding="utf-8")

        res = check_links(vault)
        assert res.is_clean
        assert res.total_links == 3
        assert res.resolved_links == 3


class TestCorruptedAndWeirdBibTeXCslJsonIngest:
    """Adversarial testing of ingest parser."""

    def test_ingest_malformed_bibtex_syntax(self, tmp_path):
        bad_bib = tmp_path / "corrupted.bib"
        bad_bib.write_text("""@article{broken2024,
  title = {Unclosed title
  author = {Smith, John}
""", encoding="utf-8")
        
        vault = tmp_path / "vault"
        vault.mkdir(parents=True)
        
        try:
            created = ingest_file(bad_bib, vault_dir=vault)
            assert isinstance(created, list)
        except Exception as e:
            assert "BibTeX" in str(e) or "parse" in str(e).lower() or "corrupted" in str(e).lower()

    def test_ingest_latex_accents_and_math_symbols(self, tmp_path):
        bib = tmp_path / "accents.bib"
        bib.write_text(r"""@article{schrodinger1926undulatory,
  title = {Quantisierung als {Eigenwertproblem} und {\"U}berlagerung von {$\alpha$}-Strahlen},
  author = {Schr{\"o}dinger, Erwin and Poincar{\'e}, Henri and M{\o}ller, Chr{\ae}stian},
  journal = {Annalen der Physik},
  year = {1926},
  volume = {79},
  pages = {361--376}
}""", encoding="utf-8")

        vault = tmp_path / "vault"
        (vault / "Sources" / "Papers").mkdir(parents=True)

        created = ingest_file(bib, vault_dir=vault)
        assert len(created) == 1
        note_path = created[0]
        assert note_path.exists()
        content = note_path.read_text(encoding="utf-8")
        assert "1926" in content

    def test_ingest_csl_json_edge_cases(self, tmp_path):
        csl = tmp_path / "papers.json"
        csl.write_text(json.dumps([
            {
                "id": "csl2024minimal",
                "type": "article-journal",
                "title": "Minimal CSL Entry",
                "author": [{"family": "Doe", "given": "Jane"}],
                "issued": {"date-parts": [[2024, 5, 1]]}
            },
            {
                "id": "csl2024noauthor",
                "title": "No Author Entry",
                "issued": {"date-parts": [[2024]]}
            }
        ]), encoding="utf-8")

        vault = tmp_path / "vault"
        (vault / "Sources" / "Papers").mkdir(parents=True)

        created = ingest_file(csl, vault_dir=vault)
        assert len(created) == 2
        for p in created:
            assert p.exists()

    def test_ingest_duplicate_citekey_handling(self, tmp_path):
        bib = tmp_path / "dup.bib"
        bib.write_text("""@article{dup2024,
  title = {Original Title},
  author = {Original Author},
  year = {2024}
}
""", encoding="utf-8")

        vault = tmp_path / "vault"
        (vault / "Sources" / "Papers").mkdir(parents=True)

        created1 = ingest_file(bib, vault_dir=vault)
        assert len(created1) == 1
        note_file = created1[0]
        note_file.write_text(note_file.read_text(encoding="utf-8") + "\nCustom User Notes Added Here.\n", encoding="utf-8")

        created2 = ingest_file(bib, vault_dir=vault, overwrite=False)
        assert "Custom User Notes Added Here." in note_file.read_text(encoding="utf-8")

        created3 = ingest_file(bib, vault_dir=vault, overwrite=True)
        assert "Custom User Notes Added Here." not in note_file.read_text(encoding="utf-8")


class TestBoundaryVaultTopologies:
    """Empty vault, single isolated note vault, disconnected topology."""

    def test_empty_vault_sync_registry(self, tmp_path):
        vault = tmp_path / "empty_vault"
        vault.mkdir(parents=True)

        res = sync_registry(vault)
        assert res["papers_count"] == 0
        assert res["knowledge_count"] == 0
        assert (vault / "02-Index.md").exists()
        assert (vault / "02-Index.md").exists()
        assert (vault / "_system" / "registry.md").exists()

    def test_empty_vault_generate_canvas(self, tmp_path):
        vault = tmp_path / "empty_vault"
        vault.mkdir(parents=True)

        canvas_path = generate_canvas_file(vault)
        assert canvas_path.exists()
        canvas_data = json.loads(canvas_path.read_text(encoding="utf-8"))
        assert "nodes" in canvas_data
        assert "edges" in canvas_data
        assert isinstance(canvas_data["nodes"], list)
        assert isinstance(canvas_data["edges"], list)

    def test_empty_vault_synthesize(self, tmp_path):
        vault = tmp_path / "empty_vault"
        vault.mkdir(parents=True)

        files = run_synthesis(vault)
        assert isinstance(files, list)
        assert (vault / "Knowledge" / "Literature Overview.md").exists()

    def test_single_isolated_note_canvas(self, tmp_path):
        vault = tmp_path / "single_note_vault"
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)

        (papers / "single2024.md").write_text("""---
type: paper
citekey: single2024
title: "Single Paper"
authors: ["Lone Author"]
year: 2024
claim_strength: strong
---
# Single Paper
No links.
""", encoding="utf-8")

        graph = build_canvas_graph(vault)
        assert len(graph["nodes"]) >= 1
        file_nodes = [n for n in graph["nodes"] if n.get("type") == "file"]
        assert len(file_nodes) == 1
        assert file_nodes[0]["file"] == "Sources/Papers/single2024.md"

    def test_hidden_canvas_visibility_omits_node(self, tmp_path):
        vault = tmp_path / "hidden_vault"
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)

        (papers / "hidden2024.md").write_text("""---
type: paper
citekey: hidden2024
title: "Hidden Paper"
authors: ["Author"]
year: 2024
claim_strength: strong
canvas_visibility: hidden
---
# Hidden Paper
""", encoding="utf-8")

        graph = build_canvas_graph(vault)
        file_nodes = [n for n in graph["nodes"] if n.get("type") == "file"]
        assert len(file_nodes) == 0


class TestCliJsonOutputAndExitCodes:
    """Verify CLI --json outputs and return codes across all subcommands."""

    def test_cli_lint_clean_and_corrupted_json_output(self, tmp_path, capsys):
        vault = tmp_path / "vault"
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)

        (papers / "valid2024.md").write_text(make_valid_paper_note("valid2024", "Valid Paper"), encoding="utf-8")

        code = main(["lint", "--vault-dir", str(vault), "--json"])
        out, _ = capsys.readouterr()
        assert code == 0
        parsed = json.loads(out)
        assert parsed["is_clean"] is True
        assert parsed["error_count"] == 0

        (papers / "corrupt.md").write_text("--- invalid yaml ---", encoding="utf-8")
        code_corrupt = main(["lint", "--vault-dir", str(vault), "--json"])
        out_corrupt, _ = capsys.readouterr()
        assert code_corrupt != 0
        parsed_corrupt = json.loads(out_corrupt)
        assert parsed_corrupt["is_clean"] is False
        assert parsed_corrupt["error_count"] > 0

    def test_cli_all_subcommands_json_flag(self, tmp_path, capsys):
        vault = tmp_path / "vault"
        papers = vault / "Sources" / "Papers"
        papers.mkdir(parents=True)

        (papers / "valid2024.md").write_text(make_valid_paper_note("valid2024", "Sample Paper"), encoding="utf-8")

        code = main(["sync-registry", "--vault-dir", str(vault), "--json"])
        out, _ = capsys.readouterr()
        assert code == 0
        assert isinstance(json.loads(out), dict)

        code = main(["check-links", "--vault-dir", str(vault), "--json"])
        out, _ = capsys.readouterr()
        assert code == 0
        assert isinstance(json.loads(out), dict)

        code = main(["repair-links", "--vault-dir", str(vault), "--json"])
        out, _ = capsys.readouterr()
        assert code == 0
        assert isinstance(json.loads(out), dict)

        code = main(["synthesize", "--vault-dir", str(vault), "--json"])
        out, _ = capsys.readouterr()
        assert code == 0
        assert isinstance(json.loads(out), dict)

        code = main(["generate-canvas", "--vault-dir", str(vault), "--json"])
        out, _ = capsys.readouterr()
        assert code == 0
        assert isinstance(json.loads(out), dict)

    def test_cli_invalid_vault_dir_returns_nonzero(self, capsys):
        nonexistent = Path("non_existent_vault_dir_xyz_123")
        code = main(["sync-registry", "--vault-dir", str(nonexistent)])
        assert code == 1


class TestJsonCanvasStrictSchemaValidation:
    """Validate Maps/literature.canvas strictly against JSON Canvas v1.0 specification."""

    def test_literature_canvas_conforms_to_json_canvas_v1_0(self):
        canvas_path = Path("Maps/literature.canvas").resolve()
        assert canvas_path.exists(), "Maps/literature.canvas must exist"

        data = json.loads(canvas_path.read_text(encoding="utf-8"))
        assert isinstance(data, dict), "Root must be an object"
        assert "nodes" in data, "Canvas must have 'nodes' key"
        assert "edges" in data, "Canvas must have 'edges' key"
        assert isinstance(data["nodes"], list)
        assert isinstance(data["edges"], list)

        node_ids = set()
        for node in data["nodes"]:
            assert "id" in node and isinstance(node["id"], str) and len(node["id"]) > 0
            assert node["id"] not in node_ids, f"Duplicate node ID: {node['id']}"
            node_ids.add(node["id"])

            assert "type" in node
            assert node["type"] in ("text", "file", "link", "group"), f"Invalid node type: {node['type']}"

            for coord in ("x", "y", "width", "height"):
                assert coord in node, f"Node {node['id']} missing coordinate {coord}"
                assert isinstance(node[coord], (int, float)), f"Node {node['id']} {coord} must be numeric"
            assert node["width"] > 0, f"Node {node['id']} width must be > 0"
            assert node["height"] > 0, f"Node {node['id']} height must be > 0"

            if node["type"] == "file":
                assert "file" in node and isinstance(node["file"], str)
                file_target = Path(node["file"])
                assert file_target.exists(), f"Canvas file node target does not exist: {node['file']}"
            elif node["type"] == "text":
                assert "text" in node and isinstance(node["text"], str)
            elif node["type"] == "group":
                if "label" in node:
                    assert isinstance(node["label"], str)

            if "color" in node:
                color_val = str(node["color"])
                assert color_val in ("1", "2", "3", "4", "5", "6") or color_val.startswith("#")

        for edge in data["edges"]:
            assert "id" in edge and isinstance(edge["id"], str)
            assert "fromNode" in edge and isinstance(edge["fromNode"], str)
            assert "toNode" in edge and isinstance(edge["toNode"], str)
            assert edge["fromNode"] in node_ids, f"Edge fromNode does not exist: {edge['fromNode']}"
            assert edge["toNode"] in node_ids, f"Edge toNode does not exist: {edge['toNode']}"

            if "fromSide" in edge:
                assert edge["fromSide"] in ("top", "right", "bottom", "left")
            if "toSide" in edge:
                assert edge["toSide"] in ("top", "right", "bottom", "left")
            if "color" in edge:
                color_val = str(edge["color"])
                assert color_val in ("1", "2", "3", "4", "5", "6") or color_val.startswith("#")


class TestLiveVaultIntegrity:
    """Run live validation commands directly against the real vault."""

    def test_live_vault_zero_lint_errors(self):
        vault_path = Path(".").resolve()
        res = lint_vault(vault_path)
        assert res.is_clean, f"Live vault has lint errors: {[i.message for i in res.issues if i.severity == 'error']}"
        assert res.error_count == 0

    def test_live_vault_zero_broken_links(self):
        vault_path = Path(".").resolve()
        res = check_links(vault_path)
        assert res.is_clean, f"Live vault has broken links: {[(b.source_file, b.target) for b in res.broken_links]}"
        assert len(res.broken_links) == 0

    def test_live_vault_sync_registry_idempotent(self):
        vault_path = Path(".").resolve()
        res = sync_registry(vault_path, dry_run=False)
        assert res["papers_count"] >= 0
        assert res["knowledge_count"] >= 0
        res2 = sync_registry(vault_path, dry_run=False)
        assert res2["papers_count"] == res["papers_count"]
        assert res2["knowledge_count"] == res["knowledge_count"]
