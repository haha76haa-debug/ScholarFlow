@echo off
setlocal
cd /d "%~dp0\.."
echo ======================================================================
echo  Restoring Demo Literature Network (????????)
echo ======================================================================
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" "Scripts\restore_demo.py"
) else (
    python "Scripts\restore_demo.py"
)
pause
