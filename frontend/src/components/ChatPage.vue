<template>
  <div class="chat-app">
    <!-- Main Chat Area -->
    <div class="main-content" :class="{ 'sidebar-hidden': !sidebarOpen }">
      <!-- Header -->
      <div class="chat-header">
        <button class="menu-btn" @click="toggleSidebar">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
            <path d="M4 6h16M4 12h16M4 18h16" stroke="currentColor" stroke-width="2"/>
          </svg>
        </button>
        
        <div class="chat-info">
          <h2>{{ currentChat.title }}</h2>
          <div class="chat-status">
            <span class="status-dot"></span>
            В сети
          </div>
        </div>
        
        <div class="header-actions">
          <button class="action-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" stroke="currentColor" stroke-width="2"/>
            </svg>
          </button>
          <button class="action-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M12 5v.01M12 12v.01M12 19v.01M12 6a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2zm0 7a1 1 0 110-2 1 1 0 010 2z" stroke="currentColor" stroke-width="2"/>
            </svg>
          </button>
        </div>
      </div>

      <!-- Messages -->
      <div class="messages-container" ref="messagesContainer">
        <transition-group name="message-fade" tag="div">
          <div
            v-for="(msg, index) in currentChat.messages"
            :key="`${msg.id}-${index}`"
            :class="['message', msg.sender]"
          >
            <div class="message-avatar">
              <div v-if="msg.sender === 'bot'" class="avatar bot">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm-1 15h-2v-6h2v6zm4 0h-2v-6h2v6zm-6-8c0-.55.45-1 1-1s1 .45 1 1-.45 1-1 1-1-.45-1-1zm8 0c0-.55.45-1 1-1s1 .45 1 1-.45 1-1 1-1-.45-1-1z"/>
                </svg>
              </div>
              <div v-else class="avatar user">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                  <path d="M12 12c2.21 0 4-1.79 4-4s-1.79-4-4-4-4 1.79-4 4 1.79 4 4 4zm0 2c-2.67 0-8 1.34-8 4v2h16v-2c0-2.66-5.33-4-8-4z"/>
                </svg>
              </div>
            </div>
            
            <div class="message-content">
              <div class="message-bubble">
                <p>{{ msg.text }}</p>
                <div class="message-time">{{ msg.time }}</div>
              </div>
            </div>
          </div>
        </transition-group>

        <!-- Typing Indicator -->
        <div v-if="typing" class="typing-indicator">
          <div class="typing-dots">
            <span></span>
            <span></span>
            <span></span>
          </div>
          <p>ИИ печатает...</p>
        </div>
      </div>

      <!-- Input Area -->
      <div class="input-area">
        <div class="input-container">
          <div class="input-actions">
            <button class="input-action">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M14.828 14.828a4 4 0 01-5.656 0M9 10h.01M15 10h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" stroke="currentColor" stroke-width="2"/>
              </svg>
            </button>
            <button class="input-action">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
                <path d="M15.172 7l-6.586 6.586a2 2 0 102.828 2.828l6.414-6.586a4 4 0 00-5.656-5.656l-6.415 6.585a6 6 0 108.486 8.486L20.5 13" stroke="currentColor" stroke-width="2"/>
              </svg>
            </button>
          </div>
          
          <input
            v-model="newMessage"
            type="text"
            placeholder="Введите ваше сообщение..."
            class="message-input"
            @keypress.enter="sendMessage"
          />
          
          <button class="send-btn" @click="sendMessage" :disabled="!newMessage.trim()">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
              <path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/>
            </svg>
          </button>
        </div>
      </div>
    </div>

    <!-- Sidebar (справа) -->
    <transition name="sidebar-slide">
      <div class="sidebar right-sidebar" v-if="sidebarOpen">
        <div class="sidebar-header">
          <h2>💬 Мои чаты</h2>
          <button class="close-btn" @click="toggleSidebar">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2"/>
            </svg>
          </button>
        </div>
        
        <div class="chats-list">
          <div
            v-for="chat in chats"
            :key="chat.id"
            :class="['chat-item', { active: chat.id === activeChatId }]"
            @click="setActiveChat(chat.id)"
          >
            <div class="chat-icon">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="currentColor">
                <path d="M20 2H4c-1.1 0-1.99.9-1.99 2L2 22l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2zM6 9h12v2H6V9zm8 5H6v-2h8v2zm4-6H6V6h12v2z"/>
              </svg>
            </div>
            <div class="chat-info">
              <div class="chat-title">{{ chat.title }}</div>
              <div class="chat-preview">{{ getLastMessage(chat) }}</div>
            </div>
            <div class="chat-time">{{ getLastMessageTime(chat) }}</div>
          </div>
        </div>
        
        <button class="new-chat-btn" @click="createChat">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none">
            <path d="M12 5v14M5 12h14" stroke="currentColor" stroke-width="2"/>
          </svg>
          Новый чат
        </button>
      </div>
    </transition>
    
    <!-- Overlay for mobile -->
    <transition name="fade">
      <div v-if="sidebarOpen && isMobile" class="sidebar-overlay" @click="toggleSidebar"></div>
    </transition>
  </div>
</template>

<script>
import { ref, computed, onMounted, onUnmounted, nextTick } from 'vue'

export default {
  name: "ChatApp",
  setup() {
    const newMessage = ref("")
    const activeChatId = ref(1)
    const typing = ref(false)
    const sidebarOpen = ref(true)
    const messagesContainer = ref(null)
    const isMobile = ref(false)
    
    // Generate unique IDs for messages
    let messageIdCounter = 1000
    
    const chats = ref([
      {
        id: 1,
        title: "Общий чат",
        messages: [
          { 
            id: 1, 
            sender: "bot", 
            text: "Привет! Я ваш ИИ-помощник. Чем могу помочь сегодня?", 
            time: formatTime(new Date()) 
          },
        ],
      },
    ])
    
    const nextChatId = ref(4)
    
    const currentChat = computed(() => {
      return chats.value.find(c => c.id === activeChatId.value) || chats.value[0]
    })
    
    function sendMessage() {
      const text = newMessage.value.trim()
      if (!text) return
      
      const newMsg = {
        id: messageIdCounter++,
        sender: "user",
        text,
        time: formatTime(new Date())
      }
      
      currentChat.value.messages.push(newMsg)
      newMessage.value = ""
      scrollToBottom()
      
      typing.value = true
      setTimeout(() => {
        typing.value = false
        const responses = [
          "Это интересно! Расскажите подробнее.",
          "Понятно. Чем еще могу вам помочь?",
          "Отличная мысль! Что бы вы хотели сделать дальше?",
          "Ясно. Дайте знать, если нужно что-то уточнить.",
          "Спасибо, что поделились! Хотите обсудить что-то еще?"
        ]
        
        const botMsg = {
          id: messageIdCounter++,
          sender: "bot",
          text: responses[Math.floor(Math.random() * responses.length)],
          time: formatTime(new Date())
        }
        
        currentChat.value.messages.push(botMsg)
        scrollToBottom()
      }, 2000)
    }
    
    function scrollToBottom() {
      nextTick(() => {
        if (messagesContainer.value) {
          messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
        }
      })
    }
    
    function toggleSidebar() {
      sidebarOpen.value = !sidebarOpen.value
    }
    
    function setActiveChat(id) {
      activeChatId.value = id
      if (isMobile.value) {
        sidebarOpen.value = false
      }
      scrollToBottom()
    }
    
    function createChat() {
      const newChat = {
        id: nextChatId.value++,
        title: `Чат ${nextChatId.value - 1}`,
        messages: [
          { 
            id: messageIdCounter++,
            sender: "bot", 
            text: "Привет! Я ваш новый ИИ-помощник. Чем могу помочь сегодня?", 
            time: formatTime(new Date())
          },
        ],
      }
      chats.value.push(newChat)
      activeChatId.value = newChat.id
      scrollToBottom()
    }
    
    function getLastMessage(chat) {
      const lastMsg = chat.messages[chat.messages.length - 1]
      return lastMsg ? lastMsg.text : "Пока нет сообщений"
    }
    
    function getLastMessageTime(chat) {
      const lastMsg = chat.messages[chat.messages.length - 1]
      if (!lastMsg) return ""
      
      const msgTime = new Date()
      return formatTimeShort(msgTime)
    }
    
    function formatTime(date) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
    
    function formatTimeShort(date) {
      return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
    }
    
    function checkMobile() {
      isMobile.value = window.innerWidth < 768
      if (isMobile.value) {
        sidebarOpen.value = false
      }
    }
    
    onMounted(() => {
      checkMobile()
      window.addEventListener('resize', checkMobile)
      scrollToBottom()
    })
    
    onUnmounted(() => {
      window.removeEventListener('resize', checkMobile)
    })
    
    return {
      newMessage,
      chats,
      activeChatId,
      typing,
      sidebarOpen,
      messagesContainer,
      isMobile,
      currentChat,
      sendMessage,
      toggleSidebar,
      setActiveChat,
      createChat,
      getLastMessage,
      getLastMessageTime
    }
  }
}

</script>

<style scoped>
.chat-app {
  display: flex;
  height: 100vh;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
  position: relative;
  overflow: hidden;
  background: rgba(0, 0, 0, 0.3); /* Добавляем легкий фон для всего приложения */
}


/* Sidebar справа */
.sidebar {
  width: 320px;
  background: rgba(15, 23, 42, 0.25) !important; /* Увеличиваем прозрачность */
  backdrop-filter: blur(25px); /* Усиливаем размытие */
  border-left: 1px solid rgba(255, 255, 255, 0.08); /* Делаем границу более прозрачной */
  display: flex;
  flex-direction: column;
  padding: 20px;
  color: #e2e8f0;
  z-index: 100;
  position: relative;
}

.right-sidebar {
  order: 2;
}

.sidebar-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.sidebar-header h2 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #e2e8f0;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
}

.chats-list {
  flex: 1;
  overflow-y: auto;
  margin-bottom: 20px;
}

.chats-list::-webkit-scrollbar {
  width: 4px;
}

.chats-list::-webkit-scrollbar-track {
  border-radius: 10px;
}

.chats-list::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
}

.chat-item {
  display: flex;
  align-items: center;
  padding: 15px;
  border-radius: 15px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.3s ease;
  border: 1px solid rgba(255, 255, 255, 0.05);
}

.chat-item:hover {
  background: rgba(51, 65, 85, 0.4) !important; /* Более прозрачный */
  transform: translateX(-5px);
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
}

.chat-item.active {
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8)) !important;
  color: white;
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.3);
}


.chat-icon {
  width: 40px;
  height: 40px;
  border-radius: 10px;
  background: rgba(99, 102, 241, 0.1);
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
  color: #6366f1;
}

.chat-item.active .chat-icon {
  background: rgba(255, 255, 255, 0.2);
  color: white;
}

.chat-info {
  flex: 1;
  min-width: 0;
}

.chat-title {
  font-weight: 600;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-preview {
  font-size: 0.85rem;
  opacity: 0.7;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.chat-time {
  font-size: 0.8rem;
  opacity: 0.6;
  white-space: nowrap;
}

.new-chat-btn {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 15px;
  background: linear-gradient(135deg, rgba(99, 102, 241, 0.8), rgba(139, 92, 246, 0.8)) !important;
  color: white;
  border: none;
  border-radius: 15px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.25);
}

.new-chat-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(99, 102, 241, 0.4);
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: rgba(15, 23, 42, 0.2) !important; /* Увеличиваем прозрачность */
  backdrop-filter: blur(25px); /* Усиливаем размытие */
  transition: all 0.3s ease;
  order: 1;
  position: relative;
  z-index: 1;
}

.main-content.sidebar-hidden {
  margin-right: 0;
}

.chat-header {
  display: flex;
  align-items: center;
  padding: 20px 30px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.08); /* Более прозрачная граница */
  background: rgba(15, 23, 42, 0.15) !important; /* Полупрозрачный фон */
  backdrop-filter: blur(25px);
  color: #e2e8f0;
}

.menu-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 10px;
  border-radius: 10px;
  margin-right: 20px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.menu-btn:hover {
  background: rgba(255, 255, 255, 0.1);
}

.chat-info {
  flex: 1;
}

.chat-info h2 {
  font-size: 1.3rem;
  font-weight: 700;
  color: #e2e8f0;
  margin-bottom: 4px;
  margin: 0;
}

.chat-status {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
  color: #4ade80;
}

.status-dot {
  width: 8px;
  height: 8px;
  background: #4ade80;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.5; }
  100% { opacity: 1; }
}

.header-actions {
  display: flex;
  gap: 10px;
}

.action-btn {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 10px;
  border-radius: 10px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.action-btn:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
}

/* Messages */
.messages-container {
  flex: 1;
  padding: 30px;
  overflow-y: auto;
  scroll-behavior: smooth;
}

.messages-container::-webkit-scrollbar {
  width: 6px;
}

.messages-container::-webkit-scrollbar-track {
  border-radius: 10px;
}

.messages-container::-webkit-scrollbar-thumb {
  background: rgba(255, 255, 255, 0.2);
  border-radius: 10px;
}

.message {
  display: flex;
  margin-bottom: 25px;
  animation: messageSlide 0.3s ease-out;
}

@keyframes messageSlide {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.message.user {
  flex-direction: row-reverse;
}

.message-avatar {
  margin: 0 15px;
}

.avatar {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 700;
  font-size: 0.8rem;
}

.avatar.bot {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
}

.avatar.user {
  background: linear-gradient(135deg, #4ade80, #22c55e);
  color: white;
}

.message-content {
  max-width: 60%;
}

.message-bubble {
  padding: 15px 20px;
  border-radius: 20px;
  position: relative;
}

.message.user .message-bubble {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  color: white;
  border-bottom-right-radius: 5px;
}

.message.bot .message-bubble {
  background: rgba(30, 41, 59, 0.4) !important; /* Более прозрачный */
  color: #e2e8f0;
  border-bottom-left-radius: 5px;
  border: 1px solid rgba(255, 255, 255, 0.08); /* Более прозрачная граница */
}

.message-time {
  font-size: 0.75rem;
  opacity: 0.7;
  margin-top: 8px;
  text-align: right;
}

.message.bot .message-time {
  text-align: left;
}

/* Typing Indicator */
.typing-indicator {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 20px;
  background: rgba(30, 41, 59, 0.4) !important; /* Более прозрачный */
  border-radius: 20px;
  margin: 20px 0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.15);
  animation: slideIn 0.3s ease;
  color: #e2e8f0;
  max-width: 200px;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.typing-dots {
  display: flex;
  gap: 4px;
}

.typing-dots span {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #6366f1;
  animation: typing 1.4s infinite ease-in-out;
}

.typing-dots span:nth-child(1) { animation-delay: -0.32s; }
.typing-dots span:nth-child(2) { animation-delay: -0.16s; }

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

/* Input Area */
.input-area {
  padding: 20px 30px;
  background: rgba(15, 23, 42, 0.2) !important; /* Более прозрачный */
  border-top: 1px solid rgba(255, 255, 255, 0.08);
  backdrop-filter: blur(25px);
}

.input-container {
  display: flex;
  align-items: center;
  background: rgba(30, 41, 59, 0.4) !important; /* Увеличиваем прозрачность */
  border-radius: 25px;
  padding: 5px 20px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  border: 1px solid rgba(255, 255, 255, 0.08); /* Более прозрачная граница */
  transition: all 0.3s ease;
}

.input-container:focus-within {
  border-color: rgba(99, 102, 241, 0.5);
  box-shadow: 0 4px 20px rgba(99, 102, 241, 0.2);
}

.input-actions {
  display: flex;
  gap: 10px;
  margin-right: 15px;
}

.input-action {
  background: none;
  border: none;
  color: #94a3b8;
  cursor: pointer;
  padding: 8px;
  border-radius: 8px;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
}

.input-action:hover {
  background: rgba(255, 255, 255, 0.1);
  color: #e2e8f0;
}

.message-input {
  flex: 1;
  border: none;
  outline: none;
  padding: 15px 0;
  font-size: 1rem;
  background: transparent;
  color: #e2e8f0;
}

.message-input::placeholder {
  color: #94a3b8;
}

.send-btn {
  background: linear-gradient(135deg, #6366f1, #8b5cf6);
  border: none;
  border-radius: 50%;
  width: 45px;
  height: 45px;
  cursor: pointer;
  color: white;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 4px 15px rgba(99, 102, 241, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

/* Overlay for mobile */
.sidebar-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(5px);
  z-index: 99;
}

/* Transitions */
.sidebar-slide-enter-active,
.sidebar-slide-leave-active {
  transition: all 0.3s ease;
}

.sidebar-slide-enter-from,
.sidebar-slide-leave-to {
  transform: translateX(100%);
  opacity: 0;
}

.message-fade-enter-active {
  transition: all 0.3s ease;
}

.message-fade-enter-from {
  opacity: 0;
  transform: translateY(20px);
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

/* Responsive */
@media (max-width: 768px) {
  .sidebar {
    position: fixed;
    right: 0;
    top: 0;
    bottom: 0;
    z-index: 100;
    width: 85%;
    max-width: 320px;
  }
  
  .message-content {
    max-width: 80%;
  }
  
  .chat-header {
    padding: 15px 20px;
  }
  
  .messages-container {
    padding: 20px;
  }
  
  .input-area {
    padding: 15px 20px;
  }
  
  .avatar {
    width: 36px;
    height: 36px;
  }
  
  .message-bubble {
    padding: 12px 16px;
  }
}
</style>