#!/bin/bash
tmux new-session -d -s pi-usb

# Backend Window
tmux rename-window -t pi-usb:0 'backend'
tmux send-keys -t pi-usb:0 "cd /home/hpi/pi-usb-toggle && source venv/bin/activate && python3 backend/app.py" C-m

# Frontend Window
tmux new-window -t pi-usb:1 -n 'frontend'
tmux send-keys -t pi-usb:1 "cd /home/hpi/pi-usb-toggle/frontend && npm run dev" C-m

echo "Started in tmux session 'pi-usb'"
echo "View with: tmux attach -t pi-usb"
