# Audio Extractor UI - Windows Build Script (PowerShell)
# Run this script to build a Windows executable

param(
    [switch]$Clean = $false,
    [switch]$BuildOnly = $false,
    [string]$OutputDir = "release"
)

Write-Host "🚀 Audio Extractor UI - Windows Build Script" -ForegroundColor Cyan
Write-Host "=" * 50

# Check if we're in the right directory
if (-not (Test-Path "src/main.py")) {
    Write-Host "❌ Error: src/main.py not found. Run this script from the project root." -ForegroundColor Red
    exit 1
}

# Function to check if virtual environment is activated
function Test-VirtualEnvironment {
    if ($env:VIRTUAL_ENV) {
        Write-Host "✅ Virtual environment detected: $env:VIRTUAL_ENV" -ForegroundColor Green
        return $true
    } else {
        Write-Host "⚠️  No virtual environment detected. Consider activating one." -ForegroundColor Yellow
        return $false
    }
}

# Function to clean build artifacts
function Clear-BuildArtifacts {
    Write-Host "🧹 Cleaning previous build artifacts..." -ForegroundColor Yellow
    
    $dirsToClean = @('build', 'dist', '__pycache__', $OutputDir)
    foreach ($dir in $dirsToClean) {
        if (Test-Path $dir) {
            Remove-Item -Recurse -Force $dir
            Write-Host "   Removed: $dir" -ForegroundColor Gray
        }
    }
    
    # Clean .pyc files
    Get-ChildItem -Recurse -Filter "*.pyc" | Remove-Item -Force
}

# Function to check dependencies
function Test-Dependencies {
    Write-Host "🔍 Checking dependencies..." -ForegroundColor Yellow
    
    # Check PyInstaller
    try {
        $pyinstallerVersion = python -c "import PyInstaller; print(PyInstaller.__version__)" 2>$null
        if ($pyinstallerVersion) {
            Write-Host "   ✅ PyInstaller: $pyinstallerVersion" -ForegroundColor Green
        } else {
            Write-Host "   ❌ PyInstaller not found. Install with: pip install pyinstaller" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "   ❌ PyInstaller not found. Install with: pip install pyinstaller" -ForegroundColor Red
        return $false
    }
    
    # Check FFmpeg
    try {
        $ffmpegCheck = ffmpeg -version 2>$null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ FFmpeg: Available" -ForegroundColor Green
        } else {
            Write-Host "   ⚠️  FFmpeg: Check failed (may still work)" -ForegroundColor Yellow
        }
    } catch {
        Write-Host "   ⚠️  FFmpeg: Not found in PATH (required for audio extraction)" -ForegroundColor Yellow
    }
    
    return $true
}

# Function to build executable
function Build-Executable {
    Write-Host "🔨 Building Windows executable..." -ForegroundColor Yellow
    
    $specFile = "audio_extractor_ui.spec"
    
    if (Test-Path $specFile) {
        Write-Host "   Using spec file: $specFile" -ForegroundColor Gray
        $cmd = "pyinstaller --clean $specFile"
    } else {
        Write-Host "   Using direct command (no spec file found)" -ForegroundColor Gray
        $cmd = @(
            "pyinstaller",
            "--onefile",
            "--windowed",
            "--name AudioExtractorUI",
            "--add-data audio-extractor/src;audio-extractor/src",
            "--hidden-import audio_extractor_ui.gui",
            "--hidden-import audio_extractor_ui.core",
            "--hidden-import tkinter",
            "--hidden-import tkinter.ttk",
            "--hidden-import yt_dlp",
            "src/main.py"
        ) -join " "
    }
    
    try {
        Invoke-Expression $cmd
        if ($LASTEXITCODE -eq 0) {
            Write-Host "   ✅ Build completed successfully!" -ForegroundColor Green
            return $true
        } else {
            Write-Host "   ❌ Build failed with exit code: $LASTEXITCODE" -ForegroundColor Red
            return $false
        }
    } catch {
        Write-Host "   ❌ Build failed: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Function to create release package
function New-ReleasePackage {
    Write-Host "📦 Creating release package..." -ForegroundColor Yellow
    
    if (Test-Path $OutputDir) {
        Remove-Item -Recurse -Force $OutputDir
    }
    New-Item -ItemType Directory -Path $OutputDir | Out-Null
    
    # Copy executable
    $exePath = "dist/AudioExtractorUI.exe"
    if (Test-Path $exePath) {
        Copy-Item $exePath "$OutputDir/AudioExtractorUI.exe"
        Write-Host "   ✅ Copied: $exePath" -ForegroundColor Green
        
        # Show file size
        $size = [math]::Round((Get-Item "$OutputDir/AudioExtractorUI.exe").Length / 1MB, 1)
        Write-Host "   📊 Executable size: ${size} MB" -ForegroundColor Gray
    } else {
        Write-Host "   ❌ Executable not found: $exePath" -ForegroundColor Red
        return $false
    }
    
    # Copy documentation
    $filesToCopy = @("README.md", "LICENSE")
    foreach ($file in $filesToCopy) {
        if (Test-Path $file) {
            Copy-Item $file "$OutputDir/$file"
            Write-Host "   ✅ Copied: $file" -ForegroundColor Green
        }
    }
    
    # Create usage instructions
    $usageText = @"
# Audio Extractor UI - Windows Release

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

## Build Information:
- Built on: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
- Python version: $(python --version 2>$null)
- PyInstaller version: $(python -c "import PyInstaller; print(PyInstaller.__version__)" 2>$null)
"@
    
    $usageText | Out-File -FilePath "$OutputDir/USAGE.txt" -Encoding UTF8
    Write-Host "   ✅ Created: USAGE.txt" -ForegroundColor Green
    
    Write-Host "`n🎉 Release package created in: $OutputDir" -ForegroundColor Cyan
    return $true
}

# Main execution
try {
    # Check virtual environment
    Test-VirtualEnvironment
    
    # Clean if requested
    if ($Clean) {
        Clear-BuildArtifacts
    }
    
    # Check dependencies
    if (-not (Test-Dependencies)) {
        exit 1
    }
    
    # Clean build artifacts
    if (-not $Clean) {
        Clear-BuildArtifacts
    }
    
    # Build executable
    if (-not (Build-Executable)) {
        exit 1
    }
    
    # Create release package (unless BuildOnly is specified)
    if (-not $BuildOnly) {
        if (-not (New-ReleasePackage)) {
            exit 1
        }
    }
    
    Write-Host "`n✅ Build process completed successfully!" -ForegroundColor Green
    Write-Host "`n📋 Next steps:" -ForegroundColor Cyan
    Write-Host "   1. Test the executable in the '$OutputDir' directory" -ForegroundColor White
    Write-Host "   2. Ensure FFmpeg is installed on target systems" -ForegroundColor White
    Write-Host "   3. Distribute the '$OutputDir' directory or create an installer" -ForegroundColor White
    
    if (-not $BuildOnly) {
        Write-Host "`n💡 Quick test:" -ForegroundColor Yellow
        Write-Host "   cd $OutputDir && .\AudioExtractorUI.exe --help" -ForegroundColor Gray
    }
    
} catch {
    Write-Host "`n❌ Build process failed: $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
