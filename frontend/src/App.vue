<template>
  <div class="app">
    <!-- Шапка с навигацией -->
    <header class="header">
      <nav class="nav">
        <router-link to="/" class="nav-link" active-class="active">Главная</router-link>
        <router-link to="/login" class="nav-link" active-class="active">Вход</router-link>
        <router-link to="/register" class="nav-link" active-class="active">Регистрация</router-link>
        <router-link to="/lk" class="nav-link" active-class="active">Личный кабинет</router-link>
      </nav>
    </header>

    <!-- Основной контент -->
    <main class="main">
      <router-view />
    </main>

    <!-- Подвал -->
    <footer class="footer">
      <p>© 2023 Watermelon inc. Все права защищены.</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
};
</script>

<style>
/* Общие стили */
body {
  margin: 0;
  font-family: Arial, sans-serif;
  background-color: #f8f9fa;
  color: #333;
}

.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

/* Шапка */
.header {
  background-color: #2c3e50;
  padding: 15px 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.nav {
  display: flex;
  justify-content: center;
  gap: 20px;
}

.nav-link {
  color: white;
  text-decoration: none;
  font-size: 1.1rem;
  padding: 5px 10px;
  border-radius: 5px;
  transition: background-color 0.3s ease;
}

.nav-link:hover {
  background-color: #1a2a36;
}

.nav-link.active {
  background-color: #1a2a36;
  font-weight: bold;
}

/* Основной контент */
.main {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

/* Подвал */
.footer {
  text-align: center;
  padding: 15px;
  background-color: #2c3e50;
  color: white;
  margin-top: auto;
}

/* Адаптивность */
@media (max-width: 768px) {
  .nav {
    flex-direction: column;
    align-items: center;
    gap: 10px;
  }

  .nav-link {
    width: 100%;
    text-align: center;
  }
}
</style>