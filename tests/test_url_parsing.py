import pytest
from twitter_downloader import App
from tests.conftest import is_headless


class TestURLParsing:
    """Tests for URL parsing functionality."""

    @pytest.mark.skipif(is_headless(), reason="Skipping GUI test in headless environment")
    def test_get_id_from_url_valid(self):
        """Test extracting tweet ID from valid Twitter/X URLs."""
        app = App()

        # Standard Twitter URL
        url1 = "https://twitter.com/user/status/1234567890123456789"
        assert app.get_id_from_url(url1) == "1234567890123456789"

        # X.com URL
        url2 = "https://x.com/user/status/9876543210987654321"
        assert app.get_id_from_url(url2) == "9876543210987654321"

        # URL with query parameters
        url3 = "https://x.com/user/status/1234567890123456789?s=20"
        assert app.get_id_from_url(url3) == "1234567890123456789"

    @pytest.mark.skipif(is_headless(), reason="Skipping GUI test in headless environment")
    def test_get_id_from_url_invalid(self):
        """Test handling of invalid URLs."""
        app = App()

        # URL without status ID
        url1 = "https://x.com/user"
        assert app.get_id_from_url(url1) == "tweet_video"

        # Non-Twitter URL
        url2 = "https://youtube.com/watch?v=123"
        assert app.get_id_from_url(url2) == "tweet_video"

        # Empty string
        url3 = ""
        assert app.get_id_from_url(url3) == "tweet_video"

        # Malformed URL
        url4 = "not-a-url"
        assert app.get_id_from_url(url4) == "tweet_video"