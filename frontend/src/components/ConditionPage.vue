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
              v-for="(emoji, index) in filteredEmojis" 
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
              <span class="emoji-name">{{ emoji.name }}</span>
            </button>
          </div>
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
            <div class="emoji-label">{{ selectedEmoji?.name || questionEmoji.name }}</div>
          </div>
          <button 
            v-if="selectedEmoji"
            @click="clearEmoji"
            class="emoji-action-button"
          >
            Убрать эмоцию
          </button>
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
    pageTitle: 'Мое состояние',
    loading: true,
    newNote: '',
    notes: [],
    emojis: [
      { 
          id: 1, 
          name: 'Счастье', 
          icon: require('@/assets/emojis/happy.png'),
          code: '😀'
      },
      { 
          id: 2, 
          name: 'Возбуждение', 
          icon: require('@/assets/emojis/excited.png'),
          code: '🤩'
      },
      { 
          id: 3, 
          name: 'Удовлетворение', 
          icon: require('@/assets/emojis/satisfied.png'),
          code: '😌'
      },
      { 
          id: 4, 
          name: 'Радость', 
          icon: require('@/assets/emojis/joyful.png'),
          code: '😊'
      },
      { 
          id: 5, 
          name: 'Непонимание', 
          icon: require('@/assets/emojis/misunderstanding.png'),
          code: '😐'
      },
      { 
          id: 6, 
          name: 'Беспокойство', 
          icon: require('@/assets/emojis/worried.png'),
          code: '😟'
      },
      { 
          id: 7, 
          name: 'Грусть', 
          icon: require('@/assets/emojis/sad.png'),
          code: '😢'
      },
      { 
          id: 8, 
          name: 'Уныние', 
          icon: require('@/assets/emojis/depressed.png'),
          code: '😞'
      },
      { 
          id: 9, 
          name: 'Злость', 
          icon: require('@/assets/emojis/angry.png'),
          code: '😠'
      },
      { 
          id: 10, 
          name: 'Не оценено', 
          icon: require('@/assets/emojis/question.png'),
          code: '❓',
          isQuestion: true
      },
    ],
    selectedEmoji: null
  };
},
computed: {
  questionEmoji() {
    return this.emojis.find(e => e.isQuestion);
  },
  filteredEmojis() {
    return this.emojis.filter(e => !e.isQuestion);
  }
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
      const newEmoji = this.selectedEmoji?.id === emoji.id ? null : emoji;
      
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
  
  async clearEmoji() {
    await this.selectEmoji(this.selectedEmoji);
  }
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
flex-direction: column;
min-height: calc(100vh - 200px);
}

/* Стили для секции с заметками */
.notes-section {
width: 100%;
max-width: 900px;
margin: 0 auto;
height: calc(100vh - 300px);
overflow-y: auto;
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

/* Виджет с эмодзи */
.emoji-sidebar {
position: fixed;
right: 20px;
top: 50%;
transform: translateY(-50%);
width: 80px;
height: 80px;
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

.emoji-sidebar:hover {
width: 300px;
height: calc(100vh - 100px);
min-height: 400px;
max-height: 90vh;
padding: 20px;
overflow-y: auto;
}

.emoji-sidebar h3 {
margin: 0 0 15px 0;
padding: 0;
color: #2c3e50;
font-size: 1.2rem;
opacity: 0;
transition: opacity 0.2s ease 0.1s;
width: 100%;
text-align: center;
}

.emoji-sidebar:hover h3 {
opacity: 1;
}

/* Сетка эмодзи */
.emoji-grid-container {
display: grid;
grid-template-columns: repeat(3, 1fr);
gap: 15px;
width: 100%;
opacity: 0;
transition: opacity 0.3s ease 0.1s;
}

.emoji-sidebar:hover .emoji-grid-container {
opacity: 1;
}

/* Кнопка с эмодзи */
.emoji-button {
width: 100%;
height: auto;
aspect-ratio: 1/1;
padding: 10px;
border: 2px solid transparent;
background: white;
border-radius: 10px;
cursor: pointer;
transition: all 0.2s ease;
display: flex;
flex-direction: column;
align-items: center;
justify-content: center;
}

.emoji-button:hover {
transform: scale(1.05);
background: #e0e0e0;
}

.emoji-button.selected {
border-color: #2c3e50;
background: #e8f4ff;
}

.emoji-icon {
width: 50px;
height: 50px;
object-fit: contain;
margin-bottom: 5px;
}

.emoji-name {
font-size: 0.8rem;
text-align: center;
color: #333;
}

/* Контейнер выбранного смайлика */
.selected-emoji-container {
width: 100%;
margin-top: 20px;
padding-top: 20px;
border-top: 1px solid #eee;
display: flex;
flex-direction: column;
align-items: center;
opacity: 0;
transition: opacity 0.3s ease;
}

.emoji-sidebar:hover .selected-emoji-container {
opacity: 1;
}

.selected-emoji {
display: flex;
flex-direction: column;
align-items: center;
margin-bottom: 15px;
}

.emoji-label {
font-size: 1rem;
margin-top: 8px;
color: #2c3e50;
font-weight: 500;
}

.emoji-action-button {
background-color: #f8f9fa;
color: #2c3e50;
border: 1px solid #ddd;
padding: 8px 15px;
border-radius: 5px;
cursor: pointer;
font-size: 0.9rem;
transition: all 0.2s ease;
}

.emoji-action-button:hover {
background-color: #e9ecef;
}

/* Компактный режим (без наведения) */
.emoji-sidebar:not(:hover) .selected-emoji-container {
position: absolute;
bottom: 10px;
left: 50%;
transform: translateX(-50%);
width: 60px;
height: 60px;
margin: 0;
padding: 0;
border: none;
opacity: 1;
}

.emoji-sidebar:not(:hover) .selected-emoji {
margin: 0;
}

.emoji-sidebar:not(:hover) .emoji-label,
.emoji-sidebar:not(:hover) .emoji-action-button {
display: none;
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

/* Адаптация для мобильных устройств */
@media (max-width: 768px) {
.emoji-sidebar {
  right: 10px;
  width: 60px;
  height: 60px;
}

.emoji-sidebar:hover {
  width: calc(100% - 40px);
  right: 20px;
  border-radius: 12px;
}

.emoji-icon {
  width: 40px;
  height: 40px;
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

@media (min-width: 2560px) {
.emoji-sidebar:hover {
  height: calc(100vh - 150px);
}
}
</style>