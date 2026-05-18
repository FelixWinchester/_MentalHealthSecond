<template>
  <div class="page">
    <div class="page-header">
      <div class="greeting">
        <span class="greeting-emoji">{{ greetingEmoji }}</span>
        <div>
          <p class="greeting-time">{{ greetingText }}</p>
          <h2 class="greeting-name">{{ username }}</h2>
        </div>
      </div>
    </div>

    <!-- Today's mood card -->
    <div class="card today-card">
      <div class="today-header">
        <span class="today-icon">{{ todayMoodIcon }}</span>
        <div>
          <p class="today-label">Сегодня</p>
          <p class="today-mood">{{ todayMoodText }}</p>
        </div>
      </div>
      <router-link to="/mood" class="btn btn-primary" style="text-align:center; display:block; text-decoration:none;">
        {{ todayMood ? 'Изменить настроение' : 'Отметить настроение' }}
      </router-link>
    </div>

    <!-- Quick actions -->
    <div class="quick-actions">
      <router-link to="/chart" class="action-card">
        <span class="action-icon">📊</span>
        <span class="action-label">График</span>
      </router-link>
      <router-link to="/forum" class="action-card">
        <span class="action-icon">💬</span>
        <span class="action-label">Форум</span>
      </router-link>
      <router-link to="/achievements" class="action-card">
        <span class="action-icon">🏆</span>
        <span class="action-label">Достижения</span>
      </router-link>
      <router-link to="/profile" class="action-card">
        <span class="action-icon">👤</span>
        <span class="action-label">Профиль</span>
      </router-link>
    </div>

    <!-- Motivational quote -->
    <div class="card quote-card">
      <p class="quote-text">"{{ quote }}"</p>
    </div>
  </div>
</template>

<script>
import api from '@/api/api';

const MOOD_ICONS = {
  happy: '😄', excited: '🤩', satisfied: '😊', joyful: '😁',
  misunderstanding: '😕', worried: '😰', sad: '😢', depressed: '😞', angry: '😠',
};

const MOOD_LABELS = {
  happy: 'Счастливый', excited: 'Воодушевлённый', satisfied: 'Довольный',
  joyful: 'Радостный', misunderstanding: 'Непонимание', worried: 'Тревожный',
  sad: 'Грустный', depressed: 'Подавленный', angry: 'Злой',
};

const QUOTES = [
  'Маленькие шаги каждый день ведут к большим переменам.',
  'Забота о себе — это не эгоизм, это необходимость.',
  'Каждый день — это новый шанс стать лучшей версией себя.',
  'Вы сильнее, чем думаете.',
  'Один день за раз — и всё получится.',
];

export default {
  name: 'HomeView',
  data() {
    return {
      username: '',
      todayMood: null,
      quote: QUOTES[Math.floor(Math.random() * QUOTES.length)],
    };
  },
  computed: {
    greetingEmoji() {
      const h = new Date().getHours();
      if (h < 6) return '🌙';
      if (h < 12) return '☀️';
      if (h < 18) return '🌤';
      return '🌙';
    },
    greetingText() {
      const h = new Date().getHours();
      if (h < 6) return 'Доброй ночи,';
      if (h < 12) return 'Доброе утро,';
      if (h < 18) return 'Добрый день,';
      return 'Добрый вечер,';
    },
    todayMoodIcon() {
      return this.todayMood ? (MOOD_ICONS[this.todayMood] || '😐') : '❓';
    },
    todayMoodText() {
      return this.todayMood ? (MOOD_LABELS[this.todayMood] || this.todayMood) : 'Ещё не отмечено';
    },
  },
  async mounted() {
    try {
      const user = await api.getUserInfo();
      this.username = user.data.username;
    } catch { /* */ }

    try {
      const mood = await api.getTodaysMood();
      this.todayMood = mood.data?.mood || null;
    } catch { /* */ }
  },
};
</script>

<style scoped>
.greeting {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 4px;
}

.greeting-emoji { font-size: 2.4rem; }

.greeting-time {
  color: var(--text-muted);
  font-size: 0.85rem;
}

.greeting-name {
  font-size: 1.4rem;
  font-weight: 800;
  color: var(--text);
}

.today-card { margin-bottom: 20px; }

.today-header {
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
}

.today-icon { font-size: 2.4rem; }

.today-label {
  color: var(--text-muted);
  font-size: 0.8rem;
  margin-bottom: 2px;
}

.today-mood {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
  margin-bottom: 16px;
}

.action-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 16px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  text-decoration: none;
  transition: border-color 0.2s;
}

.action-card:active { border-color: var(--primary); }

.action-icon { font-size: 1.6rem; }

.action-label {
  font-size: 0.7rem;
  color: var(--text-sub);
  text-align: center;
}

.quote-card {
  border-left: 3px solid var(--primary);
}

.quote-text {
  color: var(--text-sub);
  font-style: italic;
  font-size: 0.9rem;
  line-height: 1.6;
}
</style>
