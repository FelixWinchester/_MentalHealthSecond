import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  withCredentials: false,
  headers: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
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
};