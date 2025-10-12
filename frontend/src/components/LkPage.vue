<template>
  <div class="lk-page">
    <!-- Основной контент -->
    <main class="content">
      <!-- Герой секция -->
      <section class="hero-section">
        <div class="hero-content">
          <h1>Личный кабинет</h1>
          <p class="hero-subtitle">Добро пожаловать, {{ userName }}! Рады видеть вас снова</p>
          
          <!-- Баннер гостевого режима -->
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

      <!-- Секция с информацией о пользователе -->
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
                <button 
                  v-if="!isGuest" 
                  class="edit-button" 
                  @click="triggerAvatarUpload"
                >
                  <span class="button-icon">🖼️</span>
                  Сменить аватар
                </button>
                <button 
                  v-else 
                  class="cta-button primary" 
                  @click="goToRegister"
                >
                  <span class="button-icon">🚀</span>
                  Зарегистрироваться
                </button>
              </div>
            </div>
            
            <div class="profile-details">
              <div class="detail-card">
                <div class="detail-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M20 21V19C20 17.9391 19.5786 16.9217 18.8284 16.1716C18.0783 15.4214 17.0609 15 16 15H8C6.93913 15 5.92172 15.4214 5.17157 16.1716C4.42143 16.9217 4 17.9391 4 19V21" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M12 11C14.2091 11 16 9.20914 16 7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7C8 9.20914 9.79086 11 12 11Z" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <label>Имя пользователя</label>
                  <h3>{{ userName }}</h3>
                </div>
              </div>
              
              <div class="detail-card">
                <div class="detail-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M4 4H20C21.1 4 22 4.9 22 6V18C22 19.1 21.1 20 20 20H4C2.9 20 2 19.1 2 18V6C2 4.9 2.9 4 4 4Z" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    <path d="M22 6L12 13L2 6" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <label>Email</label>
                  <h3>{{ userEmail }}</h3>
                </div>
              </div>
              
              <div class="detail-card">
                <div class="detail-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M8 7V3M16 7V3M7 11H17M5 21H19C20.1046 21 21 20.1046 21 19V7C21 5.89543 20.1046 5 19 5H5C3.89543 5 3 5.89543 3 7V19C3 20.1046 3.89543 21 5 21Z" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  </svg>
                </div>
                <div class="detail-content">
                  <label>Дата регистрации</label>
                  <h3>{{ joinDate }}</h3>
                </div>
              </div>
              
              <div class="detail-card" v-if="isGuest">
                <div class="detail-icon">
                  <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
                    <path d="M12 15.5C14.2091 15.5 16 13.7091 16 11.5C16 9.29086 14.2091 7.5 12 7.5C9.79086 7.5 8 9.29086 8 11.5C8 13.7091 9.79086 15.5 12 15.5Z" stroke="#805AD5" stroke-width="2"/>
                    <path d="M5 20.5C5 18.2909 6.79086 16.5 9 16.5H15C17.2091 16.5 19 18.2909 19 20.5" stroke="#805AD5" stroke-width="2" stroke-linecap="round"/>
                    <circle cx="12" cy="12" r="10" stroke="#805AD5" stroke-width="2"/>
                  </svg>
                </div>
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

      <!-- Секция со статистикой -->
      <section class="stats-section" id="stats-section">
        <div class="stats-container">
          <h2>Ваша активность</h2>
          <p class="section-description">Отслеживайте ваш прогресс и достижения</p>
          
          <div class="stats-grid">
            <div class="stat-card">
              <div class="stat-icon">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                  <path d="M9 11L12 14L22 4" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M21 12V19C21 19.5304 20.7893 20.0391 20.4142 20.4142C20.0391 20.7893 19.5304 21 19 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H16" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="stat-content">
                <span class="stat-value">{{ completedTasks }}</span>
                <span class="stat-label">Завершено сессий</span>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                  <path d="M21 10H3M16 2V6M8 2V6M10.5 14L12 13V18M10.75 18H13.25M7 21H17C18.1046 21 19 20.1046 19 19V7C19 5.89543 18.1046 5 17 5H7C5.89543 5 5 5.89543 5 7V19C5 20.1046 5.89543 21 7 21Z" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="stat-content">
                <span class="stat-value">{{ daysActive }}</span>
                <span class="stat-label">Дней с нами</span>
              </div>
            </div>
            
            <div class="stat-card">
              <div class="stat-icon">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none">
                  <path d="M12 2L15.09 8.26L22 9.27L17 14.14L18.18 21.02L12 17.77L5.82 21.02L7 14.14L2 9.27L8.91 8.26L12 2Z" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="stat-content">
                <span class="stat-value">{{ achievements }}</span>
                <span class="stat-label">Достижения</span>
              </div>
            </div>
          </div>
          
          <div v-if="isGuest" class="guest-stats-note">
            <div class="note-content">
              <h4>📊 Полная статистика</h4>
              <p>Зарегистрируйтесь, чтобы отслеживать весь ваш прогресс и получить доступ к расширенной статистике</p>
              <button class="outline-button" @click="goToRegister">
                Открыть все возможности
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- Секция с настройками -->
      <section class="settings-section" id="settings-section">
        <div class="settings-container">
          <h2>Управление аккаунтом</h2>
          <p class="section-description">Настройки безопасности и параметры вашего профиля</p>
          
          <div class="settings-grid">
            <button 
              v-if="!isGuest" 
              class="settings-card" 
              @click="changePassword"
            >
              <div class="settings-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                  <path d="M12 15V17M6 21H18C19.1046 21 20 20.1046 20 19V13C20 11.8954 19.1046 11 18 11H6C4.89543 11 4 11.8954 4 13V19C4 20.1046 4.89543 21 6 21Z" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M16 11V7C16 4.79086 14.2091 3 12 3C9.79086 3 8 4.79086 8 7V11" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="settings-content">
                <h3>Безопасность</h3>
                <p>Изменить пароль и настройки входа</p>
              </div>
              <div class="settings-arrow">→</div>
            </button>
            
            <button 
              v-if="!isGuest" 
              class="settings-card" 
              @click="updateEmail"
            >
              <div class="settings-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                  <path d="M4 4H20C21.1 4 22 4.9 22 6V18C22 19.1 21.1 20 20 20H4C2.9 20 2 19.1 2 18V6C2 4.9 2.9 4 4 4Z" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M22 6L12 13L2 6" stroke="#805AD5" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="settings-content">
                <h3>Контакты</h3>
                <p>Обновить email и способ связи</p>
              </div>
              <div class="settings-arrow">→</div>
            </button>
            
            <button 
              v-if="isGuest" 
              class="settings-card primary" 
              @click="goToRegister"
            >
              <div class="settings-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                  <path d="M16 21V19C16 17.9391 15.5786 16.9217 14.8284 16.1716C14.0783 15.4214 13.0609 15 12 15H5C3.93913 15 2.92172 15.4214 2.17157 16.1716C1.42143 16.9217 1 17.9391 1 19V21" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M8.5 11C10.7091 11 12.5 9.20914 12.5 7C12.5 4.79086 10.7091 3 8.5 3C6.29086 3 4.5 4.79086 4.5 7C4.5 9.20914 6.29086 11 8.5 11Z" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M20 8V14M23 11H17" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="settings-content">
                <h3>Создать аккаунт</h3>
                <p>Получите полный доступ ко всем функциям</p>
              </div>
              <div class="settings-arrow">→</div>
            </button>
            
            <button class="settings-card logout" @click="logout">
              <div class="settings-icon">
                <svg width="32" height="32" viewBox="0 0 24 24" fill="none">
                  <path d="M9 21H5C4.46957 21 3.96086 20.7893 3.58579 20.4142C3.21071 20.0391 3 19.5304 3 19V5C3 4.46957 3.21071 3.96086 3.58579 3.58579C3.96086 3.21071 4.46957 3 5 3H9" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M16 17L21 12L16 7" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M21 12H9" stroke="#ef4444" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
              </div>
              <div class="settings-content">
                <h3>{{ isGuest ? 'Выйти из гостевого режима' : 'Выйти из аккаунта' }}</h3>
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

export default {
  name: 'LkPage',
  data() {
    return {
      userName: 'Гость',
      userEmail: 'guest@example.com',
      joinDate: new Date().toLocaleDateString('ru-RU'),
      completedTasks: 0,
      daysActive: 0,
      achievements: 0,
      avatar: '',
      isGuest: true
    };
  },
  async created() {
    await this.checkAuth();
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
          }
        } catch (error) {
          console.error('Ошибка при получении информации о пользователе:', error);
          this.setupGuestMode();
        }
      } else if (guestData) {
        this.setupGuestMode();
      } else {
        this.$router.push('/');
      }
    },
    
    setupGuestMode() {
      const guestData = localStorage.getItem('guestUser');
      if (guestData) {
        const userData = JSON.parse(guestData);
        this.userName = userData.name;
        this.userEmail = userData.email;
        this.avatar = userData.avatar || '';
      }
      this.joinDate = new Date().toLocaleDateString('ru-RU');
      this.isGuest = true;
      
      // Демо-статистика для гостя
      this.completedTasks = 3;
      this.daysActive = 1;
      this.achievements = 0;
    },
    
    async loadUserStats() {
      try {
        // Здесь можно добавить запросы к API для получения статистики
        // const statsResponse = await api.getUserStats();
        // this.completedTasks = statsResponse.data.completed_tasks;
        // this.daysActive = statsResponse.data.days_active;
        // this.achievements = statsResponse.data.achievements;
        
        // Временные демо-данные
        this.completedTasks = 12;
        this.daysActive = Math.floor((new Date() - new Date(this.joinDate)) / (1000 * 60 * 60 * 24));
        this.achievements = 2;
      } catch (error) {
        console.error('Ошибка при загрузке статистики:', error);
      }
    },

    triggerAvatarUpload() {
      this.$refs.avatarInput.click();
    },
    
    async handleAvatarChange(event) {
      const file = event.target.files[0];
      if (file) {
        try {
          await this.updateAvatar(file);
          alert('Аватар успешно обновлен!');
        } catch (error) {
          console.error('Ошибка при обновлении аватара:', error);
          alert('Ошибка при обновлении аватара: ' + (error.response?.data?.detail || 'Неизвестная ошибка'));
        }
      }
    },
    
    async updateAvatar(file) {
      const token = localStorage.getItem('token');
      if (token) {
        const formData = new FormData();
        formData.append('avatar', file);
        const response = await api.updateUserInfo(token, formData);
        if (response.data) {
          this.avatar = response.data.avatar_path;
        }
      }
    },
    
    changePassword() {
      alert('Функция изменения пароля в разработке.');
    },
    
    updateEmail() {
      alert('Функция изменения email в разработке.');
    },
    
    goToRegister() {
      this.$router.push('/register');
    },
    
    logout() {
      if (this.isGuest) {
        localStorage.removeItem('guestUser');
      } else {
        localStorage.removeItem('token');
      }
      this.$router.push('/');
    },

    scrollToStats() {
      const element = document.getElementById('stats-section');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    },

    scrollToSettings() {
      const element = document.getElementById('settings-section');
      if (element) {
        element.scrollIntoView({ behavior: 'smooth' });
      }
    }
  },
};
</script>

<style scoped>
/* Основные стили из главной страницы */
.lk-page {
  color: #e2e8f0;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
  line-height: 1.6;
}

.content {
  position: relative;
  z-index: 2;
  width: 100%;
  box-sizing: border-box;
  margin: 0;
  padding: 0rem 5vw;
}

section {
  margin-bottom: 8rem;
}

h2 {
  text-align: center;
  font-size: clamp(1.8rem, 4vw, 2.5rem);
  margin-bottom: 1rem;
  color: #e2e8f0;
  font-weight: 700;
}

.section-description {
  text-align: center;
  color: #94a3b8;
  font-size: clamp(1rem, 2.5vw, 1.2rem);
  margin-bottom: 3rem;
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

/* Герой-секция */
.hero-section {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
  padding: 4rem 0;
  gap: 3rem;
}

.hero-content {
  text-align: center;
  max-width: 900px;
}

.hero-content h1 {
  font-size: clamp(2.5rem, 5vw, 3.5rem);
  font-weight: 800;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  margin-bottom: 1.5rem;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: clamp(1.2rem, 2.5vw, 1.5rem);
  color: #cbd5e1;
  margin-bottom: 2.5rem;
  line-height: 1.6;
}

.hero-actions {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
}

.cta-button {
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  font-size: 1.1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  border: none;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.cta-button.primary {
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  color: white;
}

.cta-button.primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 25px rgba(128, 90, 213, 0.4);
}

.cta-button.secondary {
  background: transparent;
  color: #e2e8f0;
  border: 1px solid #805AD5;
}

.cta-button.secondary:hover {
  background: rgba(128, 90, 213, 0.1);
  transform: translateY(-2px);
}

.cta-button.small {
  padding: 0.75rem 1.5rem;
  font-size: 1rem;
}

.button-icon {
  font-size: 1.2rem;
}

/* Баннер гостевого режима */
.guest-warning {
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid #805AD5;
  border-radius: 16px;
  padding: 2rem;
  margin: 2rem 0;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  text-align: left;
  box-shadow: 0 10px 30px rgba(128, 90, 213, 0.2);
}

.warning-icon {
  width: 60px;
  height: 60px;
  background: rgba(128, 90, 213, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.warning-icon svg {
  color: #805AD5;
}

.warning-content {
  flex: 1;
}

.warning-content h4 {
  color: #e2e8f0;
  margin: 0 0 0.5rem 0;
  font-size: 1.3rem;
}

.warning-content p {
  color: #94a3b8;
  margin: 0;
  line-height: 1.5;
}

.hero-visual {
  position: relative;
  width: 100%;
  max-width: 1000px;
  height: 250px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.floating-card {
  position: absolute;
  background: rgba(15, 23, 42, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 1.5rem;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
  width: 180px;
  transition: all 0.5s ease;
}

.floating-card:hover {
  transform: translateY(-5px);
}

.card-1 {
  top: 10%;
  left: 10%;
  animation: float 6s ease-in-out infinite;
}

.card-2 {
  top: 20%;
  right: 15%;
  animation: float 7s ease-in-out infinite 1s;
}

.card-3 {
  bottom: 10%;
  left: 50%;
  transform: translateX(-50%);
  animation: float 8s ease-in-out infinite 2s;
}

.card-icon {
  font-size: 2rem;
  margin-bottom: 0.5rem;
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

/* Секция профиля */
.profile-section {
  padding: 4rem 0;
}

.profile-container {
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid #334155;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
}

.profile-content {
  display: grid;
  grid-template-columns: 300px 1fr;
  gap: 3rem;
  align-items: start;
}

.avatar-section {
  text-align: center;
}

.avatar-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.avatar-circle {
  position: relative;
  width: 200px;
  height: 200px;
  border-radius: 50%;
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  padding: 8px;
  box-shadow: 0 10px 30px rgba(128, 90, 213, 0.3);
}

.avatar {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
  border: 4px solid #1e293b;
}

.avatar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  opacity: 0;
  transition: all 0.3s ease;
  cursor: pointer;
}

.avatar-circle:hover .avatar-overlay {
  opacity: 1;
}

.avatar-overlay svg {
  color: white;
  width: 32px;
  height: 32px;
}

.edit-button {
  background: transparent;
  color: #e2e8f0;
  border: 1px solid #805AD5;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 500;
}

.edit-button:hover {
  background: rgba(128, 90, 213, 0.1);
  transform: translateY(-2px);
}

.profile-details {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.detail-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s ease;
}

.detail-card:hover {
  border-color: #805AD5;
  transform: translateY(-2px);
}

.detail-icon {
  width: 50px;
  height: 50px;
  background: rgba(128, 90, 213, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.detail-content label {
  display: block;
  color: #94a3b8;
  font-size: 0.9rem;
  margin-bottom: 0.25rem;
}

.detail-content h3 {
  color: #e2e8f0;
  margin: 0;
  font-size: 1.2rem;
}

.guest-note {
  color: #805AD5;
  font-size: 0.9rem;
  margin: 0.25rem 0 0 0;
  font-style: italic;
}

/* Секция статистики */
.stats-section {
  padding: 4rem 0;
}

.stats-container {
  background: linear-gradient(135deg, rgba(128, 90, 213, 0.05) 0%, rgba(102, 126, 234, 0.05) 100%);
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.stat-card {
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 2.5rem 2rem;
  text-align: center;
  transition: all 0.3s ease;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
}

.stat-card:hover {
  transform: translateY(-10px);
  border-color: #805AD5;
}

.stat-icon {
  width: 80px;
  height: 80px;
  background: rgba(128, 90, 213, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.stat-content {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 800;
  color: #805AD5;
  line-height: 1;
}

.stat-label {
  color: #94a3b8;
  font-size: 1rem;
  font-weight: 500;
}

.guest-stats-note {
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 2.5rem;
  text-align: center;
}

.note-content h4 {
  color: #e2e8f0;
  margin-bottom: 1rem;
  font-size: 1.3rem;
}

.note-content p {
  color: #94a3b8;
  margin-bottom: 1.5rem;
  line-height: 1.6;
}

.outline-button {
  background: transparent;
  border: 1px solid #805AD5;
  color: #cbd5e1;
  padding: 0.75rem 1.5rem;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
}

.outline-button:hover {
  background: rgba(128, 90, 213, 0.1);
  transform: translateY(-2px);
}

/* Секция настроек */
.settings-section {
  padding: 4rem 0;
}

.settings-container {
  background: rgba(15, 23, 42, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid #334155;
  border-radius: 20px;
  padding: 3rem;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.5);
}

.settings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 1.5rem;
}

.settings-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 16px;
  padding: 2rem;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  text-align: left;
  border: none;
  width: 100%;
}

.settings-card:hover {
  transform: translateY(-5px);
  border-color: #805AD5;
  box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
}

.settings-card.primary {
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  color: white;
}

.settings-card.primary:hover {
  background: linear-gradient(135deg, #7048c8 0%, #5a6fd8 100%);
}

.settings-card.logout {
  background: rgba(239, 68, 68, 0.1);
  border: 1px solid rgba(239, 68, 68, 0.3);
}

.settings-card.logout:hover {
  background: rgba(239, 68, 68, 0.2);
  border-color: #ef4444;
}

.settings-icon {
  width: 60px;
  height: 60px;
  background: rgba(128, 90, 213, 0.1);
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.settings-card.primary .settings-icon {
  background: rgba(255, 255, 255, 0.2);
}

.settings-card.logout .settings-icon {
  background: rgba(239, 68, 68, 0.2);
}

.settings-content {
  flex: 1;
}

.settings-content h3 {
  color: #e2e8f0;
  margin: 0 0 0.5rem 0;
  font-size: 1.2rem;
}

.settings-card.primary .settings-content h3,
.settings-card.primary .settings-content p {
  color: white;
}

.settings-card.logout .settings-content h3 {
  color: #ef4444;
}

.settings-content p {
  color: #94a3b8;
  margin: 0;
  font-size: 0.9rem;
  line-height: 1.4;
}

.settings-arrow {
  color: #94a3b8;
  font-size: 1.2rem;
  font-weight: 300;
  transition: all 0.3s ease;
}

.settings-card:hover .settings-arrow {
  color: #805AD5;
  transform: translateX(5px);
}

.settings-card.primary:hover .settings-arrow {
  color: white;
}

.settings-card.logout:hover .settings-arrow {
  color: #ef4444;
}

/* Адаптивность */
@media (max-width: 768px) {
  .content {
    padding: 0rem 3vw;
  }

  .hero-section {
    min-height: 60vh;
    padding: 2rem 0;
  }

  .profile-content {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 2rem;
  }

  .guest-warning {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .settings-grid {
    grid-template-columns: 1fr;
  }

  .settings-card {
    padding: 1.5rem;
  }

  .floating-card {
    position: relative;
    margin-bottom: 1rem;
    left: auto;
    right: auto;
    top: auto;
    bottom: auto;
    transform: none;
    width: 100%;
    max-width: 250px;
  }

  .hero-visual {
    flex-direction: column;
    height: auto;
    gap: 1rem;
  }
}

@media (max-width: 480px) {
  .hero-actions {
    flex-direction: column;
  }

  .cta-button {
    width: 100%;
    justify-content: center;
  }

  .avatar-circle {
    width: 150px;
    height: 150px;
  }

  .detail-card {
    flex-direction: column;
    text-align: center;
    gap: 1rem;
  }
}
</style>