<template>
  <div class="condition-page">
    <!-- Основной контент -->
    <main class="content">
      <!-- Герой секция -->
      <section class="hero-section">
        <div class="hero-content">
          <h1>Отслеживайте ваше эмоциональное состояние</h1>
          <p class="hero-subtitle">Записывайте мысли, отслеживайте настроение и наблюдайте за прогрессом</p>
          <div class="hero-actions">
            <button class="cta-button primary" @click="showEmojiModal = true">
              <span class="button-icon">🎯</span>
              Оценить состояние
            </button>
            <button class="cta-button secondary" @click="scrollToNotes">
              <span class="button-icon">📝</span>
              Мои записи
            </button>
          </div>
        </div>
        <div class="hero-visual">
          <div class="floating-card card-1">
            <div class="card-icon">📊</div>
            <p>Анализ прогресса</p>
          </div>
          <div class="floating-card card-2">
            <div class="card-icon">💭</div>
            <p>Личные заметки</p>
          </div>
          <div class="floating-card card-3">
            <div class="card-icon">🎭</div>
            <p>Эмоции и настроение</p>
          </div>
        </div>
      </section>

      <!-- Секция с заметками -->
      <section class="notes-section" id="notes-section">
        <div class="notes-container">
          <h2>Мои записи о состоянии</h2>
          <p class="section-description">История ваших мыслей и эмоциональных состояний</p>
          
          <div class="notes-list" v-if="notes.length > 0">
            <div v-for="(note, index) in notes" :key="index" class="note-card">
              <div class="note-content">
                <p>{{ note.text }}</p>
              </div>
              <div class="note-date">
                {{ formatDate(note.created_at) }}
              </div>
            </div>
          </div>
          
          <div class="empty-state" v-else>
            <div class="empty-icon">📝</div>
            <h3>Пока нет записей</h3>
            <p>Начните отслеживать ваше состояние, чтобы видеть здесь историю</p>
            <button class="outline-button" @click="showEmojiModal = true">
              Создать первую запись
            </button>
          </div>
        </div>
      </section>

      <!-- Быстрый доступ к текущему состоянию -->
      <section class="quick-access-section">
        <div class="quick-access-container">
          <h2>Текущее состояние</h2>
          <p class="section-description">Ваша текущая эмоция и быстрый ввод</p>
          
          <div class="current-state-card">
            <div class="state-visual">
              <div class="current-emoji-display" @click="showEmojiModal = true">
                <div class="emoji-circle">
                  <img 
                    :src="selectedEmoji?.icon || questionEmoji.icon" 
                    :alt="selectedEmoji?.name || questionEmoji.name"
                    class="emoji-icon-large"
                  >
                </div>
                <div class="emoji-info">
                  <h3>{{ selectedEmoji?.displayName || questionEmoji.displayName }}</h3>
                  <p>{{ getEmojiDescription(selectedEmoji?.name) }}</p>
                </div>
              </div>
            </div>
            
            <div class="quick-input">
              <div class="input-wrapper">
                <textarea 
                  v-model="newNote" 
                  placeholder="Опишите, что вы чувствуете или о чем думаете..."
                  class="note-input"
                  rows="3"
                ></textarea>
                <button @click="saveState" class="send-button">
                  <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                    <path d="M22 2L11 13" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M22 2L15 22L11 13L2 9L22 2Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </button>
              </div>
              <div class="input-hint">
                Нажмите Enter или кнопку отправки для сохранения
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- Модальное окно для выбора эмоций -->
      <div v-if="showEmojiModal" class="emoji-modal-overlay" @click.self="closeEmojiModal">
        <div class="emoji-modal">
          <div class="emoji-modal-header">
            <h3>Как вы себя чувствуете сейчас?</h3>
            <p class="modal-subtitle">Выберите эмоцию, которая лучше всего описывает ваше состояние</p>
            <button @click="closeEmojiModal" class="close-button">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
              </svg>
            </button>
          </div>
          
          <div class="emoji-modal-content">
            <div class="emoji-categories">
              <div class="category-tabs">
                <button 
                  v-for="category in emotionCategories" 
                  :key="category.id"
                  @click="activeCategory = category.id"
                  :class="['category-tab', { 'active': activeCategory === category.id }]"
                >
                  {{ category.name }}
                </button>
              </div>
              
              <div class="emoji-grid">
                <button 
                  v-for="emoji in getCategoryEmojis" 
                  :key="emoji.id"
                  @click="selectEmoji(emoji)"
                  class="emoji-option"
                  :class="{ 'selected': selectedEmoji?.id === emoji.id }"
                >
                  <div class="emoji-visual">
                    <img 
                      :src="emoji.icon" 
                      :alt="emoji.name"
                      class="emoji-icon"
                    >
                  </div>
                  <span class="emoji-name">{{ emoji.displayName }}</span>
                </button>
              </div>
            </div>
            
            <div class="selected-preview">
              <div class="preview-header">
                <h4>Ваш выбор</h4>
              </div>
              <div class="preview-content">
                <div class="selected-emoji-preview">
                  <div class="preview-emoji">
                    <img 
                      v-if="selectedEmoji" 
                      :src="selectedEmoji.icon" 
                      :alt="selectedEmoji.name"
                      class="emoji-icon-large"
                    >
                    <img 
                      v-else
                      :src="questionEmoji.icon" 
                      :alt="questionEmoji.name"
                      class="emoji-icon-large"
                    >
                  </div>
                  <div class="preview-info">
                    <h3>{{ selectedEmoji?.displayName || 'Не выбрано' }}</h3>
                    <p class="emoji-description">
                      {{ getEmojiDescription(selectedEmoji?.name) }}
                    </p>
                  </div>
                </div>
                
                <div class="preview-actions">
                  <button 
                    v-if="selectedEmoji"
                    @click="clearEmoji"
                    class="action-button secondary"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Сбросить
                  </button>
                  <button 
                    @click="saveState"
                    class="action-button primary"
                    :disabled="!selectedEmoji"
                  >
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none">
                      <path d="M20 6L9 17L4 12" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                    Сохранить состояние
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import api from '@/api/api';

export default {
  name: 'ConditionPage',
  data() {
    return {
      pageTitle: 'Мое состояние',
      loading: true,
      newNote: '',
      notes: [],
      emojis: [
        { 
            id: 1, 
            name: 'HAPPY', 
            displayName: 'Счастье',
            icon: '/emojis/happy.png',
            code: '😀',
            category: 'positive'
        },
        { 
            id: 2, 
            name: 'EXCITED',
            displayName: 'Возбуждение', 
            icon: '/emojis/excited.png',
            code: '🤩',
            category: 'positive'
        },
        { 
            id: 3, 
            name: 'SATISFIED',
            displayName: 'Удовлетворение', 
            icon: '/emojis/satisfied.png',
            code: '😌',
            category: 'positive'
        },
        { 
            id: 4, 
            name: 'JOYFUL', 
            displayName: 'Радость',
            icon: '/emojis/joyful.png',
            code: '😊',
            category: 'positive'
        },
        { 
            id: 5, 
            name: 'MISUNDERSTANDING', 
            displayName: 'Непонимание',
            icon: '/emojis/misunderstanding.png',
            code: '😐',
            category: 'neutral'
        },
        { 
            id: 6, 
            name: 'WORRIED', 
            displayName: 'Беспокойство',
            icon: '/emojis/worried.png',
            code: '😟',
            category: 'negative'
        },
        { 
            id: 7, 
            name: 'SAD', 
            displayName: 'Грусть',
            icon: '/emojis/sad.png',
            code: '😢',
            category: 'negative'
        },
        { 
            id: 8, 
            name: 'DEPRESSED', 
            displayName: 'Уныние',
            icon: '/emojis/depressed.png',
            code: '😞',
            category: 'negative'
        },
        { 
            id: 9, 
            name: 'ANGRY', 
            displayName: 'Злость',
            icon: '/emojis/angry.png',
            code: '😠',
            category: 'negative'
        },
        { 
            id: 10, 
            name: 'question', 
            displayName: 'Не оценено',
            icon: '/emojis/question.png',
            code: '❓',
            isQuestion: true
        },
      ],
      selectedEmoji: null,
      showEmojiModal: false,
      activeCategory: 'all',
      emotionCategories: [
        { id: 'all', name: 'Все эмоции' },
        { id: 'positive', name: 'Позитивные' },
        { id: 'neutral', name: 'Нейтральные' },
        { id: 'negative', name: 'Плохие' }
      ]
    };
  },
  computed: {
    questionEmoji() {
      return this.emojis.find(e => e.isQuestion);
    },

    filteredEmojis() {
      return this.emojis.filter(e => !e.isQuestion);
    },

    getCategoryEmojis() {
      if (this.activeCategory === 'all') {
        return this.filteredEmojis;
      }
      return this.filteredEmojis.filter(emoji => emoji.category === this.activeCategory);
    }
  },
  async created() {
    await this.fetchData();
  },
  methods: {
    getEmojiDescription(emojiName) {
      const descriptions = {
        'HAPPY': 'Чувство радости и удовлетворения',
        'EXCITED': 'Энергичное ожидание и восторг',
        'SATISFIED': 'Спокойное удовлетворение и гармония',
        'JOYFUL': 'Яркое чувство счастья и веселья',
        'MISUNDERSTANDING': 'Неопределенность и поиск ответов',
        'WORRIED': 'Тревога и беспокойство о будущем',
        'SAD': 'Грусть и легкая тоска',
        'DEPRESSED': 'Глубокое уныние и подавленность',
        'ANGRY': 'Раздражение и злость'
      };
      return descriptions[emojiName] || 'Выберите эмоцию для описания';
    },

    formatDate(dateString) {
      if (!dateString) return 'Сегодня';
      const date = new Date(dateString);
      return date.toLocaleDateString('ru-RU', {
        day: 'numeric',
        month: 'long',
        hour: '2-digit',
        minute: '2-digit'
      });
    },

    scrollToNotes() {
      const element = document.getElementById('notes-section');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    },

    async fetchData() {
        this.loading = true;
        try {
            const notesResponse = await api.getNotes();
            this.notes = notesResponse.data.map(note => ({ 
              text: note.details,
              created_at: note.created_at 
            }));

            try {
                const todaysMoodResponse = await api.getTodaysMood();
                const moodData = todaysMoodResponse.data;
                
                if (moodData) {
                    this.selectedEmoji = this.emojis.find(e => e.name === moodData.mood);
                    this.newNote = moodData.details || '';
                }
            } catch (error) {
                if (error.response?.status !== 404) {
                    console.error('Ошибка загрузки состояния за сегодня:', error);
                }
            }

        } catch (error) {
            console.error('Ошибка загрузки данных:', error);
            if (error.response?.status === 401) {
                this.$router.push('/login');
            }
        } finally {
            this.loading = false;
        }
    },

    selectEmoji(emoji) {
        if (this.selectedEmoji?.id === emoji.id) {
            this.selectedEmoji = null;
        } else {
            this.selectedEmoji = emoji;
        }
    },

    async saveState() {
        if (!this.selectedEmoji) {
            alert('Пожалуйста, выберите эмоцию.');
            return;
        }

        try {
            const payload = {
                // Отправляем как есть (на бэкенде ваш отладчик уже умеет кушать любой регистр)
                mood: this.selectedEmoji.name, 
                details: this.newNote.trim()
            };
            
            await api.createMoodEntry(payload);
            
            // Если текст был введен, добавляем его в локальный список сразу
            if (this.newNote.trim()) {
                this.notes.unshift({ 
                    text: this.newNote.trim(),
                    created_at: new Date().toISOString()
                });
            }
            
            this.showEmojiModal = false;
            // Можно вызвать fetchData(), чтобы синхронизировать всё с базой
            // await this.fetchData(); 
            
        } catch (error) {
            console.error('Ошибка сохранения:', error);
            alert('Не удалось сохранить.');
        }
},
    
    async clearEmoji() {
      this.selectedEmoji = null;
      this.newNote = '';
      try {
        await api.createMoodEntry({
          mood: '',
          details: ''
        });
      } catch (error) {
        console.error('Ошибка очистки эмоции:', error);
      }
    },

    closeEmojiModal() {
      this.showEmojiModal = false;
    }
  }
};
</script>

<style scoped>
/* Основные стили из главной страницы */
.condition-page {
  color: #e2e8f0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  line-height: 1.6;
}

.content {
  position: relative;
  z-index: 2;
  width: 100%;
  box-sizing: border-box;
  margin: 0;
  padding: 0rem 5vw;
}

section {
  margin-bottom: 8rem;
}

h2 {
  text-align: center;
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  margin-bottom: 1rem;
  color: #e2e8f0;
  font-weight: 700;
}

.section-description {
  text-align: center;
  color: #94a3b8;
  font-size: clamp(1rem, 2.5vw, 1.2rem);
  margin-bottom: 3rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

/* Герой-секция */
.hero-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  padding: 4rem 0;
  gap: 3rem;
}

.hero-content {
  text-align: center;
  max-width: 900px;
}

.hero-content h1 {
  font-size: clamp(2.5rem, 5vw, 3.5rem);
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: clamp(1.2rem, 2.5vw, 1.5rem);
  color: #cbd5e1;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-button {
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cta-button.primary {
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  color: white;
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(128, 90, 213, 0.4);
}

.cta-button.secondary {
  background: transparent;
  color: #e2e8f0;
  border: 1px solid #805AD5;
}

.cta-button.secondary:hover {
  background: rgba(128, 90, 213, 0.1);
  transform: translateY(-2px);
}

.button-icon {
  font-size: 1.2rem;
}

.hero-visual {
  position: relative;
  width: 100%;
  max-width: 1000px;
  height: 250px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.floating-card {
  position: absolute;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 180px;
  transition: all 0.5s ease;
}

.floating-card:hover {
  transform: translateY(-5px);
}

.card-1 {
  top: 10%;
  left: 10%;
  animation: float 6s ease-in-out infinite;
}

.card-2 {
  top: 20%;
  right: 15%;
  animation: float 7s ease-in-out infinite 1s;
}

.card-3 {
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
  animation: float 8s ease-in-out infinite 2s;
}

.card-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* Секция с заметками */
.notes-section {
  padding: 4rem 0;
}

.notes-container {
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid #334155;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
}

.notes-list {
  display: grid;
  gap: 1.5rem;
  max-height: 500px;
  overflow-y: auto;
  padding-right: 1rem;
}

.note-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 1.5rem;
  transition: all 0.3s ease;
  position: relative;
}

.note-card:hover {
  border-color: #805AD5;
  transform: translateY(-2px);
}

.note-content p {
  color: #e2e8f0;
  line-height: 1.6;
  margin: 0;
}

.note-date {
  color: #94a3b8;
  font-size: 0.9rem;
  margin-top: 0.5rem;
}

.empty-state {
  text-align: center;
  padding: 3rem 2rem;
  color: #94a3b8;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
}

.empty-state h3 {
  color: #e2e8f0;
  margin-bottom: 1rem;
}

.outline-button {
  background: transparent;
  border: 1px solid #805AD5;
  color: #cbd5e1;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  margin-top: 1rem;
}

.outline-button:hover {
  background: rgba(128, 90, 213, 0.1);
  transform: translateY(-2px);
}

/* Секция быстрого доступа */
.quick-access-section {
  padding: 4rem 0;
}

.quick-access-container {
  background: linear-gradient(135deg, rgba(128, 90, 213, 0.05) 0%, rgba(102, 126, 234, 0.05) 100%);
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.current-state-card {
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 2.5rem;
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  align-items: center;
}

.current-emoji-display {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 1rem;
  border-radius: 12px;
}

.current-emoji-display:hover {
  background: rgba(128, 90, 213, 0.1);
}

.emoji-circle {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 1rem;
  box-shadow: 0 8px 25px rgba(128, 90, 213, 0.3);
}

.emoji-icon-large {
  width: 60px;
  height: 60px;
  object-fit: contain;
}

.emoji-info h3 {
  color: #e2e8f0;
  margin-bottom: 0.5rem;
  text-align: center;
}

.emoji-info p {
  color: #94a3b8;
  text-align: center;
  font-size: 0.9rem;
}

.quick-input {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input-wrapper {
  display: flex;
  background: #1e293b;
  border-radius: 12px;
  border: 1px solid #475569;
  transition: all 0.3s ease;
  overflow: hidden;
}

.input-wrapper:focus-within {
  border-color: #805AD5;
  box-shadow: 0 0 0 2px rgba(128, 90, 213, 0.5);
}

.note-input {
  flex-grow: 1;
  background: transparent;
  border: none;
  color: white;
  padding: 1rem;
  font-size: 1rem;
  outline: none;
  resize: vertical;
  min-height: 80px;
  font-family: inherit;
}

.note-input::placeholder {
  color: #64748b;
}

.send-button {
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  border: none;
  color: white;
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-button:hover {
  background: linear-gradient(135deg, #7048c8 0%, #5a6fd8 100%);
}

.send-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.input-hint {
  color: #94a3b8;
  font-size: 0.9rem;
  text-align: center;
}

/* Модальное окно эмоций */
.emoji-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.emoji-modal {
  width: 90vw;
  max-width: 1000px;
  height: 80vh;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 20px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.emoji-modal-header {
  padding: 2rem;
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  color: white;
  position: relative;
}

.emoji-modal-header h3 {
  margin: 0 0 0.5rem 0;
  font-size: 1.5rem;
}

.modal-subtitle {
  margin: 0;
  opacity: 0.9;
  font-size: 1rem;
}

.close-button {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: rgba(255, 255, 255, 0.1);
  border: none;
  border-radius: 8px;
  color: white;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.close-button:hover {
  background: rgba(255, 255, 255, 0.2);
}

.emoji-modal-content {
  flex: 1;
  display: grid;
  grid-template-columns: 2fr 1fr;
  overflow: hidden;
}

.emoji-categories {
  padding: 2rem;
  display: flex;
  flex-direction: column;
  border-right: 1px solid #334155;
}

.category-tabs {
  display: flex;
  gap: 0.5rem;
  margin-bottom: 2rem;
  flex-wrap: wrap;
}

.category-tab {
  background: transparent;
  border: 1px solid #475569;
  color: #94a3b8;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 500;
}

.category-tab:hover {
  border-color: #805AD5;
  color: #e2e8f0;
}

.category-tab.active {
  background: #805AD5;
  border-color: #805AD5;
  color: white;
}

.emoji-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: 1rem;
  overflow-y: auto;
  padding-right: 1rem;
}

.emoji-option {
  background: #0f172a;
  border: 2px solid transparent;
  border-radius: 12px;
  padding: 1.5rem 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
}

.emoji-option:hover {
  border-color: #475569;
  transform: translateY(-2px);
}

.emoji-option.selected {
  border-color: #805AD5;
  background: rgba(128, 90, 213, 0.1);
  transform: translateY(-2px);
}

.emoji-visual {
  width: 50px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.emoji-icon {
  width: 40px;
  height: 40px;
  object-fit: contain;
}

.emoji-name {
  color: #e2e8f0;
  font-weight: 500;
  text-align: center;
  font-size: 0.9rem;
}

.selected-preview {
  padding: 2rem;
  display: flex;
  flex-direction: column;
}

.preview-header {
  margin-bottom: 2rem;
}

.preview-header h4 {
  color: #e2e8f0;
  margin: 0;
  font-size: 1.2rem;
}

.preview-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.selected-emoji-preview {
  text-align: center;
  padding: 2rem 1rem;
  background: rgba(128, 90, 213, 0.05);
  border-radius: 16px;
  border: 1px solid #334155;
}

.preview-emoji {
  margin-bottom: 1.5rem;
}

.preview-info h3 {
  color: #e2e8f0;
  margin-bottom: 0.5rem;
}

.emoji-description {
  color: #94a3b8;
  font-size: 0.9rem;
  line-height: 1.5;
}

.preview-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-button {
  padding: 1rem 1.5rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  border: none;
}

.action-button.primary {
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  color: white;
}

.action-button.primary:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(128, 90, 213, 0.4);
}

.action-button.primary:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
}

.action-button.secondary {
  background: transparent;
  color: #94a3b8;
  border: 1px solid #475569;
}

.action-button.secondary:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: #805AD5;
  color: #e2e8f0;
}

/* Адаптивность */
@media (max-width: 768px) {
  .content {
    padding: 0rem 3vw;
  }

  .hero-section {
    min-height: 60vh;
    padding: 2rem 0;
  }

  .current-state-card {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .emoji-modal-content {
    grid-template-columns: 1fr;
  }

  .emoji-categories {
    border-right: none;
    border-bottom: 1px solid #334155;
  }

  .emoji-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .floating-card {
    position: relative;
    margin-bottom: 1rem;
    left: auto;
    right: auto;
    top: auto;
    bottom: auto;
    transform: none;
    width: 100%;
    max-width: 250px;
  }

  .hero-visual {
    flex-direction: column;
    height: auto;
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .hero-actions {
    flex-direction: column;
  }

  .cta-button {
    width: 100%;
    justify-content: center;
  }

  .category-tabs {
    flex-direction: column;
  }

  .category-tab {
    width: 100%;
  }

  .emoji-grid {
    grid-template-columns: 1fr;
  }
}
/* Переопределяем z-index для модального окна */
.emoji-modal-overlay {
  z-index: 10000 !important;
}

/* Убеждаемся, что сайдбар имеет меньший z-index */
.sidebar {
  z-index: 100;
}

/* Основное исправление позиционирования */
.emoji-modal-overlay {
  position: fixed;
  top: 0;
  left: 280px; /* Начинаем от края сайдбара */
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 10000;
  backdrop-filter: blur(5px);
  padding: 2rem;
  box-sizing: border-box;
}

.emoji-modal {
  width: 100%;
  max-width: 1000px;
  height: 80vh;
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 20px;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.5);
  display: flex;
  flex-direction: column;
  overflow: hidden;
  margin: 0 auto;
}

/* Адаптация для разных размеров экрана */
@media (max-width: 968px) {
  .emoji-modal-overlay {
    left: 240px; /* Учитываем уменьшенную ширину сайдбара */
  }
}

@media (max-width: 768px) {
  .emoji-modal-overlay {
    left: 0;
    padding: 1rem;
  }
  
  .emoji-modal {
    height: 85vh;
  }
}
</style>