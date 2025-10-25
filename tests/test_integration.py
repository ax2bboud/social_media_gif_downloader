import pytest
import json
import os
from unittest.mock import patch, Mock
from twitter_gif_downloader import App
from tests.conftest import is_headless


class TestIntegration:
    """Integration tests for the complete download workflow."""

    @pytest.mark.skipif(is_headless(), reason="Skipping GUI test in headless environment")
    def test_workflow_with_cancelled_save_dialog(self, mock_subprocess):
        """Test workflow when user cancels the save dialog."""
        with patch('os.environ', {'DISPLAY': ':99'}):
            app = App()

        # Mock successful yt-dlp info command
        info_result = Mock()
        info_result.returncode = 0
        info_result.stdout = json.dumps({"fps": 25})

        mock_subprocess.return_value = info_result

        with patch('tkinter.filedialog.asksaveasfilename', return_value=""), \
             patch.object(app, 'update_status') as mock_update, \
             patch.object(app, 'reset_button') as mock_reset:

            app.prompt_for_save_location("https://x.com/test/status/123", "123", 25)

        mock_update.assert_called_with("Download cancelled.", "gray")
        mock_reset.assert_called_once()

    @pytest.mark.skipif(is_headless(), reason="Skipping GUI test in headless environment")
    def test_workflow_with_default_fps_fallback(self, mock_subprocess, mock_video_file_clip):
        """Test workflow when FPS detection fails and uses default."""
        with patch('os.environ', {'DISPLAY': ':99'}):
            app = App()

        # Mock yt-dlp info command with invalid JSON
        info_result = Mock()
        info_result.returncode = 0
        info_result.stdout = "invalid json"

        # Mock successful download
        download_result = Mock()
        download_result.returncode = 0

        mock_subprocess.side_effect = [info_result, download_result]

        with patch('os.path.exists', return_value=True), \
             patch('tkinter.filedialog.asksaveasfilename', return_value="/tmp/test.gif"), \
             patch.object(app, 'update_status') as mock_update:

            app.get_video_info("https://x.com/test/status/123")

        # Should proceed with default FPS (15)
        # The prompt_for_save_location would be called with default FPS

    @pytest.mark.skipif(is_headless(), reason="Skipping GUI test in headless environment")
    def test_temp_file_cleanup_on_success(self, mock_subprocess, mock_video_file_clip, temp_dir):
        """Test that temporary files are cleaned up after successful conversion."""
        with patch('os.environ', {'DISPLAY': ':99'}):
            app = App()

        # Mock successful download
        download_result = Mock()
        download_result.returncode = 0
        mock_subprocess.return_value = download_result

        output_gif = os.path.join(temp_dir, "output.gif")
        temp_video = os.path.join(os.getcwd(), "temp_video.mp4")

        # Create a mock temp file
        with open(temp_video, 'w') as f:
            f.write("mock video data")

        with patch('os.path.exists', return_value=True), \
             patch.object(app, 'update_status'), \
             patch.object(app, 'reset_button', create=True):

            app.download_and_convert("https://x.com/test/status/123", output_gif, 30)

        # Temp file should be removed
        assert not os.path.exists(temp_video)

    @pytest.mark.skipif(is_headless(), reason="Skipping GUI test in headless environment")
    def test_temp_file_cleanup_on_error(self, mock_subprocess, temp_dir):
        """Test that temporary files are cleaned up even when conversion fails."""
        with patch('os.environ', {'DISPLAY': ':99'}):
            app = App()

        # Mock failed download
        download_result = Mock()
        download_result.returncode = 1
        mock_subprocess.return_value = download_result

        temp_video = os.path.join(os.getcwd(), "temp_video.mp4")

        # Create a mock temp file
        with open(temp_video, 'w') as f:
            f.write("mock video data")

        with patch('os.path.exists', return_value=True), \
             patch.object(app, 'update_status'), \
             patch.object(app, 'reset_button', create=True):

            app.download_and_convert("https://x.com/test/status/123", "/tmp/output.gif", 30)

        # Temp file should still be removed
        assert not os.path.exists(temp_video)