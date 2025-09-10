"""
Formats a raw transcript markdown file and generates a summary using Gemini API.
Creates two files: formatted_<original>.md and summary_<original>.md
"""

import sys
from pathlib import Path


# Import Gemini API call from separate module
from gemini_api import call_gemini_api
# Import prompts from config
from config import FORMAT_PROMPT, SUMMARY_PROMPT


def main():
    if len(sys.argv) < 2:
        print("Usage: python editor.py <transcript_file.md>")
        sys.exit(1)
    transcript_path = Path(sys.argv[1])
    if not transcript_path.exists():
        print(f"File not found: {transcript_path}")
        sys.exit(1)
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript_text = f.read()

    # 1. Format the transcript nicely
    formatted_text = call_gemini_api(FORMAT_PROMPT, transcript_text)
    formatted_path = transcript_path.parent / f"formatted_{transcript_path.name}"
    with open(formatted_path, 'w', encoding='utf-8') as f:
        f.write(formatted_text)
    print(f"Formatted notes saved to {formatted_path}")

    # 2. Generate a summary
    summary_text = call_gemini_api(SUMMARY_PROMPT, transcript_text)
    summary_path = transcript_path.parent / f"summary_{transcript_path.name}"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_text)
    print(f"Summary notes saved to {summary_path}")

if __name__ == "__main__":
    main()
