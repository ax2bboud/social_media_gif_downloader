"""
Copyright (c) 2024 ax2bboud

This software is licensed under the MIT License. See LICENSE file for details.

This project uses the following third-party libraries:
- moviepy (MIT License, Copyright (c) 2015 Zulko)
- customtkinter (MIT License, Copyright (c) 2021 Tom Schimansky)
- yt-dlp (Unlicense - Public Domain)
- FFmpeg (LGPL v2.1 or later, Copyright (c) 2000-2023 the FFmpeg developers)

For full attributions and license texts, see ATTRIBUTIONS.md.
"""

__version__ = "1.0.1"

import sys
import os
import re  # For parsing the URL
import json  # For reading video metadata
import logging
import platform
from typing import Optional, Any

# Configure logging
if getattr(sys, 'frozen', False):
    # In bundled exe, log to a file since console may not be visible
    log_file = os.path.join(os.path.dirname(sys.executable), 'twitter_downloader.log')
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
else:
    # In development, log to console
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

# --- PYINSTALLER FFMPEG FIX ---
# This block must be at the VERY TOP, before moviepy is imported.
# It tells the script where to find ffmpeg.exe when it's bundled.
if getattr(sys, 'frozen', False):
    if hasattr(sys, '_MEIPASS'):
        # This is the temporary path PyInstaller creates
        base_path = sys._MEIPASS
    else:
        # Fallback for some environments
        base_path = os.path.dirname(sys.executable)

    # Set the environment variable for moviepy
    ffmpeg_binary = "ffmpeg.exe" if platform.system() == "Windows" else "ffmpeg"
    ffmpeg_path = os.path.join(base_path, ffmpeg_binary)
    os.environ["FFMPEG_BINARY"] = ffmpeg_path
    logging.info(f"Frozen mode: FFMPEG_BINARY set to {ffmpeg_path}")
else:
    logging.info("Running in non-frozen mode")
# --- END OF FIX ---


# Now, when moviepy is imported, it will use the path we just set
from moviepy.video.io.VideoFileClip import VideoFileClip
import customtkinter as ctk
import tkinter.filedialog as filedialog
import threading
import subprocess


# --- Constants ---
TEMP_VIDEO_FILE = "temp_video.mp4"
DEFAULT_GIF_FPS = 15  # Fallback if FPS detection fails

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("Twitter GIF Downloader")
        self.geometry("500x250")
        ctk.set_appearance_mode("System")

        # --- Widgets ---
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        # URL Entry
        self.url_label = ctk.CTkLabel(self, text="Paste Twitter/X Post URL:")
        self.url_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.url_entry = ctk.CTkEntry(self, placeholder_text="https://x.com/user/status/123...")
        self.url_entry.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        # Download Button
        self.download_button = ctk.CTkButton(
            self, text="Download as GIF",
            command=self.start_get_info_thread
        )
        self.download_button.grid(row=2, column=0, padx=20, pady=20, sticky="n")

        # Status Label
        self.status_label = ctk.CTkLabel(self, text="")
        self.status_label.grid(row=3, column=0, padx=20, pady=(10, 20), sticky="w")

    def get_id_from_url(self, url: str) -> str:
        """
        Parses the tweet ID from the URL to use as a filename.
        """
        match = re.search(r"status/(\d+)", url)
        if match:
            return match.group(1)
        return "tweet_video"

    def start_get_info_thread(self) -> None:
        """
        Starts a background thread to fetch the video FPS and default name.
        """
        url = self.url_entry.get()
        if not url:
            self.update_status("Error: Please paste a URL first.", "red")
            return

        self.download_button.configure(state="disabled", text="Getting info...")
        self.update_status("Fetching video info...", "white")

        info_thread = threading.Thread(
            target=self.get_video_info,
            args=(url,),
            daemon=True
        )
        info_thread.start()

    def get_video_info(self, url: str) -> None:
        """
        (Background Thread)
        Runs yt-dlp to get FPS and generates a default filename.
        """
        try:
            yt_dlp_executable = 'yt-dlp.exe' if platform.system() == "Windows" else 'yt-dlp'
            yt_dlp_command_info = [
                yt_dlp_executable,
                '--print-json',
                '-f', 'bestvideo[ext=mp4]',
                '--skip-download',
                url
            ]

            result_info = subprocess.run(
                yt_dlp_command_info,
                capture_output=True,
                text=True,
                encoding='utf-8',
                creationflags=(subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
            )

            video_fps = DEFAULT_GIF_FPS
            if result_info.returncode == 0 and result_info.stdout:
                try:
                    video_info = json.loads(result_info.stdout)
                    video_fps = video_info.get('fps', DEFAULT_GIF_FPS)
                except json.JSONDecodeError:
                    pass  # Use default FPS

            default_name = self.get_id_from_url(url)

            self.after(0, self.prompt_for_save_location, url, default_name, video_fps)

        except subprocess.CalledProcessError as e:
            self.update_status(f"Error running yt-dlp: {e}", "red")
            logging.error(f"yt-dlp subprocess error: {e}")
            self.after(0, self.reset_button)
        except json.JSONDecodeError as e:
            self.update_status("Error parsing video info.", "red")
            logging.error(f"JSON decode error: {e}")
            self.after(0, self.reset_button)
        except Exception as e:
            self.update_status(f"Unexpected error getting info: {e}", "red")
            logging.error(f"Unexpected error in get_video_info: {e}")
            self.after(0, self.reset_button)

    def prompt_for_save_location(self, url: str, default_name: str, detected_fps: int) -> None:
        """
        (Main Thread)
        Opens the "Save As" dialog with the fetched info.
        """
        output_gif_file = filedialog.asksaveasfilename(
            defaultextension=".gif",
            filetypes=[("GIF files", "*.gif")],
            title="Save GIF as...",
            initialfile=f"{default_name}.gif"
        )

        if not output_gif_file:
            self.update_status("Download cancelled.", "gray")
            self.reset_button()
            return

        self.update_status(f"Downloading for conversion at {detected_fps} FPS...", "white")

        download_thread = threading.Thread(
            target=self.download_and_convert,
            args=(url, output_gif_file, detected_fps),
            daemon=True
        )
        download_thread.start()


    def download_and_convert(self, url: str, output_gif_file: str, video_fps: int) -> None:
        """
        (Background Thread)
        The main logic: downloads video, converts to GIF, and cleans up.
        """
        try:
            # Log ffmpeg path
            ffmpeg_env = os.environ.get("FFMPEG_BINARY", "Not set")
            logging.info(f"FFMPEG_BINARY: {ffmpeg_env}")
            if getattr(sys, 'frozen', False):
                base_path = (sys._MEIPASS if hasattr(sys, '_MEIPASS')
                             else os.path.dirname(sys.executable))
                logging.info(f"Frozen mode: base_path = {base_path}")

            yt_dlp_executable = 'yt-dlp.exe' if platform.system() == "Windows" else 'yt-dlp'
            yt_dlp_command_dl = [
                yt_dlp_executable,
                '-f', 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                '-o', TEMP_VIDEO_FILE,
                '--force-overwrites',
                url
            ]
            result_dl = subprocess.run(
                yt_dlp_command_dl,
                capture_output=True,
                text=True,
                creationflags=(subprocess.CREATE_NO_WINDOW if platform.system() == "Windows" else 0)
            )

            if result_dl.returncode != 0:
                self.update_status("Error: Download failed. Check console.", "red")
                logging.error(f"yt-dlp Error: {result_dl.stderr}")
                return

            if not os.path.exists(TEMP_VIDEO_FILE):
                self.update_status("Error: Download file not found.", "red")
                logging.error("TEMP_VIDEO_FILE not found after download")
                return

            # Log file size
            file_size = os.path.getsize(TEMP_VIDEO_FILE)
            logging.info(f"TEMP_VIDEO_FILE exists, size: {file_size} bytes")

            self.update_status(f"Converting to GIF at {video_fps} FPS...", "white")

            logging.info("Creating VideoFileClip...")
            clip = VideoFileClip(TEMP_VIDEO_FILE)
            logging.info(f"VideoFileClip created: {clip is not None}, duration: {clip.duration if clip else 'N/A'}")

            if clip is None:
                raise ValueError("VideoFileClip returned None")

            # Disable moviepy's default logger to prevent tqdm issues in bundled apps
            try:
                from moviepy import logger
                original_logger = logger.get_logger()
                logger.set_logger(None)  # Disable logging to avoid tqdm issues
                logger_restored = True
            except ImportError:
                # If logger import fails, just proceed without logger management
                logger_restored = False
                logging.warning("Could not import moviepy logger, proceeding without logger management")

            try:
                clip.write_gif(output_gif_file, fps=video_fps, logger=None)
                logging.info("write_gif completed")
            finally:
                # Restore original logger if it was successfully imported
                if logger_restored:
                    try:
                        logger.set_logger(original_logger)
                    except Exception as e:
                        logging.warning(f"Could not restore moviepy logger: {e}")

            self.update_status(f"Success! Saved as {os.path.basename(output_gif_file)}", "green")

        except subprocess.CalledProcessError as e:
            self.update_status("Error during video download.", "red")
            logging.error(f"yt-dlp download error: {e}")
        except FileNotFoundError as e:
            self.update_status("Error: Temporary video file not found.", "red")
            logging.error(f"File not found: {e}")
        except ValueError as e:
            self.update_status(f"Error processing video: {e}", "red")
            logging.error(f"Value error: {e}")
        except OSError as e:
            self.update_status("Error accessing files.", "red")
            logging.error(f"OS error: {e}")
        except Exception as e:
            self.update_status(f"An unexpected error occurred: {e}", "red")
            import traceback
            logging.error(f"Exception in download_and_convert: {e}")
            logging.error("Full traceback:")
            logging.error(traceback.format_exc())

        finally:
            # Ensure clip is closed before attempting to delete the file
            try:
                if 'clip' in locals() and clip is not None:
                    clip.close()
                    logging.info("VideoFileClip closed")
            except Exception as e:
                logging.warning(f"Error closing clip: {e}")

            # Try to remove temp file, with retry on permission error
            if os.path.exists(TEMP_VIDEO_FILE):
                try:
                    os.remove(TEMP_VIDEO_FILE)
                    logging.info("TEMP_VIDEO_FILE removed")
                except PermissionError:
                    logging.warning("PermissionError removing TEMP_VIDEO_FILE - file may still be in use")
                    # Could add a retry mechanism here if needed
            self.after(0, self.reset_button)

    def update_status(self, message: str, color: str) -> None:
        """Safely updates the status label from any thread."""
        def do_update():
            self.status_label.configure(text=message, text_color=color)
        self.after(0, do_update)

    def reset_button(self) -> None:
        """Safely re-enables the download button."""
        self.download_button.configure(state="normal", text="Download as GIF")


if __name__ == "__main__":
    app = App()
    app.mainloop()
