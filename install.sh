#!/bin/bash

# ==========================================
# VORTEX-X Automated Installation Script
# Non-Interactive / Auto-Permission Mode
# ==========================================

# Force non-interactive mode to prevent prompt interruptions
export DEBIAN_FRONTEND=noninteractive

echo "[+] Upgrading system packages and repositories..."
if command -v pkg &> /dev/null; then
    pkg update -y && pkg upgrade -y
elif command -v apt-get &> /dev/null; then
    sudo apt-get update -y && sudo apt-get upgrade -y
fi

echo "[+] Installing core dependencies (Python, Git, Pip)..."
if command -v pkg &> /dev/null; then
    pkg install python git -y
elif command -v apt-get &> /dev/null; then
    sudo apt-get install python3 python3-pip git -y
fi

echo "[+] Installing required Python packages..."
pip install --no-cache-dir requests

echo -e "\n[✔] Installation and setup completed successfully!"
echo -e "[⚡] Run the tool using: python vortex_x.py\n"
