<template>
  <div class="auth-page">
    <div class="auth-logo">
      <div class="logo-icon">🧠</div>
      <h1>Регистрация</h1>
      <p>Создайте аккаунт, чтобы начать</p>
    </div>

    <form class="auth-form" @submit.prevent="submit">
      <div class="input-group">
        <label>Имя пользователя</label>
        <input v-model="form.username" type="text" placeholder="Придумайте имя" autocomplete="username" required />
      </div>
      <div class="input-group">
        <label>Email</label>
        <input v-model="form.email" type="email" placeholder="your@email.com" autocomplete="email" required />
      </div>
      <div class="input-group">
        <label>Пароль</label>
        <input v-model="form.password" type="password" placeholder="Минимум 6 символов" autocomplete="new-password" required />
      </div>

      <p class="error-msg" v-if="error">{{ error }}</p>
      <p class="success-msg" v-if="success">Аккаунт создан! Войдите.</p>

      <button class="btn btn-primary" type="submit" :disabled="loading">
        {{ loading ? 'Создаём...' : 'Зарегистрироваться' }}
      </button>
    </form>

    <p class="auth-switch">
      Уже есть аккаунт?
      <router-link to="/login">Войти</router-link>
    </p>
  </div>
</template>

<script>
import api from '@/api/api';

export default {
  name: 'RegisterView',
  data() {
    return {
      form: { username: '', email: '', password: '' },
      error: '',
      success: false,
      loading: false,
    };
  },
  methods: {
    async submit() {
      this.error = '';
      this.success = false;
      this.loading = true;
      try {
        await api.register(this.form);
        this.success = true;
        setTimeout(() => this.$router.push('/login'), 1500);
      } catch (e) {
        this.error = e?.response?.data?.detail || 'Ошибка регистрации';
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

.logo-icon { font-size: 3.5rem; margin-bottom: 12px; }

.auth-logo h1 {
  font-size: 1.8rem;
  font-weight: 800;
  background: linear-gradient(135deg, #805AD5, #667eea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 6px;
}

.auth-logo p { color: var(--text-muted); font-size: 0.9rem; }

.auth-form { margin-bottom: 24px; }

.error-msg {
  color: var(--danger);
  font-size: 0.85rem;
  text-align: center;
  margin-bottom: 12px;
}

.success-msg {
  color: var(--success);
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

.btn:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
