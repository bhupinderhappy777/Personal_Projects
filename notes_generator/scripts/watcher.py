"""
Watches a specified folder for new .mp4 files and triggers conversion.

This script continuously monitors a folder for new video files (.mp4).
When a new file is detected, it can trigger a conversion process (e.g., to .mp3).
Processed files are tracked to avoid duplicate processing.
"""

# Standard library imports
import time  # For sleep intervals between folder checks
import os    # (Not used, but commonly imported for file ops)
from pathlib import Path  # For platform-independent file paths



# Import folder paths from config
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
        # Iterate over all .mp4 files in the watched directory
        for file in WATCHED_VIDEOS_DIR.glob('*.mp4'):
            # If the file hasn't been processed yet
            if str(file) not in processed:
                print(f"New file detected: {file.name}")
                # Trigger the converter script to convert .mp4 to .mp3
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
