"""State management and configuration persistence."""

import json
from pathlib import Path
from typing import Optional


class Config:
    """Manages application configuration and state persistence."""
    
    def __init__(self):
        """Initialize configuration manager."""
        self.config_dir = Path.home() / ".ytdl_cli"
        self.config_file = self.config_dir / "config.json"
        # Use user's Downloads folder as default
        self.base_download_dir = Path.home() / "Downloads" / "YouTube"
        self._ensure_config_exists()
    
    def _ensure_config_exists(self) -> None:
        """Create config directory and file if they don't exist."""
        self.config_dir.mkdir(parents=True, exist_ok=True)
        
        if not self.config_file.exists():
            self._write_config({
                "last_quality": "720",
                "download_dir": str(self.base_download_dir)
            })
    
    def _read_config(self) -> dict:
        """Read configuration from file."""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _write_config(self, data: dict) -> None:
        """Write configuration to file."""
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
    
    def get_last_quality(self) -> str:
        """Get the last selected quality preference."""
        config = self._read_config()
        return config.get("last_quality", "720")
    
    def set_last_quality(self, quality: str) -> None:
        """Save the last selected quality preference."""
        config = self._read_config()
        config["last_quality"] = quality
        self._write_config(config)
    
    def get_download_dir(self) -> Path:
        """Get the base download directory."""
        config = self._read_config()
        dir_path = config.get("download_dir", str(self.base_download_dir))
        return Path(dir_path)
    
    def set_download_dir(self, directory: str) -> None:
        """Set the base download directory.
        
        Args:
            directory: Path to the download directory.
        """
        config = self._read_config()
        config["download_dir"] = directory
        self._write_config(config)
    
    def get_last_used_dir(self) -> Optional[str]:
        """Get the last used download directory (not default).
        
        Returns:
            Last used directory or None if same as default.
        """
        config = self._read_config()
        last_used = config.get("last_used_dir")
        default = str(self.get_download_dir())
        
        # Only return if different from default
        if last_used and last_used != default:
            return last_used
        return None
    
    def set_last_used_dir(self, directory: str) -> None:
        """Save the last used download directory.
        
        Args:
            directory: Path to the last used directory.
        """
        config = self._read_config()
        config["last_used_dir"] = directory
        self._write_config(config)
    
    def get_archive_file(self, playlist_title: Optional[str] = None, quality: str = "") -> Path:
        """Get the path to the download archive file.
        
        Args:
            playlist_title: If provided, returns archive file in playlist folder.
            quality: Quality setting (e.g., "720p") to create quality-specific archive.
        
        Returns:
            Path to the download archive file.
        """
        base_dir = self.get_download_dir()
        
        # Create quality-specific archive filename
        quality_suffix = f"_{quality}" if quality else ""
        archive_name = f"downloads{quality_suffix}.archive"
        
        if playlist_title:
            playlist_dir = base_dir / playlist_title
            playlist_dir.mkdir(parents=True, exist_ok=True)
            return playlist_dir / archive_name
        else:
            base_dir.mkdir(parents=True, exist_ok=True)
            return base_dir / archive_name
