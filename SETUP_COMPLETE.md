# Pi USB Toggle - Setup Complete ✅

## What Was Built

A full-stack web application to control Raspberry Pi 4B USB hub power with:

### Backend (Flask REST API)
- **Port:** 5000
- **Dependencies:** Flask 3.0.0, Flask-CORS 4.0.0 ✅
- **Virtual Environment:** `venv/` ✅
- **Features:**
  - Real-time USB device status detection
  - Individual USB port control
  - Bulk operations (toggle all on/off)
  - CORS-enabled for frontend communication

### Frontend (React + Vite)
- **Port:** 3000
- **Dependencies:** React 18.2.0, Vite 5.0.0, Axios, etc. ✅
- **Features:**
  - Modern responsive UI
  - Real-time status polling
  - One-click device control
  - Mobile-friendly design
  - Live error handling

## Project Structure

```
pi-usb-toggle/
├── backend/
│   ├── app.py                    # Flask API server
│   └── requirements.txt          # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React component
│   │   ├── App.css              # Styling
│   │   └── main.jsx             # Entry point
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── start-frontend.sh        # Frontend launcher
├── venv/                         # Python virtual environment
├── setup.sh                      # Installation script
├── start-backend.sh             # Backend launcher
├── test-api.sh                  # API test script
├── QUICKSTART.md                # Quick start guide
├── README.md                    # Full documentation
└── .gitignore
```

## Installation Status

✅ **Python Environment**
- Virtual environment created: `/venv`
- Flask 3.0.0 installed
- Flask-CORS 4.0.0 installed

✅ **Node.js & npm**
- Node.js v20.19.2 installed
- npm 11.11.0 installed
- All 85 npm packages installed
- node_modules present in frontend/

✅ **Git Repository**
- Initialized at `/home/hpi/pi-usb-toggle`
- 2 commits made
- Ready for version control

## How to Run

### Method 1: Two Terminal Windows (Recommended)

**Terminal 1 - Start Backend:**
```bash
cd /home/hpi/pi-usb-toggle
sudo bash start-backend.sh
```

**Terminal 2 - Start Frontend:**
```bash
cd /home/hpi/pi-usb-toggle/frontend
bash start-frontend.sh
```

### Method 2: Manual Commands

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

## Access the Application

1. Start both backend and frontend (see above)
2. Open your browser: **http://localhost:3000**
3. You should see the USB control dashboard

## API Endpoints

### Health Check
```bash
curl http://localhost:5000/api/health
```

### List USB Devices
```bash
curl http://localhost:5000/api/usb/devices
```

### Toggle USB Device
```bash
curl -X POST http://localhost:5000/api/usb/device/usb1/power \
  -H "Content-Type: application/json" \
  -d '{"action": "toggle"}'
```

### Test All Endpoints
```bash
bash test-api.sh
```

## What Each Script Does

| Script | Purpose | Requires Sudo |
|--------|---------|---------------|
| `setup.sh` | First-time setup (venv, deps) | ✅ Yes |
| `start-backend.sh` | Launch Flask API server | ✅ Yes |
| `frontend/start-frontend.sh` | Launch React dev server | ❌ No |
| `test-api.sh` | Test API endpoints | ❌ No |

## Important Notes

⚠️ **Backend requires sudo** for USB device control via sysfs
- USB power control needs root permissions
- Run `start-backend.sh` with sudo
- Or activate venv and run python with sudo

🔧 **Virtual Environment**
- Always activate venv before running Python code
- The startup scripts handle this automatically

🌐 **Frontend Communication**
- Frontend runs on port 3000
- Backend API runs on port 5000
- Vite proxy is configured for development

## Verify Everything Works

```bash
# 1. Check Python packages
cd /home/hpi/pi-usb-toggle
source venv/bin/activate
python3 -c "import flask; print('✅ Flask working')"

# 2. Check npm packages
cd frontend
npm list react react-dom axios vite

# 3. Test API (after starting backend)
bash test-api.sh
```

## Next Steps

1. ✅ Setup complete - both backend and frontend are ready
2. 🚀 **Start the application** using the commands above
3. 🌐 Open http://localhost:3000 in your browser
4. 🎮 Control your Pi's USB ports!

## Troubleshooting

### Backend Won't Start
```bash
# Check if port 5000 is in use
lsof -i :5000
kill -9 <PID>

# Try running with explicit Python path
sudo /usr/bin/python3 backend/app.py
```

### Frontend Won't Start
```bash
# Reinstall dependencies
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

### Permission Denied
```bash
# Make sure scripts are executable
chmod +x start-backend.sh
chmod +x frontend/start-frontend.sh
chmod +x test-api.sh

# Or just use bash
bash start-backend.sh
```

---

**Everything is ready to go! 🚀**

Start with the commands in "How to Run" above.
