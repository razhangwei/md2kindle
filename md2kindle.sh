#!/bin/bash

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Python 3 is required but not installed. Please install Python 3."
    exit 1
fi

# Check if Pandoc is installed
if ! command -v pandoc &> /dev/null; then
    echo "Pandoc is required but not installed. Please install Pandoc from https://pandoc.org/installing.html"
    exit 1
fi

# Get the directory of this script
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

# Check if .env file exists
if [ ! -f "$SCRIPT_DIR/.env" ] && [ ! -f "$HOME/.md2kindle.env" ]; then
    echo "No .env file found. Creating one from template..."
    if [ -f "$SCRIPT_DIR/.env.example" ]; then
        cp "$SCRIPT_DIR/.env.example" "$SCRIPT_DIR/.env"
        echo "Created .env file at $SCRIPT_DIR/.env"
        echo "Please edit this file with your email settings before sending to Kindle."
    else
        echo "No .env.example file found. Please create a .env file manually."
    fi
fi

# Run the Python script with all arguments passed to this shell script
python3 "$SCRIPT_DIR/md2kindle.py" "$@"
