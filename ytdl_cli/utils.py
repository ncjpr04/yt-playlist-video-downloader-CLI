"""Utility functions for path handling, format selection, and metadata parsing."""

import re
from pathlib import Path
from typing import List, Dict, Optional


def sanitize_filename(filename: str) -> str:
    """Sanitize filename for Windows compatibility.
    
    Args:
        filename: Raw filename string.
    
    Returns:
        Sanitized filename safe for Windows filesystems.
    """
    # Remove or replace invalid Windows filename characters
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    
    # Remove leading/trailing spaces and dots
    sanitized = sanitized.strip('. ')
    
    # Limit filename length (Windows has 255 char limit)
    if len(sanitized) > 200:
        sanitized = sanitized[:200]
    
    return sanitized


def build_format_string(quality: str) -> str:
    """Build yt-dlp format selector string based on quality preference.
    
    Args:
        quality: Quality preference (e.g., "720", "1080", "720p", "1080p (FHD)").
    
    Returns:
        yt-dlp format selector string with fallback chain.
    """
    # Extract just the number from quality string (handles "1080p (FHD)" -> "1080")
    height = quality.replace('p', '').split()[0].strip()
    
    # Build format selector with proper fallback chain
    # Try to get video+audio separately, then fallback to combined formats
    format_string = (
        f"bestvideo[height<={height}][ext=mp4]+bestaudio[ext=m4a]/"
        f"bestvideo[height<={height}]+bestaudio/"
        f"best[height<={height}][ext=mp4]/"
        f"best[height<={height}]/"
        f"best"
    )
    
    return format_string


def get_quality_choices() -> List[str]:
    """Get available quality choices.
    
    Returns:
        List of quality options with labels.
    """
    return [
        '2160p (4K)',
        '1440p (2K)',
        '1080p (FHD)',
        '720p (HD)',
        '480p (SD)',
        '360p',
        '240p',
        '144p'
    ]


def parse_video_selection(selection: str, total_videos: int) -> List[int]:
    """Parse user video selection input into list of indices.
    
    Args:
        selection: User input (e.g., "all", "1-5", "1,3,5", "1-3,7,10-12").
        total_videos: Total number of videos in playlist.
    
    Returns:
        List of video indices (1-indexed).
    
    Raises:
        ValueError: If selection format is invalid.
    """
    selection = selection.strip().lower()
    
    if selection == "all":
        return list(range(1, total_videos + 1))
    
    indices = set()
    parts = selection.split(',')
    
    for part in parts:
        part = part.strip()
        
        # Handle range (e.g., "1-5")
        if '-' in part:
            try:
                start, end = part.split('-')
                start_idx = int(start.strip())
                end_idx = int(end.strip())
                
                if start_idx < 1 or end_idx > total_videos or start_idx > end_idx:
                    raise ValueError(f"Invalid range: {part}")
                
                indices.update(range(start_idx, end_idx + 1))
            except ValueError as e:
                raise ValueError(f"Invalid range format: {part}") from e
        else:
            # Handle single number
            try:
                idx = int(part)
                if idx < 1 or idx > total_videos:
                    raise ValueError(f"Index out of range: {idx}")
                indices.add(idx)
            except ValueError as e:
                raise ValueError(f"Invalid number: {part}") from e
    
    return sorted(list(indices))


def format_file_size(bytes: int) -> str:
    """Format file size in human-readable format.
    
    Args:
        bytes: File size in bytes.
    
    Returns:
        Formatted file size string.
    """
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            return f"{bytes:.2f} {unit}"
        bytes /= 1024.0
    return f"{bytes:.2f} PB"


def parse_playlist_index(video_info: Dict) -> Optional[int]:
    """Extract playlist index from video info.
    
    Args:
        video_info: Video metadata dictionary.
    
    Returns:
        Playlist index or None if not in a playlist.
    """
    return video_info.get('playlist_index') or video_info.get('n_entries')
