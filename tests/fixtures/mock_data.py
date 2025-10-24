# Sample data for testing Twitter/X video downloader

# Sample Twitter/X URLs for testing
SAMPLE_URLS = {
    "valid_twitter": "https://twitter.com/username/status/1234567890123456789",
    "valid_x": "https://x.com/username/status/9876543210987654321",
    "with_query": "https://x.com/username/status/1234567890123456789?s=20&t=abc",
    "invalid_no_status": "https://x.com/username",
    "invalid_other_site": "https://youtube.com/watch?v=123456789",
    "empty": "",
    "malformed": "not-a-url"
}

# Sample yt-dlp JSON output for video info
SAMPLE_VIDEO_INFO = {
    "id": "1234567890123456789",
    "title": "Sample Twitter Video",
    "duration": 5.5,
    "fps": 30,
    "width": 1920,
    "height": 1080,
    "format": "bestvideo[ext=mp4]",
    "ext": "mp4",
    "filesize": 2048576,
    "url": "https://video.twimg.com/ext_tw_video/1234567890123456789/pu/vid/1920x1080/sample.mp4"
}

# Sample video info with different FPS values
SAMPLE_VIDEO_INFO_VARIATIONS = {
    "high_fps": {**SAMPLE_VIDEO_INFO, "fps": 60},
    "low_fps": {**SAMPLE_VIDEO_INFO, "fps": 15},
    "no_fps": {**SAMPLE_VIDEO_INFO, "fps": None},
    "short_video": {**SAMPLE_VIDEO_INFO, "duration": 1.2},
    "long_video": {**SAMPLE_VIDEO_INFO, "duration": 120.0}
}

# Sample subprocess results
SAMPLE_SUBPROCESS_RESULTS = {
    "success_info": {
        "returncode": 0,
        "stdout": '{"fps": 30, "duration": 5.5}',
        "stderr": ""
    },
    "success_download": {
        "returncode": 0,
        "stdout": "",
        "stderr": ""
    },
    "failure_download": {
        "returncode": 1,
        "stdout": "",
        "stderr": "ERROR: Unable to download video"
    },
    "invalid_json": {
        "returncode": 0,
        "stdout": "invalid json response",
        "stderr": ""
    }
}

# Sample file paths for testing
SAMPLE_FILE_PATHS = {
    "temp_video": "temp_video.mp4",
    "output_gif": "sample_video.gif",
    "output_gif_with_path": "/tmp/sample_video.gif",
    "nonexistent": "/nonexistent/path/file.gif"
}

# Sample error messages
SAMPLE_ERROR_MESSAGES = {
    "url_empty": "Error: Please paste a URL first.",
    "download_failed": "Error: Download failed. Check console.",
    "file_not_found": "Error: Download file not found.",
    "video_processing": "Error processing video: VideoFileClip returned None",
    "temp_file_missing": "Error: Temporary video file not found.",
    "file_access": "Error accessing files.",
    "unexpected": "An unexpected error occurred: {error}",
    "cancelled": "Download cancelled.",
    "success": "Success! Saved as {filename}"
}

# Sample status messages
SAMPLE_STATUS_MESSAGES = {
    "fetching_info": "Fetching video info...",
    "downloading": "Downloading for conversion at {fps} FPS...",
    "converting": "Converting to GIF at {fps} FPS...",
    "success": "Success! Saved as {filename}"
}

# Sample platform-specific data
SAMPLE_PLATFORM_DATA = {
    "windows": {
        "yt_dlp_exe": "yt-dlp.exe",
        "ffmpeg_binary": "ffmpeg.exe",
        "creationflags": 0x08000000  # CREATE_NO_WINDOW
    },
    "linux": {
        "yt_dlp_exe": "yt-dlp",
        "ffmpeg_binary": "ffmpeg",
        "creationflags": 0
    },
    "macos": {
        "yt_dlp_exe": "yt-dlp",
        "ffmpeg_binary": "ffmpeg",
        "creationflags": 0
    }
}