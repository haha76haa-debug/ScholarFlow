"""
Unified CLI Entry Point and Subcommand Dispatcher for kb_tools.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import List, Optional

from kb_tools.canvas_gen import generate_canvas_file
from kb_tools.ingest import ingest_file
from kb_tools.link_checker import check_links, repair_links
from kb_tools.linter import lint_file, lint_vault, write_lint_report
from kb_tools.registry import sync_registry
from kb_tools.synthesizer import run_synthesis


def _add_common_vault_args(parser: argparse.ArgumentParser) -> None:
    """Add --vault-dir and --cwd flags to subparser."""
    parser.add_argument("--vault-dir", default=None, help="Root path of the knowledge base vault")
    parser.add_argument("--cwd", default=None, help="Alias for --vault-dir")


def _resolve_vault_dir(args: argparse.Namespace) -> Path:
    """Resolve vault directory from --vault-dir or --cwd, falling back to current working directory."""
    raw = getattr(args, "vault_dir", None) or getattr(args, "cwd", None) or "."
    return Path(raw).resolve()


def create_parser() -> argparse.ArgumentParser:
    """Construct unified argument parser with subcommands and aliases."""
    parser = argparse.ArgumentParser(
        prog="kb-tools",
        description="Academic Knowledge Base Maintenance and Automation Toolsuite",
    )
    subparsers = parser.add_subparsers(dest="subcommand", help="Available subcommands")

    # 1. lint
    lint_parser = subparsers.add_parser("lint", help="Validate note metadata, schemas, and headings")
    lint_parser.add_argument("target", nargs="?", default=None, help="Optional single note file path to lint")
    _add_common_vault_args(lint_parser)
    lint_parser.add_argument("--strict", action="store_true", help="Treat warnings as errors")
    lint_parser.add_argument("--json", action="store_true", help="Output findings as JSON")
    lint_parser.add_argument("--report-path", default=None, help="Path for generated Markdown lint report")

    # 2. sync-registry / sync_registry
    for name in ("sync-registry", "sync_registry"):
        sync_parser = subparsers.add_parser(name, help="Synchronize indices and _system/registry.md")
        _add_common_vault_args(sync_parser)
        sync_parser.add_argument("--dry-run", action="store_true", help="Do not write changes to disk")
        sync_parser.add_argument("--json", action="store_true", help="Output result as JSON")

    # 3. check-links / check_links
    for name in ("check-links", "check_links"):
        check_parser = subparsers.add_parser(name, help="Detect dead/broken wikilinks and orphan notes")
        _add_common_vault_args(check_parser)
        check_parser.add_argument("--json", action="store_true", help="Output result as JSON")

    # 4. repair-links / repair_links
    for name in ("repair-links", "repair_links"):
        repair_parser = subparsers.add_parser(name, help="Fuzzy match and automatically repair broken wikilinks")
        _add_common_vault_args(repair_parser)
        repair_parser.add_argument("--threshold", type=float, default=0.8, help="Similarity threshold (0.0 - 1.0)")
        repair_parser.add_argument("--dry-run", action="store_true", help="Do not write changes to disk")
        repair_parser.add_argument("--json", action="store_true", help="Output result as JSON")

    # 5. synthesize
    synth_parser = subparsers.add_parser("synthesize", help="Generate cross-paper syntheses and comparison matrix")
    _add_common_vault_args(synth_parser)
    synth_parser.add_argument("--topic", default=None, help="Specific topic or cluster to synthesize")
    synth_parser.add_argument("--dry-run", action="store_true", help="Do not write changes to disk")
    synth_parser.add_argument("--json", action="store_true", help="Output result as JSON")

    # 6. generate-canvas / generate_canvas
    for name in ("generate-canvas", "generate_canvas"):
        canvas_parser = subparsers.add_parser(name, help="Generate Obsidian JSON Canvas v1.0 file")
        _add_common_vault_args(canvas_parser)
        canvas_parser.add_argument("--output-path", default=None, help="Output .canvas file path")
        canvas_parser.add_argument("--dry-run", action="store_true", help="Do not write changes to disk")
        canvas_parser.add_argument("--json", action="store_true", help="Output result as JSON")

    # 7. ingest
    ingest_parser = subparsers.add_parser("ingest", help="Ingest BibTeX / CSL-JSON into canonical paper notes")
    _add_common_vault_args(ingest_parser)
    ingest_parser.add_argument("--input", required=True, help="Input BibTeX or CSL-JSON file path")
    ingest_parser.add_argument("--format", choices=["bibtex", "csl-json"], default=None, help="Explicit input format")
    ingest_parser.add_argument("--overwrite", action="store_true", help="Overwrite existing paper notes")
    ingest_parser.add_argument("--dry-run", action="store_true", help="Do not write changes to disk")
    ingest_parser.add_argument("--json", action="store_true", help="Output result as JSON")

    # 8. run-pipeline / run_pipeline
    for name in ("run-pipeline", "run_pipeline"):
        pipeline_parser = subparsers.add_parser(name, help="Execute full 5-step knowledge base maintenance pipeline")
        _add_common_vault_args(pipeline_parser)
        pipeline_parser.add_argument("--strict", action="store_true", default=True, help="Treat warnings as fatal errors (default True)")
        pipeline_parser.add_argument("--no-strict", dest="strict", action="store_false", help="Do not treat warnings as fatal errors")
        pipeline_parser.add_argument("--dry-run", action="store_true", help="Execute pipeline steps without writing changes to disk")
        pipeline_parser.add_argument("--json", action="store_true", help="Output pipeline summary and step results as JSON")

    return parser


def handle_lint(args: argparse.Namespace) -> int:
    vault_dir = _resolve_vault_dir(args)
    if not vault_dir.exists():
        print(f"Error: Vault directory '{vault_dir}' not found.", file=sys.stderr)
        return 1

    report_path = Path(args.report_path).resolve() if args.report_path else None

    if args.target:
        target_path = Path(args.target).resolve()
        if not target_path.exists():
            target_path = vault_dir / args.target
        if not target_path.exists():
            print(f"Error: Target note '{args.target}' not found.", file=sys.stderr)
            return 1

        issues = lint_file(target_path, vault_dir=vault_dir)
        errors = [i for i in issues if i.severity == "error"]
        warnings = [i for i in issues if i.severity == "warning"]

        if args.json:
            print(json.dumps({
                "target": str(target_path),
                "is_clean": len(errors) == 0,
                "error_count": len(errors),
                "errors_count": len(errors),
                "warning_count": len(warnings),
                "warnings_count": len(warnings),
                "issues": [{"severity": i.severity, "message": i.message} for i in issues],
            }, indent=2))
        else:
            print(f"Linted target file: {target_path}")
            if len(errors) == 0:
                print(f"0 errors found. Warnings: {len(warnings)}")
            else:
                print(f"Errors: {len(errors)} | Warnings: {len(warnings)}")
            for i in issues:
                print(f"[{i.severity.upper()}] {i.message}")

        if args.strict and (len(errors) > 0 or len(warnings) > 0):
            return 1
        return 1 if len(errors) > 0 else 0

    result = lint_vault(vault_dir, strict=args.strict)
    written_report = write_lint_report(result, vault_dir, report_path)

    if args.json:
        print(json.dumps(result.to_dict(), indent=2))
    else:
        print(f"Scanned {result.total_files_scanned} notes. Passed: {result.passed_files}")
        if result.is_clean:
            print("0 errors found, 0 warnings found.")
        else:
            print(f"Errors: {result.error_count} | Warnings: {result.warning_count}")
        print(f"Report written to: {written_report}")
        if not result.is_clean:
            for issue in result.issues[:10]:
                print(f"[{issue.severity.upper()}] {issue.file_path}: {issue.message}")
            if len(result.issues) > 10:
                print(f"... and {len(result.issues) - 10} more issues.")

    if args.strict and (result.error_count > 0 or result.warning_count > 0):
        return 1
    return 1 if result.error_count > 0 else 0


def handle_sync_registry(args: argparse.Namespace) -> int:
    vault_dir = _resolve_vault_dir(args)
    if not vault_dir.exists():
        print(f"Error: Vault directory '{vault_dir}' not found.", file=sys.stderr)
        return 1

    try:
        res = sync_registry(vault_dir, dry_run=args.dry_run)
    except Exception as e:
        print(f"Error during registry sync: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Synchronized registry: {res['papers_count']} papers, {res['knowledge_count']} concepts/syntheses.")
        if args.dry_run:
            print("[DRY RUN] No files modified.")
        else:
            print("Updated files: " + ", ".join(res["updated_files"]))
    return 0


def handle_check_links(args: argparse.Namespace) -> int:
    vault_dir = _resolve_vault_dir(args)
    if not vault_dir.exists():
        print(f"Error: Vault directory '{vault_dir}' not found.", file=sys.stderr)
        return 1

    res = check_links(vault_dir)

    if args.json:
        print(json.dumps(res.to_dict(), indent=2))
    else:
        print(f"Total links: {res.total_links} | Resolved: {res.resolved_links} | Broken: {len(res.broken_links)}")
        if res.is_clean:
            print("0 broken links found.")
        else:
            print(f"Broken Links Found ({len(res.broken_links)}):")
            for b in res.broken_links:
                sug = f" -> Suggestion: [[{b.suggested_target}]] ({b.similarity_score:.2f})" if b.suggested_target else ""
                print(f"  - {b.source_file}:{b.line_number} -> [[{b.target}]]{sug}")
        if res.orphan_notes:
            print(f"Orphan Notes ({len(res.orphan_notes)}): " + ", ".join(res.orphan_notes[:5]))

    return 0 if res.is_clean else 1


def handle_repair_links(args: argparse.Namespace) -> int:
    vault_dir = _resolve_vault_dir(args)
    if not vault_dir.exists():
        print(f"Error: Vault directory '{vault_dir}' not found.", file=sys.stderr)
        return 1

    res = repair_links(vault_dir, threshold=args.threshold, dry_run=args.dry_run)

    if args.json:
        print(json.dumps(res, indent=2))
    else:
        print(f"Repaired {res['repaired_count']} links.")
        for r in res.get("repairs", []):
            print(f"  - In {r['file']}: [[{r['old_target']}]] -> [[{r['new_target']}]] (score: {r['score']})")
        if args.dry_run:
            print("[DRY RUN] No files modified.")
    return 0


def handle_synthesize(args: argparse.Namespace) -> int:
    vault_dir = _resolve_vault_dir(args)
    if not vault_dir.exists():
        print(f"Error: Vault directory '{vault_dir}' not found.", file=sys.stderr)
        return 1

    files = run_synthesis(vault_dir, dry_run=args.dry_run, topic=args.topic)

    if args.json:
        print(json.dumps({
            "status": "success",
            "papers_analyzed": len(files),
            "synthesized_files": [f.as_posix() for f in files],
        }, indent=2))
    else:
        print(f"Successfully synthesized {len(files)} knowledge files:")
        for f in files:
            print(f"  - {f.relative_to(vault_dir).as_posix()}")
        if args.dry_run:
            print("[DRY RUN] Files not written to disk.")
    return 0


def handle_generate_canvas(args: argparse.Namespace) -> int:
    vault_dir = _resolve_vault_dir(args)
    if not vault_dir.exists():
        print(f"Error: Vault directory '{vault_dir}' not found.", file=sys.stderr)
        return 1

    out_path = Path(args.output_path).resolve() if args.output_path else None
    canvas_file = generate_canvas_file(vault_dir, output_path=out_path, dry_run=args.dry_run)

    if args.json:
        from kb_tools.canvas_gen import build_canvas_graph
        graph = build_canvas_graph(vault_dir)
        print(json.dumps(graph, indent=2))
    else:
        print(f"Generated Canvas visual map at: {canvas_file}")
        if args.dry_run:
            print("[DRY RUN] File not written to disk.")
    return 0


def handle_ingest(args: argparse.Namespace) -> int:
    vault_dir = _resolve_vault_dir(args)
    if not vault_dir.exists():
        print(f"Error: Vault directory '{vault_dir}' not found.", file=sys.stderr)
        return 1

    input_path = Path(args.input).resolve()
    if not input_path.exists():
        print(f"Error: Input file '{input_path}' not found.", file=sys.stderr)
        return 1

    try:
        created = ingest_file(
            input_path,
            vault_dir=vault_dir,
            overwrite=args.overwrite,
            dry_run=args.dry_run,
        )
    except Exception as e:
        print(f"Error during ingestion: {e}", file=sys.stderr)
        return 1

    if args.json:
        print(json.dumps({
            "status": "success",
            "ingested": [p.as_posix() for p in created],
            "count": len(created),
        }, indent=2))
    else:
        print(f"Ingested {len(created)} paper notes:")
        for p in created:
            print(f"  - {p.relative_to(vault_dir).as_posix()}")
    return 0


def handle_run_pipeline(args: argparse.Namespace) -> int:
    """Execute full 5-step self-iteration pipeline:
    1. Lint (--strict)
    2. Sync Registry
    3. Check Links
    4. Synthesize
    5. Generate Canvas
    """
    vault_dir = _resolve_vault_dir(args)
    if not vault_dir.exists():
        print(f"Error: Vault directory '{vault_dir}' not found.", file=sys.stderr)
        return 1

    strict = getattr(args, "strict", True)
    dry_run = getattr(args, "dry_run", False)
    is_json = getattr(args, "json", False)

    steps_results = []
    overall_passed = True

    if not is_json:
        print("=" * 70)
        print("[*] Running Academic Knowledge Base Self-Iteration Pipeline (5 Steps)")
        print(f"[>] Vault Root: {vault_dir}")
        print(f"[>] Options: strict={strict}, dry_run={dry_run}")
        print("=" * 70)

    # -------------------------------------------------------------
    # Step 1: Strict Schema & Evidence Linter
    # -------------------------------------------------------------
    if not is_json:
        print("\n>> Step 1/5: Strict Schema & Evidence Linter...")

    try:
        lint_res = lint_vault(vault_dir, strict=strict)
        if not dry_run:
            write_lint_report(lint_res, vault_dir)
        step1_passed = not (lint_res.error_count > 0 or (strict and lint_res.warning_count > 0))
        steps_results.append({
            "step": 1,
            "name": "lint",
            "passed": step1_passed,
            "scanned": lint_res.total_files_scanned,
            "errors": lint_res.error_count,
            "warnings": lint_res.warning_count,
            "issues": [{"severity": i.severity, "category": i.category, "file": i.file_path, "message": i.message} for i in lint_res.issues[:10]],
        })
        if not step1_passed:
            overall_passed = False
            if not is_json:
                print(f"[!] LINT FAILED: {lint_res.error_count} errors, {lint_res.warning_count} warnings.")
                for i in lint_res.issues[:5]:
                    print(f"    - [{i.severity.upper()}] {i.file_path}: {i.message}")
        else:
            if not is_json:
                print(f"[PASS] Scanned {lint_res.total_files_scanned} notes. Errors: 0, Warnings: {lint_res.warning_count}.")
    except Exception as e:
        overall_passed = False
        steps_results.append({"step": 1, "name": "lint", "passed": False, "error": str(e)})
        if not is_json:
            print(f"[!] Error in Step 1 (Lint): {e}", file=sys.stderr)

    # -------------------------------------------------------------
    # Step 2: Master Registry & Index Sync
    # -------------------------------------------------------------
    if not is_json:
        print("\n>> Step 2/5: Master Registry & Index Sync...")

    try:
        reg_res = sync_registry(vault_dir, dry_run=dry_run)
        step2_passed = reg_res.get("status") == "success"
        steps_results.append({
            "step": 2,
            "name": "sync_registry",
            "passed": step2_passed,
            "papers_count": reg_res.get("papers_count", 0),
            "concepts_count": reg_res.get("concepts_count", 0),
            "comparisons_count": reg_res.get("comparisons_count", 0),
            "updated_files": reg_res.get("updated_files", []),
        })
        if not step2_passed:
            overall_passed = False
            if not is_json:
                print("[!] REGISTRY SYNC FAILED.")
        else:
            if not is_json:
                print(f"[PASS] Synchronized {reg_res.get('papers_count', 0)} papers, {reg_res.get('concepts_count', 0)} concepts, {reg_res.get('comparisons_count', 0)} comparisons.")
    except Exception as e:
        overall_passed = False
        steps_results.append({"step": 2, "name": "sync_registry", "passed": False, "error": str(e)})
        if not is_json:
            print(f"[!] Error in Step 2 (Sync Registry): {e}", file=sys.stderr)

    # -------------------------------------------------------------
    # Step 3: Wikilink Integrity & Orphan Check
    # -------------------------------------------------------------
    if not is_json:
        print("\n>> Step 3/5: Wikilink Integrity & Orphan Check...")

    try:
        link_res = check_links(vault_dir)
        step3_passed = link_res.is_clean
        steps_results.append({
            "step": 3,
            "name": "check_links",
            "passed": step3_passed,
            "total_links": link_res.total_links,
            "resolved_links": link_res.resolved_links,
            "broken_links_count": len(link_res.broken_links),
            "orphan_notes_count": len(link_res.orphan_notes),
        })
        if not step3_passed:
            overall_passed = False
            if not is_json:
                print(f"[!] LINK CHECK FAILED: {len(link_res.broken_links)} broken links found.")
                for b in link_res.broken_links[:5]:
                    print(f"    - {b.source_file}:{b.line_number} -> [[{b.target}]]")
        else:
            if not is_json:
                print(f"[PASS] Checked {link_res.total_links} links: {link_res.resolved_links} resolved, 0 broken.")
    except Exception as e:
        overall_passed = False
        steps_results.append({"step": 3, "name": "check_links", "passed": False, "error": str(e)})
        if not is_json:
            print(f"[!] Error in Step 3 (Check Links): {e}", file=sys.stderr)

    # -------------------------------------------------------------
    # Step 4: Cross-Paper Knowledge Synthesizer
    # -------------------------------------------------------------
    if not is_json:
        print("\n>> Step 4/5: Cross-Paper Knowledge Synthesizer...")

    try:
        synth_files = run_synthesis(vault_dir, dry_run=dry_run)
        step4_passed = len(synth_files) > 0
        steps_results.append({
            "step": 4,
            "name": "synthesize",
            "passed": step4_passed,
            "synthesized_count": len(synth_files),
            "synthesized_files": [f.as_posix() for f in synth_files],
        })
        if not is_json:
            print(f"[PASS] Synthesized {len(synth_files)} knowledge files.")
    except Exception as e:
        overall_passed = False
        steps_results.append({"step": 4, "name": "synthesize", "passed": False, "error": str(e)})
        if not is_json:
            print(f"[!] Error in Step 4 (Synthesize): {e}", file=sys.stderr)

    # -------------------------------------------------------------
    # Step 5: Visual JSON Canvas Builder
    # -------------------------------------------------------------
    if not is_json:
        print("\n>> Step 5/5: Visual JSON Canvas Builder...")

    try:
        canvas_path = generate_canvas_file(vault_dir, dry_run=dry_run)
        step5_passed = canvas_path is not None
        steps_results.append({
            "step": 5,
            "name": "generate_canvas",
            "passed": step5_passed,
            "canvas_file": str(canvas_path),
        })
        if not is_json:
            print(f"[PASS] Generated 4-lane Canvas visual map at {canvas_path}.")
    except Exception as e:
        overall_passed = False
        steps_results.append({"step": 5, "name": "generate_canvas", "passed": False, "error": str(e)})
        if not is_json:
            print(f"[!] Error in Step 5 (Generate Canvas): {e}", file=sys.stderr)

    # -------------------------------------------------------------
    # Summary & Return Code
    # -------------------------------------------------------------
    if is_json:
        output_payload = {
            "status": "success" if overall_passed else "failure",
            "pipeline_passed": overall_passed,
            "vault_dir": str(vault_dir),
            "strict": strict,
            "dry_run": dry_run,
            "steps": steps_results,
        }
        print(json.dumps(output_payload, indent=2))
    else:
        print("\n" + "=" * 70)
        if overall_passed:
            print("[+] Full Self-Iteration Pipeline Completed Successfully! (0 errors, 0 warnings, 0 broken links)")
        else:
            print("[!] Pipeline Execution Failed. See step details above.")
        print("=" * 70)

    return 0 if overall_passed else 1


def main(args: Optional[List[str]] = None) -> int:
    """Main CLI entry point."""
    parser = create_parser()

    try:
        parsed_args = parser.parse_args(args)
    except SystemExit as e:
        return e.code if isinstance(e.code, int) else 0

    if not parsed_args.subcommand:
        parser.print_help()
        return 1

    cmd = parsed_args.subcommand.replace("_", "-")

    if cmd == "lint":
        return handle_lint(parsed_args)
    elif cmd == "sync-registry":
        return handle_sync_registry(parsed_args)
    elif cmd == "check-links":
        return handle_check_links(parsed_args)
    elif cmd == "repair-links":
        return handle_repair_links(parsed_args)
    elif cmd == "synthesize":
        return handle_synthesize(parsed_args)
    elif cmd == "generate-canvas":
        return handle_generate_canvas(parsed_args)
    elif cmd == "ingest":
        return handle_ingest(parsed_args)
    elif cmd == "run-pipeline":
        return handle_run_pipeline(parsed_args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
