"""Twitter Downloader - A GUI application to download Twitter/X videos and convert them to GIFs."""

__version__ = "1.0.0"

from .twitter_downloader import App

__all__ = ["__version__", "App"]

def main():
    """Entry point for the application."""
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()