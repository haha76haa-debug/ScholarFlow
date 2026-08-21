@echo off
setlocal
cd /d "%~dp0\.."
echo ======================================================================
echo  Resetting Vault to Clean Blank Slate (????????)
echo ======================================================================
if exist ".venv\Scripts\python.exe" (
    ".venv\Scripts\python.exe" "Scripts\clean_vault.py"
) else (
    python "Scripts\clean_vault.py"
)
pause
