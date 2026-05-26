@echo off

IF NOT EXIST .venv (
echo .venv folder not found. Please create it first.
pause
exit /b 1
)

call .\.venv\Scripts\activate.bat

set PYTHON=".venv\Scripts\Python.exe"
echo Using Python from .venv: %PYTHON%

%PYTHON% Launcher.py

echo.
if errorlevel 1 (
    echo Launch unsuccessful. Exiting.
) else (
    echo Launcher exited successfully.
)
pause