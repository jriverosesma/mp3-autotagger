cd %~dp0..
echo y | conda env create -f environment.yml -p .venv
call conda activate %~dp0../.venv 
python scripts\fixes.py
python -m unittest discover -s tests
call conda deactivate