#!/usr/bin/env python3
"""
Demo script to showcase the Audio Extractor UI with output path and filename controls.

This script demonstrates the new features:
- Custom output directory selection
- Custom output filename specification
- Auto-population of filename based on input file
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Run the GUI demo."""
    try:
        from audio_extractor_ui.gui import AudioExtractorGUI
        
        print("🚀 Starting Audio Extractor UI Demo")
        print("✨ New Features:")
        print("  📁 Custom output directory selection")
        print("  📝 Custom output filename specification")
        print("  🔄 Auto-filename population from input file")
        print("  🎛️ Separate controls for both File and URL tabs")
        print()
        print("💡 Instructions:")
        print("  1. Select a video file or enter a URL")
        print("  2. Choose your preferred output directory")
        print("  3. Optionally specify a custom filename")
        print("  4. Select format and quality settings")
        print("  5. Click Extract Audio!")
        print()
        print("📝 Notes:")
        print("  - Output directory defaults to 'output' folder")
        print("  - Filename auto-populates when you select a file")
        print("  - Leave filename empty for automatic naming")
        print("  - Custom filenames are sanitized for filesystem safety")
        print()
        
        # Create and run the GUI
        app = AudioExtractorGUI()
        app.run()
        
    except ImportError as e:
        print(f"❌ Could not start GUI: {e}")
        print("💡 Make sure tkinter is available on your system")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
