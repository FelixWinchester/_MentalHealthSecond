<template>
  <div class="thread-details-container" v-if="thread">
    <button class="back-btn" @click="$router.push('/forum')">
      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor">
        <path d="M19 12H5M12 19l-7-7 7-7" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
      </svg>
      Назад к списку
    </button>

    <article class="main-post">
      <div class="post-header">
        <div class="user-meta">
          <div class="avatar-small" :class="{ anon: thread.is_anonymous }">
            {{ thread.is_anonymous ? '?' : (thread.author_name?.[0] || 'U').toUpperCase() }}
          </div>
          <div>
            <div class="author-name">{{ thread.is_anonymous ? 'Анонимный пользователь' : thread.author_name }}</div>
            <div class="post-time">{{ formatDate(thread.created_at) }}</div>
          </div>
        </div>
        <div class="post-rating">
        
          <button class="v-btn" @click="handleVote(1)" :class="{ active: thread.user_vote === 1 }">▲</button>
          <span class="count">{{ thread.rating }}</span>
          <button class="v-btn" @click="handleVote(-1)" :class="{ active: thread.user_vote === -1 }">▼</button>
        </div>
      </div>

      <h1 class="post-title">{{ thread.title }}</h1>
      <div class="post-body">{{ thread.content }}</div>
    </article>

    <section class="comments-section">
      <h3 class="comments-title">Ответы ({{ comments.length }})</h3>

      <div class="comments-list">
        <div v-for="comment in comments" :key="comment.id" class="comment-item">
          <div class="comment-bubble">
            <div class="comment-meta">
              <span class="c-author">{{ comment.is_anonymous ? 'Аноним' : comment.author_name }}</span>
              <span class="c-date">{{ formatDate(comment.created_at) }}</span>
            </div>
            <p class="c-text">{{ comment.content }}</p>
          </div>
        </div>
      </div>

      <div class="comment-input-area">
        <div class="input-wrapper">
          <textarea 
            v-model="newCommentText" 
            placeholder="Напишите ваш ответ..." 
            @keypress.enter.prevent="submitComment"
          ></textarea>
          <div class="input-actions">
            <label class="anon-toggle">
              <input type="checkbox" v-model="commentIsAnonymous">
              <span>Анонимно</span>
            </label>
            <button class="send-comment-btn" :disabled="!newCommentText.trim()" @click="submitComment">
              Отправить
            </button>
          </div>
        </div>
      </div>
    </section>
  </div>
  
  <div v-else class="loading-state">
     <div class="spinner"></div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api/api';

export default {
  setup() {
    const route = useRoute();
    const thread = ref(null);
    const comments = ref([]);
    const newCommentText = ref('');
    const commentIsAnonymous = ref(false);

    const loadData = async () => {
      const threadId = route.params.id;
      try {
        const [threadRes, commentsRes] = await Promise.all([
          api.getThreadById(threadId),
          api.getComments(threadId)
        ]);
        thread.value = threadRes.data;
        comments.value = commentsRes.data;
      } catch (err) {
        console.error("Ошибка загрузки данных треда", err);
      }
    };

    const handleVote = async (val) => {
  try {
    const res = await api.voteThread(thread.value.id, val);
    
    // Бэкенд должен вернуть объект с актуальными данными
    // Например: { total_rating: 15, user_vote: 1 }
    thread.value.rating = res.data.total_rating;
    thread.value.user_vote = res.data.user_vote;
    
  } catch (e) {
    if (e.response?.status === 401) {
      alert("Нужно войти в аккаунт, чтобы голосовать");
    } else {
      alert("Ошибка при сохранении голоса");
    }
  }
};

    const submitComment = async () => {
      if (!newCommentText.value.trim()) return;
      try {
        const res = await api.createComment(thread.value.id, {
          content: newCommentText.value,
          is_anonymous: commentIsAnonymous.value
        });
        comments.value.push(res.data);
        newCommentText.value = '';
      } catch (e) { alert("Не удалось отправить комментарий"); }
    };

    const formatDate = (d) => new Date(d).toLocaleString('ru-RU', { day: 'numeric', month: 'short', hour: '2-digit', minute: '2-digit' });

    onMounted(loadData);

    return {
      thread, comments, newCommentText, commentIsAnonymous,
      handleVote, submitComment, formatDate
    };
  }
}
</script>

<style scoped>
.thread-details-container {
  max-width: 800px;
  margin: 0 auto;
  padding: 40px 20px;
}

.back-btn {
  display: flex;
  align-items: center;
  gap: 8px;
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  margin-bottom: 20px;
  transition: color 0.3s;
}

.back-btn:hover { color: #6366f1; }

/* Карточка основного поста */
.main-post {
  background: rgba(30, 41, 59, 0.4);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 24px;
  padding: 30px;
  margin-bottom: 40px;
}

.post-header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}

.user-meta {
  display: flex;
  gap: 12px;
  align-items: center;
}

.avatar-small {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  background: linear-gradient(135deg, #6366f1, #a78bfa);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

.avatar-small.anon { background: #475569; }

.author-name { font-weight: 600; color: #f1f5f9; }
.post-time { font-size: 0.8rem; color: #64748b; }

.post-title {
  font-size: 1.8rem;
  margin-bottom: 15px;
  line-height: 1.3;
}

.post-body {
  line-height: 1.6;
  color: #cbd5e1;
  white-space: pre-wrap;
}

/* Комментарии */
.comments-title {
  margin-bottom: 20px;
  font-size: 1.2rem;
  color: #94a3b8;
}

.comment-item {
  margin-bottom: 15px;
  display: flex;
}

.comment-bubble {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 18px;
  border-bottom-left-radius: 4px;
  padding: 15px 20px;
  max-width: 85%;
}

.comment-meta {
  display: flex;
  gap: 10px;
  font-size: 0.8rem;
  margin-bottom: 5px;
}

.c-author { color: #818cf8; font-weight: 600; }
.c-date { color: #475569; }

/* Поле ввода */
.comment-input-area {
  margin-top: 30px;
  background: rgba(15, 23, 42, 0.3);
  border-radius: 20px;
  padding: 20px;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.input-wrapper textarea {
  width: 100%;
  background: transparent;
  border: none;
  color: white;
  resize: none;
  height: 80px;
  outline: none;
  font-family: inherit;
  font-size: 1rem;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
  padding-top: 10px;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.send-comment-btn {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 10px;
  cursor: pointer;
  font-weight: 600;
}

.anon-toggle {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: #94a3b8;
  cursor: pointer;
}
</style>