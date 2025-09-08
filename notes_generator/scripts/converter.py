"""
Converts .mp4 files in the watched folder to .mp3 in the 'audio' directory using ffmpeg.

This script takes a .mp4 video file and extracts the audio as an .mp3 file.
It is intended to be called from the command line or another script.
"""

# Standard library imports
import subprocess  # For running ffmpeg as a subprocess
from pathlib import Path  # For platform-independent file paths
import sys  # For command-line argument handling


# Directory containing the .mp4 files to convert
WATCHED_DIR = Path(r"C:\Users\bhupi\Videos\Zoom_Trainings")
# Directory where the .mp3 files will be saved
AUDIO_DIR = Path(r"G:\Other computers\My Computer\Documents\Trainings_Audio")
# Ensure the audio output directory exists
AUDIO_DIR.mkdir(exist_ok=True)


def convert_to_mp3(mp4_path):
    """
    Converts a .mp4 video file to an .mp3 audio file using ffmpeg.
    Args:
        mp4_path (Path): Path to the .mp4 file to convert.
    Returns:
        Path: Path to the created .mp3 file.
    """
    mp3_path = AUDIO_DIR / (mp4_path.stem + '.mp3')  # Output .mp3 path
    # ffmpeg command to extract audio
    cmd = [
        'ffmpeg', '-y', '-i', str(mp4_path),  # -y to overwrite, -i for input
        '-vn',  # No video
        '-acodec', 'libmp3lame',  # Use mp3 encoder
        str(mp3_path)
    ]
    subprocess.run(cmd, check=True)  # Run the command, raise error if fails
    print(f"Converted {mp4_path.name} to {mp3_path.name}")
    return mp3_path


# Entry point for the script
if __name__ == "__main__":
    # Check for required command-line argument
    if len(sys.argv) < 2:
        print("Usage: python converter.py <video_file.mp4>")
        sys.exit(1)
    mp4_file = Path(sys.argv[1])  # Get the input file path
    if not mp4_file.exists():
        print(f"File not found: {mp4_file}")
        sys.exit(1)
    convert_to_mp3(mp4_file)
