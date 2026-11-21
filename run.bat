@echo off
REM ==== Starts the FINAL Voice AI Coding CLI (Phase 2) ====
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
    echo Please double-click setup.bat first.
    pause
    exit /b 1
)
".venv\Scripts\python.exe" main.py
pause
