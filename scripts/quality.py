#!/usr/bin/env python3
"""
Development script for code quality checks and formatting.
"""

import sys
import subprocess
import argparse
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return the result."""
    if description:
        print(f"🔄 {description}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description or 'Command'} passed")
        if result.stdout.strip():
            print(result.stdout)
        return True
    else:
        print(f"❌ {description or 'Command'} failed")
        if result.stderr.strip():
            print(result.stderr)
        if result.stdout.strip():
            print(result.stdout)
        return False


def format_code():
    """Format code with black and isort."""
    success = True
    
    print("🎨 Formatting code...")
    success &= run_command("black src tests", "Running Black formatter")
    success &= run_command("isort src tests", "Sorting imports with isort")
    
    return success


def lint_code():
    """Run linting checks."""
    success = True
    
    print("🔍 Running linting checks...")
    success &= run_command("flake8 src tests", "Running flake8")
    success &= run_command("mypy src", "Running mypy type checking")
    
    return success


def check_code():
    """Run all code quality checks without formatting."""
    success = True
    
    print("📋 Running code quality checks...")
    success &= run_command("black --check src tests", "Checking Black formatting")
    success &= run_command("isort --check-only src tests", "Checking import sorting")
    success &= run_command("flake8 src tests", "Running flake8")
    success &= run_command("mypy src", "Running mypy type checking")
    
    return success


def main():
    parser = argparse.ArgumentParser(description="Code quality tools")
    parser.add_argument("--format", action="store_true", help="Format code (black + isort)")
    parser.add_argument("--lint", action="store_true", help="Run linting (flake8 + mypy)")
    parser.add_argument("--check", action="store_true", help="Check code quality without formatting")
    parser.add_argument("--all", action="store_true", help="Format and lint code")
    
    args = parser.parse_args()
    
    success = True
    
    if args.format or args.all:
        success &= format_code()
    
    if args.lint or args.all:
        success &= lint_code()
    
    if args.check:
        success &= check_code()
    
    if not any([args.format, args.lint, args.check, args.all]):
        # Default behavior: run checks
        success = check_code()
    
    if success:
        print("\n🎉 All checks passed!")
        sys.exit(0)
    else:
        print("\n💥 Some checks failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
