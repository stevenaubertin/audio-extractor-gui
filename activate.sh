#!/bin/bash
# Audio Extractor UI - Virtual Environment Activation Script (Unix/Linux/macOS)
# Usage: source activate.sh or . activate.sh

echo "🔄 Activating virtual environment..."

# Check if virtual environment exists
if [ ! -f "venv/bin/activate" ]; then
    echo "❌ Virtual environment not found. Creating it now..."
    python -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

if [ $? -eq 0 ]; then
    echo "✅ Virtual environment activated!"
    echo "📦 Installing/updating dependencies..."
    
    # Install requirements if they exist
    if [ -f "requirements.txt" ]; then
        pip install -r requirements.txt
    fi
    
    # Install development requirements if they exist
    if [ -f "requirements-dev.txt" ]; then
        pip install -r requirements-dev.txt
    fi
    
    echo "🚀 Ready to develop! Use 'deactivate' to exit the virtual environment."
else
    echo "❌ Failed to activate virtual environment"
fi
