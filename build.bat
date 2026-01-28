@echo off
echo Building Albert Sound Controller...
echo.

pyinstaller --onefile --noconsole --icon=assets/icon.ico --name="Albert Sound Controller by Light Intensity" app.py

echo.
echo Done! Your exe is in the "dist" folder.
pause
