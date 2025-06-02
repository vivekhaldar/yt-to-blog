import os
from google import genai
from google.genai import types
import argparse
from dotenv import load_dotenv
import logging
import importlib.resources

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


def get_default_prompt():
    """Get the default prompt from the bundled prompt.md file"""
    try:
        # Try to read from the package resources
        with importlib.resources.open_text('yt_to_blog', 'prompt.md') as f:
            return f.read()
    except (ImportError, FileNotFoundError):
        # Fallback: try to read from relative path (for development)
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompt_path = os.path.join(os.path.dirname(current_dir), 'prompt.md')
        try:
            with open(prompt_path, "r") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(
                "Could not find prompt.md file. Please specify --prompt-file explicitly."
            )


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
    parser.add_argument("--prompt-file", type=str, required=False, help="Path to file containing the main prompt for the AI model (defaults to bundled prompt.md)")
    parser.add_argument("--video-specific-prompt", type=str, required=False, help="Path to file containing video-specific content (e.g., reference links)")
    
    args = parser.parse_args()
    gemini_key = load_gemini_key()

    # Read the main prompt - use default if not specified
    if args.prompt_file:
        with open(args.prompt_file, "r") as f:
            main_prompt = f.read()
    else:
        main_prompt = get_default_prompt()
    
    # Read the video-specific prompt
    if args.video_specific_prompt:
        with open(args.video_specific_prompt, "r") as f:
            video_specific_content = f.read()
    else:
        video_specific_content = ""

    # Combine main prompt and video-specific content
    prompt = f"{main_prompt}\n\n{video_specific_content}"

    blog_post = analyze_youtube_video(args.youtube_url, gemini_key, prompt)

    print(blog_post)

if __name__ == "__main__":
    main()

