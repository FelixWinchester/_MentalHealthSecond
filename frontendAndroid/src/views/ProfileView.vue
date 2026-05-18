<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">Профиль</h1>
    </div>

    <div class="card profile-card">
      <div class="avatar">{{ avatarLetter }}</div>
      <h2 class="username">{{ username }}</h2>
      <p class="email">{{ email }}</p>
    </div>

    <div class="card stats-card" v-if="stats">
      <div class="stat-row">
        <span class="stat-label">🔥 Серия</span>
        <span class="stat-value">{{ stats.current_streak }} дней</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">📅 Всего записей</span>
        <span class="stat-value">{{ stats.total_entries }}</span>
      </div>
      <div class="stat-row">
        <span class="stat-label">🏆 Рекорд</span>
        <span class="stat-value">{{ stats.longest_streak }} дней</span>
      </div>
    </div>

    <button class="btn btn-ghost" @click="logout">Выйти из аккаунта</button>
  </div>
</template>

<script>
import api from '@/api/api';

export default {
  name: 'ProfileView',
  data() {
    return {
      username: '',
      email: '',
      stats: null,
    };
  },
  computed: {
    avatarLetter() {
      return this.username ? this.username[0].toUpperCase() : '?';
    },
  },
  async mounted() {
    try {
      const res = await api.getUserInfo();
      this.username = res.data.username;
      this.email = res.data.email;
      this.stats = {
        current_streak: res.data.current_streak ?? 0,
        total_entries: res.data.total_entries ?? 0,
        longest_streak: res.data.longest_streak ?? 0,
      };
    } catch { /* */ }
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('user_id');
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.profile-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px 20px;
  margin-bottom: 16px;
}

.avatar {
  width: 72px;
  height: 72px;
  border-radius: 50%;
  background: linear-gradient(135deg, #805AD5, #667eea);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 800;
  color: white;
  margin-bottom: 14px;
}

.username {
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--text);
  margin-bottom: 4px;
}

.email {
  font-size: 0.85rem;
  color: var(--text-muted);
}

.stats-card {
  display: flex;
  flex-direction: column;
  gap: 0;
  padding: 0;
  overflow: hidden;
  margin-bottom: 20px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 14px 20px;
  border-bottom: 1px solid var(--border);
}
.stat-row:last-child { border-bottom: none; }

.stat-label {
  font-size: 0.9rem;
  color: var(--text-sub);
}

.stat-value {
  font-size: 0.95rem;
  font-weight: 700;
  color: var(--text);
}
</style>
