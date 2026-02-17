# Script d'exécution pour Windows PowerShell
# Naturalisation CAE Prediction

Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "  Naturalisation CAE Prediction v1.0" -ForegroundColor Cyan
Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Vérifier venv
$venv_path = ".\.venv\Scripts\Activate.ps1"
if (-not (Test-Path $venv_path)) {
    Write-Host "[ERROR] Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create it with: python -m venv .venv" -ForegroundColor Yellow
    exit 1
}

Write-Host "[INFO] Activating virtual environment..." -ForegroundColor Yellow
& $venv_path

Write-Host "[INFO] Running prediction pipeline..." -ForegroundColor Yellow
Write-Host ""

# Run main script
python src/main.py

if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
    Write-Host "  Pipeline completed successfully!" -ForegroundColor Green
    Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Green
}
else {
    Write-Host ""
    Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Red
    Write-Host "  Pipeline failed with exit code: $LASTEXITCODE" -ForegroundColor Red
    Write-Host "═══════════════════════════════════════════════════════════════════" -ForegroundColor Red
    exit 1
}
