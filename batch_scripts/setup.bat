:: setup.bat - Setup script for the RSA_SHOR_Simulator project
@echo off

REM ---------------------------------------
REM Configuration
REM ---------------------------------------
set "SCRIPT_DIR=%~dp0"
set "VENV_DIR=.venv"
set "REQ_FILE=%SCRIPT_DIR%requirements.txt"
set "BOOTSTRAP_SCRIPT=bootstrap.py"
set "REQUIRED_PACKAGES="


goto :main


REM ==================================================
REM Step 1 - Start
REM ==================================================
:preamble
echo [INFO] Starting setup...
echo [INFO] Script directory: %SCRIPT_DIR%
exit /b 0


REM ==================================================
REM Step 2 - Check Python
REM ==================================================
:check_python

py -3 --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=py -3"
    exit /b 0
)

python --version >nul 2>&1
if %errorlevel% equ 0 (
    set "PYTHON_CMD=python"
    exit /b 0
)

echo [ERROR] Python not found.
echo Install Python 3 and ensure it is in PATH.
exit /b 1


REM ==================================================
REM Step 3 - Validate Python
REM ==================================================
:select_python

echo [INFO] Using %PYTHON_CMD%
%PYTHON_CMD% --version
if %errorlevel% neq 0 (
    echo [ERROR] Python invocation failed.
    exit /b 1
)

exit /b 0


REM ==================================================
REM Step 4 - Ensure venv
REM ==================================================
:check_environment

if exist "%VENV_DIR%\Scripts\python.exe" (
    echo [INFO] venv already exists
    exit /b 0
)

echo [INFO] Creating venv...
%PYTHON_CMD% -m venv "%VENV_DIR%"
if %errorlevel% neq 0 (
    echo [ERROR] venv creation failed
    exit /b 1
)

exit /b 0


REM ==================================================
REM Step 5 - Activate venv
REM ==================================================
:activate_environment

if not exist "%VENV_DIR%\Scripts\activate.bat" (
    echo [ERROR] activate script missing
    exit /b 1
)

call "%VENV_DIR%\Scripts\activate.bat"
if %errorlevel% neq 0 (
    echo [ERROR] activation failed
    exit /b 1
)

echo [INFO] venv activated
exit /b 0


REM ==================================================
REM Step 6 - Upgrade pip
REM ==================================================
:upgrade_pip

%PYTHON_CMD% -m pip install --upgrade pip
if %errorlevel% neq 0 (
    echo [ERROR] pip upgrade failed
    exit /b 1
)

exit /b 0


REM ==================================================
REM Step 7 - Install deps
REM ==================================================
:install_dependencies

if exist "%REQ_FILE%" (
    echo [INFO] Installing from %REQ_FILE%
    %PYTHON_CMD% -m pip install -r "%REQ_FILE%"
    if %errorlevel% neq 0 exit /b 1
    exit /b 0
)

REM ==================================================
REM Step 8 - Bootstrap
REM ==================================================
:run_bootstrap

if not exist "%BOOTSTRAP_SCRIPT%" (
    echo [INFO] No bootstrap script
    exit /b 0
)

%PYTHON_CMD% "%BOOTSTRAP_SCRIPT%"
if %errorlevel% neq 0 exit /b 1

exit /b 0


REM ==================================================
REM Step 10 - Finalize
REM ==================================================
:finalize_setup

echo [INFO] Setup complete
exit /b 0


:fail
echo [ERROR] Setup failed
endlocal
exit /b 1

REM ==================================================
REM MAIN FLOW
REM ==================================================
:main

call :preamble || goto :fail
call :check_python || goto :fail
call :select_python || goto :fail
call :check_environment || goto :fail
call :activate_environment || goto :fail
call :upgrade_pip || goto :fail
call :install_dependencies || goto :fail
call :run_bootstrap || goto :fail
call :finalize_setup || goto :fail

:eof
echo [INFO] Script execution finished
pause
exit /b 0