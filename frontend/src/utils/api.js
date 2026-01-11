import axios from 'axios';

// Create an axios instance with a base URL
const api = axios.create({
    baseURL: import.meta.env.VITE_API_BASE_URL || ''
});

export default api;
