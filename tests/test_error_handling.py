import pytest
import json
import os
from unittest.mock import patch, Mock
from twitter_downloader import App
from tests.conftest import is_headless


class TestErrorHandling:
    """Tests for error handling in various scenarios."""

    @pytest.mark.skipif(is_headless(), reason="Skipping GUI test in headless environment")
    def test_get_video_info_subprocess_error(self, mock_subprocess):
        """Test handling of yt-dlp subprocess errors."""
        with patch('os.environ', {'DISPLAY': ':99'}):
            app = App()
        mock_subprocess.side_effect = Exception("Subprocess failed")

        with patch.object(app, 'update_status') as mock_update:
            app.get_video_info("https://x.com/test/status/123")

        mock_update.assert_called_with("Unexpected error getting info: Subprocess failed", "red")

    @pytest.mark.skipif(is_headless(), reason="Skipping GUI test in headless environment")
    def test_get_video_info_json_decode_error(self, mock_subprocess):
        """Test handling of invalid JSON from yt-dlp."""
        with patch('os.environ', {'DISPLAY': ':99'}):
            app = App()
        mock_result = Mock()
        mock_result.returncode = 0
        mock_result.stdout = "invalid json"
        mock_subprocess.return_value = mock_result

        with patch.object(app, 'update_status') as mock_update:
            app.get_video_info("https://x.com/test/status/123")

        # Should still proceed with default FPS
        mock_update.assert_not_called()

    @pytest.mark.skipif(is_headless(), reason="Skipping GUI test in headless environment")
    def test_download_and_convert_missing_temp_file(self, mock_subprocess, mock_video_file_clip):
        """Test handling when temp video file is not created."""
        with patch('os.environ', {'DISPLAY': ':99'}):
            app = App()
        mock_result = Mock()
        mock_result.returncode = 0
        mock_subprocess.return_value = mock_result

        with patch('os.path.exists', return_value=False), \
             patch.object(app, 'update_status') as mock_update:
            app.download_and_convert("https://x.com/test/status/123", "output.gif", 30)

        mock_update.assert_called_with("Error: Download file not found.", "red")

    @pytest.mark.skipif(is_headless(), reason="Skipping GUI test in headless environment")
    def test_download_and_convert_yt_dlp_failure(self, mock_subprocess):
        """Test handling of yt-dlp download failure."""
        with patch('os.environ', {'DISPLAY': ':99'}):
            app = App()
        mock_result = Mock()
        mock_result.returncode = 1
        mock_result.stderr = "Download failed"
        mock_subprocess.return_value = mock_result

        with patch.object(app, 'update_status') as mock_update:
            app.download_and_convert("https://x.com/test/status/123", "output.gif", 30)

        mock_update.assert_called_with("Error: Download failed. Check console.", "red")

    @pytest.mark.skipif(is_headless(), reason="Skipping GUI test in headless environment")
    def test_start_get_info_thread_empty_url(self):
        """Test handling of empty URL input."""
        with patch('os.environ', {'DISPLAY': ':99'}):
            app = App()

        with patch.object(app, 'update_status') as mock_update:
            app.start_get_info_thread()

        mock_update.assert_called_with("Error: Please paste a URL first.", "red")