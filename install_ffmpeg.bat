@echo off
:: FFmpeg Installation Script for AudioExtractorUI (Windows)
:: This batch file provides an easy way to install FFmpeg

title AudioExtractorUI - FFmpeg Installation

echo.
echo ========================================
echo   FFmpeg Installation for AudioExtractorUI
echo ========================================
echo.

:: Check if FFmpeg is already installed
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo [✓] FFmpeg is already installed!
    echo.
    ffmpeg -version | findstr /i "ffmpeg version"
    echo.
    echo AudioExtractorUI should work correctly.
    goto :end
)

echo [!] FFmpeg not found. Installation required.
echo.

:: Check for PowerShell
powershell -Command "Write-Host 'PowerShell available'" >nul 2>&1
if %errorlevel% neq 0 (
    echo [x] PowerShell not available. Cannot run automated installation.
    goto :manual
)

echo Choose installation method:
echo.
echo 1. System installation (requires Administrator)
echo 2. Portable installation (current folder)
echo 3. Show manual installation instructions
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" goto :system
if "%choice%"=="2" goto :portable
if "%choice%"=="3" goto :manual
if "%choice%"=="4" goto :end
goto :invalid

:system
echo.
echo [i] Running system installation...
echo [i] You may be prompted for Administrator privileges.
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0install_ffmpeg.ps1"
goto :end

:portable
echo.
echo [i] Running portable installation...
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0install_ffmpeg.ps1" -Portable
goto :end

:manual
echo.
echo ========================================
echo   Manual Installation Instructions
echo ========================================
echo.
echo Method 1: Package Managers
echo.
echo   Chocolatey (if installed):
echo   ^> choco install ffmpeg
echo.
echo   Scoop (if installed):
echo   ^> scoop install ffmpeg
echo.
echo   Winget:
echo   ^> winget install Gyan.FFmpeg
echo.
echo Method 2: Manual Download
echo.
echo   1. Go to: https://ffmpeg.org/download.html
echo   2. Click "Windows" and download "Windows builds"
echo   3. Extract the downloaded zip file
echo   4. Copy ffmpeg.exe to a folder (e.g., C:\ffmpeg\bin\)
echo   5. Add that folder to your system PATH:
echo      - Press Win+R, type "sysdm.cpl", press Enter
echo      - Click "Environment Variables"
echo      - Under "System Variables", find "Path" and click "Edit"
echo      - Click "New" and add your ffmpeg folder path
echo      - Click OK to save all changes
echo      - Restart your command prompt
echo.
echo Method 3: Use with AudioExtractorUI (if you have ffmpeg.exe)
echo.
echo   1. Put ffmpeg.exe in the same folder as AudioExtractorUI.exe
echo   2. AudioExtractorUI should find it automatically
echo.
goto :end

:invalid
echo.
echo [x] Invalid choice. Please enter 1, 2, 3, or 4.
echo.
pause
goto :start

:end
echo.
echo ========================================
echo.
echo After installation, test with: ffmpeg -version
echo Then run AudioExtractorUI.exe
echo.
pause
