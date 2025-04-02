import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import LkPage from '../components/LkPage.vue';

const routes = [
  {
    path: '/:page?', // Добавляем параметр :page
    component: HomePage,
    props: true, // Передаем параметры как props
  },
  {
    path: '/login/:page?', // Добавляем параметр :page
    component: LoginPage,
    props: true,
  },
  {
    path: '/register/:page?', // Добавляем параметр :page
    component: RegisterPage,
    props: true,
  },
  {
    path: '/lk/:page?', // Добавляем параметр :page
    component: LkPage,
    props: true,
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;