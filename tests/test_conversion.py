#!/usr/bin/env python3
import os
import sys
import tempfile
import subprocess
from pathlib import Path
import unittest

class TestMarkdownConversion(unittest.TestCase):
    
    def setUp(self):
        self.sample_md = Path("sample.md")
        self.script_path = Path("./md2kindle.py")
        self.temp_dir = tempfile.TemporaryDirectory()
        
    def tearDown(self):
        self.temp_dir.cleanup()
        
    def test_script_exists(self):
        self.assertTrue(self.script_path.exists(), "Script file doesn't exist")
        
    def test_sample_exists(self):
        self.assertTrue(self.sample_md.exists(), "Sample markdown file doesn't exist")
        
    def test_conversion_to_epub(self):
        output_path = Path(self.temp_dir.name) / "output.epub"
        cmd = [
            sys.executable, 
            str(self.script_path),
            str(self.sample_md),
            "--output", str(output_path),
            "--no-send"
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, f"Process failed: {result.stderr}")
        self.assertTrue(output_path.exists(), "Output EPUB file wasn't created")

if __name__ == "__main__":
    unittest.main()