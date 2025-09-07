"""
Audio Extractor UI - A user interface for extracting audio from videos.
"""

__version__ = "0.1.0"
__author__ = "Your Name"
__email__ = "your.email@example.com"
__description__ = "A user interface for extracting audio from videos using ffmpeg and yt-dlp"

# Package imports
from . import core
from . import utils

__all__ = [
    "__version__",
    "__author__", 
    "__email__",
    "__description__",
    "core",
    "utils",
]
