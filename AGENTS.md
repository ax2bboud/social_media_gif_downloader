# Agent Development Guide

## Commands

### Initial Setup
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -e .[dev]
```

### Build
```bash
pip install -e .
```

### Tests
```bash
pytest --cov=social_media_gif_downloader --cov-report=xml --ignore=tests/test_integration.py
```

### Run Application
```bash
python social_media_gif_downloader.py
```

## Tech Stack
- **Language**: Python 3.8+ (supports 3.8-3.12)
- **GUI**: CustomTkinter (modern tkinter wrapper)
- **Video Processing**: MoviePy + FFmpeg
- **Downloading**: yt-dlp
- **Testing**: pytest, pytest-mock, pytest-cov, pytest-xdist

## Architecture
- `social_media_gif_downloader.py`: Main GUI application with CustomTkinter interface and threading for background downloads
- `platforms.py`: Abstract base class `PlatformDownloader` with platform-specific implementations (Twitter, Pinterest, Instagram)
- `tests/`: pytest-based test suite with fixtures, platform detection, URL parsing, and error handling tests

## Code Style
- No linting tool configured; follow existing conventions in codebase
- Use type hints from `typing` module
- Logging via Python's `logging` module (file-based when frozen, console otherwise)
- Thread-safe GUI updates via `after()` for cross-thread communication
- Abstract base classes for platform extensibility
