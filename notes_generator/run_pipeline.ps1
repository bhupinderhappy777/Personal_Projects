
# PowerShell script to activate venv, start all pipeline watcher scripts, and launch the dashboard in a new window

& "G:\Other computers\My Computer\Documents\Personal_Projects\.venv\Scripts\Activate.ps1"

# Create a timestamped log subfolder for this run
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$logDir = "G:\Other computers\My Computer\Documents\Personal_Projects\notes_generator\logs\$timestamp"
if (!(Test-Path $logDir)) {
	New-Item -ItemType Directory -Path $logDir | Out-Null
}

Write-Host "Starting all pipeline watchers in parallel. Logs will be saved in $logDir."

# Start all watcher scripts in parallel jobs, appending logs
Start-Process -NoNewWindow -FilePath python -ArgumentList "scripts/video_watcher.py" -RedirectStandardOutput "$logDir/video_watcher.log" -RedirectStandardError "$logDir/video_watcher.err.log" 
Start-Process -NoNewWindow -FilePath python -ArgumentList "scripts/audio_watcher.py" -RedirectStandardOutput "$logDir/audio_watcher.log" -RedirectStandardError "$logDir/audio_watcher.err.log" 
Start-Process -NoNewWindow -FilePath python -ArgumentList "scripts/transcript_watcher.py" -RedirectStandardOutput "$logDir/transcript_watcher.log" -RedirectStandardError "$logDir/transcript_watcher.err.log" 

# Start the dashboard in a new PowerShell window
Start-Process pwsh -ArgumentList "-NoExit", "-Command", "& 'python' 'notes_generator/scripts/pipeline_dashboard.py' '$logDir'" -WindowStyle Normal

Write-Host "All pipeline watchers started. Dashboard launched in a new window. Logs for this run are in: $logDir"
