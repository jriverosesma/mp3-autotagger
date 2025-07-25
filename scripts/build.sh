#!/bin/bash

# Activate the Conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate mp3-autotagger

# Build binary distribution
pyinstaller mp3_autotagger.spec
