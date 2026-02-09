<template>
  <div class="review-view">
    <!-- Background Effects -->
    <div class="bg-effects">
      <div class="circuit-grid"></div>
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>
    </div>

    <!-- Top Back Button -->
    <div class="top-back-section">
      <button @click="goBack" class="top-back-btn">
        <span class="icon">←</span>
        <span>ГЛАВНОЕ МЕНЮ</span>
      </button>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-state">
      <div class="cyber-loader"></div>
      <div class="loading-text">ЗАГРУЗКА ОШИБОК...</div>
    </div>

    <!-- Empty State -->
    <div v-else-if="!currentBatch || currentBatch.words.length === 0" class="empty-state">
      <div class="empty-icon">📚</div>
      <h2 class="empty-title">ПОКА НЕТ ОШИБОК!</h2>
      <p class="empty-text">Отличная работа! Продолжайте учиться, чтобы накапливать ошибки</p>
      <router-link to="/learn" class="cyber-btn cyber-btn-primary">
        <span class="btn-text">НАЗАД К ОБУЧЕНИЮ</span>
        <span class="btn-glitch"></span>
      </router-link>
    </div>

    <!-- Review Card -->
    <SwipeContainer
      v-else
      :current-index="reviewIndex"
      :total="currentBatch.words.length"
      hint="СВАЙП ВВЕРХ ДЛЯ СЛЕДУЮЩЕЙ КАРТОЧКИ"
      @next="nextCard"
      @previous="previousCard"
    >
      <template #default>
        <div class="review-container">
          <!-- Progress Header -->
          <div class="progress-header">
            <div class="progress-info">
              <span class="current">{{ reviewIndex + 1 }}</span>
              <span class="divider">/</span>
              <span class="total">{{ currentBatch.words.length }}</span>
            </div>
            <div class="batch-badge">ПАРТИЯ {{ currentBatch.batch_number }}</div>
          </div>

          <!-- Word Card -->
          <div class="word-card" :class="{ revealed: isRevealed }">
            <div class="card-glow"></div>

            <!-- Chinese Character -->
            <div class="hanzi-section">
              <div class="hanzi clickable-word" @click="speakHanzi" title="Нажмите для озвучки">
                {{ currentCard?.hanzi }}
              </div>
              <div v-if="isRevealed" class="pinyin clickable-word" @click="speakHanzi" title="Нажмите для озвучки">
                {{ currentCard?.pinyin }}
              </div>
            </div>

            <!-- Translation (revealed) -->
            <div v-if="isRevealed" class="translation-section">
              <div class="translation ru">{{ currentCard?.translation_ru }}</div>
              <div class="translation kz">{{ currentCard?.translation_kz }}</div>
            </div>

            <!-- Action Buttons -->
            <button
              v-if="!isRevealed"
              @click="reveal"
              class="cyber-btn cyber-btn-large reveal-btn"
            >
              <span class="btn-text">НАЖМИТЕ ЧТОБЫ УВИДЕТЬ</span>
              <span class="btn-glitch"></span>
            </button>

            <!-- Rating Buttons (revealed) -->
            <div v-else class="rating-section">
              <button @click="rate(0)" class="rate-btn rate-again">
                <span class="rate-icon">❌</span>
                <span class="rate-label">СНОВА</span>
                <span class="rate-value">0</span>
              </button>
              <button @click="rate(3)" class="rate-btn rate-hard">
                <span class="rate-icon">💪</span>
                <span class="rate-label">СЛОЖНО</span>
                <span class="rate-value">3</span>
              </button>
              <button @click="rate(4)" class="rate-btn rate-good">
                <span class="rate-icon">👍</span>
                <span class="rate-label">ХОРОШО</span>
                <span class="rate-value">4</span>
              </button>
              <button @click="rate(5)" class="rate-btn rate-easy">
                <span class="rate-icon">⚡</span>
                <span class="rate-label">ЛЕГКО</span>
                <span class="rate-value">5</span>
              </button>
            </div>

            <!-- Card Footer -->
            <div class="card-footer">
              <button
                @click="playAudio"
                class="audio-btn"
                title="Прослушать произношение"
              >
                🔊
              </button>
              <div class="word-stats">
                <span class="stat">Level {{ currentCard?.srs_level }}</span>
                <span class="divider">•</span>
                <span class="stat">{{ currentCard?.total_reviews }} reviews</span>
                <span v-if="currentCard?.accuracy !== undefined" class="divider">•</span>
                <span v-if="currentCard?.accuracy !== undefined" class="stat accuracy" :class="getAccuracyClass(currentCard.accuracy)">
                  {{ Math.round(currentCard.accuracy * 100) }}% accuracy
                </span>
              </div>
            </div>
          </div>
        </div>
      </template>
    </SwipeContainer>

    <!-- Back Button -->
    <div class="back-section">
      <button @click="goBack" class="back-btn neon-button-home">
        <span class="icon">←</span>
        <span>НАЗАД В ГЛАВНОЕ МЕНЮ</span>
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSRSStore } from '@/stores/srs'
import SwipeContainer from '@/components/layout/SwipeContainer.vue'
import { speakChinese } from '@/utils/speech'

const router = useRouter()
const srsStore = useSRSStore()

const isLoading = ref(true)
const isRevealed = ref(false)
const reviews = ref<Array<{ word_id: number; quality: number; time_spent_seconds: number }>>([])

const currentBatch = computed(() => srsStore.currentBatch)
const reviewIndex = computed(() => srsStore.currentReviewIndex)
const currentCard = computed(() => srsStore.getCurrentCard())

onMounted(async () => {
  await loadBatch()
})

async function loadBatch() {
  isLoading.value = true
  try {
    await srsStore.loadMistakesBatch({ batch_size: 20 })
  } catch (error) {
    console.error('Failed to load mistakes batch:', error)
  } finally {
    isLoading.value = false
  }
}

function reveal() {
  isRevealed.value = true
}

async function rate(quality: number) {
  if (!currentCard.value) return

  reviews.value.push({
    word_id: currentCard.value.id,
    quality,
    time_spent_seconds: 5,
  })

  isRevealed.value = false

  if (reviewIndex.value < (currentBatch.value?.words.length || 0) - 1) {
    srsStore.nextCard()
  } else {
    await submitBatch()
  }
}

async function submitBatch() {
  if (!currentBatch.value || reviews.value.length === 0) return

  try {
    await srsStore.submitReview({
      batch_id: currentBatch.value.batch_id,
      reviews: reviews.value,
    })

    reviews.value = []
    await loadBatch()
  } catch (error) {
    console.error('Failed to submit review:', error)
  }
}

function nextCard() {
  srsStore.nextCard()
  isRevealed.value = false
}

function previousCard() {
  srsStore.previousCard()
  isRevealed.value = false
}

function playAudio() {
  if (currentCard.value?.hanzi) {
    speakChinese(currentCard.value.hanzi)
  }
}

function speakHanzi() {
  if (currentCard.value?.hanzi) {
    speakChinese(currentCard.value.hanzi)
  }
}

function getAccuracyClass(accuracy: number) {
  if (accuracy < 0.4) return 'accuracy-poor'
  if (accuracy < 0.7) return 'accuracy-medium'
  return 'accuracy-good'
}

function goBack() {
  router.push('/app')
}
</script>

<style scoped>
.review-view {
  height: 100vh;
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

/* Top Back Button */
.top-back-section {
  position: absolute;
  top: var(--spacing-lg);
  left: var(--spacing-lg);
  z-index: 10;
}

.top-back-btn {
  background: rgba(0, 0, 0, 0.7);
  backdrop-filter: blur(10px);
  border: 2px solid var(--color-accent-cyan);
  border-radius: var(--radius-md);
  padding: 0.8rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-accent-cyan);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-transform: uppercase;
  box-shadow: 0 0 15px rgba(0, 229, 255, 0.3);
}

.top-back-btn:hover {
  background: var(--gradient-cyber);
  color: var(--color-bg-primary);
  box-shadow: 0 0 25px rgba(0, 229, 255, 0.6);
  transform: translateX(-5px);
}

.top-back-btn .icon {
  font-size: 1.2rem;
}

/* Loading & Empty States */
.loading-state,
.empty-state {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  height: 100vh;
  text-align: center;
  padding: var(--spacing-lg);
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

.empty-icon {
  font-size: 5rem;
  margin-bottom: var(--spacing-md);
}

.empty-title {
  font-size: 2rem;
  font-weight: 900;
  color: var(--color-text-primary);
  letter-spacing: 3px;
  text-shadow: 0 0 20px var(--color-accent-cyan);
  margin-bottom: var(--spacing-sm);
}

.empty-text {
  color: var(--color-text-muted);
  margin-bottom: var(--spacing-lg);
  font-size: 1.1rem;
}

.cyber-btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: var(--radius-md);
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 2px;
  cursor: pointer;
  text-decoration: none;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
  display: inline-block;
}

.cyber-btn-primary {
  background: var(--gradient-cyber);
  color: var(--color-text-primary);
  box-shadow: var(--shadow-cyan);
}

.cyber-btn:hover {
  transform: translateY(-2px);
}

.cyber-btn-primary:hover {
  box-shadow: 0 0 30px rgba(0, 229, 255, 0.5);
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

/* Review Container */
.review-container {
  position: relative;
  z-index: 1;
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: var(--spacing-lg);
}

/* Progress Header */
.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-md);
  background: rgba(17, 19, 24, 0.8);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 229, 255, 0.2);
  border-radius: var(--radius-md);
  margin-bottom: var(--spacing-md);
}

.progress-info {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.2rem;
  font-weight: 700;
}

.current {
  color: var(--color-accent-cyan);
  font-size: 1.5rem;
}

.divider {
  color: var(--color-text-muted);
}

.total {
  color: var(--color-text-secondary);
}

.batch-badge {
  background: rgba(0, 229, 255, 0.2);
  border: 1px solid var(--color-accent-cyan);
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--color-accent-cyan);
  letter-spacing: 1px;
}

/* Word Card */
.word-card {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: rgba(17, 19, 24, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 229, 255, 0.3);
  border-radius: var(--radius-xl);
  padding: var(--spacing-xl);
  position: relative;
  overflow: hidden;
  transition: all 0.5s ease;
}

.card-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradient-cyber);
  box-shadow: var(--shadow-cyan);
}

.word-card.revealed {
  border-color: var(--color-accent-cyan);
  box-shadow: var(--shadow-cyan);
}

.hanzi-section {
  text-align: center;
  margin-bottom: var(--spacing-xl);
}

.hanzi {
  font-size: 6rem;
  font-weight: 900;
  color: var(--color-text-primary);
  line-height: 1;
  margin-bottom: var(--spacing-md);
  text-shadow: 0 0 30px rgba(0, 229, 255, 0.3);
}

.pinyin {
  font-size: 2rem;
  color: var(--color-text-secondary);
  letter-spacing: 2px;
}

.clickable-word {
  cursor: pointer;
  transition: all 0.3s;
  border-radius: var(--radius-md);
  padding: 0.5rem;
}

.clickable-word:hover {
  color: var(--color-accent-cyan);
  text-shadow: 0 0 20px var(--color-accent-cyan);
  transform: scale(1.05);
}

.translation-section {
  text-align: center;
  margin-bottom: var(--spacing-xl);
  animation: fadeInUp 0.5s ease;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.translation {
  font-size: 1.3rem;
  margin: var(--spacing-sm) 0;
}

.translation.ru {
  color: var(--color-text-primary);
  font-weight: 600;
}

.translation.kz {
  color: var(--color-text-muted);
  font-size: 1.1rem;
}

/* Buttons */
.cyber-btn-large {
  padding: 1.5rem 4rem;
  font-size: 1.1rem;
  min-width: 300px;
}

.reveal-btn {
  background: rgba(0, 229, 255, 0.1);
  border: 2px solid var(--color-accent-cyan);
  color: var(--color-accent-cyan);
  box-shadow: var(--shadow-cyan);
}

.reveal-btn:hover {
  background: var(--gradient-cyber);
  color: var(--color-text-primary);
}

/* Rating Section */
.rating-section {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--spacing-md);
  width: 100%;
  max-width: 600px;
  animation: fadeInUp 0.5s ease;
}

.rate-btn {
  background: rgba(17, 19, 24, 0.9);
  border: 2px solid;
  padding: var(--spacing-md) var(--spacing-sm);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.rate-btn:hover {
  transform: translateY(-4px);
}

.rate-again {
  border-color: var(--color-accent-red);
  color: var(--color-accent-red);
}

.rate-again:hover {
  background: var(--color-accent-red);
  box-shadow: var(--shadow-red);
}

.rate-hard {
  border-color: var(--color-accent-gold);
  color: var(--color-accent-gold);
}

.rate-hard:hover {
  background: var(--color-accent-gold);
  box-shadow: var(--shadow-gold);
}

.rate-good {
  border-color: #4caf50;
  color: #4caf50;
}

.rate-good:hover {
  background: #4caf50;
  box-shadow: 0 0 20px rgba(76, 175, 80, 0.5);
}

.rate-easy {
  border-color: var(--color-accent-cyan);
  color: var(--color-accent-cyan);
}

.rate-easy:hover {
  background: var(--gradient-cyber);
  box-shadow: var(--shadow-cyan);
}

.rate-icon {
  font-size: 1.5rem;
}

.rate-label {
  font-size: 0.75rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.rate-value {
  font-size: 1.5rem;
  font-weight: 900;
}

/* Card Footer */
.card-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-md);
  width: 100%;
}

.audio-btn {
  width: 60px;
  height: 60px;
  border: none;
  background: var(--gradient-cyber);
  color: var(--color-text-primary);
  border-radius: 50%;
  font-size: 1.8rem;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: var(--shadow-cyan);
}

.audio-btn:hover {
  transform: scale(1.1);
  box-shadow: 0 0 30px rgba(0, 229, 255, 0.5);
}

.word-stats {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.9rem;
  color: var(--color-text-muted);
}

.stat {
  font-weight: 600;
}

.accuracy {
  font-weight: 700;
}

.accuracy-poor {
  color: #ff4757;
  text-shadow: 0 0 10px rgba(255, 71, 87, 0.5);
}

.accuracy-medium {
  color: #ffa502;
  text-shadow: 0 0 10px rgba(255, 165, 2, 0.5);
}

.accuracy-good {
  color: #2ed573;
  text-shadow: 0 0 10px rgba(46, 213, 115, 0.5);
}

.back-section {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.back-btn {
  background: rgba(17, 19, 24, 0.9);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(0, 212, 255, 0.5);
  border-radius: var(--radius-lg);
  padding: 1.2rem 3rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--color-accent-primary);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
}

.back-btn:hover {
  transform: translateY(-4px);
  background: var(--gradient-cyber);
  color: var(--color-bg-primary);
  border-color: var(--color-accent-cyan);
  box-shadow: 0 0 30px rgba(0, 229, 255, 0.6);
}

.back-btn .icon {
  font-size: 1.5rem;
}

@media (max-width: 768px) {
  .top-back-section {
    top: var(--spacing-md);
    left: var(--spacing-md);
  }

  .top-back-btn {
    padding: 0.6rem 1rem;
    font-size: 0.75rem;
  }

  .top-back-btn .icon {
    font-size: 1rem;
  }

  .rating-section {
    grid-template-columns: repeat(2, 1fr);
  }

  .hanzi {
    font-size: 4rem;
  }

  .pinyin {
    font-size: 1.5rem;
  }
}
</style>
