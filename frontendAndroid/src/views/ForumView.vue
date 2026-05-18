<template>
  <div class="page">
    <div class="page-header">
      <div class="header-row">
        <div>
          <h1 class="page-title">Форум</h1>
          <p class="page-sub">Сообщество поддержки</p>
        </div>
        <button class="new-btn" @click="showCreate = true">+</button>
      </div>
    </div>

    <div v-if="isLoading" class="center-loader">
      <div class="loader"></div>
    </div>

    <div v-else-if="threads.length === 0" class="empty-state">
      <span>💬</span>
      <p>Тем пока нет. Создайте первую!</p>
    </div>

    <div v-else class="thread-list">
      <div
        v-for="thread in threads"
        :key="thread.id"
        class="card thread-card"
        @click="$router.push(`/forum/${thread.id}`)"
      >
        <div class="thread-top">
          <span class="thread-author">{{ thread.is_anonymous ? 'Аноним' : thread.author_name }}</span>
          <span class="thread-rating" :class="thread.rating > 0 ? 'pos' : thread.rating < 0 ? 'neg' : ''">
            {{ thread.rating > 0 ? '+' : '' }}{{ thread.rating }}
          </span>
        </div>
        <h3 class="thread-title">{{ thread.title }}</h3>
        <p class="thread-preview">{{ thread.content.slice(0, 100) }}{{ thread.content.length > 100 ? '...' : '' }}</p>
        <div class="thread-meta">
          <span>💬 {{ thread.comments_count }}</span>
          <span>{{ formatDate(thread.created_at) }}</span>
        </div>
      </div>
    </div>

    <!-- Create thread modal -->
    <div class="modal-overlay" v-if="showCreate" @click.self="showCreate = false">
      <div class="modal">
        <h3 class="modal-title">Новая тема</h3>
        <div class="input-group">
          <label>Заголовок</label>
          <input v-model="newThread.title" placeholder="О чём хотите поговорить?" />
        </div>
        <div class="input-group">
          <label>Содержание</label>
          <textarea v-model="newThread.content" placeholder="Поделитесь своими мыслями..."></textarea>
        </div>
        <label class="toggle-row">
          <input type="checkbox" v-model="newThread.is_anonymous" />
          <span>Анонимно</span>
        </label>
        <p class="error-msg" v-if="createError">{{ createError }}</p>
        <div class="modal-actions">
          <button class="btn btn-ghost" @click="showCreate = false">Отмена</button>
          <button class="btn btn-primary" @click="createThread" :disabled="creating">
            {{ creating ? '...' : 'Создать' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api/api';

export default {
  name: 'ForumView',
  data() {
    return {
      threads: [],
      isLoading: true,
      showCreate: false,
      creating: false,
      createError: '',
      newThread: { title: '', content: '', is_anonymous: false, is_public: true },
    };
  },
  async mounted() {
    await this.loadThreads();
  },
  methods: {
    async loadThreads() {
      this.isLoading = true;
      try {
        const res = await api.getThreads();
        this.threads = res.data || [];
      } catch { this.threads = []; }
      finally { this.isLoading = false; }
    },
    async createThread() {
      if (!this.newThread.title.trim() || !this.newThread.content.trim()) {
        this.createError = 'Заполните заголовок и содержание';
        return;
      }
      this.creating = true;
      this.createError = '';
      try {
        await api.createThread(this.newThread);
        this.showCreate = false;
        this.newThread = { title: '', content: '', is_anonymous: false, is_public: true };
        await this.loadThreads();
      } catch {
        this.createError = 'Ошибка при создании темы';
      } finally {
        this.creating = false;
      }
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' });
    },
  },
};
</script>

<style scoped>
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.new-btn {
  width: 40px;
  height: 40px;
  border-radius: 50%;
  background: var(--primary);
  color: white;
  font-size: 1.5rem;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}

.center-loader {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}

.loader {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(128, 90, 213, 0.2);
  border-top-color: #805AD5;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 60px 20px;
  color: var(--text-muted);
  font-size: 0.9rem;
}
.empty-state span { font-size: 2.5rem; }

.thread-list { display: flex; flex-direction: column; gap: 12px; }

.thread-card { cursor: pointer; }
.thread-card:active { opacity: 0.85; }

.thread-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.thread-author { font-size: 0.8rem; color: var(--text-muted); }

.thread-rating {
  font-size: 0.82rem;
  font-weight: 700;
  color: var(--text-muted);
}
.thread-rating.pos { color: var(--success); }
.thread-rating.neg { color: var(--danger); }

.thread-title {
  font-size: 1rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 6px;
  line-height: 1.3;
}

.thread-preview {
  font-size: 0.85rem;
  color: var(--text-sub);
  line-height: 1.4;
  margin-bottom: 10px;
}

.thread-meta {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: var(--text-muted);
}

/* Modal */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: flex-end;
  z-index: 200;
}

.modal {
  background: var(--surface);
  border-radius: 24px 24px 0 0;
  padding: 24px 20px calc(24px + env(safe-area-inset-bottom, 0px));
  width: 100%;
}

.modal-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 16px;
}

.toggle-row {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-sub);
  font-size: 0.9rem;
  margin-bottom: 16px;
  cursor: pointer;
}

.modal-actions {
  display: flex;
  gap: 10px;
}

.modal-actions .btn {
  flex: 1;
}

.error-msg {
  color: var(--danger);
  font-size: 0.82rem;
  margin-bottom: 10px;
}
</style>
