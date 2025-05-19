import React, { useState } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [service1Response, setService1Response] = useState('');
  const [service2Response, setService2Response] = useState('');

  const callService1 = async () => {
    try {
      const response = await fetch(`/api/service1/?input=${input}`);
      const data = await response.json();
      setService1Response(data.message);
    } catch (error) {
      console.error('Error calling service 1:', error);
      setService1Response('Error: Could not connect to service');
    }
  };

  const callService2 = async () => {
    try {
      const response = await fetch(`/api/service2/?input=${input}`);
      const data = await response.json();
      setService2Response(data.message);
    } catch (error) {
      console.error('Error calling service 2:', error);
      setService2Response('Error: Could not connect to service');
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>SWE590 Term Project</h1>
        <div className="input-container">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            placeholder="Enter your name"
          />
        </div>
        <div className="buttons-container">
          <button onClick={callService1}>Call Service 1</button>
          <button onClick={callService2}>Call Service 2</button>
        </div>
        <div className="responses-container">
          <div className="response">
            <h3>Service 1 Response:</h3>
            <p>{service1Response}</p>
          </div>
          <div className="response">
            <h3>Service 2 Response:</h3>
            <p>{service2Response}</p>
          </div>
        </div>
      </header>
    </div>
  );
}

export default App;
