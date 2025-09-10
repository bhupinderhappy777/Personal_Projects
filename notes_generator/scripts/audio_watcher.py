"""
Watches the Trainings_Audio folder for new .mp3 files and runs transcriber.py
to generate markdown transcripts automatically.
"""


import time
from pathlib import Path
import subprocess
import sys

def is_file_unlocked(filepath, retries=6, delay=5):
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
                print(f"[audio_watcher] File {filepath.name} is locked (attempt {attempt+1}/{retries}), retrying in {delay}s...")
                time.sleep(delay)
    print(f"[audio_watcher] File {filepath.name} is still locked after {retries} attempts. Skipping for now.")
    return False


# Import folder paths from config
from config import AUDIO_DIR, PROCESSED_AUDIO_FILE

def get_processed_files():
    """
    Reads the list of already processed files from the processed_transcriptions file.
    Returns a set of file paths as strings.
    """
    if not PROCESSED_AUDIO_FILE.exists():
        return set()
    with open(PROCESSED_AUDIO_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_processed_file(filename):
    """
    Appends a processed filename to the processed_transcriptions file.
    """
    with open(PROCESSED_AUDIO_FILE, "a", encoding="utf-8") as f:
        f.write(filename + "\n")

def main():
    """
    Main loop that watches the AUDIO_DIR for new .mp3 files.
    When a new file is found, it triggers transcriber.py and marks the file as processed.
    """
    print(f"Watching {AUDIO_DIR} for new .mp3 files...")
    processed = get_processed_files()
    while True:
        for file in AUDIO_DIR.glob("*.mp3"):
            if str(file) not in processed:
                print(f"New audio file detected: {file.name}")
                # Check if file is unlocked before processing
                if not is_file_unlocked(file, retries=6, delay=5):
                    print(f"[audio_watcher] Skipping {file.name} for now (still locked). Will check again later.")
                    continue
                transcriber_path = Path(__file__).parent / "transcriber.py"
                try:
                    subprocess.run(
                        [sys.executable, str(transcriber_path), str(file)],
                        check=True
                    )
                except Exception as e:
                    print(f"Error running transcriber.py for {file}: {e}")
                save_processed_file(str(file))
                processed.add(str(file))
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()
