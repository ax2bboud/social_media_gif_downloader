import pytest
import tempfile
import os
from unittest.mock import Mock, patch


def is_headless():
    """
    Detect if running in a headless environment (no display available).
    Returns True if headless, False if display is available.
    """
    try:
        import tkinter
        # Try to create a Tk instance to check if display is available
        root = tkinter.Tk()
        root.destroy()
        return False
    except tkinter.TclError:
        # TclError indicates no display available
        return True


@pytest.fixture
def temp_dir():
    """Provides a temporary directory for testing."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield tmpdir


@pytest.fixture
def mock_subprocess():
    """Mocks subprocess.run for testing."""
    with patch('subprocess.run') as mock_run:
        yield mock_run


@pytest.fixture
def mock_video_file_clip():
    """Mocks VideoFileClip from moviepy."""
    with patch('moviepy.VideoFileClip') as mock_clip:
        mock_instance = Mock()
        mock_clip.return_value = mock_instance
        yield mock_instance


@pytest.fixture
def sample_twitter_url():
    """Provides a sample Twitter/X URL for testing."""
    return "https://x.com/username/status/1234567890123456789"


@pytest.fixture
def sample_video_info():
    """Provides sample video info JSON from yt-dlp."""
    return {
        "fps": 30,
        "duration": 5.5,
        "width": 1920,
        "height": 1080
    }


@pytest.fixture
def skip_if_headless():
    """
    Skip test if running in headless environment (no display available).
    This prevents Tkinter initialization errors in CI environments.
    """
    if is_headless():
        pytest.skip("Skipping GUI test in headless environment")