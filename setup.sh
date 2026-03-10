#!/bin/bash

# Pi USB Toggle - Helper Script (Updated)

echo "🍓 Raspberry Pi USB Control Setup"
echo "=================================="

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "⚠️  This script needs to run with sudo for USB control"
   echo "Run: sudo ./setup.sh"
   exit 1
fi

# Setup Python virtual environment
echo ""
echo "📦 Setting up Python virtual environment..."
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt

echo "✅ Python environment ready"

# Install frontend dependencies
echo ""
echo "📦 Installing frontend dependencies..."
cd frontend
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Quick Start:"
echo "  1. Backend: cd /home/hpi/pi-usb-toggle && source venv/bin/activate && sudo python3 backend/app.py"
echo "  2. Frontend (new terminal): cd /home/hpi/pi-usb-toggle/frontend && npm run dev"
echo "  3. Open: http://localhost:3000"
echo ""
