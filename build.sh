#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status

# Update package lists and install system dependencies
apt-get update && apt-get install -y build-essential python3-dev python3-pip

# Upgrade pip, setuptools, and wheel
pip install --no-cache-dir --upgrade pip setuptools wheel

# Install Python dependencies from requirements.txt
if [ -f "requirements.txt" ]; then
    pip install --no-cache-dir -r requirements.txt
else
    echo "requirements.txt not found! Skipping dependency installation."
fi

echo "Build script executed successfully."
