# FFmpeg Installation Script for Windows
# This script helps install FFmpeg automatically for AudioExtractorUI

param(
    [switch]$Force = $false,
    [switch]$Portable = $false,
    [string]$InstallPath = "$env:ProgramFiles\FFmpeg"
)

Write-Host "🎬 FFmpeg Installation Script for AudioExtractorUI" -ForegroundColor Cyan
Write-Host "=" * 55

# Check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Check if FFmpeg is already installed
function Test-FFmpegInstallation {
    try {
        $ffmpegVersion = ffmpeg -version 2>$null
        if ($LASTEXITCODE -eq 0) {
            $versionLine = ($ffmpegVersion -split "`n")[0]
            Write-Host "✅ FFmpeg is already installed: $versionLine" -ForegroundColor Green
            return $true
        }
    } catch {
        Write-Host "❌ FFmpeg not found in PATH" -ForegroundColor Yellow
        return $false
    }
    return $false
}

# Download FFmpeg
function Get-FFmpeg {
    param(
        [string]$DownloadPath
    )
    
    Write-Host "⬇️ Downloading FFmpeg..." -ForegroundColor Yellow
    
    # FFmpeg download URLs (these may need updating)
    $ffmpegUrl = "https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip"
    $zipFile = Join-Path $env:TEMP "ffmpeg-release-essentials.zip"
    
    try {
        # Download with progress
        $webClient = New-Object System.Net.WebClient
        $webClient.DownloadFile($ffmpegUrl, $zipFile)
        Write-Host "✅ Downloaded FFmpeg to: $zipFile" -ForegroundColor Green
        return $zipFile
    } catch {
        Write-Host "❌ Failed to download FFmpeg: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "💡 Please download manually from: https://ffmpeg.org/download.html" -ForegroundColor Yellow
        return $null
    }
}

# Extract and install FFmpeg
function Install-FFmpeg {
    param(
        [string]$ZipFile,
        [string]$InstallPath
    )
    
    Write-Host "📦 Installing FFmpeg to: $InstallPath" -ForegroundColor Yellow
    
    try {
        # Create installation directory
        if (-not (Test-Path $InstallPath)) {
            New-Item -ItemType Directory -Path $InstallPath -Force | Out-Null
        }
        
        # Extract ZIP file
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        $zip = [System.IO.Compression.ZipFile]::OpenRead($ZipFile)
        
        foreach ($entry in $zip.Entries) {
            if ($entry.Name -match "ffmpeg\.exe|ffprobe\.exe|ffplay\.exe") {
                $destinationPath = Join-Path $InstallPath $entry.Name
                [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $destinationPath, $true)
                Write-Host "   Extracted: $($entry.Name)" -ForegroundColor Gray
            }
        }
        
        $zip.Dispose()
        Write-Host "✅ FFmpeg installed successfully!" -ForegroundColor Green
        return $true
    } catch {
        Write-Host "❌ Failed to install FFmpeg: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Add FFmpeg to PATH
function Add-FFmpegToPath {
    param(
        [string]$FFmpegPath
    )
    
    Write-Host "🔧 Adding FFmpeg to system PATH..." -ForegroundColor Yellow
    
    try {
        # Get current PATH
        $currentPath = [Environment]::GetEnvironmentVariable("Path", "Machine")
        
        # Check if FFmpeg path is already in PATH
        if ($currentPath -split ";" | Where-Object { $_ -eq $FFmpegPath }) {
            Write-Host "✅ FFmpeg path already in system PATH" -ForegroundColor Green
            return $true
        }
        
        # Add to PATH
        $newPath = $currentPath + ";" + $FFmpegPath
        [Environment]::SetEnvironmentVariable("Path", $newPath, "Machine")
        
        # Update current session PATH
        $env:Path = [Environment]::GetEnvironmentVariable("Path", "Machine") + ";" + [Environment]::GetEnvironmentVariable("Path", "User")
        
        Write-Host "✅ FFmpeg added to system PATH" -ForegroundColor Green
        Write-Host "💡 You may need to restart your command prompt/PowerShell" -ForegroundColor Yellow
        return $true
    } catch {
        Write-Host "❌ Failed to add FFmpeg to PATH: $($_.Exception.Message)" -ForegroundColor Red
        Write-Host "💡 Please add '$FFmpegPath' to your PATH manually" -ForegroundColor Yellow
        return $false
    }
}

# Create portable installation
function Install-FFmpegPortable {
    param(
        [string]$ZipFile
    )
    
    $portableDir = Join-Path (Get-Location) "ffmpeg"
    Write-Host "📦 Creating portable FFmpeg installation in: $portableDir" -ForegroundColor Yellow
    
    try {
        if (-not (Test-Path $portableDir)) {
            New-Item -ItemType Directory -Path $portableDir -Force | Out-Null
        }
        
        # Extract executables
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        $zip = [System.IO.Compression.ZipFile]::OpenRead($ZipFile)
        
        foreach ($entry in $zip.Entries) {
            if ($entry.Name -match "ffmpeg\.exe|ffprobe\.exe|ffplay\.exe") {
                $destinationPath = Join-Path $portableDir $entry.Name
                [System.IO.Compression.ZipFileExtensions]::ExtractToFile($entry, $destinationPath, $true)
                Write-Host "   Extracted: $($entry.Name)" -ForegroundColor Gray
            }
        }
        
        $zip.Dispose()
        
        # Create batch file for easy usage
        $batchContent = @"
@echo off
echo AudioExtractorUI - Portable FFmpeg Setup
echo Adding FFmpeg to PATH for this session...
set PATH=%~dp0ffmpeg;%PATH%
echo.
echo FFmpeg is now available. You can run:
echo - AudioExtractorUI.exe
echo - ffmpeg -version (to test)
echo.
pause
"@
        $batchContent | Out-File -FilePath "run_with_ffmpeg.bat" -Encoding ASCII
        
        Write-Host "✅ Portable FFmpeg installation completed!" -ForegroundColor Green
        Write-Host "💡 Use 'run_with_ffmpeg.bat' to run AudioExtractorUI with FFmpeg" -ForegroundColor Yellow
        return $true
    } catch {
        Write-Host "❌ Failed to create portable installation: $($_.Exception.Message)" -ForegroundColor Red
        return $false
    }
}

# Alternative installation methods
function Show-AlternativeInstallMethods {
    Write-Host "`n🔧 Alternative Installation Methods:" -ForegroundColor Cyan
    Write-Host ""
    
    Write-Host "1. Chocolatey (if installed):" -ForegroundColor Yellow
    Write-Host "   choco install ffmpeg" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "2. Scoop (if installed):" -ForegroundColor Yellow
    Write-Host "   scoop install ffmpeg" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "3. Winget:" -ForegroundColor Yellow
    Write-Host "   winget install Gyan.FFmpeg" -ForegroundColor Gray
    Write-Host ""
    
    Write-Host "4. Manual Download:" -ForegroundColor Yellow
    Write-Host "   https://ffmpeg.org/download.html" -ForegroundColor Gray
    Write-Host "   Download 'Windows builds' and extract to a folder" -ForegroundColor Gray
    Write-Host "   Add the folder to your system PATH" -ForegroundColor Gray
}

# Main execution
try {
    # Check if FFmpeg is already installed
    if ((Test-FFmpegInstallation) -and -not $Force) {
        Write-Host "`n✅ FFmpeg is already available! AudioExtractorUI should work correctly." -ForegroundColor Green
        exit 0
    }
    
    if ($Force) {
        Write-Host "🔄 Force installation requested..." -ForegroundColor Yellow
    }
    
    # Check for administrator privileges (required for system installation)
    if (-not $Portable -and -not (Test-Administrator)) {
        Write-Host "⚠️  Administrator privileges required for system installation." -ForegroundColor Yellow
        $response = Read-Host "Install as portable instead? (y/N)"
        if ($response -eq 'y' -or $response -eq 'Y') {
            $Portable = $true
        } else {
            Write-Host "💡 Please run this script as Administrator for system installation." -ForegroundColor Yellow
            Show-AlternativeInstallMethods
            exit 1
        }
    }
    
    # Download FFmpeg
    $zipFile = Get-FFmpeg -DownloadPath $env:TEMP
    if (-not $zipFile) {
        Show-AlternativeInstallMethods
        exit 1
    }
    
    if ($Portable) {
        # Portable installation
        $success = Install-FFmpegPortable -ZipFile $zipFile
    } else {
        # System installation
        $success = Install-FFmpeg -ZipFile $zipFile -InstallPath $InstallPath
        if ($success) {
            $success = Add-FFmpegToPath -FFmpegPath $InstallPath
        }
    }
    
    # Cleanup
    if (Test-Path $zipFile) {
        Remove-Item $zipFile -Force
    }
    
    if ($success) {
        Write-Host "`n🎉 Installation completed successfully!" -ForegroundColor Green
        Write-Host ""
        
        if ($Portable) {
            Write-Host "📁 Portable installation created in: ffmpeg/" -ForegroundColor Cyan
            Write-Host "🚀 Use 'run_with_ffmpeg.bat' to run AudioExtractorUI" -ForegroundColor Cyan
        } else {
            Write-Host "🔧 FFmpeg installed to: $InstallPath" -ForegroundColor Cyan
            Write-Host "🚀 You can now run AudioExtractorUI.exe" -ForegroundColor Cyan
            Write-Host "💡 Restart your command prompt to refresh PATH" -ForegroundColor Yellow
        }
        
        Write-Host "`n🧪 Test FFmpeg installation:" -ForegroundColor Cyan
        Write-Host "   ffmpeg -version" -ForegroundColor Gray
    } else {
        Write-Host "`n❌ Installation failed!" -ForegroundColor Red
        Show-AlternativeInstallMethods
        exit 1
    }
    
} catch {
    Write-Host "`n❌ Unexpected error: $($_.Exception.Message)" -ForegroundColor Red
    Show-AlternativeInstallMethods
    exit 1
}
