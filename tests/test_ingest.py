"""
Test Suite for kb_tools.ingest and CLI 'ingest' subcommand.
Covers Tier 1 (Unit & Schema Contracts) and Tier 2 (CLI & Functional Boundaries).
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


SAMPLE_BIBTEX_RESNET = """@inproceedings{he2016deep,
  title={Deep Residual Learning for Image Recognition},
  author={He, Kaiming and Zhang, Xiangyu and Ren, Shaoqing and Sun, Jian},
  booktitle={Proceedings of the IEEE conference on computer vision and pattern recognition (CVPR)},
  pages={770--778},
  year={2016},
  doi={10.1109/CVPR.2016.90},
  url={https://arxiv.org/abs/1512.03385}
}"""

SAMPLE_BIBTEX_TRANSFORMER = """@inproceedings{vaswani2017attention,
  title={Attention Is All You Need},
  author={Vaswani, Ashish and Shazeer, Noam and Parmar, Niki and Uszkoreit, Jakob and Jones, Llion and Gomez, Aidan N and Kaiser, {\\L}ukasz and Polosukhin, Illia},
  booktitle={Advances in Neural Information Processing Systems (NeurIPS)},
  volume={30},
  year={2017},
  eprint={1706.03762},
  archivePrefix={arXiv}
}"""

SAMPLE_BIBTEX_UNICODE = """@article{schmidt2020uber,
  title={{\\"U}ber die \\textbf{Stabilit{\\"a}t} von {RNN}s \\& {Transformers}},
  author={Schmidt, J{\\"o}rg and M{\\"u}ller, Fran{\\c{c}}ois and Nov{\\'a}k, Petr and {\v{S}}im{\\l}ek, Jan},
  journal={Journal of Machine Learning},
  year={2020},
  doi={10.1000/182}
}"""

SAMPLE_CSL_JSON = [
    {
        "id": "hu2021lora",
        "type": "paper-conference",
        "title": "LoRA: Low-Rank Adaptation of Large Language Models",
        "author": [
            {"family": "Hu", "given": "Edward J."},
            {"family": "Shen", "given": "Yelong"},
            {"family": "Wallis", "given": "Phillip"},
            {"family": "Chen", "given": "Weizhu"}
        ],
        "issued": {"date-parts": [[2021]]},
        "container-title": "International Conference on Learning Representations (ICLR)",
        "DOI": "arXiv:2106.09685",
        "URL": "https://arxiv.org/abs/2106.09685"
    }
]


@pytest.fixture
def ingest_vault(tmp_path):
    """Create an empty mock vault ready for ingestion testing."""
    vault = tmp_path / "ingest_vault"
    (vault / "Sources" / "Papers").mkdir(parents=True, exist_ok=True)
    (vault / "Knowledge").mkdir(parents=True, exist_ok=True)
    (vault / "Writing").mkdir(parents=True, exist_ok=True)
    (vault / "Maps").mkdir(parents=True, exist_ok=True)
    (vault / "Templates").mkdir(parents=True, exist_ok=True)
    (vault / "_system" / "schemas").mkdir(parents=True, exist_ok=True)
    return vault


# ==============================================================================
# Tier 1: Unit & Parser Tests
# ==============================================================================

def test_parse_bibtex_entry():
    """Test parsing a raw BibTeX string into a structured dictionary."""
    from kb_tools.ingest import parse_bibtex

    entries = parse_bibtex(SAMPLE_BIBTEX_RESNET)
    assert len(entries) == 1

    entry = entries[0]
    assert entry["citekey"] == "he2016deep"
    assert entry["title"] == "Deep Residual Learning for Image Recognition"
    assert len(entry["authors"]) == 4
    assert entry["authors"][0] in ("Kaiming He", "He, Kaiming")
    assert int(entry["year"]) == 2016
    assert entry["doi"] == "10.1109/CVPR.2016.90"


def test_parse_csl_json():
    """Test parsing CSL-JSON format entries."""
    from kb_tools.ingest import parse_csl_json

    entries = parse_csl_json(SAMPLE_CSL_JSON)
    assert len(entries) == 1

    entry = entries[0]
    assert entry["citekey"] == "hu2021lora"
    assert entry["title"] == "LoRA: Low-Rank Adaptation of Large Language Models"
    assert int(entry["year"]) == 2021
    assert any("Hu" in a for a in entry["authors"])


def test_clean_latex_unicode_and_formatting():
    """Test cleaning LaTeX commands, accents, and escaped characters."""
    from kb_tools.ingest import clean_latex_string

    raw_title = "{\\\"U}ber die \\textbf{Stabilit{\\\"a}t} von {RNN}s \\& {Transformers}"
    cleaned_title = clean_latex_string(raw_title)

    assert "Über" in cleaned_title or "Uber" in cleaned_title or "über" in cleaned_title.lower()
    assert "Stabilität" in cleaned_title or "Stabilitat" in cleaned_title or "stabilit" in cleaned_title.lower()
    assert "\\textbf" not in cleaned_title
    assert "&" in cleaned_title
    assert "{" not in cleaned_title
    assert "}" not in cleaned_title


def test_sanitize_citekey():
    """Test citekey sanitization adheres to [auth:lower][year][veryshorttitle:lower]."""
    from kb_tools.ingest import sanitize_citekey

    assert sanitize_citekey("He_2016_Deep") == "he2016deep"
    assert sanitize_citekey("Vaswani-2017-Attention-Is-All") == "vaswani2017attention"
    assert sanitize_citekey("Hu2021LoRA!") == "hu2021lora"


def test_render_paper_note_markdown():
    """Test generating compliant Markdown note content from parsed entry data."""
    from kb_tools.ingest import render_paper_note

    entry = {
        "citekey": "he2016deep",
        "title": "Deep Residual Learning for Image Recognition",
        "authors": ["Kaiming He", "Xiangyu Zhang", "Shaoqing Ren", "Jian Sun"],
        "year": 2016,
        "venue": "CVPR 2016",
        "doi": "10.1109/CVPR.2016.90",
        "url": "https://arxiv.org/abs/1512.03385",
        "item_type": "conferencePaper",
    }

    markdown = render_paper_note(entry)

    # Required Frontmatter
    assert "type: paper" in markdown
    assert "citekey: he2016deep" in markdown
    assert "title: \"Deep Residual Learning for Image Recognition\"" in markdown or "title: Deep Residual" in markdown
    assert "year: 2016" in markdown
    assert "status: unread" in markdown or "status: to-read" in markdown
    assert "claim_strength: observed" in markdown or "claim_strength: strong" in markdown

    # Required Headings
    assert "## Claim" in markdown
    assert "## Research question" in markdown
    assert "## Method" in markdown
    assert "## Evidence" in markdown
    assert "## Strengths" in markdown
    assert "## Limitation" in markdown
    assert "## Direct relevance to repo" in markdown
    assert "## Relation to other papers" in markdown
    assert "## Knowledge links" in markdown

    # Evidence Record Contract
    assert "Evidence ID: EVD-he2016deep-01" in markdown
    assert "Source: [[Sources/Papers/he2016deep]]" in markdown


# ==============================================================================
# Tier 2: Functional Ingestion & CLI Tests
# ==============================================================================

def test_ingest_single_bibtex_file(ingest_vault, tmp_path):
    """Test ingesting a single BibTeX file creating Sources/Papers/<citekey>.md."""
    from kb_tools.ingest import ingest_file

    bib_file = tmp_path / "resnet.bib"
    bib_file.write_text(SAMPLE_BIBTEX_RESNET, encoding="utf-8")

    created = ingest_file(bib_file, vault_dir=ingest_vault)

    expected_note = ingest_vault / "Sources" / "Papers" / "he2016deep.md"
    assert expected_note.exists()

    content = expected_note.read_text(encoding="utf-8")
    assert "citekey: he2016deep" in content
    assert "EVD-he2016deep-01" in content


def test_ingest_csl_json_file(ingest_vault, tmp_path):
    """Test ingesting a CSL-JSON file creating Sources/Papers/<citekey>.md."""
    from kb_tools.ingest import ingest_file

    csl_file = tmp_path / "lora.json"
    csl_file.write_text(json.dumps(SAMPLE_CSL_JSON), encoding="utf-8")

    created = ingest_file(csl_file, vault_dir=ingest_vault)

    expected_note = ingest_vault / "Sources" / "Papers" / "hu2021lora.md"
    assert expected_note.exists()

    content = expected_note.read_text(encoding="utf-8")
    assert "citekey: hu2021lora" in content


def test_ingest_batch_bibtex_file(ingest_vault, tmp_path):
    """Test ingesting a multi-entry BibTeX file."""
    from kb_tools.ingest import ingest_file

    batch_bib = tmp_path / "batch.bib"
    batch_bib.write_text(SAMPLE_BIBTEX_RESNET + "\n\n" + SAMPLE_BIBTEX_TRANSFORMER, encoding="utf-8")

    created = ingest_file(batch_bib, vault_dir=ingest_vault)

    assert len(created) == 2
    assert (ingest_vault / "Sources" / "Papers" / "he2016deep.md").exists()
    assert (ingest_vault / "Sources" / "Papers" / "vaswani2017attention.md").exists()


def test_ingest_duplicate_without_overwrite_preserves_content(ingest_vault, tmp_path):
    """Test ingesting an existing note without overwrite flag preserves existing notes."""
    from kb_tools.ingest import ingest_file

    paper_note = ingest_vault / "Sources" / "Papers" / "he2016deep.md"
    paper_note.write_text("# Custom Existing Content That Must Be Kept\n", encoding="utf-8")

    bib_file = tmp_path / "resnet.bib"
    bib_file.write_text(SAMPLE_BIBTEX_RESNET, encoding="utf-8")

    ingest_file(bib_file, vault_dir=ingest_vault, overwrite=False)

    # Verify content was preserved
    assert paper_note.read_text(encoding="utf-8") == "# Custom Existing Content That Must Be Kept\n"


def test_ingest_duplicate_with_overwrite_replaces_content(ingest_vault, tmp_path):
    """Test ingesting an existing note with overwrite flag replaces existing note."""
    from kb_tools.ingest import ingest_file

    paper_note = ingest_vault / "Sources" / "Papers" / "he2016deep.md"
    paper_note.write_text("# Custom Old Content\n", encoding="utf-8")

    bib_file = tmp_path / "resnet.bib"
    bib_file.write_text(SAMPLE_BIBTEX_RESNET, encoding="utf-8")

    ingest_file(bib_file, vault_dir=ingest_vault, overwrite=True)

    # Verify content was replaced
    content = paper_note.read_text(encoding="utf-8")
    assert "Deep Residual Learning for Image Recognition" in content
    assert "# Custom Old Content" not in content


def test_ingest_cli_invocation(ingest_vault, tmp_path, capsys):
    """Test CLI subcommand 'ingest'."""
    from kb_tools.cli import main

    bib_file = tmp_path / "papers.bib"
    bib_file.write_text(SAMPLE_BIBTEX_TRANSFORMER, encoding="utf-8")

    exit_code = main(["ingest", "--input", str(bib_file), "--vault-dir", str(ingest_vault)])
    assert exit_code == 0

    assert (ingest_vault / "Sources" / "Papers" / "vaswani2017attention.md").exists()


def test_ingest_cli_dry_run(ingest_vault, tmp_path):
    """Test CLI ingest with --dry-run flag does not write files."""
    from kb_tools.cli import main

    bib_file = tmp_path / "papers.bib"
    bib_file.write_text(SAMPLE_BIBTEX_TRANSFORMER, encoding="utf-8")

    note_path = ingest_vault / "Sources" / "Papers" / "vaswani2017attention.md"
    if note_path.exists():
        note_path.unlink()

    exit_code = main(["ingest", "--input", str(bib_file), "--vault-dir", str(ingest_vault), "--dry-run"])
    assert exit_code == 0
    assert not note_path.exists()


def test_ingest_cli_json_output(ingest_vault, tmp_path, capsys):
    """Test CLI ingest with --json output flag."""
    from kb_tools.cli import main

    bib_file = tmp_path / "papers.bib"
    bib_file.write_text(SAMPLE_BIBTEX_TRANSFORMER, encoding="utf-8")

    exit_code = main(["ingest", "--input", str(bib_file), "--vault-dir", str(ingest_vault), "--json"])
    assert exit_code == 0

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "ingested" in data or "papers" in data or isinstance(data, list)


def test_ingest_invalid_file_handling(ingest_vault, tmp_path):
    """Test ingesting a malformed or non-existent file handles errors cleanly."""
    from kb_tools.cli import main

    non_existent = tmp_path / "non_existent.bib"
    exit_code = main(["ingest", "--input", str(non_existent), "--vault-dir", str(ingest_vault)])
    assert exit_code != 0
