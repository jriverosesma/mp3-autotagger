cd "%~dp0.."
conda create -y -p .venv python=3.11.4 --no-default-packages
call conda activate "%~dp0..\.venv"
call conda install ffmpeg
python -m pip install --upgrade pip
pip install .
call conda deactivate
cd "%~dp0.."
