#!/bin/bash

# Launch Pi USB Toggle in tmux with backend and frontend

SESSION_NAME="pi-usb-toggle"
REPO_PATH="/home/hpi/pi-usb-toggle"

echo "🍓 Starting Pi USB Toggle in tmux..."
echo ""

# Check if tmux session already exists
if tmux has-session -t $SESSION_NAME 2>/dev/null; then
    echo "⚠️  Session '$SESSION_NAME' already exists"
    echo "Attaching to existing session..."
    sleep 1
    tmux attach-session -t $SESSION_NAME
    exit 0
fi

# Create new tmux session with 2 windows
tmux new-session -d -s $SESSION_NAME -x 200 -y 50

# Window 0: Backend API
tmux rename-window -t $SESSION_NAME:0 "backend"
tmux send-keys -t $SESSION_NAME:backend "cd $REPO_PATH && source venv/bin/activate && echo '🍓 Pi USB Toggle - Backend API' && echo '=============================' && echo '' && echo '▶️  Starting API server (port 5000)...' && echo '📝 Press Ctrl+C to stop' && echo '' && sudo python3 backend/app.py" Enter
sleep 2

# Window 1: Frontend
tmux new-window -t $SESSION_NAME:1 -n "frontend"
tmux send-keys -t $SESSION_NAME:frontend "cd $REPO_PATH/frontend && echo '🍓 Pi USB Toggle - Frontend Dev Server' && echo '=======================================' && echo '' && echo '▶️  Starting dev server (port 3000)...' && echo '🌐 Access from any device:' && echo '   http://$(hostname -I | awk '{print \$1}'):3000' && echo '📝 Press Ctrl+C to stop' && echo '' && npm run dev" Enter
sleep 3

# Display info
clear
cat << 'EOF'

╔════════════════════════════════════════════════════════════════════════════╗
║         🍓 PI USB TOGGLE - RUNNING IN TMUX ✅                             ║
╚════════════════════════════════════════════════════════════════════════════╝

🎮 TMUX SESSION: pi-usb-toggle

Windows:
  • Window 0: backend  → Backend API (port 5000)
  • Window 1: frontend → Frontend UI (port 3000, open to all IPs)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🌐 ACCESS FROM EXTERNAL DEVICES:

  Get your Pi's IP address:
    hostname -I

  Then open in browser:
    http://<Pi-IP>:3000

  Example: http://192.168.1.100:3000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 TMUX COMMANDS:

  Navigate between windows:
    • Ctrl+B, N = Next window
    • Ctrl+B, P = Previous window
    • Ctrl+B, 0 = Backend window
    • Ctrl+B, 1 = Frontend window

  Stop/Kill the session:
    • tmux kill-session -t pi-usb-toggle

  Reattach to session:
    • tmux attach-session -t pi-usb-toggle

  View all sessions:
    • tmux list-sessions

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✅ Both services are starting now!

Press a key to attach to the tmux session...

EOF

read -p ""

# Attach to the session
tmux attach-session -t $SESSION_NAME
