<template>
  <div class="condition-page">
    <!-- Заголовок страницы -->
    <header class="header">
      <h1>{{ pageTitle }}</h1>
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

        <!-- Блок с текущей эмоцией справа -->
        <div class="current-emoji-side" @click="showEmojiModal = true">
          <div class="current-emoji">
            <img 
              :src="selectedEmoji?.icon || questionEmoji.icon" 
              :alt="selectedEmoji?.name || questionEmoji.name"
              class="emoji-icon"
            >
            <div class="emoji-label">
              {{ selectedEmoji?.displayName || questionEmoji.displayName }}
            </div>
          </div>
        </div>
        
        <!-- Поле ввода вынесено отдельно -->
        <div class="new-note">
          <textarea 
              v-model="newNote" 
              placeholder="Опишите, что вы чувствуете..."
              @keyup.enter.prevent="saveState" ></textarea>
          <button @click="saveState" class="cta-button">Сохранить</button>
        </div>

        <!-- Модальное окно для выбора эмоций -->
        <div v-if="showEmojiModal" class="emoji-modal-overlay" @click.self="closeEmojiModal">
          <div class="emoji-modal">
            <div class="emoji-modal-header">
              <h3>Как вы себя чувствуете сегодня?</h3>
              <button @click="closeEmojiModal" class="close-button">&times;</button>
            </div>
            <div class="emoji-modal-content">
              <div class="emoji-grid-container">
                <button 
                  v-for="(emoji, index) in filteredEmojis" 
                  :key="index"
                  @click="selectEmoji(emoji)"
                  class="emoji-button"
                  :class="{ 'selected': selectedEmoji?.id === emoji.id }"
                >
                  <div class="emoji-icon-container">
                    <img 
                      :src="emoji.icon" 
                      :alt="emoji.name"
                      class="emoji-icon"
                    >
                  </div>
                  <span class="emoji-name">{{ emoji.name }}</span>
                </button>
              </div>
              <div class="selected-emoji-container">
                <div class="selected-emoji">
                  <img 
                    v-if="selectedEmoji" 
                    :src="selectedEmoji.icon" 
                    :alt="selectedEmoji.name"
                    class="emoji-icon"
                  >
                  <img 
                    v-else
                    :src="questionEmoji.icon" 
                    :alt="questionEmoji.name"
                    class="emoji-icon"
                  >
                  <div class="emoji-label">{{ emojiDisplayName(selectedEmoji?.name) || questionEmoji.displayName }}</div>
                </div>
                <button 
                  v-if="selectedEmoji"
                  @click="clearEmoji"
                  class="emoji-action-button"
                >
                  Убрать эмоцию
                </button>
                <button 
                    @click="saveState"
                    class="emoji-action-button primary"
                >
                    Готово
                </button>
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
            name: 'happy', 
            displayName: 'Счастье',
            icon: '/emojis/happy.png',
            code: '😀'
        },
        { 
            id: 2, 
            name: 'excited',
            displayName: 'Возбуждение', 
            icon: '/emojis/excited.png',
            code: '🤩'
        },
        { 
            id: 3, 
            name: 'satisfied',
            displayName: 'Удовлетворение', 
            icon: '/emojis/satisfied.png',
            code: '😌'
        },
        { 
            id: 4, 
            name: 'joyful', 
            displayName: 'Радость',
            icon: '/emojis/joyful.png',
            code: '😊'
        },
        { 
            id: 5, 
            name: 'misunderstanding', 
            displayName: 'Непонимание',
            icon: '/emojis/misunderstanding.png',
            code: '😐'
        },
        { 
            id: 6, 
            name: 'worried', 
            displayName: 'Беспокойство',
            icon: '/emojis/worried.png',
            code: '😟'
        },
        { 
            id: 7, 
            name: 'sad', 
            displayName: 'Грусть',
            icon: '/emojis/sad.png',
            code: '😢'
        },
        { 
            id: 8, 
            name: 'depressed', 
            displayName: 'Уныние',
            icon: '/emojis/depressed.png',
            code: '😞'
        },
        { 
            id: 9, 
            name: 'angry', 
            displayName: 'Злость',
            icon: '/emojis/angry.png',
            code: '😠'
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
      showEmojiModal: false
    };
  },
  computed: {
    questionEmoji() {
      return this.emojis.find(e => e.isQuestion);
    },

    filteredEmojis() {
      return this.emojis.filter(e => !e.isQuestion);
    },

    emojiDisplayName() {
      return (emojiName) => {
        const emoji = this.emojis.find(e => e.name === emojiName);
        return emoji ? emoji.displayName : emojiName;
      }
    }
  },
  async created() {
    await this.fetchData();
    // Убрали автоматическое открытие модального окна
    // this.showEmojiModal = true;
  },
  methods: {
    async fetchData() {
        this.loading = true;
        try {
            // Загружаем ВСЕ заметки для списка (как и раньше)
            const notesResponse = await api.getNotes();
            // ВАЖНО: getNotes теперь возвращает массив {id, text, created_at}
            // Убедимся, что мы правильно его обрабатываем
            this.notes = notesResponse.data.map(note => ({ text: note.text }));

            // Пытаемся загрузить сегодняшнюю запись (эмоцию + заметку)
            try {
                const todaysMoodResponse = await api.getTodaysMood();
                const moodData = todaysMoodResponse.data;
                
                if (moodData) {
                    // Устанавливаем выбранную эмоцию
                    this.selectedEmoji = this.emojis.find(e => e.name === moodData.mood);
                    
                    // ЗАГРУЖАЕМ ТЕКСТ ЗАМЕТКИ В ПОЛЕ ВВОДА
                    this.newNote = moodData.details || '';
                }
            } catch (error) {
                // Ошибки 404 (записи за сегодня нет) - это нормально, просто игнорируем
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

    selectEmoji(emoji) {
        // Если кликнули на ту же эмоцию - очищаем выбор
        if (this.selectedEmoji?.id === emoji.id) {
            this.selectedEmoji = null;
        } else {
            // Просто обновляем состояние в компоненте
            this.selectedEmoji = emoji;
        }
    },

    async saveState() {
        // Проверяем, выбрана ли эмоция. Если нет, ничего не делаем.
        if (!this.selectedEmoji) {
            // Если есть только текст заметки, можно его сохранить как отдельную заметку
            // Но по текущей логике лучше требовать выбор эмоции.
            // Если хотите разрешить заметки без эмоций, нужна другая логика.
            alert('Пожалуйста, выберите эмоцию, чтобы сохранить состояние.');
            return;
        }

        try {
            const payload = {
                mood: this.selectedEmoji.name.toLowerCase(),
                details: this.newNote.trim()
            };
            // Отправляем единый запрос на создание/обновление
            const response = await api.createMoodEntry(payload);
            
            // Если заметка была добавлена, добавим её в локальный список
            if (this.newNote.trim()) {
                // Важно: API должен возвращать созданную/обновленную запись
                // Мы предполагаем, что в response.data есть поле 'details'
                // Возможно, понадобится обновить список всех заметок с сервера
                this.notes.push({ text: response.data.details }); // Упрощенный вариант
                this.newNote = ''; // Очищаем поле ввода
            }
            
            // Закрываем модальное окно, если оно было открыто
            this.showEmojiModal = false;
            
        } catch (error) {
            console.error('Ошибка сохранения состояния:', error);
            alert('Не удалось сохранить состояние. Пожалуйста, попробуйте еще раз.');
        }
    },
    
    async clearEmoji() {
      this.selectedEmoji = null;
      try {
        await api.createMoodEntry({
          mood: '',
          details: ''
        });
      } catch (error) {
        console.error('Ошибка очистки эмоции:', error);
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
  position: fixed;
  left: 0;
  right: 0;
  overflow: hidden;
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
  min-height: calc(100vh - 200px);
  position: relative;
}

/* Стили для секции с заметками */
.notes-section {
  flex: 1;
  max-width: 900px;
  height: calc(100vh - 300px);
  overflow-y: auto;
  padding: 15px;
  box-sizing: border-box;
  margin-right: 20px;
}

/* Контейнер для текущей эмоции */
.current-emoji-side {
  position: fixed;
  right: 20px;
  top: 50%;
  transform: translateY(-50%);
  width: 120px;
  height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: white;
  border-radius: 50%;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: all 0.3s ease;
  z-index: 10;
}

.current-emoji-side:hover {
  transform: translateY(-50%) scale(1.05);
  box-shadow: 0 6px 25px rgba(0, 0, 0, 0.15);
}

.current-emoji {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px;
}

.current-emoji .emoji-icon {
  width: 60px;
  height: 60px;
  margin-bottom: 8px;
}

.current-emoji .emoji-label {
  font-size: 0.9rem;
  text-align: center;
  color: #2c3e50;
  font-weight: 500;
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
  width: 1200px;
  max-width: 90%;
  background: white;
  padding: 15px;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  box-sizing: border-box;
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
  box-sizing: border-box;
  font-size: 16px;
  line-height: 1.5;
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
  margin-top: 10px;
  transition: background-color 0.2s ease;
}

.cta-button:hover {
  background-color: #1a2a36;
}

/* Стили для модального окна с эмодзи */
.emoji-modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.emoji-modal {
  width: 70vw;
  height: calc(70vw * 3 / 4);
  max-width: 900px;
  max-height: calc(1000px * 3 / 4);
  background: white;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.emoji-modal-header {
  padding: 20px;
  background: #2c3e50;
  color: white;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.emoji-modal-header h3 {
  margin: 0;
  font-size: 1.5rem;
}

.close-button {
  background: none;
  border: none;
  color: white;
  font-size: 2rem;
  cursor: pointer;
  line-height: 1;
  padding: 0 10px;
}

.emoji-modal-content {
  flex: 1;
  display: flex;
  padding: 20px;
  overflow: hidden;
}

.emoji-grid-container {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(3, 1fr); /* Фиксированная сетка 3x3 */
  gap: 15px;
  overflow-y: auto;
  padding-right: 20px;
  align-content: start; /* Выравнивание по верхнему краю */
}

.emoji-button {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 10px;
  border: 2px solid transparent;
  background: white;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
  aspect-ratio: 1/1; /* Квадратные кнопки */
  height: 100%; /* Занимают всю доступную высоту */
}

.emoji-button:hover {
  background: #f0f0f0;
}

.emoji-button.selected {
  border-color: #2c3e50;
  background: #e8f4ff;
}

/* Контейнер для иконки с фиксированными размерами */
.emoji-icon-container {
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-bottom: 8px;
}

.emoji-icon {
  width: 50px;
  height: 50px;
  object-fit: contain;
  margin-bottom: 8px;
}

.emoji-name {
  font-size: 0.9rem;
  text-align: center;
  color: #333;
}

.selected-emoji-container {
  width: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  border-left: 1px solid #eee;
  padding-left: 20px;
}

.selected-emoji {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 20px;
}

.emoji-label {
  font-size: 1.1rem;
  margin-top: 10px;
  color: #2c3e50;
  font-weight: 500;
}

.emoji-action-button {
  margin: 5px 0;
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 0.9rem;
  transition: all 0.2s ease;
  width: 100%;
  background-color: #f8f9fa;
  color: #2c3e50;
  border: 1px solid #ddd;
}

.emoji-action-button:hover {
  background-color: #e9ecef;
}

.emoji-action-button.primary {
  background-color: #2c3e50;
  color: white;
  border: none;
}

.emoji-action-button.primary:hover {
  background-color: #1a2a36;
}

/* Адаптация для мобильных устройств */
@media (max-width: 768px) {
  .main-layout {
    flex-direction: column;
  }

  .notes-section {
    margin-right: 0;
    margin-bottom: 20px;
  }

  .current-emoji-side {
    position: static;
    transform: none;
    margin: 20px auto;
    width: 100px;
    height: 100px;
  }
  
  .current-emoji-side:hover {
    transform: none;
  }
  
  .current-emoji .emoji-icon {
    width: 50px;
    height: 50px;
  }
}
</style>