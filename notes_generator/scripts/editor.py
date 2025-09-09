"""
Formats a raw transcript markdown file and generates a summary using Gemini API.
Creates two files: formatted_<original>.md and summary_<original>.md
"""

import sys
from pathlib import Path

# Import Gemini API call from separate module
from gemini_api import call_gemini_api


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
    format_prompt = (
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
    formatted_text = call_gemini_api(format_prompt, transcript_text)
    formatted_path = transcript_path.parent / f"formatted_{transcript_path.name}"
    with open(formatted_path, 'w', encoding='utf-8') as f:
        f.write(formatted_text)
    print(f"Formatted notes saved to {formatted_path}")

    # 2. Generate a summary
    summary_prompt = (
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
    summary_text = call_gemini_api(summary_prompt, transcript_text)
    summary_path = transcript_path.parent / f"summary_{transcript_path.name}"
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_text)
    print(f"Summary notes saved to {summary_path}")

if __name__ == "__main__":
    main()
