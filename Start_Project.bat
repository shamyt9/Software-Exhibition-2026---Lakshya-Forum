@echo off
REM Cybercrime Project - Auto Startup Script
REM This batch file will set up the environment and run the Flask application

echo.
echo ========================================
echo Cybercrime Management & Digital Investigation System
echo ========================================
echo.

REM Get the directory where this batch file is located
cd /d "%~dp0"

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8+ from https://www.python.org/
    pause
    exit /b 1
)

echo [*] Python found successfully
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [*] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo [+] Virtual environment created
) else (
    echo [*] Virtual environment already exists
)

echo.

REM Activate virtual environment
echo [*] Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo [+] Virtual environment activated
echo.

REM Install requirements
echo [*] Installing dependencies from requirements.txt...
pip install -r requirements.txt
if errorlevel 1 (
    echo WARNING: Some dependencies may have failed to install
    echo Continuing anyway...
)

echo [+] Dependencies installed
echo.

REM Run the Flask application
echo ========================================
echo [*] Starting Flask Application...
echo ========================================
echo.
echo Access the application at: http://localhost:5000
echo Press Ctrl+C to stop the server
echo.

python app.py

REM If script reaches here, application closed or error occurred
echo.
echo Application closed or error occurred.
pause
