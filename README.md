# yt-to-blog

A Python CLI tool that transforms YouTube videos into high-quality blog posts using Google's Gemini AI model. The tool analyzes video content and generates blog posts following a specific writing style and incorporating external references.

## Features

- **YouTube Video Analysis**: Processes YouTube videos directly using Google's Gemini 2.5 Pro model
- **Custom Writing Style**: Transforms content to match a specific analytical, reflective, and historically-informed writing style
- **Reference Integration**: Incorporates quotes and citations from provided reference links
- **CLI Interface**: Simple command-line interface for easy automation and scripting

## Installation

This project uses [uv](https://github.com/astral-sh/uv) for dependency management. Make sure you have uv installed.

### Prerequisites

- Python 3.11 or higher
- uv package manager
- Google Gemini API key

### Install Dependencies

```bash
uv sync
```

### Environment Setup

1. Create a `.env` file in the project root:
```bash
touch .env
```

2. Add your Gemini API key to the `.env` file:
```
LLM_GEMINI_KEY=your_gemini_api_key_here
```

Alternatively, you can set the environment variable directly:
```bash
export LLM_GEMINI_KEY=your_gemini_api_key_here
```

## Usage

### Command Line Arguments

The tool accepts the following arguments:

**Required:**
- `--youtube-url`: The YouTube video URL to analyze

**Optional:**
- `--prompt-file`: Path to a custom general prompt file (if not specified, uses built-in default prompt)
- `--video-specific-prompt`: Path to a video-specific prompt file containing reference links and additional context

### Prompt System

The tool uses a two-part prompt system:

1. **General Prompt**: Contains the core instructions for video analysis and blog post generation
   - If `--prompt-file` is provided, uses that file
   - If not provided, uses the built-in default prompt from `src/prompt.py`
   - Defines the AI's role, writing style guidelines, and general process

2. **Video-Specific Prompt**: Contains context specific to individual videos
   - Optional file specified with `--video-specific-prompt`
   - Typically contains reference links, citations, and video-specific context
   - Gets inserted into the general prompt template at the `{VIDEO_SPECIFIC_CONTENT}` placeholder
   - Examples: `video-specific-prompt-jevons.md`, `video-specific-prompt-factory-work.md`

### Basic Usage

**Minimal usage (only required arguments):**
```bash
yt-to-blog --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID"
```

**With custom general prompt:**
```bash
yt-to-blog --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID" --prompt-file prompt.md
```

**With video-specific context:**
```bash
yt-to-blog --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID" --video-specific-prompt video-specific-prompt-jevons.md
```

**With both custom prompts:**
```bash
yt-to-blog --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID" --prompt-file prompt.md --video-specific-prompt video-specific-prompt-jevons.md
```

### Using with uv

```bash
uv run yt-to-blog --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID" --video-specific-prompt video-specific-prompt-jevons.md
```

### Using with uvx (Direct from Git)

You can run the tool directly from the GitHub repository without cloning:

```bash
uvx --from git+https://github.com/vivekhaldar/yt-to-blog yt-to-blog --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Complete Example

```bash
yt-to-blog --youtube-url "https://www.youtube.com/watch?v=GT_sXIUJPUo" --video-specific-prompt video-specific-prompt-jevons.md > blog_post.md
```

## Prompt File

The tool includes a comprehensive `prompt.md` file that defines:

- **Role**: Expert content repurposing assistant
- **Writing Style Guide**: Detailed specifications for tone and approach including:
  - Analytical and conceptual framework
  - Reflective and self-aware perspective
  - Historical context and parallels
  - Critical technology engagement
  - Evidence-based citations
  - Clear, structured prose

- **Process**: Step-by-step instructions for video analysis and blog post generation

## Project Structure

```
yt-to-blog/
├── src/
│   └── yt_to_blog.py          # Main application code
├── prompt.md                   # AI prompt template
├── pyproject.toml             # Project configuration
├── uv.lock                    # Dependency lock file
├── .gitignore                 # Git ignore rules
└── README.md                  # This file
```

## Dependencies

- **google-genai**: Google Generative AI SDK for Gemini model access
- **jinja2**: Template engine (for future template functionality)
- **python-dotenv**: Environment variable management

### Development Dependencies

- **ruff**: Python linter and formatter

## API Usage

The tool uses Google's Gemini 2.5 Pro Preview model (`gemini-2.5-pro-preview-05-06`) which supports:
- Direct video file processing
- Large context windows
- High-quality content generation

## Writing Style

The generated blog posts follow a specific style that is:

- **Analytical**: Breaks down complex topics with clear frameworks
- **Reflective**: Includes personal insights and self-awareness
- **Historical**: Draws parallels with technological precedents
- **Critical**: Thoughtfully evaluates tools and trends
- **Practical**: Grounded in real-world software engineering
- **Well-cited**: Incorporates external references and quotes

## Configuration

### Environment Variables

- `LLM_GEMINI_KEY`: Your Google Gemini API key (required)

### Customization

You can modify the `prompt.md` file to:
- Adjust the writing style guidelines
- Change the reference integration approach
- Modify the output format requirements

## Error Handling

The tool will raise a `ValueError` if the Gemini API key is not found in either:
1. The `.env` file
2. The `LLM_GEMINI_KEY` environment variable

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run the linter: `uv run ruff check`
5. Submit a pull request

## License

This project is open source. Please check the repository for license details.

## Troubleshooting

### Common Issues

1. **Missing API Key**: Ensure `LLM_GEMINI_KEY` is set in your environment or `.env` file
2. **Invalid YouTube URL**: Make sure the URL is accessible and public
3. **Network Issues**: Check your internet connection for API access

### Getting Help

If you encounter issues:
1. Check that all dependencies are installed with `uv sync`
2. Verify your Gemini API key is valid
3. Ensure the YouTube video is publicly accessible
4. Review the prompt file format

## Version

Current version: 0.1.0

---

**Note**: This tool requires a valid Google Gemini API key and internet access to function properly.
