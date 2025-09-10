
# Set a custom process title for easier identification in process lists
import setproctitle

"""
audio_watcher.py
----------------
Watches the audio folder for new .mp3 files and triggers transcription.

This script continuously monitors the audio folder for new .mp3 files.
When a new file is detected, it triggers the transcription process (transcriber.py).
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
                print(f"[audio_watcher] File {filepath.name} is locked (attempt {attempt+1}/{retries}), retrying in {delay}s...")
                time.sleep(delay)
    print(f"[audio_watcher] File {filepath.name} is still locked after {retries} attempts. Skipping for now.")
    return False


# Import folder paths from config
from config import AUDIO_DIR, PROCESSED_AUDIO_FILE

def get_processed_files():
    """
    Reads the list of already processed files from the processed_audios file.
    Returns a set of normalized absolute file paths as strings.
    """
    """
    Reads the list of already processed files from the processed_audios file.
    Returns a set of normalized absolute file paths as strings.
    """
    if not PROCESSED_AUDIO_FILE.exists():
        return set()
    with open(PROCESSED_AUDIO_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    return set(str(Path(line).resolve()) for line in lines)

def save_processed_file(filename):
    """
    Appends a processed filename to the processed_transcriptions file.
    """
    """
    Appends a processed filename to the processed_transcriptions file.
    """
    with open(PROCESSED_AUDIO_FILE, "a", encoding="utf-8") as f:
        f.write(str(Path(filename).resolve()) + "\n")


def main():
    setproctitle.setproctitle("audio_watcher.py")
    """
    Main loop that watches the AUDIO_DIR for new .mp3 files.
    When a new file is found, triggers transcriber.py and marks the file as processed.
    Exits cleanly if STOP_PIPELINE file is detected.
    """
    print(f"[audio_watcher] Watching {AUDIO_DIR} for new .mp3 files...")
    processed = get_processed_files()
    stop_file = Path(__file__).parent.parent / "STOP_PIPELINE"
    while True:
        if stop_file.exists():
            print("[audio_watcher] STOP_PIPELINE detected. Exiting watcher.")
            break
        for file in AUDIO_DIR.glob("*.mp3"):
            file_path = str(file.resolve())
            if file_path not in processed:
                print(f"[audio_watcher] New audio file detected: {file.name}")
                # Check if file is unlocked before processing
                if not is_file_unlocked(file, retries=6, delay=5):
                    print(f"[audio_watcher] Skipping {file.name} for now (still locked). Will check again later.")
                    continue
                transcriber_path = Path(__file__).parent / "transcriber.py"
                try:
                    process = subprocess.Popen(
                        [sys.executable, str(transcriber_path), str(file)],
                        stdout=sys.stdout,
                        stderr=sys.stderr
                    )
                    # While the transcription runs, check for STOP_PIPELINE
                    while process.poll() is None:
                        if stop_file.exists():
                            print("[audio_watcher] STOP_PIPELINE detected during processing. Terminating subprocess.")
                            process.terminate()
                            process.wait(timeout=5)
                            break
                        time.sleep(1)
                    if process.returncode not in (0, None):
                        print(f"[audio_watcher] Error: transcriber.py exited with code {process.returncode} for {file}")
                except Exception as e:
                    print(f"[audio_watcher] Error running transcriber.py for {file}: {e}")
                save_processed_file(file_path)
                processed.add(file_path)
        time.sleep(5)  # Check every 5 seconds

if __name__ == "__main__":
    main()
