# Pi USB Toggle - Tmux Quick Reference

## Quick Access

```bash
# View running services
tmux attach-session -t pi-usb-toggle

# Kill everything
tmux kill-session -t pi-usb-toggle

# Restart everything
bash /home/hpi/pi-usb-toggle/run-tmux.sh
```

## Service URLs

| Service | URL | Notes |
|---------|-----|-------|
| Frontend (local) | http://localhost:3000 | Access from this Pi |
| Frontend (external) | http://192.168.88.7:3000 | Access from any device |
| Backend API | http://localhost:5000/api | Only localhost |
| API Health | http://localhost:5000/api/health | Check if API is running |

## Tmux Window Navigation

**Inside tmux session:**

```
Ctrl+B, N     Next window
Ctrl+B, P     Previous window
Ctrl+B, 0     Go to window 0 (backend)
Ctrl+B, 1     Go to window 1 (frontend)
Ctrl+B, D     Detach from session
Ctrl+B, [     Enter scroll mode (for viewing output)
Ctrl+B, ]     Exit scroll mode
```

## Window Management (from command line)

```bash
# List windows
tmux list-windows -t pi-usb-toggle

# Select specific window
tmux select-window -t pi-usb-toggle:0   # backend
tmux select-window -t pi-usb-toggle:1   # frontend

# Kill specific window
tmux kill-window -t pi-usb-toggle:0

# Create new window
tmux new-window -t pi-usb-toggle -c /path/to/dir
```

## View Logs

```bash
# Attach to session to see live logs
tmux attach-session -t pi-usb-toggle

# Switch between windows to see each service's logs
# Ctrl+B, 0 = backend logs
# Ctrl+B, 1 = frontend logs
```

## Restart Individual Services

**Restart Backend:**
```bash
tmux kill-window -t pi-usb-toggle:0
tmux new-window -t pi-usb-toggle:0 -c /home/hpi/pi-usb-toggle
tmux send-keys -t pi-usb-toggle:0 'source venv/bin/activate && sudo python3 backend/app.py' Enter
```

**Restart Frontend:**
```bash
tmux kill-window -t pi-usb-toggle:1
tmux new-window -t pi-usb-toggle:1 -c /home/hpi/pi-usb-toggle/frontend
tmux send-keys -t pi-usb-toggle:1 'npm run dev' Enter
```

## Debug & Troubleshooting

```bash
# Check if processes are running
ps aux | grep -E 'python|npm'

# Check port usage
lsof -i :5000   # Backend
lsof -i :3000   # Frontend

# View tmux session list
tmux list-sessions

# View detailed window info
tmux list-panes -t pi-usb-toggle -a

# Send command to window without attaching
tmux send-keys -t pi-usb-toggle:0 'your-command' Enter

# Clear window
tmux send-keys -t pi-usb-toggle:0 'clear' Enter
```

## Advanced: Custom Tmux Configuration

Create `~/.tmux.conf` for persistent settings:

```
# Set default terminal
set -g default-terminal "screen-256color"

# Set mouse mode
set -g mouse on

# Increase history
set -g history-limit 10000

# Faster key repeat
set -g repeat-time 300

# Easier prefix key
set -g prefix C-a
unbind C-b
bind C-a send-prefix
```

## Keep Services Running After SSH Disconnect

Since services are in tmux, they'll keep running even if you:
- Close the SSH connection
- Disconnect the terminal
- Log out of the Pi

Just reconnect and run:
```bash
tmux attach-session -t pi-usb-toggle
```

## External Network Access

Your Pi's IP: **192.168.88.7**

Access from any device on the same network:
```
http://192.168.88.7:3000
```

If you need external internet access, consider:
- Port forwarding on your router
- Using a tunneling service (ngrok, Cloudflare Tunnel, etc.)
- VPN access to your home network

---

**All commands can be run from any terminal. The services keep running in the background!**
