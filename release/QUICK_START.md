# 🚀 Quick Start Guide - AudioExtractorUI

## For End Users (Windows)

### Step 1: Install FFmpeg (Required)
AudioExtractorUI needs FFmpeg to extract audio. Choose your preferred method:

#### 🟢 **Option A: Automated Installation (Easiest)**
1. Double-click `install_ffmpeg.bat` 
2. Choose option 1 (System) or 2 (Portable)
3. Follow the prompts

#### 🟡 **Option B: Package Managers**
If you have these installed:
```bash
# Chocolatey
choco install ffmpeg

# Scoop
scoop install ffmpeg

# Winget
winget install Gyan.FFmpeg
```

#### 🔴 **Option C: Manual Installation**
1. Go to [ffmpeg.org/download.html](https://ffmpeg.org/download.html)
2. Download "Windows builds"
3. Extract and add to system PATH

### Step 2: Run AudioExtractorUI
1. Double-click `AudioExtractorUI.exe`
2. The GUI will open automatically

### Step 3: Extract Audio
1. **For local files**: Use "File Extraction" tab, browse for video
2. **For YouTube/URLs**: Use "URL Extraction" tab, paste URL
3. Choose format (MP3, WAV, FLAC, AAC) and quality
4. Set time range if needed (with millisecond precision!)
5. Click "Extract Audio"

---

## For Developers (Python Package)

### Installation
```bash
pip install audio_extractor_ui-0.1.0-py3-none-any.whl
```

### Usage
```bash
# Launch GUI
audio-extractor-ui

# Command line options
audio-extractor-ui --cli
audio-extractor-ui --core-cli --format mp3 local "video.mp4"
```

---

## 🎯 Features

- ✅ **Local video files** - Extract from any video format
- ✅ **URL downloads** - YouTube, Vimeo, and more
- ✅ **Multiple formats** - MP3, WAV, FLAC, AAC
- ✅ **Quality options** - High, medium, low
- ✅ **Time ranges** - Extract specific segments
- ✅ **Millisecond precision** - Precise timing (e.g., 1:23.456)
- ✅ **Custom output paths** - Choose where to save
- ✅ **Progress tracking** - See extraction progress

---

## 🆘 Troubleshooting

### "FFmpeg not found" error
- Run the FFmpeg installation script
- Or ensure ffmpeg.exe is in your PATH

### GUI doesn't open
- Check that you have the full release package
- Try running from command prompt to see error messages

### Audio extraction fails
- Verify the video file is valid
- Check your internet connection for URL downloads
- Ensure you have write permissions to the output directory

### Need help?
- Check the full README.md for detailed documentation
- Visit: https://github.com/stevenaubertin/audio-extractor-gui

---

## 📋 Quick Reference

### Time Format Examples
```
1:30        # 1 minute 30 seconds
90          # 90 seconds
1:23.456    # 1 min 23 sec 456 milliseconds
00:01:30.500 # Same as above, full format
```

### Command Line Usage
```bash
# Show help
AudioExtractorUI.exe --help

# Launch GUI (default)
AudioExtractorUI.exe
AudioExtractorUI.exe --gui

# Use CLI mode
AudioExtractorUI.exe --cli
```

---

**Made with ❤️ by [Steven Aubertin](https://github.com/stevenaubertin)**
