conda create -y -n mp3-autotagger python=3.10.12 --no-default-packages
call conda activate mp3-autotagger
call conda install -y ffmpeg
python -m pip install --upgrade pip
pip install mp3-autotagger
call conda deactivate
