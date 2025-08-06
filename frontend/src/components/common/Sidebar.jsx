import React from 'react';
import { Link, useLocation } from 'react-router-dom';

const Sidebar = () => {
  const location = useLocation();

  const menuItems = [
    { path: '/', label: 'Home', icon: '��' },
    { path: '/cameras', label: 'Cameras', icon: '��' },
    { path: '/events', label: 'Events', icon: '��' },
    { path: '/notifications', label: 'Notifications', icon: '��' },
    { path: '/settings', label: 'Settings', icon: '⚙️' }
  ];

  return (
    <aside className="bg-gray-100 w-64 min-h-screen p-4">
      <nav>
        <ul className="space-y-2">
          {menuItems.map((item) => (
            <li key={item.path}>
              <Link
                to={item.path}
                className={`flex items-center space-x-2 p-2 rounded hover:bg-gray-200 ${
                  location.pathname === item.path ? 'bg-gray-200' : ''
                }`}
              >
                <span>{item.icon}</span>
                <span>{item.label}</span>
              </Link>
            </li>
          ))}
        </ul>
      </nav>
    </aside>
  );
};

export default Sidebar;
