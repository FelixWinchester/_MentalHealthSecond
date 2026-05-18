<template>
  <div class="page">
    <div class="page-header">
      <h1 class="page-title">Достижения</h1>
      <p class="page-sub">Ваши успехи</p>
    </div>

    <div class="stub-card card">
      <div class="stub-icon">🏆</div>
      <h3>Скоро здесь появятся достижения</h3>
      <p>Отмечайте настроение каждый день и зарабатывайте награды!</p>
      <div class="stub-examples">
        <div class="example-badge">🔥 Серия 7 дней</div>
        <div class="example-badge">⭐ Первая запись</div>
        <div class="example-badge">💎 Серия 30 дней</div>
        <div class="example-badge">🌟 Серия 100 дней</div>
      </div>
    </div>
  </div>
</template>

<script>
export default { name: 'AchievementsView' };
</script>

<style scoped>
.stub-card {
  text-align: center;
  padding: 40px 20px;
}

.stub-icon {
  font-size: 3.5rem;
  margin-bottom: 16px;
}

.stub-card h3 {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text);
  margin-bottom: 10px;
}

.stub-card p {
  color: var(--text-muted);
  font-size: 0.88rem;
  line-height: 1.5;
  margin-bottom: 24px;
}

.stub-examples {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  justify-content: center;
}

.example-badge {
  background: var(--surface2);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 8px 16px;
  font-size: 0.85rem;
  color: var(--text-sub);
}
</style>
