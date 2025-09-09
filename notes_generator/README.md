

# Notes Generator

This project automates the process of generating well-structured and summarized markdown notes from video files using Python scripts, ffmpeg, OpenAI Whisper, and Gemini API.

## Full Automated Workflow

1. **Drop a video file** (`.mp4`) into the `watched_videos` folder.
2. **watcher.py** detects the new video and triggers `converter.py` to convert it to `.mp3` audio.
3. **converter.py** saves the audio file in the `audio` folder.
4. **audio_watcher.py** detects the new `.mp3` and triggers `transcriber.py` to transcribe it using Whisper.
5. **transcriber.py** saves the raw transcript as a markdown file in the `transcripts` folder.
6. **transcript_watcher.py** detects the new transcript and triggers `editor.py`.
7. **editor.py** uses Gemini API to:
	- Format the transcript into a well-structured markdown file (`formatted_...md`).
	- Generate a summary markdown file (`summary_...md`) with key ideas and action items.

All watcher scripts can be started at once using the provided PowerShell script:

### `run_pipeline.ps1`
This script:
- Activates your Python virtual environment
- Starts all watcher scripts in the background
- Logs output and errors to the `logs/` directory for easy monitoring

## Folder Structure

```
notes_generator/
	scripts/
		watcher.py
		converter.py
		audio_watcher.py
		transcriber.py
		transcript_watcher.py
		editor.py
		gemini_api.py
	watched_videos/           # Folder to place new .mp4 files
	audio/                    # Folder where .mp3 files are saved
	transcripts/              # Folder where .md files are saved
	logs/                     # Folder for watcher logs
	run_pipeline.ps1          # Script to launch the full pipeline
```

## Requirements

- Python 3.8+
- ffmpeg (must be installed and in your PATH)
- ffmpeg-python (`pip install ffmpeg-python`)
- OpenAI Whisper CLI (`pip install openai-whisper`)
- google-generativeai (`pip install google-generativeai`)
- Gemini API key (set as `GOOGLE_API_KEY` environment variable)

## Usage

1. Place your `.mp4` video files in the `watched_videos` folder.
2. Run `run_pipeline.ps1` from your project root in PowerShell:
   ```powershell
   .\run_pipeline.ps1
   ```
3. All watcher scripts will run in the background, and logs will be saved in the `logs/` folder.
4. Find your generated formatted and summary markdown notes in the `transcripts` folder.


## Customization

- **Centralized configuration:**
	- Update all folder paths and settings in `scripts/config.py` to match your system. All scripts will use these values automatically.
- Change the Whisper model in `transcriber.py` for higher accuracy (e.g., `base`, `small`, `medium`, `large`) at the cost of speed.
- Update prompts in `editor.py` for different formatting or summarization styles.

---
This project is modular, fully automated, and easy to extend for other automation or note-taking workflows.
