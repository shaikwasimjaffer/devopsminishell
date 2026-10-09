@echo off
setlocal
REM ==============================================================================
REM Quick Launch Script for DevOps Mini Shell (Windows / WSL)
REM ==============================================================================

echo ===================================================
echo   DevOps Mini Shell - Launch Helper (Windows)
echo ===================================================

where wsl.exe >nul 2>&1
if %ERRORLEVEL% NEQ 0 goto try_gcc

echo Detected Windows Subsystem for Linux (WSL).
for /f "delims=" %%I in ('wsl.exe wslpath -a -u "%~dp0."') do set "WSL_DIR=%%I"
echo Launching DevOps Mini Shell inside WSL Ubuntu...
echo.
wsl.exe -d Ubuntu bash -c "cd '%WSL_DIR%' && gcc -Wall -Wextra devops_shell.c -o devops-shell && ./devops-shell"
echo.
pause
goto end

:try_gcc
where gcc.exe >nul 2>&1
if %ERRORLEVEL% NEQ 0 goto no_compiler
echo Compiling natively with Windows GCC...
gcc -Wall -Wextra devops_shell.c -o devops-shell.exe
if %ERRORLEVEL% EQU 0 (
    devops-shell.exe
) else (
    echo Compilation failed.
)
goto end

:no_compiler
echo ERROR: Neither WSL nor native GCC was detected in PATH.
echo Please install GCC or enable WSL to run DevOps Mini Shell.
pause

:end
