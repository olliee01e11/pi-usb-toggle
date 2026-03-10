# Raspberry Pi USB Toggle

A modern web interface to control USB hub power on Raspberry Pi 4B. Toggle individual USB ports or manage all ports simultaneously.

## Features

- **Real-time USB Status**: Monitor USB hub power state in real-time
- **Individual Control**: Toggle each USB port on/off
- **Bulk Actions**: Turn all USB ports on/off at once
- **REST API**: Full control via HTTP endpoints
- **Responsive UI**: Works on desktop and mobile
- **Zero Dependencies**: Pure Python/React implementation

## Hardware Requirements

- Raspberry Pi 4B (ARMv8, 64-bit)
- USB hub with power control support (VIA Labs hub on Pi 4B)

## API Endpoints

### Health Check
```
GET /api/health
```

### List Devices
```
GET /api/usb/devices
```

### Get Device Status
```
GET /api/usb/device/{device_id}
```

### Control Device Power
```
POST /api/usb/device/{device_id}/power
Body: { "action": "toggle" | "on" | "off" }
```

### Control All Devices
```
POST /api/usb/all/power
Body: { "action": "toggle" | "on" | "off" }
```

## Installation

### 1. Clone & Setup
```bash
cd pi-usb-toggle
sudo bash setup.sh
```

### 2. Start Backend (Terminal 1)
```bash
sudo python3 backend/app.py
```

### 3. Start Frontend (Terminal 2)
```bash
cd frontend
npm run dev
```

### 4. Open Browser
```
http://localhost:3000
```

## Usage Examples

### cURL API Commands

```bash
# Get device list
curl http://localhost:5000/api/usb/devices

# Toggle USB 2.0 hub
curl -X POST http://localhost:5000/api/usb/device/usb1/power \
  -H "Content-Type: application/json" \
  -d '{"action": "toggle"}'

# Turn on all devices
curl -X POST http://localhost:5000/api/usb/all/power \
  -H "Content-Type: application/json" \
  -d '{"action": "on"}'
```

### JavaScript

```javascript
const toggleUSB = async (deviceId) => {
  const response = await fetch('http://localhost:5000/api/usb/device/' + deviceId + '/power', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ action: 'toggle' })
  });
  return response.json();
};
```

## Permissions

This tool requires root/sudo access to control USB device power. Options:

### Option 1: Run with sudo (Easiest)
```bash
sudo python3 backend/app.py
```

### Option 2: Configure udev rules (Persistent)
Create `/etc/udev/rules.d/99-usb-control.rules`:
```
SUBSYSTEM=="usb", ACTION=="add", RUN+="/path/to/usb-control.sh"
```

## Directory Structure

```
pi-usb-toggle/
├── backend/
│   ├── app.py              # Flask API server
│   └── requirements.txt     # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx         # React main component
│   │   ├── App.css         # Styling
│   │   └── main.jsx        # React entry point
│   ├── index.html          # HTML template
│   ├── package.json        # Node dependencies
│   └── vite.config.js      # Vite config
├── setup.sh                # Installation script
├── start.sh                # Quick start script
└── README.md               # This file
```

## Troubleshooting

### "Permission denied" Error
- Make sure you're running with `sudo`
- Check USB device paths in `/sys/bus/usb/devices/`

### API Connection Error
- Ensure backend is running: `sudo python3 backend/app.py`
- Check port 5000 is available: `lsof -i :5000`

### Frontend Not Loading
- Install Node dependencies: `npm install`
- Check port 3000 is available: `lsof -i :3000`
- Try: `npm run dev`

### USB Hub Not Found
- Verify Pi 4B USB hub is connected
- Check: `lsusb`
- Review API logs for device detection errors

## Architecture

**Backend (Flask)**
- CORS-enabled REST API
- Direct sysfs USB device control
- Power state monitoring
- Graceful error handling

**Frontend (React + Vite)**
- Real-time device status polling
- Responsive grid layout
- One-click device control
- Mobile-friendly interface

## Notes

- Requires Raspberry Pi OS (Debian-based)
- USB control via sysfs power/control interface
- Some USB hubs may need custom drivers
- VIA Labs hub on Pi 4B is fully supported

## License

MIT
