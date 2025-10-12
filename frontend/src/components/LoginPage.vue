<template>
  <div class="login-page">
    <!-- Canvas для частиц -->

    <!-- Основной контент -->
    <main class="content">
      <div class="login-box">
        <h1 class="title">Вход</h1>
        <form @submit.prevent="handleLogin" class="login-form">
          <input
            v-model="username"
            type="text"
            placeholder="Имя пользователя"
            required
            class="input"
          />
          <input
            v-model="password"
            type="password"
            placeholder="Пароль"
            required
            class="input"
          />
          <button type="submit" class="login-button">Войти</button>
        </form>
        <p class="hint">
          Нет аккаунта? <router-link to="/register">Зарегистрируйтесь</router-link>
        </p>
      </div>
    </main>
  </div>
</template>

<script>
import api from '@/api/api';

export default {
  name: 'LoginPage',
  data() {
    return {
      username: '',
      password: '',
      animationFrame: null,
    };
  },
  mounted() {
    window.addEventListener('resize', this.handleResize);
  },
  beforeUnmount() {
    if (this.animationFrame) cancelAnimationFrame(this.animationFrame);
    window.removeEventListener('resize', this.handleResize);
  },
  methods: {
    async handleLogin() {
      try {
        const response = await api.login({
          username: this.username,
          password: this.password,
        });

        if (response.data?.access_token) {
          localStorage.setItem('token', response.data.access_token);
          this.$router.push('/lk');
        } else {
          alert('Ошибка: токен не получен');
        }
      } catch (error) {
        console.error('Ошибка при входе:', error);
        alert(
          'Ошибка при входе: ' +
            (error.response?.data?.detail || 'Неизвестная ошибка')
        );
      }
    },

    // particles (тот же стиль, что и в HomePage)
   
    resizeCanvas() {
      const canvas = this.$refs.particlesCanvas;
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
    },
    handleResize() {
      this.resizeCanvas();
      const canvas = this.$refs.particlesCanvas;
      this.createParticles(canvas);
    },
    createParticles(canvas) {
      this.particles = [];
      const colors = ['#805AD5', '#3182CE', '#00B5D8'];
      const particleCount = Math.min(
        50,
        Math.floor((window.innerWidth * window.innerHeight) / 20000)
      );

      for (let i = 0; i < particleCount; i++) {
        this.particles.push({
          x: Math.random() * canvas.width,
          y: Math.random() * canvas.height,
          size: Math.random() * 2 + 1,
          speedX: Math.random() * 1 - 0.5,
          speedY: Math.random() * 1 - 0.5,
          color: colors[Math.floor(Math.random() * colors.length)],
        });
      }
    },
    animateParticles(canvas, ctx) {
      const animate = () => {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        for (let i = 0; i < this.particles.length; i++) {
          const p = this.particles[i];
          p.x += p.speedX;
          p.y += p.speedY;
          if (p.x < 0 || p.x > canvas.width) p.speedX *= -1;
          if (p.y < 0 || p.y > canvas.height) p.speedY *= -1;

          ctx.beginPath();
          ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2);
          ctx.fillStyle = p.color;
          ctx.fill();

          for (let j = i + 1; j < this.particles.length; j++) {
            const p2 = this.particles[j];
            const dx = p.x - p2.x;
            const dy = p.y - p2.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < 100) {
              ctx.beginPath();
              ctx.strokeStyle = `rgba(128, 90, 213, ${1 - distance / 100})`;
              ctx.lineWidth = 0.5;
              ctx.moveTo(p.x, p.y);
              ctx.lineTo(p2.x, p2.y);
              ctx.stroke();
            }
          }
        }
        this.animationFrame = requestAnimationFrame(animate);
      };
      animate();
    },
  },
};
</script>

<style scoped>
.login-page {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #e2e8f0;
}

.particles-canvas {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  pointer-events: none;
}

.content {
  position: relative;
  z-index: 2;
  width: 100%;
  max-width: 400px;
  padding: 1rem;
  box-sizing: border-box;
}

.login-box {
  background: rgba(15, 23, 42, 0.85);
  backdrop-filter: blur(12px);
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
  text-align: center;
}

.title {
  font-size: 1.8rem;
  margin-bottom: 1.5rem;
  background: linear-gradient(135deg, #667eea, #805AD5);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #475569;
  border-radius: 10px;
  background: rgba(30, 41, 59, 0.7);
  color: white;
  font-size: 1rem;
  outline: none;
}

.input::placeholder {
  color: #94a3b8;
}

.login-button {
  width: 100%;
  padding: 0.75rem 1rem;
  margin-top: 0.5rem;
  background: linear-gradient(135deg, #805AD5 0%, #667eea 100%);
  border: none;
  border-radius: 10px;
  color: white;
  font-size: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.login-button:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 20px rgba(128, 90, 213, 0.4);
}

.hint {
  margin-top: 1.5rem;
  color: #94a3b8;
  font-size: 0.9rem;
}

.hint a {
  color: #805AD5;
  text-decoration: none;
}

.hint a:hover {
  text-decoration: underline;
}
</style>
