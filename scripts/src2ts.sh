#!/bin/bash

# Activate the conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate mp3-autotagger

# Generate .ts file
pylupdate5  mp3_autotagger/gui/*.py mp3_autotagger/utils/*.py -ts translations/eng-es.ts
