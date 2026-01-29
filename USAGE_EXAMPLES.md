# YouTube Downloader CLI - Usage Examples

Quick reference guide for using the YouTube Downloader CLI tool.

## Basic Usage

### Single Video Download

```powershell
# Run the tool
ytdl-start

# Paste URL when prompted:
https://www.youtube.com/watch?v=dQw4w9WgXcQ

# Choose download directory (default or custom)
# Select quality (720p/480p/360p)
# Confirm download

# Result:
# E:/Lectures/Video Title.mp4 (or your custom directory)
```

### Playlist Download - All Videos

```powershell
ytdl-start

# Paste playlist URL:
https://www.youtube.com/playlist?list=PLrAXtmErZgOeiKm4sgNOknGvNjby9efdf

# When prompted for selection, type:
all

# Select quality
# Tool downloads all videos numbered:
# E:/Lectures/Playlist Name/01_Video1.mp4
# E:/Lectures/Playlist Name/02_Video2.mp4
# etc.
```

### Playlist Download - Specific Range

```powershell
ytdl-start

# Paste playlist URL
# When prompted for selection, type:
1-10

# Downloads videos 1 through 10
```

### Playlist Download - Specific Videos

```powershell
ytdl-start

# Paste playlist URL
# When prompted for selection, type:
1,5,7,15

# Downloads only videos 1, 5, 7, and 15
```

### Playlist Download - Combined Selection

```powershell
ytdl-start

# Paste playlist URL
# When prompted for selection, type:
1-5,10,15-20

# Downloads:
# - Videos 1 through 5
# - Video 10
# - Videos 15 through 20
```

## Advanced Usage

### Resume Interrupted Download

If a download is interrupted (network issue, Ctrl+C, etc.):

```powershell
# Simply run the tool again with the same URL
ytdl-start

# Paste the same URL
# Tool will automatically resume partial downloads
# and skip completed videos
```

### Change Download Quality

```powershell
# Run normally
ytdl-start

# Select different quality (e.g., 480p instead of 720p)
# Tool remembers this preference for next time
```

### Check Configuration

Your configuration is stored at:
```
C:\Users\<YourName>\.ytdl_cli\config.json
```

Example config:
```json
{
  "last_quality": "720",
  "download_dir": "E:/Lectures"
}
```

You can manually edit this file to:
- Change default quality
- Change download directory

### Run Without Installing

If you haven't installed the package:

```powershell
# Navigate to project directory
cd P:\yt-cli

# Run directly
python -m ytdl_cli.cli
```

## Common Scenarios

### Downloading a Course Playlist

```powershell
ytdl-start

# Paste course playlist URL
# Select "all" to download entire course
# Choose 720p for high quality
# Videos download with lecture numbers: 01_, 02_, etc.
```

### Downloading Select Lectures

```powershell
ytdl-start

# Paste playlist URL
# View the numbered list of videos
# Select specific lectures: 1,3,5,7-12
# Downloads only those lectures
```

### Network Interruption Recovery

```powershell
# If download fails or is interrupted:

# 1. Check your internet connection
# 2. Run ytdl-start again
# 3. Paste the same URL
# 4. Tool resumes automatically
# 5. Already completed videos are skipped
```

## Keyboard Shortcuts

- **Ctrl+C**: Cancel current operation
- **Up/Down arrows**: Navigate quality selection menu
- **Enter**: Confirm selection

## Output Structure

### Single Video
```
E:/Lectures/
└── Video Title.mp4
```

### Playlist
```
E:/Lectures/
└── Playlist Name/
    ├── downloads.archive    # Tracks completed downloads
    ├── 01_First Video.mp4
    ├── 02_Second Video.mp4
    └── 03_Third Video.mp4
```

## Troubleshooting

### "Invalid YouTube URL" error
- Ensure URL contains "youtube.com" or "youtu.be"
- Check URL is copied completely

### Download is slow
- This is often YouTube throttling
- Tool already uses parallel fragment downloads
- Consider downloading during off-peak hours

### "Quality not available" (implicit fallback)
- Tool automatically selects best available quality
- Some videos don't have all quality options
- Check downloaded video to confirm quality

### Permission errors
- Ensure E:/Lectures exists and is writable
- Or edit config to use different directory

## Tips & Best Practices

1. **For courses**: Always use "all" to maintain numbering
2. **For large playlists**: Consider downloading in batches using ranges
3. **For archiving**: Use 720p for quality/size balance
4. **For mobile**: Use 480p or 360p for smaller files
5. **Regular use**: Tool remembers your quality preference

## Building Executable

To create a standalone .exe:

```powershell
# Install PyInstaller (if needed)
pip install pyinstaller

# Run build script
python build.py

# Find executable at:
# dist/ytdl-start.exe

# Copy and run anywhere on Windows!
```

---

**For more information**: See [README.md](file:///P:/yt-cli/README.md)
