#!/usr/bin/env python3
"""
Audio Extractor UI - Main Application Entry Point
"""

import sys
import argparse
from pathlib import Path

# Add src to path for relative imports
sys.path.insert(0, str(Path(__file__).parent))

from audio_extractor_ui import __version__


def create_parser():
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Audio Extractor UI - A user interface for extracting audio from videos",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    parser.add_argument(
        "--version", 
        action="version", 
        version=f"%(prog)s {__version__}"
    )
    
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the graphical user interface (default)"
    )
    
    parser.add_argument(
        "--cli",
        action="store_true", 
        help="Use command line interface"
    )
    
    return parser


def main():
    """Main application entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Default to GUI if no interface is specified
    if not args.cli:
        try:
            from audio_extractor_ui.gui import run_gui
            print(f"🚀 Starting Audio Extractor UI v{__version__}")
            run_gui()
        except ImportError as e:
            print(f"❌ GUI dependencies not available: {e}")
            print("💡 Try installing with: pip install -r requirements.txt")
            sys.exit(1)
    else:
        try:
            from audio_extractor_ui.cli import run_cli
            run_cli(args)
        except ImportError as e:
            print(f"❌ CLI dependencies not available: {e}")
            sys.exit(1)


if __name__ == "__main__":
    main()
