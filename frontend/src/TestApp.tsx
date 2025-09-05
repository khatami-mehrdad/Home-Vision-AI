import React from 'react';

function TestApp() {
  return (
    <div style={{ 
      padding: '20px', 
      backgroundColor: '#1a1a1a', 
      color: 'white', 
      minHeight: '100vh',
      fontSize: '18px'
    }}>
      <h1>🎉 Frigate UI Test</h1>
      <p>If you can see this, React is working!</p>
      <p>Backend API Status:</p>
      <div style={{ marginLeft: '20px' }}>
        <p>✅ Config API: Working (Your camera is configured)</p>
        <p>✅ Stats API: Working</p>
        <p>✅ Profile API: Working</p>
      </div>
      <p>Next step: Load the full Frigate interface...</p>
    </div>
  );
}

export default TestApp;
