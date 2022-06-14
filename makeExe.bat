TITLE Build Executable
set PATH=c:\Python38\;c:\Python38\Lib\site-packages\;c:\Python38\Scripts\;%PATH%
set PYTHONPATH=c:\Python38\Lib\
set PYTHONHOME=c:\Python38\
pyinstaller ^
    --onefile ^
    --noconsole ^
    --distpath bin ^
    --clean ^
    --log-level INFO ^
    --name "CardDAV2MicroSIP Bridge" ^
    --distpath release ^
    bridge.py
pause