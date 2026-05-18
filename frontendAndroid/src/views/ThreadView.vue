<template>
  <div class="page">
    <button class="back-btn" @click="$router.back()">← Назад</button>

    <div v-if="isLoading" class="center-loader">
      <div class="loader"></div>
    </div>

    <template v-else-if="thread">
      <div class="card thread-body">
        <div class="thread-meta-top">
          <span class="thread-author">{{ thread.is_anonymous ? 'Аноним' : thread.author_name }}</span>
          <span class="thread-date">{{ formatDate(thread.created_at) }}</span>
        </div>
        <h2 class="thread-title">{{ thread.title }}</h2>
        <p class="thread-content">{{ thread.content }}</p>
        <div class="vote-row">
          <button class="vote-btn" @click="vote(1)" :class="{ active: thread.user_vote === 1 }">👍</button>
          <span class="rating" :class="thread.rating > 0 ? 'pos' : thread.rating < 0 ? 'neg' : ''">
            {{ thread.rating }}
          </span>
          <button class="vote-btn" @click="vote(-1)" :class="{ active: thread.user_vote === -1 }">👎</button>
        </div>
      </div>

      <div class="comments-header">
        <span>Комментарии ({{ comments.length }})</span>
      </div>

      <div class="comment-list">
        <div v-for="c in comments" :key="c.id" class="card comment-card">
          <div class="comment-top">
            <span class="comment-author">{{ c.author_name || 'Аноним' }}</span>
            <span class="comment-date">{{ formatDate(c.created_at) }}</span>
          </div>
          <p class="comment-text">{{ c.content }}</p>
        </div>

        <div v-if="comments.length === 0" class="empty-comments">
          Комментариев пока нет. Будьте первым!
        </div>
      </div>

      <div class="add-comment card">
        <div class="input-group">
          <textarea v-model="newComment" placeholder="Написать комментарий..." rows="3"></textarea>
        </div>
        <label class="toggle-row">
          <input type="checkbox" v-model="isAnonymous" />
          <span>Анонимно</span>
        </label>
        <button class="btn btn-primary" @click="addComment" :disabled="!newComment.trim() || posting">
          {{ posting ? '...' : 'Отправить' }}
        </button>
      </div>
    </template>
  </div>
</template>

<script>
import api from '@/api/api';

export default {
  name: 'ThreadView',
  data() {
    return {
      thread: null,
      comments: [],
      isLoading: true,
      newComment: '',
      isAnonymous: false,
      posting: false,
    };
  },
  async mounted() {
    const id = this.$route.params.id;
    try {
      const [t, c] = await Promise.all([api.getThreadById(id), api.getComments(id)]);
      this.thread = t.data;
      this.comments = c.data || [];
    } catch { /* */ }
    finally { this.isLoading = false; }
  },
  methods: {
    async vote(value) {
      if (!this.thread) return;
      try {
        await api.voteThread(this.thread.id, value);
        const res = await api.getThreadById(this.thread.id);
        this.thread = res.data;
      } catch { /* */ }
    },
    async addComment() {
      if (!this.newComment.trim()) return;
      this.posting = true;
      try {
        await api.createComment(this.thread.id, { content: this.newComment, is_anonymous: this.isAnonymous });
        const res = await api.getComments(this.thread.id);
        this.comments = res.data || [];
        this.newComment = '';
      } catch { /* */ }
      finally { this.posting = false; }
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' });
    },
  },
};
</script>

<style scoped>
.back-btn {
  background: none;
  border: none;
  color: var(--primary-light);
  font-size: 0.95rem;
  cursor: pointer;
  margin-bottom: 16px;
  padding: 0;
}

.center-loader {
  display: flex;
  justify-content: center;
  padding: 60px 0;
}
.loader {
  width: 32px; height: 32px;
  border: 3px solid rgba(128,90,213,0.2);
  border-top-color: #805AD5;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

.thread-meta-top {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: var(--text-muted);
  margin-bottom: 10px;
}

.thread-title {
  font-size: 1.15rem;
  font-weight: 800;
  color: var(--text);
  margin-bottom: 12px;
  line-height: 1.3;
}

.thread-content {
  color: var(--text-sub);
  font-size: 0.92rem;
  line-height: 1.6;
  margin-bottom: 16px;
}

.vote-row {
  display: flex;
  align-items: center;
  gap: 14px;
}

.vote-btn {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 10px;
  padding: 6px 12px;
  font-size: 1rem;
  cursor: pointer;
  transition: border-color 0.2s;
}
.vote-btn.active { border-color: var(--primary); }

.rating { font-size: 1rem; font-weight: 700; color: var(--text-sub); }
.rating.pos { color: var(--success); }
.rating.neg { color: var(--danger); }

.comments-header {
  font-size: 0.85rem;
  color: var(--text-muted);
  margin-bottom: 10px;
  padding: 0 4px;
}

.comment-list { display: flex; flex-direction: column; gap: 10px; margin-bottom: 16px; }

.comment-card { padding: 14px; }

.comment-top {
  display: flex;
  justify-content: space-between;
  font-size: 0.78rem;
  color: var(--text-muted);
  margin-bottom: 8px;
}

.comment-text { font-size: 0.9rem; color: var(--text-sub); line-height: 1.5; }

.empty-comments {
  text-align: center;
  color: var(--text-muted);
  font-size: 0.85rem;
  padding: 20px 0;
}

.add-comment { }

.toggle-row {
  display: flex;
  align-items: center;
  gap: 10px;
  color: var(--text-sub);
  font-size: 0.85rem;
  margin-bottom: 12px;
  cursor: pointer;
}

.btn:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
