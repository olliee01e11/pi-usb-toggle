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

# USB hubs controlled by uhubctl
# Format: {device_id: (uhubctl_hub_number, hub_name)}
USB_DEVICES = {
    "usb1": {"hub": "1", "name": "USB 2.0 Hub (Top)"},
    "usb2": {"hub": "2", "name": "USB 3.0 Hub"},
}

def get_usb_status(device_id):
    """Get USB hub power status using uhubctl"""
    try:
        device = USB_DEVICES.get(device_id)
        if not device:
            return None
        
        # Run uhubctl to get hub status
        result = subprocess.run(
            ["sudo", "-n", "uhubctl", "-l", device["hub"]],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode != 0:
            return "error"
        
        # Parse uhubctl output to find port power status
        # Look for "Port X: 02a0 power" (on) or "Port X: 0000 off" (off)
        output = result.stdout
        
        # Extract all port status lines
        port_lines = [line.strip() for line in output.split('\n') if line.strip().startswith('Port')]
        
        if not port_lines:
            return "error"
        
        # Check if ANY port is powered off
        for port_line in port_lines:
            if "0000 off" in port_line:
                return "off"
        
        # All ports are powered on
        return "on"
    except subprocess.TimeoutExpired:
        return "error"
    except Exception as e:
        return "error"

def set_usb_power(device_id, state):
    """Enable/disable USB hub via uhubctl"""
    try:
        device = USB_DEVICES.get(device_id)
        if not device:
            return False, "Device not found"
        
        # Use uhubctl to control power
        action = "on" if state else "off"
        
        result = subprocess.run(
            ["sudo", "-n", "uhubctl", "-l", device["hub"], "-a", action],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            return True, f"Device {device_id} turned {action}"
        else:
            error_msg = result.stderr.strip() if result.stderr else "Unknown error"
            return False, f"Control failed: {error_msg}"
    
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
