
# PowerShell script to activate venv and start all pipeline watcher scripts in parallel, showing output in the same terminal

& "G:\Other computers\My Computer\Documents\Personal_Projects\.venv\Scripts\Activate.ps1"

Write-Host "Starting all pipeline watchers in parallel. Output will be available via Receive-Job."

# Start all watcher scripts in parallel jobs
$videoJob = Start-Job -ScriptBlock { python "scripts/video_watcher.py" }
$audioJob = Start-Job -ScriptBlock { python "scripts/audio_watcher.py" }
$transcriptJob = Start-Job -ScriptBlock { python "scripts/transcript_watcher.py" }

Write-Host "All pipeline watchers started as background jobs. Use 'Get-Job' to see status, 'Receive-Job -Id <id>' to view output, and 'Stop-Job -Id <id>' to stop."
