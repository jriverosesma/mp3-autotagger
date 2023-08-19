#!/bin/bash

# Activate the conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate mp3-autotagger

# Convert the UI file to a Python file
pyuic5 gui/main_window.ui -o mp3_autotagger/gui/ui.py

# Deactivate the conda environment
conda deactivate
