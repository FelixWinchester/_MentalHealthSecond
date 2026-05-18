import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://10.0.2.2:8000',
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use(config => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

export default {
  register(user) {
    return apiClient.post('/auth/register', user);
  },

  login(user) {
    const params = new URLSearchParams();
    params.append('username', user.username);
    params.append('password', user.password);
    return apiClient.post('/auth/token', params, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    });
  },

  getUserInfo() {
    return apiClient.get('/users/me');
  },

  getTodaysMood() {
    return apiClient.get('/mood/today');
  },

  createMoodEntry(data) {
    return apiClient.post('/mood/', data);
  },

  getMoodChart(period = 'month') {
    return apiClient.get('/users/mood/chart', { params: { period } });
  },

  getThreads() {
    return apiClient.get('/forum/threads');
  },

  getThreadById(id) {
    return apiClient.get(`/forum/threads/${id}`);
  },

  createThread(data) {
    return apiClient.post('/forum/threads', data);
  },

  voteThread(threadId, value) {
    return apiClient.post(`/forum/threads/${threadId}/vote`, { value });
  },

  getComments(threadId) {
    return apiClient.get(`/forum/threads/${threadId}/comments`);
  },

  createComment(threadId, data) {
    return apiClient.post(`/forum/threads/${threadId}/comments`, data);
  },
};
