import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

// Response interceptor for consistent error handling
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response) {
      // Server returned an error response
      const detail = error.response.data?.detail;
      if (detail && typeof detail === 'object') {
        error.friendlyMessage = detail.message || 'An error occurred';
        error.errorField = detail.field;
      } else if (typeof detail === 'string') {
        error.friendlyMessage = detail;
      } else {
        error.friendlyMessage = error.response.data?.message || 'An error occurred';
      }
    } else if (error.request) {
      error.friendlyMessage = 'Unable to connect to the server. Please check if the backend is running.';
    } else {
      error.friendlyMessage = 'An unexpected error occurred';
    }
    return Promise.reject(error);
  }
);

export default api;
