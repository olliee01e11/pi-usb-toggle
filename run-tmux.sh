#!/bin/bash

# Launch Pi USB Toggle in tmux - Full Version

SESSION_NAME="pi-usb-toggle"
REPO_PATH="/home/hpi/pi-usb-toggle"

echo "🍓 Launching Pi USB Toggle in tmux..."
echo ""

# Kill existing session if it exists
tmux kill-session -t $SESSION_NAME 2>/dev/null

# Create new tmux session with backend
tmux new-session -d -s $SESSION_NAME -x 250 -y 50 -c "$REPO_PATH"

# Window 0: Backend
tmux send-keys -t $SESSION_NAME "cd $REPO_PATH && source venv/bin/activate && sudo python3 backend/app.py" Enter

# Wait a bit for backend to start
sleep 2

# Window 1: Frontend
tmux new-window -t $SESSION_NAME -c "$REPO_PATH/frontend"
tmux send-keys -t $SESSION_NAME npm run dev Enter

# Sleep a bit more for frontend to start
sleep 3

# Get the Pi's IP
PI_IP=$(hostname -I | awk '{print $1}')

cat << EOF

╔════════════════════════════════════════════════════════════════════════════╗
║         🍓 PI USB TOGGLE - RUNNING IN TMUX ✅                             ║
╚════════════════════════════════════════════════════════════════════════════╝

✅ Both services are now running in the background!

🌐 ACCESS THE APP:

  From this Pi:
    http://localhost:3000

  From another device:
    http://$PI_IP:3000

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📋 TMUX COMMANDS:

  View the session:
    tmux attach-session -t pi-usb-toggle

  List all windows:
    tmux list-windows -t pi-usb-toggle

  Switch to backend window:
    tmux select-window -t pi-usb-toggle:0

  Switch to frontend window:
    tmux select-window -t pi-usb-toggle:1

  Kill the session:
    tmux kill-session -t pi-usb-toggle

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎮 TMUX KEYBOARD SHORTCUTS (once attached):

  Prefix key: Ctrl+B

  Navigation:
    • Ctrl+B, N = Next window
    • Ctrl+B, P = Previous window
    • Ctrl+B, 0 = Go to window 0 (backend)
    • Ctrl+B, 1 = Go to window 1 (frontend)

  Terminal control:
    • Ctrl+B, C = Create new window
    • Ctrl+B, X = Kill window
    • Ctrl+B, D = Detach from session
    • Ctrl+B, [ = Copy/Scroll mode

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ FEATURES:
  • Backend API running on port 5000
  • Frontend UI running on port 3000 (open to all IPs: 0.0.0.0)
  • Both services run in separate tmux windows
  • Easy to switch between windows
  • Easy to stop/restart individual services

📝 TO VIEW LOGS:

  Attach to the session:
    tmux attach-session -t pi-usb-toggle

  This will show you all the output from both services!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Ready to go! Open http://$PI_IP:3000 in your browser! 🚀

EOF
