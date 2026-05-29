@echo off

pip install pyinstaller
pip install pillow

pyinstaller ^
--distpath %CD%\.. ^
--onefile ^
--add-data "%CD%\..\content;content" ^
--windowed ^
--clean ^
--optimize 2 ^
--icon %CD%\..\content\icon.png ^
--version-file version.txt ^
%CD%\..\main.py

del %CD%\..\PyMaker.exe
ren %CD%\..\main.exe PyMaker.exe
rmdir /s /q build

pause
