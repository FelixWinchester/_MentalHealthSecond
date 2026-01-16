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
    // data может содержать { mood: 'HAPPY', details: 'Сегодня отличный день' }
    return apiClient.post('/mood/', data);
  },

  // Получить запись за сегодня (чтобы показать текущий статус)
  getTodaysMood() {
    return apiClient.get('/mood/today');
  },

  // Получить ВСЕ записи пользователя (которые по сути и есть его заметки)
  getNotes() {
    // Если у вас есть роут для получения истории/списка, используйте его.
    // Если нет, обычно это GET запрос на базовый /mood/
    return apiClient.get('/mood/'); 
  },

  // Добавление "заметки" теперь делает то же самое, что и создание настроения
  addNote(noteData) {
    return apiClient.post('/mood/', noteData);
  },

  // Удаление конкретной записи по ID
  deleteNote(entryId) {
    // Исправлено: добавляем /mood/ перед ID, если роут в бэкенде защищен префиксом
    return apiClient.delete(`/mood/${entryId}`);
  },
  
  // Получить конкретную запись по ID
  getNoteById(entryId) {
    return apiClient.get(`/mood/${entryId}`);
  }
};