<template>
  <div class="app">
    <!-- Боковая шапка -->
    <aside class="sidebar">
      <h1 class="logo">Serenity</h1>
      <nav class="nav">
        <router-link to="/" class="nav-link" active-class="active">Главная</router-link>
        <router-link to="/forum" class="nav-link" active-class="active">Сообщество</router-link>
        <router-link to="/condition" class="nav-link" active-class="active">Состояние</router-link>
        <router-link to="/chat" class="nav-link" active-class="active">Чат</router-link>

        
        <!-- Компонент профиля -->
        <div class="profile-container">
          <div class="profile-trigger" @click="toggleProfileMenu">
            <div class="profile-avatar">
              <img v-if="user.avatar" :src="user.avatar" alt="Аватар" />
              <div v-else class="default-avatar">
                {{ userInitials }}
              </div>
            </div>
            <span class="profile-name">{{ isAuthenticated ? user.name : 'Профиль' }}</span>
            <svg class="dropdown-arrow" :class="{ 'rotated': showProfileMenu }" width="12" height="7" viewBox="0 0 12 7" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M1 1L6 6L11 1" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
          
          <!-- Выпадающее меню профиля -->
          <div v-if="showProfileMenu" class="profile-dropdown">
            <div v-if="isAuthenticated" class="dropdown-section">
              <div class="user-info">
                <div class="dropdown-avatar">
                  <img v-if="user.avatar" :src="user.avatar" alt="Аватар" />
                  <div v-else class="default-avatar">
                    {{ userInitials }}
                  </div>
                </div>
                <div class="user-details">
                  <p class="user-name">{{ user.name }}</p>
                  <p class="user-email">{{ user.email }}</p>
                </div>
              </div>
              <hr class="dropdown-divider">
              <router-link to="/lk" class="dropdown-item" @click="closeMenu">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M13.5 14V12.5C13.5 11.837 13.2366 11.2011 12.7678 10.7322C12.2989 10.2634 11.663 10 11 10H5C4.33696 10 3.70107 10.2634 3.23223 10.7322C2.76339 11.2011 2.5 11.837 2.5 12.5V14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M8 7.5C9.38071 7.5 10.5 6.38071 10.5 5C10.5 3.61929 9.38071 2.5 8 2.5C6.61929 2.5 5.5 3.61929 5.5 5C5.5 6.38071 6.61929 7.5 8 7.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Личный кабинет
              </router-link>
              <button class="dropdown-item" @click="logout">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6 14H3.33333C2.97971 14 2.64057 13.8595 2.39052 13.6095C2.14048 13.3594 2 13.0203 2 12.6667V3.33333C2 2.97971 2.14048 2.64057 2.39052 2.39052C2.64057 2.14048 2.97971 2 3.33333 2H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M10.6667 11.3333L14 8L10.6667 4.66667" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M14 8H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Выйти
              </button>
            </div>
            
            <div v-else class="dropdown-section">
              <button class="dropdown-item guest-login-btn" @click="guestLogin">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M13.5 14V12.5C13.5 11.837 13.2366 11.2011 12.7678 10.7322C12.2989 10.2634 11.663 10 11 10H5C4.33696 10 3.70107 10.2634 3.23223 10.7322C2.76339 11.2011 2.5 11.837 2.5 12.5V14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M8 7.5C9.38071 7.5 10.5 6.38071 10.5 5C10.5 3.61929 9.38071 2.5 8 2.5C6.61929 2.5 5.5 3.61929 5.5 5C5.5 6.38071 6.61929 7.5 8 7.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Гостевой вход
                <span class="guest-badge">Тест</span>
              </button>
              <router-link to="/login" class="dropdown-item" @click="closeMenu">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M6 2H3.33333C2.97971 2 2.64057 2.14048 2.39052 2.39052C2.14048 2.64057 2 2.97971 2 3.33333V12.6667C2 13.0203 2.14048 13.3594 2.39052 13.6095C2.64057 13.8595 2.97971 14 3.33333 14H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M10.6667 11.3333L14 8L10.6667 4.66667" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M14 8H6" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Войти
              </router-link>
              <router-link to="/register" class="dropdown-item" @click="closeMenu">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <path d="M13.5 14V12.5C13.5 11.837 13.2366 11.2011 12.7678 10.7322C12.2989 10.2634 11.663 10 11 10H5C4.33696 10 3.70107 10.2634 3.23223 10.7322C2.76339 11.2011 2.5 11.837 2.5 12.5V14" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                  <path d="M8 7.5C9.38071 7.5 10.5 6.38071 10.5 5C10.5 3.61929 9.38071 2.5 8 2.5C6.61929 2.5 5.5 3.61929 5.5 5C5.5 6.38071 6.61929 7.5 8 7.5Z" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>
                </svg>
                Регистрация
              </router-link>
            </div>
          </div>
        </div>
      </nav>
      <footer class="sidebar-footer">
        <p>© 2025 Watermelon inc.</p>
      </footer>
    </aside>

    <!-- Контент справа -->
    <main class="main">
      <!-- Баннер гостевого режима -->
      <div v-if="isAuthenticated && isGuest" class="guest-banner">
        <div class="guest-banner-content">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M12 15.5C14.2091 15.5 16 13.7091 16 11.5C16 9.29086 14.2091 7.5 12 7.5C9.79086 7.5 8 9.29086 8 11.5C8 13.7091 9.79086 15.5 12 15.5Z" stroke="currentColor" stroke-width="2"/>
            <path d="M5 20.5C5 18.2909 6.79086 16.5 9 16.5H15C17.2091 16.5 19 18.2909 19 20.5" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            <circle cx="12" cy="12" r="10" stroke="currentColor" stroke-width="2"/>
          </svg>
          <span>Вы вошли как гость. Данные не сохраняются.</span>
          <button @click="logout" class="guest-banner-close">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <path d="M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
              <path d="M6 6L18 18" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>
      </div>
      <router-view />
    </main>

    <!-- Затемнение фона при открытом меню (для мобильных устройств) -->
    <div v-if="showProfileMenu" class="overlay" @click="closeMenu"></div>
  </div>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      showProfileMenu: false,
      isAuthenticated: false,
      isGuest: false,
      user: {
        name: "",
        email: "",
        avatar: null
      }
    };
  },
  computed: {
    userInitials() {
      if (!this.user.name) return "?";
      return this.user.name
        .split(" ")
        .map(word => word[0])
        .join("")
        .toUpperCase();
    }
  },
  methods: {
    toggleProfileMenu() {
      this.showProfileMenu = !this.showProfileMenu;
    },
    closeMenu() {
      this.showProfileMenu = false;
    },
    guestLogin() {
      this.isAuthenticated = true;
      this.isGuest = true;
      this.user = {
        name: "Гость",
        email: "guest@example.com",
        avatar: null
      };
      this.closeMenu();
      
      // Показываем уведомление о гостевом входе
      this.showGuestNotification();
    },
    logout() {
      this.isAuthenticated = false;
      this.isGuest = false;
      this.user = {
        name: "",
        email: "",
        avatar: null
      };
      this.closeMenu();
      this.$router.push('/');
    },
    checkAuth() {
      // Проверяем, есть ли данные гостя в localStorage
      const guestData = localStorage.getItem('guestUser');
      if (guestData) {
        const userData = JSON.parse(guestData);
        this.isAuthenticated = true;
        this.isGuest = true;
        this.user = userData;
      }
    },
    showGuestNotification() {
      // Сохраняем данные гостя в localStorage
      localStorage.setItem('guestUser', JSON.stringify(this.user));
      
      // Можно добавить toast-уведомление здесь
      console.log('Гостевой вход выполнен успешно!');
    }
  },
  mounted() {
    this.checkAuth();
  }
};
</script>

<style>
/* Базовые стили */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  color: #e2e8f0;
  min-height: 100vh;
  line-height: 1.6;
}

/* Основной контейнер */
.app {
  display: flex;
  min-height: 100vh;
  position: relative;
}

/* ===== Сайдбар с эффектом стекла ===== */
.sidebar {
  width: 280px;
  min-height: 100vh;
  backdrop-filter: blur(20px);
  border-right: 1px solid rgba(255, 255, 255, 0.1);
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  padding: 2.5rem 1.5rem;
  box-sizing: border-box;
  position: sticky;
  top: 0;
  z-index: 100;
}

/* Логотип с градиентом */
.logo {
  font-size: 1.8rem;
  font-weight: 800;
  text-align: center;
  margin-bottom: 2.5rem;
  background: linear-gradient(135deg, #818cf8 0%, #a78bfa 50%, #f472b6 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  text-shadow: 0 2px 10px rgba(129, 140, 248, 0.3);
  letter-spacing: -0.5px;
}

/* Навигация */
.nav {
  display: flex;
  flex-direction: column;
  gap: 0.8rem;
}

.nav-link {
  color: #cbd5e1;
  text-decoration: none;
  font-size: 1.1rem;
  font-weight: 500;
  padding: 1rem 1.2rem;
  border-radius: 12px;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  background: rgba(30, 41, 59, 0.4);
  border: 1px solid rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
}

.nav-link:hover {
  color: #fff;
  transform: translateX(6px);
  background: rgba(99, 102, 241, 0.2);
  border-color: rgba(99, 102, 241, 0.3);
}

.nav-link.active {
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  color: white;
  font-weight: 600;
  box-shadow: 0 8px 25px rgba(99, 102, 241, 0.3);
  border: none;
}

/* Контейнер профиля */
.profile-container {
  position: relative;
  margin-top: 1.5rem;
}

.profile-trigger {
  display: flex;
  align-items: center;
  padding: 1rem 1.2rem;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.3s ease;
  background: rgba(30, 41, 59, 0.4);
  color: #cbd5e1;
  border: 1px solid rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
}

.profile-trigger:hover {
  background: rgba(99, 102, 241, 0.2);
  color: #fff;
  border-color: rgba(99, 102, 241, 0.3);
}

.profile-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 12px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.profile-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.default-avatar {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  font-weight: 600;
}

.profile-name {
  flex: 1;
  font-size: 1.1rem;
  font-weight: 500;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.dropdown-arrow {
  transition: transform 0.3s ease;
  margin-left: 8px;
}

.dropdown-arrow.rotated {
  transform: rotate(180deg);
}

/* Выпадающее меню профиля */
.profile-dropdown {
  position: absolute;
  bottom: 100%;
  left: 0;
  right: 0;
  background: rgba(15, 23, 42, 0.95);
  backdrop-filter: blur(25px);
  border-radius: 16px;
  padding: 1.2rem;
  margin-bottom: 0.8rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
  z-index: 101;
  border: 1px solid rgba(255, 255, 255, 0.1);
}

.dropdown-section {
  display: flex;
  flex-direction: column;
  gap: 0.6rem;
}

.user-info {
  display: flex;
  align-items: center;
  margin-bottom: 0.8rem;
}

.dropdown-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  overflow: hidden;
  margin-right: 14px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
  color: white;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.3);
}

.dropdown-avatar img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.user-details {
  flex: 1;
}

.user-name {
  font-weight: 600;
  margin: 0;
  font-size: 1.1rem;
  color: #f8fafc;
}

.user-email {
  margin: 0;
  font-size: 0.9rem;
  color: #94a3b8;
  font-weight: 400;
}

.dropdown-divider {
  border: none;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(99, 102, 241, 0.3), transparent);
  margin: 0.8rem 0;
}

.dropdown-item {
  display: flex;
  align-items: center;
  padding: 0.9rem 1rem;
  border-radius: 10px;
  color: #e2e8f0;
  text-decoration: none;
  background: transparent;
  border: none;
  cursor: pointer;
  font-size: 1rem;
  font-weight: 500;
  transition: all 0.2s ease;
  text-align: left;
  position: relative;
}

.dropdown-item:hover {
  background: rgba(99, 102, 241, 0.15);
  color: #fff;
  transform: translateX(4px);
}

.dropdown-item svg {
  margin-right: 12px;
  opacity: 0.8;
}

/* Стили для кнопки гостевого входа */
.guest-login-btn {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
  border: 1px solid rgba(99, 102, 241, 0.3);
}

.guest-login-btn:hover {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.2) 0%, rgba(139, 92, 246, 0.2) 100%);
  border-color: rgba(99, 102, 241, 0.5);
}

.guest-badge {
  background: linear-gradient(135deg, #10b981 0%, #059669 100%);
  color: white;
  font-size: 0.7rem;
  font-weight: 600;
  padding: 2px 6px;
  border-radius: 6px;
  margin-left: auto;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

/* Баннер гостевого режима */
.guest-banner {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%);
  border: 1px solid rgba(99, 102, 241, 0.3);
  border-radius: 12px;
  padding: 1rem 1.5rem;
  margin-bottom: 2rem;
  backdrop-filter: blur(10px);
}

.guest-banner-content {
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #cbd5e1;
  font-size: 0.95rem;
}

.guest-banner-content svg {
  margin-right: 12px;
  opacity: 0.8;
  flex-shrink: 0;
}

.guest-banner-close {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s ease;
  flex-shrink: 0;
  margin-left: 12px;
}

.guest-banner-close:hover {
  background: rgba(99, 102, 241, 0.1);
  color: #e2e8f0;
}

/* Футер внутри сайдбара */
.sidebar-footer {
  text-align: center;
  font-size: 0.9rem;
  color: #94a3b8;
  margin-top: auto;
  padding-top: 2rem;
  opacity: 0.7;
}

/* ===== Контент ===== */
.main {
  flex: 1;
  padding: 3rem;
  overflow-y: auto;
}

/* Затемнение фона */
.overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  z-index: 99;
  display: none;
}

/* Адаптив */
@media (max-width: 968px) {
  .sidebar {
    width: 240px;
    padding: 2rem 1.2rem;
  }
  
  .main {
    padding: 2rem;
  }
}

@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    left: -280px;
    transition: left 0.3s ease;
    z-index: 100;
  }
  
  .sidebar.open {
    left: 0;
  }
  
  .main {
    padding: 1.5rem;
  }
  
  .overlay {
    display: block;
  }
  
  .logo {
    font-size: 1.6rem;
  }
  
  .nav-link {
    font-size: 1rem;
    padding: 0.9rem 1rem;
  }
  
  .guest-banner-content {
    flex-direction: column;
    align-items: flex-start;
    gap: 0.8rem;
  }
  
  .guest-banner-close {
    align-self: flex-end;
    margin-left: 0;
  }
}
</style>