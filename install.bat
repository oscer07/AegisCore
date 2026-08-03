@echo off
echo [*] Installing AegisCore for Windows...

echo [*] Setting up Python virtual environment...
python -m venv venv
call venv\Scripts\activate.bat

echo [*] Installing requirements and tool...
python -m pip install --upgrade pip
pip install -e .

echo [+] Installation Complete!
echo [+] To run AegisCore, type: venv\Scripts\aegis
