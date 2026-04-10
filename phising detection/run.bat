@echo off
echo.
echo ========================================
echo PhishGuard - Phishing Detection Tool
echo ========================================
echo.

REM Check if Python virtual environment exists
if not exist ".venv" (
    echo Creating Python virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install required packages if needed
echo Checking dependencies...
pip install -r requirements.txt -q

REM Run the Flask application
echo.
echo ========================================
echo Starting PhishGuard...
echo ========================================
echo.
echo The application is starting on:
echo   - Local: http://localhost:5000
echo   - Network: http://0.0.0.0:5000
echo.
echo Press CTRL+C to stop the server.
echo.

python app.py

pause
