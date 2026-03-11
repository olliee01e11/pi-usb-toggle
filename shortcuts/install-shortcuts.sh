#!/bin/bash
# macOS installer script for Shortcuts pack
# Requires macOS 12+ with the `shortcuts` CLI

HOST="hpi.local:5000"

echo "Installing Pi USB Toggle shortcuts using macOS 'shortcuts' CLI..."

if ! command -v shortcuts &> /dev/null; then
  echo "Error: 'shortcuts' CLI not found. Run on macOS with Shortcuts app installed."
  exit 1
fi

# Toggle All
shortcuts add "Toggle Pi USB" \
  -a "Get Contents of URL" "http://$HOST/api/usb/device/all_ports/power" "POST" "JSON" '{"action":"toggle"}' \
  -a "Show Result"

# Turn On
shortcuts add "Turn Pi USB on" \
  -a "Get Contents of URL" "http://$HOST/api/usb/device/all_ports/power" "POST" "JSON" '{"action":"on"}' \
  -a "Show Result"

# Turn Off
shortcuts add "Turn Pi USB off" \
  -a "Get Contents of URL" "http://$HOST/api/usb/device/all_ports/power" "POST" "JSON" '{"action":"off"}' \
  -a "Show Result"

# Check Status
shortcuts add "Pi USB status" \
  -a "Get Contents of URL" "http://$HOST/api/usb/devices" "GET" "" "" \
  -a "Show Result"

echo "Shortcuts created. Open Shortcuts app to edit Siri phrases or automation settings."

exit 0
