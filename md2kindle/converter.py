"""Converter for transforming markdown to various formats."""

import os
import sys
import tempfile
import subprocess
from pathlib import Path

from md2kindle.utils.styles import EPUB_CSS
from md2kindle.markdown import preprocess_markdown


def check_dependencies():
    """Check if required dependencies are installed."""
    # Check for pandoc
    try:
        subprocess.run(['pandoc', '--version'], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
    except (subprocess.SubprocessError, FileNotFoundError):
        print("Error: Pandoc is not installed or not in PATH.")
        print("Please install Pandoc: https://pandoc.org/installing.html")
        sys.exit(1)


def convert_markdown(args):
    """Convert markdown to the specified output format.
    
    Args:
        args: Command line arguments
        
    Returns:
        Path to the output file
    """
    input_file = Path(args.markdown_file)
    
    # Preprocess markdown for better formatting if not disabled
    if args.no_formatting_fix:
        processed_file = str(input_file)
    else:
        processed_file = preprocess_markdown(input_file)
    
    # Determine output file
    if args.output:
        output_file = Path(args.output)
    else:
        output_file = input_file.with_suffix(f'.{args.format}')
    
    # Build pandoc command
    cmd = ['pandoc', processed_file, '-o', str(output_file), '--standalone']
    
    # Add metadata if provided
    if args.title:
        cmd.extend(['--metadata', f'title={args.title}'])
    else:
        cmd.extend(['--metadata', f'title={input_file.stem}'])
        
    if args.author:
        cmd.extend(['--metadata', f'author={args.author}'])
    
    # Add cover image if provided
    if args.cover and os.path.exists(args.cover):
        cmd.extend(['--epub-cover-image', args.cover])
    
    # Add CSS for better bullet point rendering in EPUB with compact spacing
    if args.format == 'epub':
        css_file = Path(tempfile.gettempdir()) / "kindle_style.css"
        with open(css_file, 'w', encoding='utf-8') as f:
            f.write(EPUB_CSS)
        cmd.extend(['--css', str(css_file)])
    
    # Add additional options for better list rendering
    cmd.extend(['--wrap=none', '--toc'])
    
    # Run pandoc
    try:
        print(f"Converting {input_file} to {output_file}...")
        subprocess.run(cmd, check=True)
        print(f"Conversion complete: {output_file}")
        return output_file
    except subprocess.CalledProcessError as e:
        print(f"Error during conversion: {e}")
        sys.exit(1)
    finally:
        # Clean up temp files
        if processed_file != str(input_file) and os.path.exists(processed_file):
            os.unlink(processed_file)