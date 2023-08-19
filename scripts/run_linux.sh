#!/bin/bash

# Activate the conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate mp3-autotagger

# Run mp3-autotagger
mp3-autotagger

# Deactivate the conda environment
conda deactivate
