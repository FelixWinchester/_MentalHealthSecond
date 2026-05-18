<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">График настроения</h1>
      <p class="page-sub">Динамика вашего состояния</p>
    </div>

    <div class="period-filters">
      <button
        v-for="f in filters"
        :key="f.value"
        class="filter-btn"
        :class="{ active: selectedPeriod === f.value }"
        @click="selectPeriod(f.value)"
      >
        {{ f.label }}
      </button>
    </div>

    <div class="chart-wrap card" v-if="!isLoading && chartData.length > 0">
      <canvas ref="chartCanvas"></canvas>
    </div>

    <div class="chart-empty card" v-else-if="!isLoading">
      <span class="empty-icon">📊</span>
      <p>Нет данных за период</p>
      <span class="empty-sub">Начните отмечать настроение каждый день</span>
    </div>

    <div class="chart-loading" v-else>
      <div class="loader"></div>
      <p>Загрузка...</p>
    </div>

    <div class="card verdict-card" v-if="verdict && !isLoading && chartData.length > 0">
      <span class="verdict-icon">{{ verdict.icon }}</span>
      <p>{{ verdict.text }}</p>
    </div>

    <div class="legend">
      <div v-for="item in legend" :key="item.score" class="legend-item">
        <span class="legend-dot" :style="{ background: item.color }"></span>
        <span>{{ item.label }}</span>
      </div>
    </div>
  </div>
</template>

<script>
import { Chart, LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Filler } from 'chart.js';
import api from '@/api/api';

Chart.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Tooltip, Filler);

const MOOD_SCORE = {
  happy: 5, excited: 5, satisfied: 4, joyful: 4,
  misunderstanding: 3, worried: 3, sad: 2, depressed: 1, angry: 1,
};
const MOOD_LABEL = {
  happy: 'Счастливый', excited: 'Воодушевлённый', satisfied: 'Довольный',
  joyful: 'Радостный', misunderstanding: 'Непонимание', worried: 'Тревожный',
  sad: 'Грустный', depressed: 'Подавленный', angry: 'Злой',
};
const SCORE_COLOR = { 5: '#22c55e', 4: '#86efac', 3: '#facc15', 2: '#fb923c', 1: '#ef4444' };
const SCORE_Y_LABEL = { 1: 'Плохо', 2: 'Грустно', 3: 'Нейтрально', 4: 'Хорошо', 5: 'Отлично' };
const PERIOD_LABEL = {
  week: 'неделю', two_weeks: 'две недели', month: 'месяц',
  three_months: 'три месяца', half_year: 'полгода', year: 'год',
};
const VERDICTS = [
  { min: 4.5, icon: '🌟', text: p => `За эту ${p} у вас было восхитительное настроение!` },
  { min: 4.0, icon: '😊', text: p => `За эту ${p} настроение было хорошим. Вы молодец!` },
  { min: 3.5, icon: '💪', text: p => `${p.charAt(0).toUpperCase() + p.slice(1)} прошёл неплохо.` },
  { min: 3.0, icon: '🌤', text: p => `За эту ${p} было по-разному. Всё наладится!` },
  { min: 2.5, icon: '🌱', text: p => `Эта ${p} далась непросто. Берегите себя!` },
  { min: 0,   icon: '❤️', text: () => `Было тяжело, но вы не сдаётесь. Вы не одни!` },
];

export default {
  name: 'ChartView',
  data() {
    return {
      selectedPeriod: 'month',
      chartData: [],
      isLoading: false,
      chartInstance: null,
      verdict: null,
      loadId: 0,
      filters: [
        { label: '7д', value: 'week' },
        { label: '2нед', value: 'two_weeks' },
        { label: 'Месяц', value: 'month' },
        { label: '3мес', value: 'three_months' },
        { label: 'Полгода', value: 'half_year' },
        { label: 'Год', value: 'year' },
      ],
      legend: [
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
    if (this.chartInstance) this.chartInstance.destroy();
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
      if (this.chartInstance) { this.chartInstance.destroy(); this.chartInstance = null; }
      try {
        const res = await api.getMoodChart(this.selectedPeriod);
        if (id !== this.loadId) return;
        this.chartData = res.data || [];
      } catch {
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
      const p = PERIOD_LABEL[this.selectedPeriod] || 'период';
      return { icon: bucket.icon, text: bucket.text(p) };
    },
    formatDate(dateStr) {
      return new Date(dateStr).toLocaleDateString('ru-RU', { day: 'numeric', month: 'short' });
    },
    renderChart() {
      try {
        const ctx = this.$refs.chartCanvas;
        if (!ctx) return;
        const labels = this.chartData.map(e => this.formatDate(e.date));
        const scores = this.chartData.map(e => MOOD_SCORE[e.mood] ?? 3);
        const pointColors = scores.map(s => SCORE_COLOR[s] ?? '#805AD5');
        const rawEntries = this.chartData;

        const gradient = ctx.getContext('2d').createLinearGradient(0, 0, 0, 220);
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
              pointRadius: 5,
              pointHoverRadius: 8,
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
                ticks: { color: '#94a3b8', maxTicksLimit: 7, maxRotation: 45, font: { size: 10 } },
              },
              y: {
                min: 0.5,
                max: 5.5,
                ticks: { stepSize: 1, color: '#94a3b8', callback: val => SCORE_Y_LABEL[val] || '', font: { size: 10 } },
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
                padding: 12,
                callbacks: {
                  title: items => {
                    const d = new Date(rawEntries[items[0].dataIndex].date);
                    return d.toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' });
                  },
                  label: items => {
                    const entry = rawEntries[items.dataIndex];
                    return `Настроение: ${MOOD_LABEL[entry.mood] || entry.mood}`;
                  },
                  afterLabel: items => {
                    const details = rawEntries[items.dataIndex].details;
                    if (!details) return '';
                    const words = details.split(' ');
                    const lines = [];
                    let line = 'Заметка: ';
                    for (const word of words) {
                      if ((line + word).length > 35) { lines.push(line.trimEnd()); line = word + ' '; }
                      else { line += word + ' '; }
                    }
                    if (line.trim()) lines.push(line.trimEnd());
                    return lines;
                  },
                },
              },
            },
          },
        });
      } catch { /* canvas was removed */ }
    },
  },
};
</script>

<style scoped>
.period-filters {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  padding-bottom: 4px;
  margin-bottom: 16px;
  scrollbar-width: none;
}
.period-filters::-webkit-scrollbar { display: none; }

.filter-btn {
  flex-shrink: 0;
  padding: 6px 14px;
  border-radius: 20px;
  border: 1px solid var(--border);
  background: transparent;
  color: var(--text-sub);
  font-size: 0.82rem;
  font-weight: 500;
  cursor: pointer;
  white-space: nowrap;
}

.filter-btn.active {
  background: var(--primary);
  border-color: var(--primary);
  color: white;
}

.chart-wrap {
  height: 260px;
  padding: 16px 8px;
  margin-bottom: 16px;
  position: relative;
}

.chart-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 40px 20px;
  text-align: center;
  color: var(--text-muted);
  margin-bottom: 16px;
}

.empty-icon { font-size: 2.5rem; opacity: 0.5; }
.empty-sub { font-size: 0.82rem; color: var(--text-muted); }

.chart-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  padding: 40px 0;
  color: var(--text-muted);
  font-size: 0.9rem;
}

.loader {
  width: 32px;
  height: 32px;
  border: 3px solid rgba(128, 90, 213, 0.2);
  border-top-color: #805AD5;
  border-radius: 50%;
  animation: spin 0.9s linear infinite;
}

@keyframes spin { to { transform: rotate(360deg); } }

.verdict-card {
  display: flex;
  align-items: center;
  gap: 12px;
  border-left: 3px solid var(--primary);
  margin-bottom: 16px;
}

.verdict-icon { font-size: 1.5rem; flex-shrink: 0; }

.verdict-card p {
  color: var(--text-sub);
  font-size: 0.88rem;
  line-height: 1.5;
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
  padding-bottom: 8px;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.78rem;
  color: var(--text-sub);
}

.legend-dot {
  width: 9px;
  height: 9px;
  border-radius: 50%;
  flex-shrink: 0;
}
</style>
