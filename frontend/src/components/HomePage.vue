<template>
  <div class="home-page">
    <!-- Заголовок страницы -->
    <header class="header">
      <h1>{{ pageTitle }}</h1>
      <p>Добро пожаловать на наш сайт! Мы заботимся о вашем психическом здоровье.</p>
    </header>

    <!-- Основной контент -->
    <main class="content">
      <!-- Секция с приветствием -->
      <section class="section welcome-section">
        <div class="welcome-text">
          <h2>Почему это важно?</h2>
          <p>
            Психическое здоровье так же важно, как и физическое. Оно влияет на наше настроение, продуктивность
            и качество жизни. Забота о себе — это первый шаг к счастливой и гармоничной жизни.
          </p>
          <button class="cta-button" @click="scrollToFeatures">Узнать больше</button>
        </div>
        <div class="welcome-image">
          <img
            src="https://via.placeholder.com/400x300"
            alt="Психическое здоровье"
            class="image"
          />
        </div>
      </section>

      <!-- Секция с преимуществами -->
      <section class="section features-section" ref="features">
        <h2>Наши преимущества</h2>
        <div class="features-container">
          <div class="feature-item">
            <img
              src="https://via.placeholder.com/100x100"
              alt="Поддержка"
              class="feature-icon"
            />
            <h3>Поддержка 24/7</h3>
            <p>Мы всегда готовы помочь вам в трудную минуту.</p>
          </div>
          <div class="feature-item">
            <img
              src="https://via.placeholder.com/100x100"
              alt="Эксперты"
              class="feature-icon"
            />
            <h3>Искуственный интеллект</h3>
            <p>Наш ИИ готов помогать вам с вашими ментальными проблемами в любую минуту.</p>
          </div>
          <div class="feature-item">
            <img
              src="https://via.placeholder.com/100x100"
              alt="Доступность"
              class="feature-icon"
            />
            <h3>Доступность</h3>
            <p>Мы предоставляем услуги для всех, независимо от возраста и дохода.</p>
          </div>
        </div>
      </section>

      <!-- Секция с цитатой -->
      <section class="section quote-section">
        <blockquote class="quote">
          "Здоровье — это не просто отсутствие болезней, это состояние полного физического, психического
          и социального благополучия."
          <footer>— Всемирная организация здравоохранения</footer>
        </blockquote>
      </section>
    </main>
  </div>
</template>

<script>
export default {
  name: 'HomePage',
  props: {
    page: {
      type: String,
      default: 'Главная страница', // Значение по умолчанию
    },
  },
  computed: {
    pageTitle() {
      return this.page || 'Главная страница';
    },
  },
  methods: {
    scrollToFeatures() {
      this.$refs.features.scrollIntoView({ behavior: 'smooth' });
    },
  },
};
</script>

<style scoped>
.home-page {
  font-family: Arial, sans-serif;
  color: #333;
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
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

.welcome-section {
  display: flex;
  align-items: center;
  gap: 40px;
}

.welcome-text {
  flex: 1;
}

.welcome-text p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #444;
  margin-bottom: 20px;
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

.welcome-image img {
  max-width: 100%;
  border-radius: 10px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.features-section {
  text-align: center;
}

.features-container {
  display: flex;
  justify-content: space-around;
  gap: 20px;
}

.feature-item {
  flex: 1;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 10px;
  background-color: #f8f9fa;
}

.feature-icon {
  width: 100px;
  height: 100px;
  margin-bottom: 10px;
}

.feature-item h3 {
  font-size: 1.5rem;
  color: #2c3e50;
  margin-bottom: 10px;
}

.feature-item p {
  font-size: 1rem;
  color: #666;
}

.quote-section {
  text-align: center;
}

.quote {
  font-style: italic;
  font-size: 1.2rem;
  color: #555;
  border-left: 4px solid #2c3e50;
  padding-left: 20px;
  margin: 20px 0;
}

.quote footer {
  font-size: 1rem;
  color: #777;
  margin-top: 10px;
}

.footer {
  text-align: center;
  padding: 20px;
  background-color: #f8f9fa;
  border-top: 1px solid #ddd;
  margin-top: 40px;
}

.footer p {
  font-size: 0.9rem;
  color: #666;
}
</style>