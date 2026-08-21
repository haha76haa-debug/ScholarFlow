@echo off
chcp 65001 >nul
echo ===================================================
echo [*] Pushing ScholarFlow to GitHub...
echo ===================================================
git push -u origin main --force
echo ===================================================
echo [+] Push Completed! Check your repo on GitHub:
echo     https://github.com/haha76haa-debug/ScholarFlow
echo ===================================================
pause
