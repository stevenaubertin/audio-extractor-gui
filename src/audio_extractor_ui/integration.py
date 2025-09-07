"""
Integration module for the audio-extractor submodule.

This module provides a clean interface to the core audio extraction functionality
from the audio-extractor submodule, making it easy to use within the UI components.
"""

import sys
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any, List
import importlib.util


class AudioExtractorCore:
    """Interface to the core audio-extractor functionality."""
    
    def __init__(self):
        """Initialize the audio extractor core interface."""
        self.core_path = self._find_core_path()
        self.core_available = self._check_core_availability()
    
    def _find_core_path(self) -> Optional[Path]:
        """Find the path to the audio-extractor core module."""
        # Start from the current file's directory and go up to project root
        current_dir = Path(__file__).parent
        project_root = current_dir.parent.parent
        
        # Look for the audio-extractor submodule
        submodule_path = project_root / "audio-extractor" / "src"
        
        if submodule_path.exists():
            return submodule_path
        return None
    
    def _check_core_availability(self) -> bool:
        """Check if the core audio extractor is available."""
        if not self.core_path:
            return False
        
        extract_audio_path = self.core_path / "extract_audio.py"
        return extract_audio_path.exists()
    
    def is_available(self) -> bool:
        """Check if the core audio extractor is available."""
        return self.core_available
    
    def get_core_version(self) -> Optional[str]:
        """Get the version of the core audio extractor."""
        if not self.is_available():
            return None
        
        try:
            # Add the core path to sys.path temporarily
            if str(self.core_path) not in sys.path:
                sys.path.insert(0, str(self.core_path))
            
            # Try to import and get version info
            spec = importlib.util.spec_from_file_location(
                "extract_audio", self.core_path / "extract_audio.py"
            )
            extract_audio = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(extract_audio)
            
            # Look for version information
            if hasattr(extract_audio, '__version__'):
                return extract_audio.__version__
            
            # If no version attribute, try to get it from git or other means
            return "unknown"
            
        except Exception:
            return None
    
    def run_core_command(self, args: List[str]) -> Dict[str, Any]:
        """
        Run a core audio extractor command.
        
        Args:
            args: List of command line arguments for the core extractor
            
        Returns:
            Dict containing result information
        """
        if not self.is_available():
            return {
                "success": False,
                "error": "Core audio extractor not available",
                "output": "",
                "exit_code": -1
            }
        
        try:
            # Build the command
            python_exe = sys.executable
            core_script = self.core_path / "extract_audio.py"
            cmd = [python_exe, str(core_script)] + args
            
            # Run the command
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                cwd=str(self.core_path.parent)
            )
            
            return {
                "success": result.returncode == 0,
                "error": result.stderr if result.returncode != 0 else "",
                "output": result.stdout,
                "exit_code": result.returncode
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Failed to run core command: {str(e)}",
                "output": "",
                "exit_code": -1
            }
    
    def extract_from_local_file(
        self, 
        input_path: str, 
        output_dir: str = "output",
        format: str = "mp3",
        quality: str = "high",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        duration: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract audio from a local video file.
        
        Args:
            input_path: Path to the input video file
            output_dir: Output directory for extracted audio
            format: Audio format (mp3, wav, flac, aac)
            quality: Audio quality (high, medium, low)
            start_time: Start time for extraction (optional)
            end_time: End time for extraction (optional)
            duration: Duration for extraction (optional)
            
        Returns:
            Dict containing extraction result
        """
        args = [
            "--format", format,
            "--quality", quality,
            "--output", output_dir,
            "local", input_path
        ]
        
        # Add time range parameters if specified
        if start_time:
            args.extend(["--start-time", start_time])
        if end_time:
            args.extend(["--end-time", end_time])
        if duration:
            args.extend(["--duration", duration])
        
        return self.run_core_command(args)
    
    def extract_from_url(
        self, 
        url: str, 
        output_dir: str = "output",
        format: str = "mp3",
        quality: str = "high",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        duration: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Extract audio from a URL (YouTube, etc.).
        
        Args:
            url: URL to download and extract audio from
            output_dir: Output directory for extracted audio
            format: Audio format (mp3, wav, flac, aac)
            quality: Audio quality (high, medium, low)
            start_time: Start time for extraction (optional)
            end_time: End time for extraction (optional)
            duration: Duration for extraction (optional)
            
        Returns:
            Dict containing extraction result
        """
        args = [
            "--format", format,
            "--quality", quality,
            "--output", output_dir,
            "url", url
        ]
        
        # Add time range parameters if specified
        if start_time:
            args.extend(["--start-time", start_time])
        if end_time:
            args.extend(["--end-time", end_time])
        if duration:
            args.extend(["--duration", duration])
        
        return self.run_core_command(args)
    
    def batch_extract(
        self, 
        input_dir: str, 
        output_dir: str = "output",
        format: str = "mp3",
        quality: str = "high"
    ) -> Dict[str, Any]:
        """
        Perform batch audio extraction from a directory.
        
        Args:
            input_dir: Directory containing video files
            output_dir: Output directory for extracted audio
            format: Audio format (mp3, wav, flac, aac)
            quality: Audio quality (high, medium, low)
            
        Returns:
            Dict containing extraction result
        """
        args = [
            "--format", format,
            "--quality", quality,
            "--output", output_dir,
            "batch", input_dir
        ]
        
        return self.run_core_command(args)
    
    def check_dependencies(self) -> Dict[str, Any]:
        """
        Check if all required dependencies are available.
        
        Returns:
            Dict containing dependency check results
        """
        args = ["check-dependencies"]
        return self.run_core_command(args)


# Global instance for easy access
audio_extractor = AudioExtractorCore()


def get_audio_extractor() -> AudioExtractorCore:
    """Get the global audio extractor instance."""
    return audio_extractor


def is_core_available() -> bool:
    """Check if the audio extractor core is available."""
    return audio_extractor.is_available()


def get_core_info() -> Dict[str, Any]:
    """Get information about the core audio extractor."""
    return {
        "available": audio_extractor.is_available(),
        "version": audio_extractor.get_core_version(),
        "core_path": str(audio_extractor.core_path) if audio_extractor.core_path else None
    }
