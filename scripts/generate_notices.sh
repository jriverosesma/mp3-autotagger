#!/bin/bash

# Activate the conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate mp3-autotagger

# Generate NOTICES file
pip-licenses --output-file=NOTICES

# Deactivate the conda environment
conda deactivate
