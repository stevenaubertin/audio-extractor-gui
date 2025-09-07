"""
Tests for the core audio extraction functionality.
"""

import unittest
import sys
from pathlib import Path

# Add src to path for testing
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from audio_extractor_ui.core import AudioExtractor
from audio_extractor_ui.utils import validate_file_path, validate_url


class TestAudioExtractor(unittest.TestCase):
    """Test cases for AudioExtractor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.extractor = AudioExtractor()
    
    def test_initialization(self):
        """Test AudioExtractor initialization."""
        self.assertIsInstance(self.extractor, AudioExtractor)
        self.assertTrue(self.extractor.output_dir.exists())
    
    def test_supported_formats(self):
        """Test getting supported formats."""
        formats = self.extractor.get_supported_formats()
        self.assertIsInstance(formats, list)
        self.assertIn("mp3", formats)
        self.assertIn("wav", formats)
    
    def test_quality_options(self):
        """Test getting quality options."""
        qualities = self.extractor.get_quality_options()
        self.assertIsInstance(qualities, list)
        self.assertIn("high", qualities)
        self.assertIn("medium", qualities)
        self.assertIn("low", qualities)


class TestUtils(unittest.TestCase):
    """Test cases for utility functions."""
    
    def test_validate_url(self):
        """Test URL validation."""
        # Valid URLs
        self.assertTrue(validate_url("https://www.youtube.com/watch?v=test"))
        self.assertTrue(validate_url("http://example.com"))
        
        # Invalid URLs
        self.assertFalse(validate_url("not-a-url"))
        self.assertFalse(validate_url(""))
        self.assertFalse(validate_url("ftp://example.com"))
    
    def test_validate_file_path(self):
        """Test file path validation."""
        # This file should exist
        self.assertTrue(validate_file_path(__file__))
        
        # This file should not exist
        self.assertFalse(validate_file_path("nonexistent_file.txt"))


if __name__ == "__main__":
    unittest.main()
