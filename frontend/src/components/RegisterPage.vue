<template>
  <div class="register-page">
    <!-- Заголовок страницы -->
    <header class="header">
      <h1>{{ pageTitle }}</h1>
      <p>Создайте новый аккаунт, чтобы получить доступ ко всем возможностям нашего сайта.</p>
    </header>

    <!-- Основной контент -->
    <main class="content">
      <!-- Секция с формой регистрации -->
      <section class="section register-section">
        <div class="register-form">
          <h2>Регистрация</h2>
          <form @submit.prevent="handleRegister">
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
              <label for="email">Электронная почта:</label>
              <input
                type="email"
                id="email"
                v-model="email"
                required
                placeholder="Введите вашу электронную почту"
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
            <div class="form-group">
              <label for="confirm-password">Подтвердите пароль:</label>
              <input
                type="password"
                id="confirm-password"
                v-model="confirmPassword"
                required
                placeholder="Подтвердите ваш пароль"
              />
            </div>
            <button type="submit" class="cta-button" :disabled="isLoading">
              {{ isLoading ? 'Регистрация...' : 'Зарегистрироваться' }}
            </button>
          </form>
        </div>
        <div class="register-image">
          <img
            src="https://via.placeholder.com/400x300"
            alt="Регистрация"
            class="image"
          />
        </div>
      </section>

      <!-- Секция с дополнительной информацией -->
      <section class="section info-section">
        <h2>Уже есть аккаунт?</h2>
        <p>
          Если у вас уже есть аккаунт, вы можете <a href="/login">войти в систему</a>.
        </p>
      </section>
    </main>
  </div>
</template>

<script>
import api from '@/api/api'; // Укажите правильный путь к файлу api.js

export default {
  name: 'RegisterPage',
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: '',
      isLoading: false,
      pageTitle: 'Регистрация', // Добавьте это свойство
    };
  },
  methods: {
        async handleRegister() {
          if (this.password !== this.confirmPassword) {
            alert('Пароли не совпадают!');
            return;
          }

          this.isLoading = true;

          try {
            const response = await api.register({
              username: this.username,
              email: this.email,
              password: this.password,
            });

            console.log('Ответ сервера:', response);
            alert('Регистрация прошла успешно!');
            this.$router.push('/login');
          } catch (error) {
            console.error('Ошибка при регистрации:', error);
            if (error.response) {
              alert('Ошибка при регистрации: ' + error.response.data.detail);
            } else if (error.request) {
              alert('Ошибка сети: сервер не ответил');
            } else {
              alert('Ошибка: ' + error.message);
            }
          } finally {
            this.isLoading = false;
          }
    },
  },
};
</script>

<style scoped>
.register-page {
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

.register-section {
  display: flex;
  align-items: center;
  gap: 40px;
}

.register-form {
  flex: 1;
}

.register-form p {
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

.cta-button:disabled {
  background-color: #cccccc;
  cursor: not-allowed;
}

.register-image img {
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