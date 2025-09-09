
# Notes Generator

This project automates the process of generating markdown notes from video files using Python scripts, ffmpeg, and OpenAI Whisper.

## Workflow Overview

1. **Video Watcher** (`watcher.py`):
	- Monitors a specified folder for new `.mp4` video files.
	- When a new video is detected, it automatically triggers the conversion script.

2. **Video to Audio Converter** (`converter.py`):
	- Converts `.mp4` video files to `.mp3` audio files using the `ffmpeg-python` package (requires ffmpeg installed).
	- Saves the audio files to a designated audio folder.

3. **Audio Watcher** (`audio_watcher.py`):
	- Monitors the audio folder for new `.mp3` files.
	- When a new audio file is detected, it automatically triggers the transcription script.

4. **Transcriber** (`transcriber.py`):
	- Uses the OpenAI Whisper CLI to transcribe `.mp3` audio files to text.
	- Saves the transcription as a markdown (`.md`) file in a transcripts folder.
	- By default, uses the `tiny` Whisper model for faster CPU transcription.

## Folder Structure

```
notes_generator/
	 scripts/
		  watcher.py
		  converter.py
		  audio_watcher.py
		  transcriber.py
	 watched_videos/           # Folder to place new .mp4 files
	 audio/                    # Folder where .mp3 files are saved
	 transcripts/              # Folder where .md files are saved
```

## Requirements

- Python 3.8+
- ffmpeg (must be installed and in your PATH)
- ffmpeg-python (`pip install ffmpeg-python`)
- OpenAI Whisper CLI (`pip install openai-whisper`)

## Usage

1. Place your `.mp4` video files in the `watched_videos` folder.
2. Run `watcher.py` to monitor for new videos and convert them to audio.
3. Run `audio_watcher.py` to monitor for new audio files and transcribe them.
4. Find your generated markdown notes in the `transcripts` folder.

You can run the watcher scripts in the background for full automation.

## Customization

- Update the folder paths in each script to match your system if needed.
- Change the Whisper model in `transcriber.py` for higher accuracy (e.g., `base`, `small`, `medium`, `large`) at the cost of speed.

---
This project is modular and easy to extend for other automation or note-taking workflows.
