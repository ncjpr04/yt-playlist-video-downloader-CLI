# Custom Download Directory Feature

## Enhancement Overview

Added the ability for users to specify a custom download directory instead of being limited to the default `E:/Lectures` location.

## Implementation

### 1. New Prompt Function
**File:** `ytdl_cli/prompts.py`

Added `prompt_download_directory()` function that:
- Shows the current default directory
- Offers choice between default or custom directory
- Validates and creates custom directory if specified
- Handles errors gracefully with retry logic

### 2. State Management
**File:** `ytdl_cli/state.py`

Added `set_download_dir()` method to:
- Update download directory in config file
- Persist the selection for future sessions

### 3. CLI Integration
**File:** `ytdl_cli/cli.py`

Integrated directory selection into the workflow:
- Prompts user after URL validation
- Updates configuration if directory changes
- Updates downloader instance with new directory

## User Experience

When running `ytdl-start`, users now see:

```
Paste YouTube URL: [URL]

Download Directory:
Current default: E:/Lectures

[?] Choose download location:
 > Use default directory
   Specify custom directory
```

If "Specify custom directory" is selected:
```
Enter download path: D:/My Videos
✓ Will download to: D:\My Videos
```

## Benefits

✅ Flexibility - Download to any location
✅ Persistence - Directory choice is remembered
✅ Validation - Ensures paths are valid and creates directories
✅ Fallback - Easy return to default if custom path fails
✅ Cross-platform - Works with Windows, Linux, and Mac paths

## Usage Examples

### Use Default Directory
1. Run `ytdl-start`
2. Select "Use default directory"
3. Videos download to `E:/Lectures`

### Specify Custom Directory
1. Run `ytdl-start`
2. Select "Specify custom directory"
3. Enter path: `D:/YouTube/Courses`
4. Videos download to `D:/YouTube/Courses`

### Persistent Selection
Once you set a custom directory, it becomes the new default for future runs.

## Testing

Tested scenarios:
- Default directory selection
- Custom directory with valid path
- Custom directory with invalid path (error handling)
- Empty input (defaults to current default)
- Directory creation for non-existent paths
- Path persistence across sessions
