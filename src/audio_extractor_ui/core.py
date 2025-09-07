"""
Core functionality for audio extraction operations.
Integrates with the audio-extractor submodule for actual processing.
"""

import logging
from pathlib import Path
from typing import Optional, Dict, Any, List

from .integration import get_audio_extractor, is_core_available, get_core_info

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class AudioExtractor:
    """Core audio extraction functionality using audio-extractor submodule."""

    def __init__(self):
        """Initialize the audio extractor."""
        self.output_dir = Path("output")
        self.output_dir.mkdir(exist_ok=True)
        self.core_extractor = get_audio_extractor()

    def is_available(self) -> bool:
        """Check if the core audio extractor is available."""
        return is_core_available()

    def extract_from_file(
        self,
        input_file: str,
        output_format: str = "mp3",
        quality: str = "high",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        duration: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Extract audio from a local video file.

        Args:
            input_file: Path to the input video file
            output_format: Audio format (mp3, wav, flac, aac)
            quality: Audio quality (high, medium, low)
            start_time: Start time for extraction (optional)
            end_time: End time for extraction (optional)
            duration: Duration for extraction (optional)

        Returns:
            Dict containing extraction results
        """
        logger.info(f"Extracting audio from: {input_file}")

        if not self.is_available():
            error_msg = (
                "Audio extractor core not available. "
                "Initialize submodule first."
            )
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "output": "",
                "exit_code": -1,
            }

        return self.core_extractor.extract_from_local_file(
            input_path=input_file,
            output_dir=str(self.output_dir),
            format=output_format,
            quality=quality,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
        )

    def extract_from_url(
        self,
        url: str,
        output_format: str = "mp3",
        quality: str = "high",
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        duration: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Extract audio from a URL (YouTube, etc.).

        Args:
            url: Video URL
            output_format: Audio format (mp3, wav, flac, aac)
            quality: Audio quality (high, medium, low)
            start_time: Start time for extraction (optional)
            end_time: End time for extraction (optional)
            duration: Duration for extraction (optional)

        Returns:
            Dict containing extraction results
        """
        logger.info(f"Extracting audio from URL: {url}")

        if not self.is_available():
            error_msg = (
                "Audio extractor core not available. "
                "Initialize submodule first."
            )
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "output": "",
                "exit_code": -1,
            }

        return self.core_extractor.extract_from_url(
            url=url,
            output_dir=str(self.output_dir),
            format=output_format,
            quality=quality,
            start_time=start_time,
            end_time=end_time,
            duration=duration,
        )

    def batch_extract(
        self, input_dir: str, output_format: str = "mp3", quality: str = "high"
    ) -> Dict[str, Any]:
        """
        Perform batch audio extraction from a directory.

        Args:
            input_dir: Directory containing video files
            output_format: Audio format (mp3, wav, flac, aac)
            quality: Audio quality (high, medium, low)

        Returns:
            Dict containing batch extraction results
        """
        logger.info(f"Batch extracting audio from directory: {input_dir}")

        if not self.is_available():
            error_msg = (
                "Audio extractor core not available. "
                "Initialize submodule first."
            )
            logger.error(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "output": "",
                "exit_code": -1,
            }

        return self.core_extractor.batch_extract(
            input_dir=input_dir,
            output_dir=str(self.output_dir),
            format=output_format,
            quality=quality,
        )

    def check_dependencies(self) -> Dict[str, Any]:
        """Check if all required dependencies are available."""
        if not self.is_available():
            return {
                "success": False,
                "error": "Audio extractor core not available",
                "dependencies": {
                    "core_available": False,
                    "ffmpeg": "unknown",
                    "yt-dlp": "unknown",
                },
            }

        return self.core_extractor.check_dependencies()

    def get_supported_formats(self) -> List[str]:
        """Get list of supported audio formats."""
        return ["mp3", "wav", "flac", "aac"]

    def get_quality_options(self) -> List[str]:
        """Get list of available quality options."""
        return ["high", "medium", "low"]

    def get_core_info(self) -> Dict[str, Any]:
        """Get information about the core audio extractor."""
        return get_core_info()
