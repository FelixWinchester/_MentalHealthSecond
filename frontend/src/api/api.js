import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
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
  // Auth methods
  register(user) {
    return apiClient.post('/auth/register', user);
  },

  login(user) {
    const params = new URLSearchParams();
    params.append('username', user.username);
    params.append('password', user.password);

    return apiClient.post('/auth/token', params, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
      },
    });
  },

  async getUserInfo(token) {
    try {
      const response = await apiClient.get('/users/me', {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response;
    } catch (error) {
      console.error('Ошибка при запросе информации о пользователе:', error);
      throw error;
    }
  },

  updateUserInfo(token, userData) {
    return apiClient.put('/users/me/update', userData, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
  },

  // Mood methods
  createMoodEntry(data) {
    return apiClient.post('/mood', data);
  },

  getTodaysMood() {
    return apiClient.get('/mood/today');
  },

  deleteMoodEntry() {
    return apiClient.delete('/mood');
  },

  getMoodAnalytics(startDate, endDate) {
    return apiClient.get('/mood/analytics/moods', {
      params: { start_date: startDate, end_date: endDate }
    });
  },

  // Notes methods
  addNote(noteData) {
    return apiClient.post('/mood/notes', noteData);
  },

  getNotes() {
    return apiClient.get('/mood/notes');
  },

  deleteNote(noteId) {
    return apiClient.delete(`/notes/${noteId}`);
  },
};