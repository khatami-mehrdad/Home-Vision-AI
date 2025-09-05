import React from 'react';
import { useAuth } from '../../context/AuthContext';
import { LogOut, Clock } from 'lucide-react';

const Header = () => {
  const { user, logout } = useAuth();
  const currentTime = new Date().toLocaleTimeString();

  return (
    <header className="bg-gray-800 border-b border-gray-700 px-4 py-2">
      <div className="flex justify-between items-center">
        {/* Left side - Minimal info */}
        <div className="flex items-center space-x-3">
          <div className="flex items-center space-x-1 text-gray-400">
            <div className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></div>
            <span className="text-xs">Live</span>
          </div>
          <div className="flex items-center space-x-1 text-gray-400">
            <Clock className="h-3 w-3" />
            <span className="text-xs font-mono">{currentTime}</span>
          </div>
        </div>

        {/* Right side - User controls */}
        <div className="flex items-center space-x-2">
          {user && (
            <button
              onClick={logout}
              className="flex items-center space-x-1 text-gray-400 hover:text-white px-2 py-1 rounded transition-colors duration-200 text-xs"
            >
              <LogOut className="h-3 w-3" />
              <span>Logout</span>
            </button>
          )}
        </div>
      </div>
    </header>
  );
};

export default Header;
