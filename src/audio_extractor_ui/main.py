#!/usr/bin/env python3
"""
Main entry point for the Audio Extractor UI package.
"""

import sys
import argparse
from pathlib import Path

# Add the audio-extractor submodule to the path
current_dir = Path(__file__).parent
project_root = current_dir.parent.parent
audio_extractor_path = project_root / "audio-extractor" / "src"

if audio_extractor_path.exists():
    sys.path.insert(0, str(audio_extractor_path))

from .core import AudioExtractor
from .cli import run_cli as cli_main

try:
    from .gui import AudioExtractorGUI
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False


def main():
    """Main entry point for the application."""
    parser = argparse.ArgumentParser(
        description="Audio Extractor UI - Extract audio from videos"
    )
    parser.add_argument(
        "--mode",
        choices=["gui", "cli", "core-cli"],
        default="gui",
        help="Interface mode (default: gui)"
    )
    parser.add_argument(
        "--gui",
        action="store_const",
        const="gui",
        dest="mode",
        help="Launch GUI interface (default)"
    )
    parser.add_argument(
        "--cli",
        action="store_const", 
        const="cli",
        dest="mode",
        help="Use command-line interface"
    )
    parser.add_argument(
        "--core-cli",
        action="store_const",
        const="core-cli",
        dest="mode",
        help="Use core CLI directly"
    )
    parser.add_argument(
        "--version",
        action="version",
        version="audio-extractor-ui 0.1.0"
    )

    # Parse known args to allow core CLI args to pass through
    args, remaining = parser.parse_known_args()

    if args.mode == "gui":
        if not GUI_AVAILABLE:
            print("Error: GUI not available. Please install tkinter or use --cli mode.")
            sys.exit(1)
        
        app = AudioExtractorGUI()
        app.run()
    
    elif args.mode == "cli":
        # Use our CLI interface
        cli_main(remaining)
    
    elif args.mode == "core-cli":
        # Import and run the core CLI directly
        try:
            from extract_audio import cli
            # Restore the remaining args to sys.argv for core CLI
            sys.argv = ["extract_audio"] + remaining
            cli()
        except ImportError:
            print("Error: Core audio extractor not available.")
            print("Please ensure the audio-extractor submodule is properly initialized.")
            sys.exit(1)
    
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
