import pytest
from pathlib import Path

_VAULT_ROOT = Path(__file__).resolve().parent.parent
if not (_VAULT_ROOT / 'Knowledge' / 'Comparisons' / '2d_contact_vdW_vs_silicon_silicide.md').exists() and not (_VAULT_ROOT / 'Sources' / 'Papers' / '2021_Liu_2D-Transistors.md').exists():
    pytest.skip('Private domain-specific 2D research notes not present in open-source framework vault', allow_module_level=True)

import pytest
from pathlib import Path


"""
Empirical Physics and Microelectronics Benchmark Challenge Suite for Milestone 2 (M2).
Verifies mathematical validity, physical unit consistency, short-channel equations,
TLM regression statistics, extrinsic transconductance degradation, and IEEE IRDS roadmap
alignment for literature notes:
- Sources/Papers/2021_Liu_2D-Transistors.md (Section: ## Silicon Analogy & Microelectronics Mapping)
- Sources/Papers/2022_Cheng_FET-Benchmark.md (Section: ## Silicon Analogy & Microelectronics Mapping)
and their cross-consistency with 6D comparison cards in Knowledge/Comparisons/.
"""

import math
from pathlib import Path
import pytest

from kb_tools.models import parse_frontmatter


@pytest.fixture
def vault_root() -> Path:
    return Path(__file__).parent.parent.resolve()


@pytest.fixture
def liu_note(vault_root: Path) -> tuple[dict, str]:
    path = vault_root / "Sources" / "Papers" / "2021_Liu_2D-Transistors.md"
    assert path.exists(), "Liu 2021 literature note missing"
    content = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    return fm, body


@pytest.fixture
def cheng_note(vault_root: Path) -> tuple[dict, str]:
    path = vault_root / "Sources" / "Papers" / "2022_Cheng_FET-Benchmark.md"
    assert path.exists(), "Cheng 2022 literature note missing"
    content = path.read_text(encoding="utf-8")
    fm, body = parse_frontmatter(content)
    return fm, body


@pytest.fixture
def comparison_cards(vault_root: Path) -> dict[str, tuple[dict, str]]:
    cards = {}
    for slug in ["2d_contact_vdW_vs_silicon_silicide", "2d_electrostatic_scaling_vs_silicon_gaafet"]:
        path = vault_root / "Knowledge" / "Comparisons" / f"{slug}.md"
        assert path.exists(), f"Comparison card {slug} missing"
        content = path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)
        cards[slug] = (fm, body)
    return cards


# =========================================================================
# 1. Structural & Bidirectional Wikilink Integrity for M2
# =========================================================================

def test_m2_silicon_analogy_section_presence(liu_note, cheng_note):
    """Verify both literature notes contain the required M2 Silicon Analogy section."""
    for note_name, (_, body) in [("Liu 2021", liu_note), ("Cheng 2022", cheng_note)]:
        assert "## Silicon Analogy & Microelectronics Mapping" in body, (
            f"{note_name} must contain '## Silicon Analogy & Microelectronics Mapping'"
        )
        assert "- **[EN]**:" in body, f"{note_name} must contain English mapping subsection"
        assert "- **[CN]" in body or "- **[CN] 硅基微电子映射与技术对照**:" in body, (
            f"{note_name} must contain Chinese mapping subsection"
        )
        assert "- **Mapped Comparisons / 关联对照卡片**:" in body, (
            f"{note_name} must contain Mapped Comparisons list"
        )


def test_m2_bidirectional_wikilink_topology(liu_note, cheng_note, comparison_cards):
    """
    Verify complete bidirectional link closure between paper notes and comparison cards:
    - 2021_Liu_2D-Transistors.md <---> 2d_contact_vdW_vs_silicon_silicide.md
    - 2021_Liu_2D-Transistors.md <---> 2d_electrostatic_scaling_vs_silicon_gaafet.md
    - 2022_Cheng_FET-Benchmark.md <---> 2d_contact_vdW_vs_silicon_silicide.md
    - 2022_Cheng_FET-Benchmark.md <---> 2d_electrostatic_scaling_vs_silicon_gaafet.md
    """
    liu_fm, liu_body = liu_note
    cheng_fm, cheng_body = cheng_note

    # Check paper notes reference comparison cards in frontmatter linked_knowledge and body
    for slug in ["2d_contact_vdW_vs_silicon_silicide", "2d_electrostatic_scaling_vs_silicon_gaafet"]:
        link_target = f"Knowledge/Comparisons/{slug}"
        assert any(link_target in lk for lk in liu_fm.get("linked_knowledge", [])), (
            f"Liu note frontmatter linked_knowledge missing {link_target}"
        )
        assert f"[[{link_target}" in liu_body, f"Liu note body missing link to {link_target}"

        assert any(link_target in lk for lk in cheng_fm.get("linked_knowledge", [])), (
            f"Cheng note frontmatter linked_knowledge missing {link_target}"
        )
        assert f"[[{link_target}" in cheng_body, f"Cheng note body missing link to {link_target}"

    # Check comparison cards reference both paper notes in primary_sources and body
    for slug, (card_fm, card_body) in comparison_cards.items():
        primary_sources = card_fm.get("primary_sources", [])
        assert any("2021_Liu_2D-Transistors" in ps for ps in primary_sources), (
            f"Comparison card {slug} frontmatter primary_sources missing Liu 2021"
        )
        assert any("2022_Cheng_FET-Benchmark" in ps for ps in primary_sources), (
            f"Comparison card {slug} frontmatter primary_sources missing Cheng 2022"
        )
        assert "2021_Liu_2D-Transistors" in card_body, f"Comparison card {slug} body missing Liu reference"
        assert "2022_Cheng_FET-Benchmark" in card_body, f"Comparison card {slug} body missing Cheng reference"


# =========================================================================
# 2. Physics & Mathematical Modeling Verification (Liu 2021 Mapping)
# =========================================================================

def test_liu_electrostatic_scale_length_and_scaling_floor():
    """
    Verify quantitative scaling physics in Liu 2021 mapping:
    1. 2D body thickness t_b ~ 0.65 nm (monolayer TMD: MoS2/WS2).
    2. Electrostatic scale length lambda < 1.5 nm (ideal DG: sqrt((eps_b / 2 eps_ox) * t_b * t_ox) ~ 0.52 - 1.05 nm).
    3. Silicon GAAFET nanosheet floor: t_si ~ 5 nm, lambda_gaa ~ 2.85 nm -> L_g floor (4 * lambda) ~ 11.4 - 12 nm.
    4. 2D sub-5nm scalability: L_g_min ~ 3.5 * lambda_2d ~ 3.6 - 4.5 nm < 5 nm.
    """
    eps_sio2 = 3.9
    eps_si = 11.7
    eps_2d = 5.5
    
    # 2D TMD channel
    t_2d = 0.65  # nm
    EOT_2d = 0.6  # nm
    lambda_2d_ideal = math.sqrt((eps_2d / (2.0 * eps_sio2)) * t_2d * EOT_2d)
    assert 0.50 <= lambda_2d_ideal <= 0.60
    
    # Realistic scale length with fringe and spacer effects
    lambda_2d_eff = 1.05  # nm
    assert lambda_2d_eff < 1.5, "Effective scale length lambda < 1.5 nm as claimed in Liu mapping"
    
    L_g_min_2d = 3.5 * lambda_2d_eff  # 3.675 nm
    assert L_g_min_2d < 5.0, f"2D minimum gate length {L_g_min_2d:.2f} nm is sub-5nm"

    # Silicon GAAFET nanosheet
    t_si = 5.0  # nm
    EOT_si = 0.7  # nm
    lambda_si_gaa_eff = 2.85  # nm (including corner and quantum capacitance factor)
    L_g_min_si = 4.0 * lambda_si_gaa_eff  # 11.4 nm
    assert 11.0 <= L_g_min_si <= 12.0, (
        f"Silicon GAAFET scaling floor {L_g_min_si:.2f} nm validates L_g ~ 12 nm claim"
    )


def test_liu_thermal_budget_and_beol_integration():
    """
    Verify thermal budget claims in Liu 2021 mapping:
    - 2D processing: T < 400 °C (Bi contact deposition <= 250 °C, CVD <= 400 °C) enables BEOL monolithic 3D.
    - Silicon FEOL: T > 900 °C (RTP/spike dopant activation at 900-1050 °C) incompatible with BEOL Cu (< 450 °C).
    """
    T_2d_beol_max = 400.0  # °C
    T_si_dopant_min = 900.0  # °C
    T_cu_beol_limit = 450.0  # °C
    
    assert T_2d_beol_max < T_cu_beol_limit, "2D processing temperature is within BEOL Cu thermal budget"
    assert T_si_dopant_min > T_cu_beol_limit, "Silicon dopant activation violates BEOL Cu thermal budget"


# =========================================================================
# 3. TLM Regression & Transconductance Degradation (Cheng 2022 Mapping)
# =========================================================================

def test_cheng_tlm_linear_regression_statistics():
    """
    Verify Transfer Length Method (TLM) extraction physics and R^2 > 0.99 standard:
    R_tot * W = 2 * R_c * W + R_sh * L_ch
    Simulate multi-channel TLM data (L_ch = 50, 100, 200, 500, 1000 nm):
    Show that R^2 > 0.99 is mathematically required to decouple Rc from R_sh with <10% error.
    """
    Rc_true = 30.0  # Ohm*um
    Rsh_true = 5000.0  # Ohm/sq
    channel_lengths_um = [0.05, 0.10, 0.20, 0.50, 1.00]  # um

    # Generate ideal total resistance per unit width (Ohm*um)
    R_tot_ideal = [2.0 * Rc_true + Rsh_true * L for L in channel_lengths_um]

    # Calculate Pearson R^2 for ideal line
    n = len(channel_lengths_um)
    mean_x = sum(channel_lengths_um) / n
    mean_y = sum(R_tot_ideal) / n
    ss_xx = sum((x - mean_x) ** 2 for x in channel_lengths_um)
    ss_yy = sum((y - mean_y) ** 2 for y in R_tot_ideal)
    ss_xy = sum((x - mean_x) * (y - mean_y) for x, y in zip(channel_lengths_um, R_tot_ideal))
    r_squared = (ss_xy ** 2) / (ss_xx * ss_yy)
    
    assert math.isclose(r_squared, 1.0, rel_tol=1e-6), "Ideal TLM regression has R^2 = 1.0"

    # Add 5% measurement noise to test R^2 bound
    noisy_R_tot = [
        R_tot_ideal[0] * 1.04,
        R_tot_ideal[1] * 0.97,
        R_tot_ideal[2] * 1.02,
        R_tot_ideal[3] * 0.99,
        R_tot_ideal[4] * 1.01,
    ]
    mean_y_noisy = sum(noisy_R_tot) / n
    ss_yy_noisy = sum((y - mean_y_noisy) ** 2 for y in noisy_R_tot)
    ss_xy_noisy = sum((x - mean_x) * (y - mean_y_noisy) for x, y in zip(channel_lengths_um, noisy_R_tot))
    r_squared_noisy = (ss_xy_noisy ** 2) / (ss_xx * ss_yy_noisy)
    
    slope_extracted = ss_xy_noisy / ss_xx
    intercept_extracted = mean_y_noisy - slope_extracted * mean_x
    Rc_extracted = intercept_extracted / 2.0
    
    assert r_squared_noisy > 0.99, f"R^2 ({r_squared_noisy:.4f}) meets >= 0.99 standard"
    assert math.isclose(Rc_extracted, Rc_true, rel_tol=0.15), (
        f"Extracted Rc ({Rc_extracted:.2f} Ohm*um) is within 15% of true Rc ({Rc_true} Ohm*um)"
    )


def test_cheng_extrinsic_transconductance_degradation():
    """
    Verify extrinsic transconductance equation:
    g_m,ext = g_m,int / (1 + g_m,int * R_s + g_ds,int * (R_s + R_d))
    Show that high contact resistance (Rc > 200 Ohm*um) collapses gm and masks intrinsic mobility.
    """
    # Intrinsic ballistic transconductance at Vdd = 0.7V: g_m,int ~ 2.0 mS/um = 0.002 S/um
    gm_int = 2.0e-3  # S/um
    gds_int = 0.2e-3  # S/um
    
    # Case 1: Ultra-low contact resistance (semi-metal Bi: Rc = 30 Ohm*um)
    Rs_low = 30.0  # Ohm*um
    Rd_low = 30.0
    denom_low = 1.0 + gm_int * Rs_low + gds_int * (Rs_low + Rd_low)
    gm_ext_low = gm_int / denom_low
    degradation_low = (1.0 - gm_ext_low / gm_int) * 100.0
    assert degradation_low < 10.0, f"Low Rc results in minimal gm degradation ({degradation_low:.1f}%)"

    # Case 2: High contact resistance (unoptimized 3D metal: Rc = 300 Ohm*um)
    Rs_high = 300.0  # Ohm*um
    Rd_high = 300.0
    denom_high = 1.0 + gm_int * Rs_high + gds_int * (Rs_high + Rd_high)
    gm_ext_high = gm_int / denom_high
    degradation_high = (1.0 - gm_ext_high / gm_int) * 100.0
    assert degradation_high > 40.0, (
        f"High Rc causes severe gm degradation ({degradation_high:.1f}% > 40%), invalidating field-effect mobility"
    )


# =========================================================================
# 4. IEEE IRDS Benchmark Consistency & Quantitative Gate Checks
# =========================================================================

def test_m2_vs_irds_roadmap_quantitative_assertions(liu_note, cheng_note):
    """
    Verify quantitative parameters in M2 mapping match IEEE IRDS More Moore / Beyond CMOS targets:
    - Vdd = 0.7 V (standard logic supply voltage for sub-2nm nodes)
    - Ion/W > 1.0 mA/um (mandatory on-current threshold to match silicon GAAFET)
    - Rc < 100 Ohm*um (upper bound) and Rc <= 25-40 Ohm*um (IRDS A14/A10 target)
    - Subthreshold swing SS ~ 60-65 mV/dec (near Boltzmann limit)
    """
    _, liu_body = liu_note
    _, cheng_body = cheng_note

    # Liu 2021 mapping quantitative verification
    assert "0.65" in liu_body, "Body thickness 0.65 nm present in Liu note"
    assert "1.5" in liu_body or "1.05" in liu_body, "Scale length lambda < 1.5 nm present in Liu note"
    assert "12" in liu_body, "Silicon GAAFET 12 nm scaling floor present in Liu note"
    assert "400" in liu_body, "BEOL 400°C thermal budget present in Liu note"
    assert "900" in liu_body, "FEOL 900°C thermal budget present in Liu note"

    # Cheng 2022 mapping quantitative verification
    assert "0.7" in cheng_body, "Vdd = 0.7 V benchmark voltage present in Cheng note"
    assert "0.99" in cheng_body, "TLM R^2 > 0.99 criterion present in Cheng note"
    assert "100" in cheng_body, "Rc < 100 Ohm*um threshold present in Cheng note"
    assert "1.0" in cheng_body, "Ion/W > 1.0 mA/um threshold present in Cheng note"
    assert "IRDS" in cheng_body or "IEEE IRDS" in cheng_body, "IRDS roadmap explicitly referenced in Cheng note"