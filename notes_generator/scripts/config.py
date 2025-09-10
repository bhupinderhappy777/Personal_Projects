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
    "You are given a raw transcript of a training session. "
    "Your task is to convert it into a clear, well-structured markdown script that closely follows the original delivery and language of the speaker. "
    "Do NOT summarize or shorten the content. Instead, correct grammar, spelling, and transcription errors to make the script readable and faithful to the speaker's style. "
    "Retain the full script, removing only obvious fillers or off-topic remarks, and keep at least 90% of the original content. "
    "Divide the script into sections based on topics discussed (or every ~5 minutes if topics are unclear). "
    "For each section:\n"
    "- Start with a heading for the topic or time range.\n"
    "- Write the improved script for that section, using bullet points, blockquotes, bold, or italics for emphasis and clarity where appropriate.\n"
    "- **Whenever the speaker says something important or insightful, make it stand out by putting it in a blockquote and using bold or italics.**\n"
    "- After the script, add a '**Key Learnings**' subsection with bullet points summarizing the main ideas or lessons from that part.\n"
    "- Add a brief observation about the speaker's mindset, delivery style, and what can be learnt from their way of presenting.\n"
    "- You may add your own brief remarks or insights, but stay true to the original transcript.\n"
    "Do NOT summarize the entire transcript; work section by section as described above.\n"
    "**Give the full output, even if it is long or takes time. Do not omit any sections.**\n"
    "Respond ONLY with markdown. Here is an example format:\n\n"
    "```markdown\n"
    "# Session Title\n"
    "## Topic or Time Range\n"
    "Improved script for this section...\n"
    "> **\"Important Quote from the Speaker.\"**\n"
    "**Speaker's mindset:** _Observation about mindset and delivery._\n"
    "**Key Learnings:**\n"
    "- Main idea 1\n"
    "- Main idea 2\n"
    "```\n"
    "Now, format the following transcript:\n"
)

SUMMARY_PROMPT = (
    "Summarize the following transcript into concise, well-structured markdown notes. "
    "Use markdown formatting: headings for topics, bullet points for key ideas, numbered lists for steps or sequences, and blockquotes for important statements or quotes. "
    "Highlight main points, action items, and any insights or lessons learned. "
    "If possible, include a short section at the end with 'Key Takeaways' and 'Action Items'. "
    "**Give the full summary, even if it is long or takes time. Do not omit any important points.**\n"
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