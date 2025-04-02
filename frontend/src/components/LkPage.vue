<template>
  <div class="lk-page">
    <!-- Заголовок страницы -->
    <header class="header">
      <h1>Личный кабинет</h1>
      <p>Добро пожаловать, {{ userName }}!</p>
    </header>

    <!-- Основной контент -->
    <main class="content">
      <!-- Секция с информацией о пользователе -->
      <section class="section user-info">
        <h2>Ваши данные</h2>
        <div class="info-container">
          <div class="avatar-container">
            <img
              :src="avatar || 'https://via.placeholder.com/150'"
              alt="Аватар пользователя"
              class="avatar"
            />
            <input
              type="file"
              accept="image/*"
              @change="handleAvatarChange"
              style="display: none"
              ref="avatarInput"
            />
            <button class="edit-button" @click="triggerAvatarUpload">Изменить фото</button>
          </div>
          <div class="details">
            <p><strong>Имя:</strong> {{ userName }}</p>
            <p><strong>Email:</strong> {{ userEmail }}</p>
            <p><strong>Дата регистрации:</strong> {{ joinDate }}</p>
          </div>
        </div>
      </section>

      <!-- Секция с настройками -->
      <section class="section settings">
        <h2>Настройки</h2>
        <div class="settings-options">
          <button class="settings-button" @click="changePassword">Изменить пароль</button>
          <button class="settings-button" @click="updateEmail">Изменить email</button>
          <button class="settings-button" @click="logout">Выйти из аккаунта</button>
        </div>
      </section>

      <!-- Секция со статистикой -->
      <section class="section statistics">
        <h2>Ваша активность</h2>
        <div class="stats-container">
          <div class="stat-item">
            <span class="stat-value">{{ completedTasks }}</span>
            <span class="stat-label">Завершено задач</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ daysActive }}</span>
            <span class="stat-label">Дней с нами</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">{{ achievements }}</span>
            <span class="stat-label">Достижения</span>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import api from '@/api/api'; // Импортируйте api

export default {
  name: 'LkPage',
  data() {
    return {
      userName: '',
      userEmail: '',
      joinDate: '',
      completedTasks: 0,
      daysActive: 0,
      achievements: 0,
      avatar: '', // URL аватара пользователя
    };
  },
  async created() {
    const token = localStorage.getItem('token');
    if (token) {
      try {
        const response = await api.getUserInfo(token);
        if (response.data) {
          this.userName = response.data.username;
          this.userEmail = response.data.email;
          this.joinDate = new Date(response.data.created_at).toLocaleDateString();
          this.avatar = response.data.avatar_path || ''; // Загружаем аватар, если он есть
        } else {
          console.error('Ошибка: данные не получены');
          alert('Ошибка: данные не получены');
        }
      } catch (error) {
        console.error('Ошибка при получении информации о пользователе:', error);
        alert(
          'Ошибка при получении информации о пользователе: ' +
            (error.response?.data?.detail || 'Неизвестная ошибка')
        );
      }
    } else {
      this.$router.push('/login');
    }
  },
  methods: {
    // Запуск выбора файла для аватара
    triggerAvatarUpload() {
      this.$refs.avatarInput.click();
    },
    // Обработка выбора файла
    async handleAvatarChange(event) {
      const file = event.target.files[0];
      if (file) {
        try {
          await this.updateAvatar(file);
          alert('Аватар успешно обновлен!');
        } catch (error) {
          console.error('Ошибка при обновлении аватара:', error);
          alert('Ошибка при обновлении аватара: ' + error.response?.data?.detail || 'Неизвестная ошибка');
        }
      }
    },
    // Обновление аватара на сервере
    async updateAvatar(file) {
      const token = localStorage.getItem('token');
      if (token) {
        const formData = new FormData();
        formData.append('avatar', file);
        const response = await api.updateUserInfo(token, formData);
        if (response.data) {
          this.avatar = response.data.avatar_path; // Обновляем URL аватара
        }
      }
    },
    changePassword() {
      alert('Функция изменения пароля в разработке.');
    },
    updateEmail() {
      alert('Функция изменения email в разработке.');
    },
    logout() {
      localStorage.removeItem('token');
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.lk-page {
  font-family: Arial, sans-serif;
  color: #333;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;
}

.header h1 {
  font-size: 2.5rem;
  color: #2c3e50;
}

.header p {
  font-size: 1.2rem;
  color: #666;
}

.content {
  margin-bottom: 40px;
}

.section {
  margin-bottom: 40px;
}

.section h2 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 20px;
}

.user-info .info-container {
  display: flex;
  align-items: center;
  gap: 40px;
}

.avatar-container {
  text-align: center;
}

.avatar {
  width: 150px;
  height: 150px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 10px;
}

.edit-button {
  background-color: #2c3e50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.edit-button:hover {
  background-color: #1a2a36;
}

.details p {
  font-size: 1.1rem;
  margin-bottom: 10px;
}

.settings-options {
  display: flex;
  gap: 20px;
}

.settings-button {
  background-color: #2c3e50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.settings-button:hover {
  background-color: #1a2a36;
}

.statistics .stats-container {
  display: flex;
  justify-content: space-around;
  text-align: center;
}

.stat-item {
  flex: 1;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f8f9fa;
}

.stat-value {
  font-size: 2rem;
  font-weight: bold;
  color: #2c3e50;
}

.stat-label {
  font-size: 1rem;
  color: #666;
}

.footer {
  text-align: center;
  padding: 20px;
  background-color: #f8f9fa;
  border-top: 1px solid #ddd;
  margin-top: 40px;
}

.footer p {
  font-size: 0.9rem;
  color: #666;
}
</style>