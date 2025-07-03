"""Command-line interface for md2kindle."""

import os
import sys
import argparse
from pathlib import Path

from md2kindle.converter import check_dependencies, convert_markdown
from md2kindle.email import send_to_kindle


def parse_arguments():
    """Parse command-line arguments.
    
    Returns:
        Parsed arguments
    """
    parser = argparse.ArgumentParser(description='Convert Markdown files to Kindle format and send to device')
    parser.add_argument('markdown_file', help='Path to the Markdown file')
    parser.add_argument('--title', help='Book title (defaults to filename)')
    parser.add_argument('--author', help='Author name')
    parser.add_argument('--cover', help='Path to cover image')
    parser.add_argument('--format', choices=['epub'], default='epub', 
                        help='Output format (default: epub)')
    parser.add_argument('--no-send', action='store_true', help='Convert only, don\'t send via email')
    parser.add_argument('--output', help='Output file path (defaults to input file with new extension)')
    parser.add_argument('--no-formatting-fix', action='store_true', 
                        help='Skip Markdown formatting fixes (for bullet points, etc.)')
    return parser.parse_args()


def main():
    """Main entry point for the command-line interface."""
    args = parse_arguments()
    
    # Check if input file exists
    if not os.path.exists(args.markdown_file):
        print(f"Error: File not found: {args.markdown_file}")
        sys.exit(1)
    
    # Check for pandoc and other dependencies
    check_dependencies()
    
    # Convert markdown to specified format
    output_file = convert_markdown(args)
    
    # Send to Kindle unless --no-send flag is used
    if not args.no_send:
        send_to_kindle(output_file, args)
    
    print("Done!")


if __name__ == "__main__":
    main()