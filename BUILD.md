# Build Documentation

This document explains how to build the Audio Extractor UI for different distribution formats.

## 🎯 Build Options Available

### 1. Python Package Distribution (`python -m build`)
Creates Python packages that can be installed via pip:

```bash
# Create wheel and source distribution
python -m build

# Output files:
# - dist/audio_extractor_ui-0.1.0-py3-none-any.whl
# - dist/audio_extractor_ui-0.1.0.tar.gz
```

**Use case**: For Python developers who want to install via pip
**Requirements**: Target system must have Python and dependencies installed

### 2. Windows Executable (PyInstaller)
Creates standalone executable for Windows users:

```bash
# Method 1: Use Python build script
python build_exe.py

# Method 2: Use PowerShell script (Windows)
.\build_exe.ps1

# Method 3: Manual PyInstaller command
pyinstaller --clean audio_extractor_ui.spec
```

**Use case**: For end users who don't have Python installed
**Requirements**: Only FFmpeg needs to be installed on target system

---

## 🛠️ Setting Up Build Environment

### Prerequisites
```bash
# Install build dependencies
pip install build pyinstaller

# Ensure FFmpeg is available
ffmpeg -version
```

### Virtual Environment (Recommended)
```bash
# Windows PowerShell
.\activate.ps1

# Windows CMD
activate.bat

# macOS/Linux
source activate.sh
```

---

## 📦 Python Package Build

### Basic Package Build
```bash
python -m build
```

### Advanced Package Options
```bash
# Build only wheel
python -m build --wheel

# Build only source distribution
python -m build --sdist

# Build with verbose output
python -m build --verbose
```

### Installing the Package
```bash
# Install from wheel
pip install dist/audio_extractor_ui-0.1.0-py3-none-any.whl

# Install in development mode
pip install -e .

# Install with extras
pip install -e .[dev]
```

---

## 🖥️ Windows Executable Build

### Method 1: Automated Python Script
```bash
python build_exe.py
```

**Features:**
- ✅ Dependency checking
- ✅ Automatic cleanup
- ✅ Release package creation
- ✅ Cross-platform (Python)

### Method 2: PowerShell Script (Windows)
```powershell
# Basic build
.\build_exe.ps1

# Build with options
.\build_exe.ps1 -Clean -OutputDir "my_release"
.\build_exe.ps1 -BuildOnly  # Skip release package creation
```

**Features:**
- ✅ Native PowerShell integration
- ✅ Colored output
- ✅ Advanced parameter support
- ✅ Build information tracking

### Method 3: Manual PyInstaller
```bash
# Using spec file (recommended)
pyinstaller --clean audio_extractor_ui.spec

# Direct command
pyinstaller --onefile --windowed --name AudioExtractorUI src/main.py
```

### Build Configuration

#### PyInstaller Spec File (`audio_extractor_ui.spec`)
The spec file provides fine-grained control over the build process:

- **Hidden Imports**: Ensures all required modules are included
- **Data Files**: Bundles the audio-extractor submodule
- **Exclusions**: Removes unnecessary packages to reduce size
- **Console/Windowed**: Controls whether a console window appears

#### Key Settings:
```python
# Console vs Windowed
console=False  # No console window (GUI only)
console=True   # Show console window (for debugging)

# Single file vs Directory
# Current: Single executable file (~22 MB)
# Alternative: Directory distribution (faster startup)
```

---

## 🎭 Build Outputs

### Python Package
```
dist/
├── audio_extractor_ui-0.1.0-py3-none-any.whl    # Wheel package
└── audio_extractor_ui-0.1.0.tar.gz               # Source distribution
```

### Windows Executable
```
release/
├── AudioExtractorUI.exe    # Main executable (~22 MB)
├── README.md              # Project documentation
├── LICENSE                # License file
└── USAGE.txt             # User instructions
```

---

## 🧪 Testing Builds

### Testing Python Package
```bash
# Test installation
pip install dist/audio_extractor_ui-0.1.0-py3-none-any.whl

# Test entry point
audio-extractor-ui --help
audio-extractor-ui --version

# Test uninstallation
pip uninstall audio-extractor-ui
```

### Testing Windows Executable
```bash
cd release

# Test command line options
.\AudioExtractorUI.exe --help
.\AudioExtractorUI.exe --version
.\AudioExtractorUI.exe --cli

# Test GUI (should open without errors)
.\AudioExtractorUI.exe
```

---

## 🚀 Distribution

### Python Package Distribution
```bash
# Upload to PyPI (requires account and twine)
pip install twine
twine upload dist/*

# Upload to Test PyPI first
twine upload --repository testpypi dist/*
```

### Windows Executable Distribution
```bash
# Create installer (optional - requires NSIS or similar)
# Or simply distribute the release/ directory

# Create ZIP for distribution
Compress-Archive -Path release/* -DestinationPath AudioExtractorUI-v0.1.0-Windows.zip
```

---

## 🐛 Troubleshooting

### Common Issues

#### PyInstaller Build Fails
```bash
# Clear cache and rebuild
pyinstaller --clean --noconfirm audio_extractor_ui.spec

# Check for missing modules
python -c "import audio_extractor_ui.gui"  # Should not error
```

#### Large Executable Size
- Current size: ~22 MB (acceptable for bundled application)
- To reduce: Add more exclusions to spec file
- Alternative: Use directory distribution instead of single file

#### Missing Dependencies at Runtime
- Add missing modules to `hiddenimports` in spec file
- Ensure all data files are included in `datas`

#### GUI Doesn't Start
- Check if tkinter is available: `python -c "import tkinter"`
- Ensure `console=False` in spec file for windowed mode
- Test with `console=True` for debugging

### Debug Mode
```bash
# Build with console window for debugging
# Edit audio_extractor_ui.spec: console=True
pyinstaller --clean audio_extractor_ui.spec
```

---

## 📋 Build Checklist

Before releasing:

- [ ] All tests pass (`pytest`)
- [ ] Package builds without errors (`python -m build`)
- [ ] Executable builds without errors (`python build_exe.py`)
- [ ] Entry points work correctly
- [ ] GUI launches and functions properly
- [ ] Core functionality works (audio extraction)
- [ ] FFmpeg dependency is documented
- [ ] Version numbers are updated
- [ ] Documentation is current

---

## 🔄 Continuous Integration

For automated builds, consider setting up:

### GitHub Actions Example
```yaml
name: Build Release
on:
  release:
    types: [created]

jobs:
  build-windows:
    runs-on: windows-latest
    steps:
      - uses: actions/checkout@v3
        with:
          submodules: recursive
      
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install build pyinstaller
      
      - name: Build packages
        run: |
          python -m build
          python build_exe.py
      
      - name: Upload artifacts
        uses: actions/upload-artifact@v3
        with:
          name: release-files
          path: |
            dist/
            release/
```

This would automatically build both Python packages and Windows executables when a release is created on GitHub.
