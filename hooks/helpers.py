"""
PyInstaller Helper Functions for social-media-gif-downloader

This module provides reusable functions to assist with the PyInstaller bundling
process, particularly for locating and handling external binaries like ffmpeg and yt-dlp.
"""

import os
import sys
import shutil
from pathlib import Path

def find_binary(name: str) -> str:
    """
    Finds a binary in common locations and returns its full path.

    Search order:
    1. Project root directory.
    2. A 'bin' subdirectory in the project root.
    3. System's PATH.

    Args:
        name (str): The name of the binary to find (e.g., 'ffmpeg.exe' or 'yt-dlp').

    Returns:
        str: The full path to the binary, or an empty string if not found.
    """
    # 1. Check project root
    if os.path.exists(name):
        print(f"[INFO] Found binary '{name}' in project root.")
        return name

    # 2. Check 'bin' subdirectory
    bin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'bin', name)
    if os.path.exists(bin_path):
        print(f"[INFO] Found binary '{name}' in 'bin' directory.")
        return bin_path

    # 3. Check system PATH
    path = shutil.which(name)
    if path:
        print(f"[INFO] Found binary '{name}' in system PATH: {path}")
        return path
    
    print(f"[WARNING] Binary '{name}' not found in project root, 'bin' directory, or system PATH.")
    return ""