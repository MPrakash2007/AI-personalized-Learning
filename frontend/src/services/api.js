import axios from 'axios';

// Normalize API Base URL
// In development: can use VITE_API_URL (e.g. http://127.0.0.1:8000) or default to '/api' via Vite proxy
// In production on Vercel: always uses '/api' on the same origin (no localhost leaks, no /api/api duplication)
const rawBaseURL = import.meta.env.VITE_API_URL;
let resolvedBaseURL = '/api';

if (rawBaseURL && typeof rawBaseURL === 'string') {
  const trimmed = rawBaseURL.trim().replace(/\/+$/, '');
  resolvedBaseURL = trimmed.endsWith('/api') ? trimmed : `${trimmed}/api`;
}

const api = axios.create({
  baseURL: resolvedBaseURL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 15000,
});

// Attach JWT token to outgoing requests
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('codeorbit_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor with resilient error handling for production
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // 401 Unauthorized handling
    if (error.response?.status === 401) {
      const currentPath = window.location.pathname;
      if (!currentPath.includes('/login') && !currentPath.includes('/register') && currentPath !== '/') {
        localStorage.removeItem('codeorbit_token');
        localStorage.removeItem('codeorbit_user');
        window.location.href = '/login';
      }
    }

    // Friendly server/network error message formatting
    if (!error.response) {
      error.userFriendlyMessage = 'Unable to connect to the CodeOrbit server. Please check your network or try again in a few moments.';
    } else if (error.response.status >= 500) {
      error.userFriendlyMessage = 'The CodeOrbit server encountered a temporary issue. Please try again shortly.';
    } else if (error.response.data?.detail) {
      error.userFriendlyMessage = typeof error.response.data.detail === 'string'
        ? error.response.data.detail
        : JSON.stringify(error.response.data.detail);
    }

    return Promise.reject(error);
  }
);

export default api;
