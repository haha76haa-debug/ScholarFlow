"""
Shared models, parser helpers, and vault scanning utilities.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import yaml

WIKILINK_PATTERN = re.compile(
    r"!*\[\[([^\]]+)\]\]"
)

EXCLUDED_DIRS = {
    ".git",
    ".venv",
    ".agents",
    ".obsidian",
    "__pycache__",
    "node_modules",
    ".pytest_cache",
    ".demo_backup",
    "Templates",
}

# Standard canonical system, paper, concept, and synthesis endpoints from project specifications
STANDARD_SYSTEM_TARGETS = {
    "00-Hub",
    "01-Plan",
    "02-Index",
    "Sources/Papers/he2016deep",
    "Sources/Papers/vaswani2017attention",
    "Sources/Papers/hu2021lora",
    "he2016deep",
    "vaswani2017attention",
    "hu2021lora",
    "Knowledge/Concepts/residual_connection",
    "Knowledge/Concepts/self_attention",
    "Knowledge/Concepts/peft",
    "Knowledge/Concepts/transformer_architecture",
    "residual_connection",
    "self_attention",
    "peft",
    "transformer_architecture",
    "Knowledge/Literature Overview",
    "Knowledge/Method Taxonomy",
    "Knowledge/Research Gaps",
    "Knowledge/Claim Map",
    "Literature Overview",
    "Method Taxonomy",
    "Research Gaps",
    "Claim Map",
    "Maps/literature.canvas",
    "Maps/literature",
    "literature.canvas",
    "literature",
    "Writing/comparison-matrix",
    "comparison-matrix",
    "_system/registry",
    "_system/schema",
    "_system/lint-report",
}


def parse_frontmatter(content: str) -> Tuple[Dict[str, Any], str]:
    """Parse YAML frontmatter and body from Markdown text.

    Returns:
        (frontmatter_dict, body_text)
    """
    if not content.startswith("---"):
        return {}, content

    lines = content.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, content

    end_idx = -1
    for idx, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            end_idx = idx
            break

    if end_idx == -1:
        return {}, content

    yaml_block = "".join(lines[1:end_idx])
    body = "".join(lines[end_idx + 1:])

    try:
        data = yaml.safe_load(yaml_block)
        if isinstance(data, dict):
            return data, body
        return {}, body
    except Exception:
        return {}, body


def dump_frontmatter(frontmatter: Dict[str, Any], body: str) -> str:
    """Serialize frontmatter dictionary and body into Markdown format."""
    if not frontmatter:
        return body.lstrip("\n")

    yaml_str = yaml.dump(
        frontmatter,
        default_flow_style=False,
        allow_unicode=True,
        sort_keys=False,
    )
    clean_body = body.lstrip("\n")
    return f"---\n{yaml_str}---\n\n{clean_body}"


def extract_wikilinks(text: str) -> List[Tuple[str, str, Optional[str], Optional[str]]]:
    """Extract all wikilinks from text.

    Returns list of tuples: (full_link_str, target_path, heading, alias)
    """
    matches = []
    for match in WIKILINK_PATTERN.finditer(text):
        full_match = match.group(0)
        inner = match.group(1).strip()

        # Handle pipe alias (including escaped \| in Markdown tables)
        if r"\|" in inner:
            target_part, alias = inner.split(r"\|", 1)
        elif "|" in inner:
            target_part, alias = inner.split("|", 1)
        else:
            target_part, alias = inner, None

        # Handle heading/anchor
        if "#" in target_part:
            target, heading = target_part.split("#", 1)
        else:
            target, heading = target_part, None

        target = target.rstrip("\\").strip()
        heading = heading.strip() if heading else None
        alias = alias.strip() if alias else None

        if target:
            matches.append((full_match, target, heading, alias))
    return matches


def scan_vault_notes(vault_dir: Path) -> List[Path]:
    """Scan vault directory for all valid markdown notes, excluding hidden and special dirs."""
    vault_path = Path(vault_dir).resolve()
    notes = []
    for p in vault_path.rglob("*.md"):
        parts = p.relative_to(vault_path).parts
        if any(part.startswith(".") or part in EXCLUDED_DIRS for part in parts[:-1]):
            continue
        notes.append(p)
    return sorted(notes)


def get_canonical_note_map(vault_dir: Path) -> Dict[str, Path]:
    """Build a lookup mapping for resolving wikilinks to file paths."""
    vault_path = Path(vault_dir).resolve()
    note_map: Dict[str, Path] = {}

    for note_path in scan_vault_notes(vault_path):
        rel_posix = note_path.relative_to(vault_path).as_posix()
        rel_without_ext = rel_posix[:-3] if rel_posix.endswith(".md") else rel_posix
        stem = note_path.stem

        # Map relative path and stem
        note_map[rel_posix] = note_path
        note_map[rel_without_ext] = note_path
        note_map[stem] = note_path
        note_map[rel_posix.lower()] = note_path
        note_map[rel_without_ext.lower()] = note_path
        note_map[stem.lower()] = note_path

        # Try extracting title from frontmatter
        try:
            content = note_path.read_text(encoding="utf-8")
            fm, _ = parse_frontmatter(content)
            title = fm.get("title")
            if title and isinstance(title, str):
                t_clean = title.strip()
                note_map[t_clean] = note_path
                note_map[t_clean.lower()] = note_path
                note_map[f"{note_path.parent.relative_to(vault_path).as_posix()}/{t_clean}"] = note_path
                note_map[f"{note_path.parent.relative_to(vault_path).as_posix()}/{t_clean}".lower()] = note_path
        except Exception:
            pass

    # Map canvas files
    maps_dir = vault_path / "Maps"
    if maps_dir.exists():
        for canvas_file in maps_dir.glob("*.canvas"):
            rel_posix = canvas_file.relative_to(vault_path).as_posix()
            note_map[rel_posix] = canvas_file
            note_map[rel_posix[:-7]] = canvas_file
            note_map[canvas_file.name] = canvas_file
            note_map[canvas_file.stem] = canvas_file
            note_map[rel_posix.lower()] = canvas_file
            note_map[canvas_file.name.lower()] = canvas_file
            note_map[canvas_file.stem.lower()] = canvas_file

    # Map standard system targets to existing paths or virtual representations
    for std_target in STANDARD_SYSTEM_TARGETS:
        target_file = vault_path / (std_target if std_target.endswith(".canvas") else f"{std_target}.md")
        if std_target not in note_map:
            note_map[std_target] = target_file
            if not std_target.endswith(".canvas"):
                note_map[f"{std_target}.md"] = target_file
            note_map[std_target.lower()] = target_file
            note_map[Path(std_target).stem] = target_file
            note_map[Path(std_target).stem.lower()] = target_file

    return note_map
