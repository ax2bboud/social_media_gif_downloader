# AGENTS.md

## Setup
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .[dev]
```

## Commands
- **Build**: `python -m build`
- **Test**: `pytest --cov=social_media_gif_downloader --cov-report=xml --ignore=tests/test_integration.py`
- **Lint**: No linter configured
- **Dev Server**: `python social_media_gif_downloader.py` (launches GUI)

## Tech Stack
- **Language**: Python 3.8+
- **GUI**: CustomTkinter
- **Video Processing**: MoviePy, FFmpeg
- **Downloader**: yt-dlp
- **Testing**: pytest, pytest-mock, pytest-cov
- **Build**: setuptools

## Architecture
- `social_media_gif_downloader.py`: Main GUI app with threading for non-blocking downloads
- `platforms.py`: Abstract base class `PlatformDownloader` with platform-specific implementations (Twitter, Pinterest, Instagram)
- Entry point: `social-media-gif-downloader` command after installation

## Code Style
- No explicit linter/formatter configured
- Follow existing conventions: type hints, docstrings for public methods, logging for errors
- Use abstract base classes for platform extensibility
