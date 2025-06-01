import os
from google import genai
from google.genai import types
import argparse
from dotenv import load_dotenv


def load_gemini_key():
    """Load Gemini key from .env file or environment variable called LLM_GEMINI_KEY"""
    load_dotenv()
    LLM_GEMINI_KEY = os.getenv("LLM_GEMINI_KEY")
    if not LLM_GEMINI_KEY:
        raise ValueError("LLM_GEMINI_KEY environment variable is not set.")
    return LLM_GEMINI_KEY


def analyze_youtube_video(youtube_url, gemini_key, prompt):
    client = genai.Client(api_key=gemini_key)
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

    return response.text

def main():
    parser = argparse.ArgumentParser(description="Analyze a YouTube video and generate a blog post.")
    parser.add_argument("--youtube-url", type=str, required=True, help="YouTube video URL")
    parser.add_argument("--prompt-file", type=str, required=True, help="Path to file containing the prompt for the AI model")
    
    args = parser.parse_args()
    gemini_key = load_gemini_key()

    with open(args.prompt_file, "r") as f:
        prompt = f.read()

    blog_post = analyze_youtube_video(args.youtube_url, gemini_key, prompt)

    print(blog_post)

if __name__ == "__main__":
    main()

