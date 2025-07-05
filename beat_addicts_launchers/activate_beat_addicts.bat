@echo off
echo BEAT ADDICTS - Environment Activator
echo ===================================

REM Check if virtual environment exists in user directory
set VENV_PATH=%USERPROFILE%\beat_addicts_env
if exist "%VENV_PATH%\Scripts\activate.bat" (
    echo Activating virtual environment...
    call "%VENV_PATH%\Scripts\activate.bat"
    echo Installing BEAT ADDICTS dependencies in virtual environment...
    pip install flask==3.0.0 colorama==0.4.6 werkzeug==3.0.1
) else (
    echo No virtual environment found - using system Python with --user
    pip install --user flask==3.0.0 colorama==0.4.6 werkzeug==3.0.1
)

echo Starting BEAT ADDICTS Studio...
cd /d "%~dp0beat_addicts_core"
python run.py

pause
