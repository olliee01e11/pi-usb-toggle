import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [devices, setDevices] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [apiUrl] = useState('http://localhost:5000');

  useEffect(() => {
    fetchDevices();
    const interval = setInterval(fetchDevices, 2000); // Poll every 2 seconds
    return () => clearInterval(interval);
  }, []);

  const fetchDevices = async () => {
    try {
      const response = await axios.get(`${apiUrl}/api/usb/devices`);
      setDevices(response.data);
      setLoading(false);
      setError(null);
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const toggleDevice = async (deviceId) => {
    try {
      setLoading(true);
      await axios.post(`${apiUrl}/api/usb/device/${deviceId}/power`, {
        action: 'toggle'
      });
      fetchDevices();
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const turnOnAll = async () => {
    try {
      setLoading(true);
      await axios.post(`${apiUrl}/api/usb/all/power`, {
        action: 'on'
      });
      fetchDevices();
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  const turnOffAll = async () => {
    try {
      setLoading(true);
      await axios.post(`${apiUrl}/api/usb/all/power`, {
        action: 'off'
      });
      fetchDevices();
    } catch (err) {
      setError(err.message);
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <header className="header">
        <h1>🍓 Raspberry Pi USB Control</h1>
        <p>Toggle USB hub power on/off</p>
      </header>

      {error && (
        <div className="error-box">
          ⚠️ {error}
          <br />
          <small>Make sure the API is running: <code>sudo python3 backend/app.py</code></small>
        </div>
      )}

      {loading && devices.length === 0 ? (
        <div className="loading">Loading devices...</div>
      ) : (
        <div className="content">
          <div className="devices-grid">
            {devices.map((device) => (
              <div key={device.id} className={`device-card ${device.status === 'on' ? 'active' : 'inactive'}`}>
                <div className="device-header">
                  <h3>{device.name}</h3>
                  <span className={`status-badge ${device.status === 'on' ? 'on' : 'off'}`}>
                    {device.status === 'on' ? '🟢 ON' : '🔴 OFF'}
                  </span>
                </div>
                <div className="device-id">ID: {device.id}</div>
                <button
                  className={`toggle-button ${device.status === 'on' ? 'turn-off' : 'turn-on'}`}
                  onClick={() => toggleDevice(device.id)}
                  disabled={loading}
                >
                  {device.status === 'on' ? 'Turn Off' : 'Turn On'}
                </button>
              </div>
            ))}
          </div>

          <div className="controls">
            <button className="control-button on" onClick={turnOnAll} disabled={loading}>
              Turn All On
            </button>
            <button className="control-button off" onClick={turnOffAll} disabled={loading}>
              Turn All Off
            </button>
          </div>
        </div>
      )}

      <footer className="footer">
        <small>Pi USB Toggle • Requires sudo to control USB devices</small>
      </footer>
    </div>
  );
}

export default App;
