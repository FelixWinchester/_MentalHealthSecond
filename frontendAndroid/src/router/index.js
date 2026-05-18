import { createRouter, createWebHashHistory } from 'vue-router';

import LoginView from '@/views/LoginView.vue';
import RegisterView from '@/views/RegisterView.vue';
import HomeView from '@/views/HomeView.vue';
import MoodView from '@/views/MoodView.vue';
import ChartView from '@/views/ChartView.vue';
import ForumView from '@/views/ForumView.vue';
import ThreadView from '@/views/ThreadView.vue';
import AchievementsView from '@/views/AchievementsView.vue';
import ProfileView from '@/views/ProfileView.vue';

const routes = [
  { path: '/', redirect: '/home' },
  { path: '/login', component: LoginView, meta: { guest: true } },
  { path: '/register', component: RegisterView, meta: { guest: true } },
  { path: '/home', component: HomeView, meta: { auth: true } },
  { path: '/mood', component: MoodView, meta: { auth: true } },
  { path: '/chart', component: ChartView, meta: { auth: true } },
  { path: '/forum', component: ForumView, meta: { auth: true } },
  { path: '/forum/:id', component: ThreadView, meta: { auth: true } },
  { path: '/achievements', component: AchievementsView, meta: { auth: true } },
  { path: '/profile', component: ProfileView, meta: { auth: true } },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

router.beforeEach((to, _from, next) => {
  const token = localStorage.getItem('token');
  if (to.meta.auth && !token) return next('/login');
  if (to.meta.guest && token) return next('/home');
  next();
});

export default router;
