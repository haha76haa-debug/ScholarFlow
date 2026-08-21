"""
Zotero-Obsidian Academic Knowledge Base - Demo Restorer
Restores demo papers, concepts, and graphs from .demo_backup/ back into the active vault.
"""
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Ensure UTF-8 output encoding
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

def main():
    vault_root = Path(__file__).resolve().parent.parent
    archive_demo = vault_root / ".demo_backup"

    if not archive_demo.exists():
        print("[-] No archived demo examples found at: .demo_backup/")
        return

    print("=" * 70)
    print("[*] Restoring Demo Literature & Knowledge Network (恢复示例数据模式)")
    print(f"[>] Vault Root: {vault_root}")
    print("=" * 70)

    # 1. Restore papers
    demo_papers_dir = archive_demo / "Papers"
    papers_dir = vault_root / "Sources" / "Papers"
    papers_dir.mkdir(parents=True, exist_ok=True)
    if demo_papers_dir.exists():
        for p in demo_papers_dir.glob("*.md"):
            shutil.copy2(p, papers_dir / p.name)
            print(f"  [+] Restored paper note: {p.name}")

    # 2. Restore concepts
    demo_concepts_dir = archive_demo / "Concepts"
    concepts_dir = vault_root / "Knowledge" / "Concepts"
    concepts_dir.mkdir(parents=True, exist_ok=True)
    if demo_concepts_dir.exists():
        for c in demo_concepts_dir.glob("*.md"):
            shutil.copy2(c, concepts_dir / c.name)
            print(f"  [+] Restored concept note: {c.name}")

    # 3. Restore syntheses, matrix, canvas
    for synth_name in ["Literature Overview.md", "Method Taxonomy.md", "Research Gaps.md", "index.md"]:
        src_f = archive_demo / synth_name
        if src_f.exists():
            shutil.copy2(src_f, vault_root / "Knowledge" / synth_name)

    if (archive_demo / "comparison-matrix.md").exists():
        shutil.copy2(archive_demo / "comparison-matrix.md", vault_root / "Writing" / "comparison-matrix.md")

    if (archive_demo / "literature.canvas").exists():
        shutil.copy2(archive_demo / "literature.canvas", vault_root / "Maps" / "literature.canvas")

    # 4. Re-run pipeline to ensure registry & graph are 100% synchronized
    print("\n>> Re-synchronizing indices and validation...")
    subprocess.run([sys.executable, "-m", "kb_tools", "sync-registry", "--vault-dir", str(vault_root)], cwd=str(vault_root))
    subprocess.run([sys.executable, "-m", "kb_tools", "generate-canvas", "--vault-dir", str(vault_root)], cwd=str(vault_root))
    subprocess.run([sys.executable, "-m", "kb_tools", "lint", "--vault-dir", str(vault_root)], cwd=str(vault_root))

    print("\n[+] Demo examples restored successfully!")
    print("=" * 70)

if __name__ == "__main__":
    main()
