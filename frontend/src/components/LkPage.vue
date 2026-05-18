<template>
  <div class="lk-page">
    <div v-if="isLoading" class="loading-screen">
      <div class="loader"></div>
      <p>Загрузка профиля...</p>
    </div>

    <main v-else class="content">
      
      <section class="hero-section">
        <div class="hero-content">
          <h1>Личный кабинет</h1>
          <p class="hero-subtitle">
            {{ isGuest ? 'Добро пожаловать! Зарегистрируйтесь, чтобы сохранить прогресс.' : `Рады видеть вас снова, ${userName}!` }}
          </p>
          
          <div v-if="isGuest" class="guest-warning">
            <div class="warning-icon">
              <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                <path d="M12 15.5C14.2091 15.5 16 13.7091 16 11.5C16 9.29086 14.2091 7.5 12 7.5C9.79086 7.5 8 9.29086 8 11.5C8 13.7091 9.79086 15.5 12 15.5Z" stroke="currentColor" stroke-width="2"/>
                <path d="M5 20.5C5 18.2909 6.79086 16.5 9 16.5H15C17.2091 16.5 19 18.2909 19 20.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
                <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
              </svg>
            </div>
            <div class="warning-content">
              <h4>Гостевой режим</h4>
              <p>Для сохранения вашего прогресса и данных требуется регистрация</p>
            </div>
            <button class="cta-button primary small" @click="goToRegister">
              Создать аккаунт
            </button>
          </div>
          
          <div class="hero-actions" v-else>
            <button class="cta-button secondary" @click="scrollToStats">
              <span class="button-icon">📊</span>
              Моя статистика
            </button>
            <button class="cta-button secondary" @click="scrollToSettings">
              <span class="button-icon">⚙️</span>
              Настройки
            </button>
          </div>
        </div>

        <div class="hero-visual">
          <div class="floating-card card-1">
            <div class="card-icon">👤</div>
            <p>Ваш профиль</p>
          </div>
          <div class="floating-card card-2">
            <div class="card-icon">📈</div>
            <p>Прогресс</p>
          </div>
          <div class="floating-card card-3">
            <div class="card-icon">🎯</div>
            <p>Достижения</p>
          </div>
        </div>
      </section>

      <section class="profile-section">
        <div class="profile-container">
          <h2>Ваш профиль</h2>
          <p class="section-description">Основная информация и настройки профиля</p>
          
          <div class="profile-content">
            <div class="avatar-section">
              <div class="avatar-container">
                <div class="avatar-circle">
                  <img
                    :src="avatar || 'https://via.placeholder.com/150/805AD5/FFFFFF?text=👤'"
                    alt="Аватар пользователя"
                    class="avatar"
                  />
                  <div class="avatar-overlay" v-if="!isGuest" @click="triggerAvatarUpload">
                    <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                      <path d="M4 16L8 12L12 16" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M12 8V20" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                      <path d="M17 12L20 15L17 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </svg>
                  </div>
                </div>
                <input
                  v-if="!isGuest"
                  type="file"
                  accept="image/*"
                  @change="handleAvatarChange"
                  style="display: none"
                  ref="avatarInput"
                />
                
                <button v-if="!isGuest" class="edit-button" @click="triggerAvatarUpload">
                  <span class="button-icon">🖼️</span>
                  Сменить аватар
                </button>
                
                <button v-else class="cta-button primary" @click="goToRegister">
                  <span class="button-icon">🚀</span>
                  Зарегистрироваться
                </button>
              </div>
            </div>
            
            <div class="profile-details">
              <div class="detail-card">
                <div class="detail-icon">👤</div>
                <div class="detail-content">
                  <label>Имя пользователя</label>
                  <h3>{{ userName }}</h3>
                </div>
              </div>
              
              <div class="detail-card">
                <div class="detail-icon">📧</div>
                <div class="detail-content">
                  <label>Email</label>
                  <h3>{{ userEmail }}</h3>
                </div>
              </div>
              
              <div class="detail-card">
                <div class="detail-icon">📅</div>
                <div class="detail-content">
                  <label>Дата регистрации</label>
                  <h3>{{ joinDate }}</h3>
                </div>
              </div>
              
              <div class="detail-card guest-badge" v-if="isGuest">
                <div class="detail-icon">⚠️</div>
                <div class="detail-content">
                  <label>Режим</label>
                  <h3>Гостевой</h3>
                  <p class="guest-note">Данные не сохраняются</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section class="chart-section" v-if="!isGuest">
        <MoodChart />
      </section>

      <section class="stats-section" id="stats-section">
        <div class="stats-container">
          <h2>Ваша активность</h2>
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-value">{{ completedTasks }}</div>
              <div class="stat-label">Завершено сессий</div>
            </div>
            
            <div class="stat-card">
              <div class="stat-value">{{ daysActive }}</div>
              <div class="stat-label">Дней с нами</div>
            </div>
            
            <div class="stat-card">
              <div class="stat-value">{{ achievements }}</div>
              <div class="stat-label">Достижения</div>
            </div>
          </div>
          
          <div v-if="isGuest" class="guest-stats-note">
            <div class="note-content">
              <h4>📊 Полная статистика</h4>
              <p>Зарегистрируйтесь, чтобы отслеживать весь ваш прогресс</p>
              <button class="outline-button" @click="goToRegister">
                Открыть все возможности
              </button>
            </div>
          </div>
        </div>
      </section>

      <section class="settings-section" id="settings-section">
        <div class="settings-container">
          <h2>Управление аккаунтом</h2>
          <div class="settings-grid">
            
            <template v-if="!isGuest">
              <button class="settings-card" @click="changePassword">
                <div class="settings-icon">🔒</div>
                <div class="settings-content">
                  <h3>Безопасность</h3>
                  <p>Изменить пароль</p>
                </div>
                <div class="settings-arrow">→</div>
              </button>
              
              <button class="settings-card" @click="updateEmail">
                <div class="settings-icon">📧</div>
                <div class="settings-content">
                  <h3>Контакты</h3>
                  <p>Обновить email</p>
                </div>
                <div class="settings-arrow">→</div>
              </button>
            </template>
            
            <button v-else class="settings-card primary" @click="goToRegister">
              <div class="settings-icon">✨</div>
              <div class="settings-content">
                <h3>Создать аккаунт</h3>
                <p>Получите полный доступ</p>
              </div>
              <div class="settings-arrow">→</div>
            </button>
            
            <button class="settings-card logout" @click="logout">
              <div class="settings-icon">🚪</div>
              <div class="settings-content">
                <h3>{{ isGuest ? 'Покинуть гостевой режим' : 'Выйти из аккаунта' }}</h3>
                <p>Завершить текущую сессию</p>
              </div>
              <div class="settings-arrow">→</div>
            </button>
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<script>
import api from '@/api/api';
import MoodChart from '@/components/MoodChart.vue';

export default {
  name: 'LkPage',
  components: { MoodChart },
  data() {
    return {
      isLoading: true, // По умолчанию идет загрузка
      isGuest: false,  // По умолчанию считаем, что пользователь не гость
      userName: 'Пользователь',
      userEmail: '',
      joinDate: '',
      completedTasks: 0,
      daysActive: 0,
      achievements: 0,
      avatar: ''
    };
  },
  async created() {
    await this.checkAuth();
    this.isLoading = false; // После проверки выключаем экран загрузки
  },
  methods: {
    async checkAuth() {
      const token = localStorage.getItem('token');
      const guestData = localStorage.getItem('guestUser');
      
      if (token) {
        try {
          const response = await api.getUserInfo(token);
          if (response.data) {
            this.userName = response.data.username;
            this.userEmail = response.data.email;
            this.joinDate = new Date(response.data.created_at).toLocaleDateString('ru-RU');
            this.avatar = response.data.avatar_path || '';
            this.isGuest = false;
            await this.loadUserStats();
            return; // Успешно авторизован
          }
        } catch (error) {
          console.error('Ошибка сессии:', error);
          localStorage.removeItem('token'); // Чистим невалидный токен
        }
      }
      
      // Если токена нет или произошла ошибка — проверяем гостевой вход
      if (guestData) {
        this.setupGuestMode();
      } else {
        // Если нет ни токена, ни гостевых данных — на главную
        this.$router.push('/');
      }
    },
    
    setupGuestMode() {
      const guestData = JSON.parse(localStorage.getItem('guestUser') || '{}');
      this.userName = guestData.name || 'Гость';
      this.userEmail = guestData.email || '—';
      this.avatar = guestData.avatar || '';
      this.joinDate = new Date().toLocaleDateString('ru-RU');
      this.isGuest = true;
      
      // Демо-данные для гостя
      this.completedTasks = 3;
      this.daysActive = 1;
      this.achievements = 0;
    },
    
    async loadUserStats() {
      try {
        // Здесь предполагается ваш вызов к API
        // const stats = await api.getUserStats();
        this.completedTasks = 12;
        this.daysActive = 5;
        this.achievements = 2;
      } catch (error) {
        console.error('Ошибка загрузки статистики:', error);
      }
    },

    triggerAvatarUpload() {
      if (this.$refs.avatarInput) this.$refs.avatarInput.click();
    },
    
    async handleAvatarChange(event) {
      const file = event.target.files[0];
      if (file && !this.isGuest) {
        try {
          const token = localStorage.getItem('token');
          const formData = new FormData();
          formData.append('avatar', file);
          const response = await api.updateUserInfo(token, formData);
          if (response.data) {
            this.avatar = response.data.avatar_path;
            alert('Аватар обновлен!');
          }
        } catch (error) {
          alert('Ошибка загрузки: ' + (error.response?.data?.detail || 'Ошибка'));
        }
      }
    },
    
    changePassword() { alert('Смена пароля в разработке'); },
    updateEmail() { alert('Смена email в разработке'); },
    goToRegister() { this.$router.push('/register'); },
    
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('guestUser');
      this.$router.push('/');
    },

    scrollToStats() {
      document.getElementById('stats-section')?.scrollIntoView({ behavior: 'smooth' });
    },

    scrollToSettings() {
      document.getElementById('settings-section')?.scrollIntoView({ behavior: 'smooth' });
    }
  }
};
</script>

<style scoped>
/* СТИЛИ */
.lk-page {
  background-color: #0f172a;
  min-height: 100vh;
  color: #e2e8f0;
  font-family: sans-serif;
}

/* Экран загрузки */
.loading-screen {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  height: 100vh;
  gap: 1.5rem;
}

.loader {
  width: 50px;
  height: 50px;
  border: 4px solid rgba(128, 90, 213, 0.2);
  border-top-color: #805AD5;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.content {
  padding: 0 5vw 4rem;
  max-width: 1200px;
  margin: 0 auto;
}

/* Секции */
section {
  margin-bottom: 6rem;
}

h1, h2 {
  font-weight: 800;
  text-align: center;
}

.hero-section {
  padding-top: 4rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 3rem;
}

.hero-content h1 {
  font-size: clamp(2rem, 5vw, 3.5rem);
  background: linear-gradient(135deg, #805AD5, #667eea);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1rem;
}

/* Баннеры и карточки */
.guest-warning {
  background: rgba(128, 90, 213, 0.1);
  border: 1px solid rgba(128, 90, 213, 0.4);
  border-radius: 16px;
  padding: 1.5rem 2rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  max-width: 700px;
  margin: 2rem auto;
}

.profile-container, .stats-container, .settings-container {
  background: #1e293b;
  border-radius: 24px;
  padding: 2.5rem;
  border: 1px solid #334155;
}

.profile-content {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 3rem;
  margin-top: 2rem;
}

.avatar-circle {
  width: 200px;
  height: 200px;
  border-radius: 50%;
  overflow: hidden;
  position: relative;
  border: 4px solid #805AD5;
  margin-bottom: 1.5rem;
}

.avatar {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.avatar-overlay {
  position: absolute;
  inset: 0;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: 0.3s;
  cursor: pointer;
}

.avatar-circle:hover .avatar-overlay {
  opacity: 1;
}

.detail-card {
  background: #0f172a;
  padding: 1.2rem;
  border-radius: 12px;
  display: flex;
  align-items: center;
  gap: 1rem;
  margin-bottom: 1rem;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 1.5rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: #0f172a;
  padding: 2rem;
  border-radius: 20px;
  text-align: center;
  border: 1px solid #334155;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: #805AD5;
}

/* Кнопки */
.cta-button {
  padding: 0.8rem 1.8rem;
  border-radius: 10px;
  border: none;
  font-weight: 600;
  cursor: pointer;
  transition: 0.3s;
}

.primary { background: #805AD5; color: white; }
.primary:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(128,90,213,0.4); }

.secondary { background: transparent; border: 1px solid #805AD5; color: white; }
.secondary:hover { background: rgba(128, 90, 213, 0.1); }

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 1.2rem;
}

.settings-card {
  background: #0f172a;
  border: 1px solid #334155;
  padding: 1.5rem;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 1rem;
  cursor: pointer;
  transition: 0.3s;
  text-align: left;
  color: white;
}

.settings-card:hover { border-color: #805AD5; transform: translateX(5px); }

.logout { border-color: rgba(239, 68, 68, 0.3); }
.logout:hover { border-color: #ef4444; color: #ef4444; }

/* Адаптивность */
@media (max-width: 768px) {
  .profile-content { grid-template-columns: 1fr; justify-items: center; }
  .hero-visual { display: none; }
}
</style>