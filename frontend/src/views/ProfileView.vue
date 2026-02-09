<template>
  <div class="profile-view">
    <!-- Background Effects -->
    <div class="bg-effects">
      <div class="circuit-grid"></div>
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>
    </div>

    <!-- Content -->
    <div class="content">
      <div v-if="isLoading" class="loading-state">
        <div class="cyber-loader"></div>
        <div class="loading-text">ЗАГРУЗКА ПРОФИЛЯ...</div>
      </div>

      <div v-else class="profile-container">
        <!-- Header -->
        <div class="section-header">
          <h1 class="cyber-title">
            <span class="title-icon">👤</span>
            {{ isOwnProfile ? 'ПРОФИЛЬ' : 'ПРОФИЛЬ ПОЛЬЗОВАТЕЛЯ' }}
          </h1>
          <div class="tech-line"></div>
        </div>

        <!-- User Card -->
        <div class="cyber-card user-card">
          <div class="card-glow"></div>
          <div class="user-avatar">
            <div class="avatar-ring"></div>
            <div class="avatar-text">{{ user?.username?.charAt(0).toUpperCase() }}</div>
          </div>
          <div class="user-info">
            <h2 class="username">{{ user?.username }}</h2>
            <p class="email">{{ isOwnProfile ? user?.email : '' }}</p>
          </div>
        </div>

        <!-- Social Stats -->
        <div class="social-stats-section">
          <div class="cyber-card social-stats-card">
            <div class="card-glow"></div>
            <div class="social-stats-grid">
              <div class="social-stat">
                <div class="social-stat-icon">👥</div>
                <div class="social-stat-value">{{ user?.followers_count || 0 }}</div>
                <div class="social-stat-label">ПОДПИСЧИКИ</div>
              </div>
              <div class="social-stat-divider"></div>
              <div class="social-stat">
                <div class="social-stat-icon">👣</div>
                <div class="social-stat-value">{{ user?.following_count || 0 }}</div>
                <div class="social-stat-label">ПОДПИСКИ</div>
              </div>
              <div class="social-stat-divider"></div>
              <div class="social-stat">
                <div class="social-stat-icon">❤️</div>
                <div class="social-stat-value">{{ user?.likes_received || 0 }}</div>
                <div class="social-stat-label">ЛАЙКИ</div>
              </div>
            </div>
          </div>
        </div>

        <!-- Stats Grid -->
        <div class="stats-section">
          <h3 class="section-title">СТАТИСТИКА ПРОГРЕССА</h3>
          <div class="stats-grid">
            <div class="stat-card stat-gold">
              <div class="stat-icon">
                <img src="/src/images/coin.png" alt="coins" class="coin-icon-profile">
              </div>
              <div class="stat-value">{{ user?.progress?.total_xp || 0 }}</div>
              <div class="stat-label">ВСЕГО СКРОЛЛОВ</div>
              <div class="stat-bar"></div>
            </div>
            <div class="stat-card stat-red">
              <div class="stat-icon">🔥</div>
              <div class="stat-value">{{ user?.progress?.streak_days || 0 }}</div>
              <div class="stat-label">ДНЕЙ ПОДРЯД</div>
              <div class="stat-bar"></div>
            </div>
            <div class="stat-card stat-gold">
              <div class="stat-icon">📅</div>
              <div class="stat-value">{{ user?.progress?.current_day || 1 }}</div>
              <div class="stat-label">ТЕКУЩИЙ ДЕНЬ</div>
              <div class="stat-bar"></div>
            </div>
            <div class="stat-card stat-cyan">
              <div class="stat-icon">✅</div>
              <div class="stat-value">{{ user?.progress?.completed_days?.length || 0 }}</div>
              <div class="stat-label">ЗАВЕРШЕНО</div>
              <div class="stat-bar"></div>
            </div>
          </div>
        </div>

        <!-- User Videos Section -->
        <div class="videos-section">
          <h3 class="section-title">
            <span class="title-icon">🎬</span>
            {{ isOwnProfile ? 'МОИ ВИДЕО' : 'ВИДЕО' }}
            <span class="video-count">{{ userVideos.length }}</span>
          </h3>

          <div v-if="isLoadingVideos" class="loading-state">
            <div class="cyber-loader"></div>
            <div class="loading-text">ЗАГРУЗКА ВИДЕО...</div>
          </div>

          <div v-else-if="userVideos.length === 0" class="empty-videos">
            <div class="empty-icon">📹</div>
            <div class="empty-text">Пока нет видео</div>
          </div>

          <div v-else class="videos-grid">
            <div
              v-for="video in userVideos"
              :key="video.id"
              @click="goToVideo(video.id)"
              class="video-preview-card"
            >
              <div class="video-thumbnail">
                <video v-if="video.thumbnail || video.video_file" :src="video.video_file" class="preview-video" muted></video>
                <div class="play-overlay">
                  <div class="play-icon">▶</div>
                </div>
                <div class="video-duration">{{ formatDuration(video.duration) }}</div>
              </div>
              <div class="video-info">
                <div class="video-description">{{ video.description || 'Нет описания' }}</div>
                <div class="video-stats">
                  <span class="stat">❤️ {{ video.likes_count }}</span>
                  <span class="stat">💬 {{ video.comments_count }}</span>
                  <span class="stat">👁️ {{ video.views_count }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Post Video Section (only for own profile) -->
        <div v-if="isOwnProfile" class="post-video-section">
          <h3 class="section-title">
            <span class="title-icon">📹</span>
            ДОБАВИТЬ ВИДЕО
          </h3>
          <button @click="showPostVideoModal = true" class="cyber-btn cyber-btn-primary">
            <span class="btn-text">+ ПОСТИТЬ ВИДЕО</span>
            <span class="btn-glitch"></span>
          </button>
        </div>

        <!-- Post Video Modal -->
        <div v-if="showPostVideoModal" class="modal-overlay" @click.self="showPostVideoModal = false">
          <div class="modal-content">
            <div class="modal-header">
              <h2>📹 Добавить видео</h2>
              <button @click="showPostVideoModal = false" class="close-btn">×</button>
            </div>
            <form @submit.prevent="postVideo" class="post-video-form">
              <div class="form-group">
                <label class="form-label">Название *</label>
                <input
                  v-model="videoForm.title"
                  type="text"
                  class="cyber-input"
                  placeholder="Название видео"
                  required
                >
              </div>
              <div class="form-group">
                <label class="form-label">Ссылка на видео *</label>
                <input
                  v-model="videoForm.video_url"
                  type="url"
                  class="cyber-input"
                  placeholder="https://youtube.com/watch?v=..."
                  required
                >
                <div class="form-hint">Поддерживается: YouTube, Vimeo, и другие платформы</div>
              </div>
              <div class="form-group">
                <label class="form-label">Ссылка на обложку</label>
                <input
                  v-model="videoForm.thumbnail_url"
                  type="url"
                  class="cyber-input"
                  placeholder="https://img.youtube.com/vi/.../maxresdefault.jpg"
                >
              </div>
              <div class="form-group">
                <label class="form-label">Описание</label>
                <textarea
                  v-model="videoForm.description"
                  class="cyber-textarea"
                  rows="3"
                  placeholder="О чем видео..."
                ></textarea>
              </div>
              <div class="form-group">
                <label class="form-label">Уровень HSK</label>
                <select v-model="videoForm.hsk_level" class="cyber-select">
                  <option :value="1">HSK 1</option>
                  <option :value="2">HSK 2</option>
                  <option :value="3">HSK 3</option>
                  <option :value="4">HSK 4</option>
                  <option :value="5">HSK 5</option>
                  <option :value="6">HSK 6</option>
                </select>
              </div>
              <div class="form-group">
                <label class="form-label">Теги (через запятую)</label>
                <input
                  v-model="videoForm.tags"
                  type="text"
                  class="cyber-input"
                  placeholder="грамматика, произношение, иероглифы"
                >
              </div>
              <div class="form-actions">
                <button type="button" @click="showPostVideoModal = false" class="cyber-btn cyber-btn-secondary">
                  <span class="btn-text">ОТМЕНА</span>
                </button>
                <button type="submit" class="cyber-btn cyber-btn-primary" :disabled="isPosting">
                  <span class="btn-text">{{ isPosting ? 'ОТПРАВКА...' : 'ОПУБЛИКОВАТЬ' }}</span>
                </button>
              </div>
            </form>
          </div>
        </div>

        <!-- Settings -->
        <div v-if="isOwnProfile" class="settings-section">
          <h3 class="section-title">НАСТРОЙКИ</h3>
          <div class="cyber-card">
            <div class="card-glow"></div>
            <div class="setting-item">
              <label class="setting-label">
                <span class="label-icon">🌍</span>
                <span>Язык обучения</span>
              </label>
              <select v-model="profileForm.learning_language" @change="updateProfile" class="cyber-select">
                <option value="RU">Русский</option>
                <option value="KZ">Казахский</option>
              </select>
            </div>
            <div class="setting-item">
              <label class="setting-label">
                <span class="label-icon">📊</span>
                <span>Уровень HSK</span>
              </label>
              <div class="setting-value">HSK {{ user?.profile?.current_hsk_level || 1 }}</div>
            </div>
          </div>
        </div>

        <!-- Logout Button -->
        <button v-if="isOwnProfile" @click="logout" class="cyber-btn cyber-btn-danger">
          <span class="btn-text">ВЫЙТИ</span>
          <span class="btn-glitch"></span>
        </button>

        <!-- Back Button -->
        <div class="back-section">
          <button @click="goBack" class="cyber-btn back-btn-profile">
            <span class="btn-text">← НАЗАД ДОМОЙ</span>
            <span class="btn-glitch"></span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { authAPI } from '@/api/auth'
import { videoAPI, Video } from '@/api/video'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()

const isLoading = ref(true)
const isLoadingVideos = ref(true)
const isOwnProfile = computed(() => !route.params.id)
const profileUserId = computed(() => route.params.id ? parseInt(route.params.id as string) : authStore.user?.id)
const user = ref(authStore.user)
const userVideos = ref<Video[]>([])
const profileForm = ref({
  learning_language: user.value?.profile?.learning_language || 'RU'
})

// Post video form
const showPostVideoModal = ref(false)
const isPosting = ref(false)
const videoForm = ref({
  title: '',
  video_url: '',
  thumbnail_url: '',
  description: '',
  hsk_level: 1,
  tags: ''
})

onMounted(async () => {
  // Load profile data
  if (!isOwnProfile.value && profileUserId.value) {
    // Load another user's profile
    try {
      user.value = await authAPI.getUserById(profileUserId.value)
    } catch (error) {
      console.error('Error loading user profile:', error)
      router.push('/videos')
    }
  } else {
    // Load own profile
    if (!user.value) {
      await authStore.loadUser()
      user.value = authStore.user
      if (user.value?.profile) {
        profileForm.value.learning_language = user.value.profile.learning_language
      }
    }
  }
  isLoading.value = false

  // Load user videos
  await loadUserVideos()
})

async function loadUserVideos() {
  if (!user.value?.id) return

  try {
    isLoadingVideos.value = true
    // Get videos from the user's feed endpoint
    const videos = await videoAPI.getUserFeed(user.value.id)
    userVideos.value = videos.map(video => ({
      ...video,
      url: video.video_file,
      thumbnail: video.thumbnail || ''
    }))
    console.log('User videos loaded:', userVideos.value.length)
  } catch (error) {
    console.error('Error loading user videos:', error)
  } finally {
    isLoadingVideos.value = false
  }
}

async function postVideo() {
  if (!videoForm.value.title.trim() || !videoForm.value.video_url.trim()) {
    alert('Пожалуйста, заполните название и ссылку на видео')
    return
  }

  try {
    isPosting.value = true

    // Parse tags from comma-separated string
    const tagsArray = videoForm.value.tags
      .split(',')
      .map(tag => tag.trim())
      .filter(tag => tag.length > 0)

    const videoData = {
      title: videoForm.value.title.trim(),
      video_url: videoForm.value.video_url.trim(),
      thumbnail_url: videoForm.value.thumbnail_url.trim() || undefined,
      description: videoForm.value.description.trim() || '',
      hsk_level: videoForm.value.hsk_level,
      tags: tagsArray
    }

    const newVideo = await videoAPI.postVideo(videoData)

    // Add to videos list
    userVideos.value.unshift(newVideo)

    // Close modal and reset form
    showPostVideoModal.value = false
    videoForm.value = {
      title: '',
      video_url: '',
      thumbnail_url: '',
      description: '',
      hsk_level: 1,
      tags: ''
    }

    alert('Видео успешно опубликовано!')
  } catch (error: any) {
    console.error('Error posting video:', error)
    alert('Ошибка при публикации видео: ' + (error.response?.data?.detail || error.message))
  } finally {
    isPosting.value = false
  }
}

async function updateProfile() {
  if (user.value && isOwnProfile.value) {
    await authStore.updateProfile(profileForm.value)
  }
}

async function logout() {
  await authStore.logout()
  router.push('/login')
}

function goToVideo(videoId: number) {
  // Store the video to navigate and open VideosView
  router.push({ name: 'videos', query: { video: videoId.toString() } })
}

function formatDuration(seconds: number): string {
  if (!seconds) return '0:00'
  const mins = Math.floor(seconds / 60)
  const secs = Math.floor(seconds % 60)
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

function goBack() {
  router.push('/app')
}
</script>

<style scoped>
.profile-view {
  min-height: 100vh;
  position: relative;
  overflow: hidden;
  background: var(--color-bg-primary);
}

/* Background Effects */
.bg-effects {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  pointer-events: none;
}

.circuit-grid {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(0, 229, 255, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(0, 229, 255, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
}

.glow-orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(100px);
  opacity: 0.3;
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 500px;
  height: 500px;
  background: var(--color-accent-cyan);
  top: -200px;
  right: -200px;
}

.orb-2 {
  width: 400px;
  height: 400px;
  background: var(--color-accent-red);
  bottom: -150px;
  left: -150px;
  animation-delay: -10s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0); }
  50% { transform: translate(50px, 50px); }
}

/* Content */
.content {
  position: relative;
  z-index: 1;
  padding: var(--spacing-lg);
  max-width: 800px;
  margin: 0 auto;
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 70vh;
}

.cyber-loader {
  width: 80px;
  height: 80px;
  border: 4px solid transparent;
  border-top-color: var(--color-accent-cyan);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  box-shadow: 0 0 30px var(--color-accent-cyan);
}

.loading-text {
  margin-top: 2rem;
  color: var(--color-accent-cyan);
  font-size: 0.9rem;
  letter-spacing: 3px;
  font-weight: 600;
  animation: flicker 2s infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Profile Container */
.profile-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

/* Section Header */
.section-header {
  text-align: center;
  margin-bottom: var(--spacing-md);
}

.cyber-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--color-text-primary);
  letter-spacing: 5px;
  text-shadow: 0 0 20px var(--color-accent-cyan);
  margin-bottom: 1rem;
}

.title-icon {
  font-size: 2rem;
}

.tech-line {
  height: 2px;
  background: var(--gradient-cyber);
  box-shadow: var(--shadow-cyan);
  max-width: 200px;
  margin: 0 auto;
}

/* Cyber Card */
.cyber-card {
  background: rgba(17, 19, 24, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 229, 255, 0.2);
  border-radius: var(--radius-lg);
  padding: var(--spacing-lg);
  position: relative;
  overflow: hidden;
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-cyber);
  box-shadow: var(--shadow-cyan);
}

/* User Card */
.user-card {
  display: flex;
  align-items: center;
  gap: var(--spacing-lg);
}

.user-avatar {
  position: relative;
  width: 100px;
  height: 100px;
  flex-shrink: 0;
}

.avatar-ring {
  position: absolute;
  top: -5px;
  left: -5px;
  right: -5px;
  bottom: -5px;
  border: 2px solid var(--color-accent-cyan);
  border-radius: 50%;
  animation: pulse 2s ease-in-out infinite;
}

.avatar-text {
  width: 100%;
  height: 100%;
  background: var(--gradient-cyber);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--color-bg-primary);
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(1.05); }
}

.user-info {
  flex: 1;
}

.username {
  font-size: 1.8rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: 0.5rem;
}

.email {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

/* Social Stats Section */
.social-stats-section {
  margin-bottom: var(--spacing-lg);
}

.social-stats-card {
  padding: var(--spacing-lg);
}

.social-stats-grid {
  display: flex;
  align-items: center;
  justify-content: space-around;
  gap: var(--spacing-md);
}

.social-stat {
  flex: 1;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.social-stat-icon {
  font-size: 2rem;
  margin-bottom: 0.25rem;
}

.social-stat-value {
  font-size: 2rem;
  font-weight: 900;
  color: var(--color-text-primary);
  text-shadow: 0 0 15px var(--color-accent-cyan);
}

.social-stat-label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  letter-spacing: 2px;
  font-weight: 600;
  text-transform: uppercase;
}

.social-stat-divider {
  width: 2px;
  height: 60px;
  background: var(--gradient-cyber);
  box-shadow: var(--shadow-glow-primary);
}

/* Stats Section */
.section-title {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: 2px;
  margin-bottom: var(--spacing-md);
  text-shadow: 0 0 10px var(--color-accent-cyan);
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-md);
}

.stat-card {
  background: rgba(17, 19, 24, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 229, 255, 0.3);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  position: relative;
  overflow: hidden;
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
}

.stat-cyan::before {
  background: var(--gradient-cyber);
}

.stat-red::before {
  background: var(--gradient-red);
}

.stat-gold::before {
  background: var(--gradient-gold);
}

.stat-icon {
  font-size: 1.5rem;
  margin-bottom: 0.5rem;
}

.coin-icon-profile {
  width: 40px;
  height: 40px;
  object-fit: contain;
  animation: coinSpin 3s linear infinite;
  filter: drop-shadow(0 0 8px rgba(255, 215, 0, 0.6));
}

@keyframes coinSpin {
  0% {
    transform: rotateY(0deg);
  }
  100% {
    transform: rotateY(360deg);
  }
}

.stat-value {
  font-size: 2rem;
  font-weight: 900;
  color: var(--color-text-primary);
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  letter-spacing: 2px;
  font-weight: 600;
}

.stat-bar {
  height: 2px;
  margin-top: var(--spacing-sm);
  border-radius: 1px;
}

.stat-cyan .stat-bar {
  background: var(--gradient-cyber);
  box-shadow: var(--shadow-cyan);
}

.stat-red .stat-bar {
  background: var(--gradient-red);
  box-shadow: var(--shadow-red);
}

.stat-gold .stat-bar {
  background: var(--gradient-gold);
  box-shadow: var(--shadow-gold);
}

/* Settings Section */
.setting-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md) 0;
  border-bottom: 1px solid rgba(0, 229, 255, 0.1);
}

.setting-item:last-child {
  border-bottom: none;
}

.setting-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  color: var(--color-text-primary);
  font-weight: 600;
}

.label-icon {
  font-size: 1.2rem;
}

.cyber-select {
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid rgba(0, 229, 255, 0.3);
  color: var(--color-text-primary);
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s;
}

.cyber-select:hover {
  background: rgba(0, 229, 255, 0.2);
  border-color: var(--color-accent-cyan);
  box-shadow: var(--shadow-cyan);
}

.setting-value {
  background: rgba(0, 229, 255, 0.1);
  padding: 0.75rem 1.5rem;
  border-radius: var(--radius-md);
  color: var(--color-accent-cyan);
  font-weight: 700;
}

/* Buttons */
.cyber-btn {
  position: relative;
  width: 100%;
  padding: 1.25rem 2rem;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 2px;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s;
}

.cyber-btn-danger {
  background: var(--gradient-red);
  color: var(--color-text-primary);
  box-shadow: var(--shadow-red);
}

.cyber-btn:hover {
  transform: translateY(-2px);
}

.cyber-btn-danger:hover {
  box-shadow: 0 0 30px rgba(255, 46, 46, 0.5);
}

.btn-text {
  position: relative;
  z-index: 1;
}

.btn-glitch {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(255, 255, 255, 0.1);
  opacity: 0;
  transition: opacity 0.3s;
}

.cyber-btn:hover .btn-glitch {
  opacity: 1;
}

/* Videos Section */
.videos-section {
  margin-top: var(--spacing-lg);
}

.section-title {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: 2px;
  margin-bottom: var(--spacing-md);
  text-shadow: 0 0 10px var(--color-accent-cyan);
}

.title-icon {
  font-size: 1.5rem;
}

.video-count {
  margin-left: auto;
  background: rgba(0, 229, 255, 0.2);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
  font-size: 0.85rem;
  color: var(--color-accent-cyan);
  font-weight: 700;
}

.videos-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-md);
}

.video-preview-card {
  background: rgba(17, 19, 24, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 229, 255, 0.2);
  border-radius: var(--radius-lg);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
}

.video-preview-card:hover {
  border-color: var(--color-accent-cyan);
  box-shadow: var(--shadow-cyan), 0 0 30px rgba(0, 229, 255, 0.3);
  transform: translateY(-4px);
}

.video-thumbnail {
  position: relative;
  width: 100%;
  height: 400px;
  background: #000;
  overflow: hidden;
}

.preview-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.play-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(0, 0, 0, 0.3);
  opacity: 0;
  transition: opacity 0.3s;
}

.video-preview-card:hover .play-overlay {
  opacity: 1;
}

.play-icon {
  font-size: 3rem;
  color: white;
  text-shadow: 0 0 20px rgba(0, 0, 0, 0.8);
}

.video-duration {
  position: absolute;
  bottom: 8px;
  right: 8px;
  background: rgba(0, 0, 0, 0.7);
  color: white;
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 600;
}

.video-info {
  padding: var(--spacing-md);
}

.video-description {
  color: var(--color-text-primary);
  font-weight: 600;
  margin-bottom: var(--spacing-sm);
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  line-height: 1.4;
}

.video-stats {
  display: flex;
  gap: var(--spacing-md);
  font-size: 0.8rem;
}

.video-stats .stat {
  color: var(--color-text-muted);
}

.empty-videos {
  text-align: center;
  padding: var(--spacing-3xl);
  color: var(--color-text-muted);
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
}

.empty-text {
  font-size: 1rem;
}

.back-section {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.back-btn-profile {
  background: rgba(17, 19, 24, 0.9);
  border: 1px solid rgba(0, 229, 255, 0.3);
  padding: 1rem 2rem;
  color: var(--color-accent-cyan);
  letter-spacing: 1px;
}

.back-btn-profile:hover {
  border-color: var(--color-accent-cyan);
  box-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
}

@media (max-width: 768px) {
  .social-stats-grid {
    gap: var(--spacing-sm);
  }

  .social-stat-value {
    font-size: 1.5rem;
  }

  .social-stat-icon {
    font-size: 1.5rem;
  }

  .social-stat-divider {
    height: 40px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .user-card {
    flex-direction: column;
    text-align: center;
  }

  .videos-grid {
    grid-template-columns: 1fr;
  }

  .video-thumbnail {
    height: 350px;
  }
}

/* Post Video Section */
.post-video-section {
  margin-top: 2rem;
}

/* Modal Overlay */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(5px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 1rem;
}

.modal-content {
  background: var(--color-bg-card);
  border: 2px solid var(--color-neon-cyan);
  border-radius: var(--radius-2xl);
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: 0 0 50px rgba(0, 245, 255, 0.3);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.5rem;
  border-bottom: 1px solid var(--color-border-primary);
}

.modal-header h2 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 900;
  background: var(--gradient-neon-cyan);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.close-btn {
  background: none;
  border: none;
  color: var(--color-text-primary);
  font-size: 2rem;
  cursor: pointer;
  line-height: 1;
  padding: 0;
  width: 32px;
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--radius-md);
  transition: all 0.3s;
}

.close-btn:hover {
  background: rgba(255, 107, 53, 0.2);
}

/* Post Video Form */
.post-video-form {
  padding: 1.5rem;
}

.form-group {
  margin-bottom: 1.5rem;
}

.form-label {
  display: block;
  margin-bottom: 0.5rem;
  color: var(--color-text-primary);
  font-weight: 700;
  font-size: 0.9rem;
  letter-spacing: 1px;
}

.cyber-input {
  width: 100%;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  padding: 0.75rem 1rem;
  color: var(--color-text-primary);
  font-size: 1rem;
  transition: all 0.3s;
  box-sizing: border-box;
}

.cyber-input:focus {
  outline: none;
  border-color: var(--color-neon-cyan);
  box-shadow: 0 0 10px rgba(0, 245, 255, 0.2);
}

.cyber-textarea {
  width: 100%;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  padding: 0.75rem 1rem;
  color: var(--color-text-primary);
  font-size: 1rem;
  font-family: inherit;
  resize: vertical;
  transition: all 0.3s;
  box-sizing: border-box;
}

.cyber-textarea:focus {
  outline: none;
  border-color: var(--color-neon-cyan);
  box-shadow: 0 0 10px rgba(0, 245, 255, 0.2);
}

.cyber-select {
  width: 100%;
  background: var(--color-bg-elevated);
  border: 1px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  padding: 0.75rem 1rem;
  color: var(--color-text-primary);
  font-size: 1rem;
  transition: all 0.3s;
  cursor: pointer;
}

.cyber-select:focus {
  outline: none;
  border-color: var(--color-neon-cyan);
  box-shadow: 0 0 10px rgba(0, 245, 255, 0.2);
}

.form-hint {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  margin-top: 0.25rem;
}

.form-actions {
  display: flex;
  gap: 1rem;
  margin-top: 2rem;
}

.form-actions .cyber-btn {
  flex: 1;
}
</style>
