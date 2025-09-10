
"""
transcriber.py
--------------
Transcribes .mp3 files in the audio folder to text using OpenAI Whisper CLI.

This script is called by audio_watcher.py when a new .mp3 file is detected.
It uses the Whisper CLI to generate a .txt transcript in the transcripts folder.
"""

from pathlib import Path
import sys
import subprocess


# Import transcript directory from config
from config import TRANSCRIPTS_DIR
# Ensure the transcript directory exists
TRANSCRIPTS_DIR.mkdir(exist_ok=True)

def transcribe(mp3_path):
    """
    Transcribes a single .mp3 file to text using the Whisper CLI.
    The output is saved as a .txt file in the transcript directory.
    """
    """
    Transcribes a single .mp3 file to markdown using the Whisper CLI.
    The output is saved as a .md file in the TRANSCRIPT_DIR.
    """
    print ("Transcribing:", mp3_path.name)
    # Build the whisper CLI command
    cmd = [
        'whisper', str(mp3_path), '--model', 'tiny', '--output_format', 'txt', '--output_dir', str(TRANSCRIPTS_DIR)
    ]
    # Run the whisper command to generate a .txt transcript and show progress in real time
    process = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    process.communicate()
    if process.returncode != 0:
        raise subprocess.CalledProcessError(process.returncode, cmd)
    txt_path = TRANSCRIPTS_DIR / (mp3_path.stem + '.txt')
    print(f"Transcribed {mp3_path.name} to {txt_path.name}")
    return txt_path

if __name__ == "__main__":
    # Entry point: expects a .mp3 file path as argument
    if len(sys.argv) < 2:
        print("Usage: python transcriber.py <audio_file.mp3>")
        sys.exit(1)
    mp3_file = Path(sys.argv[1])
    if not mp3_file.exists():
        print(f"File not found: {mp3_file}")
        sys.exit(1)
    # Transcribe the provided .mp3 file
    transcribe(mp3_file)