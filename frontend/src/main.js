import { createApp } from 'vue';
import App from './App.vue';
import router from './router'; // Импорт маршрутов

createApp(App)
  .use(router) // Использование Vue Router
  .mount('#app');