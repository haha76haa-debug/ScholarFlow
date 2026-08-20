"""
Zotero-Obsidian Academic Knowledge Base - Master Pipeline Runner
Executes lint -> sync-registry -> check-links -> synthesize -> generate-canvas in one command.
"""
import os
import subprocess
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
    print("=" * 70)
    print("[*] Running Academic Knowledge Base Self-Iteration Pipeline")
    print(f"[>] Vault Root: {vault_root}")
    print("=" * 70)

    steps = [
        ("1. Strict Schema & Evidence Linter", ["-m", "kb_tools", "lint", "--vault-dir", str(vault_root), "--strict"]),
        ("2. Master Registry & Index Sync", ["-m", "kb_tools", "sync-registry", "--vault-dir", str(vault_root)]),
        ("3. Wikilink Integrity & Orphan Check", ["-m", "kb_tools", "check-links", "--vault-dir", str(vault_root)]),
        ("4. Cross-Paper Knowledge Synthesizer", ["-m", "kb_tools", "synthesize", "--vault-dir", str(vault_root)]),
        ("5. Visual JSON Canvas Builder", ["-m", "kb_tools", "generate-canvas", "--vault-dir", str(vault_root)]),
    ]

    for title, args in steps:
        print(f"\n>> {title}...")
        cmd = [sys.executable] + args
        result = subprocess.run(cmd, cwd=str(vault_root))
        if result.returncode != 0:
            print(f"[!] Error during step: {title} (Exit Code: {result.returncode})")
            sys.exit(result.returncode)

    print("\n" + "=" * 70)
    print("[+] Full Self-Iteration Pipeline Completed Successfully!")
    print("=" * 70)

if __name__ == "__main__":
    main()
