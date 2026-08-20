"""
Dead Link Detector, Wikilink Resolver, and Fuzzy Auto-Repair Engine.
"""

from __future__ import annotations

import difflib
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Set, Tuple

from kb_tools.models import (
    WIKILINK_PATTERN,
    extract_wikilinks,
    get_canonical_note_map,
    parse_frontmatter,
    scan_vault_notes,
)


@dataclass
class DeadLink:
    source_file: str
    target: str
    heading: Optional[str] = None
    alias: Optional[str] = None
    full_match: str = ""
    line_number: int = 0
    suggested_target: Optional[str] = None
    similarity_score: float = 0.0

    def __getitem__(self, key: str) -> Any:
        return getattr(self, key, None)

    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source_file,
            "source_file": self.source_file,
            "target": self.target,
            "heading": self.heading,
            "alias": self.alias,
            "line": self.line_number,
            "line_number": self.line_number,
            "suggestion": self.suggested_target,
            "suggested_target": self.suggested_target,
            "score": round(self.similarity_score, 3),
            "similarity_score": round(self.similarity_score, 3),
        }


@dataclass
class LinkCheckResult:
    total_links: int = 0
    resolved_links: int = 0
    broken_links: List[DeadLink] = field(default_factory=list)
    orphan_notes: List[str] = field(default_factory=list)
    dead_ends: List[str] = field(default_factory=list)

    @property
    def is_clean(self) -> bool:
        return len(self.broken_links) == 0

    def __iter__(self) -> Iterator[DeadLink]:
        return iter(self.broken_links)

    def __getitem__(self, key: str) -> Any:
        return self.to_dict().get(key)

    def get(self, key: str, default: Any = None) -> Any:
        return self.to_dict().get(key, default)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "total_links": self.total_links,
            "resolved_links": self.resolved_links,
            "broken_link_count": len(self.broken_links),
            "total_broken": len(self.broken_links),
            "orphan_count": len(self.orphan_notes),
            "dead_end_count": len(self.dead_ends),
            "is_clean": self.is_clean,
            "broken_links": [b.to_dict() for b in self.broken_links],
            "orphan_notes": self.orphan_notes,
            "dead_ends": self.dead_ends,
        }


def find_all_wikilinks(text: str) -> List[Tuple[str, str, Optional[str], Optional[str]]]:
    """Extract only Obsidian-style internal wikilinks, ignoring external http/https/zotero URLs."""
    raw_links = extract_wikilinks(text)
    filtered = []
    for full_match, target, heading, alias in raw_links:
        t_lower = target.strip().lower()
        if (
            t_lower.startswith("http://")
            or t_lower.startswith("https://")
            or t_lower.startswith("zotero://")
            or t_lower.startswith("mailto:")
        ):
            continue
        filtered.append((full_match, target, heading, alias))
    return filtered


def _find_best_match(
    target: str, valid_targets: List[str], threshold: float = 0.8
) -> Tuple[Optional[str], float]:
    """Find the best fuzzy match for a broken target."""
    clean_target = target.strip().lower().replace("-", "").replace("_", "")
    best_match = None
    best_score = 0.0

    for candidate in valid_targets:
        clean_cand = candidate.strip().lower().replace("-", "").replace("_", "")
        score = difflib.SequenceMatcher(None, clean_target, clean_cand).ratio()
        if score > best_score:
            best_score = score
            best_match = candidate

    if best_score >= threshold:
        return best_match, best_score

    close = difflib.get_close_matches(target, valid_targets, n=1, cutoff=threshold)
    if close:
        return close[0], difflib.SequenceMatcher(None, target, close[0]).ratio()

    return None, 0.0


def check_note_links(note_path: Path, vault_dir: Path) -> List[DeadLink]:
    """Check broken wikilinks in a single note."""
    vault_path = Path(vault_dir).resolve()
    canonical_map = get_canonical_note_map(vault_path)
    rel_posix = note_path.relative_to(vault_path).as_posix() if note_path.is_relative_to(vault_path) else note_path.name
    broken: List[DeadLink] = []

    try:
        content = note_path.read_text(encoding="utf-8")
    except Exception:
        return broken

    for line_idx, line in enumerate(content.splitlines(), start=1):
        for full_match, target, heading, alias in find_all_wikilinks(line):
            resolved = (
                canonical_map.get(target)
                or canonical_map.get(target.lower())
                or canonical_map.get(f"{target}.md")
                or canonical_map.get(f"{target.lower()}.md")
            )
            if not resolved:
                broken.append(
                    DeadLink(
                        source_file=rel_posix,
                        target=target,
                        heading=heading,
                        alias=alias,
                        full_match=full_match,
                        line_number=line_idx,
                    )
                )
    return broken


def check_links(vault_dir: Path) -> LinkCheckResult:
    """Scan vault and detect all dead links, orphans, and dead ends."""
    vault_path = Path(vault_dir).resolve()
    all_notes = scan_vault_notes(vault_path)
    canonical_map = get_canonical_note_map(vault_path)

    valid_canonical_targets: Set[str] = set()
    for note_path in all_notes:
        rel = note_path.relative_to(vault_path).as_posix()
        rel_no_ext = rel[:-3] if rel.endswith(".md") else rel
        valid_canonical_targets.add(rel)
        valid_canonical_targets.add(rel_no_ext)
        valid_canonical_targets.add(note_path.stem)

    valid_targets_list = sorted(list(valid_canonical_targets))

    incoming_link_counts: Dict[str, int] = {
        p.relative_to(vault_path).as_posix(): 0 for p in all_notes
    }
    outgoing_link_counts: Dict[str, int] = {
        p.relative_to(vault_path).as_posix(): 0 for p in all_notes
    }

    result = LinkCheckResult()

    for note_path in all_notes:
        rel_posix = note_path.relative_to(vault_path).as_posix()
        try:
            content = note_path.read_text(encoding="utf-8")
        except Exception:
            continue

        lines = content.splitlines()
        for line_idx, line in enumerate(lines, start=1):
            matches = find_all_wikilinks(line)
            for full_match, target, heading, alias in matches:
                result.total_links += 1
                outgoing_link_counts[rel_posix] = outgoing_link_counts.get(rel_posix, 0) + 1

                resolved_path = (
                    canonical_map.get(target)
                    or canonical_map.get(target.lower())
                    or canonical_map.get(f"{target}.md")
                    or canonical_map.get(f"{target.lower()}.md")
                )

                if resolved_path:
                    result.resolved_links += 1
                    try:
                        target_rel = resolved_path.relative_to(vault_path).as_posix()
                        incoming_link_counts[target_rel] = (
                            incoming_link_counts.get(target_rel, 0) + 1
                        )
                    except Exception:
                        pass
                else:
                    suggestion, score = _find_best_match(target, valid_targets_list)
                    result.broken_links.append(
                        DeadLink(
                            source_file=rel_posix,
                            target=target,
                            heading=heading,
                            alias=alias,
                            full_match=full_match,
                            line_number=line_idx,
                            suggested_target=suggestion,
                            similarity_score=score,
                        )
                    )

    # Check canvas files for dead file references
    maps_dir = vault_path / "Maps"
    if maps_dir.exists():
        for canvas_file in maps_dir.glob("*.canvas"):
            rel_canvas = canvas_file.relative_to(vault_path).as_posix()
            try:
                data = json.loads(canvas_file.read_text(encoding="utf-8"))
                nodes = data.get("nodes", [])
                for node in nodes:
                    if node.get("type") == "file":
                        f_target = node.get("file", "")
                        result.total_links += 1
                        resolved_path = canonical_map.get(f_target) or canonical_map.get(f_target.lower())
                        if resolved_path:
                            result.resolved_links += 1
                            try:
                                t_rel = resolved_path.relative_to(vault_path).as_posix()
                                incoming_link_counts[t_rel] = incoming_link_counts.get(t_rel, 0) + 1
                            except Exception:
                                pass
                        else:
                            suggestion, score = _find_best_match(f_target, valid_targets_list)
                            result.broken_links.append(
                                DeadLink(
                                    source_file=rel_canvas,
                                    target=f_target,
                                    heading=None,
                                    alias=None,
                                    full_match=f_target,
                                    line_number=0,
                                    suggested_target=suggestion,
                                    similarity_score=score,
                                )
                            )
            except Exception:
                pass

    # Identify orphans and dead ends
    for rel_path, in_count in incoming_link_counts.items():
        if (
            in_count == 0
            and not rel_path.startswith("Templates/")
            and rel_path not in ("00-Hub.md", "01-Plan.md", "02-Index.md")
            and not (rel_path.endswith("/index.md") or rel_path.endswith("/z-Index.md") or rel_path.endswith("/z_index.md"))
        ):
            result.orphan_notes.append(rel_path)

    for rel_path, out_count in outgoing_link_counts.items():
        if (
            out_count == 0
            and not rel_path.startswith("Templates/")
            and not (rel_path.endswith("/index.md") or rel_path.endswith("/z-Index.md") or rel_path.endswith("/z_index.md"))
        ):
            result.dead_ends.append(rel_path)

    result.orphan_notes.sort()
    result.dead_ends.sort()

    return result


def check_all_links(vault_dir: Path) -> Dict[str, Any]:
    """Alias to check_links returning dict."""
    return check_links(vault_dir).to_dict()


def check_vault_links(vault_dir: Path) -> LinkCheckResult:
    """Alias for check_links."""
    return check_links(vault_dir)


def repair_links(
    vault_dir: Path,
    threshold: float = 0.8,
    fuzzy: bool = True,
    dry_run: bool = False,
) -> Dict[str, Any]:
    """Fuzzy match and automatically rewrite broken wikilinks in-place."""
    vault_path = Path(vault_dir).resolve()
    all_notes = scan_vault_notes(vault_path)
    canonical_map = get_canonical_note_map(vault_path)

    valid_targets_list = sorted(list(set(canonical_map.keys())))
    repairs_applied: List[Dict[str, Any]] = []
    files_to_modify: Dict[Path, str] = {}

    for note_path in all_notes:
        rel_posix = note_path.relative_to(vault_path).as_posix()
        try:
            content = note_path.read_text(encoding="utf-8")
        except Exception:
            continue

        file_changed = False
        lines = content.splitlines(keepends=True)
        new_lines = []

        for line in lines:
            matches = find_all_wikilinks(line)
            new_line = line
            for full_match, target, heading, alias in matches:
                # If target resolves directly to canonical target
                resolved = (
                    canonical_map.get(target)
                    or canonical_map.get(target.lower())
                    or canonical_map.get(f"{target}.md")
                    or canonical_map.get(f"{target.lower()}.md")
                )

                # Check if fuzzy repair is needed (e.g. bare citekey needing canonical path or typo)
                suggestion, score = _find_best_match(target, valid_targets_list, threshold=threshold)
                if (not resolved or (fuzzy and "/" not in target and suggestion and "/" in suggestion)) and suggestion:
                    if score >= threshold:
                        target_replacement = suggestion
                        if target_replacement.endswith(".md"):
                            target_replacement = target_replacement[:-3]

                        if target_replacement != target:
                            # Replace target inside [[...]]
                            pattern = re.compile(
                                r"(!*\[\[)" + re.escape(target) + r"((?:#[^\]|]+)?(?:\|[^\]]+)?\]\])"
                            )
                            replaced_line, count = pattern.subn(
                                lambda m: f"{m.group(1)}{target_replacement}{m.group(2)}",
                                new_line,
                            )
                            if count > 0:
                                new_line = replaced_line
                                file_changed = True
                                repairs_applied.append({
                                    "file": rel_posix,
                                    "old_target": target,
                                    "new_target": target_replacement,
                                    "score": round(score, 3),
                                })
            new_lines.append(new_line)

        if file_changed:
            files_to_modify[note_path] = "".join(new_lines)

    if not dry_run:
        for file_path, new_content in files_to_modify.items():
            file_path.write_text(new_content, encoding="utf-8")

    return {
        "status": "success",
        "repaired_count": len(repairs_applied),
        "repaired": len(repairs_applied),
        "dry_run": dry_run,
        "repairs": repairs_applied,
    }


def repair_all_links(
    vault_dir: Path, threshold: float = 0.8, dry_run: bool = False
) -> Dict[str, Any]:
    """Alias for repair_links."""
    return repair_links(vault_dir, threshold=threshold, dry_run=dry_run)


def repair_vault_links(
    vault_dir: Path, threshold: float = 0.8, dry_run: bool = False
) -> Dict[str, Any]:
    """Alias for repair_links."""
    return repair_links(vault_dir, threshold=threshold, dry_run=dry_run)


def build_vault_graph(vault_dir: Path) -> Dict[str, Dict[str, List[str]]]:
    """Build directed graph mapping notes to incoming and outgoing note links."""
    vault_path = Path(vault_dir).resolve()
    all_notes = scan_vault_notes(vault_path)
    canonical_map = get_canonical_note_map(vault_path)

    graph: Dict[str, Dict[str, List[str]]] = {}
    for p in all_notes:
        rel = p.relative_to(vault_path).as_posix()
        graph[rel] = {"outgoing": [], "incoming": []}

    for note_path in all_notes:
        rel_posix = note_path.relative_to(vault_path).as_posix()
        try:
            content = note_path.read_text(encoding="utf-8")
        except Exception:
            continue

        for _, target, _, _ in find_all_wikilinks(content):
            resolved = (
                canonical_map.get(target)
                or canonical_map.get(target.lower())
                or canonical_map.get(f"{target}.md")
                or canonical_map.get(f"{target.lower()}.md")
            )
            if resolved and resolved.exists():
                try:
                    t_rel = resolved.relative_to(vault_path).as_posix()
                    if t_rel not in graph[rel_posix]["outgoing"]:
                        graph[rel_posix]["outgoing"].append(t_rel)
                    if rel_posix not in graph[t_rel]["incoming"]:
                        graph[t_rel]["incoming"].append(rel_posix)
                except Exception:
                    pass

    return graph
