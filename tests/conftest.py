import pytest
import tempfile
import os
from unittest.mock import Mock, patch


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