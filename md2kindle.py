#!/usr/bin/env python3
"""
MD2Kindle - Convert Markdown files to Kindle format and send to device.

This script has been refactored for better maintainability.
The main functionality is now in the md2kindle package.
"""

from md2kindle.cli import main

if __name__ == "__main__":
    main()