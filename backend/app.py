#!/usr/bin/env python3
"""
Raspberry Pi 4B USB Control API
Manages USB hub power on/off via sysfs
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import subprocess
import os
import json
from pathlib import Path

app = Flask(__name__)
CORS(app)

# USB device paths (Pi 4B USB hub)
USB_DEVICES = {
    "usb1": {"path": "/sys/bus/usb/devices/usb1", "name": "USB 2.0 Hub (Top)"},
    "usb2": {"path": "/sys/bus/usb/devices/usb2", "name": "USB 3.0 Hub"},
}

def get_usb_status(device_id):
    """Get USB device power status"""
    try:
        device = USB_DEVICES.get(device_id)
        if not device:
            return None
        
        power_path = os.path.join(device["path"], "power/control")
        if os.path.exists(power_path):
            with open(power_path, 'r') as f:
                status = f.read().strip()
                return status
        
        # Check if device is bound
        driver_path = os.path.join(device["path"], "driver")
        is_bound = os.path.exists(driver_path)
        
        return "on" if is_bound else "off"
    except Exception as e:
        return f"error: {str(e)}"

def set_usb_power(device_id, state):
    """Enable/disable USB device via power control"""
    try:
        device = USB_DEVICES.get(device_id)
        if not device:
            return False, "Device not found"
        
        # Try power/control method (preferred)
        power_path = os.path.join(device["path"], "power/control")
        if os.path.exists(power_path):
            try:
                # Use shell with sudo for write operations
                # Valid values: "auto" (can autosuspend), "on" (always on)
                value = "on" if state else "auto"
                result = subprocess.run(
                    ["sudo", "-n", "bash", "-c", f"echo {value} > {power_path}"],
                    capture_output=True,
                    text=True,
                    timeout=5
                )
                if result.returncode == 0:
                    return True, f"Device {device_id} turned {'on' if state else 'off'}"
                else:
                    error_msg = result.stderr.strip() if result.stderr else "Unknown error"
                    # If sudo requires password, try direct write as fallback
                    if "password" in error_msg.lower():
                        try:
                            with open(power_path, 'w') as f:
                                f.write(value)
                            return True, f"Device {device_id} turned {'on' if state else 'off'}"
                        except PermissionError:
                            return False, "Permission denied. No sudo NOPASSWD configured."
                    return False, f"Control failed: {error_msg}"
            except subprocess.TimeoutExpired:
                return False, "Control operation timed out"
            except Exception as e:
                return False, f"Control error: {str(e)}"
        
        return False, "USB power control not supported on this device"
        
    except Exception as e:
        return False, f"Error: {str(e)}"

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
