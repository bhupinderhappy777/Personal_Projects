# PowerShell script to activate venv and start all pipeline watcher scripts with logging

# Activate the virtual environment
& "G:\Other computers\My Computer\Documents\Personal_Projects\.venv\Scripts\Activate.ps1"

# Define log directory
$logDir = "G:\Other computers\My Computer\Documents\Personal_Projects\notes_generator\logs"
if (!(Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir | Out-Null
}

# Start watcher.py (video watcher)
Start-Process -NoNewWindow -FilePath python -ArgumentList "scripts\watcher.py" -RedirectStandardOutput "$logDir\watcher.log" -RedirectStandardError "$logDir\watcher.err.log"

# Start audio_watcher.py (audio watcher)
Start-Process -NoNewWindow -FilePath python -ArgumentList "scripts\audio_watcher.py" -RedirectStandardOutput "$logDir\audio_watcher.log" -RedirectStandardError "$logDir\audio_watcher.err.log"

# Start transcript_watcher.py (transcript watcher)
Start-Process -NoNewWindow -FilePath python -ArgumentList "scripts\transcript_watcher.py" -RedirectStandardOutput "$logDir\transcript_watcher.log" -RedirectStandardError "$logDir\transcript_watcher.err.log"

Write-Host "All pipeline watchers started in background processes. Logs are in $logDir."
