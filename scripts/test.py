#!/usr/bin/env python3
"""
Development script for running tests with various options.
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
        print(f"✅ Success")
        if result.stdout.strip():
            print(result.stdout)
    else:
        print(f"❌ Failed")
        if result.stderr.strip():
            print(result.stderr)
    
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Run tests with various options")
    parser.add_argument("--coverage", action="store_true", help="Run with coverage")
    parser.add_argument("--html", action="store_true", help="Generate HTML coverage report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Verbose output")
    parser.add_argument("--file", help="Run specific test file")
    parser.add_argument("--watch", action="store_true", help="Watch for changes")
    
    args = parser.parse_args()
    
    # Base command
    cmd = ["pytest"]
    
    if args.verbose:
        cmd.append("-v")
    
    if args.coverage:
        cmd.extend(["--cov=src", "--cov-report=term-missing"])
        
    if args.html:
        cmd.extend(["--cov=src", "--cov-report=html"])
    
    if args.file:
        cmd.append(args.file)
    
    if args.watch:
        cmd.append("--looponfail")
    
    # Run the command
    cmd_str = " ".join(cmd)
    print(f"Running: {cmd_str}")
    
    try:
        subprocess.run(cmd_str, shell=True)
    except KeyboardInterrupt:
        print("\n🛑 Tests interrupted by user")
        sys.exit(1)


if __name__ == "__main__":
    main()
