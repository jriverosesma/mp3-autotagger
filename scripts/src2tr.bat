cd "%~dp0..\translations"
call conda activate pyqt
@echo on
pylupdate5 ..\src\main.py ..\src\utils.py ..\src\ui_main_window.py -ts eng-es.ts
call conda deactivate
cd "%~dp0"
@echo off
echo Done