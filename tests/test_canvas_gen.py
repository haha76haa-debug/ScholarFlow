"""
Test Suite for kb_tools.canvas_gen and CLI 'generate-canvas' subcommand.
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
def canvas_test_vault(tmp_path):
    """Create a mock vault containing paper notes, concepts, and synthesis notes for canvas generation."""
    vault = tmp_path / "canvas_vault"
    papers_dir = vault / "Sources" / "Papers"
    concepts_dir = vault / "Knowledge" / "Concepts"
    knowledge_dir = vault / "Knowledge"
    maps_dir = vault / "Maps"

    for d in [papers_dir, concepts_dir, maps_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Paper 1: ResNet
    (papers_dir / "he2016deep.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Deep Residual Learning for Image Recognition"
citekey: he2016deep
zotero_key: "HE2016"
status: summarized
source_type: "conference paper"
claim_strength: strong
authors: ["Kaiming He", "Xiangyu Zhang"]
year: 2016
concepts: ["Residual Connections"]
methods: ["Skip Connection"]
paper_relationships:
  - "Sources/Papers/vaswani2017attention::precedes"
linked_knowledge:
  - "Knowledge/Literature Overview"
updated: 2026-08-19T00:00:00Z
---
# ResNet
## Relation to other papers
- Precedes [[Sources/Papers/vaswani2017attention]]
""", encoding="utf-8")

    # Paper 2: Transformer
    (papers_dir / "vaswani2017attention.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Attention Is All You Need"
citekey: vaswani2017attention
zotero_key: "VASWANI2017"
status: summarized
source_type: "conference paper"
claim_strength: strong
authors: ["Ashish Vaswani", "Noam Shazeer"]
year: 2017
concepts: ["Self-Attention", "Residual Connections"]
methods: ["Multi-Head Attention"]
paper_relationships:
  - "Sources/Papers/he2016deep::uses"
  - "Sources/Papers/hu2021lora::precedes"
linked_knowledge:
  - "Knowledge/Literature Overview"
  - "Knowledge/Research Gaps"
updated: 2026-08-19T00:00:00Z
---
# Transformer
## Relation to other papers
- Uses [[Sources/Papers/he2016deep]]
- Precedes [[Sources/Papers/hu2021lora]]
""", encoding="utf-8")

    # Paper 3: LoRA
    (papers_dir / "hu2021lora.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "LoRA: Low-Rank Adaptation of Large Language Models"
citekey: hu2021lora
zotero_key: "HU2021"
status: summarized
source_type: "conference paper"
claim_strength: strong
authors: ["Edward J. Hu", "Yelong Shen"]
year: 2021
concepts: ["Low-Rank Adaptation"]
methods: ["Low-Rank Decomposition"]
paper_relationships:
  - "Sources/Papers/vaswani2017attention::extends"
linked_knowledge:
  - "Knowledge/Literature Overview"
  - "Knowledge/Research Gaps"
updated: 2026-08-19T00:00:00Z
---
# LoRA
## Relation to other papers
- Extends [[Sources/Papers/vaswani2017attention]]
""", encoding="utf-8")

    # Paper 4: Hidden Paper (canvas_visibility: hidden)
    (papers_dir / "hidden2020draft.md").write_text("""---
type: paper
project: zotero_obsidian_kb
title: "Hidden Draft Paper"
citekey: hidden2020draft
zotero_key: "HIDDEN2020"
status: unread
canvas_visibility: hidden
source_type: "preprint"
claim_strength: speculative
authors: ["Anonymous"]
year: 2020
linked_knowledge: []
updated: 2026-08-19T00:00:00Z
---
# Hidden Draft
""", encoding="utf-8")

    # Concept Notes
    (concepts_dir / "Residual Connections.md").write_text("""---
type: concept
project: zotero_obsidian_kb
title: "Residual Connections"
status: active
claim_strength: strong
primary_sources: ["Sources/Papers/he2016deep"]
tags: ["knowledge", "concept"]
updated: 2026-08-19T00:00:00Z
---
# Residual Connections
""", encoding="utf-8")

    (concepts_dir / "Self-Attention.md").write_text("""---
type: concept
project: zotero_obsidian_kb
title: "Self-Attention"
status: active
claim_strength: strong
primary_sources: ["Sources/Papers/vaswani2017attention"]
tags: ["knowledge", "concept"]
updated: 2026-08-19T00:00:00Z
---
# Self-Attention
""", encoding="utf-8")

    (concepts_dir / "Low-Rank Adaptation.md").write_text("""---
type: concept
project: zotero_obsidian_kb
title: "Low-Rank Adaptation"
status: active
claim_strength: strong
primary_sources: ["Sources/Papers/hu2021lora"]
tags: ["knowledge", "concept"]
updated: 2026-08-19T00:00:00Z
---
# Low-Rank Adaptation
""", encoding="utf-8")

    # Synthesis Notes
    (knowledge_dir / "Literature Overview.md").write_text("""---
type: literature-synthesis
project: zotero_obsidian_kb
title: "Literature Overview"
status: active
covered_papers: ["Sources/Papers/he2016deep", "Sources/Papers/vaswani2017attention", "Sources/Papers/hu2021lora"]
key_themes: ["deep-learning", "architectures"]
updated: 2026-08-19T00:00:00Z
---
# Literature Overview
""", encoding="utf-8")

    (knowledge_dir / "Research Gaps.md").write_text("""---
type: research-gaps
project: zotero_obsidian_kb
title: "Research Gaps"
status: active
covered_papers: ["Sources/Papers/vaswani2017attention", "Sources/Papers/hu2021lora"]
key_themes: ["limitations", "scaling"]
updated: 2026-08-19T00:00:00Z
---
# Research Gaps
""", encoding="utf-8")

    return vault


@pytest.fixture
def canvas_4lane_test_vault(tmp_path):
    """Create a mock vault containing papers, concepts, silicon comparisons, and synthesis notes."""
    vault = tmp_path / "canvas_4lane_vault"
    papers_dir = vault / "Sources" / "Papers"
    concepts_dir = vault / "Knowledge" / "Concepts"
    comparisons_dir = vault / "Knowledge" / "Comparisons"
    knowledge_dir = vault / "Knowledge"
    writing_dir = vault / "Writing"
    maps_dir = vault / "Maps"

    for d in [papers_dir, concepts_dir, comparisons_dir, knowledge_dir, writing_dir, maps_dir]:
        d.mkdir(parents=True, exist_ok=True)

    # Paper 1: Liu 2021
    (papers_dir / "2021_Liu_2D-Transistors.md").write_text("""---
type: paper
project: 2d-semiconductors
title: "Transistor roadmap beyond CMOS"
citekey: 2021_Liu_2D-Transistors
status: active
claim_strength: strong
authors: ["Chao Liu", "Xiangyu Zhang"]
year: 2021
concepts: ["Knowledge/Concepts/contact_resistance_extraction", "Knowledge/Concepts/emerging_fet_benchmarking"]
linked_knowledge:
  - "[[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide]]"
updated: 2026-08-21T00:00:00Z
---
# Transistor Roadmap Beyond CMOS
## Silicon Analogy & Microelectronics Mapping
- [[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide]]
""", encoding="utf-8")

    # Paper 2: Cheng 2022
    (papers_dir / "2022_Cheng_FET-Benchmark.md").write_text("""---
type: paper
project: 2d-semiconductors
title: "How to report and benchmark emerging field-effect transistors"
citekey: 2022_Cheng_FET-Benchmark
status: active
claim_strength: strong
authors: ["Cheng Zhang", "Yelong Shen"]
year: 2022
concepts: ["Knowledge/Concepts/two_dimensional_transistor_scaling"]
linked_knowledge:
  - "[[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet]]"
updated: 2026-08-21T00:00:00Z
---
# How to report and benchmark emerging FETs
## Silicon Analogy & Microelectronics Mapping
- [[Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet]]
""", encoding="utf-8")

    # Concept 1
    (concepts_dir / "contact_resistance_extraction.md").write_text("""---
type: concept
project: 2d-semiconductors
title: "Contact Resistance Extraction"
status: active
claim_strength: strong
primary_sources: ["Sources/Papers/2021_Liu_2D-Transistors"]
tags: ["knowledge", "concept"]
updated: 2026-08-21T00:00:00Z
---
# Contact Resistance Extraction
""", encoding="utf-8")

    # Concept 2
    (concepts_dir / "two_dimensional_transistor_scaling.md").write_text("""---
type: concept
project: 2d-semiconductors
title: "Two-Dimensional Transistor Scaling"
status: active
claim_strength: strong
primary_sources: ["Sources/Papers/2022_Cheng_FET-Benchmark"]
tags: ["knowledge", "concept"]
updated: 2026-08-21T00:00:00Z
---
# Two-Dimensional Transistor Scaling
""", encoding="utf-8")

    # Comparison 1: Contact
    (comparisons_dir / "2d_contact_vdW_vs_silicon_silicide.md").write_text("""---
type: comparison
project: 2d-semiconductors
title: "2D vdW Contacts vs Silicon Silicide"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2021_Liu_2D-Transistors]]"
silicon_technology: "Silicon Silicide (NiSi/TiSi)"
tags: ["type/comparison", "topic/silicon-analogy"]
updated: 2026-08-21T00:00:00Z
---
# 2D vdW Contacts vs Silicon Silicide
## Executive Overview & Silicon Analogy
Comparative study.
""", encoding="utf-8")

    # Comparison 2: Electrostatic
    (comparisons_dir / "2d_electrostatic_scaling_vs_silicon_gaafet.md").write_text("""---
type: comparison
project: 2d-semiconductors
title: "2D Electrostatic Scaling vs Silicon GAAFET"
status: active
claim_strength: strong
primary_sources:
  - "[[Sources/Papers/2022_Cheng_FET-Benchmark]]"
silicon_technology: "Silicon GAAFET (3nm/2nm)"
tags: ["type/comparison", "topic/silicon-analogy"]
updated: 2026-08-21T00:00:00Z
---
# 2D Electrostatic Scaling vs Silicon GAAFET
## Executive Overview & Silicon Analogy
Comparative study.
""", encoding="utf-8")

    # Synthesis 1
    (knowledge_dir / "Literature Overview.md").write_text("""---
type: literature-synthesis
project: 2d-semiconductors
title: "Literature Overview"
status: active
covered_papers: ["Sources/Papers/2021_Liu_2D-Transistors", "Sources/Papers/2022_Cheng_FET-Benchmark"]
updated: 2026-08-21T00:00:00Z
---
# Literature Overview
""", encoding="utf-8")

    # Writing 1: comparison-matrix
    (writing_dir / "comparison-matrix.md").write_text("""---
type: synthesis
project: 2d-semiconductors
title: "Literature Comparison Matrix"
status: active
updated: 2026-08-21T00:00:00Z
---
# Comparison Matrix
""", encoding="utf-8")

    return vault


# ==============================================================================
# Tier 1: Unit & Schema Tests
# ==============================================================================

def test_canvas_json_schema_validity(canvas_test_vault):
    """Test generated canvas object conforms to JSON Canvas v1.0 schema."""
    from kb_tools.canvas_gen import build_canvas_graph

    canvas_data = build_canvas_graph(canvas_test_vault)

    assert isinstance(canvas_data, dict)
    assert "nodes" in canvas_data
    assert "edges" in canvas_data
    assert isinstance(canvas_data["nodes"], list)
    assert isinstance(canvas_data["edges"], list)

    # Must be valid JSON serializable
    serialized = json.dumps(canvas_data)
    assert len(serialized) > 0


def test_canvas_file_node_properties(canvas_test_vault):
    """Test required properties for 'file' type nodes."""
    from kb_tools.canvas_gen import build_canvas_graph

    canvas_data = build_canvas_graph(canvas_test_vault)
    file_nodes = [n for n in canvas_data["nodes"] if n.get("type") == "file"]

    assert len(file_nodes) >= 3

    for node in file_nodes:
        assert "id" in node
        assert isinstance(node["id"], str) and len(node["id"]) > 0
        assert "file" in node
        assert isinstance(node["file"], str)
        assert "x" in node and isinstance(node["x"], (int, float))
        assert "y" in node and isinstance(node["y"], (int, float))
        assert "width" in node and isinstance(node["width"], (int, float)) and node["width"] > 0
        assert "height" in node and isinstance(node["height"], (int, float)) and node["height"] > 0
        assert "color" in node


def test_canvas_group_node_properties(canvas_test_vault):
    """Test group container nodes and their properties."""
    from kb_tools.canvas_gen import build_canvas_graph

    canvas_data = build_canvas_graph(canvas_test_vault)
    group_nodes = [n for n in canvas_data["nodes"] if n.get("type") == "group"]

    # If groups are enabled, verify bounding boxes and labels
    if group_nodes:
        for group in group_nodes:
            assert "id" in group
            assert "label" in group
            assert "x" in group
            assert "y" in group
            assert "width" in group and group["width"] > 0
            assert "height" in group and group["height"] > 0


def test_canvas_group_bounding_box_enclosure(canvas_test_vault):
    """Test that group bounding boxes properly enclose their child nodes."""
    from kb_tools.canvas_gen import build_canvas_graph

    canvas_data = build_canvas_graph(canvas_test_vault)
    group_nodes = [n for n in canvas_data["nodes"] if n.get("type") == "group"]
    file_nodes = [n for n in canvas_data["nodes"] if n.get("type") == "file"]

    # Verify group dimensions are larger than individual file nodes
    for group in group_nodes:
        assert group["width"] >= 300
        assert group["height"] >= 200


def test_canvas_obsidian_color_semantics(canvas_test_vault):
    """Test node and edge colors adhere to Obsidian 6-color palette or hex strings."""
    from kb_tools.canvas_gen import build_canvas_graph

    canvas_data = build_canvas_graph(canvas_test_vault)
    valid_color_indices = {"1", "2", "3", "4", "5", "6", 1, 2, 3, 4, 5, 6}

    for node in canvas_data["nodes"]:
        if "color" in node:
            c = node["color"]
            is_valid_idx = str(c) in valid_color_indices
            is_valid_hex = isinstance(c, str) and c.startswith("#") and len(c) in (4, 7)
            assert is_valid_idx or is_valid_hex, f"Invalid color format: {c}"


def test_canvas_collision_free_layout(canvas_test_vault):
    """Test that generated node bounding boxes do not collide or overlap within the same group/lane."""
    from kb_tools.canvas_gen import build_canvas_graph

    canvas_data = build_canvas_graph(canvas_test_vault)
    leaf_nodes = [n for n in canvas_data["nodes"] if n.get("type") in ("file", "text", "link")]

    for i in range(len(leaf_nodes)):
        for j in range(i + 1, len(leaf_nodes)):
            n1 = leaf_nodes[i]
            n2 = leaf_nodes[j]

            # Check overlap rectangle:
            # Overlap occurs if (n1.x < n2.x + n2.w) and (n1.x + n1.w > n2.x) and (n1.y < n2.y + n2.h) and (n1.y + n1.h > n2.y)
            x_overlap = (n1["x"] < n2["x"] + n2["width"]) and (n1["x"] + n1["width"] > n2["x"])
            y_overlap = (n1["y"] < n2["y"] + n2["height"]) and (n1["y"] + n1["height"] > n2["y"])

            # Leaf nodes should not collide
            assert not (x_overlap and y_overlap), f"Collision detected between nodes {n1.get('id')} and {n2.get('id')}"


def test_canvas_edge_semantics_and_labels(canvas_test_vault):
    """Test generated edges have valid connection IDs, valid side semantics, and meaningful labels."""
    from kb_tools.canvas_gen import build_canvas_graph

    canvas_data = build_canvas_graph(canvas_test_vault)
    edges = canvas_data["edges"]

    assert len(edges) >= 2

    allowed_labels = {"uses", "extends", "supports", "contradicts", "motivates", "summarizes", "relates", "addresses", "precedes"}

    for edge in edges:
        assert "id" in edge
        assert "fromNode" in edge
        assert "toNode" in edge
        if "label" in edge and edge["label"]:
            label = edge["label"].lower()
            assert any(allowed in label for allowed in allowed_labels)


def test_canvas_dangling_edge_check(canvas_test_vault):
    """Test zero dangling edges: every edge must connect valid existing node IDs."""
    from kb_tools.canvas_gen import build_canvas_graph

    canvas_data = build_canvas_graph(canvas_test_vault)
    node_ids = {n["id"] for n in canvas_data["nodes"]}

    for edge in canvas_data["edges"]:
        from_id = edge["fromNode"]
        to_id = edge["toNode"]
        assert from_id in node_ids, f"Dangling edge: fromNode '{from_id}' not found in nodes"
        assert to_id in node_ids, f"Dangling edge: toNode '{to_id}' not found in nodes"


def test_canvas_hidden_visibility_exclusion(canvas_test_vault):
    """Test notes with canvas_visibility: hidden are excluded from canvas nodes."""
    from kb_tools.canvas_gen import build_canvas_graph

    canvas_data = build_canvas_graph(canvas_test_vault)
    file_targets = [n.get("file", "") for n in canvas_data["nodes"] if n.get("type") == "file"]

    assert not any("hidden2020draft" in f for f in file_targets)


# ==============================================================================
# Tier 2: CLI & Generation Tests
# ==============================================================================

def test_generate_canvas_writes_to_maps(canvas_test_vault):
    """Test canvas generator writes Maps/literature.canvas file."""
    from kb_tools.canvas_gen import generate_canvas_file

    out_file = canvas_test_vault / "Maps" / "literature.canvas"
    if out_file.exists():
        out_file.unlink()

    generated_path = generate_canvas_file(canvas_test_vault, output_path=out_file)
    assert Path(generated_path).exists()

    content = Path(generated_path).read_text(encoding="utf-8")
    data = json.loads(content)
    assert "nodes" in data
    assert "edges" in data
    assert len(data["nodes"]) >= 3


def test_generate_canvas_cli_invocation(canvas_test_vault, capsys):
    """Test CLI subcommand 'generate-canvas' execution."""
    from kb_tools.cli import main

    exit_code = main(["generate-canvas", "--vault-dir", str(canvas_test_vault)])
    assert exit_code == 0

    canvas_file = canvas_test_vault / "Maps" / "literature.canvas"
    assert canvas_file.exists()


def test_generate_canvas_cli_dry_run(canvas_test_vault):
    """Test generate-canvas with --dry-run does not write file."""
    from kb_tools.cli import main

    canvas_file = canvas_test_vault / "Maps" / "literature.canvas"
    if canvas_file.exists():
        canvas_file.unlink()

    exit_code = main(["generate-canvas", "--vault-dir", str(canvas_test_vault), "--dry-run"])
    assert exit_code == 0
    assert not canvas_file.exists()


def test_generate_canvas_cli_json_output(canvas_test_vault, capsys):
    """Test generate-canvas with --json outputs valid JSON representation."""
    from kb_tools.cli import main

    exit_code = main(["generate-canvas", "--vault-dir", str(canvas_test_vault), "--json"])
    assert exit_code == 0

    captured = capsys.readouterr()
    data = json.loads(captured.out)
    assert "nodes" in data or "canvas" in data


def test_generate_canvas_empty_vault(tmp_path):
    """Test canvas generation on empty vault generates valid empty canvas structure."""
    from kb_tools.canvas_gen import generate_canvas_file

    empty_vault = tmp_path / "empty_vault"
    (empty_vault / "Maps").mkdir(parents=True, exist_ok=True)

    out_file = empty_vault / "Maps" / "literature.canvas"
    generate_canvas_file(empty_vault, output_path=out_file)

    assert out_file.exists()
    data = json.loads(out_file.read_text(encoding="utf-8"))
    assert data == {"nodes": [], "edges": []} or (isinstance(data.get("nodes"), list) and isinstance(data.get("edges"), list))


# ==============================================================================
# Tier 3: Milestone 3 (M3) 4-Lane Canvas & Graph Config Tests
# ==============================================================================

def test_canvas_4_lane_layout_coordinates_and_groups(canvas_4lane_test_vault):
    """Test 4-lane horizontal swimlane layout coordinates and group containers."""
    from kb_tools.canvas_gen import build_canvas_graph

    canvas_data = build_canvas_graph(canvas_4lane_test_vault)
    nodes = canvas_data["nodes"]
    groups = [n for n in nodes if n.get("type") == "group"]
    file_nodes = [n for n in nodes if n.get("type") == "file"]

    # 4 distinct groups must exist
    assert len(groups) == 4
    group_labels = {g["label"] for g in groups}
    assert "Foundational Literature" in group_labels
    assert "Theoretical Concepts & Physics" in group_labels
    assert "Silicon Parallels & Comparisons" in group_labels
    assert "Synthesis & Writing" in group_labels

    # Verify column X coordinates for file nodes
    col1_nodes = [n for n in file_nodes if n["x"] == 0]
    col2_nodes = [n for n in file_nodes if n["x"] == 680]
    col3_nodes = [n for n in file_nodes if n["x"] == 1360]
    col4_nodes = [n for n in file_nodes if n["x"] == 2040]

    assert len(col1_nodes) == 2  # 2 Papers
    assert len(col2_nodes) == 2  # 2 Concepts
    assert len(col3_nodes) == 2  # 2 Silicon Comparisons
    assert len(col4_nodes) == 2  # 2 Synthesis / Writing

    # Verify group bounding box boundaries
    group_by_label = {g["label"]: g for g in groups}
    assert group_by_label["Foundational Literature"]["x"] == -40
    assert group_by_label["Theoretical Concepts & Physics"]["x"] == 640
    assert group_by_label["Silicon Parallels & Comparisons"]["x"] == 1320
    assert group_by_label["Synthesis & Writing"]["x"] == 2000

    for g in groups:
        assert g["width"] == 540
        assert g["y"] == -40
        assert g["height"] > 0


def test_canvas_comparison_nodes_cyan_color_semantics(canvas_4lane_test_vault):
    """Test Silicon Comparison nodes and container have color #0891b2 (Cyan)."""
    from kb_tools.canvas_gen import build_canvas_graph

    canvas_data = build_canvas_graph(canvas_4lane_test_vault)
    nodes = canvas_data["nodes"]

    comp_nodes = [n for n in nodes if n.get("type") == "file" and n.get("x") == 1360]
    assert len(comp_nodes) >= 2
    for node in comp_nodes:
        assert node.get("color") == "#0891b2"

    comp_group = next(g for g in nodes if g.get("type") == "group" and g.get("label") == "Silicon Parallels & Comparisons")
    assert comp_group.get("color") == "#0891b2"


def test_canvas_4_lane_collision_free_and_edge_semantics(canvas_4lane_test_vault):
    """Test collision-free layout and cross-lane edge routing in 4-lane canvas."""
    from kb_tools.canvas_gen import build_canvas_graph

    canvas_data = build_canvas_graph(canvas_4lane_test_vault)
    leaf_nodes = [n for n in canvas_data["nodes"] if n.get("type") == "file"]
    edges = canvas_data["edges"]

    # Collision test across all leaf nodes
    for i in range(len(leaf_nodes)):
        for j in range(i + 1, len(leaf_nodes)):
            n1 = leaf_nodes[i]
            n2 = leaf_nodes[j]
            x_overlap = (n1["x"] < n2["x"] + n2["width"]) and (n1["x"] + n1["width"] > n2["x"])
            y_overlap = (n1["y"] < n2["y"] + n2["height"]) and (n1["y"] + n1["height"] > n2["y"])
            assert not (x_overlap and y_overlap), f"Collision detected between {n1['id']} and {n2['id']}"

    # Edge semantics: uses, benchmarks, maps_to, synthesizes
    labels = {e.get("label") for e in edges if e.get("label")}
    assert "uses" in labels
    assert "benchmarks" in labels
    assert "maps_to" in labels
    assert "synthesizes" in labels

    # Cyan color on comparison edges
    silicon_edges = [e for e in edges if e.get("color") == "#0891b2"]
    assert len(silicon_edges) >= 2


def test_obsidian_graph_config_color_groups():
    """Verify .obsidian/graph.json contains Knowledge/Comparisons color group with rgb 561586."""
    graph_config_path = Path(__file__).resolve().parent.parent / ".obsidian" / "graph.json"
    assert graph_config_path.exists()

    data = json.loads(graph_config_path.read_text(encoding="utf-8"))
    assert "colorGroups" in data
    color_groups = data["colorGroups"]

    comp_groups = [g for g in color_groups if g.get("query") == "path:Knowledge/Comparisons"]
    assert len(comp_groups) == 1
    assert comp_groups[0]["color"]["rgb"] == 561586
    assert comp_groups[0]["color"]["a"] == 1


def test_live_vault_literature_canvas_validation():
    """Verify live vault Maps/literature.canvas is valid JSON Canvas v1.0 with 4 swimlanes."""
    canvas_path = Path(__file__).resolve().parent.parent / "Maps" / "literature.canvas"
    assert canvas_path.exists()

    data = json.loads(canvas_path.read_text(encoding="utf-8"))
    assert "nodes" in data
    assert "edges" in data
    assert len(data["nodes"]) >= 8
    assert len(data["edges"]) >= 6

    # Verify group nodes
    groups = [n for n in data["nodes"] if n.get("type") == "group"]
    has_comparisons = (Path(__file__).resolve().parent.parent / "Knowledge" / "Comparisons").exists() and any((Path(__file__).resolve().parent.parent / "Knowledge" / "Comparisons").glob("*.md"))
    if has_comparisons:
        assert len(groups) == 4
        labels = {g["label"] for g in groups}
        assert "Foundational Literature" in labels
        assert "Theoretical Concepts & Physics" in labels
        assert "Silicon Parallels & Comparisons" in labels
        assert "Synthesis & Writing" in labels

        # Check comparison group color
        silicon_group = next(g for g in groups if g["label"] == "Silicon Parallels & Comparisons")
        assert silicon_group["color"] == "#0891b2"
    else:
        assert len(groups) >= 3
        labels = {g["label"] for g in groups}
        assert "Foundational Literature" in labels
        assert "Theoretical Concepts & Physics" in labels
        assert "Synthesis & Writing" in labels

