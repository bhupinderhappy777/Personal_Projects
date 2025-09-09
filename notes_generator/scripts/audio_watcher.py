"""
Watches the Trainings_Audio folder for new .mp3 files and runs transcriber.py
to generate markdown transcripts automatically.
"""

import time
from pathlib import Path
import subprocess
import sys

AUDIO_DIR = Path(r"G:\Other computers\My Computer\Documents\Trainings_Audio")
PROCESSED_FILE = AUDIO_DIR / "processed_transcriptions.txt"

def get_processed_files():
    """
    Reads the list of already processed files from the processed_transcriptions file.
    Returns a set of file paths as strings.
    """
    if not PROCESSED_FILE.exists():
        return set()
    with open(PROCESSED_FILE, "r", encoding="utf-8") as f:
        return set(line.strip() for line in f if line.strip())

def save_processed_file(filename):
    """
    Appends a processed filename to the processed_transcriptions file.
    """
    with open(PROCESSED_FILE, "a", encoding="utf-8") as f:
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
                # Trigger the transcriber script
            
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
