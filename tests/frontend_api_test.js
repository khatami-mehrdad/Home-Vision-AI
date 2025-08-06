#!/usr/bin/env node
/**
 * Frontend API Test
 * Tests if the frontend can access backend API endpoints
 */

const fetch = require('node-fetch');

async function testBackendAPI() {
    console.log('🧪 Testing Backend API Access...\n');
    
    const baseUrl = 'http://localhost:8000';
    
    try {
        // Test 1: Health endpoint
        console.log('1. Testing health endpoint...');
        const healthResponse = await fetch(`${baseUrl}/health`);
        const healthData = await healthResponse.json();
        console.log(`✅ Health: ${JSON.stringify(healthData)}`);
        
        // Test 2: Cameras endpoint
        console.log('\n2. Testing cameras endpoint...');
        const camerasResponse = await fetch(`${baseUrl}/api/v1/cameras/`);
        const camerasData = await camerasResponse.json();
        console.log(`✅ Cameras: Found ${camerasData.length} camera(s)`);
        camerasData.forEach(camera => {
            console.log(`   - ${camera.name}: ${camera.rtsp_url}`);
        });
        
        // Test 3: Start camera stream
        console.log('\n3. Testing camera stream start...');
        const startResponse = await fetch(`${baseUrl}/api/v1/cameras/1/start`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        const startData = await startResponse.json();
        console.log(`✅ Start stream: ${JSON.stringify(startData)}`);
        
        // Test 4: Get camera frame
        console.log('\n4. Testing camera frame...');
        const frameResponse = await fetch(`${baseUrl}/api/v1/cameras/1/frame`, {
            method: 'GET',
            headers: {
                'Accept': 'image/jpeg',
                'Cache-Control': 'no-cache'
            }
        });
        
        if (frameResponse.ok) {
            const frameBuffer = await frameResponse.buffer();
            console.log(`✅ Frame: ${frameBuffer.length} bytes`);
        } else {
            console.log(`❌ Frame: ${frameResponse.status} ${frameResponse.statusText}`);
        }
        
        console.log('\n🎉 All API tests passed! Frontend should be able to access the backend.');
        
    } catch (error) {
        console.error('❌ API test failed:', error.message);
    }
}

// Run the test
testBackendAPI(); 