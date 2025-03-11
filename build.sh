#!/bin/bash

set -e  # Exit if any command fails

# Install required system dependencies
apt-get update && apt-get install -y python3.10 python3.10-dev python3.10-venv python3.10-distutils

# Set Python3.10 as default
update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1

# Upgrade pip and install dependencies
python3.10 -m ensurepip --upgrade
python3.10 -m pip install --upgrade pip setuptools wheel

# Install dependencies
if [ -f "requirements.txt" ]; then
    python3.10 -m pip install --no-cache-dir -r requirements.txt
else
    echo "requirements.txt not found! Skipping dependency installation."
fi

echo "Build script executed successfully."
