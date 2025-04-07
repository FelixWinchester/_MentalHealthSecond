<template>
    <div class="login-page">
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
          <div class="new-note">
            <textarea 
              v-model="newNote" 
              placeholder="Добавьте новую заметку..."
              @keyup.enter="addNote"
            ></textarea>
            <button @click="addNote" class="cta-button">Добавить</button>
          </div>
        </section>

        <!-- Блок с эмодзи -->
        <aside class="emoji-sidebar">
          <h3>Выберите эмоцию</h3>
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
          <div class="selected-emoji">
            Выбрано: {{ selectedEmoji?.name || 'пока ничего' }}
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
            name: 'Грусть', 
            icon: require('@/assets/emojis/sad.svg'),
            code: '😢'
        },
        { 
            id: 3, 
            name: 'Нейтральный', 
            icon: require('@/assets/emojis/neutral.svg'),
            code: '😐'
        },
        { 
            id: 4, 
            name: 'Нейтральный', 
            icon: require('@/assets/emojis/neutral.svg'),
            code: '😐'
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

.emoji-grid-container {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr)); /* Всегда 3 колонки */
  gap: 8px; /* Расстояние между элементами */
  padding: 5px;
  grid-auto-rows: min-content;
  width: fit-content;
}

.emoji-item {
  aspect-ratio: 1/1; /* Квадратные ячейки */
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  transition: transform 0.2s;
}


.emoji-item img {
  width: 80%; /* Размер внутри ячейки */
  height: 80%;
  object-fit: contain;
}

.emoji-button {
  width: 80px;   /* Фиксированная ширина */
  height: 80px;  /* Фиксированная высота */
  padding: 5px; /* Отступ внутри кнопки */
  border: 2px solid transparent;
  background: #f8f9fa;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.emoji-button:hover {
  background: #e0e0e0;
  transform: scale(1.05);
}

.emoji-button.selected {
  border-color: #2c3e50;
  background: #e8f4ff;
}

.loading {
  text-align: center;
  padding: 20px;
  color: #666;
}

.delete-button {
  background: none;
  border: none;
  color: #ff4444;
  cursor: pointer;
  float: right;
  font-size: 1.2rem;
  line-height: 1;
}

.delete-button:hover {
  color: #cc0000;
}

.selected {
  border-color: #2c3e50 !important;
  background-color: #e8f4ff !important;
}

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

.content {
  margin-bottom: 40px;
}

.section {
  margin-bottom: 40px;
}

.section h2 {
  font-size: 2rem;
  color: #2c3e50;
  margin-bottom: 20px;
}


.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  font-size: 1rem;
  color: #444;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 5px;
  font-size: 1rem;
}

.cta-button {
  background-color: #2c3e50;
  color: white;
  border: none;
  padding: 10px 20px;
  border-radius: 5px;
  cursor: pointer;
  font-size: 1rem;
}

.cta-button:hover {
  background-color: #1a2a36;
}


.info-section {
  text-align: center;
}

.info-section p {
  font-size: 1.1rem;
  color: #666;
}

.info-section a {
  color: #2c3e50;
  text-decoration: none;
}

.info-section a:hover {
  text-decoration: underline;
}
</style>