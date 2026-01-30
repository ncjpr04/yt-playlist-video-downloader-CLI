"""YouTube downloader using yt-dlp backend."""

import json
import subprocess
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeRemainingColumn
from ytdl_cli.utils import build_format_string, sanitize_filename
from ytdl_cli.state import Config

console = Console()


def check_ffmpeg() -> bool:
    """Check if FFmpeg is available.
    
    Returns:
        True if FFmpeg is available, False otherwise.
    """
    try:
        subprocess.run(
            ['ffmpeg', '-version'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False
        )
        return True
    except FileNotFoundError:
        return False


def warn_no_ffmpeg(quality: str):
    """Warn user if FFmpeg is not available for high quality downloads.
    
    Args:
        quality: Selected quality string.
    """
    # Extract quality number
    try:
        quality_num = int(quality.replace('p', '').split()[0].strip())
    except (ValueError, IndexError):
        return
    
    # High quality (720p+) needs FFmpeg for best results
    if quality_num >= 720 and not check_ffmpeg():
        console.print()
        console.print("[bold yellow]⚠ FFmpeg not found![/bold yellow]")
        console.print("[yellow]For {quality}, FFmpeg is needed to merge video+audio streams.[/yellow]")
        console.print("[dim]Without FFmpeg, you'll get separate video and audio files.[/dim]")
        console.print("[dim]Install: choco install ffmpeg (or download from ffmpeg.org)[/dim]")
        console.print()


class VideoInfo:
    """Container for video metadata."""
    
    def __init__(self, data: dict):
        """Initialize video info from yt-dlp metadata."""
        self.id = data.get('id', '')
        self.title = data.get('title', 'Unknown')
        self.duration = data.get('duration', 0)
        self.duration_string = data.get('duration_string', 'N/A')
        self.url = data.get('webpage_url', data.get('url', ''))
        self.is_playlist = '_type' in data and data['_type'] == 'playlist'
        self.playlist_title = data.get('playlist_title', data.get('title', ''))
        self.playlist_count = data.get('playlist_count', 0)
        self.entries = data.get('entries', [])


class Downloader:
    """Handles video download operations using yt-dlp."""
    
    def __init__(self, config: Config):
        """Initialize downloader with configuration.
        
        Args:
            config: Configuration instance.
        """
        self.config = config
        self.base_download_dir = config.get_download_dir()
    
    def fetch_metadata(self, url: str) -> VideoInfo:
        """Fetch video or playlist metadata.
        
        Args:
            url: YouTube URL.
        
        Returns:
            VideoInfo instance with metadata.
        
        Raises:
            RuntimeError: If metadata fetch fails.
        """
        console.print("[cyan]Fetching video information...[/cyan]")
        
        cmd = [
            'yt-dlp',
            '--dump-json',
            '--flat-playlist',
            '--no-warnings',
            url
        ]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                encoding='utf-8'
            )
            
            # Parse JSON output (might be multiple lines for playlists)
            lines = result.stdout.strip().split('\n')
            
            if len(lines) > 1:
                # Playlist - parse first line for playlist info
                first_data = json.loads(lines[0])
                
                # Check if first line is playlist metadata
                if first_data.get('_type') == 'playlist':
                    # Parse all video entries
                    entries = []
                    for line in lines[1:]:
                        if line.strip():
                            entries.append(json.loads(line))
                    first_data['entries'] = entries
                    return VideoInfo(first_data)
                else:
                    # Old format - all lines are entries
                    entries = [json.loads(line) for line in lines if line.strip()]
                    # Create synthetic playlist info
                    playlist_data = {
                        '_type': 'playlist',
                        'title': f"Playlist ({len(entries)} videos)",
                        'playlist_title': f"Playlist ({len(entries)} videos)",
                        'playlist_count': len(entries),
                        'entries': entries
                    }
                    return VideoInfo(playlist_data)
            else:
                # Single video
                data = json.loads(lines[0])
                return VideoInfo(data)
                
        except subprocess.CalledProcessError as e:
            error_msg = e.stderr if e.stderr else str(e)
            raise RuntimeError(f"Failed to fetch metadata: {error_msg}")
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse metadata: {e}")
    
    def is_playlist(self, url: str) -> Tuple[bool, VideoInfo]:
        """Check if URL is a playlist.
        
        Args:
            url: YouTube URL.
        
        Returns:
            Tuple of (is_playlist, video_info).
        """
        info = self.fetch_metadata(url)
        return (info.is_playlist or len(info.entries) > 0, info)
    
    def download_single_video(self, url: str, quality: str, output_dir: Optional[Path] = None) -> bool:
        """Download a single video.
        
        Args:
            url: YouTube URL.
            quality: Quality preference (e.g., "720p").
            output_dir: Output directory (defaults to base download dir).
        
        Returns:
            True if successful, False otherwise.
        """
        if output_dir is None:
            output_dir = self.base_download_dir
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Warn about FFmpeg if needed
        warn_no_ffmpeg(quality)
        
        # Get format string
        quality_num = quality.replace('p', '')
        format_str = build_format_string(quality_num)
        
        # Get quality-specific archive file to allow re-downloading in different quality
        archive_file = self.config.get_archive_file(quality=quality)
        
        # Build output template
        output_template = str(output_dir / "%(title)s.%(ext)s")
        
        cmd = [
            'yt-dlp',
            '-f', format_str,
            '--merge-output-format', 'mp4',
            '--continue',  # Resume partial downloads
            '--concurrent-fragments', '4',
            '--no-warnings',
            '-o', output_template,
            url
        ]
        
        try:
            # Run with progress display
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                errors='replace',  # Replace non-UTF8 characters
                bufsize=1
            )
            
            # Store all output for error reporting
            all_output = []
            
            with Progress(
                TextColumn("[bold blue]{task.description}"),
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.0f}%",
                TimeRemainingColumn(),
                console=console
            ) as progress:
                task = progress.add_task("Downloading...", total=100)
                
                for line in process.stdout:
                    all_output.append(line)  # Store all lines
                    
                    # Parse yt-dlp output for progress
                    if '[download]' in line and '%' in line:
                        try:
                            # Extract percentage
                            percent_match = line.split('%')[0].split()[-1]
                            percent = float(percent_match)
                            progress.update(task, completed=percent)
                        except (ValueError, IndexError):
                            pass
            
            # Get the return code
            returncode = process.wait()
            
            if returncode != 0:
                # Show the last error lines
                error_lines = [l for l in all_output if 'ERROR' in l.upper() or 'error' in l]
                if not error_lines:
                    error_lines = all_output[-10:]  # Show last 10 lines
                
                console.print(f"\n[bold red]yt-dlp error:[/bold red]")
                for line in error_lines[-5:]:  # Show last 5 error lines
                    console.print(f"[red]{line.strip()}[/red]")
                raise RuntimeError(f"Download failed with code {returncode}")
            
            return True
            
        except subprocess.TimeoutExpired:
            process.kill()
            console.print("[bold red]Download timed out[/bold red]")
            return False
        except Exception as e:
            console.print(f"[bold red]Error: {str(e)}[/bold red]")
            return False
    
    def download_playlist(
        self,
        url: str,
        quality: str,
        video_indices: List[int],
        playlist_title: str
    ) -> bool:
        """Download selected videos from a playlist.
        
        Args:
            url: Playlist URL.
            quality: Quality preference.
            video_indices: List of video indices to download (1-indexed).
            playlist_title: Title of the playlist.
        
        Returns:
            True if successful, False otherwise.
        """
        # Sanitize playlist title for folder name
        safe_playlist_title = sanitize_filename(playlist_title)
        playlist_dir = self.base_download_dir / safe_playlist_title
        playlist_dir.mkdir(parents=True, exist_ok=True)
        
        # Get format string
        quality_num = quality.replace('p', '')
        format_str = build_format_string(quality_num)
        
        # Get quality-specific archive file for this playlist
        archive_file = self.config.get_archive_file(safe_playlist_title, quality=quality)
        
        # Build output template with numbering
        output_template = str(playlist_dir / "%(playlist_index)02d_%(title)s.%(ext)s")
        
        # Convert indices to playlist item spec
        playlist_items = ','.join(map(str, video_indices))
        
        cmd = [
            'yt-dlp',
            '-f', format_str,
            '--merge-output-format', 'mp4',
            '--continue',  # Resume partial downloads
            '--playlist-items', playlist_items,
            '--concurrent-fragments', '4',
            '--no-warnings',
            '-o', output_template,
            url
        ]
        
        try:
            console.print(f"\n[cyan]Downloading {len(video_indices)} video(s) to:[/cyan]")
            console.print(f"[white]{playlist_dir}[/white]\n")
            
            # Warn about FFmpeg if needed
            warn_no_ffmpeg(quality)
            
            # Run with progress display
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                encoding='utf-8',
                bufsize=1
            )
            
            current_file = "Downloading..."
            
            with Progress(
                TextColumn("[bold blue]{task.description}", justify="left"),
                BarColumn(),
                "[progress.percentage]{task.percentage:>3.0f}%",
                TimeRemainingColumn(),
                console=console
            ) as progress:
                task = progress.add_task(current_file, total=100)
                
                for line in process.stdout:
                    # Update current file
                    if '[download] Destination:' in line:
                        filename = line.split('Destination:')[1].strip()
                        current_file = Path(filename).name
                        if len(current_file) > 40:
                            current_file = current_file[:37] + "..."
                        progress.update(task, description=current_file, completed=0)
                    
                    # Parse progress
                    elif '[download]' in line and '%' in line:
                        try:
                            percent_str = line.split('%')[0].split()[-1]
                            percent = float(percent_str)
                            progress.update(task, completed=percent)
                        except (ValueError, IndexError):
                            pass
                    
                    # Check for completion
                    elif 'has already been downloaded' in line or '100%' in line:
                        progress.update(task, completed=100)
                
                process.wait()
            
            if process.returncode == 0:
                return True
            else:
                console.print(f"[red]Download failed with code {process.returncode}[/red]")
                return False
                
        except Exception as e:
            console.print(f"[red]Download error: {e}[/red]")
            return False
