#!/bin/bash

# Start Pi USB Toggle

echo "🍓 Raspberry Pi USB Control"
echo "============================="
echo ""

# Check for sudo
if [[ $EUID -ne 0 ]]; then
    echo "❌ Error: This must run with sudo"
    echo "Run: sudo bash start.sh"
    exit 1
fi

# Start backend
echo "▶️  Starting API server (port 5000)..."
cd "$(dirname "$0")"
python3 backend/app.py &
API_PID=$!

echo "✅ API running on http://localhost:5000"
echo ""
echo "📝 Frontend setup (in another terminal):"
echo "  cd frontend"
echo "  npm run dev"
echo ""
echo "🌐 Open browser: http://localhost:3000"
echo ""
echo "Press Ctrl+C to stop the API server"
echo ""

wait $API_PID
