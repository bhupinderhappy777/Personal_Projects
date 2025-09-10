
# Set a custom process title for easier identification in process lists
import setproctitle

"""
video_watcher.py
----------------
Watches a specified folder for new .mp4 files and triggers conversion to .mp3 audio.

This script continuously monitors a folder for new video files (.mp4).
When a new file is detected, it triggers the conversion process (converter.py).
Processed files are tracked to avoid duplicate processing.
The watcher can be stopped gracefully by creating a STOP_PIPELINE file in the parent directory.
"""

# Standard library imports

import time  # For sleep intervals between folder checks
from pathlib import Path  # For platform-independent file paths

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
                print(f"[video_watcher] File {filepath.name} is locked (attempt {attempt+1}/{retries}), retrying in {delay}s...")
                time.sleep(delay)
    print(f"[video_watcher] File {filepath.name} is still locked after {retries} attempts. Skipping for now.")
    return False



# Import watched directory and processed file from config
from config import WATCHED_VIDEOS_DIR, PROCESSED_VIDEOS_FILE



def get_processed_files():
    """
    Reads the processed files log and returns a set of normalized absolute processed file paths.
    Returns:
        set: Set of file paths (as strings) that have already been processed.
    """
    """
    Reads the processed files log and returns a set of normalized absolute processed file paths.
    Returns:
        set: Set of file paths (as strings) that have already been processed.
    """
    if PROCESSED_VIDEOS_FILE.exists():
        with open(PROCESSED_VIDEOS_FILE, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
        return set(str(Path(line).resolve()) for line in lines)
    return set()


def save_processed_file(filename):
    """
    Appends a filename to the processed files log.
    Args:
        filename (str): The path of the file to mark as processed.
    """
    """
    Appends a filename to the processed files log.
    Args:
        filename (str): The path of the file to mark as processed.
    """
    with open(PROCESSED_VIDEOS_FILE, 'a') as f:
        f.write(str(Path(filename).resolve()) + '\n')



def main():
    setproctitle.setproctitle("video_watcher.py")
    """
    Main loop that watches the directory for new .mp4 files.
    When a new file is found, triggers converter.py and marks the file as processed.
    Exits cleanly if STOP_PIPELINE file is detected.
    """
    print(f"[video_watcher] Watching {WATCHED_VIDEOS_DIR} for new .mp4 files...")
    processed = get_processed_files()
    stop_file = Path(__file__).parent.parent / "STOP_PIPELINE"
    while True:
        if stop_file.exists():
            print("[video_watcher] STOP_PIPELINE detected. Exiting watcher.")
            break
        for file in WATCHED_VIDEOS_DIR.glob('*.mp4'):
            file_path = str(file.resolve())
            if file_path not in processed:
                print(f"[video_watcher] New file detected: {file.name}")
                # Check if file is unlocked before processing
                if not is_file_unlocked(file, retries=6, delay=5):
                    print(f"[video_watcher] Skipping {file.name} for now (still locked). Will check again later.")
                    continue
                import subprocess, sys
                converter_path = Path(__file__).parent / 'converter.py'
                try:
                    process = subprocess.Popen([
                        sys.executable, str(converter_path), str(file)
                    ], stdout=sys.stdout, stderr=sys.stderr)
                    # While the conversion runs, check for STOP_PIPELINE
                    while process.poll() is None:
                        if stop_file.exists():
                            print("[video_watcher] STOP_PIPELINE detected during processing. Terminating subprocess.")
                            process.terminate()
                            process.wait(timeout=5)
                            break
                        time.sleep(1)
                    if process.returncode not in (0, None):
                        print(f"[video_watcher] Error: converter.py exited with code {process.returncode} for {file}")
                except Exception as e:
                    print(f"[video_watcher] Error running converter.py for {file}: {e}")
                file_path = str(file.resolve())
                save_processed_file(file_path)  # Mark as processed
                processed.add(file_path)
        time.sleep(5)  # Wait before checking again

# Entry point for the script
if __name__ == "__main__":
    main()
