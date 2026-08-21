$ErrorActionPreference = "Stop"
$VaultDir = Split-Path -Parent $PSScriptRoot
Set-Location $VaultDir

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " Running Zotero-Obsidian Academic Knowledge Base Automation Pipeline" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$PythonExe = "python"
if (Test-Path "$VaultDir\.venv\Scripts\python.exe") {
    $PythonExe = "$VaultDir\.venv\Scripts\python.exe"
}

& $PythonExe "$VaultDir\Scripts\run_pipeline.py"
if ($LASTEXITCODE -eq 0) {
    Write-Host "`nPipeline completed successfully!" -ForegroundColor Green
} else {
    Write-Host "`nPipeline failed with exit code $LASTEXITCODE" -ForegroundColor Red
}
