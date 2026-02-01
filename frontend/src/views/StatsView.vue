<template>
  <div class="stats-view">
    <!-- Neon Background Effects -->
    <div class="bg-effects">
      <div class="grid-lines"></div>
      <div class="scanlines"></div>
    </div>

    <!-- Header -->
    <div class="header">
      <h1 class="title text-gradient-rainbow">STATISTICS</h1>
      <div class="title-line"></div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading-container">
      <div class="spinner-neon"></div>
      <p class="loading-text text-glow-cyan">LOADING DATA...</p>
    </div>

    <!-- Stats Content -->
    <div v-else-if="stats" class="stats-container">
      <!-- Overview Card -->
      <div class="neon-card stat-card-overview">
        <div class="card-glow"></div>
        <h3 class="card-title">
          <span class="icon">📊</span>
          <span class="title-text text-gradient-cyan">OVERVIEW</span>
        </h3>

        <div class="stats-grid">
          <div class="stat-item stat-pink">
            <div class="stat-value text-glow-pink">{{ stats.total_words }}</div>
            <div class="stat-label">TOTAL WORDS</div>
            <div class="stat-bar">
              <div class="stat-bar-fill" style="width: 100%"></div>
            </div>
          </div>

          <div class="stat-item stat-cyan">
            <div class="stat-value text-glow-cyan">{{ Math.round(stats.retention_rate * 100) }}%</div>
            <div class="stat-label">RETENTION RATE</div>
            <div class="stat-bar">
              <div class="stat-bar-fill" :style="{ width: (stats.retention_rate * 100) + '%' }"></div>
            </div>
          </div>

          <div class="stat-item stat-yellow">
            <div class="stat-value text-glow-yellow">{{ stats.avg_reviews_per_word }}</div>
            <div class="stat-label">AVG REVIEWS</div>
            <div class="stat-bar">
              <div class="stat-bar-fill" :style="{ width: Math.min(stats.avg_reviews_per_word * 20, 100) + '%' }"></div>
            </div>
          </div>

          <div class="stat-item stat-purple">
            <div class="stat-value text-glow-purple">{{ stats.streak_days }}</div>
            <div class="stat-label">DAY STREAK</div>
            <div class="stat-bar">
              <div class="stat-bar-fill" :style="{ width: Math.min(stats.streak_days * 5, 100) + '%' }"></div>
            </div>
          </div>
        </div>
      </div>

      <!-- SRS Levels Card -->
      <div class="neon-card stat-card-srs">
        <div class="card-glow"></div>
        <h3 class="card-title">
          <span class="icon">🧠</span>
          <span class="title-text text-gradient-purple">SRS LEVELS</span>
        </h3>

        <div class="level-bars">
          <div
            v-for="(count, level) in stats.by_srs_level"
            :key="level"
            class="level-bar"
          >
            <span class="level-label">LEVEL {{ level }}</span>
            <div class="bar-container">
              <div
                class="bar-fill"
                :style="{ width: getPercentage(count, stats.total_words) + '%' }"
              >
                <div class="bar-shine"></div>
              </div>
            </div>
            <span class="level-count text-glow-cyan">{{ count }}</span>
          </div>
        </div>
      </div>

      <!-- Upcoming Reviews Card -->
      <div class="neon-card stat-card-upcoming">
        <div class="card-glow"></div>
        <h3 class="card-title">
          <span class="icon">📅</span>
          <span class="title-text text-gradient-pink">UPCOMING REVIEWS</span>
        </h3>

        <div class="upcoming-list">
          <div
            v-for="item in stats.upcoming_reviews"
            :key="item.date"
            class="upcoming-item"
          >
            <div class="date-badge">
              <span class="date-icon">📆</span>
              <span class="date-text">{{ formatDate(item.date) }}</span>
            </div>
            <div class="count-badge glow-cyan">
              <span class="count-value">{{ item.count }}</span>
              <span class="count-label">WORDS</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useSRSStore } from '@/stores/srs'
import type { SRSStatsResponse } from '@/types/api'

const srsStore = useSRSStore()

const isLoading = ref(true)
const stats = ref<SRSStatsResponse | null>(null)

onMounted(async () => {
  await loadStats()
})

async function loadStats() {
  isLoading.value = true

  try {
    stats.value = await srsStore.loadStats()
  } catch (error) {
    console.error('Failed to load stats:', error)
  } finally {
    isLoading.value = false
  }
}

function getPercentage(count: number, total: number) {
  return total > 0 ? (count / total) * 100 : 0
}

function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  const today = new Date()
  const tomorrow = new Date(today)
  tomorrow.setDate(tomorrow.getDate() + 1)

  if (date.toDateString() === today.toDateString()) {
    return 'Today'
  } else if (date.toDateString() === tomorrow.toDateString()) {
    return 'Tomorrow'
  } else {
    return date.toLocaleDateString('en-US', { weekday: 'short', month: 'short', day: 'numeric' })
  }
}
</script>

<style scoped>
.stats-view {
  min-height: 100vh;
  padding: var(--spacing-2xl);
  background: var(--color-bg-primary);
  position: relative;
  overflow: hidden;
}

/* ============================================
   BACKGROUND EFFECTS
   ============================================ */

.bg-effects {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  pointer-events: none;
}

.grid-lines {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(var(--color-neon-cyan-light) 1px, transparent 1px),
    linear-gradient(90deg, var(--color-neon-cyan-light) 1px, transparent 1px);
  background-size: 60px 60px;
  animation: gridMove 30s linear infinite;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(60px, 60px); }
}

.scanlines {
  position: absolute;
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.05) 0px,
    rgba(0, 0, 0, 0.05) 1px,
    transparent 1px,
    transparent 4px
  );
  opacity: 0.3;
}

/* ============================================
   HEADER
   ============================================ */

.header {
  text-align: center;
  margin-bottom: var(--spacing-3xl);
  position: relative;
  z-index: 1;
}

.title {
  font-size: var(--font-size-5xl);
  font-weight: 900;
  letter-spacing: 6px;
  text-transform: uppercase;
  margin: 0 0 var(--spacing-lg) 0;
}

.title-line {
  width: 200px;
  height: 4px;
  background: var(--gradient-neon-cyber);
  margin: 0 auto;
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-glow-cyan);
  animation: borderGlow 6s ease-in-out infinite;
}

/* ============================================
   LOADING STATE
   ============================================ */

.loading-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 50vh;
  gap: var(--spacing-xl);
  position: relative;
  z-index: 1;
}

.spinner-neon {
  width: 80px;
  height: 80px;
  border: 4px solid transparent;
  border-top-color: var(--color-neon-cyan);
  border-right-color: var(--color-neon-pink);
  border-radius: 50%;
  animation: spinNeon 1s linear infinite;
  box-shadow:
    0 0 20px var(--color-neon-cyan-glow),
    0 0 40px var(--color-neon-pink-glow);
}

@keyframes spinNeon {
  to {
    transform: rotate(360deg);
  }
}

.loading-text {
  font-size: var(--font-size-lg);
  font-weight: 700;
  letter-spacing: 3px;
  animation: neonPulse 2s ease-in-out infinite;
}

/* ============================================
   STATS CONTAINER
   ============================================ */

.stats-container {
  position: relative;
  z-index: 1;
  max-width: 1000px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: var(--spacing-2xl);
}

/* ============================================
   NEON CARDS
   ============================================ */

.neon-card {
  position: relative;
  background: var(--color-bg-card);
  backdrop-filter: blur(20px);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-2xl);
  padding: var(--spacing-2xl);
  overflow: hidden;
  transition: all var(--transition-slow);
}

.neon-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: var(--gradient-neon-cyber);
  animation: rotateGradient 15s linear infinite;
  opacity: 0;
  transition: opacity var(--transition-slow);
  z-index: -1;
}

@keyframes rotateGradient {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.neon-card:hover {
  border-color: var(--color-neon-cyan);
  box-shadow:
    var(--shadow-card),
    var(--shadow-glow-cyan),
    inset 0 0 30px rgba(0, 245, 255, 0.1);
  transform: translateY(-4px);
}

.neon-card:hover::before {
  opacity: 0.1;
}

.card-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: var(--gradient-neon-rainbow);
  border-radius: var(--radius-2xl);
  z-index: -2;
  opacity: 0;
  filter: blur(20px);
  transition: opacity var(--transition-slow);
  animation: rainbowFlow 3s linear infinite;
}

.neon-card:hover .card-glow {
  opacity: 0.2;
}

.card-title {
  display: flex;
  align-items: center;
  gap: 1rem;
  margin: 0 0 var(--spacing-xl) 0;
  font-size: var(--font-size-2xl);
  letter-spacing: 4px;
}

.card-title .icon {
  font-size: 2.5rem;
  animation: neonPulse 2s ease-in-out infinite;
}

.title-text {
  font-weight: 900;
}

/* ============================================
   OVERVIEW STATS
   ============================================ */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: var(--spacing-lg);
}

.stat-item {
  background: var(--color-bg-elevated);
  border: 2px solid;
  padding: var(--spacing-xl);
  border-radius: var(--radius-lg);
  text-align: center;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.stat-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}

.stat-pink {
  border-color: var(--color-neon-pink);
}

.stat-pink::before {
  background: var(--gradient-pink);
}

.stat-pink:hover {
  box-shadow: var(--shadow-glow-pink);
  transform: translateY(-4px);
}

.stat-cyan {
  border-color: var(--color-neon-cyan);
}

.stat-cyan::before {
  background: var(--gradient-cyan);
}

.stat-cyan:hover {
  box-shadow: var(--shadow-glow-cyan);
  transform: translateY(-4px);
}

.stat-yellow {
  border-color: var(--color-neon-yellow);
}

.stat-yellow::before {
  background: var(--gradient-yellow);
}

.stat-yellow:hover {
  box-shadow: var(--shadow-glow-yellow);
  transform: translateY(-4px);
}

.stat-purple {
  border-color: var(--color-neon-purple);
}

.stat-purple::before {
  background: var(--gradient-purple);
}

.stat-purple:hover {
  box-shadow: var(--shadow-glow-purple);
  transform: translateY(-4px);
}

.stat-value {
  font-size: var(--font-size-4xl);
  font-weight: 900;
  margin-bottom: var(--spacing-sm);
  display: block;
}

.stat-label {
  font-size: var(--font-size-xs);
  letter-spacing: 2px;
  color: var(--color-text-muted);
  font-weight: 700;
  text-transform: uppercase;
}

.stat-bar {
  height: 4px;
  background: var(--color-bg-hover);
  margin-top: var(--spacing-md);
  border-radius: var(--radius-full);
  overflow: hidden;
  position: relative;
}

.stat-bar-fill {
  height: 100%;
  background: var(--gradient-neon-cyber);
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow: 0 0 10px var(--color-neon-cyan-glow);
}

/* ============================================
   SRS LEVELS
   ============================================ */

.level-bars {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-lg);
}

.level-bar {
  display: grid;
  grid-template-columns: 100px 1fr 60px;
  align-items: center;
  gap: var(--spacing-lg);
  padding: var(--spacing-md);
  background: var(--color-bg-elevated);
  border-radius: var(--radius-md);
  transition: all var(--transition-base);
}

.level-bar:hover {
  background: var(--color-bg-hover);
  transform: translateX(4px);
}

.level-label {
  font-size: var(--font-size-sm);
  color: var(--color-text-secondary);
  font-weight: 700;
  letter-spacing: 1px;
}

.bar-container {
  height: 24px;
  background: var(--color-bg-hover);
  border-radius: var(--radius-sm);
  overflow: hidden;
  position: relative;
  border: 1px solid var(--color-border-primary);
}

.bar-fill {
  position: relative;
  height: 100%;
  background: var(--gradient-neon-ocean);
  transition: width 1s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow:
    0 0 15px var(--color-neon-cyan-glow),
    inset 0 0 10px rgba(0, 245, 255, 0.3);
}

.bar-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.3),
    transparent
  );
  animation: shimmer 2s infinite;
}

.level-count {
  font-size: var(--font-size-sm);
  font-weight: 900;
  text-align: right;
}

/* ============================================
   UPCOMING REVIEWS
   ============================================ */

.upcoming-list {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.upcoming-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--spacing-lg);
  background: var(--color-bg-elevated);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  transition: all var(--transition-base);
}

.upcoming-item:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-neon-cyan);
  box-shadow: var(--shadow-glow-cyan);
  transform: translateX(4px);
}

.date-badge {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
}

.date-icon {
  font-size: 1.5rem;
}

.date-text {
  font-weight: 700;
  color: var(--color-text-primary);
  letter-spacing: 1px;
}

.count-badge {
  display: flex;
  align-items: center;
  gap: var(--spacing-sm);
  padding: var(--spacing-sm) var(--spacing-lg);
  background: var(--color-bg-primary);
  border: 2px solid var(--color-neon-cyan);
  border-radius: var(--radius-full);
  transition: all var(--transition-base);
}

.upcoming-item:hover .count-badge {
  background: var(--color-neon-cyan);
}

.count-value {
  font-size: var(--font-size-lg);
  font-weight: 900;
  color: var(--color-neon-cyan);
}

.upcoming-item:hover .count-value {
  color: var(--color-bg-primary);
}

.count-label {
  font-size: var(--font-size-xs);
  color: var(--color-text-muted);
  font-weight: 700;
  letter-spacing: 1px;
}

.upcoming-item:hover .count-label {
  color: var(--color-bg-primary);
}

/* ============================================
   RESPONSIVE DESIGN
   ============================================ */

@media (max-width: 768px) {
  .stats-view {
    padding: var(--spacing-lg);
  }

  .title {
    font-size: var(--font-size-3xl);
    letter-spacing: 4px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .level-bar {
    grid-template-columns: 1fr;
    gap: var(--spacing-sm);
  }

  .bar-container {
    height: 20px;
  }

  .upcoming-item {
    flex-direction: column;
    gap: var(--spacing-md);
    align-items: flex-start;
  }

  .count-badge {
    align-self: flex-end;
  }
}

@media (max-width: 480px) {
  .stats-view {
    padding: var(--spacing-md);
  }

  .neon-card {
    padding: var(--spacing-lg);
  }

  .title {
    font-size: var(--font-size-2xl);
    letter-spacing: 2px;
  }

  .stat-value {
    font-size: var(--font-size-3xl);
  }
}
</style>
