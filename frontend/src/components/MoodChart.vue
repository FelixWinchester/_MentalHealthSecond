<template>
  <div class="mood-chart-wrapper">
    <div class="chart-header">
      <h2>График настроения</h2>
      <p class="chart-subtitle">Динамика вашего состояния за выбранный период</p>
    </div>

    <div class="period-filters">
      <button
        v-for="filter in filters"
        :key="filter.value"
        class="filter-btn"
        :class="{ active: selectedPeriod === filter.value }"
        @click="selectPeriod(filter.value)"
      >
        {{ filter.label }}
      </button>
    </div>

    <div class="chart-container" v-if="!isLoading && chartData.length > 0">
      <canvas ref="chartCanvas"></canvas>
    </div>

    <div class="chart-empty" v-else-if="!isLoading && chartData.length === 0">
      <div class="empty-icon">📊</div>
      <p>Нет данных за выбранный период</p>
      <span>Начните отмечать настроение каждый день</span>
    </div>

    <div class="chart-loading" v-else>
      <div class="loader"></div>
      <p>Загрузка данных...</p>
    </div>

    <div class="mood-verdict" v-if="verdict && !isLoading && chartData.length > 0">
      <span class="verdict-icon">{{ verdict.icon }}</span>
      <p>{{ verdict.text }}</p>
    </div>

    <div class="mood-legend">
      <div v-for="item in moodLegend" :key="item.score" class="legend-item">
        <span class="legend-dot" :style="{ background: item.color }"></span>
        <span class="legend-label">{{ item.label }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Filler } from 'chart.js';
import api from '@/api/api';

Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Filler);

const MOOD_SCORE = {
  happy: 5, excited: 5,
  satisfied: 4, joyful: 4,
  misunderstanding: 3, worried: 3,
  sad: 2,
  depressed: 1, angry: 1,
};

const MOOD_LABEL = {
  happy: 'Счастливый', excited: 'Воодушевлённый',
  satisfied: 'Довольный', joyful: 'Радостный',
  misunderstanding: 'Непонимание', worried: 'Тревожный',
  sad: 'Грустный',
  depressed: 'Подавленный', angry: 'Злой',
};

const SCORE_COLOR = {
  5: '#22c55e',
  4: '#86efac',
  3: '#facc15',
  2: '#fb923c',
  1: '#ef4444',
};

const SCORE_Y_LABEL = {
  1: 'Плохо', 2: 'Грустно', 3: 'Нейтрально', 4: 'Хорошо', 5: 'Отлично',
};

const PERIOD_LABEL = {
  week: 'неделю', two_weeks: 'две недели',
  month: 'месяц', three_months: 'три месяца',
  half_year: 'полгода', year: 'год',
};

const VERDICTS = [
  { min: 4.5, icon: '🌟', texts: [
    p => `За эту ${p} у вас было восхитительное настроение — так держать!`,
    p => `Отличный ${p}! Вы в прекрасной форме, продолжайте в том же духе.`,
  ]},
  { min: 4.0, icon: '😊', texts: [
    p => `За эту ${p} настроение было по большей части хорошим. Вы молодец!`,
    p => `Хороший ${p}! Позитивный настрой — ваша сила.`,
  ]},
  { min: 3.5, icon: '💪', texts: [
    p => `${p.charAt(0).toUpperCase() + p.slice(1)} прошёл неплохо. Небольшие трудности — это нормально!`,
    p => `В целом за эту ${p} всё складывалось хорошо. Продолжайте заботиться о себе!`,
  ]},
  { min: 3.0, icon: '🌤', texts: [
    p => `За эту ${p} было по-разному, но вы держитесь. Всё наладится!`,
    () => `Бывают разные дни — главное, что вы их отмечаете. Хорошего вам настроения!`,
  ]},
  { min: 2.5, icon: '🌱', texts: [
    p => `Эта ${p} далась непросто. Помните: трудности временны, а вы — нет.`,
    p => `За эту ${p} было несладко, но вы справляетесь. Уделите себе больше заботы!`,
  ]},
  { min: 0, icon: '❤️', texts: [
    p => `Сложная ${p} позади. Вы сильнее, чем думаете — берегите себя!`,
    () => `Было тяжело, но вы не сдаётесь. Это уже победа. Вы не одни!`,
  ]},
];

export default {
  name: 'MoodChart',
  data() {
    return {
      selectedPeriod: 'month',
      chartData: [],
      isLoading: false,
      chartInstance: null,
      verdict: null,
      loadId: 0,
      filters: [
        { label: '7 дней', value: 'week' },
        { label: '2 недели', value: 'two_weeks' },
        { label: 'Месяц', value: 'month' },
        { label: '3 месяца', value: 'three_months' },
        { label: 'Полгода', value: 'half_year' },
        { label: 'Год', value: 'year' },
      ],
      moodLegend: [
        { score: 5, label: 'Отлично', color: '#22c55e' },
        { score: 4, label: 'Хорошо', color: '#86efac' },
        { score: 3, label: 'Нейтрально', color: '#facc15' },
        { score: 2, label: 'Грустно', color: '#fb923c' },
        { score: 1, label: 'Плохо', color: '#ef4444' },
      ],
    };
  },
  async mounted() {
    await this.loadChart();
  },
  beforeUnmount() {
    if (this.chartInstance) {
      this.chartInstance.destroy();
    }
  },
  methods: {
    async selectPeriod(period) {
      this.selectedPeriod = period;
      await this.loadChart();
    },

    async loadChart() {
      const id = ++this.loadId;
      this.isLoading = true;
      this.verdict = null;
      this.chartData = [];
      if (this.chartInstance) {
        this.chartInstance.destroy();
        this.chartInstance = null;
      }
      try {
        const response = await api.getMoodChart(this.selectedPeriod);
        if (id !== this.loadId) return;
        this.chartData = response.data || [];
      } catch (e) {
        if (id !== this.loadId) return;
        this.chartData = [];
      } finally {
        if (id === this.loadId) this.isLoading = false;
      }
      if (id !== this.loadId) return;
      if (this.chartData.length > 0) {
        this.verdict = this.calcVerdict();
        await this.$nextTick();
        if (id === this.loadId) this.renderChart();
      }
    },

    calcVerdict() {
      const scores = this.chartData.map(e => MOOD_SCORE[e.mood] ?? 3);
      const avg = scores.reduce((a, b) => a + b, 0) / scores.length;
      const bucket = VERDICTS.find(v => avg >= v.min);
      const periodLabel = PERIOD_LABEL[this.selectedPeriod] || 'период';
      const texts = bucket.texts;
      const text = texts[Math.floor(Math.random() * texts.length)](periodLabel);
      return { icon: bucket.icon, text };
    },

    formatDate(dateStr) {
      const d = new Date(dateStr);
      return d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' });
    },

    renderChart() {
      try {
      const ctx = this.$refs.chartCanvas;
      if (!ctx) return;

      const labels = this.chartData.map(e => this.formatDate(e.date));
      const scores = this.chartData.map(e => MOOD_SCORE[e.mood] ?? 3);
      const pointColors = scores.map(s => SCORE_COLOR[s] ?? '#805AD5');
      const rawEntries = this.chartData;

      const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 300);
      gradient.addColorStop(0, 'rgba(128, 90, 213, 0.4)');
      gradient.addColorStop(1, 'rgba(128, 90, 213, 0.0)');

      this.chartInstance = new Chart(ctx, {
        type: 'line',
        data: {
          labels,
          datasets: [{
            data: scores,
            borderColor: '#805AD5',
            borderWidth: 2.5,
            pointBackgroundColor: pointColors,
            pointBorderColor: pointColors,
            pointRadius: 6,
            pointHoverRadius: 9,
            tension: 0.4,
            fill: true,
            backgroundColor: gradient,
          }],
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          animation: false,
          interaction: { mode: 'index', intersect: false },
          scales: {
            x: {
              grid: { color: 'rgba(255,255,255,0.05)' },
              ticks: {
                color: '#94a3b8',
                maxTicksLimit: 10,
                maxRotation: 45,
              },
            },
            y: {
              min: 0.5,
              max: 5.5,
              ticks: {
                stepSize: 1,
                color: '#94a3b8',
                callback: val => SCORE_Y_LABEL[val] || '',
              },
              grid: { color: 'rgba(255,255,255,0.05)' },
            },
          },
          plugins: {
            legend: { display: false },
            tooltip: {
              backgroundColor: '#1e293b',
              borderColor: '#805AD5',
              borderWidth: 1,
              titleColor: '#e2e8f0',
              bodyColor: '#94a3b8',
              padding: 14,
              callbacks: {
                title: items => {
                  const idx = items[0].dataIndex;
                  const d = new Date(rawEntries[idx].date);
                  return d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
                },
                label: items => {
                  const idx = items.dataIndex;
                  const entry = rawEntries[idx];
                  const moodName = MOOD_LABEL[entry.mood] || entry.mood;
                  return `Настроение: ${moodName}`;
                },
                afterLabel: items => {
                  const idx = items.dataIndex;
                  const details = rawEntries[idx].details;
                  if (!details) return '';
                  const words = details.split(' ');
                  const lines = [];
                  let line = 'Заметка: ';
                  for (const word of words) {
                    if ((line + word).length > 40) {
                      lines.push(line.trimEnd());
                      line = word + ' ';
                    } else {
                      line += word + ' ';
                    }
                  }
                  if (line.trim()) lines.push(line.trimEnd());
                  return lines;
                },
              },
            },
          },
        },
      });
      } catch (e) {
        // canvas was removed during animation — safe to ignore
      }
    },
  },
};
</script>

<style scoped>
.mood-chart-wrapper {
  background: #1e293b;
  border-radius: 24px;
  padding: 2.5rem;
  border: 1px solid #334155;
}

.chart-header {
  text-align: center;
  margin-bottom: 2rem;
}

.chart-header h2 {
  font-size: 1.8rem;
  font-weight: 800;
  background: linear-gradient(135deg, #805AD5, #667eea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 0.4rem;
}

.chart-subtitle {
  color: #64748b;
  font-size: 0.95rem;
}

.period-filters {
  display: flex;
  flex-wrap: wrap;
  gap: 0.6rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.filter-btn {
  padding: 0.45rem 1.1rem;
  border-radius: 20px;
  border: 1px solid #334155;
  background: transparent;
  color: #94a3b8;
  font-size: 0.88rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s;
}

.filter-btn:hover {
  border-color: #805AD5;
  color: #e2e8f0;
}

.filter-btn.active {
  background: #805AD5;
  border-color: #805AD5;
  color: white;
}

.chart-container {
  height: 320px;
  position: relative;
  margin-bottom: 1.5rem;
}

.chart-empty,
.chart-loading {
  height: 240px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 0.8rem;
  color: #64748b;
  margin-bottom: 1.5rem;
}

.empty-icon {
  font-size: 3rem;
  opacity: 0.5;
}

.chart-empty span {
  font-size: 0.85rem;
  color: #475569;
}

.loader {
  width: 36px;
  height: 36px;
  border: 3px solid rgba(128, 90, 213, 0.2);
  border-top-color: #805AD5;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.mood-verdict {
  display: flex;
  align-items: center;
  gap: 0.8rem;
  background: rgba(128, 90, 213, 0.08);
  border: 1px solid rgba(128, 90, 213, 0.25);
  border-radius: 14px;
  padding: 1rem 1.4rem;
  margin-bottom: 1.5rem;
}

.verdict-icon {
  font-size: 1.6rem;
  flex-shrink: 0;
}

.mood-verdict p {
  color: #cbd5e1;
  font-size: 0.95rem;
  line-height: 1.5;
  margin: 0;
}

.mood-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 0.4rem;
  font-size: 0.82rem;
  color: #94a3b8;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
</style>
