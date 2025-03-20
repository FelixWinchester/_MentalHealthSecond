import axios from 'axios';

const apiClient = axios.create({
  baseURL: process.env.VUE_APP_API_URL || 'http://localhost:8000/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

export default {
  getUsers() {
    return apiClient.get('/users/');
  },
  getUser(id) {
    return apiClient.get(`/users/${id}`);
  },
  createUser(user) {
    return apiClient.post('/users/', user);
  },
};