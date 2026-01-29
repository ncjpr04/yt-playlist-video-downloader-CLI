"""Enhanced CLI entry point with main menu and settings."""

import sys
from pathlib import Path
from rich.console import Console
from ytdl_cli.state import Config
from ytdl_cli.downloader import Downloader
from ytdl_cli.utils import get_quality_choices
from ytdl_cli.prompts import (
    prompt_main_menu,
    prompt_url,
    prompt_quality,
    prompt_download_directory,
    prompt_playlist_folder_name,
    prompt_settings_menu,
    display_playlist_info,
    prompt_video_selection,
    confirm_download,
    display_success,
    display_error,
    display_info
)

console = Console()


def download_workflow(config: Config, downloader: Downloader) -> int:
    """Execute the download workflow.
    
    Args:
        config: Configuration instance.
        downloader: Downloader instance.
    
    Returns:
        Exit code (0 for success, 1 for error).
    """
    # Get URL from user
    url = prompt_url()
    
    if not url:
        display_error("No URL provided")
        return 1
    
    # Validate URL
    if 'youtube.com' not in url and 'youtu.be' not in url:
        display_error("Invalid YouTube URL")
        return 1
    
    # Prompt for download directory
    default_dir = str(config.get_download_dir())
    download_dir = prompt_download_directory(default_dir, config)
    
    # Save as last used if different from default
    if download_dir != default_dir:
        config.set_last_used_dir(download_dir)
    
    # Update downloader with selected directory
    downloader.base_download_dir = Path(download_dir)
    
    # Detect video or playlist
    try:
        is_playlist, video_info = downloader.is_playlist(url)
    except RuntimeError as e:
        display_error(str(e))
        return 1
    
    # Get last used quality
    last_quality_num = config.get_last_quality()
    # Match format in quality choices (e.g., "720" -> "720p (HD)")
    quality_choices = get_quality_choices()
    last_quality = next((q for q in quality_choices if q.startswith(last_quality_num)), quality_choices[3])  # Default to 720p (HD)
    
    if is_playlist:
        # Playlist workflow
        display_info(f"Detected playlist with {len(video_info.entries)} videos")
        
        # Display playlist info
        display_playlist_info(video_info.playlist_title, video_info.entries)
        
        # Prompt for folder name
        folder_name = prompt_playlist_folder_name(video_info.playlist_title)
        
        # Select videos
        video_indices = prompt_video_selection(len(video_info.entries))
        
        if not video_indices:
            display_error("No videos selected")
            return 1
        
        # Select quality (once for all videos)
        quality = prompt_quality(last_quality)
        
        # Confirm download
        if not confirm_download(len(video_indices), quality, str(downloader.base_download_dir)):
            display_info("Download cancelled")
            return 0
        
        # Save quality preference
        config.set_last_quality(quality.replace('p', ''))
        
        # Download playlist
        success = downloader.download_playlist(
            url,
            quality,
            video_indices,
            folder_name
        )
        
        if success:
            display_success(f"Successfully downloaded {len(video_indices)} video(s)")
            return 0
        else:
            display_error("Download failed")
            return 1
    
    else:
        # Single video workflow
        display_info("Detected single video")
        
        # Select quality
        quality = prompt_quality(last_quality)
        
        # Confirm download
        if not confirm_download(1, quality, str(downloader.base_download_dir)):
            display_info("Download cancelled")
            return 0
        
        # Save quality preference
        config.set_last_quality(quality.replace('p', ''))
        
        # Download video
        success = downloader.download_single_video(url, quality)
        
        if success:
            display_success("Download complete!")
            return 0
        else:
            display_error("Download failed")
            return 1


def main():
    """Main application entry point with menu system."""
    try:
        # Initialize configuration
        config = Config()
        downloader = Downloader(config)
        
        while True:
            # Show main menu
            choice = prompt_main_menu()
            
            if choice == 'Download video/playlist':
                result = download_workflow(config, downloader)
                if result != 0:
                    # Ask if user wants to try again
                    console.print()
                    import questionary
                    if not questionary.confirm(
                        "Return to main menu?",
                        default=True
                    ).ask():
                        return result
            
            elif choice == 'Change settings':
                prompt_settings_menu(config)
            
            elif choice == 'Exit':
                console.print("\n[bold cyan]Thank you for using YouTube Downloader CLI![/bold cyan]\n")
                return 0
            
            else:
                # Cancelled or unknown
                return 0
    
    except KeyboardInterrupt:
        console.print("\n[yellow]Goodbye![/yellow]")
        return 130
    except Exception as e:
        display_error(f"Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
