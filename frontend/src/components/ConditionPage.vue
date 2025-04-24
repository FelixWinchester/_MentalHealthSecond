<template>
    <div class="condition-page">
      <!-- Заголовок страницы -->
      <header class="header">
        <h1>{{ pageTitle }}</h1>
        <p>Пожалуйста, войдите в систему, чтобы получить доступ к вашему аккаунту.</p>
      </header>

      <!-- Основной контент -->
    <main class="content">
      <div class="main-layout">
        <!-- Блок с заметками -->
        <section class="notes-section">
          <div class="notes-list">
            <div v-for="(note, index) in notes" :key="index" class="note-card">
              {{ note.text }}
            </div>
          </div>
        </section>
        <!-- Поле ввода вынесено отдельно -->
        <div class="new-note">
          <textarea 
            v-model="newNote" 
            placeholder="Добавьте новую заметку..."
            @keyup.enter="addNote"
          ></textarea>
          <button @click="addNote" class="cta-button">Добавить</button>
        </div>

        <!-- Блок с эмодзи -->
        <aside class="emoji-sidebar">
          <h3>Выберите эмоцию</h3>
          <div class="emoji-widget">
            <div class="emoji-grid-container">
              <button 
                v-for="(emoji, index) in emojis" 
                :key="index"
                @click="selectEmoji(emoji)"
                class="emoji-button"
                :class="{ 'selected': selectedEmoji?.id === emoji.id }"
              >
                <img 
                  :src="emoji.icon" 
                  :alt="emoji.name"
                  class="emoji-icon"
                >
              </button>
            </div>
          </div>
          <div class="selected-emoji">
            {{ selectedEmoji?.name || 'Не оценено' }}
          </div>
        </aside>
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
      loading: true,
      newNote: '',
      notes: [],
      emojis: [
        { 
            id: 1, 
            name: 'Счастье', 
            icon: require('@/assets/emojis/happy.svg'),
            code: '😀'
        },
        { 
            id: 2, 
            name: 'Возбуждение', 
            icon: require('@/assets/emojis/excited.svg'),
            code: '🤩'
        },
        { 
            id: 3, 
            name: 'Удовлетворение', 
            icon: require('@/assets/emojis/satisfied.svg'),
            code: '😌'
        },
        { 
            id: 4, 
            name: 'Спокойствие', 
            icon: require('@/assets/emojis/calm.svg'),
            code: '😊'
        },
        { 
            id: 5, 
            name: 'Нейтральный', 
            icon: require('@/assets/emojis/neutral.svg'),
            code: '😐'
        },
        { 
            id: 6, 
            name: 'Беспокойство', 
            icon: require('@/assets/emojis/worried.svg'),
            code: '😟'
        },
        { 
            id: 7, 
            name: 'Грусть', 
            icon: require('@/assets/emojis/sad.svg'),
            code: '😢'
        },
        { 
            id: 8, 
            name: 'Уныние', 
            icon: require('@/assets/emojis/depressed.svg'),
            code: '😞'
        },
        { 
            id: 9, 
            name: 'Злость', 
            icon: require('@/assets/emojis/angry.svg'),
            code: '😠'
        }
      ],
      selectedEmoji: null
    };
  },
  async created() {
    await this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const [notesResponse, moodResponse] = await Promise.all([
          api.get('/notes', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          }),
          api.get('/mood', {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          })
        ]);

        this.notes = notesResponse.data;
        this.selectedEmoji = moodResponse.data.emoji;
      } catch (error) {
        console.error('Ошибка загрузки данных:', error);
        if (error.response?.status === 401) {
          this.$router.push('/login');
        }
      } finally {
        this.loading = false;
      }
    },

    async addNote() {
      if (!this.newNote.trim()) return;

      try {
        const response = await api.post('/notes', 
          { text: this.newNote },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          }
        );

        this.notes.push(response.data);
        this.newNote = '';
      } catch (error) {
        console.error('Ошибка добавления заметки:', error);
      }
    },

    async deleteNote(noteId) {
      try {
        await api.delete(`/notes/${noteId}`, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.notes = this.notes.filter(note => note.id !== noteId);
      } catch (error) {
        console.error('Ошибка удаления заметки:', error);
      }
    },

    async selectEmoji(emoji) {
      try {
        const newEmoji = this.selectedEmoji === emoji ? null : emoji;
        await api.post('/mood', 
          { emoji: newEmoji },
          {
            headers: {
              Authorization: `Bearer ${localStorage.getItem('token')}`
            }
          }
        );
        this.selectedEmoji = newEmoji;
      } catch (error) {
        console.error('Ошибка сохранения эмоции:', error);
      }
    },
  }
};
</script>

<style scoped>

/* Основной контейнер страницы */
.condition-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  position: fixed; /* Фиксируем позицию */
  left: 0;
  right: 0;
  overflow: hidden; /* Полностью отключаем скролл */
}

/* Стили для шапки */
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

/* Основной контент */
.main-layout {
  display: flex;
  flex-direction: column; /* Меняем направление на колонку */
  min-height: calc(100vh - 200px); /* Добавляем минимальную высоту */
}

/* Стили для секции с заметками */
.notes-section {
  width: 100%;
  max-width: 900px; /* Ширина чуть меньше заголовка */
  margin: 0 auto;
  height: calc(100vh - 300px); /* Фиксированная высота */
  overflow-y: auto; /* Внутренний скролл */
  padding: 15px;
  box-sizing: border-box;
}
.notes-list {
  display: grid;
  gap: 15px;
  margin-bottom: 20px;
  max-height: 60vh;
  overflow-y: auto;
  padding-right: 10px;
}
.note-card {
  padding: 15px;
  background: #f8f9fa;
  border-radius: 8px;
  border: 1px solid #eee;
  position: relative;
}

/* Стили для новой заметки */
.new-note {
  position: fixed;
  bottom: 100px;
  left: 50%;
  transform: translateX(-50%);
  width: 1200px; /* Совпадает с шириной notes-section */
  max-width: 90%;
  background: white;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  box-sizing: border-box; /* Учитываем padding в ширине */
}

.new-note textarea {
  width: 100%;
  height: 150px;
  min-height: 150px;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  resize: none;
  overflow-y: auto;
  box-sizing: border-box; /* Фиксируем размеры */
  font-size: 16px;
  line-height: 1.5;
}

/* Виджет с эмодзи */
.emoji-sidebar {
  position: fixed;
  right: 20px; /* Изменено на правую сторону */
  top: 50%;
  transform: translateY(-50%);
  width: 90px; /* Увеличенный начальный размер */
  height: 90px;
  background: #f8f9fa;
  border-radius: 12px;
  overflow: hidden;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1000;
  box-shadow: 0 2px 8px rgba(0,0,0,0.1);
  padding: 10px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.emoji-sidebar::before {
  content: '';
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 2px;
  width: 80px;
  height: 80px;
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 1;
  transition: opacity 0.2s ease;
}

.emoji-sidebar::before {
  background-image: 
    /* Формируем миниатюрную сетку смайликов */
    url('@/assets/emojis/happy.svg'),
    url('@/assets/emojis/excited.svg'),
    url('@/assets/emojis/satisfied.svg'),
    url('@/assets/emojis/calm.svg'),
    url('@/assets/emojis/neutral.svg'),
    url('@/assets/emojis/worried.svg'),
    url('@/assets/emojis/sad.svg'),
    url('@/assets/emojis/depressed.svg'),
    url('@/assets/emojis/angry.svg');
  background-size: 24px 24px;
  background-repeat: no-repeat;
  background-position:
    /* Позиционируем 9 смайликов в сетке 3x3 */
    2px 2px,
    28px 2px,
    54px 2px,
    2px 28px,
    28px 28px,
    54px 28px,
    2px 54px,
    28px 54px,
    54px 54px;
}

.emoji-sidebar:hover {
  width: 280px;
  height: auto;
  min-height: 400px;
  padding: 15px;
}

.emoji-sidebar:hover::before {
  opacity: 0;
}

.emoji-sidebar h3 {
  margin: 0 0 15px 0;
  padding: 0;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.emoji-sidebar:hover h3 {
  opacity: 1;
}

/* Сетка эмодзи */
.emoji-grid-container {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  width: 100%;
  opacity: 0;
  padding: 0;
  transition: opacity 0.3s ease;
}

.emoji-sidebar:hover .emoji-grid-container {
  opacity: 1;
}

/* Кнопка с эмодзи */
.emoji-button {
  width: 80px; /* Возвращаем исходный размер */
  height: 80px;
  padding: 5px;
  border: 2px solid transparent;
  background: white;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}

.emoji-sidebar:not(:hover) .emoji-button {
  width: 20px;
  height: 20px;
  margin: 1px;
}

.emoji-button:hover {
  transform: scale(1.1);
  background: #e0e0e0;
}

.emoji-button.selected {
  border-color: #2c3e50;
  background: #e8f4ff;
}

/* Область выбранного смайлика */
.selected-emoji {
  position: absolute;
  bottom: 10px;
  width: 80px;
  height: 80px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 10px;
  box-shadow: 0 2px 4px rgba(0,0,0,0.1);
  opacity: 0;
  transition: opacity 0.2s ease;
}

.selected-emoji img {
  width: 60px;
  height: 60px;
  object-fit: contain;
}

.emoji-sidebar:hover .selected-emoji {
  opacity: 0; /* Скрываем при открытом виджете */
}

/* Показываем выбранный смайлик только в компактном режиме */
.emoji-sidebar:not(:hover) .selected-emoji {
  opacity: 1;
}

/* Адаптация для мобильных устройств */
@media (max-width: 768px) {
  .emoji-sidebar {
    right: 10px;
    width: 80px;
    height: 80px;
  }
  
  .emoji-sidebar:hover {
    width: 100%;
    right: 0;
    border-radius: 0;
  }

  .new-note {
    width: 95%;
    max-width: 95%;
    bottom: 10px;
  }
  
  .new-note textarea {
    height: 120px;
    min-height: 120px;
  }
}

/* Иконка эмодзи */
.emoji-icon {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

/* Кнопка добавления */
.cta-button {
  align-self: flex-end;
  background-color: #2c3e50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
}

.cta-button:hover {
  background-color: #1a2a36;
}

/* Выбранная эмоция */
.selected-emoji {
  margin-top: 15px;
  padding-top: 15px;
  border-top: 1px solid #eee;
  font-size: 0.9rem;
  color: #666;
  opacity: 0;
  transition: opacity 0.2s ease;
}

.emoji-sidebar:hover .selected-emoji {
  opacity: 1;
}
</style>