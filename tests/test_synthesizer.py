"""
Test Suite for kb_tools.synthesizer and CLI 'synthesize' subcommand.
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


@pytest.fixture
def sample_vault(tmp_path):
    """Create a minimal mock vault with canonical directory structure and sample papers."""
    vault = tmp_path / "mock_vault"
    papers_dir = vault / "Sources" / "Papers"
    knowledge_dir = vault / "Knowledge" / "Concepts"
    writing_dir = vault / "Writing"
    maps_dir = vault / "Maps"
    system_dir = vault / "_system" / "schemas"

    for d in [papers_dir, knowledge_dir, writing_dir, maps_dir, system_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Paper 1: ResNet
    resnet_content = """---
type: paper
project: zotero_obsidian_kb
title: "Deep Residual Learning for Image Recognition"
citekey: he2016deep
zotero_key: "HE2016KEY"
status: summarized
source_type: "conference paper"
claim_strength: strong
authors:
  - "Kaiming He"
  - "Xiangyu Zhang"
  - "Shaoqing Ren"
  - "Jian Sun"
year: 2016
venue: "CVPR 2016"
doi: "10.1109/CVPR.2016.90"
url: "https://arxiv.org/abs/1512.03385"
keywords:
  - residual-learning
  - computer-vision
concepts:
  - "Residual Connections"
  - "Identity Mapping"
methods:
  - "Skip Connection"
subfield: computer-vision
related_papers: []
linked_knowledge:
  - "Knowledge/Literature Overview"
  - "Knowledge/Method Taxonomy"
updated: 2026-08-19T00:00:00Z
---

# Deep Residual Learning for Image Recognition

## Claim
Residual learning framework eases training of networks substantially deeper than previously possible by learning residual functions F(x) = H(x) - x.

## Research question
How to train substantially deeper neural networks without suffering from degradation and vanishing gradient problems?

## Method
Reformulate stacked layers as learning residual functions with reference to layer inputs via shortcut identity mappings.

## Evidence
```md
Evidence ID: EVD-he2016deep-01
Source: [[Sources/Papers/he2016deep]]
Source type: conference paper
Supports: "152-layer ResNet achieves 3.57% top-5 error on ImageNet, winning ILSVRC 2015"
Contradicts: "Prior assumption that deeper networks inherently suffer higher training error"
Method / dataset / metric: "ImageNet classification / Top-5 error 3.57%"
Limitation: "Residual paths require identical feature map dimensions unless projection shortcuts are used"
Project relevance: "Foundational skip connection formulation adopted across modern deep learning"
Claim strength: strong
```

## Strengths
- Enables training networks of 100+ layers without degradation.
- Zero extra parameter cost for identity shortcut connections.

## Limitation
- Increases feature map memory retention during backprop.

## Direct relevance to repo
Core architectural baseline for deep architectures.

## Relation to other papers
- Precedes [[Sources/Papers/vaswani2017attention]]

## Knowledge links
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
- [[Knowledge/Concepts/Residual Connections]]
"""
    (papers_dir / "he2016deep.md").write_text(resnet_content, encoding="utf-8")

    # Paper 2: Transformer
    transformer_content = """---
type: paper
project: zotero_obsidian_kb
title: "Attention Is All You Need"
citekey: vaswani2017attention
zotero_key: "VASWANI2017KEY"
status: summarized
source_type: "conference paper"
claim_strength: strong
authors:
  - "Ashish Vaswani"
  - "Noam Shazeer"
  - "Niki Parmar"
  - "Jakob Uszkoreit"
  - "Llion Jones"
  - "Aidan N. Gomez"
  - "Lukasz Kaiser"
  - "Illia Polosukhin"
year: 2017
venue: "NeurIPS 2017"
doi: "arXiv:1706.03762"
url: "https://arxiv.org/abs/1706.03762"
keywords:
  - transformer
  - self-attention
  - nlp
concepts:
  - "Self-Attention"
  - "Multi-Head Attention"
  - "Residual Connections"
methods:
  - "Scaled Dot-Product Attention"
  - "Multi-Head Attention"
subfield: nlp
related_papers:
  - "Sources/Papers/he2016deep"
linked_knowledge:
  - "Knowledge/Literature Overview"
  - "Knowledge/Method Taxonomy"
  - "Knowledge/Research Gaps"
updated: 2026-08-19T00:00:00Z
---

# Attention Is All You Need

## Claim
Self-attention mechanism alone, without recurrence or convolutions, achieves state-of-the-art translation quality with superior parallelizability.

## Research question
Can sequence transduction models be built entirely on attention mechanisms without sequential recurrence?

## Method
Encoder-decoder architecture based solely on multi-head self-attention and point-wise feed-forward networks, incorporating residual connections and layer normalization.

## Evidence
```md
Evidence ID: EVD-vaswani2017attention-01
Source: [[Sources/Papers/vaswani2017attention]]
Source type: conference paper
Supports: "Transformer achieves 28.4 BLEU on WMT 2014 En-De and 41.8 BLEU on WMT 2014 En-Fr"
Contradicts: "Dominant paradigm that recurrent or convolutional layers are necessary for sequence modeling"
Method / dataset / metric: "WMT 2014 English-to-German translation / BLEU 28.4"
Limitation: "Quadratic computational and memory complexity O(N^2) with sequence length N"
Project relevance: "Foundational architecture for all modern large language models"
Claim strength: strong
```

## Strengths
- Highly parallelizable training compared to RNNs.
- Constant path length O(1) for long-range dependency modeling.

## Limitation
- O(N^2) attention matrix memory footprint.

## Direct relevance to repo
Primary sequence modeling backbone.

## Relation to other papers
- Extends [[Sources/Papers/he2016deep]]
- Precedes [[Sources/Papers/hu2021lora]]

## Knowledge links
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
- [[Knowledge/Research Gaps]]
- [[Knowledge/Concepts/Self-Attention]]
"""
    (papers_dir / "vaswani2017attention.md").write_text(transformer_content, encoding="utf-8")

    # Paper 3: LoRA
    lora_content = """---
type: paper
project: zotero_obsidian_kb
title: "LoRA: Low-Rank Adaptation of Large Language Models"
citekey: hu2021lora
zotero_key: "HU2021KEY"
status: summarized
source_type: "conference paper"
claim_strength: strong
authors:
  - "Edward J. Hu"
  - "Yelong Shen"
  - "Phillip Wallis"
  - "Zeyuan Allen-Zhu"
  - "Yuanzhi Li"
  - "Shean Wang"
  - "Lu Wang"
  - "Weizhu Chen"
year: 2021
venue: "ICLR 2022"
doi: "arXiv:2106.09685"
url: "https://arxiv.org/abs/2106.09685"
keywords:
  - peft
  - lora
  - transformer
concepts:
  - "Low-Rank Adaptation"
  - "Parameter-Efficient Fine-Tuning"
methods:
  - "Low-Rank Decomposition"
subfield: nlp
related_papers:
  - "Sources/Papers/vaswani2017attention"
linked_knowledge:
  - "Knowledge/Literature Overview"
  - "Knowledge/Method Taxonomy"
  - "Knowledge/Research Gaps"
updated: 2026-08-19T00:00:00Z
---

# LoRA: Low-Rank Adaptation of Large Language Models

## Claim
Weight updates during downstream adaptation have low intrinsic rank, allowing freezing of pre-trained weights and injection of trainable rank decomposition matrices.

## Research question
How can massive pre-trained language models be adapted to specific tasks without full parameter fine-tuning?

## Method
Decompose weight update matrix Delta W into low-rank product B * A, freezing original weight W_0 and training only low-rank matrices.

## Evidence
```md
Evidence ID: EVD-hu2021lora-01
Source: [[Sources/Papers/hu2021lora]]
Source type: conference paper
Supports: "Reduces trainable parameters by 10,000x and GPU memory by 3x on GPT-3 175B while matching full fine-tuning"
Contradicts: "Belief that adapting all model weights is required to preserve full downstream capacity"
Method / dataset / metric: "GPT-3 175B adaptation on GLUE and SuperGLUE / Accuracy and Parameter Ratio"
Limitation: "Inference batching with multiple distinct task adapters requires adapter swapping or merged weights"
Project relevance: "Standard parameter-efficient fine-tuning method for all LLM adaptation"
Claim strength: strong
```

## Strengths
- 10,000x reduction in trainable parameters with zero inference latency overhead when weights are merged.
- Enables efficient task switching with small adapter checkpoints.

## Limitation
- Fixed rank r may constrain expressive capacity on complex domain shifts.

## Direct relevance to repo
Essential technique for efficient model tuning.

## Relation to other papers
- Extends [[Sources/Papers/vaswani2017attention]]

## Knowledge links
- [[Knowledge/Literature Overview]]
- [[Knowledge/Method Taxonomy]]
- [[Knowledge/Research Gaps]]
- [[Knowledge/Concepts/Low-Rank Adaptation]]
"""
    (papers_dir / "hu2021lora.md").write_text(lora_content, encoding="utf-8")

    return vault


# ==============================================================================
# Tier 1: Unit & Extraction Tests
# ==============================================================================

def test_extract_evidence_blocks_from_paper_note(sample_vault):
    """Test extracting structured Evidence Record blocks from a paper note."""
    from kb_tools.synthesizer import extract_evidence_records

    resnet_path = sample_vault / "Sources" / "Papers" / "he2016deep.md"
    records = extract_evidence_records(resnet_path)

    assert len(records) >= 1
    rec = records[0]
    assert rec["evidence_id"] == "EVD-he2016deep-01"
    assert "he2016deep" in rec["source"]
    assert "3.57%" in rec["supports"] or "ImageNet" in rec["supports"]
    assert rec["claim_strength"] == "strong"
    assert "Residual paths" in rec["limitation"] or "memory" in rec.get("limitation", "")


def test_extract_claims_from_multiple_papers(sample_vault):
    """Test extracting all claims across all paper notes in Sources/Papers/."""
    from kb_tools.synthesizer import extract_all_claims

    claims_by_paper = extract_all_claims(sample_vault)
    assert "he2016deep" in claims_by_paper
    assert "vaswani2017attention" in claims_by_paper
    assert "hu2021lora" in claims_by_paper

    for citekey, claims in claims_by_paper.items():
        assert len(claims) > 0
        assert "claim" in claims[0]
        assert "evidence_id" in claims[0]


def test_cluster_claims_by_topic_and_concept(sample_vault):
    """Test clustering extracted claims by concepts and keywords."""
    from kb_tools.synthesizer import cluster_claims

    clusters = cluster_claims(sample_vault)
    assert isinstance(clusters, dict)
    cluster_keys = [k.lower() for k in clusters.keys()]
    assert any("residual" in k or "attention" in k or "peft" in k or "nlp" in k or "vision" in k for k in cluster_keys)


def test_group_claims_by_strength(sample_vault):
    """Test grouping claims by their epistemic confidence rating."""
    from kb_tools.synthesizer import group_claims_by_strength

    grouped = group_claims_by_strength(sample_vault)
    assert isinstance(grouped, dict)
    assert "strong" in grouped
    strong_claims = grouped["strong"]
    assert len(strong_claims) >= 3  # All 3 sample papers have strong claims


def test_generate_comparison_matrix_data(sample_vault):
    """Test generating structured comparison matrix data across multiple papers."""
    from kb_tools.synthesizer import build_comparison_matrix

    matrix = build_comparison_matrix(sample_vault)
    assert len(matrix) == 3

    citekeys = [row["citekey"] for row in matrix]
    assert "he2016deep" in citekeys
    assert "vaswani2017attention" in citekeys
    assert "hu2021lora" in citekeys

    for row in matrix:
        assert "title" in row
        assert "year" in row
        assert "authors" in row
        assert "method" in row
        assert "limitation" in row


# ==============================================================================
# Tier 2: Functional Synthesis & CLI Tests
# ==============================================================================

def test_generate_literature_overview_note(sample_vault):
    """Test generating Knowledge/Literature Overview.md with all required sections."""
    from kb_tools.synthesizer import synthesize_literature_overview

    overview_content = synthesize_literature_overview(sample_vault)

    # Verify frontmatter
    assert "type: literature-synthesis" in overview_content
    assert "covered_papers:" in overview_content
    assert "he2016deep" in overview_content

    # Verify required sections
    assert "## Executive Synthesis" in overview_content
    assert "## Chronological Milestones" in overview_content
    assert "## Key Paradigms" in overview_content
    assert "## Evidence & Benchmark Matrix" in overview_content
    assert "## Cross-Paper Links" in overview_content

    # Verify wikilinks
    assert "[[Sources/Papers/he2016deep" in overview_content
    assert "[[Sources/Papers/vaswani2017attention" in overview_content
    assert "[[Sources/Papers/hu2021lora" in overview_content


def test_generate_method_taxonomy_note(sample_vault):
    """Test generating Knowledge/Method Taxonomy.md with taxonomy tree and matrix."""
    from kb_tools.synthesizer import synthesize_method_taxonomy

    taxonomy_content = synthesize_method_taxonomy(sample_vault)

    assert "type: method-taxonomy" in taxonomy_content
    assert "## Taxonomy Tree" in taxonomy_content
    assert "## Comparative Method Matrix" in taxonomy_content
    assert "## Evolutionary Lineage" in taxonomy_content


def test_generate_research_gaps_note(sample_vault):
    """Test generating Knowledge/Research Gaps.md with gap catalog and evidence anchors."""
    from kb_tools.synthesizer import synthesize_research_gaps

    gaps_content = synthesize_research_gaps(sample_vault)

    assert "type: research-gaps" in gaps_content
    assert "## Gap Catalog" in gaps_content
    assert "## Unresolved Theoretical Questions" in gaps_content
    assert "## Priority Matrix for Future Investigation" in gaps_content
    assert "EVD-" in gaps_content or "he2016deep" in gaps_content


def test_generate_writing_comparison_matrix(sample_vault):
    """Test generating Writing/comparison-matrix.md formatted table."""
    from kb_tools.synthesizer import synthesize_comparison_matrix_doc

    matrix_content = synthesize_comparison_matrix_doc(sample_vault)

    assert "# Literature Comparison Matrix" in matrix_content
    assert "| Paper |" in matrix_content
    assert "he2016deep" in matrix_content
    assert "vaswani2017attention" in matrix_content
    assert "hu2021lora" in matrix_content


def test_synthesize_all_writes_expected_files(sample_vault):
    """Test full synthesis pipeline writes all 4 synthesis notes to disk."""
    from kb_tools.synthesizer import run_synthesis

    created_files = run_synthesis(sample_vault)

    expected_files = [
        sample_vault / "Knowledge" / "Literature Overview.md",
        sample_vault / "Knowledge" / "Method Taxonomy.md",
        sample_vault / "Knowledge" / "Research Gaps.md",
        sample_vault / "Writing" / "comparison-matrix.md",
    ]

    for expected in expected_files:
        assert expected.exists(), f"Expected synthesis file not created: {expected}"
        content = expected.read_text(encoding="utf-8")
        assert len(content.strip()) > 50, f"Synthesis file is empty: {expected}"


def test_synthesize_cli_invocation(sample_vault, capsys):
    """Test running CLI subcommand 'synthesize'."""
    from kb_tools.cli import main

    exit_code = main(["synthesize", "--vault-dir", str(sample_vault)])
    assert exit_code == 0

    captured = capsys.readouterr()
    assert "Literature Overview" in captured.out or "Synthesized" in captured.out or "success" in captured.out.lower()


def test_synthesize_cli_dry_run(sample_vault):
    """Test running synthesis with --dry-run does not write to disk."""
    from kb_tools.cli import main

    lit_overview = sample_vault / "Knowledge" / "Literature Overview.md"
    if lit_overview.exists():
        lit_overview.unlink()

    exit_code = main(["synthesize", "--vault-dir", str(sample_vault), "--dry-run"])
    assert exit_code == 0
    assert not lit_overview.exists()


def test_synthesize_cli_json_output(sample_vault, capsys):
    """Test running synthesis with --json outputs valid JSON summary."""
    from kb_tools.cli import main

    exit_code = main(["synthesize", "--vault-dir", str(sample_vault), "--json"])
    assert exit_code == 0

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "papers_analyzed" in data or "synthesized_files" in data or "matrix" in data


def test_synthesize_idempotency(sample_vault):
    """Test that running synthesis twice produces identical file contents."""
    from kb_tools.synthesizer import run_synthesis

    run_synthesis(sample_vault)
    files = [
        sample_vault / "Knowledge" / "Literature Overview.md",
        sample_vault / "Knowledge" / "Method Taxonomy.md",
        sample_vault / "Knowledge" / "Research Gaps.md",
        sample_vault / "Writing" / "comparison-matrix.md",
    ]
    contents_run1 = {f: f.read_text(encoding="utf-8") for f in files}

    # Second run
    run_synthesis(sample_vault)
    contents_run2 = {f: f.read_text(encoding="utf-8") for f in files}

    for f in files:
        assert len(contents_run1[f]) == len(contents_run2[f]) or contents_run1[f].split("updated:")[0] == contents_run2[f].split("updated:")[0]


def test_synthesize_empty_vault_handling(tmp_path):
    """Test synthesis behavior when vault contains zero paper notes."""
    from kb_tools.synthesizer import run_synthesis

    empty_vault = tmp_path / "empty_vault"
    (empty_vault / "Sources" / "Papers").mkdir(parents=True, exist_ok=True)
    (empty_vault / "Knowledge").mkdir(parents=True, exist_ok=True)
    (empty_vault / "Writing").mkdir(parents=True, exist_ok=True)

    created = run_synthesis(empty_vault)
    assert isinstance(created, (list, dict))
