# Quick Start Guide

## Prerequisites
- Python 3.x ✅
- Node.js v20+ ✅
- npm ✅

## Setup (One-time only)

```bash
cd /home/hpi/pi-usb-toggle
sudo bash setup.sh
```

This will:
1. Create Python virtual environment
2. Install Flask & Flask-CORS
3. Install React, Vite, and frontend deps

## Running the Application

### Option 1: Two Terminal Windows (Recommended)

**Terminal 1 - Backend API:**
```bash
cd /home/hpi/pi-usb-toggle
sudo bash start-backend.sh
```

You should see:
```
🍓 Pi USB Toggle - Backend API
============================
✅ Virtual environment activated
▶️  Starting API server (port 5000)...
```

**Terminal 2 - Frontend Dev Server:**
```bash
cd /home/hpi/pi-usb-toggle/frontend
bash start-frontend.sh
```

You should see:
```
🍓 Pi USB Toggle - Frontend Dev Server
▶️  Starting dev server (port 3000)...
🌐 Open: http://localhost:3000
```

### Option 2: Manual Commands

**Backend:**
```bash
cd /home/hpi/pi-usb-toggle
source venv/bin/activate
sudo python3 backend/app.py
```

**Frontend:**
```bash
cd /home/hpi/pi-usb-toggle/frontend
npm run dev
```

## Access the App

Open your browser:
```
http://localhost:3000
```

## API Testing (Optional)

Test the API endpoints:

```bash
# Get USB device list
curl http://localhost:5000/api/usb/devices

# Toggle USB 2.0 hub
curl -X POST http://localhost:5000/api/usb/device/usb1/power \
  -H "Content-Type: application/json" \
  -d '{"action": "toggle"}'
```

## Troubleshooting

### Port Already in Use
```bash
# Find what's using port 5000 or 3000
lsof -i :5000
lsof -i :3000

# Kill if needed
kill -9 <PID>
```

### ModuleNotFoundError
Make sure venv is activated:
```bash
source venv/bin/activate
```

### Permission Denied
Backend requires sudo:
```bash
sudo bash start-backend.sh
```

## File Structure

```
pi-usb-toggle/
├── venv/                   # Python virtual environment (auto-created)
├── backend/
│   ├── app.py             # Flask API
│   └── requirements.txt    # Python deps
├── frontend/
│   ├── src/               # React components
│   ├── node_modules/      # npm packages (auto-created)
│   └── package.json       # Frontend deps
├── start-backend.sh       # Quick start script
├── setup.sh               # Installation script
└── README.md              # Full documentation
```

## Stop the Application

Press **Ctrl+C** in each terminal window to stop.

---

Need help? Check the main README.md for more details!
