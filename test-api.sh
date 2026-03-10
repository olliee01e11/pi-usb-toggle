#!/bin/bash

# Test Pi USB Toggle API

API_URL="http://localhost:5000"

echo "🧪 Testing Pi USB Toggle API"
echo "============================"
echo ""

# Check if API is running
echo "1️⃣  Health Check..."
RESPONSE=$(curl -s "${API_URL}/api/health")
if echo "$RESPONSE" | grep -q '"status"'; then
    echo "✅ API is running"
    echo "   $RESPONSE"
else
    echo "❌ API is not running"
    echo "   Make sure to run: sudo bash start-backend.sh"
    exit 1
fi

echo ""
echo "2️⃣  List USB Devices..."
curl -s "${API_URL}/api/usb/devices" | jq . 2>/dev/null || curl -s "${API_URL}/api/usb/devices"

echo ""
echo "3️⃣  Get USB 2.0 Hub Status..."
curl -s "${API_URL}/api/usb/device/usb1" | jq . 2>/dev/null || curl -s "${API_URL}/api/usb/device/usb1"

echo ""
echo "✅ API Tests Complete!"
echo ""
echo "📝 To toggle USB 2.0 hub:"
echo '   curl -X POST http://localhost:5000/api/usb/device/usb1/power \'
echo '     -H "Content-Type: application/json" \'
echo '     -d '"'"'{"action": "toggle"}'"'"
