@echo off
REM AI Mock Interview System - Windows Startup Script

echo.
echo ================================================
echo   AI MOCK INTERVIEW SYSTEM
echo ================================================
echo.

REM Check if .env exists
if not exist .env (
    echo ERROR: .env file not found!
    echo.
    echo Please create a .env file with your API key.
    echo See .env.example for the format.
    echo.
    pause
    exit /b 1
)

echo Starting the application...
echo.
echo The web browser should open automatically.
echo If not, manually open: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server when done.
echo.
echo ================================================
echo.

REM Start the Flask app
python app.py

pause
