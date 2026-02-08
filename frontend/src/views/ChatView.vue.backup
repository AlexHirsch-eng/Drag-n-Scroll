<template>
  <div class="chat-view">
    <!-- Modern Header -->
    <div class="chat-header">
      <div class="header-left">
        <button @click="goBack" class="back-btn">
          <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M19 12H5M12 19l-7-7 7-7"/>
          </svg>
        </button>
        <div class="header-title-group">
          <h1 class="header-title">Messages</h1>
          <span class="header-subtitle">{{ chats.length }} conversations</span>
        </div>
      </div>
      <div class="header-right">
        <button
          @click="showPracticeModal = true"
          class="practice-btn"
        >
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10 5L2 22l10-5 10 5"/>
            <circle cx="12" cy="12" r="3"/>
          </svg>
          <span>Practice</span>
        </button>
        <div class="lang-selector" @click="cycleLanguage">
          <span class="flag">{{ getFlag(translationLanguage) }}</span>
        </div>
        <button @click="createNewChat" class="new-chat-btn">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 5v14M5 12h14"/>
          </svg>
        </button>
      </div>
    </div>

    <!-- Practice Modal -->
    <div v-if="showPracticeModal" class="modal-overlay" @click="showPracticeModal = false">
      <div class="modal-content practice-modal" @click.stop>
        <div class="modal-header">
          <h2>Daily Practice</h2>
          <button @click="showPracticeModal = false" class="close-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="practice-content">
          <div class="exercise-card" @click="startExercise('vocabulary')">
            <div class="exercise-icon">📚</div>
            <div class="exercise-info">
              <h3>Vocabulary Quiz</h3>
              <p>Test your Chinese vocabulary</p>
              <div class="exercise-difficulty">
                <span class="dot primary"></span>
                <span class="dot primary"></span>
                <span class="dot secondary"></span>
              </div>
            </div>
            <svg class="exercise-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 18l6-6-6-6"/>
            </svg>
          </div>

          <div class="exercise-card" @click="startExercise('grammar')">
            <div class="exercise-icon">✍️</div>
            <div class="exercise-info">
              <h3>Grammar Practice</h3>
              <p>Chinese sentence structures</p>
              <div class="exercise-difficulty">
                <span class="dot primary"></span>
                <span class="dot tertiary"></span>
                <span class="dot secondary"></span>
              </div>
            </div>
            <svg class="exercise-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 18l6-6-6-6"/>
            </svg>
          </div>

          <div class="exercise-card" @click="startExercise('listening')">
            <div class="exercise-icon">🎧</div>
            <div class="exercise-info">
              <h3>Listening Challenge</h3>
              <p>Improve your comprehension</p>
              <div class="exercise-difficulty">
                <span class="dot primary"></span>
                <span class="dot tertiary"></span>
                <span class="dot tertiary"></span>
              </div>
            </div>
            <svg class="exercise-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 18l6-6-6-6"/>
            </svg>
          </div>

          <div class="exercise-card" @click="startExercise('writing')">
            <div class="exercise-icon">🖌️</div>
            <div class="exercise-info">
              <h3>Character Writing</h3>
              <p>Practice Chinese characters</p>
              <div class="exercise-difficulty">
                <span class="dot secondary"></span>
                <span class="dot secondary"></span>
                <span class="dot secondary"></span>
              </div>
            </div>
            <svg class="exercise-arrow" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M9 18l6-6-6-6"/>
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Stories Row -->
    <div class="stories-section">
      <div class="story-item" @click="viewMyStory">
        <div class="story-avatar my-story">
          <div class="avatar-add">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 5v14M5 12h14"/>
            </svg>
          </div>
        </div>
        <div class="story-label">Your Story</div>
      </div>

      <div
        v-for="story in stories"
        :key="story.id"
        class="story-item"
        @click="viewStory(story)"
      >
        <div class="story-avatar" :class="{ viewed: story.is_viewed }">
          <div v-if="story.user.profile?.avatar" class="story-avatar-img">
            <img :src="story.user.profile.avatar" :alt="story.user.username" />
          </div>
          <div v-else class="story-avatar-default">{{ story.user.username[0].toUpperCase() }}</div>
          <div class="story-ring"></div>
        </div>
        <div class="story-label">{{ story.user.username.split(' ')[0] }}</div>
      </div>
    </div>

    <!-- Main Content Area -->
    <div class="main-content">
      <!-- Chat List (Left Side) -->
      <div class="chat-sidebar" :class="{ 'mobile-hidden': activeChat }">
        <div class="sidebar-header">
          <h3>Conversations</h3>
          <div class="chat-stats">{{ chats.length }} chats</div>
        </div>

        <!-- Search -->
        <div class="search-container">
          <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>
          <input
            v-model="searchQuery"
            @input="searchChats"
            type="text"
            placeholder="Search conversations..."
            class="search-input"
          />
        </div>

        <!-- Chat List -->
        <div class="chat-list">
          <div
            v-for="chat in filteredChats"
            :key="chat.id"
            @click="openChat(chat)"
            class="chat-item"
            :class="{
              active: activeChat?.id === chat.id,
              unread: chat.unread_count > 0
            }"
          >
            <div class="chat-item-avatar">
              <div v-if="chat.room_type === 'direct' && chat.other_user">
                <img v-if="chat.other_user.avatar" :src="chat.other_user.avatar" />
                <div v-else class="avatar-fallback">{{ chat.other_user.username[0].toUpperCase() }}</div>
              </div>
              <div v-else class="avatar-fallback group">
                {{ (chat.name || 'Chat')[0].toUpperCase() }}
              </div>
              <div v-if="chat.other_user?.online" class="online-dot"></div>
            </div>

            <div class="chat-item-content">
              <div class="chat-item-top">
                <span class="chat-name">
                  {{ chat.room_type === 'direct' && chat.other_user ? chat.other_user.username : chat.name }}
                </span>
                <span class="chat-time">{{ formatTime(chat.last_message_at || '') }}</span>
              </div>
              <div class="chat-item-preview">
                <span class="preview-text">{{ chat.last_message_preview || 'Start a conversation' }}</span>
                <span v-if="chat.unread_count > 0" class="unread-badge">{{ chat.unread_count }}</span>
              </div>
            </div>
          </div>

          <!-- Empty State -->
          <div v-if="filteredChats.length === 0" class="empty-state">
            <div class="empty-icon">💬</div>
            <h3>No conversations yet</h3>
            <p>Start chatting with people!</p>
            <button @click="createNewChat" class="start-chat-btn">Start Chat</button>
          </div>
        </div>
      </div>

      <!-- Chat Room (Right Side) -->
      <div class="chat-room" v-if="activeChat">
        <!-- Chat Header -->
        <div class="room-header">
          <div class="room-header-left">
            <button @click="activeChat = null" class="mobile-back-btn">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M19 12H5M12 19l-7-7 7-7"/>
              </svg>
            </button>
            <div class="room-avatar">
              <img v-if="activeChat.other_user?.avatar" :src="activeChat.other_user.avatar" />
              <div v-else class="avatar-fallback">
                {{ (activeChat.name || 'Chat')[0].toUpperCase() }}
              </div>
            </div>
            <div class="room-info">
              <h3 class="room-name">
                {{ activeChat.room_type === 'direct' && activeChat.other_user ? activeChat.other_user.username : activeChat.name }}
              </h3>
              <span class="room-status">{{ activeChat.other_user?.online ? 'Online' : 'Offline' }}</span>
            </div>
          </div>
          <div class="room-header-right">
            <button @click="cycleLanguage" class="lang-mini-btn">
              {{ getFlag(translationLanguage) }}
            </button>
          </div>
        </div>

        <!-- Messages Area -->
        <div class="messages-area" ref="messagesContainer">
          <!-- Date Divider -->
          <div class="date-divider">
            <span class="date-text">Today</span>
          </div>

          <!-- Messages -->
          <div
            v-for="message in messages"
            :key="message.id"
            class="message-wrapper"
            :class="{ sent: message.sender_id === currentUserId, received: message.sender_id !== currentUserId }"
          >
            <div v-if="message.sender_id !== currentUserId && message.sender" class="message-sender-name">
              {{ message.sender.username }}
            </div>
            <div class="message-bubble">
              <div v-if="message.text" class="message-text">{{ message.text }}</div>

              <!-- Translation -->
              <div v-if="getTranslation(message)" class="message-translation">
                <div class="translation-header">
                  <span class="translation-flag">{{ getFlag(translationLanguage) }}</span>
                  <span class="translation-label">Translation</span>
                </div>
                <div class="translation-text">{{ getTranslation(message) }}</div>
              </div>

              <!-- Translate Button -->
              <button
                v-if="!getTranslation(message)"
                @click="openLanguageSelector(message.id)"
                class="translate-btn"
              >
                <span class="translate-icon">🌐</span>
                <span class="translate-text">Translate</span>
              </button>

              <!-- Language Selector Dropdown -->
              <div
                v-if="showLanguageSelector && messageToTranslate === message.id"
                class="language-selector-dropdown"
              >
                <div class="language-selector-header">
                  <span>Select Language</span>
                  <button @click="closeLanguageSelector" class="close-dropdown-btn">×</button>
                </div>
                <div class="language-options">
                  <button
                    v-for="lang in availableLanguages"
                    :key="lang.code"
                    @click="translateWithLanguage(message.id, lang.code)"
                    class="language-option"
                    :disabled="translatingMessages.has(message.id)"
                  >
                    <span class="lang-flag">{{ lang.flag }}</span>
                    <span class="lang-name">{{ lang.name }}</span>
                    <span v-if="translatingMessages.has(message.id)" class="loading-spinner-small"></span>
                  </button>
                </div>
              </div>

              <div class="message-meta">
                <span class="message-time">{{ formatMessageTime(message.created_at) }}</span>
                <span v-if="message.sender_id === currentUserId" class="message-status">
                  {{ message.status === 'read' && '✓✓' || message.status === 'delivered' && '✓✓' || '✓' }}
                </span>
              </div>
            </div>
          </div>

          <!-- Typing Indicator -->
          <div v-if="someoneTyping" class="typing-indicator">
            <div class="typing-bubble">
              <span class="typing-dots">
                <span></span>
                <span></span>
              </span>
            </div>
          </div>
        </div>

        <!-- Message Input -->
        <div class="message-input-area">
          <div class="input-container">
            <button class="attach-btn">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21.44 11.05l-9.19 9.19a6 6 0 0 0-8.49-8.49l-9.19 9.19a6 6 0 0 0 8.49 8.49l9.19-9.19a6 6 0 0 0 8.49-8.49zM10.5 8.5l2.5 2.5"/>
              </svg>
            </button>
            <input
              v-model="newMessage"
              @keyup.enter="sendMessage"
              @input="handleTyping"
              type="text"
              placeholder="Type a message..."
              class="message-input"
              ref="messageInput"
            />
            <button
              @click="sendMessage"
              class="send-btn"
              :disabled="!newMessage.trim()"
              :class="{ active: newMessage.trim() }"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 2L11 13M22 2l-7 20-4-9-9-9"/>
                <path d="M22 2l-9 9"/>
              </svg>
            </button>
          </div>
        </div>
      </div>

      <!-- Empty State (No Chat Selected) -->
      <div v-else class="no-chat-selected">
        <div class="empty-content">
          <div class="empty-icon">
            <svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
              <path d="M12 9a2 2 0 0 0-2 2H7a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h5a2 2 0 0 1 2 2z"/>
            </svg>
          </div>
          <h2>Select a conversation</h2>
          <p>Choose a chat from the left or start a new one</p>
          <button @click="createNewChat" class="start-chat-btn">New Message</button>
        </div>
      </div>
    </div>

    <!-- New Chat Modal -->
    <div v-if="showNewChatModal" class="modal-overlay" @click="closeNewChatModal">
      <div class="modal-content new-chat-modal" @click.stop>
        <div class="modal-header">
          <h3>New Message</h3>
          <button @click="closeNewChatModal" class="close-btn">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <line x1="18" y1="6" x2="6" y2="18"/>
              <line x1="6" y1="6" x2="18" y2="18"/>
            </svg>
          </button>
        </div>

        <div class="search-container">
          <svg class="search-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <circle cx="11" cy="11" r="8"/>
            <path d="M21 21l-4.35-4.35"/>
          </svg>
          <input
            v-model="userSearchQuery"
            @input="searchUsers"
            type="text"
            placeholder="Search people..."
            class="search-input"
          />
        </div>

        <div class="suggested-users-list">
          <h4>Suggested</h4>
          <div
            v-for="user in suggestedUsers"
            :key="user.id"
            @click="startChatWith(user)"
            class="user-item"
          >
            <div class="user-avatar">
              <img v-if="user.avatar" :src="user.avatar" />
              <div v-else class="avatar-fallback">{{ user.username[0].toUpperCase() }}</div>
              <div v-if="user.online" class="online-dot"></div>
            </div>
            <div class="user-info">
              <div class="user-name">{{ user.username }}</div>
              <div class="user-bio">{{ user.bio || 'Tap to chat' }}</div>
            </div>
            <div class="user-action">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-.7 5.2 8 8 0 0 1-3.15-2.16 6 6 0 0 1 2-4.5 5.5 5.5 0 0 0-2 .5"/>
              </svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRouter } from 'vue-router'
import { chatAPI, ChatRoom, ChatMessage, SuggestedUser, Story } from '@/api/chat'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

// State
const searchQuery = ref('')
const activeChat = ref<ChatRoom | null>(null)
const messages = ref<ChatMessage[]>([])
const newMessage = ref('')
const showNewChatModal = ref(false)
const userSearchQuery = ref('')
const someoneTyping = ref(false)
const currentUserId = computed(() => authStore.user?.id || 1)
const messagesContainer = ref<HTMLElement | null>(null)
const messageInput = ref<HTMLInputElement | null>(null)
const loading = ref(false)
const translationLanguage = ref<'ru' | 'en' | 'zh' | 'kz' | 'de' | 'fr' | 'es' | 'ja' | 'ko'>('ru')
const translatingMessages = ref<Set<number>>(new Set())
const pollingInterval = ref<number | null>(null)
const showPracticeModal = ref(false)
const showLanguageSelector = ref(false)
const messageToTranslate = ref<number | null>(null)

// Data
const stories = ref<Story[]>([])
const chats = ref<ChatRoom[]>([])
const suggestedUsers = ref<SuggestedUser[]>([])
const allMessages: Record<number, ChatMessage[]> = {}

// Load data on mount
onMounted(async () => {
  await Promise.all([
    loadChats(),
    loadStories(),
    loadSuggestedUsers()
  ])
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})

// Watch for chat changes
watch(activeChat, (newChat, oldChat) => {
  if (oldChat && !newChat) stopPolling()
  if (newChat && !oldChat) startPolling()
})

// API Functions
async function loadChats() {
  try {
    loading.value = true
    const data: any = await chatAPI.getChatRooms()
    const rooms = Array.isArray(data) ? data : (data.results || [])
    chats.value = rooms.filter((chat: ChatRoom) => chat != null)
  } catch (error) {
    console.error('Error loading chats:', error)
  } finally {
    loading.value = false
  }
}

async function loadStories() {
  try {
    const data: any = await chatAPI.getStories()
    stories.value = Array.isArray(data) ? data : (data.results || [])
  } catch (error) {
    console.error('Error loading stories:', error)
  }
}

async function loadSuggestedUsers() {
  try {
    const data: any = await chatAPI.getSuggestedUsers()
    suggestedUsers.value = Array.isArray(data) ? data : (data.results || [])
  } catch (error) {
    console.error('Error loading suggested users:', error)
  }
}

// Chat Functions
async function openChat(chat: ChatRoom) {
  try {
    console.log('=== Opening chat ===')
    console.log('Chat:', chat)
    activeChat.value = chat

    const messagesData: any = await chatAPI.getMessages(chat.id)
    console.log('Messages data:', messagesData)
    const messagesList = Array.isArray(messagesData) ? messagesData : (messagesData.results || [])
    messages.value = messagesList
    allMessages[chat.id] = messagesList

    await chatAPI.markMessagesRead(chat.id)
    chat.unread_count = 0

    console.log('Chat opened successfully, messages loaded:', messagesList.length)
    scrollToBottom()

    // Focus input
    nextTick(() => {
      messageInput.value?.focus()
    })
  } catch (error) {
    console.error('Error opening chat:', error)
  }
}

async function sendMessage() {
  if (!newMessage.value.trim() || !activeChat.value) return

  const messageText = newMessage.value
  newMessage.value = ''

  try {
    await chatAPI.sendMessage(
      activeChat.value.id,
      messageText,
      { messageType: 'text' }
    )

    // Refresh messages after sending (without await to not block)
    refreshMessages()

    // Update chat preview
    activeChat.value.last_message_preview = messageText
    activeChat.value.last_message_at = new Date().toISOString()
    activeChat.value.last_message_sender = 'me'

    scrollToBottom(false)
  } catch (error) {
    console.error('Error sending message:', error)
    // Restore message text on error
    newMessage.value = messageText
  }
}

async function refreshMessages() {
  if (!activeChat.value) return

  try {
    const messagesData: any = await chatAPI.getMessages(activeChat.value.id)
    const messagesList = Array.isArray(messagesData) ? messagesData : (messagesData.results || [])

    const existingIds = new Set(messages.value.map((m: ChatMessage) => m.id))
    const newMessages = messagesList.filter((m: ChatMessage) => !existingIds.has(m.id))

    if (newMessages.length > 0) {
      messages.value.push(...newMessages)

      if (!allMessages[activeChat.value.id]) {
        allMessages[activeChat.value.id] = []
      }
      allMessages[activeChat.value.id].push(...newMessages)

      scrollToBottom(false)
    }
  } catch (error) {
    console.error('Error refreshing messages:', error)
  }
}

function startPolling() {
  pollingInterval.value = window.setInterval(() => {
    if (activeChat.value) {
      refreshMessages()
    }
  }, 3000)
}

function stopPolling() {
  if (pollingInterval.value) {
    clearInterval(pollingInterval.value)
    pollingInterval.value = null
  }
}

// Translation Functions
async function translateMessage(messageId: number, targetLang: 'ru' | 'en' | 'zh' | 'kz' | 'de' | 'fr' | 'es' | 'ja' | 'ko') {
  if (translatingMessages.value.has(messageId)) return

  try {
    translatingMessages.value.add(messageId)
    const updatedMessage = await chatAPI.translateMessage(messageId, targetLang)

    const index = messages.value.findIndex(m => m.id === messageId)
    if (index !== -1) {
      messages.value[index] = updatedMessage
    }

    // Update translation language to the selected one
    translationLanguage.value = targetLang
    closeLanguageSelector()
  } catch (error: any) {
    console.error('Error translating message:', error)
    alert(`Translation failed: ${error.response?.data?.error || error.message}`)
  } finally {
    translatingMessages.value.delete(messageId)
  }
}

function openLanguageSelector(messageId: number) {
  messageToTranslate.value = messageId
  showLanguageSelector.value = true
}

function closeLanguageSelector() {
  showLanguageSelector.value = false
  messageToTranslate.value = null
}

function translateWithLanguage(messageId: number, langCode: 'ru' | 'en' | 'zh' | 'kz' | 'de' | 'fr' | 'es' | 'ja' | 'ko') {
  translateMessage(messageId, langCode)
}

const availableLanguages = [
  { code: 'ru', flag: '🇷🇺', name: 'Russian' },
  { code: 'en', flag: '🇬🇧', name: 'English' },
  { code: 'zh', flag: '🇨🇳', name: 'Chinese' },
  { code: 'kz', flag: '🇰🇿', name: 'Kazakh' },
  { code: 'de', flag: '🇩🇪', name: 'German' },
  { code: 'fr', flag: '🇫🇷', name: 'French' },
  { code: 'es', flag: '🇪🇸', name: 'Spanish' },
  { code: 'ja', flag: '🇯🇵', name: 'Japanese' },
  { code: 'ko', flag: '🇰🇷', name: 'Korean' },
]

function getTranslation(message: ChatMessage): string | null {
  if (translationLanguage.value === 'ru') return message.translation_ru || null
  if (translationLanguage.value === 'en') return message.translation_en || null
  if (translationLanguage.value === 'zh') return message.translation_zh || null
  if (translationLanguage.value === 'kz') return message.translation_kz || null
  if (translationLanguage.value === 'de') return message.translation_de || null
  if (translationLanguage.value === 'fr') return message.translation_fr || null
  if (translationLanguage.value === 'es') return message.translation_es || null
  if (translationLanguage.value === 'ja') return message.translation_ja || null
  if (translationLanguage.value === 'ko') return message.translation_ko || null
  return null
}

function cycleLanguage() {
  const languages: Array<'ru' | 'en' | 'zh' | 'kz' | 'de' | 'fr' | 'es' | 'ja' | 'ko'> = ['ru', 'en', 'zh', 'kz', 'de', 'fr', 'es', 'ja', 'ko']
  const currentIndex = languages.indexOf(translationLanguage.value)
  const nextIndex = (currentIndex + 1) % languages.length
  translationLanguage.value = languages[nextIndex]
}

function getFlag(lang: string): string {
  const flags: Record<string, string> = {
    ru: '🇷🇺',
    en: '🇬🇧',
    zh: '🇨🇳',
    kz: '🇰🇿',
    de: '🇩🇪',
    fr: '🇫🇷',
    es: '🇪🇸',
    ja: '🇯🇵',
    ko: '🇰🇷'
  }
  return flags[lang] || '🌐'
}

// Practice Functions
function startExercise(type: string) {
  showPracticeModal.value = false
  console.log('Starting exercise:', type)
}

// Utility Functions
const filteredChats = computed(() => {
  const validChats = chats.value.filter((chat): chat is ChatRoom => chat != null)

  if (!searchQuery.value) return validChats

  const query = searchQuery.value.toLowerCase()
  return validChats.filter((chat: ChatRoom) => {
    const name = chat.room_type === 'direct' && chat.other_user ? chat.other_user.username : chat.name
    const message = chat.last_message_preview || ''
    return name.toLowerCase().includes(query) || message.toLowerCase().includes(query)
  })
})

function formatTime(dateString?: string): string {
  if (!dateString) return ''

  const date = new Date(dateString)
  const now = new Date()
  const diff = Math.floor((now.getTime() - date.getTime()) / 1000)

  if (diff < 60) return 'now'
  if (diff < 3600) return `${Math.floor(diff / 60)}m`
  if (diff < 86400) return `${Math.floor(diff / 3600)}h`
  return `${Math.floor(diff / 86400)}d`
}

function formatMessageTime(dateString: string): string {
  const date = new Date(dateString)
  return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function handleTyping() {
  if (!activeChat.value) return
  chatAPI.sendTypingIndicator(activeChat.value.id).catch(console.error)
}

function scrollToBottom(force = true) {
  nextTick(() => {
    const container = messagesContainer.value
    if (!container) return

    const isNearBottom = container.scrollHeight - container.scrollTop - container.clientHeight < 100

    if (force || isNearBottom) {
      container.scrollTo({
        top: container.scrollHeight,
        behavior: 'smooth'
      })
    }
  })
}

async function searchChats() {
  // Search is handled by computed property
}

async function searchUsers() {
  // Users are already loaded, filter by search query
}

// Modal Functions
function createNewChat() {
  showNewChatModal.value = true
}

function closeNewChatModal() {
  showNewChatModal.value = false
  userSearchQuery.value = ''
}

function viewStory(story: Story) {
  console.log('View story:', story)
}

function viewMyStory() {
  console.log('View my story')
}

async function startChatWith(user: SuggestedUser) {
  try {
    // Create direct chat with user
    const chatRoom = await chatAPI.createDirectChat(user.id)

    // Add to chats list if not already there
    const existingIndex = chats.value.findIndex(c => c.id === chatRoom.id)
    if (existingIndex === -1) {
      chats.value.unshift(chatRoom)
    } else {
      // Move to top
      const [chat] = chats.value.splice(existingIndex, 1)
      chats.value.unshift(chat)
    }

    // Close modal and open chat
    closeNewChatModal()
    await openChat(chatRoom)
  } catch (error) {
    console.error('Error starting chat:', error)
    alert('Failed to start chat. Please try again.')
  }
}

function goBack() {
  router.back()
}
</script>

<style scoped>
.chat-view {
  height: 100vh;
  background: var(--color-bg-primary);
  display: flex;
  flex-direction: column;
}

/* Header */
.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1rem 1.5rem;
  background: var(--color-bg-elevated);
  border-bottom: 1px solid var(--color-border-primary);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.back-btn {
  background: var(--color-accent-primary-light);
  border: 1px solid var(--color-accent-primary-border);
  color: var(--color-accent-primary);
  width: 36px;
  height: 36px;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-base);
}

.back-btn:hover {
  background: var(--color-accent-primary);
  color: var(--color-text-primary);
}

.header-title-group {
  display: flex;
  flex-direction: column;
  gap: 0.15rem;
}

.header-title {
  font-size: 1.25rem;
  font-weight: 700;
  background: var(--gradient-primary);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  margin: 0;
}

.header-subtitle {
  font-size: 0.75rem;
  color: #A0A8C0;
  font-weight: 500;
}

.header-right {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.practice-btn {
  background: var(--gradient-secondary);
  border: none;
  color: white;
  padding: 0.5rem 0.875rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  gap: 0.375rem;
  font-weight: 600;
  font-size: 0.8125rem;
  cursor: pointer;
  transition: all var(--transition-base);
  box-shadow: var(--shadow-secondary);
}

.practice-btn:hover {
  transform: translateY(-1px);
  box-shadow: var(--shadow-glow-secondary);
}

.lang-selector {
  background: var(--color-accent-tertiary-light);
  border: 1px solid var(--color-accent-tertiary-border);
  border-radius: var(--radius-md);
  padding: 0.25rem 0.5rem;
  cursor: pointer;
  transition: all var(--transition-base);
}

.lang-selector:hover {
  background: var(--color-accent-tertiary-light);
}

.flag {
  font-size: 1rem;
}

.new-chat-btn {
  background: var(--color-accent-primary-light);
  border: 1px solid var(--color-accent-primary-border);
  border-radius: var(--radius-md);
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-accent-primary);
  cursor: pointer;
  transition: all var(--transition-base);
}

.new-chat-btn:hover {
  background: var(--color-accent-primary);
  color: var(--color-text-primary);
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(4px);
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 1rem;
  animation: fadeIn var(--transition-base) ease;
}

.modal-content {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-xl);
  width: 100%;
  max-width: 480px;
  max-height: 80vh;
  overflow-y: auto;
  box-shadow: var(--shadow-xl);
  animation: slideUp var(--transition-slow) ease;
}

.practice-modal {
  max-width: 520px;
}

.modal-header {
  padding: 1.25rem 1.5rem;
  border-bottom: 1px solid var(--color-border-primary);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.modal-header h2 {
  font-size: 1.25rem;
  font-weight: 700;
  margin: 0;
}

.close-btn {
  background: var(--color-accent-primary-light);
  border: none;
  color: var(--color-accent-primary);
  width: 32px;
  height: 32px;
  border-radius: var(--radius-md);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-base);
}

.close-btn:hover {
  background: var(--color-accent-primary);
  color: var(--color-text-primary);
  transform: rotate(90deg);
}

.practice-content {
  padding: 1.25rem 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.exercise-card {
  display: flex;
  align-items: center;
  gap: 0.875rem;
  padding: 0.875rem;
  background: var(--color-bg-secondary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all var(--transition-base);
}

.exercise-card:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-accent-primary-border);
  transform: translateX(2px);
}

.exercise-icon {
  font-size: 1.5rem;
}

.exercise-info {
  flex: 1;
}

.exercise-info h3 {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0 0 0.125rem 0;
}

.exercise-info p {
  font-size: 0.8125rem;
  color: #B0B8C8;
  margin: 0 0 0.375rem 0;
}

.exercise-difficulty {
  display: flex;
  gap: 0.125rem;
}

.dot {
  width: 5px;
  height: 5px;
  border-radius: 50%;
}

.dot.primary { background: var(--color-accent-primary); }
.dot.tertiary { background: var(--color-accent-tertiary); }
.dot.secondary { background: var(--color-accent-secondary); }

.exercise-arrow {
  color: var(--color-text-faint);
  transition: transform var(--transition-base);
}

.exercise-card:hover .exercise-arrow {
  transform: translateX(2px);
  color: var(--color-accent-primary);
}

/* Stories */
.stories-section {
  display: flex;
  gap: 0.75rem;
  padding: 1rem 1.5rem;
  overflow-x: auto;
  scrollbar-width: none;
}

.stories-section::-webkit-scrollbar {
  display: none;
}

.story-item {
  flex-shrink: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.375rem;
  cursor: pointer;
}

.story-avatar {
  position: relative;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: var(--gradient-primary);
  padding: 2px;
  transition: transform var(--transition-base);
}

.story-item:hover .story-avatar {
  transform: scale(1.05);
}

.my-story .story-avatar {
  background: var(--color-border-secondary);
}

.story-avatar-img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
}

.story-avatar-img img {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.story-avatar-default {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: var(--gradient-tertiary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-primary);
  font-weight: 700;
  font-size: 1.125rem;
}

.avatar-add {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: var(--color-bg-secondary);
  border: 1px dashed var(--color-accent-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-accent-primary);
}

.story-ring {
  position: absolute;
  inset: -2px;
  border-radius: 50%;
  background: var(--gradient-primary);
}

.story-avatar.viewed .story-ring {
  background: var(--color-border-secondary);
}

.story-label {
  font-size: 0.625rem;
  color: var(--color-text-muted);
  text-align: center;
  max-width: 60px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* Main Content */
.main-content {
  flex: 1;
  display: flex;
  overflow: hidden;
}

/* Sidebar */
.chat-sidebar {
  width: 360px;
  border-right: 1px solid var(--color-border-primary);
  display: flex;
  flex-direction: column;
  background: var(--color-bg-secondary);
  transition: transform 0.3s ease;
}

.chat-sidebar.mobile-hidden {
  display: flex;
}

.sidebar-header {
  padding: 1.125rem 1.5rem;
  border-bottom: 1px solid var(--color-border-primary);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h3 {
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.chat-stats {
  font-size: 0.75rem;
  color: var(--color-text-muted);
}

.search-container {
  padding: 0.875rem 1.5rem;
  position: relative;
}

.search-icon {
  position: absolute;
  left: 1.625rem;
  top: 50%;
  transform: translateY(-50%);
  color: var(--color-text-muted);
  pointer-events: none;
}

.search-input {
  width: 100%;
  padding: 0.625rem 0.875rem 0.625rem 2.25rem;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: 0.875rem;
  outline: none;
  transition: all var(--transition-base);
}

.search-input:focus {
  border-color: var(--color-accent-primary);
  box-shadow: 0 0 0 3px var(--color-accent-primary-light);
}

.chat-list {
  flex: 1;
  overflow-y: auto;
  padding: 0.5rem 0.75rem;
}

.chat-item {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.625rem;
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
  margin-bottom: 0.125rem;
}

.chat-item:hover {
  background: var(--color-bg-hover);
}

.chat-item.active {
  background: var(--color-accent-primary-light);
  border: 1px solid var(--color-accent-primary-border);
}

.chat-item.unread {
  background: var(--color-accent-secondary-light);
}

.chat-item-avatar {
  position: relative;
  width: 44px;
  height: 44px;
  flex-shrink: 0;
}

.avatar-fallback {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  background: var(--gradient-primary);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-text-primary);
  font-weight: 700;
  font-size: 1rem;
}

.avatar-fallback.group {
  background: var(--gradient-purple);
}

.online-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 9px;
  height: 9px;
  border-radius: 50%;
  background: var(--color-success);
  border: 2px solid var(--color-bg-primary);
}

.chat-item-content {
  flex: 1;
  min-width: 0;
}

.chat-item-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 0.125rem;
}

.chat-name {
  font-weight: 600;
  color: var(--color-text-primary);
  font-size: 0.875rem;
}

.chat-time {
  font-size: 0.6875rem;
  color: var(--color-text-muted);
}

.chat-item-preview {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 0.375rem;
}

.preview-text {
  font-size: 0.8125rem;
  color: var(--color-text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  flex: 1;
}

.unread-badge {
  background: var(--gradient-primary);
  color: var(--color-text-primary);
  font-size: 0.625rem;
  font-weight: 700;
  padding: 0.125rem 0.375rem;
  border-radius: var(--radius-sm);
  min-width: 18px;
  text-align: center;
}

/* Chat Room */
.chat-room {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: var(--color-bg-primary);
}

.room-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.875rem 1.5rem;
  border-bottom: 1px solid var(--color-border-primary);
  background: var(--color-bg-elevated);
}

.room-header-left {
  display: flex;
  align-items: center;
  gap: 0.625rem;
}

.mobile-back-btn {
  background: none;
  border: none;
  color: var(--color-text-primary);
  cursor: pointer;
  display: none;
}

@media (max-width: 768px) {
  .mobile-back-btn {
    display: flex;
  }
}

.room-avatar {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  overflow: hidden;
}

.room-avatar img,
.avatar-fallback {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.room-info {
  display: flex;
  flex-direction: column;
}

.room-name {
  font-weight: 600;
  color: var(--color-text-primary);
  font-size: 0.9375rem;
  margin: 0;
}

.room-status {
  font-size: 0.6875rem;
  color: var(--color-success);
}

.room-header-right {
  display: flex;
  align-items: center;
  gap: 0.375rem;
}

.lang-mini-btn {
  background: var(--color-accent-tertiary-light);
  border: 1px solid var(--color-accent-tertiary-border);
  border-radius: var(--radius-md);
  padding: 0.25rem 0.5rem;
  font-size: 0.875rem;
  cursor: pointer;
}

/* Messages */
.messages-area {
  flex: 1;
  overflow-y: auto;
  padding: 1.25rem;
  display: flex;
  flex-direction: column;
  gap: 0.875rem;
}

.date-divider {
  display: flex;
  align-items: center;
  margin: 0.375rem 0;
}

.date-divider::before,
.date-divider::after {
  content: '';
  flex: 1;
  border-bottom: 1px solid var(--color-border-primary);
}

.date-text {
  padding: 0 0.75rem;
  font-size: 0.6875rem;
  color: var(--color-text-muted);
  text-transform: uppercase;
  letter-spacing: 0.0625rem;
  background: var(--color-bg-elevated);
  border-radius: var(--radius-sm);
}

.message-wrapper {
  display: flex;
  flex-direction: column;
  max-width: 70%;
}

.message-wrapper.sent {
  align-self: flex-end;
  align-items: flex-end;
}

.message-wrapper.received {
  align-self: flex-start;
  align-items: flex-start;
}

.message-sender-name {
  font-size: 0.6875rem;
  color: var(--color-text-muted);
  margin-bottom: 0.25rem;
  margin-left: 0.5rem;
}

.message-wrapper.sent .message-sender-name {
  margin-right: 0.5rem;
  margin-left: 0;
  text-align: right;
}

.message-bubble {
  display: flex;
  flex-direction: column;
  position: relative;
}

.message-text {
  padding: 0.625rem 0.875rem;
  border-radius: var(--radius-lg);
  font-size: 0.9375rem;
  line-height: 1.5;
  word-wrap: break-word;
}

.message-wrapper.sent .message-text {
  background: var(--gradient-primary);
  color: var(--color-text-primary);
  border-bottom-right-radius: var(--radius-sm);
}

.message-wrapper.received .message-text {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-primary);
  color: var(--color-text-primary);
  border-bottom-left-radius: var(--radius-sm);
}

/* Translation */
.message-translation {
  margin-top: 0.375rem;
  padding: 0.375rem 0.625rem;
  background: var(--color-accent-primary-light);
  border-left: 2px solid var(--color-accent-primary);
  border-radius: var(--radius-sm);
}

.translation-header {
  display: flex;
  align-items: center;
  gap: 0.375rem;
  margin-bottom: 0.125rem;
}

.translation-flag {
  font-size: 0.75rem;
}

.translation-label {
  font-size: 0.625rem;
  font-weight: 600;
  color: var(--color-accent-primary);
  text-transform: uppercase;
  letter-spacing: 0.03125rem;
}

.translation-text {
  color: var(--color-text-secondary);
  font-size: 0.8125rem;
  line-height: 1.4;
}

.translate-btn {
  background: var(--color-accent-primary-light);
  border: 1px solid var(--color-accent-primary-border);
  border-radius: var(--radius-sm);
  padding: 0.25rem 0.625rem;
  margin-top: 0.375rem;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  transition: all var(--transition-base);
  align-self: flex-start;
}

.translate-btn:hover:not(:disabled) {
  background: var(--color-accent-primary);
  transform: scale(1.02);
}

.translate-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.loading-spinner {
  width: 10px;
  height: 10px;
  border: 2px solid var(--color-accent-primary);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

.translate-icon {
  font-size: 0.875rem;
}

.translate-text {
  font-size: 0.6875rem;
  font-weight: 600;
  color: var(--color-accent-primary);
}

/* Language Selector Dropdown */
.language-selector-dropdown {
  position: absolute;
  bottom: 100%;
  left: 0;
  margin-bottom: 0.5rem;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  box-shadow: var(--shadow-xl);
  min-width: 200px;
  z-index: 100;
}

.language-selector-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.625rem 0.875rem;
  border-bottom: 1px solid var(--color-border-primary);
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-text-primary);
}

.close-dropdown-btn {
  background: none;
  border: none;
  color: var(--color-text-muted);
  font-size: 1.25rem;
  cursor: pointer;
  padding: 0;
  width: 20px;
  height: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-sm);
  transition: all var(--transition-base);
}

.close-dropdown-btn:hover {
  background: var(--color-bg-hover);
  color: var(--color-text-primary);
}

.language-options {
  display: flex;
  flex-direction: column;
  max-height: 250px;
  overflow-y: auto;
}

.language-option {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.625rem 0.875rem;
  background: none;
  border: none;
  cursor: pointer;
  transition: all var(--transition-base);
  width: 100%;
  text-align: left;
}

.language-option:hover:not(:disabled) {
  background: var(--color-bg-hover);
}

.language-option:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.lang-flag {
  font-size: 1rem;
}

.lang-name {
  flex: 1;
  font-size: 0.8125rem;
  color: var(--color-text-primary);
}

.loading-spinner-small {
  width: 12px;
  height: 12px;
  border: 2px solid var(--color-accent-primary);
  border-top-color: transparent;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

.message-meta {
  display: flex;
  align-items: center;
  gap: 0.25rem;
  margin-top: 0.125rem;
  padding: 0 0.375rem;
}

.message-wrapper.sent .message-meta {
  justify-content: flex-end;
}

.message-wrapper.received .message-meta {
  justify-content: flex-start;
}

.message-time {
  font-size: 0.625rem;
  color: var(--color-text-faint);
}

.message-status {
  font-size: 0.6875rem;
  color: var(--color-accent-tertiary);
}

/* Typing */
.typing-indicator {
  display: flex;
  justify-content: flex-start;
  padding: 0 0.75rem;
}

.typing-bubble {
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-primary);
  padding: 0.375rem 0.75rem;
  border-radius: var(--radius-lg);
  border-bottom-left-radius: var(--radius-sm);
  display: flex;
  align-items: center;
}

.typing-dots {
  display: flex;
  gap: 3px;
}

.typing-dots span {
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--color-text-muted);
  animation: bounce 1.4s infinite ease-in-out both;
}

.typing-dots span:nth-child(2) {
  animation-delay: 0.2s;
}

.typing-dots span:nth-child(3) {
  animation-delay: 0.4s;
}

/* Input */
.message-input-area {
  padding: 0.875rem 1.5rem;
  background: var(--color-bg-elevated);
  border-top: 1px solid var(--color-border-primary);
}

.input-container {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: var(--color-bg-primary);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  padding: 0.375rem;
}

.attach-btn {
  background: none;
  border: none;
  color: var(--color-text-muted);
  cursor: pointer;
  padding: 0.375rem;
  transition: all var(--transition-base);
}

.attach-btn:hover {
  color: var(--color-accent-primary);
}

.message-input {
  flex: 1;
  background: none;
  border: none;
  color: var(--color-text-primary);
  font-size: 0.9375rem;
  outline: none;
  padding: 0.375rem;
}

.message-input::placeholder {
  color: var(--color-text-muted);
}

.send-btn {
  background: var(--gradient-primary);
  border: none;
  border-radius: var(--radius-md);
  width: 36px;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all var(--transition-base);
  color: var(--color-text-primary);
}

.send-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
  transform: none;
}

.send-btn.active {
  transform: scale(1.05);
  box-shadow: var(--shadow-glow-primary);
}

/* Empty State */
.no-chat-selected {
  flex: 1;
  display: flex;
  align-items: center;
  justify-content: center;
  background: var(--color-bg-primary);
}

.empty-content {
  text-align: center;
  padding: 2rem;
}

.empty-icon {
  margin-bottom: 1.25rem;
  opacity: 0.5;
}

.empty-icon svg {
  stroke: var(--color-text-muted);
}

.no-chat-selected h2 {
  color: var(--color-text-primary);
  font-size: 1.25rem;
  margin: 0 0 0.375rem 0;
  font-weight: 600;
}

.no-chat-selected p {
  color: var(--color-text-muted);
  margin: 0 0 1.25rem 0;
}

.start-chat-btn {
  background: var(--gradient-primary);
  border: none;
  border-radius: var(--radius-md);
  padding: 0.625rem 1.25rem;
  color: var(--color-text-primary);
  font-weight: 600;
  cursor: pointer;
  transition: all var(--transition-base);
}

.start-chat-btn:hover {
  transform: scale(1.02);
  box-shadow: var(--shadow-glow-primary);
}

/* New Chat Modal */
.new-chat-modal {
  max-width: 380px;
}

.modal-header h3 {
  font-size: 1.0625rem;
  font-weight: 600;
  color: var(--color-text-primary);
  margin: 0;
}

.suggested-users-list {
  padding: 1rem;
}

.suggested-users-list h4 {
  color: var(--color-text-muted);
  font-size: 0.6875rem;
  text-transform: uppercase;
  letter-spacing: 0.0625rem;
  margin: 0 0 0.75rem 0;
  font-weight: 600;
}

.user-item {
  display: flex;
  align-items: center;
  gap: 0.625rem;
  padding: 0.625rem;
  background: var(--color-bg-hover);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all var(--transition-base);
}

.user-item:hover {
  background: var(--color-accent-primary-light);
  border-color: var(--color-accent-primary-border);
}

.user-avatar {
  position: relative;
  width: 38px;
  height: 38px;
}

.user-avatar img,
.avatar-fallback {
  width: 100%;
  height: 100%;
  border-radius: 50%;
  object-fit: cover;
}

.user-info {
  flex: 1;
}

.user-name {
  color: var(--color-text-primary);
  font-weight: 600;
  font-size: 0.875rem;
  margin-bottom: 0.0625rem;
}

.user-bio {
  color: var(--color-text-muted);
  font-size: 0.75rem;
}

.user-action {
  color: var(--color-accent-primary);
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: 3rem 1.5rem;
}

.empty-state .empty-icon {
  font-size: 3rem;
  opacity: 0.6;
}

.empty-state h3 {
  color: var(--color-text-primary);
  font-size: 1.0625rem;
  margin: 0 0 0.375rem 0;
}

.empty-state p {
  color: var(--color-text-muted);
  font-size: 0.875rem;
  margin: 0 0 1rem 0;
}

/* Responsive */
@media (max-width: 768px) {
  .chat-sidebar {
    position: absolute;
    width: 100%;
    height: 100%;
    z-index: 10;
    transform: translateX(0);
    transition: transform 0.3s ease;
  }

  .chat-sidebar.mobile-hidden {
    transform: translateX(-100%);
  }

  .chat-room {
    width: 100%;
    position: absolute;
    top: 0;
    left: 0;
    height: 100%;
    z-index: 5;
  }

  .message-wrapper {
    max-width: 85%;
  }

  .mobile-back-btn {
    display: flex !important;
  }
}
</style>
