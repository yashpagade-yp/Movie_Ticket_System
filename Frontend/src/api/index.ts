import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

export const api = axios.create({
    baseURL: API_BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Add auth token to requests
api.interceptors.request.use((config) => {
    const token = localStorage.getItem('token');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
});

// User API
export const userApi = {
    register: async (data: {
        email: string;
        password: string;
        first_name: string;
        last_name: string;
        mobile_number: string;
    }) => {
        const response = await api.post('/users/register', data);
        return response.data;
    },

    login: async (data: { email: string; password: string }) => {
        const response = await api.post('/users/login', data);
        return response.data;
    },

    getProfile: async () => {
        const response = await api.get('/users/me');
        return response.data;
    },

    forgotPassword: async (email: string) => {
        const response = await api.post('/users/forgot-password', { email });
        return response.data;
    },

    resetPassword: async (data: {
        email: string;
        otp: string;
        new_password: string;
    }) => {
        const response = await api.post('/users/reset-password', data);
        return response.data;
    },
};
