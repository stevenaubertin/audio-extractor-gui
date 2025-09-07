#!/usr/bin/env python3
"""
Audio Extractor UI - Main Application Entry Point
Integrates with the audio-extractor submodule for core functionality.
"""

import sys
import argparse
from pathlib import Path

# Add src to path for relative imports
sys.path.insert(0, str(Path(__file__).parent))

# Add audio-extractor submodule to path
project_root = Path(__file__).parent.parent
audio_extractor_path = project_root / "audio-extractor" / "src"
if audio_extractor_path.exists():
    sys.path.insert(0, str(audio_extractor_path))

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
    
    parser.add_argument(
        "--core-cli",
        action="store_true",
        help="Launch the core audio-extractor CLI directly"
    )
    
    return parser


def main():
    """Main application entry point."""
    parser = create_parser()
    
    # Special handling for --core-cli to pass remaining args to core
    if "--core-cli" in sys.argv:
        # Remove --core-cli and pass the rest to the core CLI
        core_args = [arg for arg in sys.argv[1:] if arg != "--core-cli"]
        
        try:
            import extract_audio
            # Set up sys.argv for the core CLI
            original_argv = sys.argv
            sys.argv = ["extract_audio.py"] + core_args
            
            if not core_args:
                # If no arguments provided, show the core CLI help
                sys.argv.append("--help")
            
            # Call the core CLI click function
            extract_audio.cli()
            return 0
            
        except ImportError:
            print("❌ Error: Could not import audio-extractor module.")
            print("💡 Make sure the audio-extractor submodule is properly initialized:")
            print("   git submodule update --init --recursive")
            return 1
        except SystemExit as e:
            # The core CLI called sys.exit(), so we respect that
            return e.code if e.code is not None else 0
        finally:
            # Restore original sys.argv
            sys.argv = original_argv
    
    # Normal argument parsing for UI options
    args = parser.parse_args()
    
    if args.cli:
        try:
            from audio_extractor_ui.cli import run_cli
            run_cli(args)
        except ImportError as e:
            print(f"❌ CLI dependencies not available: {e}")
            sys.exit(1)
    else:
        # Default to GUI if no interface is specified
        try:
            from audio_extractor_ui.gui import run_gui
            print(f"🚀 Starting Audio Extractor UI v{__version__}")
            print("💡 Integrated with audio-extractor core functionality")
            print(f"📁 Core CLI available via: python src/main.py --core-cli")
            run_gui()
        except ImportError as e:
            print(f"❌ GUI dependencies not available: {e}")
            print("💡 Try installing with: pip install -r requirements.txt")
            sys.exit(1)


if __name__ == "__main__":
    main()
