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

# Prompts for Gemini API (editor.py)
FORMAT_PROMPT = (
	"Format the following transcript into well-structured markdown. "
	"Use headings, bullet points, and blockquotes where appropriate. "
	"Do not summarize; just improve readability and structure. Do not remove any content. "
	"You can add emphasis using bold or italics where relevant. "
	"Correct any obvious grammar or spelling mistakes. "
	"Treat it as a training session transcript. It should be detailed and comprehensive. "
	"Wherever necessary, add your observations about the mindset of the speaker and what can be learnt from it. "
	"Feel free to add your own insights, with your own research if necessary, but limited, staying true to the original transcript.\n\n"
	"Respond ONLY with markdown. Here is an example, but optional format:\n\n"
	"```markdown\n"
	"# Session Title\n"
	"## Key Topic\n"
	"- Main point 1\n"
	"- Main point 2\n"
	"> \"Interesting quotes from the speaker.\"\n"
	"**Speaker's mindset:** _Observation about mindset._\n"
	"```\n"
	"Now, format the following transcript:\n"
)

SUMMARY_PROMPT = (
	"Summarize the following transcript into concise, well-structured markdown notes. "
	"Use markdown formatting: headings for topics, bullet points for key ideas, numbered lists for steps or sequences, and blockquotes for important statements or quotes. "
	"Highlight main points, action items, and any insights or lessons learned. "
	"If possible, include a short section at the end with 'Key Takeaways' and 'Action Items'. "
	"Respond ONLY with markdown. Here is an example format:\n\n"
	"```markdown\n"
	"# Session Summary\n"
	"## Main Topics\n"
	"- Topic 1: Brief explanation\n"
	"- Topic 2: Brief explanation\n"
	"\n## Key Points\n"
	"- Important point 1\n"
	"- Important point 2\n"
	"> \"Notable quote from the session.\"\n"
	"\n## Key Takeaways\n"
	"- Takeaway 1\n"
	"- Takeaway 2\n"
	"\n## Action Items\n"
	"1. Action step one\n"
	"2. Action step two\n"
	"```\n"
	"Now, summarize the following transcript:\n"
)
