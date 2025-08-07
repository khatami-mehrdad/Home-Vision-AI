import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Base API configuration
const API_BASE_URL = 'http://localhost:8000/api/v1';

class ApiService {
  constructor() {
    this.api = axios.create({
      baseURL: API_BASE_URL,
      timeout: 10000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    // Add request interceptor to include auth token
    this.api.interceptors.request.use(
      async (config) => {
        const token = await AsyncStorage.getItem('authToken');
        if (token) {
          config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
      },
      (error) => {
        return Promise.reject(error);
      }
    );

    // Add response interceptor to handle auth errors
    this.api.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Token expired or invalid, clear storage
          AsyncStorage.removeItem('authToken');
          AsyncStorage.removeItem('user');
        }
        return Promise.reject(error);
      }
    );
  }

  setAuthToken(token) {
    this.api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  }

  removeAuthToken() {
    delete this.api.defaults.headers.common['Authorization'];
  }

  // Auth endpoints
  async login(username, password) {
    return this.api.post('/auth/login', { username, password });
  }

  async register(username, email, password) {
    return this.api.post('/auth/register', { username, email, password });
  }

  async verifyToken() {
    return this.api.get('/auth/verify');
  }

  // Camera endpoints
  async getCameras() {
    return this.api.get('/cameras');
  }

  async getCamera(id) {
    return this.api.get(`/cameras/${id}`);
  }

  async getCameraFrame(id) {
    return this.api.get(`/cameras/${id}/frame`, {
      responseType: 'blob',
    });
  }

  async getCameraStatus(id) {
    return this.api.get(`/cameras/${id}/status`);
  }

  async getAllCameraStatuses() {
    return this.api.get('/cameras/status/all');
  }

  async startCamera(id) {
    return this.api.post(`/cameras/${id}/start`);
  }

  async stopCamera(id) {
    return this.api.post(`/cameras/${id}/stop`);
  }

  // Event endpoints
  async getEvents(params = {}) {
    return this.api.get('/events', { params });
  }

  async getEvent(id) {
    return this.api.get(`/events/${id}`);
  }

  async deleteEvent(id) {
    return this.api.delete(`/events/${id}`);
  }

  // Notification endpoints
  async getNotifications() {
    return this.api.get('/notifications');
  }

  async markNotificationAsRead(id) {
    return this.api.put(`/notifications/${id}/read`);
  }

  async subscribeToNotifications(token, topics = []) {
    return this.api.post('/notifications/subscribe', {
      token,
      topics,
    });
  }

  async unsubscribeFromNotifications(token, topics = []) {
    return this.api.post('/notifications/unsubscribe', {
      token,
      topics,
    });
  }

  // Generic HTTP methods
  async get(url, config = {}) {
    return this.api.get(url, config);
  }

  async post(url, data = {}, config = {}) {
    return this.api.post(url, data, config);
  }

  async put(url, data = {}, config = {}) {
    return this.api.put(url, data, config);
  }

  async delete(url, config = {}) {
    return this.api.delete(url, config);
  }
}

export const apiService = new ApiService(); 