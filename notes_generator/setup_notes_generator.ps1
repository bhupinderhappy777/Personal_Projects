# setup_notes_generator.ps1
# PowerShell script to guide a user through initializing the Notes Generator pipeline on a new system

Write-Host "=== Notes Generator Pipeline Setup ===" -ForegroundColor Cyan

# 1. Check for Python
Write-Host "Checking for Python installation..."
$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    Write-Host "Python is not installed or not in PATH. Please install Python 3.8+ and re-run this script." -ForegroundColor Red
    exit 1
}

# 2. Create virtual environment
Write-Host "Creating virtual environment (.venv)..."
python -m venv .venv

# 3. Activate virtual environment
Write-Host "Activating virtual environment..."
.\.venv\Scripts\Activate.ps1

# 4. Install dependencies
Write-Host "Installing Python dependencies from requirements.txt..."
pip install --upgrade pip
pip install -r requirements.txt

# 5. Check for ffmpeg
Write-Host "Checking for ffmpeg..."
$ffmpeg = Get-Command ffmpeg -ErrorAction SilentlyContinue
if (-not $ffmpeg) {
    Write-Host "ffmpeg is not installed or not in PATH. Please install ffmpeg and ensure it is available in your PATH." -ForegroundColor Yellow
    Write-Host "Download from: https://ffmpeg.org/download.html"
} else {
    Write-Host "ffmpeg found."
}

# 6. Prompt for Gemini API key
if (-not $env:GOOGLE_API_KEY) {
    $apiKey = Read-Host "Enter your Gemini API key (will be set for this session)"
    $env:GOOGLE_API_KEY = $apiKey
    Write-Host "GOOGLE_API_KEY set for this session."
} else {
    Write-Host "GOOGLE_API_KEY already set."
}

Write-Host "\nSetup complete! Please review scripts/config.py and update any folder paths as needed for your system." -ForegroundColor Green
Write-Host "You can now run the pipeline with: .\run_pipeline.ps1" -ForegroundColor Green
