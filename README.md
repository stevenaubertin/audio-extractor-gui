# Audio Extractor UI

A modern, user-friendly interface for extracting audio from videos using ffmpeg and yt-dlp.

## ✨ Features

- 🎵 **Extract audio from local video files** - Support for all major video formats
- 🌐 **Download audio from URLs** - YouTube, Vimeo, and many other platforms
- 🎛️ **Multiple audio formats** - MP3, WAV, FLAC, AAC support
- 🎚️ **Quality options** - High, medium, and low quality settings
- 🖥️ **Dual interfaces** - Both GUI and CLI available
- 🚀 **Easy setup** - One-command environment activation
- 📦 **Cross-platform** - Windows, macOS, and Linux support

## 🚀 Quick Start

### Prerequisites

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

### Installation

1. **Clone the repository:**
```bash
git clone https://github.com/yourusername/audio-extractor-ui.git
cd audio-extractor-ui
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

### Features Overview

#### File Extraction Tab
- Browse and select local video files
- Choose output format (MP3, WAV, FLAC, AAC)
- Select quality settings
- Progress tracking

#### URL Extraction Tab
- Enter video URLs from supported platforms
- Same format and quality options
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
audio-extractor-ui/
├── src/
│   └── audio_extractor_ui/
│       ├── __init__.py          # Package initialization
│       ├── main.py              # Application entry point
│       ├── core.py              # Core audio extraction logic
│       ├── gui.py               # GUI interface
│       ├── cli.py               # CLI interface
│       └── utils.py             # Utility functions
├── tests/
│   └── test_core.py             # Unit tests
├── docs/                        # Documentation
├── scripts/                     # Development scripts
├── activate.ps1                 # Windows PowerShell activation
├── activate.bat                 # Windows CMD activation
├── activate.sh                  # Unix/Linux activation
├── requirements.txt             # Production dependencies
├── requirements-dev.txt         # Development dependencies
├── pyproject.toml              # Project configuration
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

## 🐛 Issues and Support

- **Bug reports:** [GitHub Issues](https://github.com/yourusername/audio-extractor-ui/issues)
- **Feature requests:** [GitHub Issues](https://github.com/yourusername/audio-extractor-ui/issues)
- **Discussions:** [GitHub Discussions](https://github.com/yourusername/audio-extractor-ui/discussions)

## 📈 Roadmap

- [ ] Time range extraction (start/end times)
- [ ] Batch processing for multiple files
- [ ] Custom output naming patterns
- [ ] Audio metadata preservation
- [ ] Web interface version
- [ ] Plugin system for custom extractors
- [ ] Audio preview functionality
- [ ] Drag and drop file support

---

Made with ❤️ by [Your Name](https://github.com/yourusername)
