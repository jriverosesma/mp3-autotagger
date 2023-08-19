#!/bin/bash

# Create the conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda create -y -n mp3-autotagger python=3.10.12 --no-default-packages

# Activate conda environment
conda activate mp3-autotagger

# Install required packages
conda install -y ffmpeg
python -m pip install --upgrade pip
pip install mp3-autotagger

# Deactivate the conda environment
conda deactivate
