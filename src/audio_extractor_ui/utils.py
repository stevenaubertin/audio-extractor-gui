"""
Utility functions for the audio extractor UI.
"""

import os
import re
import logging
from pathlib import Path
from typing import Optional, List, Tuple

logger = logging.getLogger(__name__)


def validate_file_path(file_path: str) -> bool:
    """
    Validate if a file path exists and is readable.
    
    Args:
        file_path: Path to the file
        
    Returns:
        bool: True if file exists and is readable, False otherwise
    """
    try:
        path = Path(file_path)
        return path.exists() and path.is_file() and os.access(path, os.R_OK)
    except Exception as e:
        logger.error(f"Error validating file path {file_path}: {e}")
        return False


def validate_url(url: str) -> bool:
    """
    Basic URL validation.
    
    Args:
        url: URL to validate
        
    Returns:
        bool: True if URL format appears valid, False otherwise
    """
    url_pattern = re.compile(
        r'^https?://'  # http:// or https://
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain...
        r'localhost|'  # localhost...
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
        r'(?::\d+)?'  # optional port
        r'(?:/?|[/?]\S+)$', re.IGNORECASE)
    
    return url_pattern.match(url) is not None


def get_video_extensions() -> List[str]:
    """
    Get list of supported video file extensions.
    
    Returns:
        List of video file extensions
    """
    return ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv', '.webm', '.m4v', '.3gp', '.ogv']


def is_video_file(file_path: str) -> bool:
    """
    Check if a file is a supported video file.
    
    Args:
        file_path: Path to the file
        
    Returns:
        bool: True if file has a video extension, False otherwise
    """
    return Path(file_path).suffix.lower() in get_video_extensions()


def format_file_size(size_bytes: int) -> str:
    """
    Format file size in human readable format.
    
    Args:
        size_bytes: Size in bytes
        
    Returns:
        Formatted file size string
    """
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename by removing invalid characters.
    
    Args:
        filename: Original filename
        
    Returns:
        Sanitized filename safe for filesystem
    """
    # Remove invalid characters for most filesystems
    invalid_chars = r'<>:"/\\|?*'
    for char in invalid_chars:
        filename = filename.replace(char, '_')
    
    # Remove leading/trailing spaces and dots
    filename = filename.strip(' .')
    
    # Ensure filename is not empty
    if not filename:
        filename = "untitled"
    
    return filename


def create_output_directory(base_path: str = "output") -> Path:
    """
    Create and return output directory path.
    
    Args:
        base_path: Base directory name
        
    Returns:
        Path object for the output directory
    """
    output_dir = Path(base_path)
    output_dir.mkdir(exist_ok=True)
    return output_dir
