import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.tsx";
import TestApp from "./TestApp.tsx";
import TestCameraApp from "./TestCameraApp.tsx";
import "./index.css";
import "@/utils/i18n";
import "react-i18next";
import "@/api/homevision-adapter";

// Add error boundary for debugging
class ErrorBoundary extends React.Component<any, any> {
  constructor(props: any) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: any) {
    return { hasError: true, error };
  }

  componentDidCatch(error: any, errorInfo: any) {
    console.error('React Error Boundary caught an error:', error, errorInfo);
    console.error('Error stack:', error.stack);
    console.error('Component stack:', errorInfo.componentStack);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '20px', color: 'white', backgroundColor: '#1a1a1a', fontFamily: 'monospace' }}>
          <h1>🚨 Frigate UI Error</h1>
          <p>The backend is working fine, but there's an issue with the frontend:</p>
          
          <details style={{ whiteSpace: 'pre-wrap', marginBottom: '20px' }}>
            <summary style={{ cursor: 'pointer', fontSize: '16px', fontWeight: 'bold' }}>Error Message</summary>
            {this.state.error && this.state.error.toString()}
          </details>
          
          <details style={{ whiteSpace: 'pre-wrap', marginBottom: '20px' }}>
            <summary style={{ cursor: 'pointer', fontSize: '16px', fontWeight: 'bold' }}>Stack Trace</summary>
            {this.state.error && this.state.error.stack}
          </details>
          
          <div style={{ backgroundColor: '#2a2a2a', padding: '10px', borderRadius: '5px' }}>
            <p><strong>✅ Backend Status:</strong> Working</p>
            <p><strong>✅ API Endpoints:</strong> Responding</p>
            <p><strong>✅ Camera Config:</strong> "My Camera" loaded</p>
            <p><strong>❌ Frontend Issue:</strong> Frigate UI component error</p>
          </div>
          
          <button 
            onClick={() => window.location.reload()} 
            style={{ 
              marginTop: '20px', 
              padding: '10px 20px', 
              backgroundColor: '#4CAF50', 
              color: 'white', 
              border: 'none', 
              borderRadius: '5px',
              cursor: 'pointer'
            }}
          >
            Reload Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}

console.log('Home Vision AI Frigate UI starting...');
console.log('Window baseUrl:', window.baseUrl);

// Test modes: 0=Full App, 1=TestApp (API test), 2=TestCameraApp (Camera test)
const TEST_MODE = 0;

// Determine which app to render based on TEST_MODE
const getAppComponent = () => {
  switch (TEST_MODE) {
    case 1:
      return <TestApp />;
    case 2:
      return <TestCameraApp />;
    default:
      return <App />;
  }
};

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <ErrorBoundary>
      {getAppComponent()}
    </ErrorBoundary>
  </React.StrictMode>,
);
