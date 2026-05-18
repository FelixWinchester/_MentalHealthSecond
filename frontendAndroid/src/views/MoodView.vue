<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">Настроение</h1>
      <p class="page-sub">Как вы себя чувствуете сегодня?</p>
    </div>

    <div v-if="saved" class="saved-banner">
      ✅ Настроение сохранено!
    </div>

    <div class="mood-grid">
      <button
        v-for="mood in moods"
        :key="mood.value"
        class="mood-btn"
        :class="{ selected: selected === mood.value }"
        @click="select(mood.value)"
      >
        <span class="mood-emoji">{{ mood.icon }}</span>
        <span class="mood-name">{{ mood.label }}</span>
      </button>
    </div>

    <div class="card note-card" v-if="selected">
      <div class="input-group">
        <label>Заметка (необязательно)</label>
        <textarea v-model="details" placeholder="Расскажите подробнее о своём состоянии..."></textarea>
      </div>
      <button class="btn btn-primary" @click="save" :disabled="saving">
        {{ saving ? 'Сохраняем...' : 'Сохранить' }}
      </button>
    </div>
  </div>
</template>

<script>
import api from '@/api/api';

const MOODS = [
  { value: 'happy', icon: '😄', label: 'Счастливый' },
  { value: 'excited', icon: '🤩', label: 'Воодушевлённый' },
  { value: 'joyful', icon: '😁', label: 'Радостный' },
  { value: 'satisfied', icon: '😊', label: 'Довольный' },
  { value: 'misunderstanding', icon: '😕', label: 'Непонимание' },
  { value: 'worried', icon: '😰', label: 'Тревожный' },
  { value: 'sad', icon: '😢', label: 'Грустный' },
  { value: 'depressed', icon: '😞', label: 'Подавленный' },
  { value: 'angry', icon: '😠', label: 'Злой' },
];

export default {
  name: 'MoodView',
  data() {
    return {
      moods: MOODS,
      selected: null,
      details: '',
      saving: false,
      saved: false,
    };
  },
  async mounted() {
    try {
      const res = await api.getTodaysMood();
      if (res.data?.mood) {
        this.selected = res.data.mood;
        this.details = res.data.details || '';
      }
    } catch { /* */ }
  },
  methods: {
    select(value) {
      this.selected = value;
      this.saved = false;
    },
    async save() {
      if (!this.selected) return;
      this.saving = true;
      try {
        await api.createMoodEntry({ mood: this.selected, details: this.details });
        this.saved = true;
        setTimeout(() => { this.saved = false; }, 3000);
      } catch { /* */ } finally {
        this.saving = false;
      }
    },
  },
};
</script>

<style scoped>
.saved-banner {
  background: rgba(34, 197, 94, 0.15);
  border: 1px solid rgba(34, 197, 94, 0.4);
  border-radius: 12px;
  padding: 12px 16px;
  color: var(--success);
  font-size: 0.9rem;
  text-align: center;
  margin-bottom: 16px;
}

.mood-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 20px;
}

.mood-btn {
  background: var(--surface);
  border: 2px solid var(--border);
  border-radius: 16px;
  padding: 16px 8px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  cursor: pointer;
  transition: border-color 0.2s, background 0.2s;
}

.mood-btn:active { opacity: 0.85; }

.mood-btn.selected {
  border-color: var(--primary);
  background: rgba(128, 90, 213, 0.1);
}

.mood-emoji { font-size: 1.8rem; }

.mood-name {
  font-size: 0.72rem;
  color: var(--text-sub);
  text-align: center;
  line-height: 1.2;
}

.note-card { margin-top: 4px; }

.btn:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
