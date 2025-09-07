# Audio Extractor UI

A modern, user-friendly interface for extracting audio from videos using ffmpeg and yt-dlp.

**🔗 Integrated with [audio-extractor](https://github.com/stevenaubertin/audio-extractor)** - Uses the proven core functionality as a git submodule for reliable audio extraction.

## ✨ Features

- 🎵 **Extract audio from local video files** - Support for all major video formats
- 🌐 **Download audio from URLs** - YouTube, Vimeo, and many other platforms
- ⏱️ **Time range extraction** - Extract specific segments with start/end times or duration
- 🎛️ **Multiple audio formats** - MP3, WAV, FLAC, AAC support
- 🎚️ **Quality options** - High, medium, and low quality settings
- 🖥️ **Dual interfaces** - Modern GUI and powerful CLI
- 🔧 **Direct core access** - Use original CLI via `--core-cli` option
- 📁 **Custom output paths** - Specify custom output directories and filenames
- 🚀 **Easy setup** - One-command environment activation
- 📦 **Cross-platform** - Windows, macOS, and Linux support

## 📥 Download

### Ready-to-Use Releases

Get the latest pre-built version for immediate use:

**🖥️ Windows Executable (Recommended for End Users)**
- **[Download v0.1.0](https://github.com/stevenaubertin/audio-extractor-gui/releases/tag/v0.1.0)**
- Single executable file (~22 MB)
- No Python installation required
- Includes FFmpeg installation scripts
- Just download, install FFmpeg, and run!

**🐍 Python Package (For Developers)**
- Install via pip: `pip install audio-extractor-ui`
- Requires Python 3.8+ and dependencies
- Full source code access

### What's Included in Windows Release:
- `AudioExtractorUI.exe` - Main application
- `install_ffmpeg.bat` - Easy FFmpeg installer
- `install_ffmpeg.ps1` - PowerShell installer
- `QUICK_START.md` - User guide
- `README.md` & `LICENSE` - Documentation

---

## 🚀 Quick Start

### For End Users (Windows)

💡 **Want to skip the setup?** Download the [Windows executable](https://github.com/stevenaubertin/audio-extractor-gui/releases/tag/v0.1.0) and follow the `QUICK_START.md` guide!

### For Developers (Source Installation)

#### Prerequisites

- Python 3.8 or higher
- FFmpeg installed and available in PATH

#### Installing FFmpeg

**Windows:**

```powershell
# Using chocolatey
choco install ffmpeg

# Using winget
winget install Gyan.FFmpeg
```

**macOS:**

```bash
brew install ffmpeg
```

**Linux:**

```bash
sudo apt update
sudo apt install ffmpeg
```

#### Installation from Source

1. **Clone the repository with submodules:**

```bash
git clone --recursive https://github.com/stevenaubertin/audio-extractor-gui.git
cd audio-extractor-gui
```

**Or if you already cloned without `--recursive`:**

```bash
git submodule update --init --recursive
```

2. **Activate the environment** (choose your platform):

**Windows PowerShell:**

```powershell
.\activate.ps1
```

**Windows Command Prompt:**

```cmd
activate.bat
```

**macOS/Linux:**

```bash
source activate.sh
```

That's it! The activation script will:

- ✅ Create the virtual environment if it doesn't exist
- ✅ Activate the virtual environment
- ✅ Install all required dependencies
- ✅ Set up the development environment

## 💻 Usage

### GUI Mode (Default)

Launch the graphical interface:

```bash
python src/main.py
```

Or simply:

```bash
python src/main.py --gui
```

### CLI Mode

Use the command-line interface:

```bash
python src/main.py --cli
```

### Core CLI Mode (Direct Access)

Access the original audio-extractor CLI directly:

```bash
python src/main.py --core-cli
```

Example core CLI usage:

```bash
# Extract audio from local file
python src/main.py --core-cli --format mp3 --quality high local "video.mp4"

# Extract with time range
python src/main.py --core-cli --format mp3 local "video.mp4" --start-time 1:30 --duration 2:00

# Download from YouTube
python src/main.py --core-cli --format mp3 url "https://www.youtube.com/watch?v=VIDEO_ID"

# Check dependencies
python src/main.py --core-cli check-dependencies
```

### Features Overview

#### File Extraction Tab

- Browse and select local video files
- Choose output format (MP3, WAV, FLAC, AAC)
- Select quality settings
- Set time range (start time, end time, or duration)
- Custom output path and filename
- Progress tracking

#### URL Extraction Tab

- Enter video URLs from supported platforms
- Same format and quality options
- Time range extraction support
- Custom output path and filename
- Download progress indication

## 🛠️ Development

### Setting Up for Development

1. **Clone and activate** (as shown above)

2. **Install development dependencies:**

```bash
pip install -r requirements-dev.txt
```

3. **Install pre-commit hooks:**

```bash
pre-commit install
```

### Project Structure

```
audio-extractor-gui/
├── src/
│   ├── main.py                  # Application entry point
│   └── audio_extractor_ui/
│       ├── __init__.py          # Package initialization
│       ├── core.py              # Core audio extraction logic
│       ├── integration.py       # Submodule integration layer
│       ├── gui.py               # GUI interface
│       ├── cli.py               # CLI interface
│       └── utils.py             # Utility functions
├── audio-extractor/             # Git submodule
│   ├── src/
│   │   └── extract_audio.py     # Core extraction CLI
│   ├── requirements.txt         # Core dependencies
│   └── README.md                # Core documentation
├── tests/
│   └── test_core.py             # Unit tests
├── .vscode/                     # VSCode configuration
│   ├── settings.json            # Editor settings
│   ├── launch.json              # Debug configurations
│   ├── tasks.json               # Build tasks
│   └── extensions.json          # Recommended extensions
├── docs/                        # Documentation
├── scripts/                     # Development scripts
├── activate.ps1                 # Windows PowerShell activation
├── activate.bat                 # Windows CMD activation
├── activate.sh                  # Unix/Linux activation
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── pyproject.toml              # Project configuration
├── .gitmodules                  # Git submodule configuration
└── README.md                   # This file
```

### Development Commands

**Run tests:**

```bash
pytest
```

**Run tests with coverage:**

```bash
pytest --cov=src --cov-report=html
```

**Format code:**

```bash
black src tests
```

**Sort imports:**

```bash
isort src tests
```

**Lint code:**

```bash
flake8 src tests
```

**Type checking:**

```bash
mypy src
```

**Run all quality checks:**

```bash
pre-commit run --all-files
```

### Virtual Environment Management

The project includes convenient activation scripts for all platforms:

**Activate environment:**

- Windows PowerShell: `.\activate.ps1`
- Windows CMD: `activate.bat`
- macOS/Linux: `source activate.sh`

**Deactivate environment:**

```bash
deactivate
```

**Recreate environment:**

```bash
# Remove existing environment
rm -rf venv

# Run activation script (will create new environment)
.\activate.ps1  # Windows
# or
source activate.sh  # macOS/Linux
```

## 🧪 Testing

The project uses pytest for testing:

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/test_core.py

# Run with verbose output
pytest -v

# Run and watch for changes
pytest --looponfail
```

## 📦 Building and Distribution

**Build the package:**

```bash
python -m build
```

**Install in development mode:**

```bash
pip install -e .
```

**Install with optional dependencies:**

```bash
pip install -e .[dev]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and quality checks
5. Commit your changes (`git commit -m 'Add some amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Code Quality

This project uses several tools to maintain code quality:

- **Black** - Code formatting
- **isort** - Import sorting
- **flake8** - Linting
- **mypy** - Type checking
- **pytest** - Testing
- **pre-commit** - Git hooks

All tools are configured in `pyproject.toml`.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - For video downloading capabilities
- [FFmpeg](https://ffmpeg.org/) - For audio/video processing
- [tkinter](https://docs.python.org/3/library/tkinter.html) - For GUI framework
