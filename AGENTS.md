# AGENTS.md

## Commands

**Initial Setup:**
```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -e .[dev]
```

**Build:** `python -m build`

**Lint:** N/A (no linter configured)

**Tests:** `pytest --cov=social_media_gif_downloader`

**Dev Server:** `python social_media_gif_downloader.py`

## Tech Stack & Architecture

- **Language:** Python 3.8+
- **GUI:** CustomTkinter
- **Video Processing:** moviepy, FFmpeg
- **Downloader:** yt-dlp
- **Testing:** pytest, pytest-cov, pytest-mock
- **Structure:** Modular platform-specific downloaders (`platforms.py`) with abstract base class pattern; main GUI in `social_media_gif_downloader.py`

## Code Style

- No comments unless complex logic requires context
- Follow existing patterns in `platforms.py` for new platform support
- Threading for background processing to keep UI responsive
- Comprehensive logging for error handling
