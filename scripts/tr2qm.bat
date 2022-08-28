cd "%~dp0..\translations"
call conda activate pyqt
@echo on
qt5-tools lrelease eng-es.ts eng-es.qm
call conda deactivate
cd "%~dp0"
@echo off
echo Done