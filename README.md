<div align="center">
  <h1>🛡️ AegisCore Security Framework</h1>
  <p>
    <b>An Advanced, Modular, and Cross-Platform Cybersecurity Toolkit for Blue & Red Teams.</b>
  </p>
  
  [![Python Version](https://img.shields.io/badge/python-3.8%2B-blue.svg)](https://python.org)
  [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
  [![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20Linux%20%7C%20Termux-lightgrey.svg)](#)
  [![Status](https://img.shields.io/badge/Status-Active-success.svg)](#)

</div>

---

## 📖 Overview

**AegisCore** is a professional-grade, command-line cybersecurity framework built entirely in Python. It consolidates network reconnaissance, web application security auditing, cryptography, and cloud security into one beautiful and extremely fast CLI powered by `Typer`, `Rich`, and `asyncio`.

Whether you are performing a defensive audit (Blue Team) or authorized reconnaissance (Red Team), AegisCore provides the essential tools to secure and test your infrastructure.

> **⚠️ Disclaimer:** This toolkit is strictly for educational purposes, defensive auditing, and authorized security testing. The developers assume no liability and are not responsible for any misuse or damage caused by this program.

---

## ✨ Features & Modules

### 🔍 1. Reconnaissance (`aegis recon`)
- **Port Scanner**: Lightning-fast, asynchronous TCP port scanner.
- **Subdomain Enumerator**: OSINT-based hidden subdomain discovery via Certificate Transparency logs.
- **PCAP Analyzer**: Parse network capture files (`.pcap`) to hunt for plaintext credentials.
- **Banner Grabber**: Identify running services and software versions on open ports.

### 🌐 2. Web Application Security (`aegis web`)
- **Security Headers**: Grade HTTP security headers (HSTS, CSP, X-Frame-Options) instantly.
- **Directory Fuzzer**: Fast, async endpoint discovery tool to find hidden admin panels or backups.
- **Web Scraper**: Crawl targets to extract hidden links and email addresses.

### 🕵️ 3. Defensive Auditing (`aegis audit`)
- **Cloud Security Auditor**: Scan AWS S3 buckets to identify public read exposures without requiring IAM credentials.
- **File Integrity Monitor (FIM)**: Generate SHA-256 baselines of critical directories and detect tampering.
- **Static Code Analyzer**: Scan source code repositories to find leaked hardcoded API keys, secrets, and private keys.

### 🔐 4. Cryptography (`aegis crypto`)
- **Steganography**: Hide (and reveal) secret text data invisibly inside standard image files.
- **Password Auditor**: Securely check passwords against the HaveIBeenPwned database using k-Anonymity.
- **Hash Tools**: Fast generation and offline dictionary-based cracking of MD5, SHA1, and SHA256 hashes.

### ⚡ 5. Automation & Reporting (`aegis automation` / `aegis report`)
- **Orchestrator**: Chain modules together automatically (e.g., Port Scan -> Header Analysis).
- **Report Generator**: Automatically compile findings into a professional, presentation-ready Markdown report.

---

## 🚀 Installation

AegisCore is 100% cross-platform. We provide easy install scripts for Windows, Linux, and Android (Termux).

### Option 1: Linux / Kali / Termux (Android)
We have provided an automated bash script that installs system requirements and sets up the Python environment.
```bash
git clone https://github.com/yourusername/aegiscore.git
cd aegiscore
chmod +x install.sh
./install.sh

# Activate the virtual environment before running:
source venv/bin/activate
```

### Option 2: Windows
Run the included batch file to set up your virtual environment automatically.
```cmd
git clone https://github.com/yourusername/aegiscore.git
cd aegiscore
install.bat

# Activate the virtual environment before running:
venv\Scripts\activate
```

---

## 💻 Usage Examples

Once the virtual environment is activated, the `aegis` command is available globally.

**View all available commands:**
```bash
aegis --help
```

**Perform an asynchronous port scan:**
```bash
aegis recon port-scan 192.168.1.100 --start 1 --end 1024
```

**Analyze Web Security Headers:**
```bash
aegis web headers https://example.com
```

**Find Hidden Subdomains:**
```bash
aegis recon subdomains example.com
```

**Audit an AWS S3 Bucket for public exposure:**
```bash
aegis audit cloud-audit my-company-bucket
```

**Generate a Professional Report:**
```bash
aegis report generate --title "Weekly Audit" --output audit.md
```

---

## 🏗️ Architecture

AegisCore relies on a modern Python stack:
- **[Typer](https://typer.tiangolo.com/)**: For an intuitive, robust CLI interface.
- **[Rich](https://rich.readthedocs.io/)**: For beautiful terminal formatting, tables, and progress bars.
- **[Asyncio / Aiohttp](https://docs.python.org/3/library/asyncio.html)**: For extreme concurrency in network scanning and fuzzing.

## 🤝 Contributing
Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/yourusername/aegiscore/issues).

## 📝 License
This project is [MIT](LICENSE) licensed.
