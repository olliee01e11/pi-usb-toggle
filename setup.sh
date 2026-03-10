#!/bin/bash

# Pi USB Toggle - Helper Script

echo "🍓 Raspberry Pi USB Control Setup"
echo "=================================="

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   echo "⚠️  This script needs to run with sudo for USB control"
   echo "Run: sudo ./setup.sh"
   exit 1
fi

# Install backend dependencies
echo ""
echo "📦 Installing backend dependencies..."
cd backend
pip install -r requirements.txt
cd ..

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "⚠️  Node.js is not installed"
    echo "Please install Node.js first: https://nodejs.org/"
    exit 1
fi

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
echo "  1. Backend: sudo python3 backend/app.py"
echo "  2. Frontend: cd frontend && npm run dev"
echo "  3. Open: http://localhost:3000"
echo ""
