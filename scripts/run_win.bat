cd "%~dp0.."
call conda activate "%~dp0..\.venv"
mp3-autotagger
call conda deactivate
cd "%~dp0.."