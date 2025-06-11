#!/bin/bash

# Activate the Conda environment
source $(conda info --base)/etc/profile.d/conda.sh
conda activate mp3-autotagger

# Generate .qm from .ts file
qt5-tools lrelease mp3_autotagger/translations/eng-es.ts -qm mp3_autotagger/translations/eng-es.qm
