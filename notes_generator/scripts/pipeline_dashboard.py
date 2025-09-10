
"""
pipeline_dashboard.py
---------------------
TUI Dashboard for Notes Generator Pipeline using rich.

Shows live status of video, audio, and transcript watchers, including their PIDs and recent log output.
Press 'q' to stop the pipeline and exit the dashboard (calls stop_pipeline.py).
"""

import time
from pathlib import Path
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.text import Text
import sys
import threading
import platform
import psutil
if platform.system() == "Windows":
    import msvcrt

def get_logs_dict(log_dir):
    """
    Returns a dictionary mapping watcher names to their log file paths.
    """
    log_dir = Path(log_dir)
    return {
        "Video Watcher (out)": log_dir / "video_watcher.log",
        "Video Watcher (err)": log_dir / "video_watcher.err.log",
        "Audio Watcher (out)": log_dir / "audio_watcher.log",
        "Audio Watcher (err)": log_dir / "audio_watcher.err.log",
        "Transcript Watcher (out)": log_dir / "transcript_watcher.log",
        "Transcript Watcher (err)": log_dir / "transcript_watcher.err.log",
    }

console = Console()

def tail_log(path, n=10, filter_errors=False):
    """
    Returns the last n lines from a log file. Optionally filters for error lines.
    """
    if not path.exists():
        return ["(no log)"]
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    if filter_errors:
        # Only keep lines that look like real errors (case-insensitive)
        error_keywords = ["error", "fail", "denied", "not found", "exception", "traceback"]
        filtered = [l for l in lines if any(k in l.lower() for k in error_keywords)]
        lines = filtered if filtered else ["(no errors detected)"]
    return lines[-n:] if len(lines) >= n else lines

def make_dashboard(logs):
    """
    Builds and returns a rich Panel containing a table of watcher status and recent logs.
    """
    table = Table(title="Notes Generator Pipeline Status", expand=True)
    table.add_column("Watcher", style="bold cyan", no_wrap=True)
    table.add_column("Status", style="bold green", no_wrap=True)
    table.add_column("Last 10 Log Lines", style="white")

    # Helper to check if a watcher process is running
    def get_watcher_process_info(watcher_name):
        """Return (is_running, pid) for the first matching process, else (False, '')"""
        for proc in psutil.process_iter(['cmdline', 'pid']):
            try:
                cmdline = ' '.join(proc.info['cmdline']) if proc.info['cmdline'] else ''
                if watcher_name in cmdline:
                    return True, proc.info['pid']
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False, ''

    watcher_map = {
        "Video Watcher": "video_watcher.py",
        "Audio Watcher": "audio_watcher.py",
        "Transcript Watcher": "transcript_watcher.py",
    }

    for name, log_path in logs.items():
        # Only filter for errors in err logs
        filter_errors = name.endswith("(err)")
        log_lines = tail_log(log_path, 10, filter_errors=filter_errors)
        log_text = "".join(log_lines).strip()
        # Determine watcher type for status
        base_name = name.split()[0] + " Watcher"
        status = ""
        if base_name in watcher_map and not filter_errors:
            is_running, pid = get_watcher_process_info(watcher_map[base_name])
            if is_running:
                status = f"Running (PID: {pid})"
            else:
                status = "Stopped"
        table.add_row(name, status, log_text or "(no output)")
    return Panel(table, title="Pipeline Dashboard (out = stdout, err = stderr, err logs filtered)", border_style="green")

def stop_pipeline():
    """
    Calls stop_pipeline.py to gracefully stop all watcher processes and print their final logs.
    """
    import subprocess
    stop_script = Path(__file__).parent / "stop_pipeline.py"
    subprocess.run([sys.executable, str(stop_script)])
    print("\n[dashboard] Pipeline stop script finished. Exiting dashboard...")

def main():
    """
    Main entry point for the dashboard. Monitors watcher status and logs, and allows stopping the pipeline with 'q'.
    """
    log_dir = sys.argv[1] if len(sys.argv) > 1 else "notes_generator/logs"
    logs = get_logs_dict(log_dir)
    print("Press 'q' to stop the pipeline and exit dashboard.")
    stop_event = threading.Event()

    def key_listener():
        try:
            if platform.system() == "Windows":
                while not stop_event.is_set():
                    if msvcrt.kbhit():
                        key = msvcrt.getwch()
                        if key.lower() == 'q':
                            stop_event.set()
                            break
                    time.sleep(0.1)
            else:
                while not stop_event.is_set():
                    key = console.input()
                    if key.strip().lower() == 'q':
                        stop_event.set()
        except (KeyboardInterrupt, EOFError):
            stop_event.set()

    listener_thread = threading.Thread(target=key_listener, daemon=True)
    listener_thread.start()


    with Live(make_dashboard(logs), refresh_per_second=1, console=console) as live:
        while not stop_event.is_set():
            time.sleep(1)
            live.update(make_dashboard(logs))

    stop_pipeline()

if __name__ == "__main__":
    main()