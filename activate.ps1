# Audio Extractor UI - Virtual Environment Activation Script (Windows PowerShell)
# Usage: .\activate.ps1

Write-Host "🔄 Activating virtual environment..." -ForegroundColor Cyan

# Check if virtual environment exists
if (-not (Test-Path "venv\Scripts\Activate.ps1")) {
    Write-Host "❌ Virtual environment not found. Creating it now..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate the virtual environment
& "venv\Scripts\Activate.ps1"

if ($LASTEXITCODE -eq 0) {
    Write-Host "✅ Virtual environment activated!" -ForegroundColor Green
    Write-Host "📦 Installing/updating dependencies..." -ForegroundColor Cyan
    
    # Install requirements if they exist
    if (Test-Path "requirements.txt") {
        pip install -r requirements.txt
    }
    
    # Install development requirements if they exist
    if (Test-Path "requirements-dev.txt") {
        pip install -r requirements-dev.txt
    }
    
    Write-Host "🚀 Ready to develop! Use 'deactivate' to exit the virtual environment." -ForegroundColor Green
} else {
    Write-Host "❌ Failed to activate virtual environment" -ForegroundColor Red
}
