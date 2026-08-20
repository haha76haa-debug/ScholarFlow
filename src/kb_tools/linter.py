"""
Metadata, Schema, Tag Taxonomy, and Heading Linter for Obsidian Vault Notes.
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple

from kb_tools.models import (
    EXCLUDED_DIRS,
    get_canonical_note_map,
    parse_frontmatter,
    scan_vault_notes,
)

# Tag taxonomy regex patterns
ALLOWED_TAG_PREFIXES = ("type/", "topic/", "status/", "method/")
ALLOWED_STANDALONE_TAGS = {
    "knowledge",
    "concept",
    "paper",
    "synthesis",
    "overview",
    "taxonomy",
    "daily",
    "reading-log",
    "web-source",
    "tutorial",
    "transformer",
    "self-attention",
    "peft",
    "lora",
    "residual-learning",
    "computer-vision",
    "nlp",
    "deep-learning",
    "attention-mechanisms",
}

VALID_STATUSES = {
    "unread",
    "reading",
    "read",
    "to-review",
    "summarized",
    "active",
    "draft",
    "deprecated",
    "archived",
}

VALID_CLAIM_STRENGTHS = {"speculative", "observed", "supported", "strong"}

VALID_SOURCE_TYPES = {
    "full paper",
    "preprint",
    "conference paper",
    "journal article",
    "abstract-only",
    "webpage placeholder",
    "book",
    "book chapter",
    "thesis",
    "report",
    "dataset",
    "doc",
}


@dataclass
class LintIssue:
    file_path: str
    severity: str  # "error" or "warning"
    category: str
    message: str
    line: Optional[int] = None

    @property
    def file(self) -> str:
        return self.file_path

    def __str__(self) -> str:
        return f"[{self.severity.upper()}] {self.file_path}: {self.message}"


@dataclass
class LintResult:
    issues: List[LintIssue] = field(default_factory=list)
    total_files_scanned: int = 0
    passed_files: int = 0
    error_count: int = 0
    warning_count: int = 0

    @property
    def is_clean(self) -> bool:
        return self.error_count == 0

    @property
    def errors(self) -> List[LintIssue]:
        return [i for i in self.issues if i.severity.lower() == "error"]

    @property
    def warnings(self) -> List[LintIssue]:
        return [i for i in self.issues if i.severity.lower() == "warning"]

    def __iter__(self) -> Iterator[LintIssue]:
        return iter(self.issues)

    def __getitem__(self, item: str) -> Any:
        return self.to_dict().get(item)

    def get(self, key: str, default: Any = None) -> Any:
        data = self.to_dict()
        return data.get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "valid": self.is_clean,
            "total_files_scanned": self.total_files_scanned,
            "passed_files": self.passed_files,
            "error_count": self.error_count,
            "errors_count": self.error_count,
            "warning_count": self.warning_count,
            "warnings_count": self.warning_count,
            "is_clean": self.is_clean,
            "errors": [
                {
                    "file": issue.file_path,
                    "severity": issue.severity,
                    "category": issue.category,
                    "message": issue.message,
                    "line": issue.line,
                }
                for issue in self.errors
            ],
            "issues": [
                {
                    "file": issue.file_path,
                    "severity": issue.severity,
                    "category": issue.category,
                    "message": issue.message,
                    "line": issue.line,
                }
                for issue in self.issues
            ],
        }


def _normalize_heading(heading: str) -> str:
    """Normalize heading string for case-insensitive comparison."""
    return re.sub(r"\s+", " ", heading.strip().lower())


def _extract_headings(body: str) -> List[str]:
    """Extract all Markdown heading lines (e.g. '## Claim')."""
    headings = []
    for line in body.splitlines():
        trimmed = line.strip()
        if trimmed.startswith("#"):
            headings.append(trimmed)
    return headings


def validate_tag(tag: Any) -> bool:
    """Check whether tag adheres to taxonomy conventions."""
    if not isinstance(tag, str):
        return False
    clean_tag = tag.strip().lstrip("#")
    if not clean_tag or " " in clean_tag:
        return False
    if clean_tag in ALLOWED_STANDALONE_TAGS:
        return True
    if any(clean_tag.startswith(prefix) for prefix in ALLOWED_TAG_PREFIXES):
        parts = clean_tag.split("/", 1)
        if len(parts) < 2 or not parts[1]:
            return False
        subtag = parts[1]
        return bool(re.match(r"^[a-zA-Z0-9_\-]+(/[a-zA-Z0-9_\-]+)*$", subtag))
    if re.match(r"^[a-zA-Z0-9_\-]+$", clean_tag):
        return True
    return False


def validate_tag_taxonomy(
    note_path: Path, allowed_prefixes: Tuple[str, ...] = ALLOWED_TAG_PREFIXES
) -> Tuple[bool, List[str]]:
    """Validate all tags in a note against allowed taxonomy prefixes."""
    errors = []
    try:
        content = note_path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)
        tags = fm.get("tags", [])
        if isinstance(tags, list):
            for tag in tags:
                clean = str(tag).strip().lstrip("#")
                if not validate_tag(clean):
                    errors.append(f"Invalid tag syntax: '{tag}'")
                elif not (
                    clean in ALLOWED_STANDALONE_TAGS
                    or any(clean.startswith(p) for p in allowed_prefixes)
                ):
                    errors.append(f"Tag prefix not allowed: '{tag}'")
    except Exception as e:
        errors.append(str(e))
    return (len(errors) == 0, errors)


def validate_claim_promotion_gate(
    note_path: Path, vault_dir: Path
) -> Tuple[bool, List[str]]:
    """Validate claim promotion gate rules for a note."""
    errors = []
    try:
        content = note_path.read_text(encoding="utf-8")
        fm, body = parse_frontmatter(content)
        source_type = str(fm.get("source_type", "")).lower()
        claim_strength = str(fm.get("claim_strength", "")).lower()

        # Reject strong claims from weak/placeholder sources
        if source_type in ("webpage placeholder", "abstract-only") and claim_strength in ("supported", "strong"):
            errors.append(
                f"Weak source type '{source_type}' cannot promote '{claim_strength}' claims"
            )
    except Exception as e:
        errors.append(str(e))
    return (len(errors) == 0, errors)


def lint_paper_note(
    path: Path,
    frontmatter: Dict[str, Any],
    body: str,
    vault_dir: Path,
) -> List[LintIssue]:
    """Lint a canonical paper note in Sources/Papers/."""
    issues: List[LintIssue] = []
    rel_path = path.relative_to(vault_dir).as_posix()
    file_stem = path.stem

    # 1. Frontmatter Required Fields
    required_fields = [
        ("type", str, lambda v: v == "paper", "type must be 'paper'"),
        ("project", str, None, None),
        ("title", str, lambda v: len(str(v).strip()) > 0, "title cannot be empty"),
        ("citekey", str, lambda v: bool(re.match(r"^[a-zA-Z0-9_-]+$", str(v).strip())), "citekey must match ^[a-zA-Z0-9_-]+$"),
        ("zotero_key", str, None, None),
        ("status", str, lambda v: str(v).lower() in VALID_STATUSES, f"status must be one of {VALID_STATUSES}"),
        ("source_type", str, lambda v: str(v).lower() in VALID_SOURCE_TYPES, f"source_type must be one of {VALID_SOURCE_TYPES}"),
        ("claim_strength", str, lambda v: str(v).lower() in VALID_CLAIM_STRENGTHS, f"claim_strength must be one of {VALID_CLAIM_STRENGTHS}"),
        ("authors", list, lambda v: len(v) > 0, "authors must be a non-empty list"),
        ("year", int, lambda v: 1900 <= int(v) <= 2100, "year must be integer between 1900 and 2100"),
        ("linked_knowledge", list, None, "linked_knowledge must be a list"),
    ]

    for field_name, expected_type, validator, err_detail in required_fields:
        if field_name not in frontmatter:
            issues.append(
                LintIssue(
                    file_path=rel_path,
                    severity="error",
                    category="Frontmatter",
                    message=f"Missing required frontmatter key: '{field_name}'",
                )
            )
        else:
            val = frontmatter[field_name]
            if expected_type == int:
                if not isinstance(val, int) or isinstance(val, bool):
                    issues.append(
                        LintIssue(
                            file_path=rel_path,
                            severity="error",
                            category="Frontmatter",
                            message=f"Key '{field_name}' must be integer type, got {type(val).__name__}",
                        )
                    )
                elif validator and not validator(val):
                    issues.append(
                        LintIssue(
                            file_path=rel_path,
                            severity="error",
                            category="Frontmatter",
                            message=f"Key '{field_name}' has invalid value: '{val}' ({err_detail})",
                        )
                    )
            elif not isinstance(val, expected_type):
                issues.append(
                    LintIssue(
                        file_path=rel_path,
                        severity="error",
                        category="Frontmatter",
                        message=f"Key '{field_name}' must be of type {expected_type.__name__ if hasattr(expected_type, '__name__') else expected_type}, got {type(val).__name__}",
                    )
                )
            elif validator and not validator(val):
                issues.append(
                    LintIssue(
                        file_path=rel_path,
                        severity="error",
                        category="Frontmatter",
                        message=f"Key '{field_name}' has invalid enum or value: '{val}' ({err_detail})",
                    )
                )

    # Check citekey matches filename
    if "citekey" in frontmatter and isinstance(frontmatter["citekey"], str):
        citekey = str(frontmatter["citekey"]).strip()
        if citekey != file_stem:
            issues.append(
                LintIssue(
                    file_path=rel_path,
                    severity="error",
                    category="Citekey Mismatch",
                    message=f"Citekey '{citekey}' does not match file stem '{file_stem}'",
                )
            )

    # 2. Tag Taxonomy Validation
    tags = frontmatter.get("tags", [])
    if isinstance(tags, list):
        for tag in tags:
            tag_str = str(tag).strip().lstrip("#")
            if not validate_tag(tag_str):
                issues.append(
                    LintIssue(
                        file_path=rel_path,
                        severity="warning",
                        category="Tag Taxonomy",
                        message=f"Tag '{tag}' violates taxonomy naming convention",
                    )
                )

    # 3. Required Headings Check
    headings = _extract_headings(body)
    normalized_headings = [_normalize_heading(h) for h in headings]

    required_heading_specs = [
        ("## Claim", ["## claim"]),
        ("## Research question", ["## research question", "## research questions"]),
        ("## Method", ["## method", "## methodology"]),
        ("## Evidence", ["## evidence"]),
        ("## Strengths", ["## strengths", "## strength"]),
        ("## Limitation", ["## limitation", "## limitations"]),
        ("## Direct relevance to repo", ["## direct relevance to repo", "## direct relevance"]),
        ("## Relation to other papers", ["## relation to other papers", "## related work"]),
        ("## Knowledge links", ["## knowledge links", "## knowledge link"]),
    ]

    for display_name, variants in required_heading_specs:
        if not any(
            any(v in nh for v in variants) for nh in normalized_headings
        ):
            issues.append(
                LintIssue(
                    file_path=rel_path,
                    severity="error",
                    category="Heading Structure",
                    message=f"Missing required section heading: '{display_name}'",
                )
            )

    # 4. Evidence Record Block Check
    if any("## evidence" in nh for nh in normalized_headings):
        has_evd_id = bool(re.search(r"Evidence ID:\s*EVD-[a-zA-Z0-9_-]+-\d+", body, re.IGNORECASE))
        has_source = bool(re.search(r"Source:\s*\[\[", body, re.IGNORECASE))
        has_supports = bool(re.search(r"Supports:\s*\"?[^\n\"]+\"?", body, re.IGNORECASE))

        if not (has_evd_id and has_source and has_supports):
            issues.append(
                LintIssue(
                    file_path=rel_path,
                    severity="error",
                    category="Evidence Gate",
                    message="Evidence section has malformed or missing Evidence Record block (Evidence ID, Source, Supports)",
                )
            )

    return issues


def lint_concept_note(
    path: Path,
    frontmatter: Dict[str, Any],
    body: str,
    vault_dir: Path,
) -> List[LintIssue]:
    """Lint an atomic concept note in Knowledge/Concepts/."""
    issues: List[LintIssue] = []
    rel_path = path.relative_to(vault_dir).as_posix()

    required_fields = [
        ("type", str, lambda v: v == "concept", "type must be 'concept'"),
        ("project", str, None, None),
        ("title", str, lambda v: len(str(v).strip()) > 0, "title cannot be empty"),
        ("status", str, lambda v: str(v).lower() in VALID_STATUSES, f"status must be one of {VALID_STATUSES}"),
        ("claim_strength", str, lambda v: str(v).lower() in VALID_CLAIM_STRENGTHS, f"claim_strength must be one of {VALID_CLAIM_STRENGTHS}"),
        ("primary_sources", list, lambda v: len(v) > 0, "primary_sources must be a non-empty list"),
    ]

    for field_name, expected_type, validator, err_detail in required_fields:
        if field_name not in frontmatter:
            issues.append(
                LintIssue(
                    file_path=rel_path,
                    severity="error",
                    category="Frontmatter",
                    message=f"Missing required frontmatter key: '{field_name}'",
                )
            )
        else:
            val = frontmatter[field_name]
            if not isinstance(val, expected_type):
                issues.append(
                    LintIssue(
                        file_path=rel_path,
                        severity="error",
                        category="Frontmatter",
                        message=f"Key '{field_name}' must be of type {expected_type.__name__}, got {type(val).__name__}",
                    )
                )
            elif validator and not validator(val):
                issues.append(
                    LintIssue(
                        file_path=rel_path,
                        severity="error",
                        category="Frontmatter",
                        message=f"Key '{field_name}' has invalid value: '{val}' ({err_detail})",
                    )
                )

    headings = _extract_headings(body)
    normalized = [_normalize_heading(h) for h in headings]

    # Required: ## Definition
    if not any("## definition" in nh for nh in normalized):
        issues.append(
            LintIssue(
                file_path=rel_path,
                severity="error",
                category="Heading Structure",
                message="Missing required heading: '## Definition'",
            )
        )

    # Required: Formulation or Mechanism
    has_formulation = any(
        any(k in nh for k in ["formulation", "mechanism", "mathematical", "algorithmic"])
        for nh in normalized
    )
    if not has_formulation:
        issues.append(
            LintIssue(
                file_path=rel_path,
                severity="warning",
                category="Heading Structure",
                message="Missing formulation heading (e.g. '## Mathematical Formulation' or '## Mechanism')",
            )
        )

    return issues


def lint_synthesis_note(
    path: Path,
    frontmatter: Dict[str, Any],
    body: str,
    vault_dir: Path,
) -> List[LintIssue]:
    """Lint a knowledge synthesis note in Knowledge/."""
    issues: List[LintIssue] = []
    rel_path = path.relative_to(vault_dir).as_posix()

    required_fields = [
        ("title", str, None, None),
        ("status", str, lambda v: str(v).lower() in VALID_STATUSES, f"status must be one of {VALID_STATUSES}"),
        ("covered_papers", list, lambda v: len(v) > 0, "covered_papers must be a non-empty list"),
        ("key_themes", list, lambda v: len(v) > 0, "key_themes must be a non-empty list"),
    ]

    for field_name, expected_type, validator, err_detail in required_fields:
        if field_name not in frontmatter:
            issues.append(
                LintIssue(
                    file_path=rel_path,
                    severity="error",
                    category="Frontmatter",
                    message=f"Synthesis note missing required frontmatter key: '{field_name}'",
                )
            )
        else:
            val = frontmatter[field_name]
            if not isinstance(val, expected_type):
                issues.append(
                    LintIssue(
                        file_path=rel_path,
                        severity="error",
                        category="Frontmatter",
                        message=f"Key '{field_name}' must be of type {expected_type.__name__}",
                    )
                )

    return issues


def lint_file(file_path: Path, vault_dir: Optional[Path] = None) -> List[LintIssue]:
    """Lint a single file and return all identified issues."""
    path = Path(file_path).resolve()
    v_dir = Path(vault_dir).resolve() if vault_dir else path.parent
    rel_posix = path.relative_to(v_dir).as_posix() if path.is_relative_to(v_dir) else path.name

    if not path.exists():
        return [
            LintIssue(
                file_path=rel_posix,
                severity="error",
                category="File Not Found",
                message=f"File does not exist: {path}",
            )
        ]

    try:
        content = path.read_text(encoding="utf-8")
    except Exception as e:
        return [
            LintIssue(
                file_path=rel_posix,
                severity="error",
                category="File Read",
                message=f"Could not read file: {e}",
            )
        ]

    frontmatter, body = parse_frontmatter(content)
    if not frontmatter:
        if rel_posix.startswith("Sources/Papers/") or rel_posix.startswith("Knowledge/Concepts/"):
            return [
                LintIssue(
                    file_path=rel_posix,
                    severity="error",
                    category="YAML Frontmatter",
                    message="Missing or malformed YAML frontmatter",
                )
            ]
        return []

    note_type = str(frontmatter.get("type", "")).lower()

    if rel_posix.startswith("Sources/Papers/") or note_type == "paper":
        return lint_paper_note(path, frontmatter, body, v_dir)
    elif rel_posix.startswith("Knowledge/Concepts/") or note_type == "concept":
        return lint_concept_note(path, frontmatter, body, v_dir)
    elif note_type in ("literature-synthesis", "method-taxonomy", "research-gaps"):
        return lint_synthesis_note(path, frontmatter, body, v_dir)

    # General tag taxonomy check
    issues = []
    tags = frontmatter.get("tags", [])
    if isinstance(tags, list):
        for tag in tags:
            tag_str = str(tag).strip().lstrip("#")
            if not validate_tag(tag_str):
                issues.append(
                    LintIssue(
                        file_path=rel_posix,
                        severity="warning",
                        category="Tag Taxonomy",
                        message=f"Tag '{tag}' violates taxonomy naming convention",
                    )
                )
    return issues


def lint_vault(vault_dir: Path, strict: bool = False) -> LintResult:
    """Perform full comprehensive linting across the vault directory."""
    vault_path = Path(vault_dir).resolve()
    all_notes = scan_vault_notes(vault_path)
    result = LintResult(total_files_scanned=len(all_notes))

    seen_citekeys: Dict[str, str] = {}
    seen_zotero_keys: Dict[str, str] = {}

    for note_path in all_notes:
        rel_posix = note_path.relative_to(vault_path).as_posix()

        # Skip Templates directory, system reports, and index navigation files from strict paper lint
        if (
            rel_posix.startswith("Templates/")
            or rel_posix.startswith("_system/")
            or rel_posix in ("00-Hub.md", "01-Plan.md", "02-Index.md")
            or rel_posix.endswith("/index.md") or rel_posix.endswith("/z-Index.md") or rel_posix.endswith("/z_index.md")
        ):
            result.passed_files += 1
            continue

        try:
            content = note_path.read_text(encoding="utf-8")
        except Exception as e:
            result.issues.append(
                LintIssue(
                    file_path=rel_posix,
                    severity="error",
                    category="File Read",
                    message=f"Could not read file: {e}",
                )
            )
            continue

        frontmatter, body = parse_frontmatter(content)

        if not frontmatter:
            if rel_posix.startswith("Sources/Papers/") or rel_posix.startswith("Knowledge/Concepts/"):
                result.issues.append(
                    LintIssue(
                        file_path=rel_posix,
                        severity="error",
                        category="YAML Frontmatter",
                        message="Missing or malformed YAML frontmatter (must start with '---')",
                    )
                )
            else:
                result.passed_files += 1
            continue

        note_type = str(frontmatter.get("type", "")).lower()
        file_issues: List[LintIssue] = []

        # Duplicate key checks for papers
        if rel_posix.startswith("Sources/Papers/") or note_type == "paper":
            citekey = str(frontmatter.get("citekey", "")).strip()
            zotero_key = str(frontmatter.get("zotero_key", "")).strip()

            if citekey:
                if citekey in seen_citekeys:
                    file_issues.append(
                        LintIssue(
                            file_path=rel_posix,
                            severity="error",
                            category="Duplicate Key",
                            message=f"Duplicate citekey '{citekey}' also used by '{seen_citekeys[citekey]}'",
                        )
                    )
                else:
                    seen_citekeys[citekey] = rel_posix

            if zotero_key:
                if zotero_key in seen_zotero_keys:
                    file_issues.append(
                        LintIssue(
                            file_path=rel_posix,
                            severity="error",
                            category="Duplicate Key",
                            message=f"Duplicate zotero_key '{zotero_key}' also used by '{seen_zotero_keys[zotero_key]}'",
                        )
                    )
                else:
                    seen_zotero_keys[zotero_key] = rel_posix

            file_issues.extend(lint_paper_note(note_path, frontmatter, body, vault_path))

        elif rel_posix.startswith("Knowledge/Concepts/") or note_type == "concept":
            file_issues.extend(lint_concept_note(note_path, frontmatter, body, vault_path))

        elif note_type in ("literature-synthesis", "method-taxonomy", "research-gaps"):
            file_issues.extend(lint_synthesis_note(note_path, frontmatter, body, vault_path))

        # Check tag taxonomy on all notes
        tags = frontmatter.get("tags", [])
        if isinstance(tags, list):
            for tag in tags:
                tag_str = str(tag).strip().lstrip("#")
                if not validate_tag(tag_str):
                    file_issues.append(
                        LintIssue(
                            file_path=rel_posix,
                            severity="warning",
                            category="Tag Taxonomy",
                            message=f"Tag '{tag}' violates taxonomy naming convention",
                        )
                    )

        if file_issues:
            result.issues.extend(file_issues)
        else:
            result.passed_files += 1

    # Summarize counts
    result.error_count = sum(1 for i in result.issues if i.severity.lower() == "error")
    result.warning_count = sum(1 for i in result.issues if i.severity.lower() == "warning")

    return result


def format_lint_report_markdown(result: LintResult) -> str:
    """Generate Markdown report for _system/lint-report.md."""
    status_str = "PASSED" if result.is_clean else "FAILED"
    lines = [
        "# Knowledge Base Lint Report",
        "",
        f"- **Status**: {status_str}",
        f"- **Total Files Scanned**: {result.total_files_scanned}",
        f"- **Files Passed**: {result.passed_files}",
        f"- **Errors Found**: {result.error_count}",
        f"- **Warnings Found**: {result.warning_count}",
        "",
    ]

    if result.issues:
        lines.extend([
            "## Findings",
            "",
            "| Severity | Category | File | Message |",
            "|---|---|---|---|",
        ])
        for issue in result.issues:
            lines.append(
                f"| {issue.severity.upper()} | {issue.category} | `{issue.file_path}` | {issue.message} |"
            )
        lines.append("")
    else:
        lines.extend([
            "## Findings",
            "",
            "*Zero issues found. All notes conform strictly to schemas and contracts.*",
            "",
        ])

    return "\n".join(lines)


def write_lint_report(
    result: LintResult,
    vault_dir: Path,
    report_path: Optional[Path] = None,
) -> Path:
    """Write lint report to disk."""
    vault_path = Path(vault_dir).resolve()
    out_path = report_path if report_path else vault_path / "_system" / "lint-report.md"
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(format_lint_report_markdown(result), encoding="utf-8")
    return out_path
