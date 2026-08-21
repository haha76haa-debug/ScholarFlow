"""
BibTeX, Better BibTeX, and CSL-JSON Ingestion and Note Instantiation Engine.
"""

from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

from kb_tools.models import dump_frontmatter


def clean_latex_string(s: str) -> str:
    """Clean LaTeX accent commands, formatting directives, and escape sequences."""
    if not s:
        return ""

    text = s

    # Common LaTeX umlauts and accents
    replacements = [
        (r'{\\"u}', "ü"),
        (r'\\"u', "ü"),
        (r'{\\"U}', "Ü"),
        (r'\\"U', "Ü"),
        (r'{\\"o}', "ö"),
        (r'\\"o', "ö"),
        (r'{\\"O}', "Ö"),
        (r'\\"O', "Ö"),
        (r'{\\"a}', "ä"),
        (r'\\"a', "ä"),
        (r'{\\"A}', "Ä"),
        (r'\\"A', "Ä"),
        (r'{\\c{c}}', "ç"),
        (r'\\c{c}', "ç"),
        (r"{\\'a}", "á"),
        (r"\\'a", "á"),
        (r"{\\'e}", "é"),
        (r"\\'e", "é"),
        (r"{\\`e}", "è"),
        (r"\\`e", "è"),
        (r"\\v{S}", "Š"),
        (r"\\v{s}", "š"),
        (r"{\\L}", "Ł"),
        (r"\\L", "Ł"),
        (r"{\\l}", "ł"),
        (r"\\l", "ł"),
        (r"\\&", "&"),
        (r"\\%", "%"),
        (r"\\$", "$"),
        (r"\\_", "_"),
        (r"\\#", "#"),
        (r"\\sim", "~"),
    ]

    for pat, rep in replacements:
        text = text.replace(pat, rep)

    # Remove \textbf{...}, \textit{...}, \emph{...}
    text = re.sub(r"\\textbf\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\textit\{([^}]*)\}", r"\1", text)
    text = re.sub(r"\\emph\{([^}]*)\}", r"\1", text)

    # Strip remaining curly braces enclosing words (e.g. {RNN}s -> RNNs)
    text = re.sub(r"\{([^{}]*)\}", r"\1", text)

    # Normalize double whitespace
    text = re.sub(r"\s+", " ", text).strip()

    return text


def sanitize_citekey(s: str) -> str:
    """Normalize citekey to lowercase alphanumeric format [a-z0-9]+ adhering to Better BibTeX [auth:lower][year][veryshorttitle:lower]."""
    if not s:
        return "unknownpaper"

    # Match structured "Author-Year-Title-Words..." or "Author_Year_Title"
    m = re.match(r"^([a-zA-Z]+)[-_](\d{4})[-_]([a-zA-Z]+)", s)
    if m:
        return f"{m.group(1).lower()}{m.group(2)}{m.group(3).lower()}"

    clean = re.sub(r"[^a-zA-Z0-9]", "", s).lower()
    return clean or "unknownpaper"


def _format_author_name(raw_name: str) -> str:
    """Format author name to standard 'Firstname Lastname' or 'Lastname, Firstname'."""
    clean = clean_latex_string(raw_name).strip()
    if "," in clean:
        parts = [p.strip() for p in clean.split(",", 1)]
        if len(parts) == 2 and parts[1]:
            return f"{parts[1]} {parts[0]}"
    return clean


def parse_bibtex(content: str) -> List[Dict[str, Any]]:
    """Parse raw BibTeX text and extract structured item records."""
    entries: List[Dict[str, Any]] = []

    entry_pattern = re.compile(
        r"@([a-zA-Z]+)\s*\{\s*([^,\s]+)\s*,([\s\S]*?)(?=\n@[a-zA-Z]+\s*\{|\Z)",
        re.MULTILINE,
    )

    for match in entry_pattern.finditer(content):
        item_type = match.group(1).lower()
        raw_citekey = match.group(2).strip()
        body = match.group(3)

        fields: Dict[str, str] = {}
        field_pattern = re.compile(
            r'([a-zA-Z_\-]+)\s*=\s*(?:\{([^{}]*(?:\{[^{}]*\}[^{}]*)*)\}|"([^"]*)"|([a-zA-Z0-9_\-]+))',
            re.MULTILINE,
        )

        for f_match in field_pattern.finditer(body):
            f_name = f_match.group(1).lower()
            f_val = f_match.group(2) or f_match.group(3) or f_match.group(4) or ""
            fields[f_name] = clean_latex_string(f_val)

        title = fields.get("title", raw_citekey)
        raw_authors = fields.get("author", "")
        author_list = []
        if raw_authors:
            for a in re.split(r"\s+and\s+", raw_authors, flags=re.IGNORECASE):
                formatted = _format_author_name(a)
                if formatted:
                    author_list.append(formatted)
        if not author_list:
            author_list = ["Anonymous"]

        year_str = fields.get("year", "")
        year_match = re.search(r"\d{4}", year_str)
        year = int(year_match.group(0)) if year_match else datetime.now().year

        venue = (
            fields.get("booktitle")
            or fields.get("journal")
            or fields.get("publisher")
            or fields.get("archiveprefix")
            or "Preprint"
        )

        doi = fields.get("doi", "")
        url = fields.get("url", "")
        if not url and fields.get("eprint"):
            url = f"https://arxiv.org/abs/{fields['eprint']}"

        citekey = sanitize_citekey(raw_citekey)

        entries.append({
            "citekey": citekey,
            "raw_citekey": raw_citekey,
            "item_type": item_type,
            "title": title,
            "authors": author_list,
            "year": year,
            "venue": venue,
            "doi": doi,
            "url": url,
            "abstract": fields.get("abstract", ""),
        })

    return entries


def parse_csl_json(data: Union[List[Any], Dict[str, Any], str]) -> List[Dict[str, Any]]:
    """Parse Citation Style Language (CSL) JSON into structured items."""
    if isinstance(data, str):
        parsed = json.loads(data)
    else:
        parsed = data

    items = parsed if isinstance(parsed, list) else [parsed]
    entries: List[Dict[str, Any]] = []

    for item in items:
        if not isinstance(item, dict):
            continue

        raw_id = str(item.get("id", item.get("citation-key", "item")))
        citekey = sanitize_citekey(raw_id)
        title = clean_latex_string(str(item.get("title", "Untitled Paper")))

        authors: List[str] = []
        author_data = item.get("author", [])
        if isinstance(author_data, list):
            for a in author_data:
                if isinstance(a, dict):
                    fam = clean_latex_string(str(a.get("family", "")))
                    given = clean_latex_string(str(a.get("given", "")))
                    if given and fam:
                        authors.append(f"{given} {fam}")
                    elif fam:
                        authors.append(fam)
                    elif str(a.get("literal", "")):
                        authors.append(str(a.get("literal")))
        if not authors:
            authors = ["Anonymous"]

        year = datetime.now().year
        issued = item.get("issued", {})
        if isinstance(issued, dict):
            date_parts = issued.get("date-parts", [])
            if date_parts and isinstance(date_parts[0], list) and date_parts[0]:
                year = int(date_parts[0][0])
            elif issued.get("raw"):
                m = re.search(r"\d{4}", str(issued.get("raw")))
                if m:
                    year = int(m.group(0))

        venue = (
            item.get("container-title")
            or item.get("publisher")
            or item.get("event")
            or "Preprint"
        )

        entries.append({
            "citekey": citekey,
            "raw_citekey": raw_id,
            "item_type": item.get("type", "article-journal"),
            "title": title,
            "authors": authors,
            "year": year,
            "venue": str(venue),
            "doi": str(item.get("DOI", "")),
            "url": str(item.get("URL", "")),
            "abstract": str(item.get("abstract", "")),
        })

    return entries


def render_paper_note(entry: Dict[str, Any]) -> str:
    """Generate Markdown note compliant with paper_schema.yaml."""
    citekey = entry.get("citekey", "paper")
    title = entry.get("title", "Untitled")
    authors = entry.get("authors", ["Anonymous"])
    year = int(entry.get("year", 2024))
    venue = entry.get("venue", "")
    doi = entry.get("doi", "")
    url = entry.get("url", "")
    item_type = entry.get("item_type", "conferencePaper")

    source_type = "conference paper"
    if "journal" in item_type.lower() or "article" in item_type.lower():
        source_type = "journal article"
    elif "preprint" in item_type.lower() or "arxiv" in str(doi).lower() or "arxiv" in str(url).lower():
        source_type = "preprint"
    elif "book" in item_type.lower():
        source_type = "book"

    zotero_key = citekey[:8].upper()

    frontmatter = {
        "type": "paper",
        "project": "zotero_obsidian_kb",
        "title": title,
        "citekey": citekey,
        "zotero_key": zotero_key,
        "status": "unread",
        "source_type": source_type,
        "claim_strength": "observed",
        "authors": authors,
        "year": year,
        "venue": venue,
        "doi": doi,
        "url": url,
        "keywords": [citekey],
        "concepts": [],
        "methods": [],
        "subfield": "general",
        "related_papers": [],
        "linked_knowledge": ["Knowledge/Literature Overview"],
        "updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
    }

    body = f"""# {title}
> **中文译名**：*(待补充中文翻译)*

## Claim
- **[EN]**: Primary assertion and findings of this work.
- **[CN] 核心主张**: 论文主要结论与核心学术论点。

## Research question
- **[EN]**: What specific open problem or hypothesis is addressed in this paper?
- **[CN] 核心科学问题**: 本文聚焦的关键科学问题或技术挑战。

## Method
- **[EN]**: Core architecture, algorithmic mechanism, or theoretical formulation.
- **[CN] 核心方法**: 核心架构、算法机理或理论方法。

## Evidence
```md
Evidence ID: EVD-{citekey}-01
Source: [[Sources/Papers/{citekey}]]
Source type: {source_type}
Supports: "Primary claim of {citekey} / 核心结论支持主张"
Contradicts: ""
Method / dataset / metric: "{venue}"
Limitation: ""
Project relevance: "Primary literature reference for {citekey} / 文献核心参考"
Claim strength: observed
```

## Strengths
- **[EN] Theoretical & Empirical**: Novel algorithmic or empirical contribution.
- **[CN] 优势与贡献**: 理论或实证创新要点。

## Limitation
- **[EN] Boundary Condition**: Identified computational constraints or open questions.
- **[CN] 局限性与不足**: 适用边界或未解决的计算限制。

## Direct relevance to repo
- **[EN]**: Implementation insights and takeaways for this research knowledge base.
- **[CN] 本库应用价值**: 对当前知识库与课题研究的直接启示。

## Relation to other papers
- **[EN]**: Related literature and comparative baselines.
- **[CN] 与其他文献关联**: 继承关系与对比基准。

## Knowledge links
- [[Knowledge/Literature Overview]]
"""

    return dump_frontmatter(frontmatter, body)


def ingest_file(
    file_path: Union[Path, str],
    vault_dir: Optional[Union[Path, str]] = None,
    overwrite: bool = False,
    dry_run: bool = False,
) -> List[Path]:
    """Ingest a BibTeX or CSL-JSON file and create canonical paper notes."""
    path = Path(file_path).resolve()
    if not path.exists():
        raise FileNotFoundError(f"Input file does not exist: {path}")

    v_dir = Path(vault_dir).resolve() if vault_dir else Path.cwd()
    papers_dir = v_dir / "Sources" / "Papers"

    content = path.read_text(encoding="utf-8")

    if path.suffix == ".json" or content.strip().startswith("[") or content.strip().startswith("{"):
        entries = parse_csl_json(content)
    else:
        entries = parse_bibtex(content)

    created_paths: List[Path] = []

    for entry in entries:
        citekey = entry["citekey"]
        target_file = papers_dir / f"{citekey}.md"

        if target_file.exists() and not overwrite:
            continue

        rendered_markdown = render_paper_note(entry)

        if not dry_run:
            papers_dir.mkdir(parents=True, exist_ok=True)
            target_file.write_text(rendered_markdown, encoding="utf-8")

        created_paths.append(target_file)

    return created_paths
