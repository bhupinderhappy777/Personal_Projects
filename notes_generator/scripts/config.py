"""
Central configuration for all folder paths and settings used in the notes generator pipeline.
Update these values to change locations globally.
"""
from pathlib import Path

# Folder to watch for new .mp4 video files
WATCHED_VIDEOS_DIR = Path(r"C:\Users\bhupi\Videos\Zoom_Trainings")
# File to keep track of processed video files
PROCESSED_VIDEOS_FILE = WATCHED_VIDEOS_DIR / "processed_files.txt"

# Folder to save .mp3 audio files
AUDIO_DIR = Path(r"G:\Other computers\My Computer\Documents\Trainings_Audio")
# File to keep track of processed audio files
PROCESSED_AUDIO_FILE = AUDIO_DIR / "processed_transcriptions.txt"

# Folder to save transcript markdown files
TRANSCRIPTS_DIR = Path(r"G:\Other computers\My Computer\Documents\Trainings_Markdown")
# File to keep track of processed transcript files
PROCESSED_TRANSCRIPTS_FILE = TRANSCRIPTS_DIR / "processed_editor.txt"

# Log directory
LOG_DIR = Path(r"G:\Other computers\My Computer\Documents\Personal_Projects\notes_generator\logs")
