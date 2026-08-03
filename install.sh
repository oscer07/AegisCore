#!/bin/bash
# ANSI Color Codes
CYAN='\033[1;36m'
GREEN='\033[1;32m'
YELLOW='\033[1;33m'
RED='\033[1;31m'
WHITE='\033[1;37m'
NC='\033[0m' # No Color

echo -e "${CYAN}=========================================================================${NC}"
echo -e "${CYAN}    █████╗ ███████╗ ██████╗ ██╗███████╗ ██████╗ ██████╗ ██████╗ ███████╗${NC}"
echo -e "${CYAN}   ██╔══██╗██╔════╝██╔════╝ ██║██╔════╝██╔════╝██╔═══██╗██╔══██╗██╔════╝${NC}"
echo -e "${CYAN}   ███████║█████╗  ██║  ███╗██║███████╗██║     ██║   ██║██████╔╝█████╗  ${NC}"
echo -e "${CYAN}   ██╔══██║██╔══╝  ██║   ██║██║╚════██║██║     ██║   ██║██╔══██╗██╔══╝  ${NC}"
echo -e "${CYAN}   ██║  ██║███████╗╚██████╔╝██║███████║╚██████╗╚██████╔╝██║  ██║███████╗${NC}"
echo -e "${CYAN}   ╚═╝  ╚═╝╚══════╝ ╚═════╝ ╚═╝╚══════╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝${NC}"
echo -e "${CYAN}=========================================================================${NC}"
echo -e "${WHITE}[*] Initializing AegisCore Enterprise Installer for Linux/Termux...${NC}"
echo -e "${CYAN}=========================================================================${NC}\n"

# Function to detect the package manager
install_dependencies() {
    echo -e "${YELLOW}[*] [1/4] Checking system dependencies...${NC}"
    if [ -n "$PREFIX" ] && [ -d "$PREFIX/bin" ]; then
        echo -e "${WHITE}    Termux environment detected. Installing packages...${NC}"
        pkg update -y >/dev/null 2>&1
        pkg install -y python python-pip rust binutils libffi openssl libjpeg-turbo libcrypt clang make >/dev/null 2>&1
    elif command -v apt &> /dev/null; then
        echo -e "${WHITE}    Debian/Ubuntu detected. Installing packages...${NC}"
        sudo apt update >/dev/null 2>&1
        sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential libffi-dev libssl-dev libjpeg-dev zlib1g-dev >/dev/null 2>&1
    elif command -v pacman &> /dev/null; then
        echo -e "${WHITE}    Arch Linux detected. Installing packages...${NC}"
        sudo pacman -Syu --noconfirm python python-pip python-virtualenv base-devel libffi openssl libjpeg-turbo zlib >/dev/null 2>&1
    elif command -v dnf &> /dev/null; then
        echo -e "${WHITE}    Fedora/RedHat detected. Installing packages...${NC}"
        sudo dnf install -y python3 python3-pip python3-devel gcc libffi-devel openssl-devel libjpeg-devel zlib-devel >/dev/null 2>&1
    else
        echo -e "${RED}[-] Could not automatically detect package manager. Proceeding anyway...${NC}"
    fi
}

install_dependencies

echo -e "${YELLOW}[*] [2/4] Setting up Python virtual environment...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_CMD="python3"
else
    PYTHON_CMD="python"
fi

$PYTHON_CMD -m venv venv

if [ -f "venv/bin/activate" ]; then
    source venv/bin/activate
else
    echo -e "${RED}[!] Failed to create virtual environment.${NC}"
fi

echo -e "${YELLOW}[*] [3/4] Upgrading pip & installing dependencies...${NC}"
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo -e "${YELLOW}[*] [4/4] Installing AegisCore package...${NC}"
pip install -e . -q

echo -e "\n${CYAN}=========================================================================${NC}"
echo -e "${GREEN}[+] INSTALLATION COMPLETE!${NC}"
echo -e "${GREEN}[+] You are now inside the AegisCore secure environment.${NC}"
echo -e "${WHITE}[+] Type 'aegis --help' to launch the framework.${NC}"
echo -e "${CYAN}=========================================================================${NC}\n"

# Drop the user into an interactive bash shell with the virtual environment activated
bash --rcfile venv/bin/activate
