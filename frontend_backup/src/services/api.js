import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/v1';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Camera API
export const getCameras = async () => {
  const response = await api.get('/cameras');
  return response.data;
};

export const getCamera = async (id) => {
  const response = await api.get(`/cameras/${id}`);
  return response.data;
};

export const createCamera = async (cameraData) => {
  const response = await api.post('/cameras', cameraData);
  return response.data;
};

export const updateCamera = async (id, cameraData) => {
  const response = await api.put(`/cameras/${id}`, cameraData);
  return response.data;
};

export const deleteCamera = async (id) => {
  const response = await api.delete(`/cameras/${id}`);
  return response.data;
};

export const startCameraStream = async (id) => {
  const response = await api.post(`/cameras/${id}/start`);
  return response.data;
};

export const stopCameraStream = async (id) => {
  const response = await api.post(`/cameras/${id}/stop`);
  return response.data;
};

export const getCameraStatus = async (id) => {
  const response = await api.get(`/cameras/${id}/status`);
  return response.data;
};

export const getAllCameraStatuses = async () => {
  const response = await api.get('/cameras/status/all');
  return response.data;
};

// Events API
export const getEvents = async (params = {}) => {
  const response = await api.get('/events', { params });
  return response.data;
};

export const getEvent = async (id) => {
  const response = await api.get(`/events/${id}`);
  return response.data;
};

export const deleteEvent = async (id) => {
  const response = await api.delete(`/events/${id}`);
  return response.data;
};

// Notifications API
export const getNotifications = async (params = {}) => {
  const response = await api.get('/notifications', { params });
  return response.data;
};

export const markNotificationAsRead = async (id) => {
  const response = await api.put(`/notifications/${id}/read`);
  return response.data;
};

export const deleteNotification = async (id) => {
  const response = await api.delete(`/notifications/${id}`);
  return response.data;
};

// Auth API
export const login = async (credentials) => {
  const response = await api.post('/auth/login', credentials);
  return response.data;
};

export const register = async (userData) => {
  const response = await api.post('/auth/register', userData);
  return response.data;
};

export const logout = async () => {
  const response = await api.post('/auth/logout');
  return response.data;
};

export const getProfile = async () => {
  const response = await api.get('/auth/profile');
  return response.data;
};

export default api; 