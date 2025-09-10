"""
TUI Dashboard for Notes Generator Pipeline using rich
Shows live status of video, audio, and transcript watchers.
"""

import time
from pathlib import Path
from rich.live import Live
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.text import Text


import sys

def get_logs_dict(log_dir):
    log_dir = Path(log_dir)
    return {
        "Video Watcher": log_dir / "video_watcher.log",
        "Audio Watcher": log_dir / "audio_watcher.log",
        "Transcript Watcher": log_dir / "transcript_watcher.log",
    }

console = Console()

def tail_log(path, n=10):
    if not path.exists():
        return ["(no log)"]
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    return lines[-n:] if len(lines) >= n else lines

def make_dashboard(logs):
    table = Table(title="Notes Generator Pipeline Status", expand=True)
    table.add_column("Watcher", style="bold cyan", no_wrap=True)
    table.add_column("Last 10 Log Lines", style="white")
    for name, log_path in logs.items():
        log_lines = tail_log(log_path, 10)
        log_text = "".join(log_lines).strip()
        table.add_row(name, log_text or "(no output)")
    return Panel(table, title="Pipeline Dashboard", border_style="green")


def main():
    log_dir = sys.argv[1] if len(sys.argv) > 1 else "notes_generator/logs"
    logs = get_logs_dict(log_dir)
    with Live(make_dashboard(logs), refresh_per_second=1, console=console) as live:
        while True:
            time.sleep(1)
            live.update(make_dashboard(logs))

if __name__ == "__main__":
    main()
