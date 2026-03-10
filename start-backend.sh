#!/bin/bash

# Start Pi USB Toggle Backend API

cd "$(dirname "$0")"

# Check for sudo
if [[ $EUID -ne 0 ]]; then
    echo "❌ Error: Backend needs root for USB control"
    echo "Run: sudo bash start-backend.sh"
    exit 1
fi

# Activate venv and start
echo "🍓 Pi USB Toggle - Backend API"
echo "=============================="
echo ""

source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""
echo "▶️  Starting API server (port 5000)..."
echo "📝 Press Ctrl+C to stop"
echo ""

python3 backend/app.py
