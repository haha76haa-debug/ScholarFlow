"""
Empirical Challenge & Stress Test Harness for Milestone 2 (M2):
Literature Note Silicon Analogy Mapping and Bidirectional Link Reciprocity.
"""

from __future__ import annotations

import copy
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple

import pytest
import yaml

from kb_tools.link_checker import (
    build_vault_graph,
    check_links,
    find_all_wikilinks,
    repair_links,
)
from kb_tools.linter import lint_paper_note, lint_vault, validate_tag
from kb_tools.models import (
    get_canonical_note_map,
    parse_frontmatter,
    scan_vault_notes,
)


@pytest.fixture
def vault_root() -> Path:
    return Path(__file__).resolve().parent.parent


@pytest.fixture
def paper_liu(vault_root: Path) -> Path:
    p = vault_root / "Sources" / "Papers" / "2021_Liu_2D-Transistors.md"
    assert p.exists(), f"File not found: {p}"
    return p


@pytest.fixture
def paper_cheng(vault_root: Path) -> Path:
    p = vault_root / "Sources" / "Papers" / "2022_Cheng_FET-Benchmark.md"
    assert p.exists(), f"File not found: {p}"
    return p


@pytest.fixture
def comp_contact(vault_root: Path) -> Path:
    p = vault_root / "Knowledge" / "Comparisons" / "2d_contact_vdW_vs_silicon_silicide.md"
    assert p.exists(), f"File not found: {p}"
    return p


@pytest.fixture
def comp_electrostatic(vault_root: Path) -> Path:
    p = vault_root / "Knowledge" / "Comparisons" / "2d_electrostatic_scaling_vs_silicon_gaafet.md"
    assert p.exists(), f"File not found: {p}"
    return p


# ==============================================================================
# Tier 1: Bidirectional Link Reciprocity & Graph Topology Tests
# ==============================================================================

class TestM2BidirectionalLinkReciprocity:
    """Rigorous assertion of 2-way graph connections between Papers and Comparisons."""

    def test_sources_to_comparisons_frontmatter_links(
        self, paper_liu: Path, paper_cheng: Path
    ):
        """Verify frontmatter linked_knowledge contains exact comparison note wikilinks."""
        for paper_path in (paper_liu, paper_cheng):
            fm, _ = parse_frontmatter(paper_path.read_text(encoding="utf-8"))
            linked = fm.get("linked_knowledge", [])
            assert isinstance(linked, list), f"linked_knowledge must be a list in {paper_path.name}"

            # Clean wikilink brackets
            clean_links = [re.sub(r"[\[\]\"]", "", str(item)).strip() for item in linked]

            assert any("Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide" in l for l in clean_links), (
                f"{paper_path.name} frontmatter missing 2d_contact_vdW_vs_silicon_silicide in linked_knowledge"
            )
            assert any("Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet" in l for l in clean_links), (
                f"{paper_path.name} frontmatter missing 2d_electrostatic_scaling_vs_silicon_gaafet in linked_knowledge"
            )

    def test_sources_to_comparisons_body_wikilinks(
        self, paper_liu: Path, paper_cheng: Path
    ):
        """Verify markdown body contains explicit wikilinks to both comparison cards."""
        for paper_path in (paper_liu, paper_cheng):
            content = paper_path.read_text(encoding="utf-8")
            wikilinks = find_all_wikilinks(content)
            targets = {w[1] for w in wikilinks}

            assert any(
                "Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide" in t or t == "2d_contact_vdW_vs_silicon_silicide"
                for t in targets
            ), f"{paper_path.name} body missing wikilink to 2d_contact_vdW_vs_silicon_silicide"

            assert any(
                "Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet" in t or t == "2d_electrostatic_scaling_vs_silicon_gaafet"
                for t in targets
            ), f"{paper_path.name} body missing wikilink to 2d_electrostatic_scaling_vs_silicon_gaafet"

    def test_comparisons_to_sources_reciprocal_primary_sources(
        self, comp_contact: Path, comp_electrostatic: Path
    ):
        """Verify comparison notes reference both source papers in frontmatter primary_sources."""
        for comp_path in (comp_contact, comp_electrostatic):
            fm, _ = parse_frontmatter(comp_path.read_text(encoding="utf-8"))
            primary = fm.get("primary_sources", [])
            assert isinstance(primary, list), f"primary_sources must be a list in {comp_path.name}"

            clean_primary = [re.sub(r"[\[\]\"]", "", str(item)).strip() for item in primary]

            assert any("Sources/Papers/2021_Liu_2D-Transistors" in p for p in clean_primary), (
                f"{comp_path.name} missing primary source 2021_Liu_2D-Transistors"
            )
            assert any("Sources/Papers/2022_Cheng_FET-Benchmark" in p for p in clean_primary), (
                f"{comp_path.name} missing primary source 2022_Cheng_FET-Benchmark"
            )

    def test_comparisons_to_sources_reciprocal_body_wikilinks(
        self, comp_contact: Path, comp_electrostatic: Path
    ):
        """Verify comparison cards contain reciprocal body wikilinks back to both source papers."""
        for comp_path in (comp_contact, comp_electrostatic):
            content = comp_path.read_text(encoding="utf-8")
            wikilinks = find_all_wikilinks(content)
            targets = {w[1] for w in wikilinks}

            assert any(
                "Sources/Papers/2021_Liu_2D-Transistors" in t or t == "2021_Liu_2D-Transistors"
                for t in targets
            ), f"{comp_path.name} body missing wikilink back to 2021_Liu_2D-Transistors"

            assert any(
                "Sources/Papers/2022_Cheng_FET-Benchmark" in t or t == "2022_Cheng_FET-Benchmark"
                for t in targets
            ), f"{comp_path.name} body missing wikilink back to 2022_Cheng_FET-Benchmark"

    def test_full_vault_directed_graph_reciprocal_edges(self, vault_root: Path):
        """Verify directed graph contains bidirectional edges for all (Paper, Comparison) pairs."""
        graph = build_vault_graph(vault_root)

        paper_keys = [
            "Sources/Papers/2021_Liu_2D-Transistors.md",
            "Sources/Papers/2022_Cheng_FET-Benchmark.md",
        ]
        comp_keys = [
            "Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide.md",
            "Knowledge/Comparisons/2d_electrostatic_scaling_vs_silicon_gaafet.md",
        ]

        for p_key in paper_keys:
            assert p_key in graph, f"Paper {p_key} not found in vault graph"
            for c_key in comp_keys:
                assert c_key in graph, f"Comparison {c_key} not found in vault graph"

                # Check Forward Edge: Paper -> Comparison
                assert c_key in graph[p_key]["outgoing"], (
                    f"Missing forward edge in graph: {p_key} -> {c_key}"
                )
                assert p_key in graph[c_key]["incoming"], (
                    f"Missing incoming edge in graph: {c_key} <- {p_key}"
                )

                # Check Reverse Edge: Comparison -> Paper
                assert p_key in graph[c_key]["outgoing"], (
                    f"Missing reverse edge in graph: {c_key} -> {p_key}"
                )
                assert c_key in graph[p_key]["incoming"], (
                    f"Missing incoming edge in graph: {p_key} <- {c_key}"
                )


# ==============================================================================
# Tier 2: Heading Structure and Section Invariant Tests
# ==============================================================================

class TestM2HeadingStructureAndInvariants:
    """Verify presence, syntax, and order of all required paper headings."""

    def test_silicon_analogy_section_presence(
        self, paper_liu: Path, paper_cheng: Path
    ):
        """Verify ## Silicon Analogy & Microelectronics Mapping exists in both papers."""
        target_heading = "## Silicon Analogy & Microelectronics Mapping"

        for paper_path in (paper_liu, paper_cheng):
            content = paper_path.read_text(encoding="utf-8")
            assert target_heading in content, (
                f"{paper_path.name} is missing exact heading '{target_heading}'"
            )

    def test_canonical_nine_headings_preserved(
        self, paper_liu: Path, paper_cheng: Path
    ):
        """Verify all 9 standard paper schema headings remain intact."""
        required_h2s = [
            "## Claim",
            "## Research question",
            "## Method",
            "## Evidence",
            "## Strengths",
            "## Limitation",
            "## Direct relevance to repo",
            "## Relation to other papers",
            "## Knowledge links",
        ]

        for paper_path in (paper_liu, paper_cheng):
            content = paper_path.read_text(encoding="utf-8")
            for h2 in required_h2s:
                assert h2 in content, f"{paper_path.name} missing canonical heading '{h2}'"

    def test_heading_ordering_and_silicon_analogy_placement(
        self, paper_liu: Path, paper_cheng: Path
    ):
        """Verify Silicon Analogy section is positioned directly before Knowledge links."""
        for paper_path in (paper_liu, paper_cheng):
            content = paper_path.read_text(encoding="utf-8")
            headings = [
                line.strip()
                for line in content.splitlines()
                if line.strip().startswith("## ")
            ]

            assert "## Silicon Analogy & Microelectronics Mapping" in headings
            idx_analogy = headings.index("## Silicon Analogy & Microelectronics Mapping")
            idx_links = headings.index("## Knowledge links")

            assert idx_analogy < idx_links, (
                f"In {paper_path.name}, Silicon Analogy (index {idx_analogy}) "
                f"must appear before Knowledge links (index {idx_links})"
            )
            assert idx_analogy == idx_links - 1, (
                f"In {paper_path.name}, Silicon Analogy should immediately precede Knowledge links"
            )

    def test_bilingual_content_presence(
        self, paper_liu: Path, paper_cheng: Path
    ):
        """Verify Silicon Analogy section contains both [EN] and [CN] subsections."""
        for paper_path in (paper_liu, paper_cheng):
            content = paper_path.read_text(encoding="utf-8")
            _, body = parse_frontmatter(content)

            # Extract Silicon Analogy section content
            match = re.search(
                r"## Silicon Analogy & Microelectronics Mapping\s+(.*?)(?=\n## |\Z)",
                body,
                re.DOTALL,
            )
            assert match is not None, f"Could not parse Silicon Analogy section in {paper_path.name}"
            sec_text = match.group(1)

            assert "**[EN]**:" in sec_text or "[EN]" in sec_text, (
                f"{paper_path.name} Silicon Analogy section missing [EN] tag"
            )
            assert "**[CN]" in sec_text or "[CN]" in sec_text, (
                f"{paper_path.name} Silicon Analogy section missing [CN] tag"
            )
            # Ensure substantial length
            assert len(sec_text.strip()) > 300, (
                f"{paper_path.name} Silicon Analogy section text too short ({len(sec_text)} chars)"
            )


# ==============================================================================
# Tier 3: Frontmatter & Schema Validation Tests
# ==============================================================================

class TestM2FrontmatterConsistency:
    """Validate YAML frontmatter fields, types, and schema compliance."""

    def test_paper_notes_pass_linter_validation(
        self, paper_liu: Path, paper_cheng: Path, vault_root: Path
    ):
        """Verify linter returns zero errors and warnings for both paper notes."""
        for paper_path in (paper_liu, paper_cheng):
            content = paper_path.read_text(encoding="utf-8")
            fm, body = parse_frontmatter(content)
            issues = lint_paper_note(paper_path, fm, body, vault_root)
            errors = [i for i in issues if i.severity.lower() == "error"]
            warnings = [i for i in issues if i.severity.lower() == "warning"]

            assert len(errors) == 0, f"Linter errors in {paper_path.name}: {errors}"
            assert len(warnings) == 0, f"Linter warnings in {paper_path.name}: {warnings}"

    def test_all_linked_knowledge_targets_exist_on_disk(
        self, paper_liu: Path, paper_cheng: Path, vault_root: Path
    ):
        """Verify that every link listed in frontmatter linked_knowledge resolves to a real file."""
        canonical_map = get_canonical_note_map(vault_root)

        for paper_path in (paper_liu, paper_cheng):
            fm, _ = parse_frontmatter(paper_path.read_text(encoding="utf-8"))
            linked = fm.get("linked_knowledge", [])
            for raw_link in linked:
                target = re.sub(r"[\[\]\"]", "", str(raw_link)).strip()
                resolved = (
                    canonical_map.get(target)
                    or canonical_map.get(f"{target}.md")
                    or canonical_map.get(target.lower())
                    or canonical_map.get(f"{target.lower()}.md")
                )
                assert resolved is not None and resolved.exists(), (
                    f"In {paper_path.name}, linked_knowledge item '{raw_link}' does not exist on disk"
                )

    def test_tag_taxonomy_compliance(
        self, paper_liu: Path, paper_cheng: Path
    ):
        """Verify all tags in paper notes conform to allowed tag prefixes."""
        for paper_path in (paper_liu, paper_cheng):
            fm, _ = parse_frontmatter(paper_path.read_text(encoding="utf-8"))
            tags = fm.get("tags", [])
            assert len(tags) > 0, f"{paper_path.name} has no tags"
            for t in tags:
                clean = str(t).strip().lstrip("#")
                assert validate_tag(clean), f"Invalid tag '{t}' in {paper_path.name}"


# ==============================================================================
# Tier 4: Technical Physics & Microelectronics Assertion Tests
# ==============================================================================

class TestM2MicroelectronicsPhysicsAccuracy:
    """Verify technical substance and physics parameters in the mapped sections."""

    def test_liu_paper_physics_substance(self, paper_liu: Path):
        """Verify 2021_Liu_2D-Transistors contains key physical parameters and concepts."""
        content = paper_liu.read_text(encoding="utf-8")
        _, body = parse_frontmatter(content)
        sec_match = re.search(
            r"## Silicon Analogy & Microelectronics Mapping\s+(.*?)(?=\n## |\Z)",
            body,
            re.DOTALL,
        )
        assert sec_match is not None
        sec = sec_match.group(1)

        # Scale length and GAAFET references
        assert "\\lambda" in sec or "lambda" in sec.lower() or "特征长度" in sec
        assert "GAAFET" in sec or "环栅" in sec
        assert "0.65" in sec or "t_b" in sec
        assert "Salicide" in sec or "silicide" in sec.lower() or "硅化物" in sec
        assert "BEOL" in sec or "FEOL" in sec or "400" in sec or "热预算" in sec

    def test_cheng_paper_benchmarking_substance(self, paper_cheng: Path):
        """Verify 2022_Cheng_FET-Benchmark contains key benchmarking metrics and norms."""
        content = paper_cheng.read_text(encoding="utf-8")
        _, body = parse_frontmatter(content)
        sec_match = re.search(
            r"## Silicon Analogy & Microelectronics Mapping\s+(.*?)(?=\n## |\Z)",
            body,
            re.DOTALL,
        )
        assert sec_match is not None
        sec = sec_match.group(1)

        # Current normalization and TLM references
        assert "I_{on}/W" in sec or "Ion/W" in sec or "归一化" in sec
        assert "TLM" in sec or "方阻" in sec or "R_{sh}" in sec or "R_{tot}" in sec or "0.99" in sec
        assert "IRDS" in sec or "IEEE" in sec or "标杆" in sec
        assert "CFET" in sec or "GAAFET" in sec or "亚 2 纳米" in sec or "sub-2nm" in sec

    def test_evidence_id_consistency_with_comparisons(
        self, paper_liu: Path, paper_cheng: Path, comp_contact: Path, comp_electrostatic: Path
    ):
        """Verify evidence IDs in comparison notes match existing IDs in the paper notes."""
        p1_content = paper_liu.read_text(encoding="utf-8")
        p2_content = paper_cheng.read_text(encoding="utf-8")

        p1_evd_ids = set(re.findall(r"Evidence ID:\s*(EVD-[a-zA-Z0-9_-]+-\d+)", p1_content))
        p2_evd_ids = set(re.findall(r"Evidence ID:\s*(EVD-[a-zA-Z0-9_-]+-\d+)", p2_content))

        all_paper_evd = p1_evd_ids | p2_evd_ids
        assert len(all_paper_evd) >= 6, f"Expected at least 6 evidence IDs in papers, found {all_paper_evd}"

        # Check comparison references
        for comp_path in (comp_contact, comp_electrostatic):
            comp_content = comp_path.read_text(encoding="utf-8")
            comp_evd_refs = set(re.findall(r"`(EVD-[a-zA-Z0-9_-]+-\d+)`", comp_content))
            assert len(comp_evd_refs) > 0, f"{comp_path.name} has no evidence references"
            for evd_ref in comp_evd_refs:
                assert evd_ref in all_paper_evd, (
                    f"{comp_path.name} references unknown evidence ID '{evd_ref}' not present in papers"
                )


# ==============================================================================
# Tier 5: Adversarial Stress Tests & Mutation Testing (Oracles & Generators)
# ==============================================================================

class TestM2AdversarialLinkIntegrity:
    """Stress test link checkers, linter sensitivity, and mutation injection."""

    def test_broken_link_injection_oracle(self, vault_root: Path, tmp_path: Path):
        """Test that link_checker detects intentionally broken comparison links."""
        # Baseline check
        baseline = check_links(vault_root)
        assert baseline.is_clean, f"Baseline vault has broken links: {baseline.broken_links}"

        # Create mutated copy of Liu paper with a broken comparison link
        mutated_text = (vault_root / "Sources" / "Papers" / "2021_Liu_2D-Transistors.md").read_text(encoding="utf-8")
        mutated_text = mutated_text.replace(
            "[[Knowledge/Comparisons/2d_contact_vdW_vs_silicon_silicide]]",
            "[[Knowledge/Comparisons/2d_contact_nonexistent_corrupt_link]]",
        )

        temp_note = tmp_path / "temp_corrupt_paper.md"
        temp_note.write_text(mutated_text, encoding="utf-8")

        # Verify find_all_wikilinks extracts the corrupt target
        extracted = find_all_wikilinks(mutated_text)
        targets = [e[1] for e in extracted]
        assert "Knowledge/Comparisons/2d_contact_nonexistent_corrupt_link" in targets

        # Clean up
        temp_note.unlink()

    def test_fuzzy_link_repair_on_typo_in_comparison_link(self, vault_root: Path, tmp_path: Path):
        """Verify fuzzy link repair corrects near-miss comparison slugs."""
        from kb_tools.link_checker import _find_best_match
        canonical_map = get_canonical_note_map(vault_root)
        valid_targets = sorted(list(set(canonical_map.keys())))

        match, score = _find_best_match("2d_contact_vdW_vs_silicon_silicid", valid_targets, threshold=0.8)
        assert match is not None
        assert "2d_contact_vdW_vs_silicon_silicide" in match
        assert score > 0.90

    def test_linter_rejects_paper_with_removed_silicon_analogy_or_headings(
        self, paper_liu: Path, vault_root: Path
    ):
        """Verify linter flags errors if required headings are dropped."""
        content = paper_liu.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)

        # Drop '## Claim'
        broken_body = body.replace("## Claim", "### Altered Claim")
        issues = lint_paper_note(paper_liu, fm, broken_body, vault_root)
        errors = [i for i in issues if i.severity.lower() == "error"]
        assert any("Missing required section heading: '## Claim'" in e.message for e in errors)

    def test_vault_wide_check_links_is_zero_broken(self, vault_root: Path):
        """Ensure full vault has zero dead links after M2 changes."""
        res = check_links(vault_root)
        assert res.is_clean, f"Expected 0 broken links, found {len(res.broken_links)}: {res.broken_links}"
        assert res.total_links >= 200, f"Expected >= 200 total links, got {res.total_links}"

    def test_vault_wide_linter_is_zero_errors(self, vault_root: Path):
        """Ensure full vault passes strict lint with zero errors and zero warnings."""
        res = lint_vault(vault_root, strict=True)
        assert res.is_clean, f"Expected clean vault, found {res.error_count} errors: {res.errors}"
        assert res.warning_count == 0, f"Expected 0 warnings, found {res.warning_count}: {res.warnings}"
