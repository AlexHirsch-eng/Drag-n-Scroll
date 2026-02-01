<template>
  <div class="learn-view">
    <div class="bg-effects">
      <div class="grid-overlay"></div>
      <div class="ambient-glow"></div>
      <div class="floating-orbs">
        <div class="orb orb-1"></div>
        <div class="orb orb-2"></div>
        <div class="orb orb-3"></div>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="isLoading" class="loading">
      <div class="warm-loader"></div>
      <div class="loading-text">LOADING...</div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="error">
      <p class="error-text">{{ error }}</p>
      <button @click="loadMainScreen" class="retry-btn">RETRY</button>
    </div>

    <!-- Main Content -->
    <div v-else class="content">
      <!-- Header -->
      <div class="header">
        <div class="day-info">
          <div class="hsk-selector">
            <button @click="changeHSKLevel(-1)" class="hsk-nav-btn" :disabled="currentHSKLevel <= 1">−</button>
            <div class="hsk-badge">HSK {{ currentHSKLevel }}</div>
            <button @click="changeHSKLevel(1)" class="hsk-nav-btn" :disabled="currentHSKLevel >= 6">+</button>
          </div>
          <div class="day-selector">
            <button @click="changeDay(-1)" class="day-nav-btn" :disabled="currentDay <= 1">←</button>
            <div class="day-number">DAY {{ currentDay }}</div>
            <button @click="changeDay(1)" class="day-nav-btn" :disabled="currentDay >= 5">→</button>
          </div>
          <span class="day-title">{{ mainScreenData?.current_course_day.title }}</span>
        </div>
        <div class="stats-row">
          <div class="stat-badge stat-primary">
            <span class="icon">⚡</span>
            <span>{{ mainScreenData?.xp_total }}</span> XP
          </div>
          <div class="stat-badge stat-pink">
            <span class="icon">🔥</span>
            <span>{{ mainScreenData?.streak_days }}</span>
          </div>
          <div class="stat-badge stat-tertiary">
            <span class="icon">📚</span>
            <span>{{ mainScreenData?.total_learning_words }}</span>
          </div>
        </div>
      </div>

      <!-- Session Cards -->
      <div class="sessions-grid">
        <!-- Session A Card -->
        <div
          class="session-card"
          :class="{
            'completed': mainScreenData?.session_a?.is_completed,
            'in-progress': mainScreenData?.session_a && !mainScreenData.session_a.is_completed
          }"
          @click="startSession('A')"
        >
          <div class="card-glow"></div>
          <div class="session-header">
            <div class="session-label">SESSION A</div>
            <div v-if="mainScreenData?.session_a?.is_completed" class="status-badge completed">
              ✓ DONE
            </div>
            <div v-else-if="mainScreenData?.session_a" class="status-badge progress">
              IN PROGRESS
            </div>
            <div v-else class="status-badge new">
              NEW
            </div>
          </div>

          <div class="session-steps">
            <div
              v-for="step in steps"
              :key="step.id"
              class="step-indicator"
              :class="{ active: isStepActive('A', step.number), completed: isStepCompleted('A', step.number) }"
            >
              <span class="step-number">{{ step.number }}</span>
              <span class="step-label">{{ step.label }}</span>
              <span class="step-time">{{ step.time }}</span>
            </div>
          </div>

          <div v-if="mainScreenData?.session_a" class="session-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: getProgress('A') + '%' }"></div>
            </div>
            <div class="progress-text">{{ getProgress('A') }}% Complete</div>
          </div>

          <div class="start-btn">
            <span v-if="!mainScreenData?.session_a">START SESSION →</span>
            <span v-else-if="mainScreenData.session_a.is_completed">REPLAY SESSION →</span>
            <span v-else>CONTINUE →</span>
          </div>
        </div>

        <!-- Session B Card -->
        <div
          class="session-card"
          :class="{
            'completed': mainScreenData?.session_b?.is_completed,
            'in-progress': mainScreenData?.session_b && !mainScreenData.session_b.is_completed
          }"
          @click="startSession('B')"
        >
          <div class="card-glow"></div>
          <div class="session-header">
            <div class="session-label">SESSION B</div>
            <div v-if="mainScreenData?.session_b?.is_completed" class="status-badge completed">
              ✓ DONE
            </div>
            <div v-else-if="mainScreenData?.session_b" class="status-badge progress">
              IN PROGRESS
            </div>
            <div v-else class="status-badge new">
              NEW
            </div>
          </div>

          <div class="session-steps">
            <div
              v-for="step in steps"
              :key="step.id"
              class="step-indicator"
              :class="{ active: isStepActive('B', step.number), completed: isStepCompleted('B', step.number) }"
            >
              <span class="step-number">{{ step.number }}</span>
              <span class="step-label">{{ step.label }}</span>
              <span class="step-time">{{ step.time }}</span>
            </div>
          </div>

          <div v-if="mainScreenData?.session_b" class="session-progress">
            <div class="progress-bar">
              <div class="progress-fill" :style="{ width: getProgress('B') + '%' }"></div>
            </div>
            <div class="progress-text">{{ getProgress('B') }}% Complete</div>
          </div>

          <div class="start-btn">
            <span v-if="!mainScreenData?.session_b">START SESSION →</span>
            <span v-else-if="mainScreenData.session_b.is_completed">REPLAY SESSION →</span>
            <span v-else>CONTINUE →</span>
          </div>
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="quick-actions">
        <button @click="goToReview" class="action-btn action-purple">
          <span class="icon">🔄</span>
          <span>REVIEW ({{ mainScreenData?.due_for_review || 0 }})</span>
        </button>
        <button @click="goToVocab" class="action-btn action-pink">
          <span class="icon">📖</span>
          <span>VOCAB</span>
        </button>
        <button @click="goToProfile" class="action-btn action-tertiary">
          <span class="icon">👤</span>
          <span>PROFILE</span>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSessionStore } from '@/stores/session'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const sessionStore = useSessionStore()
const authStore = useAuthStore()

const isLoading = ref(true)
const error = ref('')
const currentDay = ref(1)

// Initialize HSK level from user profile (will be updated in onMounted)
const currentHSKLevel = ref(1)

const steps = [
  { id: 1, number: 1, label: 'SRS Review', time: '2 min' },
  { id: 2, number: 2, label: 'New Words', time: '8 min' },
  { id: 3, number: 3, label: 'Grammar', time: '2 min' },
  { id: 4, number: 4, label: 'Dialogue', time: '2 min' },
  { id: 5, number: 5, label: 'Practice', time: '1 min' },
]

const mainScreenData = computed(() => sessionStore.mainScreenData)

onMounted(async () => {
  // Initialize HSK level from user profile after auth is loaded
  if (authStore.user?.profile?.current_hsk_level) {
    currentHSKLevel.value = authStore.user.profile.current_hsk_level
  }
  await loadMainScreen()
})

async function loadMainScreen() {
  isLoading.value = true
  error.value = ''

  try {
    await sessionStore.loadMainScreen()
    // Update currentDay from loaded data (keep current HSK level as is)
    if (sessionStore.mainScreenData?.current_course_day) {
      currentDay.value = sessionStore.mainScreenData.current_course_day.day_number
    }
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load main screen'
  } finally {
    isLoading.value = false
  }
}

async function changeHSKLevel(delta: number) {
  const newLevel = currentHSKLevel.value + delta
  if (newLevel < 1 || newLevel > 6) return

  currentHSKLevel.value = newLevel
  currentDay.value = 1 // Reset to day 1 when changing HSK level

  // Load data for new HSK level and day
  isLoading.value = true
  error.value = ''

  try {
    await sessionStore.loadMainScreenForDay(1, newLevel)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load HSK level'
  } finally {
    isLoading.value = false
  }
}

async function changeDay(delta: number) {
  const newDay = currentDay.value + delta
  if (newDay < 1 || newDay > 5) return

  currentDay.value = newDay

  // Reload screen for the new day
  isLoading.value = true
  error.value = ''

  try {
    await sessionStore.loadMainScreenForDay(currentDay.value)
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to load day'
  } finally {
    isLoading.value = false
  }
}

async function startSession(type: 'A' | 'B') {
  if (!mainScreenData.value) return

  try {
    // Resume existing session or start new one
    const existingSession = type === 'A'
      ? mainScreenData.value.session_a
      : mainScreenData.value.session_b

    if (existingSession && !existingSession.is_completed) {
      // Resume existing session
      await sessionStore.resumeSession(existingSession.id)
    } else {
      // Start new session
      await sessionStore.startSession(mainScreenData.value.current_course_day.id, type)
    }

    // Navigate to session view
    router.push('/session')
  } catch (err: any) {
    error.value = err.response?.data?.detail || 'Failed to start session'
  }
}

function isStepActive(sessionType: 'A' | 'B', stepNumber: number): boolean {
  const session = sessionType === 'A'
    ? mainScreenData.value?.session_a
    : mainScreenData.value?.session_b
  return session?.current_step === stepNumber || false
}

function isStepCompleted(sessionType: 'A' | 'B', stepNumber: number): boolean {
  const session = sessionType === 'A'
    ? mainScreenData.value?.session_a
    : mainScreenData.value?.session_b
  if (!session) return false
  return session.is_completed || session.current_step > stepNumber
}

function getProgress(sessionType: 'A' | 'B'): number {
  const session = sessionType === 'A'
    ? mainScreenData.value?.session_a
    : mainScreenData.value?.session_b
  if (!session) return 0
  return Math.round((session.current_step / 6) * 100)
}

function goToReview() {
  router.push('/review')
}

function goToVocab() {
  router.push('/vocab')
}

function goToProfile() {
  router.push('/profile')
}
</script>

<style scoped>
.learn-view {
  min-height: 100vh;
  background: var(--color-bg-primary);
  padding: 2rem;
  position: relative;
  overflow-x: hidden;
}

.bg-effects {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  pointer-events: none;
}

.grid-overlay {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(255, 107, 53, 0.03) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255, 107, 53, 0.03) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 30s linear infinite;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

.ambient-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 800px;
  height: 800px;
  background: radial-gradient(circle, rgba(255, 107, 53, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  animation: glowPulse 10s ease-in-out infinite;
}

@keyframes glowPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.6; }
  50% { transform: translate(-50%, -50%) scale(1.3); opacity: 1; }
}

.floating-orbs {
  position: absolute;
  width: 100%;
  height: 100%;
}

.orb {
  position: absolute;
  border-radius: 50%;
  filter: blur(60px);
  animation: float 20s ease-in-out infinite;
}

.orb-1 {
  width: 400px;
  height: 400px;
  background: rgba(255, 107, 53, 0.2);
  top: 10%;
  left: 10%;
  animation-delay: 0s;
}

.orb-2 {
  width: 300px;
  height: 300px;
  background: rgba(157, 78, 221, 0.15);
  top: 60%;
  right: 10%;
  animation-delay: -7s;
}

.orb-3 {
  width: 250px;
  height: 250px;
  background: rgba(255, 117, 143, 0.15);
  bottom: 10%;
  left: 30%;
  animation-delay: -14s;
}

@keyframes float {
  0%, 100% { transform: translate(0, 0) scale(1); }
  25% { transform: translate(50px, -50px) scale(1.1); }
  50% { transform: translate(-30px, 30px) scale(0.9); }
  75% { transform: translate(-50px, -30px) scale(1.05); }
}

.loading,
.error {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 60vh;
  gap: 2rem;
}

.warm-loader {
  width: 60px;
  height: 60px;
  border: 3px solid transparent;
  border-top-color: var(--color-accent-primary);
  border-right-color: var(--color-accent-secondary);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  box-shadow: var(--shadow-primary);
}

.loading-text {
  color: var(--color-accent-primary);
  font-size: 0.9rem;
  letter-spacing: 2px;
  font-weight: 600;
  animation: flicker 1.5s infinite;
}

@keyframes spin {
  to { transform: rotate(360deg); }
}

@keyframes flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.error-text {
  color: var(--color-accent-pink);
  font-size: 1.1rem;
  font-weight: 600;
  letter-spacing: 1px;
}

.retry-btn {
  padding: 1rem 2rem;
  background: var(--gradient-primary);
  color: var(--color-text-primary);
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 2px;
  cursor: pointer;
  box-shadow: var(--shadow-primary);
  transition: all 0.3s;
}

.retry-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-primary), 0 0 30px rgba(255, 107, 53, 0.5);
}

.content {
  position: relative;
  z-index: 1;
  max-width: 1200px;
  margin: 0 auto;
}

.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: rgba(37, 29, 45, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 107, 53, 0.2);
  border-radius: var(--radius-xl);
  flex-wrap: wrap;
  gap: 1rem;
}

.day-info {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.hsk-selector {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  justify-content: center;
}

.hsk-nav-btn {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid var(--color-accent-primary);
  color: var(--color-accent-primary);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.hsk-nav-btn:hover:not(:disabled) {
  background: var(--color-accent-primary);
  color: var(--color-text-primary);
  transform: scale(1.1);
  box-shadow: var(--shadow-warm);
}

.hsk-nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.hsk-badge {
  background: var(--gradient-sunset);
  color: var(--color-text-primary);
  padding: 0.5rem 1.5rem;
  border-radius: var(--radius-lg);
  font-size: 1rem;
  font-weight: 900;
  letter-spacing: 2px;
  box-shadow: var(--shadow-warm);
  min-width: 100px;
  text-align: center;
}

.day-selector {
  display: flex;
  align-items: center;
  gap: 1rem;
}

.day-nav-btn {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: rgba(255, 107, 53, 0.1);
  border: 1px solid var(--color-accent-primary);
  color: var(--color-accent-primary);
  font-size: 1.2rem;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s;
}

.day-nav-btn:hover:not(:disabled) {
  background: var(--color-accent-primary);
  color: var(--color-text-primary);
  transform: scale(1.1);
}

.day-nav-btn:disabled {
  opacity: 0.3;
  cursor: not-allowed;
}

.day-number {
  font-size: 0.9rem;
  color: var(--color-accent-primary);
  font-weight: 700;
  letter-spacing: 2px;
  min-width: 80px;
  text-align: center;
}

.day-title {
  font-size: 1.5rem;
  color: var(--color-text-primary);
  font-weight: 700;
  letter-spacing: 1px;
}

.stats-row {
  display: flex;
  gap: 1rem;
}

.stat-badge {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-weight: 700;
  font-size: 0.9rem;
}

.stat-primary {
  background: rgba(255, 107, 53, 0.15);
  border: 1px solid var(--color-accent-primary);
  color: var(--color-accent-primary);
}

.stat-pink {
  background: rgba(255, 117, 143, 0.15);
  border: 1px solid var(--color-accent-pink);
  color: var(--color-accent-pink);
}

.stat-tertiary {
  background: rgba(255, 230, 109, 0.15);
  border: 1px solid var(--color-accent-tertiary);
  color: var(--color-accent-tertiary);
}

.sessions-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(350px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.session-card {
  background: rgba(37, 29, 45, 0.9);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 107, 53, 0.2);
  border-radius: var(--radius-xl);
  padding: 2rem;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  position: relative;
  overflow: hidden;
}

.session-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradient-primary);
}

.session-card:hover {
  border-color: var(--color-accent-primary);
  transform: translateY(-6px);
  box-shadow: var(--shadow-card), var(--shadow-primary);
}

.session-card.completed {
  border-color: var(--color-accent-tertiary);
}

.session-card.completed::before {
  background: var(--gradient-secondary);
}

.session-card.in-progress {
  border-color: rgba(255, 107, 53, 0.4);
}

.card-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: var(--gradient-primary);
  border-radius: inherit;
  z-index: -1;
  opacity: 0;
  filter: blur(20px);
  transition: opacity 0.3s;
}

.session-card:hover .card-glow {
  opacity: 0.2;
}

.session-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
}

.session-label {
  font-size: 1.5rem;
  font-weight: 900;
  color: var(--color-text-primary);
  letter-spacing: 2px;
}

.status-badge {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm);
  font-size: 0.75rem;
  font-weight: 900;
  letter-spacing: 1px;
}

.status-badge.new {
  background: var(--gradient-primary);
  color: var(--color-text-primary);
}

.status-badge.progress {
  background: rgba(255, 107, 53, 0.2);
  border: 1px solid var(--color-accent-primary);
  color: var(--color-accent-primary);
}

.status-badge.completed {
  background: var(--gradient-secondary);
  color: var(--color-bg-primary);
}

.session-steps {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  margin-bottom: 2rem;
}

.step-indicator {
  display: grid;
  grid-template-columns: 30px 1fr 60px;
  gap: 1rem;
  align-items: center;
  padding: 0.75rem;
  border-radius: var(--radius-md);
  border: 1px solid rgba(255, 255, 255, 0.08);
  transition: all 0.3s;
}

.step-indicator.active {
  background: rgba(255, 107, 53, 0.15);
  border-color: var(--color-accent-primary);
}

.step-indicator.completed {
  background: rgba(6, 214, 160, 0.08);
  border-color: rgba(6, 214, 160, 0.3);
}

.step-number {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.75rem;
  font-weight: 700;
  color: var(--color-text-muted);
}

.step-indicator.completed .step-number {
  background: var(--gradient-success);
  color: var(--color-bg-primary);
}

.step-indicator.active .step-number {
  background: var(--gradient-primary);
  color: var(--color-text-primary);
  animation: pulse 2s ease-in-out infinite;
}

.step-label {
  font-size: 0.9rem;
  color: var(--color-text-secondary);
  font-weight: 500;
}

.step-indicator.active .step-label {
  color: var(--color-text-primary);
  font-weight: 600;
}

.step-time {
  font-size: 0.75rem;
  color: var(--color-text-muted);
  text-align: right;
}

.session-progress {
  margin-bottom: 1.5rem;
}

.progress-bar {
  height: 4px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-fill {
  height: 100%;
  background: var(--gradient-primary);
  transition: width 0.5s ease;
}

.session-card.completed .progress-fill {
  background: var(--gradient-secondary);
}

.progress-text {
  font-size: 0.8rem;
  color: var(--color-text-muted);
  text-align: right;
}

.start-btn {
  background: var(--gradient-primary);
  color: var(--color-text-primary);
  padding: 1rem 2rem;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 1px;
  text-align: center;
  transition: all 0.3s;
}

.session-card.completed .start-btn {
  background: var(--gradient-secondary);
  color: var(--color-bg-primary);
}

.session-card:hover .start-btn {
  transform: translateY(-2px);
  box-shadow: 0 0 20px rgba(255, 107, 53, 0.5);
}

.quick-actions {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.action-btn {
  background: rgba(37, 29, 45, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 107, 53, 0.15);
  border-radius: var(--radius-lg);
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all 0.3s;
}

.action-btn:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-card);
}

.action-purple:hover {
  background: rgba(157, 78, 221, 0.15);
  border-color: var(--color-accent-purple);
  box-shadow: var(--shadow-purple);
}

.action-pink:hover {
  background: rgba(255, 117, 143, 0.15);
  border-color: var(--color-accent-pink);
  box-shadow: var(--shadow-pink);
}

.action-tertiary:hover {
  background: rgba(255, 230, 109, 0.15);
  border-color: var(--color-accent-tertiary);
  box-shadow: var(--shadow-warm);
}

.action-btn .icon {
  font-size: 2rem;
}

.action-btn span:last-child {
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 1px;
}

@keyframes pulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.7; }
}
</style>
