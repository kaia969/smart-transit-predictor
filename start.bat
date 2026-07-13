@echo off
title Smart Transit Predictor - Northeast India
echo.
echo ============================================================
echo   Smart Transit Predictor - One-Click Launcher
echo   Double-click this file to start the app!
echo ============================================================
echo.

:: Find Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo.
    echo Download Python from: https://www.python.org/downloads/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)

:: Run the bootstrap script
python "%~dp0start.py"

:: Keep window open if there was an error
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] Something went wrong. See the error above.
    pause
)
