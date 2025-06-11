#!/bin/bash

# Activate the Conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate mp3-autotagger

# Generate .ts file
pylupdate5  mp3_autotagger/**/*.py -ts mp3_autotagger/translations/eng-es.ts
