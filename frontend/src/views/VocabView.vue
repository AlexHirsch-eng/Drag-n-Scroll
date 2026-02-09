<template>
  <div class="vocab-view">
    <!-- Background Effects -->
    <div class="bg-effects">
      <div class="circuit-grid"></div>
      <div class="glow-orb orb-1"></div>
      <div class="glow-orb orb-2"></div>
    </div>

    <!-- Content -->
    <div class="content">
      <!-- Header -->
      <div class="section-header">
        <h1 class="cyber-title">
          <span class="title-icon">📚</span>
          СЛОВАРЬ
        </h1>
        <div class="tech-line"></div>
      </div>

      <!-- Loading State -->
      <div v-if="isLoading" class="loading-state">
        <div class="cyber-loader"></div>
        <div class="loading-text">ЗАГРУЗКА СЛОВ...</div>
      </div>

      <!-- Filters & Words -->
      <div v-else class="vocab-container">
        <!-- Filters -->
        <div class="cyber-card filters-card">
          <div class="card-glow"></div>
          <div class="filters-grid">
            <div class="filter-group">
              <label class="filter-label">
                <span class="label-icon">📊</span>
                Уровень HSK
              </label>
              <select v-model="filters.hsk_level" @change="loadWords" class="cyber-select">
                <option :value="undefined">Все уровни</option>
                <option v-for="level in 6" :key="level" :value="level">HSK {{ level }}</option>
              </select>
            </div>

            <div class="filter-group">
              <label class="filter-label">
                <span class="label-icon">🎯</span>
                Статус
              </label>
              <select v-model="filters.status" @change="loadWords" class="cyber-select">
                <option :value="undefined">Все слова</option>
                <option value="new">Новые</option>
                <option value="learning">Изучаются</option>
                <option value="mastered">Освоены</option>
              </select>
            </div>
          </div>

          <div class="words-counter">
            <span class="counter-value">{{ words.length }}</span>
            <span class="counter-label">СЛОВ</span>
          </div>
        </div>

        <!-- Words List -->
        <div v-if="words.length > 0" class="words-grid">
          <div
            v-for="item in words"
            :key="item.word.id"
            class="word-card"
            :class="getCardClass(item.progress.srs_level)"
          >
            <div class="card-glow"></div>
            <div class="word-header">
              <div class="hanzi clickable-word" @click="speakWord(item.word.hanzi)" title="Нажмите для озвучки">
                {{ item.word.hanzi }}
              </div>
              <div class="srs-badge">L{{ item.progress.srs_level }}</div>
            </div>
            <div class="pinyin clickable-word" @click="speakWord(item.word.hanzi)" title="Нажмите для озвучки">
              {{ item.word.pinyin }}
            </div>
            <div class="translation">
              <div class="ru">{{ item.word.translation_ru }}</div>
              <div class="kz">{{ item.word.translation_kz }}</div>
            </div>
            <div class="word-stats">
              <div class="stat">
                <span class="stat-icon">✓</span>
                <span class="stat-value">{{ Math.round(item.progress.accuracy * 100) }}%</span>
              </div>
              <div class="stat">
                <span class="stat-icon">🔄</span>
                <span class="stat-value">{{ item.progress.total_reviews }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Empty State -->
        <div v-else class="empty-state">
          <div class="empty-icon">📭</div>
          <h3 class="empty-title">Слова не найдены</h3>
          <p class="empty-text">Попробуйте изменить фильтры или начните обучение для добавления слов</p>
          <router-link to="/learn" class="cyber-btn cyber-btn-primary">
            <span class="btn-text">НАЧАТЬ ОБУЧЕНИЕ</span>
            <span class="btn-glitch"></span>
          </router-link>
        </div>
      </div>

      <!-- Back Button -->
      <div class="back-section">
        <button @click="goBack" class="back-btn">
          <span class="icon">←</span>
          <span>НАЗАД ДОМОЙ</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { vocabAPI } from '@/api/vocab'
import type { WordWithProgress } from '@/types/api'
import { speakChinese } from '@/utils/speech'

const router = useRouter()

const isLoading = ref(true)
const words = ref<WordWithProgress[]>([])

const filters = ref({
  hsk_level: undefined as number | undefined,
  status: undefined as 'new' | 'learning' | 'mastered' | undefined,
})

onMounted(async () => {
  await loadWords()
})

async function loadWords() {
  isLoading.value = true

  try {
    const data = await vocabAPI.getMyWords({
      hsk_level: filters.value.hsk_level,
      status: filters.value.status,
    })
    words.value = data.results
  } catch (error) {
    console.error('Failed to load words:', error)
  } finally {
    isLoading.value = false
  }
}

function getCardClass(srsLevel: number) {
  if (srsLevel >= 5) return 'card-mastered'
  if (srsLevel >= 2) return 'card-learning'
  return 'card-new'
}

function goBack() {
  router.push('/app')
}

function speakWord(hanzi: string) {
  speakChinese(hanzi)
}
</script>

<style scoped>
.vocab-view {
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
  background: var(--color-accent-gold);
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
  max-width: 1200px;
  margin: 0 auto;
}

/* Section Header */
.section-header {
  text-align: center;
  margin-bottom: var(--spacing-lg);
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

/* Loading State */
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

/* Vocab Container */
.vocab-container {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
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

/* Filters */
.filters-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: var(--spacing-md);
  margin-bottom: var(--spacing-md);
}

.filter-group {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-sm);
}

.filter-label {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  color: var(--color-text-primary);
  font-weight: 600;
  font-size: 0.9rem;
  letter-spacing: 1px;
}

.label-icon {
  font-size: 1.2rem;
}

.cyber-select {
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid rgba(0, 229, 255, 0.3);
  color: var(--color-text-primary);
  padding: 0.75rem 1rem;
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

.words-counter {
  text-align: center;
  padding-top: var(--spacing-md);
  border-top: 1px solid rgba(0, 229, 255, 0.1);
}

.counter-value {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--color-accent-cyan);
  text-shadow: 0 0 20px var(--color-accent-cyan);
}

.counter-label {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  letter-spacing: 2px;
  font-weight: 600;
}

/* Words Grid */
.words-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-md);
}

.word-card {
  background: rgba(17, 19, 24, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 229, 255, 0.3);
  border-radius: var(--radius-md);
  padding: var(--spacing-md);
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
  cursor: pointer;
}

.word-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-cyber);
  opacity: 0.5;
}

.word-card:hover {
  transform: translateY(-4px);
  border-color: var(--color-accent-cyan);
  box-shadow: var(--shadow-cyan);
}

.word-card.card-new::before {
  background: var(--gradient-cyber);
}

.word-card.card-learning::before {
  background: var(--gradient-gold);
}

.word-card.card-mastered::before {
  background: var(--gradient-red);
}

.word-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: var(--spacing-sm);
}

.hanzi {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--color-text-primary);
  line-height: 1;
}

.clickable-word {
  cursor: pointer;
  transition: all 0.3s;
  padding: 0.3rem 0.5rem;
  border-radius: var(--radius-md);
  display: inline-block;
}

.clickable-word:hover {
  color: var(--color-accent-cyan);
  text-shadow: 0 0 15px var(--color-accent-cyan);
  transform: scale(1.05);
}

.srs-badge {
  background: rgba(0, 229, 255, 0.2);
  border: 1px solid var(--color-accent-cyan);
  padding: 0.25rem 0.5rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--color-accent-cyan);
  letter-spacing: 1px;
}

.pinyin {
  font-size: 1.1rem;
  color: var(--color-text-secondary);
  margin-bottom: var(--spacing-sm);
}

.translation {
  margin-bottom: var(--spacing-md);
}

.translation .ru {
  color: var(--color-text-primary);
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.translation .kz {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.word-stats {
  display: flex;
  gap: var(--spacing-md);
  padding-top: var(--spacing-sm);
  border-top: 1px solid rgba(0, 229, 255, 0.1);
}

.stat {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 0.85rem;
}

.stat-icon {
  color: var(--color-accent-cyan);
}

.stat-value {
  color: var(--color-text-secondary);
  font-weight: 700;
}

/* Empty State */
.empty-state {
  text-align: center;
  padding: var(--spacing-xl) var(--spacing-lg);
}

.empty-icon {
  font-size: 5rem;
  margin-bottom: var(--spacing-md);
  opacity: 0.5;
}

.empty-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: var(--color-text-primary);
  margin-bottom: var(--spacing-sm);
}

.empty-text {
  color: var(--color-text-muted);
  margin-bottom: var(--spacing-lg);
}

.cyber-btn {
  display: inline-block;
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

.back-section {
  display: flex;
  justify-content: center;
  margin-top: 2rem;
}

.back-btn {
  background: rgba(17, 19, 24, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 229, 255, 0.3);
  border-radius: var(--radius-lg);
  padding: 1rem 3rem;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  color: var(--color-accent-cyan);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.back-btn:hover {
  transform: translateY(-4px);
  background: rgba(0, 229, 255, 0.1);
  border-color: var(--color-accent-cyan);
  box-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
}

.back-btn .icon {
  font-size: 1.5rem;
}

@media (max-width: 768px) {
  .words-grid {
    grid-template-columns: 1fr;
  }

  .filters-grid {
    grid-template-columns: 1fr;
  }
}
</style>
