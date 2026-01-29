# YouTube Downloader CLI ⬇️

A beautiful, feature-rich command-line tool for downloading YouTube videos and playlists with an intuitive arrow-key interface.

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

## 📥 Download

**[⬇️ Download ytdl-start.exe (Latest Release)](https://github.com/ncjpr04/yt-playlist-video-downloader-CLI/releases/latest)**

> No installation required! Just download and run.
> 
> **Recommended:** Install [FFmpeg](https://ffmpeg.org/download.html) for 720p+ quality support.

## ✨ Features

- 🎯 **8 Quality Options** - From 144p to 4K (2160p)
- ⌨️ **Arrow Key Navigation** - Modern, interactive UI using `questionary`
- � **Smart Folder Selection** - Default, Previous, or Custom directory
- 🎨 **Beautiful Interface** - Rich colors, panels, and progress bars
- � **Main Menu System** - Easy navigation between downloads and settings
- ⚙️ **Settings Menu** - Save default quality and download directory
- � **Unlimited Re-downloads** - Download same video in different qualities
- � **Playlist Support** - Custom folder names and selective video downloads
- ⚡ **Resume Downloads** - Partial downloads continue automatically
- ⚠️ **FFmpeg Detection** - Warns when FFmpeg is needed for high-quality merging

## 📦 Installation

### Prerequisites

- **Python 3.8+**
- **FFmpeg** (recommended for 720p+ quality)

### Install FFmpeg (Optional but Recommended)

```powershell
# Using Chocolatey
choco install ffmpeg

# Using Scoop
scoop install ffmpeg
```

Without FFmpeg, high-quality videos (720p+) will download as separate video and audio files.

### Install YouTube Downloader

```bash
# Clone the repository
git clone https://github.com/ncjpr04/yt-playlist-video-downloader-CLI.git
cd yt-playlist-video-downloader-CLI

# Install dependencies
pip install -r requirements.txt

# Run the tool
python -m ytdl_cli.cli
```

### Build Executable (Optional)

```bash
# Build Windows executable
python build.py

# Run the executable
.\dist\ytdl-start.exe
```

## 🚀 Quick Start

1. **Launch the tool**
   ```bash
   python -m ytdl_cli.cli
   # or
   .\dist\ytdl-start.exe
   ```

2. **Select "Download video/playlist"** using arrow keys

3. **Paste YouTube URL** when prompted

4. **Choose download directory**:
   - Default: `~/Downloads/YouTube`
   - Previous: Last used custom folder
   - Custom: Enter any path

5. **Select quality** (144p to 4K) with arrow keys

6. **For playlists**:
   - Choose folder name (YouTube name or custom)
   - Select all videos or specific ones

7. **Confirm and download!**

## 📖 Usage Examples

### Download Single Video

```
? What would you like to do? Download video/playlist
? Paste YouTube URL: https://www.youtube.com/watch?v=...

? Download directory: Default (C:\Users\...\Downloads\YouTube)
? Select video quality: 1080p (FHD)

✓ Download complete!
```

### Download Playlist

```
? What would you like to do? Download video/playlist
? Paste YouTube URL: https://www.youtube.com/playlist?list=...

Playlist: Python Tutorial Series
Total videos: 50

? Playlist folder name: Use playlist name (Python Tutorial Series)
? Which videos do you want to download? Select specific videos
? Enter your selection: 1-10,15,20-25

? Select video quality: 720p (HD)

✓ Successfully downloaded 16 video(s)
```

### Change Default Settings

```
? What would you like to do? Change settings

? What would you like to change?
 » Default Quality: 720p (HD)
   Download Directory: C:\Users\...\Downloads\YouTube
   Reset to defaults
   Back to main menu

? Select video quality: 1080p (FHD)
✓ Default quality changed to 1080p (FHD)
```

## 🎨 Quality Options

| Quality | Resolution | Label | FFmpeg Needed |
|---------|------------|-------|---------------|
| 2160p | 4K UHD | 4K | Yes |
| 1440p | 2K QHD | 2K | Yes |
| 1080p | Full HD | FHD | Yes |
| 720p | HD | HD | Yes |
| 480p | Standard | SD | No |
| 360p | Low | - | No |
| 240p | Very Low | - | No |
| 144p | Minimal | - | No |

## 📁 Output Structure

### Single Videos
```
~/Downloads/YouTube/
└── Video Title.mp4
```

### Playlists
```
~/Downloads/YouTube/
└── Playlist Name/
    ├── 01_Video Title.mp4
    ├── 02_Video Title.mp4
    └── 03_Video Title.mp4
```

## ⚙️ Configuration

Settings are stored in: `~/.ytdl_cli/config.json`

**Default values:**
- Quality: `720p`
- Download Directory: `~/Downloads/YouTube`

**Customize via:**
1. Settings menu in the application
2. Manual edit of `config.json`

## 🛠️ Tech Stack

- **[yt-dlp](https://github.com/yt-dlp/yt-dlp)** - YouTube download engine
- **[Rich](https://github.com/Textualize/rich)** - Beautiful terminal output
- **[Questionary](https://github.com/tmbo/questionary)** - Interactive prompts
- **[PyInstaller](https://www.pyinstaller.org/)** - Executable creation

## 🔧 Development

### Project Structure

```
yt-cli/
├── ytdl_cli/
│   ├── __init__.py          # Package metadata
│   ├── cli.py               # Main entry point & workflow
│   ├── cli_wrapper.py       # Error handling wrapper
│   ├── prompts.py           # Interactive UI prompts
│   ├── downloader.py        # yt-dlp integration
│   ├── state.py             # Configuration management
│   └── utils.py             # Helper functions
├── build.py                 # PyInstaller build script
├── requirements.txt         # Python dependencies
├── setup.py                 # Package setup
└── README.md               # This file
```

### Build from Source

```bash
# Install development dependencies
pip install -r requirements.txt

# Run tests (if you have them)
pytest

# Build executable
python build.py

# Output: dist/ytdl-start.exe (37.7 MB)
```

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## ⚠️ Disclaimer

This tool is for personal use only. Please respect YouTube's Terms of Service and only download content you have the right to download.

## 🙏 Credits

- **yt-dlp team** - Powerful YouTube download engine
- **Rich library** - Beautiful terminal formatting
- **Questionary** - Interactive CLI framework

## 📞 Support

If you encounter any issues or have questions, please [open an issue](https://github.com/ncjpr04/yt-playlist-video-downloader-CLI/issues) on GitHub.

---

Made with ❤️ by [ncjpr04](https://github.com/ncjpr04)