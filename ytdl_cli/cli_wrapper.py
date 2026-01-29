"""Wrapper for CLI to catch and display errors in executable."""

import sys
import traceback
from ytdl_cli.cli import main

def wrapped_main():
    """Wrapper that catches errors and keeps console open."""
    try:
        exit_code = main()
        sys.exit(exit_code)
    except Exception as e:
        print("\n" + "="*60)
        print("ERROR: An unexpected error occurred")
        print("="*60)
        print(f"\n{e}\n")
        traceback.print_exc()
        print("\n" + "="*60)
        input("\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    wrapped_main()
