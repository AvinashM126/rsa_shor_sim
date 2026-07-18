:: -------------------------------------------------------------------------
:: Batch script to run the setup script and execute the main Python script.
:: Project: RSA and Shor's Algorithm
:: Title: Python implementation of RSA and SHOR
:: File: run.bat
:: Sub files: batch_scripts/setup.bat, batch_scripts/requirements.txt, batch_scripts/bootstrap.py (OPTIONAL)
:: Description: This batch script runs the setup script to create and activate the virtual environment, install dependencies, and execute the main Python script. It ensures that the setup is completed before running the main script.
:: Dependencies: Python 3.x, pip, virtualenv
:: Usage: Double-click the run.bat file or execute it from the command line.
:: Note: Ensure that Python is installed and added to the system PATH before running this script.
:: Author: Avinash M
:: mail: m.avinash@in.bosch.com
:: Last Modified: 18th June 2024
:: -------------------------------------------------------------------------

@echo off

cd /d "%~dp0"

set "ROOT_DIR=%~dp0"

REM ---------------------------------------
REM Configuration
REM ---------------------------------------
set "MAIN_SCRIPT=RSA_SHOR_main.py"
set "PYTHON_CMD=python"

goto :main

:run_setup
echo [INFO] Running setup script...
call "%ROOT_DIR%batch_scripts\setup.bat"
if errorlevel 1 (
    echo [ERROR] Setup failed
    exit /b 1
)
exit /b 0

:check_payload
if not exist "%MAIN_SCRIPT%" (
    echo [INFO] No main script
    exit /b 1
)
exit /b 0

:payload_execution_loop
echo [INFO] Do you want to run the main Python script ? (Y/N)
set /p "RUN_MAIN="
if /i "%RUN_MAIN%"=="Y" (
    %PYTHON_CMD% "%MAIN_SCRIPT%"
    if %errorlevel% neq 0 exit /b 1
    pause
    cls
) else (
    echo [INFO] Skipping main script execution.
    goto :eof
)
goto :payload_execution_loop
exit /b 0

:fail
echo [ERROR] An error occurred
exit /b 1

:main

call :run_setup || goto :fail
call :check_payload || goto :fail
call :payload_execution_loop || goto :fail

:eof
exit /b 0