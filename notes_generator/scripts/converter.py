

"""
converter.py
------------
Converts .mp4 files in the watched folder to .mp3 audio using ffmpeg-python.

This script is called by video_watcher.py when a new .mp4 file is detected.
It uses ffmpeg-python to extract audio and save it as .mp3 in the audio folder.
"""


# Standard library imports
from pathlib import Path  # For platform-independent file paths
import sys  # For command-line argument handling

# Third-party import
import ffmpeg  # ffmpeg-python package




# Import folder paths from config
from config import WATCHED_VIDEOS_DIR, AUDIO_DIR
# Ensure the audio output directory exists
AUDIO_DIR.mkdir(exist_ok=True)



def convert_to_mp3(mp4_path):
    """
    Converts a .mp4 video file to an .mp3 audio file using ffmpeg-python.
    Args:
        mp4_path (Path): Path to the .mp4 file to convert.
    Returns:
        Path: Path to the created .mp3 file.
    """
    """
    Converts a .mp4 video file to an .mp3 audio file using ffmpeg-python.
    Args:
        mp4_path (Path): Path to the .mp4 file to convert.
    Returns:
        Path: Path to the created .mp3 file.
    """
    mp3_path = AUDIO_DIR / (mp4_path.stem + '.mp3')  # Output .mp3 path
    try:
        (
            ffmpeg
            .input(str(mp4_path))
            .output(str(mp3_path), acodec='libmp3lame', vn=None)
            .overwrite_output()
            .run(quiet=False)
        )
        print(f"Converted {mp4_path.name} to {mp3_path.name}")
    except ffmpeg.Error as e:
        print(f"ffmpeg error: {e}")
        raise
    return mp3_path



# Entry point for the script
if __name__ == "__main__":
    # Entry point: expects a .mp4 file path as argument
    if len(sys.argv) < 2:
        print("Usage: python converter.py <video_file.mp4>")
        sys.exit(1)
    mp4_file = Path(sys.argv[1])
    if not mp4_file.exists():
        print(f"File not found: {mp4_file}")
        sys.exit(1)
    convert_to_mp3(mp4_file)
