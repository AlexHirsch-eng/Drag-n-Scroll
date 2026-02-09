<template>
  <div class="ai-chat-view">
    <!-- Back Button -->
    <div class="back-section">
      <button @click="goBack" class="back-btn">
        <span class="icon">←</span>
        <span>НАЗАД ДОМОЙ</span>
      </button>
    </div>

    <!-- AI Chat Container -->
    <div class="chat-wrapper">
      <!-- No Access Message -->
      <div v-if="!hasAccess" class="no-access-container">
        <div class="no-access-card">
          <div class="lock-icon">🔒</div>
          <h2 class="no-access-title">Требуется доступ к ИИ чату</h2>
          <p class="no-access-description">
            Вам нужно приобрести доступ для использования ИИ чат-бота. Практикуйте разговоры на китайском с нашим ИИ помощником!
          </p>

          <div class="features-list">
            <div class="feature-item">
              <span class="feature-icon">💬</span>
              <span>Неограниченные разговоры на китайском</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">🎯</span>
              <span>Практикуйте произношение и грамматику</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">📚</span>
              <span>Изучайте слова в контексте</span>
            </div>
            <div class="feature-item">
              <span class="feature-icon">⚡</span>
              <span>Мгновенные ответы ИИ 24/7</span>
            </div>
          </div>

          <div class="pricing-preview">
            <h3>Выберите свой план</h3>
            <div class="pricing-options">
              <div class="price-option">
                <div class="price-duration">1 День</div>
                <div class="price-amount">50 <img src="/src/images/coin.png" alt="coin" class="inline-coin"></div>
              </div>
              <div class="price-option popular">
                <div class="badge">ПОПУЛЯРНЫЙ</div>
                <div class="price-duration">7 Дней</div>
                <div class="price-amount">250 <img src="/src/images/coin.png" alt="coin" class="inline-coin"></div>
              </div>
              <div class="price-option">
                <div class="price-duration">30 Дней</div>
                <div class="price-amount">800 <img src="/src/images/coin.png" alt="coin" class="inline-coin"></div>
              </div>
            </div>
          </div>

          <button @click="goToShop" class="go-to-shop-btn">
            <span class="btn-icon">🛒</span>
            <span>Перейти в магазин</span>
          </button>
        </div>
      </div>

      <!-- Chat Container (only shown when has access) -->
      <div v-else class="chat-container">
        <!-- Chat Header -->
        <div class="chat-header">
          <div class="ai-avatar">
            <img src="/src/images/ai.png" alt="AI" class="ai-avatar-img">
          </div>
          <div class="header-info">
            <h1 class="chat-title">AI 中文助手</h1>
            <p class="chat-subtitle">Практикуйте китайский с ИИ помощником</p>
            <p v-if="accessDaysLeft > 0" class="access-info">
              ✅ Доступ: {{ accessDaysLeft }} {{ accessDaysLeft === 1 ? 'день' : accessDaysLeft < 5 ? 'дня' : 'дней' }} осталось
              (Истекает: {{ accessEndDate?.toLocaleDateString() }})
            </p>
          </div>
          <button @click="clearChat" class="clear-btn" title="Очистить чат">
            <span>🗑️</span>
          </button>
        </div>

        <!-- Messages Area -->
        <div class="messages-area" ref="messagesContainer">
          <div v-if="messages.length === 0" class="welcome-message">
            <div class="welcome-icon">👋</div>
            <h2>你好！</h2>
            <p>Я ваш ИИ помощник по изучению китайского. Давайте практиковать китайский вместе!</p>
            <div class="suggestions">
              <button @click="sendSuggestion('你好，请问你叫什么名字？')" class="suggestion-btn">
                你好，请问你叫什么名字？
              </button>
              <button @click="sendSuggestion('今天天气怎么样？')" class="suggestion-btn">
                今天天气怎么样？
              </button>
              <button @click="sendSuggestion('你能教我一些中文吗？')" class="suggestion-btn">
                你能教我一些中文吗？
              </button>
              <button @click="sendSuggestion('我想学中文')" class="suggestion-btn">
                我想学中文
              </button>
            </div>
          </div>

          <div v-for="(message, index) in messages" :key="index" :class="['message', message.role]">
            <div v-if="message.role === 'assistant'" class="message-avatar ai">
              <img src="/src/images/ai.png" alt="AI" class="ai-message-avatar">
            </div>
            <div class="message-content">
              <div class="message-text">{{ message.content }}</div>
              <div class="message-time">{{ formatTime(message.timestamp) }}</div>
            </div>
            <div v-if="message.role === 'user'" class="message-avatar user">👤</div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="isTyping" class="message assistant typing">
            <div class="message-avatar ai">
              <img src="/src/images/ai.png" alt="AI" class="ai-message-avatar">
            </div>
            <div class="message-content">
              <div class="typing-indicator">
                <span></span>
                <span></span>
                <span></span>
              </div>
            </div>
          </div>
        </div>

        <!-- Input Area -->
        <div class="input-area">
          <form @submit.prevent="sendMessage" class="message-form">
            <input
              v-model="userMessage"
              type="text"
              class="message-input"
              placeholder="用中文和我聊天... (Общайтесь со мной на китайском)"
              :disabled="isTyping"
              @keyup.enter="sendMessage"
            >
            <button
              type="submit"
              class="send-btn"
              :disabled="isTyping || !userMessage.trim()"
              title="Отправить сообщение"
            >
              <span v-if="!isTyping">📤</span>
              <span v-else>⏳</span>
            </button>
          </form>
          <div class="input-hint">
            💡 Совет: Пытайтесь общаться на китайском для практики!
          </div>
        </div>
      </div>

      <!-- Info Panel -->
      <div class="info-panel">
        <h3>🎯 练习建议 (Practice Tips)</h3>
        <ul>
          <li>尽量用中文聊天 (Try to chat in Chinese)</li>
          <li>不要怕犯错误 (Don't be afraid of mistakes)</li>
          <li>问关于日常生活的问题 (Ask about daily life)</li>
          <li>请求纠正语法 (Ask for grammar corrections)</li>
        </ul>

        <div class="common-phrases">
          <h4>📚 常用短语 (Common Phrases)</h4>
          <div class="phrase-list">
            <button @click="sendSuggestion('你好')" class="phrase-btn">你好 - Hello</button>
            <button @click="sendSuggestion('谢谢')" class="phrase-btn">谢谢 - Thank you</button>
            <button @click="sendSuggestion('再见')" class="phrase-btn">再见 - Goodbye</button>
            <button @click="sendSuggestion('早上好')" class="phrase-btn">早上好 - Good morning</button>
            <button @click="sendSuggestion('晚安')" class="phrase-btn">晚安 - Good night</button>
            <button @click="sendSuggestion('对不起')" class="phrase-btn">对不起 - Sorry</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, nextTick, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { chatAPI } from '@/api/chat'

const router = useRouter()
const authStore = useAuthStore()

interface Message {
  role: 'user' | 'assistant'
  content: string
  timestamp: Date
}

const messages = ref<Message[]>([])
const userMessage = ref('')
const isTyping = ref(false)
const messagesContainer = ref<HTMLElement | null>(null)
const error = ref<string | null>(null)

// Check AI access
const hasAccess = computed(() => authStore.hasAIAccess)
const accessDaysLeft = computed(() => authStore.aiAccessDaysLeft)
const accessEndDate = computed(() => {
  if (!authStore.aiAccessUntil) return null
  return new Date(authStore.aiAccessUntil)
})

// Load chat history from localStorage
onMounted(() => {
  const saved = localStorage.getItem('aiChatHistory')
  if (saved) {
    try {
      const parsed = JSON.parse(saved)
      messages.value = parsed.map((m: any) => ({
        ...m,
        timestamp: new Date(m.timestamp)
      }))
      scrollToBottom()
    } catch (e) {
      console.error('Failed to load chat history:', e)
    }
  }
})

function scrollToBottom() {
  nextTick(() => {
    if (messagesContainer.value) {
      messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight
    }
  })
}

function formatTime(date: Date): string {
  const now = new Date()
  const diff = now.getTime() - new Date(date).getTime()
  const minutes = Math.floor(diff / 60000)

  if (minutes < 1) return 'Только что'
  if (minutes < 60) return `${minutes}м назад`
  const hours = Math.floor(minutes / 60)
  if (hours < 24) return `${hours}ч назад`
  const days = Math.floor(hours / 24)
  return `${days}д назад`
}

function saveChatHistory() {
  localStorage.setItem('aiChatHistory', JSON.stringify(messages.value))
}

async function sendMessage() {
  const messageText = userMessage.value.trim()
  if (!messageText || isTyping.value) return

  // Clear previous errors
  error.value = null

  // Add user message
  messages.value.push({
    role: 'user',
    content: messageText,
    timestamp: new Date()
  })

  userMessage.value = ''
  saveChatHistory()
  scrollToBottom()

  // Show typing indicator
  isTyping.value = true

  try {
    // Build conversation history for API
    const history: any[] = messages.value
      .slice(-10) // Keep last 10 messages for context
      .map(msg => ({
        role: msg.role,
        content: msg.content
      }))

    // Call real AI API
    const data = await chatAPI.sendAIMessage(messageText, history)

    // Remove typing indicator
    isTyping.value = false

    // Add AI response
    messages.value.push({
      role: 'assistant',
      content: data.message,
      timestamp: new Date()
    })

    saveChatHistory()
    scrollToBottom()
  } catch (err: any) {
    isTyping.value = false
    error.value = err.message || 'Failed to get AI response'
    console.error('AI chat error:', err)

    // Show error message
    messages.value.push({
      role: 'assistant',
      content: `❌ Error: ${error.value}`,
      timestamp: new Date()
    })

    saveChatHistory()
    scrollToBottom()
  }
}

function sendSuggestion(text: string) {
  userMessage.value = text
  sendMessage()
}

function clearChat() {
  if (confirm('Вы уверены, что хотите очистить историю чата?')) {
    messages.value = []
    localStorage.removeItem('aiChatHistory')
  }
}

function goBack() {
  router.push('/')
}

function goToShop() {
  router.push('/shop')
}
</script>

<style scoped>
.ai-chat-view {
  min-height: 100vh;
  background: var(--color-bg-primary);
  padding: 1rem;
  position: relative;
}

.back-section {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.back-btn {
  background: rgba(37, 29, 45, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 245, 255, 0.15);
  border-radius: var(--radius-lg);
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.back-btn:hover {
  transform: translateY(-2px);
  background: rgba(0, 245, 255, 0.15);
  border-color: var(--color-neon-cyan);
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
}

.chat-wrapper {
  display: grid;
  grid-template-columns: 1fr 300px;
  gap: 1rem;
  max-width: 1400px;
  margin: 0 auto;
  height: calc(100vh - 80px);
}

.chat-container {
  background: var(--color-bg-card);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-2xl);
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.chat-header {
  background: rgba(0, 245, 255, 0.05);
  border-bottom: 1px solid var(--color-border-primary);
  padding: 1rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.ai-avatar {
  width: 75px;
  height: 75px;
  display: flex;
  align-items: center;
  justify-content: center;
  animation: float 3s ease-in-out infinite;
}

.ai-avatar-img {
  width: 100%;
  height: 100%;
  object-fit: contain;
  filter: drop-shadow(0 0 15px rgba(0, 245, 255, 0.5));
}

@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}

.header-info {
  flex: 1;
}

.chat-title {
  font-size: 1.2rem;
  font-weight: 900;
  margin: 0;
  background: var(--gradient-neon-cyan);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.chat-subtitle {
  font-size: 0.8rem;
  color: var(--color-text-muted);
  margin: 0;
}

.clear-btn {
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-radius: var(--radius-md);
  padding: 0.5rem 0.75rem;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1.2rem;
}

.clear-btn:hover {
  background: rgba(255, 107, 53, 0.2);
  border-color: var(--color-accent-primary);
  transform: scale(1.1);
}

.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.messages-area::-webkit-scrollbar {
  width: 6px;
}

.messages-area::-webkit-scrollbar-track {
  background: var(--color-bg-elevated);
}

.messages-area::-webkit-scrollbar-thumb {
  background: var(--color-neon-cyan);
  border-radius: 3px;
}

.welcome-message {
  text-align: center;
  padding: 2rem;
  color: var(--color-text-secondary);
}

.welcome-icon {
  font-size: 4rem;
  margin-bottom: 1rem;
}

.welcome-message h2 {
  font-size: 2rem;
  margin: 0 0 0.5rem 0;
  color: var(--color-neon-cyan);
}

.welcome-message p {
  margin: 0 0 2rem 0;
  font-size: 1rem;
}

.suggestions {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  max-width: 500px;
  margin: 0 auto;
}

.suggestion-btn {
  background: rgba(0, 245, 255, 0.1);
  border: 1px solid var(--color-neon-cyan);
  border-radius: var(--radius-lg);
  padding: 1rem;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  text-align: left;
}

.suggestion-btn:hover {
  background: rgba(0, 245, 255, 0.2);
  transform: translateX(5px);
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
}

.message {
  display: flex;
  gap: 0.75rem;
  max-width: 80%;
  animation: slideIn 0.3s ease-out;
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

.message.user {
  flex-direction: row-reverse;
  margin-left: auto;
}

.message-content {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.message-text {
  padding: 1rem;
  border-radius: var(--radius-lg);
  line-height: 1.6;
  white-space: pre-wrap;
  word-wrap: break-word;
}

.message.assistant .message-text {
  background: rgba(0, 245, 255, 0.1);
  border: 1px solid rgba(0, 245, 255, 0.3);
  border-top-left-radius: 0;
}

.message.user .message-text {
  background: rgba(255, 107, 53, 0.15);
  border: 1px solid rgba(255, 107, 53, 0.3);
  border-top-right-radius: 0;
}

.message-time {
  font-size: 0.7rem;
  color: var(--color-text-muted);
  padding: 0 0.25rem;
}

.message.assistant .message-time {
  text-align: left;
}

.message.user .message-time {
  text-align: right;
}

.message-avatar {
  width: 60px;
  height: 60px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  flex-shrink: 0;
}

.message-avatar.ai {
  background: linear-gradient(135deg, rgba(0, 245, 255, 0.2), rgba(180, 0, 255, 0.2));
  border: 2px solid var(--color-neon-cyan);
  padding: 0;
  overflow: hidden;
}

.ai-message-avatar {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.message-avatar.user {
  background: linear-gradient(135deg, rgba(255, 107, 53, 0.2), rgba(255, 60, 120, 0.2));
  border: 2px solid var(--color-accent-primary);
}

.typing-indicator {
  display: flex;
  gap: 0.5rem;
  padding: 1rem;
  background: rgba(0, 245, 255, 0.1);
  border: 1px solid rgba(0, 245, 255, 0.3);
  border-radius: var(--radius-lg);
  border-top-left-radius: 0;
}

.typing-indicator span {
  width: 8px;
  height: 8px;
  background: var(--color-neon-cyan);
  border-radius: 50%;
  animation: typingBounce 1.4s infinite ease-in-out both;
}

.typing-indicator span:nth-child(1) { animation-delay: -0.32s; }
.typing-indicator span:nth-child(2) { animation-delay: -0.16s; }
.typing-indicator span:nth-child(3) { animation-delay: 0s; }

@keyframes typingBounce {
  0%, 80%, 100% {
    transform: scale(0.8);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}

.input-area {
  padding: 1rem 1.5rem;
  border-top: 1px solid var(--color-border-primary);
  background: rgba(0, 0, 0, 0.2);
}

.message-form {
  display: flex;
  gap: 0.75rem;
}

.message-input {
  flex: 1;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  padding: 0.75rem 1rem;
  color: var(--color-text-primary);
  font-size: 1rem;
  transition: all 0.3s;
}

.message-input:focus {
  outline: none;
  border-color: var(--color-neon-cyan);
  box-shadow: 0 0 10px rgba(0, 245, 255, 0.2);
}

.message-input:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.send-btn {
  background: var(--gradient-cyan);
  border: none;
  border-radius: var(--radius-lg);
  padding: 0.75rem 1.25rem;
  font-size: 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  justify-content: center;
}

.send-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.4);
}

.send-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.input-hint {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  text-align: center;
  margin-top: 0.5rem;
}

.info-panel {
  background: var(--color-bg-card);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-2xl);
  padding: 1.5rem;
  overflow-y: auto;
}

.info-panel h3 {
  font-size: 1.1rem;
  margin: 0 0 1rem 0;
  color: var(--color-neon-pink);
}

.info-panel h4 {
  font-size: 1rem;
  margin: 1.5rem 0 0.75rem 0;
  color: var(--color-neon-yellow);
}

.info-panel ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.info-panel li {
  padding: 0.5rem 0;
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  border-bottom: 1px solid var(--color-border-primary);
}

.info-panel li:last-child {
  border-bottom: none;
}

.common-phrases {
  margin-top: 1rem;
}

.phrase-list {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.phrase-btn {
  background: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: var(--radius-md);
  padding: 0.75rem;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.85rem;
  text-align: left;
}

.phrase-btn:hover {
  background: rgba(255, 193, 7, 0.2);
  border-color: var(--color-neon-yellow);
  transform: translateX(3px);
}

@media (max-width: 1024px) {
  .chat-wrapper {
    grid-template-columns: 1fr;
    grid-template-rows: 1fr auto;
  }

  .info-panel {
    display: none;
  }
}

@media (max-width: 768px) {
  .chat-wrapper {
    height: calc(100vh - 60px);
  }

  .message {
    max-width: 90%;
  }

  .suggestions {
    max-width: 100%;
  }
}

/* No Access Styles */
.no-access-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: calc(100vh - 80px);
  padding: 2rem;
}

.no-access-card {
  background: var(--color-bg-card);
  border: 2px solid var(--color-neon-cyan);
  border-radius: var(--radius-2xl);
  padding: 3rem;
  max-width: 600px;
  width: 100%;
  text-align: center;
  box-shadow: 0 0 50px rgba(0, 245, 255, 0.2);
  animation: slideIn 0.5s ease-out;
}

.lock-icon {
  font-size: 5rem;
  margin-bottom: 1.5rem;
  animation: lockPulse 2s ease-in-out infinite;
}

@keyframes lockPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.1);
  }
}

.no-access-title {
  font-size: 2rem;
  font-weight: 900;
  margin: 0 0 1rem 0;
  background: var(--gradient-neon-rainbow);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.no-access-description {
  font-size: 1.1rem;
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0 0 2rem 0;
}

.features-list {
  display: grid;
  gap: 1rem;
  margin-bottom: 2rem;
}

.feature-item {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  padding: 1rem;
  background: rgba(0, 245, 255, 0.05);
  border: 1px solid rgba(0, 245, 255, 0.2);
  border-radius: var(--radius-lg);
  color: var(--color-text-primary);
  font-size: 1rem;
}

.feature-icon {
  font-size: 1.5rem;
}

.pricing-preview {
  margin-bottom: 2rem;
}

.pricing-preview h3 {
  font-size: 1.3rem;
  color: var(--color-neon-cyan);
  margin: 0 0 1rem 0;
}

.pricing-options {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.price-option {
  position: relative;
  background: rgba(0, 0, 0, 0.3);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  padding: 1rem;
  transition: all 0.3s;
}

.price-option:hover {
  transform: translateY(-5px);
  border-color: var(--color-neon-cyan);
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
}

.price-option.popular {
  border-color: var(--color-accent-primary);
  background: rgba(255, 107, 53, 0.1);
}

.price-option.popular:hover {
  border-color: var(--color-accent-primary);
  box-shadow: 0 0 20px rgba(255, 107, 53, 0.4);
}

.price-option .badge {
  position: absolute;
  top: -10px;
  left: 50%;
  transform: translateX(-50%);
  background: var(--gradient-pink);
  color: white;
  font-size: 0.65rem;
  font-weight: 900;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-full);
  letter-spacing: 1px;
}

.price-duration {
  font-size: 0.9rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.price-amount {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.25rem;
  font-size: 1.2rem;
  font-weight: 900;
  color: #FFD700;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.inline-coin {
  width: 20px;
  height: 20px;
  object-fit: contain;
}

.go-to-shop-btn {
  background: var(--gradient-cyan);
  border: none;
  border-radius: var(--radius-lg);
  padding: 1rem 2rem;
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--color-bg-primary);
  cursor: pointer;
  transition: all 0.3s;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  letter-spacing: 1px;
  width: 100%;
}

.go-to-shop-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 0 30px rgba(0, 245, 255, 0.5);
}

.btn-icon {
  font-size: 1.3rem;
}

.access-info {
  font-size: 0.8rem;
  color: #00FF88;
  margin: 0.25rem 0 0 0;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

@media (max-width: 768px) {
  .pricing-options {
    grid-template-columns: 1fr;
  }

  .no-access-card {
    padding: 2rem 1.5rem;
  }

  .lock-icon {
    font-size: 4rem;
  }
}
</style>
