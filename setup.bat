@echo off
REM ==== One-time setup: creates .venv and installs all libraries ====
cd /d "%~dp0"

echo Creating virtual environment...
py -3 -m venv .venv 2>nul || python -m venv .venv
if not exist ".venv\Scripts\python.exe" (
    echo.
    echo ERROR: Python was not found. Install Python 3.10 or newer from python.org
    echo and tick "Add python.exe to PATH". Then double-click setup.bat again.
    pause
    exit /b 1
)

echo Installing libraries...
".venv\Scripts\python.exe" -m pip install --upgrade pip wheel
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 (
    echo.
    echo ERROR: Library installation failed. Check your internet and try again.
    pause
    exit /b 1
)

if not exist ".env" copy ".env.example" ".env" >nul
if not exist "workspace" mkdir workspace

echo.
echo ==========================================================
echo  Setup complete!
echo  NEXT: open the .env file and paste your real OpenAI API key.
echo  Then double-click run.bat
echo ==========================================================
pause
