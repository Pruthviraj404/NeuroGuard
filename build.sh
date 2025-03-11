#!/bin/bash

# Install system dependencies
apt-get update && apt-get install -y build-essential python3-dev python3-pip

# Upgrade pip
pip install --upgrade pip setuptools wheel

# Install Python dependencies
pip install -r requirements.txt
