# Pi USB Toggle - Command Reference

## Quick Commands

### Start Backend
```bash
cd /home/hpi/pi-usb-toggle && sudo bash start-backend.sh
```

### Start Frontend
```bash
cd /home/hpi/pi-usb-toggle/frontend && bash start-frontend.sh
```

### Test API
```bash
cd /home/hpi/pi-usb-toggle && bash test-api.sh
```

## API Endpoints

### Health Check
```bash
curl http://localhost:5000/api/health
```

### List All USB Devices
```bash
curl http://localhost:5000/api/usb/devices
```

### Get Specific Device Status
```bash
curl http://localhost:5000/api/usb/device/usb1
curl http://localhost:5000/api/usb/device/usb2
```

### Toggle USB Device Power
```bash
# Toggle (switch on/off)
curl -X POST http://localhost:5000/api/usb/device/usb1/power \
  -H "Content-Type: application/json" \
  -d '{"action": "toggle"}'

# Turn On
curl -X POST http://localhost:5000/api/usb/device/usb1/power \
  -H "Content-Type: application/json" \
  -d '{"action": "on"}'

# Turn Off
curl -X POST http://localhost:5000/api/usb/device/usb1/power \
  -H "Content-Type: application/json" \
  -d '{"action": "off"}'
```

### Control All USB Devices
```bash
# Turn all on
curl -X POST http://localhost:5000/api/usb/all/power \
  -H "Content-Type: application/json" \
  -d '{"action": "on"}'

# Turn all off
curl -X POST http://localhost:5000/api/usb/all/power \
  -H "Content-Type: application/json" \
  -d '{"action": "off"}'
```

## Device IDs

- `usb1` - USB 2.0 Hub (Top ports)
- `usb2` - USB 3.0 Hub (Bottom ports)

## Python Environment

### Activate Virtual Environment
```bash
cd /home/hpi/pi-usb-toggle
source venv/bin/activate
```

### Deactivate Virtual Environment
```bash
deactivate
```

### Run Backend Manually
```bash
cd /home/hpi/pi-usb-toggle
source venv/bin/activate
sudo python3 backend/app.py
```

### Check Installed Packages
```bash
source venv/bin/activate
pip list
```

## Frontend Commands

### Install Dependencies
```bash
cd /home/hpi/pi-usb-toggle/frontend
npm install
```

### Start Development Server
```bash
cd /home/hpi/pi-usb-toggle/frontend
npm run dev
```

### Build for Production
```bash
cd /home/hpi/pi-usb-toggle/frontend
npm run build
```

## Troubleshooting Commands

### Check Port Usage
```bash
# Check port 5000 (backend)
lsof -i :5000

# Check port 3000 (frontend)
lsof -i :3000
```

### Kill Process on Port
```bash
# Kill process on port 5000
kill -9 $(lsof -t -i:5000)

# Kill process on port 3000
kill -9 $(lsof -t -i:3000)
```

### Check Node/npm Versions
```bash
node --version
npm --version
```

### Check Python Version
```bash
python3 --version
```

### Reinstall Frontend Dependencies
```bash
cd /home/hpi/pi-usb-toggle/frontend
rm -rf node_modules package-lock.json
npm install
```

### Reinstall Backend Dependencies
```bash
cd /home/hpi/pi-usb-toggle
source venv/bin/activate
pip install --upgrade pip
pip install -r backend/requirements.txt
```

## File Locations

```
/home/hpi/pi-usb-toggle/
├── backend/app.py                    # Main API file
├── frontend/src/App.jsx              # Main React component
├── venv/                             # Python environment
├── frontend/node_modules/            # npm packages
└── .git/                             # Git repository
```

## Quick Status Check

```bash
cd /home/hpi/pi-usb-toggle

# Check Python
source venv/bin/activate
python3 -c "import flask; print('Flask OK')"

# Check npm
cd frontend
npm list --depth=0

# Check git
git status
git log --oneline
```

## Environment Variables

If needed for custom configuration:

```bash
export FLASK_ENV=development
export FLASK_APP=backend/app.py
export API_HOST=0.0.0.0
export API_PORT=5000
```

## Further Help

- **QUICKSTART.md** - Get started quickly
- **README.md** - Complete documentation
- **SETUP_COMPLETE.md** - Detailed setup info
- API running on **http://localhost:5000**
- Frontend running on **http://localhost:3000**

---

Keep this handy for quick reference! 🚀
