"""
Watches a specified folder for new .mp4 files and triggers conversion.

This script continuously monitors a folder for new video files (.mp4).
When a new file is detected, it can trigger a conversion process (e.g., to .mp3).
Processed files are tracked to avoid duplicate processing.
"""

# Standard library imports

import time  # For sleep intervals between folder checks
from pathlib import Path  # For platform-independent file paths

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
                print(f"[video_watcher] File {filepath.name} is locked (attempt {attempt+1}/{retries}), retrying in {delay}s...")
                time.sleep(delay)
    print(f"[video_watcher] File {filepath.name} is still locked after {retries} attempts. Skipping for now.")
    return False



# Import watched directory and processed file from config
from config import WATCHED_VIDEOS_DIR, PROCESSED_VIDEOS_FILE



def get_processed_files():
    """
    Reads the processed files log and returns a set of processed file paths.
    Returns:
        set: Set of file paths (as strings) that have already been processed.
    """
    if PROCESSED_VIDEOS_FILE.exists():
        with open(PROCESSED_VIDEOS_FILE, 'r') as f:
            return set(line.strip() for line in f)
    return set()


def save_processed_file(filename):
    """
    Appends a filename to the processed files log.
    Args:
        filename (str): The path of the file to mark as processed.
    """
    with open(PROCESSED_VIDEOS_FILE, 'a') as f:
        f.write(filename + '\n')


def main():
    """
    Main loop that watches the directory for new .mp4 files.
    When a new file is found, it can trigger a conversion process
    and marks the file as processed.
    """
    print(f"Watching {WATCHED_VIDEOS_DIR} for new .mp4 files...")
    processed = get_processed_files()
    while True:
        for file in WATCHED_VIDEOS_DIR.glob('*.mp4'):
            if str(file) not in processed:
                print(f"New file detected: {file.name}")
                # Check if file is unlocked before processing
                if not is_file_unlocked(file, retries=6, delay=5):
                    print(f"[video_watcher] Skipping {file.name} for now (still locked). Will check again later.")
                    continue
                import subprocess, sys
                converter_path = Path(__file__).parent / 'converter.py'
                try:
                    subprocess.run([
                        sys.executable, str(converter_path), str(file)
                    ], check=True)
                except Exception as e:
                    print(f"Error running converter.py for {file}: {e}")
                save_processed_file(str(file))  # Mark as processed
                processed.add(str(file))
        time.sleep(5)  # Wait before checking again

# Entry point for the script
if __name__ == "__main__":
    main()
