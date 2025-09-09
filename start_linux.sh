#!/bin/bash
# Start AutoClicker on Linux

# Change to src directory relative to this script
cd "$(dirname "$0")/src" || exit

echo "Starting AutoClicker..."
python3 main.py

echo
read -p "Press [Enter] to exit..."
