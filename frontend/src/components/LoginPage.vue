<template>
  <div class="login-page">
    <!-- Заголовок страницы -->
    <header class="header">
      <h1>{{ pageTitle }}</h1>
      <p>Пожалуйста, войдите в систему, чтобы получить доступ к вашему аккаунту.</p>
    </header>

    <!-- Основной контент -->
    <main class="content">
      <!-- Секция с формой входа -->
      <section class="section login-section">
        <div class="login-form">
          <h2>Вход</h2>
          <form @submit.prevent="handleLogin">
            <div class="form-group">
              <label for="username">Имя пользователя:</label>
              <input
                type="text"
                id="username"
                v-model="username"
                required
                placeholder="Введите ваше имя пользователя"
              />
            </div>
            <div class="form-group">
              <label for="password">Пароль:</label>
              <input
                type="password"
                id="password"
                v-model="password"
                required
                placeholder="Введите ваш пароль"
              />
            </div>
            <button type="submit" class="cta-button">Войти</button>
          </form>
        </div>
        <div class="login-image">
          <img
            src="https://via.placeholder.com/400x300"
            alt="Вход в систему"
            class="image"
          />
        </div>
      </section>

      <!-- Секция с дополнительной информацией -->
      <section class="section info-section">
        <h2>Нет аккаунта?</h2>
        <p>
          Если у вас еще нет аккаунта, вы можете <a href="/register">зарегистрироваться</a> прямо сейчас.
          Это займет всего несколько минут!
        </p>
      </section>
    </main>
  </div>
</template>

<script>
import api from '@/api/api';

export default {
  name: 'LoginPage',
  props: {
    page: {
      type: String,
      default: 'Вход', // Значение по умолчанию
    },
  },
  data() {
    return {
      username: '',
      password: '',
    };
  },
  computed: {
    pageTitle() {
      return this.page || 'Вход';
    },
  },
  methods: {
    async handleLogin() {
  try {
    const response = await api.login({
      username: this.username,
      password: this.password,
    });

    if (response.data && response.data.access_token) {
      localStorage.setItem('token', response.data.access_token); // Токен сохраняется
      this.$router.push('/lk');
    } else {
      alert('Ошибка: токен не получен');
    }
  } catch (error) {
    console.error('Ошибка при входе:', error);
    alert('Ошибка при входе: ' + (error.response?.data?.detail || 'Неизвестная ошибка'));
  }
},
  },
};
</script>

<style scoped>
.login-page {
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

.login-section {
  display: flex;
  align-items: center;
  gap: 40px;
}

.login-form {
  flex: 1;
}

.login-form p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #444;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 1rem;
  color: #444;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.cta-button {
  background-color: #2c3e50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.cta-button:hover {
  background-color: #1a2a36;
}

.login-image img {
  max-width: 100%;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.info-section {
  text-align: center;
}

.info-section p {
  font-size: 1.1rem;
  color: #666;
}

.info-section a {
  color: #2c3e50;
  text-decoration: none;
}

.info-section a:hover {
  text-decoration: underline;
}
</style>