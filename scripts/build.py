#!/usr/bin/env python3
"""
Development script for building and deploying the package.
"""

import sys
import subprocess
import argparse
import shutil
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return the result."""
    if description:
        print(f"🔄 {description}")
    
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if result.returncode == 0:
        print(f"✅ {description or 'Command'} completed")
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


def clean_build():
    """Clean build artifacts."""
    print("🧹 Cleaning build artifacts...")
    
    # Directories to clean
    dirs_to_clean = [
        "build",
        "dist", 
        "*.egg-info",
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        "htmlcov"
    ]
    
    for pattern in dirs_to_clean:
        for path in Path(".").glob(f"**/{pattern}"):
            if path.is_dir():
                print(f"  Removing {path}")
                shutil.rmtree(path, ignore_errors=True)
            elif path.is_file():
                print(f"  Removing {path}")
                path.unlink()
    
    print("✅ Build artifacts cleaned")


def build_package():
    """Build the package."""
    success = True
    
    print("📦 Building package...")
    success &= run_command("python -m build", "Building wheel and source distribution")
    
    return success


def install_local():
    """Install package locally in development mode."""
    success = True
    
    print("📥 Installing package locally...")
    success &= run_command("pip install -e .", "Installing in development mode")
    
    return success


def install_with_deps():
    """Install package with all dependencies."""
    success = True
    
    print("📥 Installing package with all dependencies...")
    success &= run_command("pip install -e .[dev]", "Installing with development dependencies")
    
    return success


def check_package():
    """Check the built package."""
    success = True
    
    print("🔍 Checking package...")
    success &= run_command("python -m twine check dist/*", "Checking package with twine")
    
    return success


def main():
    parser = argparse.ArgumentParser(description="Build and deployment tools")
    parser.add_argument("--clean", action="store_true", help="Clean build artifacts")
    parser.add_argument("--build", action="store_true", help="Build package")
    parser.add_argument("--install", action="store_true", help="Install locally in dev mode")
    parser.add_argument("--install-deps", action="store_true", help="Install with all dependencies")
    parser.add_argument("--check", action="store_true", help="Check built package")
    parser.add_argument("--all", action="store_true", help="Clean, build, and check")
    
    args = parser.parse_args()
    
    success = True
    
    if args.clean or args.all:
        clean_build()
    
    if args.build or args.all:
        success &= build_package()
    
    if args.install:
        success &= install_local()
    
    if args.install_deps:
        success &= install_with_deps()
    
    if args.check or args.all:
        success &= check_package()
    
    if not any([args.clean, args.build, args.install, args.install_deps, args.check, args.all]):
        # Default behavior: build
        success = build_package()
    
    if success:
        print("\n🎉 Build operations completed successfully!")
        sys.exit(0)
    else:
        print("\n💥 Some build operations failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()
