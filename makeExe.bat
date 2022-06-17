@echo off
TITLE Build Executable
set PATH=c:\Python38\;c:\Python38\Lib\site-packages\;c:\Python38\Scripts\;%PATH%
set PYTHONPATH=c:\Python38\Lib\
set PYTHONHOME=c:\Python38\
rmdir /Q /S release
pyinstaller ^
    --onefile ^
    --noconsole ^
    --distpath bin ^
    --clean ^
    --log-level INFO ^
    --name bridge ^
    --distpath release ^
    bridge.py
powershell Compress-Archive release\bridge.exe release\bridge.zip
del release\bridge.exe
del /F /Q bridge.spec
rmdir /Q /S __pycache__
rmdir /Q /S build
pause