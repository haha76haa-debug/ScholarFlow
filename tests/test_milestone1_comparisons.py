"""
Unit and regression tests for Milestone 1 (M1):
- comparison_schema.yaml contract validation
- comparison_template.md structure and placeholder compliance
- 6-dimensional comparison cards in Knowledge/Comparisons/
"""

from pathlib import Path
import pytest
import yaml

from kb_tools.models import parse_frontmatter, extract_wikilinks


@pytest.fixture
def vault_root() -> Path:
    return Path(__file__).parent.parent.resolve()


def test_comparison_schema_exists_and_valid(vault_root: Path):
    schema_file = vault_root / "_system" / "schemas" / "comparison_schema.yaml"
    assert schema_file.exists(), "comparison_schema.yaml must exist"
    
    with open(schema_file, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    
    assert schema["schema_name"] == "comparison_schema"
    assert schema["version"] == "1.0.0"
    assert "required_frontmatter" in schema
    assert "required_sections" in schema
    
    req_fm = schema["required_frontmatter"]
    for expected_key in [
        "type", "project", "title", "status", "claim_strength",
        "primary_sources", "silicon_reference_nodes", "dimensions_covered",
        "tags", "updated"
    ]:
        assert expected_key in req_fm, f"Missing required frontmatter key: {expected_key}"
    
    assert len(schema["required_sections"]) == 8


def test_comparison_template_structure(vault_root: Path):
    template_file = vault_root / "Templates" / "comparison_template.md"
    assert template_file.exists(), "comparison_template.md must exist"
    
    content = template_file.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    
    assert fm.get("type") == "comparison"
    assert fm.get("project") == "2d-semiconductors"
    assert fm.get("dimensions_covered") == [1, 2, 3, 4, 5, 6]
    assert "type/comparison" in fm.get("tags", [])
    assert "topic/silicon-analogy" in fm.get("tags", [])
    
    schema_file = vault_root / "_system" / "schemas" / "comparison_schema.yaml"
    with open(schema_file, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    
    for section in schema["required_sections"]:
        heading = section["heading"]
        assert heading.lower() in content.lower(), f"Template missing heading: {heading}"


def test_contact_comparison_card(vault_root: Path):
    card_path = vault_root / "Knowledge" / "Comparisons" / "2d_contact_vdW_vs_silicon_silicide.md"
    assert card_path.exists(), "2d_contact_vdW_vs_silicon_silicide.md must exist"
    
    content = card_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    
    # Frontmatter verification
    assert fm.get("type") == "comparison"
    assert fm.get("project") == "2d-semiconductors"
    assert fm.get("status") == "active"
    assert fm.get("claim_strength") == "strong"
    assert fm.get("dimensions_covered") == [1, 2, 3, 4, 5, 6]
    assert len(fm.get("primary_sources", [])) >= 2
    assert len(fm.get("silicon_reference_nodes", [])) >= 3
    assert "type/comparison" in fm.get("tags", [])
    assert "topic/silicon-analogy" in fm.get("tags", [])
    
    # Section headings verification
    schema_file = vault_root / "_system" / "schemas" / "comparison_schema.yaml"
    with open(schema_file, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    
    for section in schema["required_sections"]:
        heading = section["heading"]
        assert heading.lower() in content.lower(), f"Card missing heading: {heading}"
    
    # Physical and mathematical content
    assert "L_T = \\sqrt" in content or "L_T" in content
    assert "R_c" in content
    assert "\\Phi_B" in content or "Schottky" in content
    assert "MIGS" in content
    assert "Salicide" in content
    assert "IRDS" in content
    assert "EVD-2021_Liu_2D-Transistors" in content
    assert "EVD-2022_Cheng_FET-Benchmark" in content


def test_electrostatic_comparison_card(vault_root: Path):
    card_path = vault_root / "Knowledge" / "Comparisons" / "2d_electrostatic_scaling_vs_silicon_gaafet.md"
    assert card_path.exists(), "2d_electrostatic_scaling_vs_silicon_gaafet.md must exist"
    
    content = card_path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    
    # Frontmatter verification
    assert fm.get("type") == "comparison"
    assert fm.get("project") == "2d-semiconductors"
    assert fm.get("status") == "active"
    assert fm.get("claim_strength") == "strong"
    assert fm.get("dimensions_covered") == [1, 2, 3, 4, 5, 6]
    assert len(fm.get("primary_sources", [])) >= 2
    assert len(fm.get("silicon_reference_nodes", [])) >= 3
    assert "type/comparison" in fm.get("tags", [])
    assert "topic/silicon-analogy" in fm.get("tags", [])
    
    # Section headings verification
    schema_file = vault_root / "_system" / "schemas" / "comparison_schema.yaml"
    with open(schema_file, "r", encoding="utf-8") as f:
        schema = yaml.safe_load(f)
    
    for section in schema["required_sections"]:
        heading = section["heading"]
        assert heading.lower() in content.lower(), f"Card missing heading: {heading}"
    
    # Physical and mathematical content
    assert "\\lambda" in content
    assert "SS" in content or "Subthreshold Swing" in content
    assert "DIBL" in content
    assert "GAAFET" in content
    assert "CFET" in content
    assert "BSIM-CMG" in content
    assert "Landauer-Büttiker" in content or "Landauer" in content
    assert "IRDS" in content
    assert "EVD-2021_Liu_2D-Transistors" in content
    assert "EVD-2022_Cheng_FET-Benchmark" in content

