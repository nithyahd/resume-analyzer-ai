import React, { useState } from 'react';
import './App.css';

function App() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);

  const handleUpload = async () => {
    if (!file) {
      alert("Please upload a PDF file.");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch("http://127.0.0.1:5000/analyze", {
      method: "POST",
      body: formData
    });

    const data = await response.json();
    setResult(data);
  };

  return (
    <div className="App">
      <h2>Resume Analyzer</h2>
      <input type="file" accept=".pdf" onChange={(e) => setFile(e.target.files[0])} />
      <br /><br />
      <button onClick={handleUpload}>Upload & Analyze</button>

      {result && (
        <div style={{ marginTop: "20px", textAlign: "left" }}>
          <h3>Analysis Result:</h3>
          <p><strong>Name:</strong> {result.Name}</p>
          <p><strong>Email:</strong> {result.Email?.join(", ")}</p>
          <p><strong>Phone:</strong> {result.Phone?.join(", ")}</p>
          <p><strong>Skills:</strong> {result.Skills?.join(", ")}</p>
        </div>
      )}
    </div>
  );
}

export default App;
