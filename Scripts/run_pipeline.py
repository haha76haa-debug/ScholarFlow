"""
Zotero-Obsidian Academic Knowledge Base - Master Pipeline Runner
Executes lint -> sync-registry -> check-links -> synthesize -> generate-canvas in one unified command.
"""
import os
import sys
from pathlib import Path

# Ensure UTF-8 output encoding on Windows consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def main():
    vault_root = Path(__file__).resolve().parent.parent
    from kb_tools.cli import main as cli_main

    exit_code = cli_main(["run-pipeline", "--vault-dir", str(vault_root), "--strict"])
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
