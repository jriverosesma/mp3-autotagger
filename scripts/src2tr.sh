#!/bin/bash

# Activate the conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate mp3-autotagger

# Generate .ts file
pylupdate5 mp3_autotagger/main.py mp3_autotagger/utils.py mp3_autotagger/ui_main_window.py -ts translations/eng-es.ts

# Deactivate the conda environment
conda deactivate
