@echo off
REM Start AutoClicker on Windows

REM Change directory to src relative to this batch file
cd /d "%~dp0\src"

echo Starting AutoClicker...
py main.py

echo.
echo Press any key to exit...
pause >nul
