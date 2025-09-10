
"""
editor.py
---------
Formats a raw transcript text file and generates a summary using Gemini API.

This script is called by transcript_watcher.py when a new transcript is detected.
It uses the Gemini API to:
    - Format the transcript into a well-structured markdown file (formatted_*.md)
    - Generate a summary markdown file (summary_*.md) with key ideas and action items
"""

import sys
from pathlib import Path


# Import Gemini API call from separate module
from gemini_api import call_gemini_api
# Import prompts from config
from config import FORMAT_PROMPT, SUMMARY_PROMPT
from config import TRANSCRIPTS_DIR

# Define output directories for formatted and summary notes
FORMATTED_DIR = TRANSCRIPTS_DIR / "formatted"
SUMMARY_DIR = TRANSCRIPTS_DIR / "summary"
FORMATTED_DIR.mkdir(parents=True, exist_ok=True)
SUMMARY_DIR.mkdir(parents=True, exist_ok=True)


def main():
    """
    Main entry point for formatting and summarizing a transcript file.
    Chunks the transcript for processing, calls Gemini API for formatting and summary,
    and writes the results to output folders.
    """
    if len(sys.argv) < 2:
        print("Usage: python editor.py <transcript_file.md>")
        sys.exit(1)
    transcript_path = Path(sys.argv[1])
    if not transcript_path.exists():
        print(f"File not found: {transcript_path}")
        sys.exit(1)
    with open(transcript_path, 'r', encoding='utf-8') as f:
        transcript_lines = f.readlines()

    # Chunking: process 500 lines at a time
    chunk_size = 500
    num_chunks = (len(transcript_lines) + chunk_size - 1) // chunk_size
    
    formatted_chunks = []
    print(f"[editor] Step 1: Formatting transcript in {num_chunks} chunks of {chunk_size} lines each...")
    for i in range(num_chunks):
        chunk_lines = transcript_lines[i*chunk_size:(i+1)*chunk_size]
        chunk_text = ''.join(chunk_lines)
        print(f"[editor] Formatting chunk {i+1}/{num_chunks}...")
        formatted_chunk = call_gemini_api(FORMAT_PROMPT, chunk_text)
        formatted_chunks.append(formatted_chunk)
    formatted_text = '\n\n'.join(formatted_chunks)
    formatted_path = FORMATTED_DIR / transcript_path.with_suffix('.md').name
    with open(formatted_path, 'w', encoding='utf-8') as f:
        f.write(formatted_text)
    print(f"[editor] Step 1 complete: Formatted notes saved to {formatted_path}")

    
    # 2. Generate a summary in chunks, then polish
    print("[editor] Step 2: Generating summary in chunks...")
    summary_chunks = []
    for i in range(num_chunks):
        chunk_lines = transcript_lines[i*chunk_size:(i+1)*chunk_size]
        chunk_text = ''.join(chunk_lines)
        print(f"[editor] Summarizing chunk {i+1}/{num_chunks}...")
        summary_chunk = call_gemini_api(SUMMARY_PROMPT, chunk_text)
        summary_chunks.append(summary_chunk)
    concatenated_summary = '\n\n'.join(summary_chunks)

    print("[editor] Step 2: Polishing concatenated summary with Gemini...")
    polished_summary = call_gemini_api(SUMMARY_PROMPT, concatenated_summary)
    summary_path = SUMMARY_DIR / transcript_path.with_suffix('.md').name
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(polished_summary)
    print(f"[editor] Step 2 complete: Summary notes saved to {summary_path}")

if __name__ == "__main__":
    main()
