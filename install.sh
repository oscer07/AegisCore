#!/bin/bash
echo "[*] Installing AegisCore for Linux / Termux..."

# Check if running in Termux
if [ -n "$PREFIX" ] && [ -d "$PREFIX/bin" ]; then
    echo "[*] Termux environment detected!"
    pkg update -y
    pkg install python python-pip -y
    pkg install libcrypt -y  # Often needed for cryptography package in Termux
else
    echo "[*] Standard Linux environment detected."
fi

echo "[*] Setting up Python virtual environment..."
python -m venv venv
source venv/bin/activate

echo "[*] Installing requirements and tool..."
pip install --upgrade pip
pip install -e .

echo "[+] Installation Complete!"
echo "[+] To run AegisCore, type: source venv/bin/activate && aegis"
