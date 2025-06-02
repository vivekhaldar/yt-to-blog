import os
from google import genai
from google.genai import types
import argparse
from dotenv import load_dotenv
import logging
from prompt import DEFAULT_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)


def load_gemini_key():
    """Load Gemini key from .env file or environment variable called LLM_GEMINI_KEY"""
    load_dotenv()
    LLM_GEMINI_KEY = os.getenv("LLM_GEMINI_KEY")
    if not LLM_GEMINI_KEY:
        raise ValueError("LLM_GEMINI_KEY environment variable is not set.")
    return LLM_GEMINI_KEY


def analyze_youtube_video(youtube_url, gemini_key, prompt):
    client = genai.Client(api_key=gemini_key)
    log.info("Starting analysis of YouTube video...")
    log.info(f"YouTube URL: {youtube_url}")
    log.info(f"Prompt: {prompt}")

    # Analyze the video
    response = client.models.generate_content(
        model="gemini-2.5-pro-preview-05-06",
        contents=types.Content(
            parts=[
                types.Part(text=prompt),
                types.Part(
                    file_data=types.FileData(file_uri=youtube_url)
                )
            ]
        )
    )

    log.info(f"Response from Gemini: {response}")

    return response.text

def main():
    parser = argparse.ArgumentParser(description="Analyze a YouTube video and generate a blog post.")
    parser.add_argument("--youtube-url", type=str, required=True, help="YouTube video URL")
    parser.add_argument("--prompt-file", type=str, required=False, help="Path to file containing the main prompt for the AI model (optional, uses default if not specified)")
    parser.add_argument("--video-specific-prompt", type=str, required=False, help="Path to file containing video-specific content (e.g., reference links)")

    args = parser.parse_args()
    gemini_key = load_gemini_key()

    # Read the main prompt
    if args.prompt_file:
        with open(args.prompt_file, "r") as f:
            main_prompt = f.read()
    else:
        main_prompt = DEFAULT_PROMPT
    
    # Read the video-specific prompt
    if args.video_specific_prompt:
        with open(args.video_specific_prompt, "r") as f:
            video_specific_content = f.read()
    else:
        video_specific_content = ""
    
    # Combine the prompts by replacing the placeholder
    prompt = main_prompt.replace("{VIDEO_SPECIFIC_CONTENT}", video_specific_content)

    blog_post = analyze_youtube_video(args.youtube_url, gemini_key, prompt)

    print(blog_post)

if __name__ == "__main__":
    main()

