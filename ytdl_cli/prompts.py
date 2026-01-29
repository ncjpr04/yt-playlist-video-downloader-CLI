"""Interactive user prompts with arrow key navigation."""

from typing import Optional, List
from pathlib import Path
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.align import Align
import questionary
from questionary import Style
from ytdl_cli.utils import get_quality_choices, parse_video_selection

console = Console()

# Custom style for questionary
custom_style = Style([
    ('qmark', 'fg:#673ab7 bold'),
    ('question', 'bold'),
    ('answer', 'fg:#f44336 bold'),
    ('pointer', 'fg:#673ab7 bold'),
    ('highlighted', 'fg:#673ab7 bold'),
    ('selected', 'fg:#cc5454'),
    ('separator', 'fg:#cc5454'),
    ('instruction', ''),
    ('text', ''),
])


def show_banner():
    """Display app banner."""
    banner = """
    ╔══════════════════════════════════════════════════════╗
    ║                                                      ║
    ║         YouTube Downloader CLI v1.0                  ║
    ║         Powered by yt-dlp                            ║
    ║                                                      ║
    ╚══════════════════════════════════════════════════════╝
    """
    console.print(Panel(
        Align.center(banner, vertical="middle"),
        style="bold cyan",
        border_style="cyan"
    ))


def prompt_main_menu() -> str:
    """Show main menu with options.
    
    Returns:
        Selected menu option.
    """
    show_banner()
    
    choices = [
        'Download video/playlist',
        'Change settings',
        'Exit'
    ]
    
    answer = questionary.select(
        "What would you like to do?",
        choices=choices,
        style=custom_style,
        use_indicator=True,
        use_shortcuts=True
    ).ask()
    
    return answer if answer else 'Exit'


def prompt_url() -> str:
    """Prompt user for YouTube URL.
    
    Returns:
        YouTube URL entered by user.
    """
    console.print()
    url = questionary.text(
        "Paste YouTube URL:",
        style=custom_style,
        validate=lambda x: len(x) > 0 or "URL cannot be empty"
    ).ask()
    
    return url.strip() if url else ""


def prompt_quality(default_quality: str = "720p (HD)") -> str:
    """Prompt user to select video quality using arrow keys.
    
    Args:
        default_quality: Default quality to pre-select.
    
    Returns:
        Selected quality (e.g., "720p (HD)").
    """
    choices = get_quality_choices()
    
    # Ensure default is in choices
    if default_quality not in choices:
        default_quality = choices[3]  # Default to 720p (HD)
    
    console.print()
    answer = questionary.select(
        "Select video quality:",
        choices=choices,
        default=default_quality,
        style=custom_style,
        use_indicator=True,
        instruction="(Use arrow keys)"
    ).ask()
    
    return answer if answer else default_quality


def prompt_playlist_folder_name(detected_name: str) -> str:
    """Prompt user for playlist folder name.
    
    Args:
        detected_name: Playlist name detected from YouTube.
    
    Returns:
        Folder name to use for playlist.
    """
    console.print()
    console.print(f"[dim]Detected playlist: {detected_name}[/dim]")
    
    choice = questionary.select(
        "Playlist folder name:",
        choices=[
            f'Use playlist name ({detected_name[:40]}...)',
            'Enter custom folder name',
        ],
        style=custom_style,
        use_indicator=True,
        instruction="(Use arrow keys)"
    ).ask()
    
    if not choice or 'Use playlist name' in choice:
        return detected_name
    
    # Ask for custom name
    while True:
        custom_name = questionary.text(
            "Enter folder name:",
            default=detected_name,
            style=custom_style,
            validate=lambda x: len(x.strip()) > 0 or "Folder name cannot be empty"
        ).ask()
        
        if custom_name and custom_name.strip():
            # Sanitize the name
            from ytdl_cli.utils import sanitize_filename
            sanitized = sanitize_filename(custom_name.strip())
            if sanitized:
                console.print(f"[green]✓[/green] Folder: {sanitized}")
                return sanitized
        
        console.print("[yellow]Using detected name[/yellow]")
        return detected_name


def display_playlist_info(playlist_title: str, videos: List[dict]) -> None:
    """Display playlist information in a formatted table.
    
    Args:
        playlist_title: Title of the playlist.
        videos: List of video metadata dictionaries.
    """
    console.print()
    console.print(Panel(
        f"[bold green]Playlist:[/bold green] {playlist_title}\n"
        f"[bold]Total videos:[/bold] {len(videos)}",
        border_style="green"
    ))
    console.print()
    
    # Create table
    table = Table(show_header=True, header_style="bold magenta", border_style="blue")
    table.add_column("#", style="cyan", width=4, justify="right")
    table.add_column("Title", style="white")
    table.add_column("Duration", style="yellow", width=10, justify="center")
    
    for idx, video in enumerate(videos, 1):
        title = video.get('title', 'Unknown')
        duration = video.get('duration_string', 'N/A')
        
        # Truncate long titles
        if len(title) > 70:
            title = title[:67] + "..."
        
        table.add_row(str(idx), title, duration)
    
    console.print(table)
    console.print()


def prompt_video_selection(total_videos: int) -> List[int]:
    """Prompt user to select which videos to download from playlist.
    
    Args:
        total_videos: Total number of videos in playlist.
    
    Returns:
        List of selected video indices (1-indexed).
    """
    # First ask if they want all or custom selection
    choice = questionary.select(
        "Which videos do you want to download?",
        choices=[
            f'All videos ({total_videos} videos)',
            'Select specific videos',
        ],
        style=custom_style,
        use_indicator=True,
        instruction="(Use arrow keys)"
    ).ask()
    
    if not choice or 'All videos' in choice:
        return list(range(1, total_videos + 1))
    
    # Custom selection
    while True:
        console.print()
        console.print("[bold yellow]Selection examples:[/bold yellow]")
        console.print("  • Type 'all' for all videos")
        console.print("  • Type ranges: '1-10'")
        console.print("  • Type specific: '1,3,7'")
        console.print("  • Combine: '1-5,7,10-12'")
        console.print()
        
        selection = questionary.text(
            "Enter your selection:",
            style=custom_style,
            validate=lambda x: len(x) > 0 or "Selection cannot be empty"
        ).ask()
        
        if not selection:
            return []
        
        try:
            indices = parse_video_selection(selection.strip(), total_videos)
            console.print(f"\n[green]✓[/green] Selected {len(indices)} video(s)")
            return indices
        except ValueError as e:
            console.print(f"[bold red]✗ Error:[/bold red] {e}")
            console.print("[yellow]Please try again.[/yellow]\n")


def confirm_download(video_count: int, quality: str, directory: str) -> bool:
    """Ask user to confirm download.
    
    Args:
        video_count: Number of videos to download.
        quality: Selected quality.
        directory: Download directory.
    
    Returns:
        True if user confirms, False otherwise.
    """
    # Show download summary
    console.print()
    summary = f"""
    [bold]Download Summary:[/bold]
    
    • Videos: {video_count}
    • Quality: {quality}
    • Directory: {directory}
    """
    console.print(Panel(summary, border_style="yellow", title="Review"))
    
    return questionary.confirm(
        "Proceed with download?",
        default=True,
        style=custom_style
    ).ask() or False


def display_success(message: str) -> None:
    """Display success message.
    
    Args:
        message: Success message to display.
    """
    console.print()
    console.print(Panel(
        f"[bold green]✓ {message}[/bold green]",
        border_style="green"
    ))
    console.print()


def display_error(message: str) -> None:
    """Display error message.
    
    Args:
        message: Error message to display.
    """
    console.print()
    console.print(Panel(
        f"[bold red]✗ {message}[/bold red]",
        border_style="red"
    ))
    console.print()


def display_info(message: str) -> None:
    """Display info message.
    
    Args:
        message: Info message to display.
    """
    console.print(f"[bold cyan]ℹ {message}[/bold cyan]")


def prompt_download_directory(default_dir: str, config) -> str:
    """Prompt user for download directory with three options.
    
    Args:
        default_dir: Default download directory.
        config: Config instance to get last used directory.
    
    Returns:
        Selected download directory path.
    """
    console.print()
    console.print(f"[dim]Default: {default_dir}[/dim]")
    
    # Build choices
    choices = [f'Default ({default_dir})']
    
    # Add previous folder if it exists and is different
    last_used = config.get_last_used_dir()
    if last_used:
        console.print(f"[dim]Previous: {last_used}[/dim]")
        choices.append(f'Previous ({last_used})')
    
    choices.append('Custom directory...')
    
    choice = questionary.select(
        "Download directory:",
        choices=choices,
        style=custom_style,
        use_indicator=True,
        instruction="(Use arrow keys)"
    ).ask()
    
    if not choice:
        return default_dir
    
    # Handle selection
    if 'Default' in choice:
        return default_dir
    
    if 'Previous' in choice and last_used:
        return last_used
    
    # Custom directory
    while True:
        custom_path = questionary.text(
            "Enter download path:",
            default=default_dir,
            style=custom_style
        ).ask()
        
        if not custom_path or custom_path == default_dir:
            console.print("[yellow]Using default directory[/yellow]")
            return default_dir
        
        # Validate and create directory
        try:
            path = Path(custom_path.strip())
            path.mkdir(parents=True, exist_ok=True)
            console.print(f"[green]✓[/green] Will download to: {path.absolute()}")
            return str(path.absolute())
        except Exception as e:
            console.print(f"[red]✗ Invalid path: {e}[/red]")
            retry = questionary.confirm("Try again?", default=True, style=custom_style).ask()
            if not retry:
                return default_dir


def prompt_settings_menu(config) -> dict:
    """Show settings menu for changing default configurations.
    
    Args:
        config: Config instance.
    
    Returns:
        Dictionary of updated settings.
    """
    console.print()
    console.print(Panel(
        "[bold cyan]Settings[/bold cyan]",
        border_style="cyan"
    ))
    
    changes = {}
    
    while True:
        current_quality_num = config.get_last_quality()
        # Match to quality choices format
        quality_choices = get_quality_choices()
        current_quality = next((q for q in quality_choices if q.startswith(current_quality_num)), quality_choices[3])
        current_dir = str(config.get_download_dir())
        
        choices = [
            f'Default Quality: {current_quality}',
            f'Download Directory: {current_dir}',
            'Reset to defaults',
            'Back to main menu'
        ]
        
        answer = questionary.select(
            "What would you like to change?",
            choices=choices,
            style=custom_style,
            use_indicator=True,
            instruction="(Use arrow keys)"
        ).ask()
        
        if not answer or 'Back to main menu' in answer:
            break
        
        if 'Default Quality' in answer:
            new_quality = prompt_quality(current_quality)
            # Extract just the number for saving
            quality_num = new_quality.replace('p', '').split()[0].strip()
            config.set_last_quality(quality_num)
            changes['quality'] = new_quality
            console.print(f"[green]✓ Default quality changed to {new_quality}[/green]")
        
        elif 'Download Directory' in answer:
            new_dir = prompt_download_directory(current_dir, config)
            if new_dir != current_dir:
                config.set_download_dir(new_dir)
                changes['directory'] = new_dir
                console.print(f"[green]✓ Download directory changed[/green]")
        
        elif 'Reset to defaults' in answer:
            if questionary.confirm(
                "Reset all settings to defaults?",
                default=False,
                style=custom_style
            ).ask():
                config.set_last_quality('720')
                default_downloads = str(Path.home() / "Downloads" / "YouTube")
                config.set_download_dir(default_downloads)
                changes['reset'] = True
                console.print("[green]✓ Settings reset to defaults[/green]")
        
        console.print()
    
    return changes
