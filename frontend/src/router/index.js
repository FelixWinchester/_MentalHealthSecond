import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import LoginPage from '../components/LoginPage.vue';
import RegisterPage from '../components/RegisterPage.vue';
import LkPage from '../components/LkPage.vue';
import ConditionPage from '@/components/ConditionPage.vue';
import ChatPage from "@/components/ChatPage.vue";
import ForumView from '../components/ForumView.vue';
import ThreadDetailsPage from '../components/ThreadDetailsPage.vue';

const routes = [
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
  {
    path: '/condition/:page?', // Добавляем параметр :page
    component: ConditionPage,
    props: true,
  },

  {
    path: '/forum',
    name: 'Forum',
    component: ForumView
  },

  {
    path: '/forum/thread/:id',
    name: 'ThreadDetails',
    component: ThreadDetailsPage,
    props: true
  },

  { path: "/chat", name: "Chat", component: ChatPage },
  {
    path: '/:page?', // Добавляем параметр :page
    component: HomePage,
    props: true, // Передаем параметры как props
  },

];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;