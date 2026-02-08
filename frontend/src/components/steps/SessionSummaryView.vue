<template>
  <div class="session-summary-view">
    <div class="summary-overlay" @click="$emit('close')"></div>

    <div class="summary-card">
      <div class="summary-header">
        <div class="icon">🎉</div>
        <h2>СЕССИЯ ЗАВЕРШЕНА!</h2>
        <p class="session-type">СЕССИЯ {{ summary?.session.session_type }}</p>
      </div>

      <div class="summary-stats">
        <div class="stat-item">
          <div class="stat-icon">📖</div>
          <div class="stat-content">
            <div class="stat-value">{{ summaryData?.words_learned }}</div>
            <div class="stat-label">Выучено слов</div>
          </div>
        </div>

        <div class="stat-item">
          <div class="stat-icon">🎯</div>
          <div class="stat-content">
            <div class="stat-value">{{ summaryData?.accuracy_percentage }}</div>
            <div class="stat-label">Точность</div>
          </div>
        </div>

        <div class="stat-item">
          <div class="stat-icon">
            <img src="/src/images/coin.png" alt="coin" class="coin-icon-summary">
          </div>
          <div class="stat-content">
            <div class="stat-value">{{ summaryData?.xp_earned }}</div>
            <div class="stat-label">Заработано СКРОЛЛОВ</div>
          </div>
        </div>

        <div class="stat-item">
          <div class="stat-icon">⏱️</div>
          <div class="stat-content">
            <div class="stat-value">{{ summaryData?.time_spent_minutes }}m</div>
            <div class="stat-label">Затрачено времени</div>
          </div>
        </div>
      </div>

      <!-- Problematic Words -->
      <div v-if="summaryData && summaryData.problematic_words_count > 0" class="problematic-section">
        <h4>Слова для повторения ({{ summaryData.problematic_words_count }})</h4>
        <div class="problematic-words">
          <div
            v-for="word in summaryData.problematic_words"
            :key="word.id"
            class="problematic-word"
          >
            <span class="hanzi">{{ word.hanzi }}</span>
            <span class="pinyin">{{ word.pinyin }}</span>
            <span class="translation">{{ word.translation_ru }}</span>
          </div>
        </div>
      </div>

      <!-- Day Completion -->
      <div v-if="summaryData?.is_day_completed" class="day-complete-banner">
        <div class="banner-icon">🏆</div>
        <div class="banner-text">
          <h3>ДЕНЬ ЗАВЕРШЁН!</h3>
          <p>Обе сессии A и B завершены</p>
        </div>
      </div>

      <div class="summary-actions">
        <button @click="$emit('close')" class="action-btn primary">
          НАЗАД К ОБУЧЕНИЮ
        </button>
        <button v-if="!summary?.is_day_completed" @click="startOtherSession" class="action-btn secondary">
          НАЧАТЬ {{ otherSessionType }} →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  session: any
  summary?: any
}>()

defineEmits(['close', 'start-other'])

const summaryData = computed(() => {
  // Use passed summary if available, otherwise compute from session
  if (props.summary) {
    return props.summary
  }

  if (!props.session) return null

  return {
    session: props.session,
    words_learned: props.session.words_learned || 0,
    accuracy_percentage: props.session.accuracy_percentage || '0%',
    problematic_words_count: (props.session.problematic_words || []).length,
    problematic_words: (props.summary?.problematic_words || props.session.problematic_words || []).map((word: any) => {
      if (typeof word === 'object') return word
      return {
        id: word,
        hanzi: `Word ${word}`,
        pinyin: 'pinyin',
        translation_ru: 'translation'
      }
    }),
    time_spent_minutes: Math.round(props.session.total_time_minutes || 0),
    xp_earned: props.session.xp_earned || 0,
    is_day_completed: props.summary?.is_day_completed || false,
    course_day_id: props.summary?.session?.course_day
  }
})

const otherSessionType = computed(() => {
  return props.session?.session_type === 'A' ? 'СЕССИЮ B' : 'СЕССИЮ A'
})

function startOtherSession() {
  // Emit event to start the other session
  // @ts-ignore
  props.summary?.session?.course_day
  // @ts-ignore
}
</script>

<style scoped>
.session-summary-view {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 1000;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
}

.summary-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  backdrop-filter: blur(10px);
}

.summary-card {
  position: relative;
  background: rgba(17, 19, 24, 0.98);
  border: 2px solid var(--color-accent-cyan);
  border-radius: var(--radius-xl);
  padding: 3rem 2rem;
  max-width: 600px;
  width: 100%;
  max-height: 90vh;
  overflow-y: auto;
  box-shadow: var(--shadow-card), var(--shadow-cyan);
  animation: slideUp 0.5s ease;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(50px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.summary-header {
  text-align: center;
  margin-bottom: 3rem;
}

.summary-header .icon {
  font-size: 4rem;
  margin-bottom: 1rem;
  animation: bounce 1s ease;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}

.summary-header h2 {
  color: var(--color-accent-cyan);
  font-size: 2rem;
  font-weight: 900;
  letter-spacing: 2px;
  margin: 0 0 0.5rem 0;
  text-shadow: 0 0 20px var(--color-accent-cyan);
}

.session-type {
  color: var(--color-text-muted);
  font-size: 1rem;
  font-weight: 600;
  letter-spacing: 1px;
  margin: 0;
}

.summary-stats {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-bottom: 3rem;
}

.stat-item {
  background: rgba(0, 229, 255, 0.05);
  border: 1px solid rgba(0, 229, 255, 0.2);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1rem;
  transition: all 0.3s;
}

.stat-item:hover {
  background: rgba(0, 229, 255, 0.1);
  border-color: var(--color-accent-cyan);
  transform: translateY(-2px);
  box-shadow: var(--shadow-cyan);
}

.stat-icon {
  font-size: 2.5rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

.coin-icon-summary {
  width: 50px;
  height: 50px;
  object-fit: contain;
  animation: coinPulse 2s ease-in-out infinite;
  filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.8));
}

@keyframes coinPulse {
  0%, 100% {
    transform: scale(1);
  }
  50% {
    transform: scale(1.15);
  }
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 2rem;
  font-weight: 900;
  color: var(--color-text-primary);
  line-height: 1;
  margin-bottom: 0.25rem;
}

.stat-label {
  font-size: 0.85rem;
  color: var(--color-text-muted);
  font-weight: 600;
  letter-spacing: 1px;
}

.problematic-section {
  background: rgba(255, 46, 46, 0.05);
  border: 1px solid rgba(255, 46, 46, 0.3);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  margin-bottom: 2rem;
}

.problematic-section h4 {
  color: var(--color-accent-red);
  margin: 0 0 1rem 0;
  font-size: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.problematic-words {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.problematic-word {
  background: rgba(0, 0, 0, 0.3);
  border-radius: var(--radius-md);
  padding: 0.75rem 1rem;
  display: flex;
  align-items: center;
  gap: 1rem;
}

.problematic-word .hanzi {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--color-text-primary);
}

.problematic-word .pinyin {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
}

.problematic-word .translation {
  margin-left: auto;
  font-size: 0.85rem;
  color: var(--color-text-muted);
}

.day-complete-banner {
  background: linear-gradient(135deg, rgba(245, 197, 66, 0.2) 0%, rgba(245, 197, 66, 0.1) 100%);
  border: 2px solid var(--color-accent-gold);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  align-items: center;
  gap: 1.5rem;
  margin-bottom: 2rem;
  animation: pulse 2s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { box-shadow: 0 0 0 0 rgba(245, 197, 66, 0.4); }
  50% { box-shadow: 0 0 20px 0 rgba(245, 197, 66, 0.2); }
}

.banner-icon {
  font-size: 3rem;
}

.banner-text h3 {
  color: var(--color-accent-gold);
  font-size: 1.3rem;
  font-weight: 900;
  letter-spacing: 1px;
  margin: 0 0 0.25rem 0;
  text-shadow: 0 0 10px var(--color-accent-gold);
}

.banner-text p {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin: 0;
}

.summary-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.action-btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 1px;
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn.primary {
  background: var(--gradient-cyber);
  color: var(--color-bg-primary);
  box-shadow: var(--shadow-cyan);
}

.action-btn.secondary {
  background: transparent;
  border: 2px solid var(--color-accent-cyan);
  color: var(--color-accent-cyan);
}

.action-btn:hover {
  transform: translateY(-2px);
}

.action-btn.primary:hover {
  box-shadow: var(--shadow-cyan), 0 0 20px rgba(0, 229, 255, 0.5);
}

.action-btn.secondary:hover {
  background: rgba(0, 229, 255, 0.1);
  box-shadow: var(--shadow-cyan);
}
</style>
