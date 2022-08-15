cd %~dp0..
call conda activate pyqt
@echo on
pyuic5 gui\main_window.ui -o src\gui_main_window.py
call conda deactivate
cd %~dp0
@echo off
echo Done