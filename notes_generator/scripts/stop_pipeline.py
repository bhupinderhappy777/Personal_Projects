"""
stop_pipeline.py
----------------
Stop pipeline script for the notes generator system.

This script creates the STOP_PIPELINE file, attempts to gracefully terminate all watcher processes,
and prints the last 2 log lines from each watcher for a final status update.

How it works:
  1. Creates STOP_PIPELINE file (signals all watchers to exit at next check).
  2. Finds all watcher processes by script name and sends terminate signal.
  3. Waits for watcher processes to exit (with timeout).
  4. Prints which watchers stopped and which did not.
  5. Prints the last 2 lines from each watcher's log file (searches recursively for timestamped subfolders).
"""

import time
from pathlib import Path
import psutil
import glob

WATCHERS = {
    "Video Watcher": "video_watcher.py",
    "Audio Watcher": "audio_watcher.py",
    "Transcript Watcher": "transcript_watcher.py",
}

def create_stop_file():
    """
    Creates the STOP_PIPELINE file in the parent directory to signal all watchers to exit.
    """
    stop_file = Path(__file__).parent.parent / "STOP_PIPELINE"
    stop_file.touch()
    print("[stop_pipeline] STOP_PIPELINE file created.")

def wait_for_watchers(timeout=30):
    """
    Attempts to terminate all watcher processes by PID and waits for them to exit.
    Returns a set of watcher names that are still running after the timeout.
    """
    print("[stop_pipeline] Attempting to terminate watcher processes by PID...")
    watcher_procs = {}
    for watcher, script in WATCHERS.items():
        for proc in psutil.process_iter(['name', 'cmdline', 'pid']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if script in cmdline:
                    watcher_procs[watcher] = proc
                    break
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
    # Terminate all found watcher processes
    for watcher, proc in watcher_procs.items():
        try:
            print(f"Terminating {watcher} (PID: {proc.pid})...")
            proc.terminate()
        except Exception as e:
            print(f"Failed to terminate {watcher} (PID: {proc.pid}): {e}")
    # Wait for all to exit
    gone, alive = psutil.wait_procs(list(watcher_procs.values()), timeout=timeout)
    still_running = set()
    for proc in alive:
        for watcher, p in watcher_procs.items():
            if p.pid == proc.pid:
                still_running.add(watcher)
    return still_running

def main():
    """
    Main entry point for stopping the pipeline and reporting watcher status and logs.
    """
    create_stop_file()
    still_running = wait_for_watchers()
    stopped = [w for w in WATCHERS if w not in still_running]
    if stopped:
        print("\nStopped watcher processes:")
        for w in stopped:
            print(f"- {w}")
    if still_running:
        print("\n[WARNING] These watcher processes did NOT stop within timeout:")
        for w in still_running:
            print(f"- {w}")
    else:
        print("\nAll watcher processes stopped successfully.")

    # Print last 2 lines from each watcher's log file (search recursively for timestamped subfolders)
    print("\n--- Last 2 log lines from each watcher ---")
    log_dir = Path(__file__).parent.parent / "logs"
    for watcher, script in WATCHERS.items():
        watcher_base = script.replace('.py', '')
        # Search recursively for log files matching watcher name
        pattern = str(log_dir / f"**/{watcher_base}*.log")
        log_files = sorted(glob.glob(pattern, recursive=True), reverse=True)
        if log_files:
            log_file = log_files[0]
            try:
                with open(log_file, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
                    print(f"\n[{watcher} - {log_file}]:")
                    for line in lines[-2:]:
                        print(line.rstrip())
            except Exception as e:
                print(f"Could not read log for {watcher}: {e}")
        else:
            print(f"\n[{watcher}]: No log file found.")

if __name__ == "__main__":
    main()
