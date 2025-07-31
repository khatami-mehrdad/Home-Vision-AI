import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';

import { AuthProvider } from './context/AuthContext';
import { CameraProvider } from './context/CameraContext';
import { NotificationProvider } from './context/NotificationContext';

import Header from './components/common/Header';
import Sidebar from './components/common/Sidebar';
import Home from './pages/Home';
import Cameras from './pages/Cameras';
import Events from './pages/Events';
import Notifications from './pages/Notifications';
import Settings from './pages/Settings';

import './styles/index.css';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <AuthProvider>
        <CameraProvider>
          <NotificationProvider>
            <Router>
              <div className="flex h-screen bg-gray-50">
                <Sidebar />
                <div className="flex-1 flex flex-col overflow-hidden">
                  <Header />
                  <main className="flex-1 overflow-x-hidden overflow-y-auto bg-gray-50">
                    <div className="container mx-auto px-6 py-8">
                      <Routes>
                        <Route path="/" element={<Home />} />
                        <Route path="/cameras" element={<Cameras />} />
                        <Route path="/events" element={<Events />} />
                        <Route path="/notifications" element={<Notifications />} />
                        <Route path="/settings" element={<Settings />} />
                      </Routes>
                    </div>
                  </main>
                </div>
              </div>
              <Toaster
                position="top-right"
                toastOptions={{
                  duration: 4000,
                  style: {
                    background: '#363636',
                    color: '#fff',
                  },
                }}
              />
            </Router>
          </NotificationProvider>
        </CameraProvider>
      </AuthProvider>
    </QueryClientProvider>
  );
}

export default App; 