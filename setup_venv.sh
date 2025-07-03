#!/bin/bash

# Remove existing virtual environment if it exists
if [ -d ".venv" ]; then
    echo "Removing existing virtual environment..."
    rm -rf .venv
fi

# Create a new virtual environment
echo "Creating virtual environment..."
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Install package in development mode
echo "Installing md2kindle in development mode..."
pip install -e .

echo "Setup complete. Use 'source .venv/bin/activate' to activate the virtual environment."