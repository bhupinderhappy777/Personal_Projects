
"""
gemini_api.py
-------------
Module for interacting with the Gemini API for text formatting and summarization.
Uses the google-generativeai package.

This module is imported by editor.py to call the Gemini LLM for formatting and summarizing transcripts.
"""

import os
import google.generativeai as genai

# Set your Gemini API key as an environment variable for security
API_KEY = os.getenv("GOOGLE_API_KEY")  # Set this in your environment

def call_gemini_api(prompt, text):
    """
    Calls the Gemini API with a prompt and input text.
    Args:
        prompt (str): The instruction for the LLM.
        text (str): The input text to process.
    Returns:
        str: The processed text from Gemini API.
    Raises:
        RuntimeError: If the API key is not set.
    """
    """
    Calls the Gemini API with a prompt and input text.
    Args:
        prompt (str): The instruction for the LLM.
        text (str): The input text to process.
    Returns:
        str: The processed text from Gemini API.
    """
    if not API_KEY:
        raise RuntimeError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=API_KEY)
    # Use the free Gemini 1.5 Flash model (usually available for all users)
    model = genai.GenerativeModel("models/gemini-2.5-flash-lite")
    print("Sent to Gemini API...")
    response = model.generate_content([prompt, text])
    print("Received response from Gemini API.")
    return response.text.strip()
