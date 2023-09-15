#!/bin/bash

# Activate the conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate mp3-autotagger

# Generate .qm from .ts file
qt5-tools lrelease translations/eng-es.ts -qm translations/eng-es.qm
