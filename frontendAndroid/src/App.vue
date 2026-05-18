<template>
  <div class="app-shell">
    <main class="page-content">
      <router-view v-slot="{ Component }">
        <transition name="slide" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>

    <nav class="bottom-nav" v-if="isAuthenticated">
      <router-link to="/home" class="nav-item" active-class="active">
        <span class="nav-icon">🏠</span>
        <span class="nav-label">Главная</span>
      </router-link>
      <router-link to="/mood" class="nav-item" active-class="active">
        <span class="nav-icon">😊</span>
        <span class="nav-label">Настроение</span>
      </router-link>
      <router-link to="/chart" class="nav-item" active-class="active">
        <span class="nav-icon">📊</span>
        <span class="nav-label">График</span>
      </router-link>
      <router-link to="/forum" class="nav-item" active-class="active">
        <span class="nav-icon">💬</span>
        <span class="nav-label">Форум</span>
      </router-link>
      <router-link to="/profile" class="nav-item" active-class="active">
        <span class="nav-icon">👤</span>
        <span class="nav-label">Профиль</span>
      </router-link>
    </nav>
  </div>
</template>

<script>
export default {
  name: 'App',
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token');
    },
  },
  watch: {
    $route() {
      this.$forceUpdate();
    },
  },
};
</script>

<style>
:root {
  --bg: #0f172a;
  --surface: #1e293b;
  --surface2: #273449;
  --border: #334155;
  --primary: #805AD5;
  --primary-light: #9f7aea;
  --text: #e2e8f0;
  --text-muted: #64748b;
  --text-sub: #94a3b8;
  --success: #22c55e;
  --warning: #facc15;
  --danger: #ef4444;
  --nav-height: 68px;
  --safe-bottom: env(safe-area-inset-bottom, 0px);
}

* { box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }

body {
  background: var(--bg);
  color: var(--text);
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
  -webkit-font-smoothing: antialiased;
}

.app-shell {
  display: flex;
  flex-direction: column;
  height: 100dvh;
  max-width: 480px;
  margin: 0 auto;
  position: relative;
}

.page-content {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding-bottom: calc(var(--nav-height) + var(--safe-bottom));
}

.bottom-nav {
  position: fixed;
  bottom: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 100%;
  max-width: 480px;
  height: calc(var(--nav-height) + var(--safe-bottom));
  padding-bottom: var(--safe-bottom);
  background: var(--surface);
  border-top: 1px solid var(--border);
  display: flex;
  align-items: flex-start;
  justify-content: space-around;
  padding-top: 8px;
  z-index: 100;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3px;
  text-decoration: none;
  color: var(--text-muted);
  flex: 1;
  padding: 4px 0;
  transition: color 0.2s;
}

.nav-item.active { color: var(--primary-light); }

.nav-icon { font-size: 1.35rem; line-height: 1; }

.nav-label { font-size: 0.65rem; font-weight: 500; }

/* Page transitions */
.slide-enter-active,
.slide-leave-active { transition: opacity 0.18s ease; }
.slide-enter-from,
.slide-leave-to { opacity: 0; }

/* Shared page styles */
.page {
  min-height: 100%;
  padding: 20px 16px;
}

.page-header {
  margin-bottom: 24px;
}

.page-title {
  font-size: 1.6rem;
  font-weight: 800;
  background: linear-gradient(135deg, #805AD5, #667eea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.page-sub {
  color: var(--text-muted);
  font-size: 0.9rem;
  margin-top: 4px;
}

.card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  margin-bottom: 16px;
}

.btn {
  display: block;
  width: 100%;
  padding: 14px;
  border-radius: 14px;
  border: none;
  font-size: 1rem;
  font-weight: 700;
  cursor: pointer;
  transition: opacity 0.2s;
}

.btn:active { opacity: 0.8; }

.btn-primary {
  background: linear-gradient(135deg, #805AD5, #667eea);
  color: white;
}

.btn-ghost {
  background: transparent;
  border: 1px solid var(--border);
  color: var(--text-sub);
}

.input-group {
  margin-bottom: 14px;
}

.input-group label {
  display: block;
  font-size: 0.85rem;
  color: var(--text-sub);
  margin-bottom: 6px;
}

.input-group input,
.input-group textarea {
  width: 100%;
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 12px;
  padding: 12px 14px;
  color: var(--text);
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s;
}

.input-group input:focus,
.input-group textarea:focus {
  border-color: var(--primary);
}

.input-group textarea {
  resize: none;
  min-height: 90px;
  font-family: inherit;
}
</style>
