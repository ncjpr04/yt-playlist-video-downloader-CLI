"""Final build script without inquirer dependency."""

import PyInstaller.__main__
import os
import sys

# Get the absolute path to the project directory
project_dir = os.path.dirname(os.path.abspath(__file__))
wrapper_path = os.path.join(project_dir, 'ytdl_cli', 'cli_wrapper.py')

print("Building ytdl-start.exe (Final Version)...")
print(f"Project directory: {project_dir}")
print()

try:
    PyInstaller.__main__.run([
        wrapper_path,
        '--name=ytdl-start',
        '--onefile',
        '--console',
        '--clean',
        '--noconfirm',
        '--noupx',
        # Include all package files
        '--hidden-import=ytdl_cli',
        '--hidden-import=ytdl_cli.cli',
        '--hidden-import=ytdl_cli.state',
        '--hidden-import=ytdl_cli.utils',
        '--hidden-import=ytdl_cli.prompts',
        '--hidden-import=ytdl_cli.downloader',
        '--hidden-import=rich',
        '--hidden-import=rich.console',
        '--hidden-import=rich.progress',
        '--hidden-import=rich.table',
        '--hidden-import=rich.prompt',
        '--hidden-import=rich.panel',
        '--hidden-import=rich.align',
        '--hidden-import=yt_dlp',
        '--hidden-import=questionary',
        '--hidden-import=prompt_toolkit',
        # Collect all data files
        '--collect-all=rich',
        '--collect-all=yt_dlp',
        '--collect-all=questionary',
        # Add paths
        f'--paths={project_dir}',
    ])
    
    print("\n" + "="*60)
    print("✓ Build complete!")
    print("="*60)
    exe_path = os.path.join(project_dir, 'dist', 'ytdl-start.exe')
    if os.path.exists(exe_path):
        print(f"\nExecutable: {exe_path}")
        print(f"Size: {os.path.getsize(exe_path) / (1024*1024):.1f} MB")
    print("\nTest it:")
    print("  cd dist")
    print("  .\\ytdl-start.exe")
    print("="*60)
    
except Exception as e:
    print(f"\n✗ Build failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
