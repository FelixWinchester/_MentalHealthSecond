<template>
  <div class="forum-container">
    <header class="forum-header">
      <h1 class="page-title">Сообщество</h1>
      <p class="page-subtitle">Делитесь опытом и поддерживайте друг друга</p>
    </header>

    <div class="forum-actions">
      <div class="filter-group">
        <button 
          class="filter-btn" 
          :class="{ active: currentFilter === 'all' }"
          @click="currentFilter = 'all'"
        >
          Все темы
        </button>
        <button 
          class="filter-btn" 
          :class="{ active: currentFilter === 'popular' }"
          @click="currentFilter = 'popular'"
        >
          Популярное
        </button>
      </div>
      
      <button class="create-thread-btn" @click="showCreateModal = true">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5">
          <line x1="12" y1="5" x2="12" y2="19"></line>
          <line x1="5" y1="12" x2="19" y2="12"></line>
        </svg>
        Создать тему
      </button>
    </div>

    <div v-if="loading" class="loading-state">
      <div class="spinner"></div>
    </div>

    <div v-else class="threads-list">
      <div 
        v-for="thread in filteredThreads" 
        :key="thread.id" 
        class="thread-card"
        @click="$router.push(`/forum/thread/${thread.id}`)"
      >
        <div class="thread-content">
          <div class="thread-meta">
            <span class="author-tag" :class="{ anon: thread.is_anonymous }">
              {{ thread.is_anonymous ? 'Анонимно' : thread.author_name }}
            </span>
            <span class="dot">•</span>
            <span class="date-tag">{{ formatDate(thread.created_at) }}</span>
          </div>
          <h2 class="thread-title">{{ thread.title }}</h2>
          <p class="thread-preview">{{ truncate(thread.content, 120) }}</p>
          
          <div class="thread-footer">
            <div class="stat">
              <span class="icon">💬</span>
              {{ thread.comments_count || 0 }} ответов
            </div>
            <div class="stat">
              <span class="icon">🔥</span>
              Рейтинг: {{ thread.rating }}
            </div>
          </div>
        </div>
      </div>
    </div>

    <div v-if="showCreateModal" class="modal-overlay" @click.self="showCreateModal = false">
      <div class="modal-content">
        <div class="modal-header">
          <h2>Новая тема</h2>
          <button class="close-btn" @click="showCreateModal = false">&times;</button>
        </div>
        
        <div class="modal-body">
          <div class="input-group">
            <label>Заголовок</label>
            <input v-model="newThread.title" placeholder="О чем вы хотите поговорить?" />
          </div>
          
          <div class="input-group">
            <label>Сообщение</label>
            <textarea v-model="newThread.content" placeholder="Опишите вашу ситуацию..."></textarea>
          </div>
          
          <div class="modal-footer">
            <label class="anon-checkbox">
              <input type="checkbox" v-model="newThread.is_anonymous">
              <span>Опубликовать анонимно</span>
            </label>
            <button class="submit-btn" :disabled="!isFormValid" @click="handleCreateThread">
              Опубликовать
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { ref, computed, onMounted } from 'vue';
import api from '@/api/api';

export default {
  setup() {
    const threads = ref([]);
    const loading = ref(true);
    const currentFilter = ref('all');
    
    // Состояние модалки
    const showCreateModal = ref(false);
    const newThread = ref({
      title: '',
      content: '',
      is_anonymous: false
    });

    const fetchThreads = async () => {
      try {
        loading.value = true;
        const res = await api.getThreads();
        threads.value = res.data;
      } catch (err) {
        console.error("Ошибка загрузки форума:", err);
      } finally {
        loading.value = false;
      }
    };

    const handleCreateThread = async () => {
      try {
        const res = await api.createThread(newThread.value);
        threads.value.unshift(res.data); // Добавляем новую тему в начало списка
        showCreateModal.value = false; // Закрываем окно
        // Сброс формы
        newThread.value = { title: '', content: '', is_anonymous: false };
      } catch (err) {
        alert("Ошибка при создании темы. Проверьте авторизацию.");
      }
    };

    const isFormValid = computed(() => {
      return newThread.value.title.trim().length > 3 && 
             newThread.value.content.trim().length > 10;
    });

    const filteredThreads = computed(() => {
      if (currentFilter.value === 'popular') {
        return [...threads.value].sort((a, b) => b.rating - a.rating);
      }
      return threads.value;
    });

    const formatDate = (d) => {
      return new Date(d).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long' });
    };

    const truncate = (text, length) => {
      if (text.length <= length) return text;
      return text.substring(0, length) + '...';
    };

    onMounted(fetchThreads);

    return {
      threads, loading, currentFilter, filteredThreads,
      showCreateModal, newThread, isFormValid,
      formatDate, truncate, handleCreateThread
    };
  }
};
</script>

<style scoped>
/* ... (предыдущие стили из ForumView) ... */

.forum-container { max-width: 1000px; margin: 0 auto; }
.forum-header { margin-bottom: 2.5rem; }
.page-title { font-size: 2.5rem; font-weight: 800; background: linear-gradient(135deg, #fff 0%, #cbd5e1 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.page-subtitle { color: #94a3b8; }
.forum-actions { display: flex; justify-content: space-between; margin-bottom: 2rem; }
.filter-group { display: flex; gap: 0.5rem; background: rgba(30, 41, 59, 0.4); padding: 0.4rem; border-radius: 14px; border: 1px solid rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); }
.filter-btn { background: transparent; border: none; color: #94a3b8; padding: 0.6rem 1.2rem; border-radius: 10px; cursor: pointer; transition: 0.3s; }
.filter-btn.active { background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); color: white; }
.create-thread-btn { background: linear-gradient(135deg, #818cf8 0%, #f472b6 100%); color: white; border: none; padding: 0.8rem 1.5rem; border-radius: 12px; font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 10px; }

/* КАРТОЧКИ ТРЕДОВ */
.thread-card { background: rgba(30, 41, 59, 0.4); border: 1px solid rgba(255, 255, 255, 0.05); border-radius: 20px; padding: 1.5rem; margin-bottom: 1rem; cursor: pointer; transition: 0.3s; backdrop-filter: blur(10px); }
.thread-card:hover { background: rgba(45, 55, 72, 0.6); transform: translateX(8px); }
.thread-title { font-size: 1.4rem; color: #f8fafc; margin: 0.5rem 0; }

/* СТИЛИ МОДАЛЬНОГО ОКНА */
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(8px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 2000;
}

.modal-content {
  background: #1e293b;
  width: 100%;
  max-width: 600px;
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.1);
  padding: 2rem;
  box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.5);
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  font-size: 2rem;
  cursor: pointer;
}

.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #94a3b8;
  font-size: 0.9rem;
}

.input-group input, .input-group textarea {
  width: 100%;
  background: rgba(15, 23, 42, 0.5);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 12px;
  padding: 1rem;
  color: white;
  font-family: inherit;
}

.input-group textarea { height: 150px; resize: none; }

.modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 2rem;
}

.anon-checkbox {
  display: flex;
  align-items: center;
  gap: 10px;
  color: #94a3b8;
  cursor: pointer;
}

.submit-btn {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  border: none;
  padding: 0.8rem 2rem;
  border-radius: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}
</style>