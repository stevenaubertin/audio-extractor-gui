@echo off
REM Audio Extractor UI - Virtual Environment Activation Script (Windows CMD)
REM Usage: activate.bat

echo 🔄 Activating virtual environment...

REM Check if virtual environment exists
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found. Creating it now...
    python -m venv venv
)

REM Activate the virtual environment
call venv\Scripts\activate.bat

if %errorlevel% equ 0 (
    echo ✅ Virtual environment activated!
    echo 📦 Installing/updating dependencies...
    
    REM Install requirements if they exist
    if exist "requirements.txt" (
        pip install -r requirements.txt
    )
    
    REM Install development requirements if they exist
    if exist "requirements-dev.txt" (
        pip install -r requirements-dev.txt
    )
    
    echo 🚀 Ready to develop! Use 'deactivate' to exit the virtual environment.
) else (
    echo ❌ Failed to activate virtual environment
)
