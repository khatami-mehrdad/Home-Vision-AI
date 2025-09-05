import React, { useState, useEffect } from 'react';
import { baseUrl } from './api/baseUrl';

// Comprehensive Live Feed Debug Component
function LiveFeedDebugger() {
  const [logs, setLogs] = useState<string[]>([]);
  const [imageError, setImageError] = useState<string | null>(null);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [apiTests, setApiTests] = useState<Record<string, any>>({});
  const [streamStatus, setStreamStatus] = useState<string>('Not started');

  const addLog = (message: string) => {
    const timestamp = new Date().toLocaleTimeString();
    const logEntry = `[${timestamp}] ${message}`;
    console.log(logEntry);
    setLogs(prev => [...prev, logEntry]);
  };

  // Test different API endpoints
  const testApiEndpoints = async () => {
    addLog('🔍 Starting API endpoint tests...');
    
    const tests = {
      cameras: null,
      cameraById: null,
      cameraFrame: null,
      cameraStart: null,
      cameraStatus: null
    };

    try {
      // Test 1: Get cameras list
      addLog('📋 Testing GET /api/v1/cameras/');
      const camerasResponse = await fetch(`${baseUrl}api/v1/cameras/`);
      tests.cameras = {
        status: camerasResponse.status,
        ok: camerasResponse.ok,
        data: camerasResponse.ok ? await camerasResponse.json() : null
      };
      addLog(`📋 Cameras API: ${camerasResponse.status} ${camerasResponse.ok ? '✅' : '❌'}`);

      // Test 2: Get specific camera
      addLog('🎥 Testing GET /api/v1/cameras/1');
      const cameraResponse = await fetch(`${baseUrl}api/v1/cameras/1`);
      tests.cameraById = {
        status: cameraResponse.status,
        ok: cameraResponse.ok,
        data: cameraResponse.ok ? await cameraResponse.json() : null
      };
      addLog(`🎥 Camera by ID: ${cameraResponse.status} ${cameraResponse.ok ? '✅' : '❌'}`);

      // Test 3: Get camera frame
      addLog('🖼️ Testing GET /api/v1/cameras/1/frame');
      const frameResponse = await fetch(`${baseUrl}api/v1/cameras/1/frame`);
      tests.cameraFrame = {
        status: frameResponse.status,
        ok: frameResponse.ok,
        contentType: frameResponse.headers.get('content-type'),
        size: frameResponse.ok ? (await frameResponse.blob()).size : null
      };
      addLog(`🖼️ Camera frame: ${frameResponse.status} ${frameResponse.ok ? '✅' : '❌'} (${tests.cameraFrame.contentType})`);

      // Test 4: Start camera stream
      addLog('🚀 Testing POST /api/v1/cameras/1/start');
      const startResponse = await fetch(`${baseUrl}api/v1/cameras/1/start`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        }
      });
      tests.cameraStart = {
        status: startResponse.status,
        ok: startResponse.ok,
        data: startResponse.ok ? await startResponse.json() : await startResponse.text()
      };
      addLog(`🚀 Camera start: ${startResponse.status} ${startResponse.ok ? '✅' : '❌'}`);
      if (!startResponse.ok) {
        addLog(`❌ Start error: ${tests.cameraStart.data}`);
      }

      // Test 5: Check camera status
      addLog('📊 Testing GET /api/v1/cameras/1/status');
      const statusResponse = await fetch(`${baseUrl}api/v1/cameras/1/status`);
      tests.cameraStatus = {
        status: statusResponse.status,
        ok: statusResponse.ok,
        data: statusResponse.ok ? await statusResponse.json() : null
      };
      addLog(`📊 Camera status: ${statusResponse.status} ${statusResponse.ok ? '✅' : '❌'}`);

    } catch (error) {
      addLog(`💥 API test error: ${error}`);
    }

    setApiTests(tests);
    addLog('🏁 API endpoint tests completed');
  };

  // Test WebSocket connection
  const testWebSocket = () => {
    addLog('🔌 Testing WebSocket connection...');
    const wsUrl = `${baseUrl.replace(/^http/, 'ws')}ws`;
    addLog(`🔌 WebSocket URL: ${wsUrl}`);
    
    try {
      const ws = new WebSocket(wsUrl);
      
      ws.onopen = () => {
        addLog('🔌 WebSocket connected ✅');
        ws.send(JSON.stringify({ topic: 'onConnect', message: '', retain: false }));
      };
      
      ws.onmessage = (event) => {
        addLog(`📨 WebSocket message: ${event.data.substring(0, 100)}...`);
      };
      
      ws.onerror = (error) => {
        addLog(`❌ WebSocket error: ${error}`);
      };
      
      ws.onclose = (event) => {
        addLog(`🔌 WebSocket closed: ${event.code} - ${event.reason}`);
      };

      // Close after 5 seconds
      setTimeout(() => {
        if (ws.readyState === WebSocket.OPEN) {
          ws.close();
          addLog('🔌 WebSocket test completed');
        }
      }, 5000);
      
    } catch (error) {
      addLog(`💥 WebSocket test error: ${error}`);
    }
  };

  // Test image loading with different URLs
  const testImageUrls = () => {
    addLog('🖼️ Testing different image URL formats...');
    
    const urls = [
      `${baseUrl}api/v1/cameras/1/frame`,
      `${baseUrl}api/v1/my_camera/latest.webp?height=360&t=${Date.now()}`,
      `${baseUrl}api/v1/My%20Camera/latest.webp?height=360&t=${Date.now()}`,
    ];

    urls.forEach((url, index) => {
      const img = new Image();
      img.onload = () => addLog(`🖼️ Image URL ${index + 1} loaded ✅: ${url}`);
      img.onerror = () => addLog(`❌ Image URL ${index + 1} failed: ${url}`);
      img.src = url;
    });
  };

  const runAllTests = () => {
    setLogs([]);
    addLog('🚀 Starting comprehensive live feed diagnostics...');
    testApiEndpoints();
    testWebSocket();
    testImageUrls();
  };

  useEffect(() => {
    runAllTests();
  }, []);

  const cameraName = "my_camera";
  const height = 360;
  const imageUrl = `${baseUrl}api/v1/cameras/1/frame?t=${Date.now()}`;
  
  console.log('🔍 Debug - baseUrl:', baseUrl);
  console.log('🔍 Debug - imageUrl:', imageUrl);

  return (
    <div style={{ padding: '20px', backgroundColor: '#1a1a1a', color: 'white', fontFamily: 'monospace' }}>
      <h1>🔍 Live Feed Diagnostics Dashboard</h1>
      
      <div style={{ display: 'flex', gap: '20px', marginBottom: '20px' }}>
        <button 
          onClick={runAllTests}
          style={{ 
            padding: '10px 20px', 
            backgroundColor: '#4CAF50', 
            color: 'white', 
            border: 'none', 
            borderRadius: '5px',
            cursor: 'pointer'
          }}
        >
          🔄 Run All Tests
        </button>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px' }}>
        {/* Current Frame Test */}
        <div style={{ border: '1px solid #333', padding: '15px', borderRadius: '8px' }}>
          <h3>📸 Current Frame Test</h3>
          <p><strong>URL:</strong> {imageUrl}</p>
          <p><strong>Status:</strong> {imageLoaded ? '✅ Loaded' : imageError ? '❌ Error' : '⏳ Loading...'}</p>
          {imageError && <p style={{ color: '#ff6b6b' }}><strong>Error:</strong> {imageError}</p>}
          
          <div style={{ border: '2px solid #333', padding: '10px', maxWidth: '400px', marginTop: '10px' }}>
            <img
              src={imageUrl}
              alt="Camera feed"
              style={{ 
                maxWidth: '100%', 
                height: 'auto',
                display: 'block'
              }}
              onLoad={() => {
                setImageLoaded(true);
                setImageError(null);
                addLog('✅ Current frame loaded successfully');
              }}
              onError={(e) => {
                const error = `Failed to load image: ${e.type}`;
                setImageError(error);
                setImageLoaded(false);
                addLog(`❌ Current frame load error: ${error}`);
              }}
            />
          </div>
        </div>

        {/* AI Frame Comparison */}
        <div style={{ border: '1px solid #333', padding: '15px', borderRadius: '8px' }}>
          <h3>🤖 AI Frame Test</h3>
          <p><strong>URL:</strong> {`${baseUrl}api/v1/cameras/1/frame/ai?t=${Date.now()}`}</p>
          <p><strong>Note:</strong> This endpoint tries AI detection first, falls back to "AI Unavailable" overlay</p>
          
          <div style={{ border: '2px solid #333', padding: '10px', maxWidth: '400px', marginTop: '10px' }}>
            <img
              src={`${baseUrl}api/v1/cameras/1/frame/ai?t=${Date.now()}`}
              alt="Camera feed with AI"
              style={{ 
                maxWidth: '100%', 
                height: 'auto',
                display: 'block'
              }}
              onLoad={() => addLog('✅ AI frame loaded successfully')}
              onError={(e) => addLog(`❌ AI frame load error: ${e.type}`)}
            />
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '20px', marginTop: '20px' }}>
        {/* API Test Results */}
        <div style={{ border: '1px solid #333', padding: '15px', borderRadius: '8px' }}>
          <h3>🔧 API Test Results</h3>
          {Object.entries(apiTests).map(([key, result]) => (
            <div key={key} style={{ marginBottom: '10px' }}>
              <strong>{key}:</strong> {result ? 
                <span style={{ color: result.ok ? '#4CAF50' : '#ff6b6b' }}>
                  {result.status} {result.ok ? '✅' : '❌'}
                </span> : 
                <span style={{ color: '#888' }}>⏳ Pending</span>
              }
            </div>
          ))}
        </div>
      </div>

      {/* Log Output */}
      <div style={{ border: '1px solid #333', padding: '15px', borderRadius: '8px', marginTop: '20px' }}>
        <h3>📋 Diagnostic Log</h3>
        <div style={{ 
          backgroundColor: '#000', 
          padding: '10px', 
          borderRadius: '4px', 
          maxHeight: '300px', 
          overflowY: 'auto',
          fontSize: '12px',
          lineHeight: '1.4'
        }}>
          {logs.map((log, index) => (
            <div key={index} style={{ marginBottom: '2px' }}>{log}</div>
          ))}
        </div>
      </div>

      <div style={{ marginTop: '20px', fontSize: '14px', color: '#888' }}>
        <p><strong>What this tests:</strong></p>
        <ul>
          <li>✅ Backend API endpoints and responses</li>
          <li>🔌 WebSocket connection for real-time updates</li>
          <li>🖼️ Image loading with different URL formats</li>
          <li>🚀 Camera stream start/stop functionality</li>
          <li>📊 Camera status and health checks</li>
        </ul>
      </div>
    </div>
  );
}

export default LiveFeedDebugger;

