import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import Particles from "vue3-particles";
import api from '@/api/api'; // Добавляем импорт api

const app = createApp(App);

// Добавляем api в глобальные свойства
app.config.globalProperties.$api = api;

app.use(router)
app.use(Particles)
   .mount('#app');