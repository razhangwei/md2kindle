"""Markdown preprocessing for better Kindle formatting."""

import re
import tempfile
from pathlib import Path


def preprocess_markdown(input_file, improved_formatting=True):
    """Preprocess markdown file to improve formatting for Kindle conversion.
    
    Args:
        input_file: Path to the markdown file
        improved_formatting: Whether to apply formatting improvements
        
    Returns:
        Path to the processed file
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    if not improved_formatting:
        return str(input_file)
    
    # Normalize bullet lists with compact formatting
    
    # Add blank lines before bullet lists if missing (list start)
    content = re.sub(r'([^\n])\n(- )', r'\1\n\n\2', content)
    
    # Add blank lines after bullet lists if missing (list end)
    content = re.sub(r'(- [^\n]+)\n([^-\n])', r'\1\n\n\2', content)
    
    # Remove any extra blank lines between bullet points to make lists compact
    content = re.sub(r'(- [^\n]+)\n\n(- )', r'\1\n\2', content)
    
    # Create temp file with processed content
    temp_file = Path(tempfile.gettempdir()) / f"processed_{Path(input_file).name}"
    with open(temp_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return str(temp_file)