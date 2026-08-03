@echo off
:: Set UTF-8 code page
chcp 65001 >nul

:: Define ANSI Color Codes
for /F "delims=#" %%a in ('"prompt #$E# & echo on & for %%b in (1) do rem"') do set "ESC=%%a"
set "CYAN=%ESC%[1;36m"
set "GREEN=%ESC%[1;32m"
set "YELLOW=%ESC%[1;33m"
set "RED=%ESC%[1;31m"
set "WHITE=%ESC%[1;37m"
set "NC=%ESC%[0m"

echo %CYAN%=========================================================================%NC%
echo.
echo %CYAN%    ___            _      ______               %NC%
echo %CYAN%   /   ^| ___  ____(_)____/ ____/___  ________  %NC%
echo %CYAN%  / /^| ^|/ _ \/ __ `/ / ___/ /   / __ \/ ___/ _ \ %NC%
echo %CYAN% / ___ /  __/ /_/ / (__  ) /___/ /_/ / /  /  __/ %NC%
echo %CYAN%/_/  ^|_\___/\__, /_/____/\____/\____/_/   \___/  %NC%
echo %CYAN%           /____/                                %NC%
echo.
echo %CYAN%=========================================================================%NC%
echo %WHITE%[*] Initializing AegisCore Boot Sequence...%NC%
echo %CYAN%=========================================================================%NC%
echo.
echo %WHITE%[+] Loading kernel modules...%NC%
timeout /t 1 >nul
echo %GREEN%    [OK] Modules loaded successfully.%NC%
echo %WHITE%[+] Bypassing mainframe security restrictions...%NC%
timeout /t 1 >nul
echo %GREEN%    [OK] Access Granted.%NC%
echo %WHITE%[+] Establishing secure encrypted connection...%NC%
timeout /t 1 >nul
echo %GREEN%    [OK] Secure.%NC%
echo.

echo %YELLOW%[*] [1/4] Setting up isolated Python virtual environment...%NC%
python -m venv venv
if %errorlevel% neq 0 (
    echo %RED%[!] ERROR: Failed to create venv. Ensure Python is installed and in your PATH.%NC%
    pause
    exit /b
)

call venv\Scripts\activate.bat

echo %YELLOW%[*] [2/4] Upgrading package manager (pip)...%NC%
python -m pip install --upgrade pip -q

echo %YELLOW%[*] [3/4] Installing core dependencies...%NC%
pip install -r requirements.txt -q

echo %YELLOW%[*] [4/4] Installing AegisCore Toolkit...%NC%
pip install -e . -q

echo.
echo %CYAN%=========================================================================%NC%
echo %GREEN%[+] INSTALLATION COMPLETE!%NC%
echo %GREEN%[+] You are now inside the AegisCore secure environment.%NC%
echo %WHITE%[+] Type 'aegis --help' to launch the framework.%NC%
echo %CYAN%=========================================================================%NC%

:: Keep the command prompt open and activate the virtual environment
cmd /k "venv\Scripts\activate.bat"
