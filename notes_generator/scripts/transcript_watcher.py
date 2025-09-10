
# Set a custom process title for easier identification in process lists
import setproctitle

"""
transcript_watcher.py
---------------------
Watches the transcripts folder for new .txt files and triggers formatting/summarization.

This script continuously monitors the transcripts folder for new .txt files.
When a new file is detected, it triggers the formatting/summarization process (editor.py).
Processed files are tracked to avoid duplicate processing.
The watcher can be stopped gracefully by creating a STOP_PIPELINE file in the parent directory.
"""


import time
from pathlib import Path
import subprocess
import sys

def is_file_unlocked(filepath, retries=6, delay=5):
    """
    Utility function to check if a file is unlocked (not in use by another process).
    Retries a few times before giving up.
    """
    """
    Checks if a file can be opened for exclusive access. Retries if locked.
    Args:
        filepath (Path): Path to the file.
        retries (int): Number of times to retry.
        delay (int): Seconds to wait between retries.
    Returns:
        bool: True if file is unlocked, False otherwise.
    """
    for attempt in range(retries):
        try:
            with open(filepath, 'rb+'):
                return True
        except (PermissionError, OSError):
            if attempt < retries - 1:
                print(f"[transcript_watcher] File {filepath.name} is locked (attempt {attempt+1}/{retries}), retrying in {delay}s...")
                time.sleep(delay)
    print(f"[transcript_watcher] File {filepath.name} is still locked after {retries} attempts. Skipping for now.")
    return False


# Import folder paths from config
from config import TRANSCRIPTS_DIR, PROCESSED_TRANSCRIPTS_FILE


def get_processed_files():
    """
    Reads the list of already processed files from the processed_editor file.
    Returns a set of normalized absolute file paths as strings.
    """
    """
    Reads the list of already processed files from the processed_editor file.
    Returns a set of normalized absolute file paths as strings.
    """
    if not PROCESSED_TRANSCRIPTS_FILE.exists():
        return set()
    with open(PROCESSED_TRANSCRIPTS_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return set(str(Path(line).resolve()) for line in lines)


def save_processed_file(filename):
    """
    Appends a processed filename to the processed_editor file.
    """
    """
    Appends a processed filename to the processed_editor file.
    """
    with open(PROCESSED_TRANSCRIPTS_FILE, "a", encoding="utf-8") as f:
        f.write(str(Path(filename).resolve()) + "\n")



def main():
    setproctitle.setproctitle("transcript_watcher.py")
    """
    Main loop that watches the TRANSCRIPTS_DIR for new .txt files.
    When a new file is found, triggers editor.py and marks the file as processed.
    Exits cleanly if STOP_PIPELINE file is detected.
    """
    print(f"[transcript_watcher] Watching folder: {TRANSCRIPTS_DIR}")
    processed = get_processed_files()
    stop_file = Path(__file__).parent.parent / "STOP_PIPELINE"
    while True:
        if stop_file.exists():
            print("[transcript_watcher] STOP_PIPELINE detected. Exiting watcher.")
            break
        for file in TRANSCRIPTS_DIR.glob("*.txt"):
            file_path = str(file.resolve())
            if file_path not in processed:
                print(f"[transcript_watcher] New transcript detected: {file.name}")
                # Check if file is unlocked before processing
                if not is_file_unlocked(file, retries=6, delay=5):
                    print(f"[transcript_watcher] Skipping {file.name} for now (still locked). Will check again later.")
                    continue
                editor_path = Path(__file__).parent / "editor.py"
                try:
                    process = subprocess.Popen(
                        [sys.executable, str(editor_path), str(file)],
                        stdout=sys.stdout,
                        stderr=sys.stderr
                    )
                    # While the formatting/summarization runs, check for STOP_PIPELINE
                    while process.poll() is None:
                        if stop_file.exists():
                            print("[transcript_watcher] STOP_PIPELINE detected during processing. Terminating subprocess.")
                            process.terminate()
                            process.wait(timeout=5)
                            break
                        time.sleep(1)
                    if process.returncode not in (0, None):
                        print(f"[transcript_watcher] Error: editor.py exited with code {process.returncode} for {file}")
                except Exception as e:
                    print(f"[transcript_watcher] Error running editor.py for {file}: {e}")
                file_path = str(file.resolve())
                save_processed_file(file_path)
                processed.add(file_path)
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()
