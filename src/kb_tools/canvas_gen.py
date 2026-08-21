"""
Obsidian JSON Canvas v1.0 Visual Topology Generator.
Minimalist, Clean, Non-Crossing Pipeline Flow.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from kb_tools.models import (
    extract_wikilinks,
    parse_frontmatter,
    scan_vault_notes,
)

# Obsidian 6-color palette + custom hex
COLOR_RED = "1"       # Gaps, contradictions, failure modes
COLOR_ORANGE = "2"    # Paper sources, empirical observations
COLOR_YELLOW = "3"    # Methods, algorithms
COLOR_GREEN = "4"     # Validated claims, benchmarks
COLOR_CYAN = "5"      # Synthesis, overviews
COLOR_PURPLE = "6"    # Concepts, mathematical paradigms
COLOR_SILICON = "#0891b2" # Silicon parallels & comparisons (Cyan hex)


def _clean_ref(raw_ref: Any) -> str:
    """Clean a target reference by stripping brackets, aliases, and anchors."""
    if raw_ref is None:
        return ""
    ref_str = str(raw_ref).strip()
    if ref_str.startswith("[["):
        ref_str = ref_str[2:]
    if ref_str.endswith("]]"):
        ref_str = ref_str[:-2]
    ref_str = ref_str.strip()
    if "|" in ref_str:
        ref_str = ref_str.split("|", 1)[0].strip()
    if "#" in ref_str:
        ref_str = ref_str.split("#", 1)[0].strip()
    return ref_str


def _resolve_target_id(ref: Any, path_to_node_id: Dict[str, str]) -> Optional[str]:
    """Resolve a target reference to a canvas node ID."""
    clean = _clean_ref(ref)
    if not clean:
        return None
    stem = Path(clean).stem
    clean_no_ext = clean[:-3] if clean.endswith(".md") else clean
    return (
        path_to_node_id.get(clean)
        or path_to_node_id.get(clean_no_ext)
        or path_to_node_id.get(stem)
        or path_to_node_id.get(clean.lower())
        or path_to_node_id.get(clean_no_ext.lower())
        or path_to_node_id.get(stem.lower())
    )


def build_canvas_graph(vault_dir: Path) -> Dict[str, Any]:
    """Scan vault and build Obsidian JSON Canvas v1.0 data structure with 4-lane streamline flow."""
    vault_path = Path(vault_dir).resolve()
    all_notes = scan_vault_notes(vault_path)

    nodes: List[Dict[str, Any]] = []
    edges: List[Dict[str, Any]] = []

    path_to_node_id: Dict[str, str] = {}
    paper_nodes: List[Dict[str, Any]] = []
    concept_nodes: List[Dict[str, Any]] = []
    comparison_nodes: List[Dict[str, Any]] = []
    synthesis_nodes: List[Dict[str, Any]] = []

    for note_path in all_notes:
        rel_posix = note_path.relative_to(vault_path).as_posix()
        if (
            rel_posix in ("00-Hub.md", "01-Plan.md", "02-Index.md")
            or rel_posix.endswith("/index.md") or rel_posix.endswith("/z-Index.md") or rel_posix.endswith("/z_index.md")
            or rel_posix.startswith("Templates/")
            or rel_posix.startswith("Archive/")
        ):
            continue

        try:
            content = note_path.read_text(encoding="utf-8")
        except Exception:
            continue

        fm, body = parse_frontmatter(content)
        visibility = str(fm.get("canvas_visibility", "visible")).lower()
        if visibility == "hidden":
            continue

        note_type = str(fm.get("type", "note")).lower()
        stem = note_path.stem
        node_id = f"node-{stem.lower().replace(' ', '-')}"

        path_to_node_id[rel_posix] = node_id
        path_to_node_id[rel_posix[:-3] if rel_posix.endswith(".md") else rel_posix] = node_id
        path_to_node_id[rel_posix.lower()] = node_id
        path_to_node_id[(rel_posix[:-3] if rel_posix.endswith(".md") else rel_posix).lower()] = node_id
        path_to_node_id[stem] = node_id
        path_to_node_id[stem.lower()] = node_id

        note_item = {
            "id": node_id,
            "path": note_path,
            "rel_posix": rel_posix,
            "stem": stem,
            "frontmatter": fm,
            "body": body,
            "type": note_type,
        }

        if rel_posix.startswith("Sources/Papers/") or note_type == "paper":
            paper_nodes.append(note_item)
        elif rel_posix.startswith("Knowledge/Concepts/") or note_type == "concept":
            concept_nodes.append(note_item)
        elif (
            rel_posix.startswith("Knowledge/Comparisons/")
            or note_type in ("comparison", "silicon-comparison")
        ):
            comparison_nodes.append(note_item)
        elif (
            rel_posix.startswith("Knowledge/")
            or rel_posix.startswith("Writing/")
            or note_type in ("literature-synthesis", "method-taxonomy", "research-gaps")
        ):
            synthesis_nodes.append(note_item)

    if not paper_nodes and not concept_nodes and not comparison_nodes and not synthesis_nodes:
        return {"nodes": [], "edges": []}

    # Card dimensions
    CARD_W = 460
    CARD_H = 340
    GAP_Y = 80
    PAD = 40

    COL1_X = 0
    COL2_X = 680
    COL3_X = 1360
    COL4_X = 2040

    total_rows = max(len(paper_nodes), len(concept_nodes), len(comparison_nodes), len(synthesis_nodes))
    total_height = total_rows * (CARD_H + GAP_Y) - GAP_Y + 2 * PAD if total_rows > 0 else 0

    # Layout Column 1: Foundational Papers (X = 0)
    paper_stride = (CARD_H + GAP_Y) * 2 if len(concept_nodes) >= len(paper_nodes) * 2 and len(paper_nodes) > 0 else (CARD_H + GAP_Y)
    for idx, p in enumerate(paper_nodes):
        y_pos = idx * paper_stride + (paper_stride - CARD_H) // 4 if paper_stride > CARD_H + GAP_Y else idx * (CARD_H + GAP_Y)
        nodes.append({
            "id": p["id"],
            "type": "file",
            "file": p["rel_posix"],
            "x": COL1_X,
            "y": y_pos,
            "width": CARD_W,
            "height": CARD_H,
            "color": COLOR_ORANGE,
        })

    if paper_nodes:
        nodes.append({
            "id": "group-foundational-literature",
            "type": "group",
            "label": "Foundational Literature",
            "x": COL1_X - PAD,
            "y": -PAD,
            "width": CARD_W + 2 * PAD,
            "height": total_height,
            "color": COLOR_ORANGE,
        })

    # Layout Column 2: Atomic Concepts & Physics (X = 680)
    for idx, c in enumerate(concept_nodes):
        y_pos = idx * (CARD_H + GAP_Y)
        nodes.append({
            "id": c["id"],
            "type": "file",
            "file": c["rel_posix"],
            "x": COL2_X,
            "y": y_pos,
            "width": CARD_W,
            "height": CARD_H,
            "color": COLOR_PURPLE,
        })

    if concept_nodes:
        nodes.append({
            "id": "group-theoretical-concepts",
            "type": "group",
            "label": "Theoretical Concepts & Physics",
            "x": COL2_X - PAD,
            "y": -PAD,
            "width": CARD_W + 2 * PAD,
            "height": total_height,
            "color": COLOR_PURPLE,
        })

    # Layout Column 3: Silicon Comparisons (X = 1360)
    comp_stride = (CARD_H + GAP_Y) * 2 if len(concept_nodes) >= len(comparison_nodes) * 2 and len(comparison_nodes) > 0 else (CARD_H + GAP_Y)
    for idx, comp in enumerate(comparison_nodes):
        y_pos = idx * comp_stride + (comp_stride - CARD_H) // 4 if comp_stride > CARD_H + GAP_Y else idx * (CARD_H + GAP_Y)
        nodes.append({
            "id": comp["id"],
            "type": "file",
            "file": comp["rel_posix"],
            "x": COL3_X,
            "y": y_pos,
            "width": CARD_W,
            "height": CARD_H,
            "color": COLOR_SILICON,
        })

    if comparison_nodes:
        nodes.append({
            "id": "group-silicon-comparisons",
            "type": "group",
            "label": "Silicon Parallels & Comparisons",
            "x": COL3_X - PAD,
            "y": -PAD,
            "width": CARD_W + 2 * PAD,
            "height": total_height,
            "color": COLOR_SILICON,
        })

    # Layout Column 4: Synthesis & Writing (X = 2040)
    for idx, s in enumerate(synthesis_nodes):
        y_pos = idx * (CARD_H + GAP_Y)
        s_type = s["type"]
        color = COLOR_RED if "gap" in s["stem"].lower() or s_type == "research-gaps" else COLOR_CYAN

        nodes.append({
            "id": s["id"],
            "type": "file",
            "file": s["rel_posix"],
            "x": COL4_X,
            "y": y_pos,
            "width": CARD_W,
            "height": CARD_H,
            "color": color,
        })

    if synthesis_nodes:
        nodes.append({
            "id": "group-synthesis-and-writing",
            "type": "group",
            "label": "Synthesis & Writing",
            "x": COL4_X - PAD,
            "y": -PAD,
            "width": CARD_W + 2 * PAD,
            "height": total_height,
            "color": COLOR_CYAN,
        })

    valid_node_ids = {n["id"] for n in nodes}
    edge_pairs: Set[Tuple[str, str]] = set()

    def _add_edge(
        from_node: str,
        to_node: str,
        label: str = "",
        color: str = "4",
        from_side: str = "right",
        to_side: str = "left",
    ):
        if from_node in valid_node_ids and to_node in valid_node_ids and from_node != to_node:
            pair = (from_node, to_node)
            if pair not in edge_pairs:
                edge_pairs.add(pair)
                edge_id = f"edge-{from_node}-{to_node}-{len(edges)}"
                edges.append({
                    "id": edge_id,
                    "fromNode": from_node,
                    "fromSide": from_side,
                    "toNode": to_node,
                    "toSide": to_side,
                    "label": label,
                    "color": color,
                    "fromEnd": "none",
                    "toEnd": "arrow",
                })

    # 1. Clean Left-to-Right Edge: Paper -> Concept (uses)
    for c in concept_nodes:
        fm = c["frontmatter"]
        concept_id = c["id"]
        sources = fm.get("primary_sources", [])
        if isinstance(sources, list):
            for s in sources:
                src_id = _resolve_target_id(s, path_to_node_id)
                if src_id:
                    _add_edge(src_id, concept_id, "uses", color=COLOR_PURPLE, from_side="right", to_side="left")

    for p in paper_nodes:
        fm = p["frontmatter"]
        p_id = p["id"]
        conc_list = fm.get("concepts", [])
        if isinstance(conc_list, list):
            for conc in conc_list:
                c_id = _resolve_target_id(conc, path_to_node_id)
                if c_id:
                    _add_edge(p_id, c_id, "uses", color=COLOR_PURPLE, from_side="right", to_side="left")

    # Inter-paper relationships & body wikilinks
    for p in paper_nodes:
        fm = p["frontmatter"]
        body = p["body"]
        from_id = p["id"]

        rels = fm.get("paper_relationships", [])
        if isinstance(rels, list):
            for rel in rels:
                if "::" in str(rel):
                    target_ref, rel_label = str(rel).split("::", 1)
                    target_id = _resolve_target_id(target_ref, path_to_node_id)
                    if target_id:
                        _add_edge(from_id, target_id, rel_label.strip().lower(), from_side="bottom", to_side="top")

        for line in body.splitlines():
            line_str = line.strip()
            for verb in ["Extends", "Precedes", "Uses", "Supports", "Contradicts", "Motivates", "Addresses"]:
                if line_str.startswith(f"- {verb} [[") or line_str.startswith(f"{verb} [["):
                    m = re.search(r"\[\[([^\]|#]+)", line_str)
                    if m:
                        target_str = m.group(1).strip()
                        target_id = _resolve_target_id(target_str, path_to_node_id)
                        if target_id:
                            _add_edge(from_id, target_id, verb.lower())

    # 2. Paper -> Comparison (benchmarks, color="#0891b2")
    if comparison_nodes:
        for comp in comparison_nodes:
            fm = comp["frontmatter"]
            comp_id = comp["id"]
            sources = fm.get("primary_sources", [])
            if isinstance(sources, list):
                for s in sources:
                    src_id = _resolve_target_id(s, path_to_node_id)
                    if src_id:
                        _add_edge(src_id, comp_id, "benchmarks", color=COLOR_SILICON, from_side="right", to_side="left")

        for p in paper_nodes:
            p_id = p["id"]
            linked = p["frontmatter"].get("linked_knowledge", [])
            if isinstance(linked, list):
                for lk in linked:
                    comp_id = _resolve_target_id(lk, path_to_node_id)
                    if comp_id and any(cn["id"] == comp_id for cn in comparison_nodes):
                        _add_edge(p_id, comp_id, "benchmarks", color=COLOR_SILICON, from_side="right", to_side="left")

    # 3. Concept -> Comparison (maps_to, color="#0891b2")
    if comparison_nodes and concept_nodes:
        connected_concept_ids: Set[str] = set()

        for comp in comparison_nodes:
            comp_id = comp["id"]
            comp_sources = {_clean_ref(s) for s in comp["frontmatter"].get("primary_sources", []) if _clean_ref(s)}
            
            for c in concept_nodes:
                c_id = c["id"]
                c_sources = {_clean_ref(s) for s in c["frontmatter"].get("primary_sources", []) if _clean_ref(s)}
                if comp_sources & c_sources:
                    _add_edge(c_id, comp_id, "maps_to", color=COLOR_SILICON, from_side="right", to_side="left")
                    connected_concept_ids.add(c_id)

        for idx, c in enumerate(concept_nodes):
            c_id = c["id"]
            if c_id not in connected_concept_ids:
                comp_idx = min(idx // 2 if len(concept_nodes) >= len(comparison_nodes) * 2 else idx, len(comparison_nodes) - 1)
                target_comp = comparison_nodes[comp_idx]
                _add_edge(c_id, target_comp["id"], "maps_to", color=COLOR_SILICON, from_side="right", to_side="left")

    # 4. Comparison -> Synthesis (synthesizes, color="5")
    if comparison_nodes and synthesis_nodes:
        for idx, comp in enumerate(comparison_nodes):
            comp_id = comp["id"]
            synth_idx = min(idx, len(synthesis_nodes) - 1)
            target_synth = synthesis_nodes[synth_idx]
            _add_edge(comp_id, target_synth["id"], "synthesizes", color=COLOR_CYAN, from_side="right", to_side="left")

        for s in synthesis_nodes:
            s_id = s["id"]
            for comp in comparison_nodes:
                comp_id = comp["id"]
                if comp["stem"] in s["body"] or comp["rel_posix"] in s["body"]:
                    _add_edge(comp_id, s_id, "synthesizes", color=COLOR_CYAN, from_side="right", to_side="left")

    # 5. Backward-Compatible Fallback: Concept -> Synthesis when no comparison nodes exist
    if not comparison_nodes and concept_nodes and synthesis_nodes:
        for idx, c in enumerate(concept_nodes):
            concept_id = c["id"]
            synth_idx = min(idx, len(synthesis_nodes) - 1)
            target_synth = synthesis_nodes[synth_idx]
            synth_id = target_synth["id"]
            stem_lower = target_synth["stem"].lower()

            if "gap" in stem_lower:
                label = "addresses"
                color = COLOR_RED
            elif "taxonomy" in stem_lower:
                label = "uses"
                color = COLOR_YELLOW
            else:
                label = "summarizes"
                color = COLOR_CYAN

            _add_edge(concept_id, synth_id, label, color=color, from_side="right", to_side="left")

    return {
        "nodes": nodes,
        "edges": edges,
    }


def generate_canvas_file(
    vault_dir: Path,
    output_path: Optional[Path] = None,
    dry_run: bool = False,
) -> Path:
    """Generate and write Maps/literature.canvas file."""
    vault_path = Path(vault_dir).resolve()
    target_file = (
        Path(output_path).resolve()
        if output_path
        else vault_path / "Maps" / "literature.canvas"
    )

    canvas_data = build_canvas_graph(vault_path)

    if not dry_run:
        target_file.parent.mkdir(parents=True, exist_ok=True)
        target_file.write_text(
            json.dumps(canvas_data, indent=2, ensure_ascii=False),
            encoding="utf-8",
        )

    return target_file
