#!/bin/bash

# Create virtual environment named "automate"
python3 -m venv automate

# Activate the virtual environment
source automate/bin/activate

# Install packages from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate

chmod +x run.sh

