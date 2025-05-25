import React, { useState } from 'react';
import './App.css';

function App() {
  const [input, setInput] = useState('');
  const [service1Response, setService1Response] = useState('');
  const [service2Response, setService2Response] = useState('');

  // --- Cloud Function State ---
  const [selectedFile, setSelectedFile] = useState(null);
  const [processing, setProcessing] = useState(false);
  const [downloadUrl, setDownloadUrl] = useState(null);
  const [cloudFnError, setCloudFnError] = useState('');

  const callService1 = async () => {
    try {
      const response = await fetch(`/api/service1/hello/?input=${encodeURIComponent(input)}`);
      const data = await response.json();
      setService1Response(data.message);
    } catch (error) {
      console.error('Error calling service 1:', error);
      setService1Response('Error: Could not connect to service');
    }
  };

  const callService2 = async () => {
    try {
      const response = await fetch(`/api/service2/evening/?input=${encodeURIComponent(input)}`);
      const data = await response.json();
      setService2Response(data.message);
    } catch (error) {
      console.error('Error calling service 2:', error);
      setService2Response('Error: Could not connect to service');
    }
  };

  // --- Cloud Function Handler (via backend proxy) ---
  const handleFileChange = (e) => {
    setSelectedFile(e.target.files[0]);
    setDownloadUrl(null);
    setCloudFnError('');
  };

  const handleCloudFunction = async () => {
    if (!selectedFile) {
      setCloudFnError('Please select an image file.');
      return;
    }
    setProcessing(true);
    setCloudFnError('');
    setDownloadUrl(null);
    try {
      const proxyUrl = '/api/service1/negative-image/';
      const formData = new FormData();
      formData.append('file', selectedFile);

      const response = await fetch(proxyUrl, {
        method: 'POST',
        body: formData
      });
      if (!response.ok) {
        const text = await response.text();
        throw new Error(`Backend proxy error: ${text}`);
      }
      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      setDownloadUrl(url);
    } catch (err) {
      setCloudFnError(err.message);
    } finally {
      setProcessing(false);
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
        {/* --- Cloud Function Section --- */}
        <div className="cloud-function-section">
          <h2>Image Negative Cloud Function</h2>
          <input type="file" accept="image/*" onChange={handleFileChange} />
          <button onClick={handleCloudFunction} disabled={processing}>
            {processing ? 'Processing...' : 'Create Negative'}
          </button>
          {cloudFnError && <p style={{ color: 'red' }}>{cloudFnError}</p>}
          {downloadUrl && (
            <a href={downloadUrl} download="negative.png">Download Negative Image</a>
          )}
        </div>
      </header>
    </div>
  );
}

export default App;
