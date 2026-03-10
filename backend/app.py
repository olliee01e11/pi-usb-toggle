#!/usr/bin/env python3
"""
Raspberry Pi 4B USB Control API
Manages USB hub power on/off via uhubctl
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import json
from pathlib import Path
import re

app = Flask(__name__)
CORS(app)

# Raspberry Pi 4B hardware quirk: 
# All 4 USB ports (2.0 and 3.0) share the same power rail.
# To cut power, we must turn off BOTH the USB 2.0 hub (1-1) and USB 3.0 hub (2).
# They cannot be controlled individually for power.
USB_DEVICES = {
    "all_ports": {"hubs": ["1-1", "2"], "name": "All USB Ports (Pi 4B)"}
}

def get_usb_status(device_id):
    """Get USB hub power status using uhubctl"""
    try:
        device = USB_DEVICES.get(device_id)
        if not device:
            return None
        
        # Check hub "1" (root hub) because it is always present
        # When we cut VBUS power, we turn off hub 1 port 1.
        result = subprocess.run(
            ["sudo", "-n", "uhubctl", "-l", "1"],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return "error"
        
        output = result.stdout
        port_lines = [line.strip() for line in output.split('\n') if line.strip().startswith('Port')]
        
        if not port_lines:
            return "error"
        
        # Check if ANY port is powered off
        for port_line in port_lines:
            if "0000 off" in port_line or "0080 off" in port_line:
                return "off"
        
        return "on"
    except subprocess.TimeoutExpired:
        return "error"
    except Exception as e:
        return "error"

def set_usb_power(device_id, state):
    """Enable/disable USB hubs via uhubctl"""
    try:
        device = USB_DEVICES.get(device_id)
        if not device:
            return False, "Device not found"
        
        # Pi 4B requires a specific sequence to toggle VBUS power
        success = True
        
        if state:
            # Turn ON sequence
            # 1. Turn on hub 1 (root hub)
            # 2. Turn on hub 2 (USB 3.0)
            # 3. Wait a moment then ensure hub 1-1 (USB 2.0) is on
            commands = [
                ["sudo", "-n", "uhubctl", "-l", "1", "-a", "on"],
                ["sudo", "-n", "uhubctl", "-l", "2", "-a", "on"]
            ]
            for cmd in commands:
                subprocess.run(cmd, capture_output=True, timeout=5)
            
            # Hub 1-1 usually comes up automatically after hub 1, but just to be sure:
            subprocess.run(["sudo", "-n", "uhubctl", "-l", "1-1", "-a", "on"], capture_output=True, timeout=5)
            
        else:
            # Turn OFF sequence
            # Turn off 2, 1-1, and 1 to guarantee VBUS goes dark
            commands = [
                ["sudo", "-n", "uhubctl", "-l", "2", "-a", "off"],
                ["sudo", "-n", "uhubctl", "-l", "1-1", "-a", "off"],
                ["sudo", "-n", "uhubctl", "-l", "1", "-a", "off"]
            ]
            for cmd in commands:
                subprocess.run(cmd, capture_output=True, timeout=5)
        
        return True, f"All USB ports turned {'on' if state else 'off'}"
    
    except subprocess.TimeoutExpired:
        return False, "Control operation timed out"
    except Exception as e:
        return False, f"Control error: {str(e)}"

@app.route('/api/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok", "device": "Raspberry Pi 4B"}), 200

@app.route('/api/usb/devices', methods=['GET'])
def list_devices():
    """List all USB devices"""
    devices = []
    for device_id, info in USB_DEVICES.items():
        status = get_usb_status(device_id)
        devices.append({
            "id": device_id,
            "name": info["name"],
            "status": status
        })
    return jsonify(devices), 200

@app.route('/api/usb/device/<device_id>', methods=['GET'])
def get_device(device_id):
    """Get specific USB device status"""
    if device_id not in USB_DEVICES:
        return jsonify({"error": "Device not found"}), 404
    
    status = get_usb_status(device_id)
    return jsonify({
        "id": device_id,
        "name": USB_DEVICES[device_id]["name"],
        "status": status
    }), 200

@app.route('/api/usb/device/<device_id>/power', methods=['POST'])
def set_device_power(device_id):
    """Toggle or set USB device power"""
    if device_id not in USB_DEVICES:
        return jsonify({"error": "Device not found"}), 404
    
    data = request.get_json() or {}
    action = data.get('action', 'toggle')
    
    current_status = get_usb_status(device_id)
    
    if action == 'toggle':
        new_state = current_status != "on"
    elif action == 'on':
        new_state = True
    elif action == 'off':
        new_state = False
    else:
        return jsonify({"error": "Invalid action"}), 400
    
    success, message = set_usb_power(device_id, new_state)
    
    if success:
        return jsonify({
            "id": device_id,
            "status": "on" if new_state else "off",
            "message": message
        }), 200
    else:
        return jsonify({
            "error": message
        }), 403

@app.route('/api/usb/all/power', methods=['POST'])
def control_all_devices():
    """Control all USB devices at once"""
    data = request.get_json() or {}
    action = data.get('action', 'toggle')
    
    results = []
    for device_id in USB_DEVICES.keys():
        current_status = get_usb_status(device_id)
        
        if action == 'toggle':
            new_state = current_status != "on"
        elif action == 'on':
            new_state = True
        elif action == 'off':
            new_state = False
        else:
            continue
        
        success, message = set_usb_power(device_id, new_state)
        results.append({
            "id": device_id,
            "success": success,
            "status": "on" if new_state else "off",
            "message": message
        })
    
    return jsonify(results), 200

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=False)
