"""
Configuration management for Social Media GIF Downloader.
Handles saving and loading user preferences to a JSON config file.
"""

import json
import logging
import os
from pathlib import Path
from typing import Optional, Dict, Any


class Config:
    CONFIG_FILENAME = ".social_media_gif_downloader.json"
    
    DEFAULT_SETTINGS = {
        "default_save_location": "",
        "preferred_output_format": "gif",
        "fps_settings": 15
    }
    
    def __init__(self):
        self.config_path = self._get_config_path()
        self.settings = self._load_config()
    
    def _get_config_path(self) -> Path:
        """Get the path to the config file in the user's home directory."""
        home_dir = Path.home()
        return home_dir / self.CONFIG_FILENAME
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file, creating it with defaults if it doesn't exist."""
        if not self.config_path.exists():
            logging.info(f"Config file not found at {self.config_path}. Creating with defaults.")
            self._save_config(self.DEFAULT_SETTINGS)
            return self.DEFAULT_SETTINGS.copy()
        
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                loaded_settings = json.load(f)
            
            settings = self.DEFAULT_SETTINGS.copy()
            settings.update(loaded_settings)
            logging.info(f"Config loaded from {self.config_path}")
            return settings
        
        except (json.JSONDecodeError, IOError) as e:
            logging.error(f"Error loading config from {self.config_path}: {e}")
            return self.DEFAULT_SETTINGS.copy()
    
    def _save_config(self, settings: Dict[str, Any]) -> None:
        """Save configuration to JSON file."""
        try:
            with open(self.config_path, 'w', encoding='utf-8') as f:
                json.dump(settings, f, indent=4)
            logging.info(f"Config saved to {self.config_path}")
        except IOError as e:
            logging.error(f"Error saving config to {self.config_path}: {e}")
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value."""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any) -> None:
        """Set a configuration value and save to disk."""
        self.settings[key] = value
        self._save_config(self.settings)
    
    def get_default_save_location(self) -> str:
        """Get the default save location."""
        return self.settings.get("default_save_location", "")
    
    def set_default_save_location(self, location: str) -> None:
        """Set the default save location."""
        self.set("default_save_location", location)
    
    def get_preferred_output_format(self) -> str:
        """Get the preferred output format ('gif' or 'mp4')."""
        return self.settings.get("preferred_output_format", "gif")
    
    def set_preferred_output_format(self, format: str) -> None:
        """Set the preferred output format ('gif' or 'mp4')."""
        if format not in ["gif", "mp4"]:
            logging.warning(f"Invalid output format: {format}. Defaulting to 'gif'.")
            format = "gif"
        self.set("preferred_output_format", format)
    
    def get_fps_settings(self) -> int:
        """Get the FPS settings."""
        return self.settings.get("fps_settings", 15)
    
    def set_fps_settings(self, fps: int) -> None:
        """Set the FPS settings."""
        if fps < 1 or fps > 60:
            logging.warning(f"Invalid FPS value: {fps}. Must be between 1 and 60.")
            fps = max(1, min(60, fps))
        self.set("fps_settings", fps)
