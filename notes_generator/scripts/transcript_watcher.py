"""
Watches the transcripts folder for new .md files and triggers editor.py to format and summarize notes using Gemini API.
"""

import time
from pathlib import Path
import subprocess
import sys


# Import folder paths from config
from config import TRANSCRIPTS_DIR, PROCESSED_TRANSCRIPTS_FILE


def get_processed_files():
    """
    Reads the list of already processed files from the processed_editor file.
    Returns a set of file paths as strings.
    """
    if not PROCESSED_TRANSCRIPTS_FILE.exists():
        return set()
    with open(PROCESSED_TRANSCRIPTS_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())


def save_processed_file(filename):
    """
    Appends a processed filename to the processed_editor file.
    """
    with open(PROCESSED_TRANSCRIPTS_FILE, "a", encoding="utf-8") as f:
        f.write(filename + "\n")


def main():
    """
    Main loop that watches the TRANSCRIPTS_DIR for new .md files.
    When a new file is found, it triggers editor.py and marks the file as processed.
    """
    print(f"Watching {TRANSCRIPTS_DIR} for new .md transcript files...")
    processed = get_processed_files()
    while True:
        for file in TRANSCRIPTS_DIR.glob("*.md"):
            if str(file) not in processed and not file.name.startswith("formatted_") and not file.name.startswith("summary_"):
                print(f"New transcript detected: {file.name}")
                editor_path = Path(__file__).parent / "editor.py"
                try:
                    subprocess.run(
                        [sys.executable, str(editor_path), str(file)],
                        check=True
                    )
                except Exception as e:
                    print(f"Error running editor.py for {file}: {e}")
                save_processed_file(str(file))
                processed.add(str(file))
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()
