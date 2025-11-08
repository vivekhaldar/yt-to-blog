# yt-to-blog: Project Context for Claude Instances

## Project Overview

**yt-to-blog** is a Python CLI tool that transforms YouTube videos into high-quality blog posts using Google's Gemini 2.5 Pro API. The tool analyzes video content, extracts key information, and generates blog posts that emulate the speaker's voice and style while incorporating external references.

**Repository**: `/Users/haldar/repos/gh/yt-to-blog`
**Language**: Python 3.11+
**Package Manager**: uv (not pip or poetry)
**Status**: Active, currently on main branch

## Project Purpose

Convert YouTube video content into publication-ready blog posts with:
- Preservation of the speaker's voice, tone, and communication style
- Integration of reference links and citations
- Analytical, reflective writing style with historical context
- Clear, structured markdown output

## Key Architectural Components

### Directory Structure

```
yt-to-blog/
├── src/
│   ├── yt_to_blog.py           # Main application entry point
│   └── prompt.py               # DEFAULT_PROMPT constant
├── pyproject.toml              # Project configuration (uv-based)
├── README.md                   # User-facing documentation
├── .gitignore                  # Standard Python gitignore
└── uv.lock                     # Dependency lock file
```

### Core Modules

#### src/yt_to_blog.py
**Purpose**: Main application logic and CLI interface

**Key Functions**:
- `load_gemini_key()`: Loads API key from `.env` or `LLM_GEMINI_KEY` environment variable. Raises ValueError if not found.
- `analyze_youtube_video(youtube_url, gemini_key, prompt)`: 
  - Creates Gemini client with provided API key
  - Sends YouTube URL as FileData object to Gemini 2.5 Pro API
  - Combines URL and prompt in a Content object with multiple Parts
  - Returns response.text containing the generated blog post
- `main()`: 
  - Parses command-line arguments
  - Loads Gemini API key
  - Reads main prompt (from file or DEFAULT_PROMPT)
  - Reads video-specific prompt if provided
  - Combines prompts using `{VIDEO_SPECIFIC_CONTENT}` placeholder
  - Calls analyze_youtube_video() and prints result to stdout

**CLI Arguments**:
- `--youtube-url` (REQUIRED): YouTube video URL
- `--prompt-file` (OPTIONAL): Path to custom general prompt file
- `--video-specific-prompt` (OPTIONAL): Path to video-specific content file with references

#### src/prompt.py
**Purpose**: Contains the default AI prompt for video-to-blog conversion

**Key Component**: `DEFAULT_PROMPT` constant
- Defines the system prompt for the Gemini API
- Specifies role as "expert content repurposing assistant"
- Detailed instructions for emulating speaker's voice and style
- Includes template placeholder `{VIDEO_SPECIFIC_CONTENT}` for injection of video-specific context
- Structured as a comprehensive prompt with:
  - Role definition
  - Primary goal with numbered requirements
  - Input description
  - Step-by-step process
  - Expected output format

## Build, Run, and Test Commands

### Setup
```bash
# Install dependencies
uv sync

# Install development dependencies
uv sync --group dev
```

### Running the Application

**Using uv run** (from project directory):
```bash
uv run yt-to-blog --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID"
```

**With custom prompts**:
```bash
uv run yt-to-blog --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID" \
  --prompt-file custom_prompt.md \
  --video-specific-prompt video-references.md
```

**Direct installation and use**:
```bash
uv pip install .
yt-to-blog --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID"
```

**From git without cloning** (uvx):
```bash
uvx --from git+https://github.com/vivekhaldar/yt-to-blog yt-to-blog \
  --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID"
```

### Code Quality

```bash
# Run linter and formatter
uv run ruff check .
uv run ruff format .
```

### Getting Help
```bash
uv run yt-to-blog --help
```

## Important Implementation Details

### Gemini API Integration

**Model Used**: `models/gemini-2.5-pro-preview-06-05`

**API Pattern**:
```python
response = client.models.generate_content(
    model="models/gemini-2.5-pro-preview-06-05",
    contents=types.Content(
        parts=[
            types.Part(file_data=types.FileData(file_uri=youtube_url)),
            types.Part(text=prompt),
        ]
    )
)
```

**Key Points**:
- YouTube URLs are passed as `file_uri` within FileData (Gemini can directly access YouTube videos)
- Prompt is passed as a separate text Part
- Both parts are combined in a single Content object
- Response contains the generated blog post in `response.text`

### Prompt System

The tool uses a **two-part prompt composition** system:

1. **General/Main Prompt**:
   - Default: Loaded from `src/prompt.py:DEFAULT_PROMPT`
   - Custom: Can be provided via `--prompt-file` argument
   - Contains core instructions, role definition, writing style guidelines
   - Includes placeholder `{VIDEO_SPECIFIC_CONTENT}`

2. **Video-Specific Prompt**:
   - Optional file provided via `--video-specific-prompt` argument
   - Contains video context, reference links, citations
   - Injected at the `{VIDEO_SPECIFIC_CONTENT}` placeholder
   - If not provided, placeholder is replaced with empty string

3. **Combination**:
   ```python
   prompt = main_prompt.replace("{VIDEO_SPECIFIC_CONTENT}", video_specific_content)
   ```

### Configuration

**Environment Variables**:
- `LLM_GEMINI_KEY` (REQUIRED): Google Gemini API key
  - Can be set in `.env` file or as environment variable
  - Tool will raise ValueError if not found

**Python Version**: 3.11+ (specified in pyproject.toml)

## Dependencies

### Runtime Dependencies
- **google-genai**: Google Generative AI SDK for Gemini API access
- **jinja2**: Template engine (currently unused but available)
- **python-dotenv**: Environment variable loading from .env files

### Development Dependencies
- **ruff>=0.9.6**: Python linter and formatter

All dependencies are specified in `pyproject.toml` and locked in `uv.lock`.

## Git History and Evolution

Recent significant commits:
- `85dad42`: Moved prompt from prompt.md file to prompt.py constant
- `0550258`: Upgraded to June 2025 model (from older model)
- `4bade8d`: Changed model from "pro" to "flash" (then back to pro in later commit)
- `1bd5697`: Made prompt file arguments optional, added default prompt handling
- `06c7776`: Initial prompt refactoring with video-specific content support

**Key Evolution**: The project has moved from file-based prompts to embedding the default prompt as a constant in the code, making it easier to package and distribute.

## Unique Patterns and Conventions

### Error Handling
- Simple ValueError for missing API key
- Logging configured at INFO level
- Direct exception propagation (minimal try-catch)

### CLI Design
- Single entry point: `main()` function
- argparse for argument parsing
- Output directly to stdout (allows piping to files)

### Logging
```python
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
```
Logs are written to console at INFO level, useful for debugging.

### Writing Style Target
The tool aims to produce blog posts that are:
- **Analytical**: Breaking down complex topics with frameworks
- **Reflective**: Personal insights and self-awareness
- **Historical**: Drawing parallels with technological precedents
- **Critical**: Thoughtful evaluation of tools and trends
- **Practical**: Grounded in real-world software engineering
- **Well-cited**: Incorporating external references with proper attribution

## Package Distribution

The project is configured as a proper Python package:
- Entry point: `yt-to-blog` command mapped to `yt_to_blog:main` in pyproject.toml
- Package uses uv's `package = true` setting
- Can be installed via `uv pip install` or distributed via PyPI/GitHub

## Common Use Cases

1. **Quick blog post generation** (minimal args):
   ```bash
   yt-to-blog --youtube-url "https://www.youtube.com/watch?v=VIDEO_ID" > post.md
   ```

2. **Academic/Research context** (with references):
   ```bash
   yt-to-blog --youtube-url "URL" --video-specific-prompt references.md
   ```

3. **Custom writing style** (custom prompt):
   ```bash
   yt-to-blog --youtube-url "URL" --prompt-file my-style.md
   ```

4. **Batch processing** (shell scripting):
   ```bash
   for url in "${urls[@]}"; do
     yt-to-blog --youtube-url "$url" > "${video_id}.md"
   done
   ```

## Important Notes for Future Development

- No test files currently exist in the repository
- The project does not use type hints extensively (opportunities for adding mypy/pydantic)
- Jinja2 is imported but not currently used (possible future template enhancement)
- The codebase is intentionally simple and focused on core functionality
- Vivek's writing style is the target model for output generation
- No database, persistence, or caching mechanisms currently implemented

## Future Enhancement Opportunities

1. Add type hints (Python 3.11+ supports PEP 647)
2. Implement batch video processing
3. Add output formatting options (HTML, PDF, etc.)
4. Cache Gemini responses to reduce API costs
5. Add testing with pytest
6. Support for other video platforms (Vimeo, etc.)
7. Local model support as alternative to Gemini
8. Streaming output for long videos

---
**Last Updated**: Based on commit 85dad42
**Maintained by**: Vivek Haldar
