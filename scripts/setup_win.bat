cd "%~dp0.."
echo y | conda env create -p .venv python=3.11.4
call conda activate "%~dp0..\.venv"
python -m pip install --upgrade pip
pip install .
python scripts\fixes.py
python -m unittest discover -s tests
call conda deactivate
cd "%~dp0.."
