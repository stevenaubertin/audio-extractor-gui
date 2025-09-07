#!/usr/bin/env python3
"""
Build script for creating Windows executable using PyInstaller
"""

import os
import sys
import shutil
import subprocess
from pathlib import Path

def clean_build():
    """Clean previous build artifacts"""
    print("🧹 Cleaning previous build artifacts...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"   Removed: {dir_name}")
    
    # Clean .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                os.remove(os.path.join(root, file))

def check_dependencies():
    """Check if all required tools are installed"""
    print("🔍 Checking dependencies...")
    
    try:
        import PyInstaller
        print(f"   ✅ PyInstaller: {PyInstaller.__version__}")
    except ImportError:
        print("   ❌ PyInstaller not found. Install with: pip install pyinstaller")
        return False
    
    # Check if FFmpeg is available
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("   ✅ FFmpeg: Available")
        else:
            print("   ⚠️  FFmpeg: Check failed (may still work)")
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("   ⚠️  FFmpeg: Not found in PATH (required for audio extraction)")
    
    return True

def build_executable():
    """Build the executable using PyInstaller"""
    print("🔨 Building Windows executable...")
    
    # Use the spec file for better control
    spec_file = "audio_extractor_ui.spec"
    
    if os.path.exists(spec_file):
        print(f"   Using spec file: {spec_file}")
        cmd = ["pyinstaller", "--clean", spec_file]
    else:
        print("   Using direct command (no spec file found)")
        cmd = [
            "pyinstaller",
            "--onefile",
            "--windowed", 
            "--name", "AudioExtractorUI",
            "--add-data", "audio-extractor/src;audio-extractor/src",
            "--hidden-import", "audio_extractor_ui.gui",
            "--hidden-import", "audio_extractor_ui.core", 
            "--hidden-import", "tkinter",
            "--hidden-import", "tkinter.ttk",
            "--hidden-import", "yt_dlp",
            "src/main.py"
        ]
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("   ✅ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"   ❌ Build failed: {e}")
        print(f"   Error output: {e.stderr}")
        return False

def create_release_package():
    """Create a release package with the executable and necessary files"""
    print("📦 Creating release package...")
    
    release_dir = Path("release")
    if release_dir.exists():
        shutil.rmtree(release_dir)
    
    release_dir.mkdir()
    
    # Copy executable
    exe_path = Path("dist/AudioExtractorUI.exe")
    if exe_path.exists():
        shutil.copy2(exe_path, release_dir / "AudioExtractorUI.exe")
        print(f"   ✅ Copied: {exe_path}")
    else:
        print(f"   ❌ Executable not found: {exe_path}")
        return False
    
    # Copy documentation
    files_to_copy = ["README.md", "LICENSE"]
    for file_name in files_to_copy:
        if os.path.exists(file_name):
            shutil.copy2(file_name, release_dir / file_name)
            print(f"   ✅ Copied: {file_name}")
    
    # Create usage instructions
    usage_text = """# Audio Extractor UI - Windows Release

## Usage:
1. Double-click AudioExtractorUI.exe to launch the graphical interface
2. Or run from command line with options:
   - AudioExtractorUI.exe --help (show help)
   - AudioExtractorUI.exe --gui (default GUI mode)
   - AudioExtractorUI.exe --cli (command line interface)

## Requirements:
- FFmpeg must be installed and available in PATH for audio extraction
- Download FFmpeg from: https://ffmpeg.org/download.html

## Features:
- Extract audio from local video files
- Download and extract audio from URLs (YouTube, etc.)
- Support for MP3, WAV, FLAC, AAC formats
- Time range extraction with millisecond precision
- Custom output paths and filenames

## Support:
- GitHub: https://github.com/stevenaubertin/audio-extractor-gui
"""
    
    with open(release_dir / "USAGE.txt", "w") as f:
        f.write(usage_text)
    print(f"   ✅ Created: USAGE.txt")
    
    print(f"\n🎉 Release package created in: {release_dir}")
    return True

def main():
    """Main build process"""
    print("🚀 Audio Extractor UI - Windows Build Script")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not os.path.exists("src/main.py"):
        print("❌ Error: src/main.py not found. Run this script from the project root.")
        sys.exit(1)
    
    # Step 1: Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Step 2: Clean previous builds
    clean_build()
    
    # Step 3: Build executable
    if not build_executable():
        sys.exit(1)
    
    # Step 4: Create release package
    if not create_release_package():
        sys.exit(1)
    
    print("\n✅ Build process completed successfully!")
    print("\n📋 Next steps:")
    print("   1. Test the executable in the 'release' directory")
    print("   2. Ensure FFmpeg is installed on target systems")
    print("   3. Distribute the 'release' directory or create an installer")

if __name__ == "__main__":
    main()
