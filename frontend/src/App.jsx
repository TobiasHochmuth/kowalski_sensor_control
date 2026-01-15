import { useState, useEffect } from 'react';
import './App.css'

export default function App() {

    const [temp, setTemp] = useState('Loading...');
    const [humid, setHumid] = useState('Loading...');

    const fetchTemp = async () => {
        const response = await fetch('http://localhost:5000/sensors/temperature');
        const data = await response.json();
        setTemp(data.temperature);
    }

    const fetchHumid = async () => {
        const response = await fetch('http://localhost:5000/sensors/humidity');
        const data = await response.json();
        setHumid(data.humidity);
    }


    // Load data when page loads
    useEffect(() => {
        fetchTemp();
        fetchHumid();
    }, []);

  return (
    <div className="screen-container">
      <div className="screen">
        <h1>Kowalski Sensor Control</h1>

        <div>
            <div className="sensor-box">
                <div className="sensor-title">Temperature</div>
                <div className="sensor-value"> {temp}°C </div>
                <button className="refresh-button" onClick={fetchTemp}></button>
            </div>
            
            <div className="sensor-box">
                <div className="sensor-title">Humidity</div>
                <div className="sensor-value"> {humid}°C </div>
                <button className="refresh-button" onClick={fetchHumid}></button>
            </div>
        </div>
        
      </div>
    </div>
  )
}
