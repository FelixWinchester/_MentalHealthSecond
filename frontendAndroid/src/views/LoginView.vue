<template>
  <div class="auth-page">
    <div class="auth-logo">
      <div class="logo-icon">🧠</div>
      <h1>Mental Health</h1>
      <p>Забота о себе начинается здесь</p>
    </div>

    <form class="auth-form" @submit.prevent="submit">
      <div class="input-group">
        <label>Имя пользователя</label>
        <input v-model="form.username" type="text" placeholder="Введите имя" autocomplete="username" required />
      </div>
      <div class="input-group">
        <label>Пароль</label>
        <input v-model="form.password" type="password" placeholder="Введите пароль" autocomplete="current-password" required />
      </div>

      <p class="error-msg" v-if="error">{{ error }}</p>

      <button class="btn btn-primary" type="submit" :disabled="loading">
        {{ loading ? 'Входим...' : 'Войти' }}
      </button>
    </form>

    <p class="auth-switch">
      Нет аккаунта?
      <router-link to="/register">Зарегистрироваться</router-link>
    </p>
  </div>
</template>

<script>
import api from '@/api/api';

export default {
  name: 'LoginView',
  data() {
    return {
      form: { username: '', password: '' },
      error: '',
      loading: false,
    };
  },
  methods: {
    async submit() {
      this.error = '';
      this.loading = true;
      try {
        const res = await api.login(this.form);
        localStorage.setItem('token', res.data.access_token);
        localStorage.setItem('user_id', res.data.user_id);
        this.$router.push('/home');
      } catch {
        this.error = 'Неверное имя пользователя или пароль';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.auth-page {
  min-height: 100dvh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding: 32px 24px;
}

.auth-logo {
  text-align: center;
  margin-bottom: 40px;
}

.logo-icon {
  font-size: 3.5rem;
  margin-bottom: 12px;
}

.auth-logo h1 {
  font-size: 1.8rem;
  font-weight: 800;
  background: linear-gradient(135deg, #805AD5, #667eea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 6px;
}

.auth-logo p {
  color: var(--text-muted);
  font-size: 0.9rem;
}

.auth-form {
  margin-bottom: 24px;
}

.error-msg {
  color: var(--danger);
  font-size: 0.85rem;
  text-align: center;
  margin-bottom: 12px;
}

.auth-switch {
  text-align: center;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.auth-switch a {
  color: var(--primary-light);
  text-decoration: none;
  font-weight: 600;
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
</style>
