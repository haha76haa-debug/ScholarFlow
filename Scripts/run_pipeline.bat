@echo off
setlocal
cd /d "%~dp0\.."
echo ======================================================================
echo  Running Zotero-Obsidian Academic Knowledge Base Automation Pipeline
echo ======================================================================
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" "Scripts\run_pipeline.py"
) else (
    python "Scripts\run_pipeline.py"
)
pause
