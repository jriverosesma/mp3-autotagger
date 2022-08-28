cd "%~dp0.."
call conda activate "%~dp0..\.venv"
.venv\python -m src.main
call conda deactivate
cd "%~dp0.."