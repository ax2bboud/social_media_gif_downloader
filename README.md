# Social Media GIF Downloader

A user-friendly GUI application for downloading videos and GIFs from Twitter/X, Pinterest, and Instagram posts and converting them to GIF format. Built with Python, this tool leverages yt-dlp for media downloading and moviepy for high-quality GIF conversion, ensuring optimal frame rates and seamless performance.

## Features

- **Multi-Platform Support**: Download from Twitter/X, Pinterest, and Instagram (videos only from Instagram)
- **Simple GUI Interface**: Intuitive CustomTkinter-based interface for easy URL input and file saving.
- **Automatic FPS Detection**: Analyzes the source video to detect and apply the appropriate frame rate for GIF conversion.
- **High-Quality Conversion**: Uses moviepy and FFmpeg to convert videos to GIFs with preserved quality.
- **GIF Preservation**: Downloads Pinterest GIFs directly without re-encoding when possible.
- **Cross-Platform Compatibility**: Runs on all platforms including Windows, macOS, and Linux with bundled dependencies.
- **Error Handling and Logging**: Comprehensive logging for troubleshooting, especially in bundled executable mode.
- **Background Processing**: Non-blocking downloads and conversions using threading for a responsive UI.
- **Custom Save Locations**: Allows users to choose output filenames and directories via a save dialog.

## Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg (required for video processing; install system-wide)
- yt-dlp (for video downloading; can be installed via pip or system package manager)

### Option 1: Run from Source
1. Clone or download the repository.
2. Install FFmpeg:
   - **Windows**: Download from [https://ffmpeg.org/download.html#build-windows](https://ffmpeg.org/download.html#build-windows) and add to PATH.
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg` (Ubuntu/Debian) or equivalent for your distribution.
3. Install yt-dlp (optional, as it's included in requirements; for system-wide: `pip install yt-dlp` or use package manager).
4. Install required Python packages:
   ```
   pip install -r requirements.txt
   ```
5. Run the application:
   ```
   python twitter_gif_downloader.py
   ```

### Option 2: Use Pre-built Executable
1. Download the latest release from the [Releases](https://github.com/ax2bboud/social-media-gif-downloader/releases) page.
2. Extract the ZIP file.
3. Run `social_media_gif_downloader.exe` (Windows) or the appropriate executable for your platform.

## Usage

1. Launch the application.
2. Paste a social media post URL into the input field:
   - Twitter/X: `https://x.com/user/status/123456789`
   - Pinterest: `https://www.pinterest.com/pin/123456789/`
   - Instagram: `https://www.instagram.com/p/{post_id}/` or `https://www.instagram.com/reel/{reel_id}/`
3. Click "Download as GIF".
4. Choose a save location and filename for the GIF in the dialog that appears.
5. The application will download the media, detect its FPS (for videos), and convert it to a GIF.
6. Monitor progress via the status messages in the interface.

**Note**: The tool automatically detects the platform from the URL. Pinterest GIFs are downloaded directly when available, while videos from all platforms are converted to GIF format. Instagram support is limited to videos only (posts and reels).


## Requirements

- **Python Libraries**:
  - `customtkinter` (for GUI)
  - `moviepy` (for video processing)
  - `yt-dlp` (for video downloading)
- **System Dependencies**:
  - FFmpeg (required for video processing; install from [https://ffmpeg.org/download.html](https://ffmpeg.org/download.html) or via package manager)
  - yt-dlp (included in Python requirements; system installation optional)
- **Operating System**: Windows 10+, macOS 10.14+, or Linux with Python support.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Attributions

This project relies on several open-source dependencies. For detailed information about licenses, copyrights, and attribution requirements for all dependencies used in this project, please refer to the [ATTRIBUTIONS.md](ATTRIBUTIONS.md) file.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature-name`.
3. Make your changes and commit: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature/your-feature-name`.
5. Open a Pull Request.

For bug reports or feature requests, please use the issues page.

---

**Disclaimer**: This tool is for personal use only. Respect the terms of service and copyright laws of Twitter/X, Pinterest, and Instagram when downloading content.