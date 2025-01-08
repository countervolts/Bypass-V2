@echo off
setlocal

REM forcecheck 2>nul

if defined forcecheck (
    echo force checking
) else (
    python --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo Python is not installed. Opening python.org...
        start https://www.python.org/
        pause
        exit /b
    ) else (
        echo Python is installed.
    )
    
    pip --version >nul 2>&1
    if %errorlevel% neq 0 (
        echo pip is not installed. Please install pip and try again.
        pause
        exit /b
    ) else (
        echo pip is installed.
    )
)

echo Press Enter to install getmac and run main.py...
pause >nul

echo Installing getmac...
python -m pip install getmac -q
echo getmac installation completed.

echo Running main.py...
python main.py
echo main.py has finished executing.

endlocal
exit
