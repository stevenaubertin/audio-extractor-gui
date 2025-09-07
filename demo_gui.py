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
        print("  📁 Unified output path control (directory + filename)")
        print("  💾 Save-as dialog for easy file selection")
        print("  🔄 Auto-path suggestion from input file")
        print("  🎛️ Consistent controls for both File and URL tabs")
        print()
        print("💡 Instructions:")
        print("  1. Select a video file or enter a URL")
        print("  2. Optionally specify output path (or leave empty for auto)")
        print("  3. Use 'Browse' for save-as dialog with file type filters")
        print("  4. Select format and quality settings")
        print("  5. Click Extract Audio!")
        print()
        print("📝 Notes:")
        print("  - Leave output path empty for automatic: output/filename.ext")
        print("  - Path auto-populates when you select a video file")
        print("  - Browse button opens save-as dialog with format filters")
        print("  - Automatic extension correction based on selected format")
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
