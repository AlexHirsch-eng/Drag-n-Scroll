<template>
  <div class="swipe-container" ref="container">
    <!-- Neon Progress Bar -->
    <div class="progress-bar">
      <div class="progress-glow"></div>
      <div class="progress-fill" :style="{ width: progress + '%' }">
        <div class="progress-shine"></div>
      </div>
    </div>

    <!-- Neon Header -->
    <div class="header">
      <button @click="previous" :disabled="currentIndex === 0" class="nav-btn nav-btn-left">
        <span class="btn-arrow">◄</span>
      </button>

      <div class="progress-indicator">
        <span class="current text-gradient-cyan">{{ currentIndex + 1 }}</span>
        <span class="divider text-glow-pink">/</span>
        <span class="total">{{ total }}</span>
      </div>

      <button @click="next" :disabled="currentIndex >= total - 1" class="nav-btn nav-btn-right">
        <span class="btn-arrow">►</span>
      </button>
    </div>

    <div class="cards-wrapper" ref="wrapper">
      <slot :current-index="currentIndex"></slot>
    </div>

    <!-- Neon Swipe Hint -->
    <div class="swipe-hint" v-if="showHint">
      <div class="hint-icon">⬆</div>
      <div class="hint-text">{{ hint }}</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'

const props = defineProps<{
  currentIndex: number
  total: number
  hint?: string
}>()

const emit = defineEmits<{
  (e: 'next'): void
  (e: 'previous'): void
}>()

const container = ref<HTMLElement>()
const wrapper = ref<HTMLElement>()
const showHint = ref(true)

const progress = computed(() => ((props.currentIndex + 1) / props.total) * 100)

function next() {
  emit('next')
}

function previous() {
  emit('previous')
}

// Handle keyboard navigation
function handleKeydown(e: KeyboardEvent) {
  if (e.key === 'ArrowDown' || e.key === 'ArrowRight') {
    next()
  } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
    previous()
  }
}

// Handle swipe gestures
let touchStartY = 0
let touchStartX = 0

function handleTouchStart(e: TouchEvent) {
  touchStartY = e.touches[0].clientY
  touchStartX = e.touches[0].clientX
  showHint.value = false
}

function handleTouchEnd(e: TouchEvent) {
  const touchEndY = e.changedTouches[0].clientY
  const touchEndX = e.changedTouches[0].clientX

  const deltaY = touchStartY - touchEndY
  const deltaX = touchStartX - touchEndX

  const minSwipeDistance = 50

  // Vertical swipe (primary)
  if (Math.abs(deltaY) > Math.abs(deltaX)) {
    if (deltaY > minSwipeDistance) {
      next()
    } else if (deltaY < -minSwipeDistance) {
      previous()
    }
  }
  // Horizontal swipe (secondary)
  else {
    if (deltaX > minSwipeDistance) {
      next()
    } else if (deltaX < -minSwipeDistance) {
      previous()
    }
  }
}

// Handle wheel events
let wheelTimeout: NodeJS.Timeout | null = null
function handleWheel(e: WheelEvent) {
  if (wheelTimeout) return

  const minWheelDelta = 50

  if (e.deltaY < -minWheelDelta) {
    previous()
  } else if (e.deltaY > minWheelDelta) {
    next()
  }

  wheelTimeout = setTimeout(() => {
    wheelTimeout = null
  }, 500)
}

onMounted(() => {
  window.addEventListener('keydown', handleKeydown)
  if (container.value) {
    container.value.addEventListener('touchstart', handleTouchStart)
    container.value.addEventListener('touchend', handleTouchEnd)
    container.value.addEventListener('wheel', handleWheel, { passive: true })
  }
})

onUnmounted(() => {
  window.removeEventListener('keydown', handleKeydown)
  if (container.value) {
    container.value.removeEventListener('touchstart', handleTouchStart)
    container.value.removeEventListener('touchend', handleTouchEnd)
    container.value.removeEventListener('wheel', handleWheel)
  }
})
</script>

<style scoped>
.swipe-container {
  position: relative;
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  background: var(--color-bg-primary);
}

/* ============================================
   NEON PROGRESS BAR
   ============================================ */

.progress-bar {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 6px;
  background: var(--color-bg-secondary);
  z-index: var(--z-sticky);
  overflow: hidden;
}

.progress-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--gradient-neon-cyber);
  opacity: 0.1;
  filter: blur(10px);
  animation: rainbowFlow 3s linear infinite;
}

.progress-fill {
  position: relative;
  height: 100%;
  background: var(--gradient-neon-cyber);
  transition: width 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  box-shadow:
    0 0 20px var(--color-neon-cyan-glow),
    0 0 40px var(--color-neon-pink-glow);
}

.progress-shine {
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.4),
    transparent
  );
  animation: progressShine 2s infinite;
}

@keyframes progressShine {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

/* ============================================
   NEON HEADER
   ============================================ */

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 1.25rem 1.5rem;
  background: var(--color-bg-card);
  backdrop-filter: blur(20px);
  border-bottom: 2px solid var(--color-border-primary);
  position: relative;
  z-index: var(--z-fixed);
}

.header::before {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-neon-cyber);
  animation: rainbowFlow 3s linear infinite;
}

.nav-btn {
  width: 50px;
  height: 50px;
  border: 2px solid var(--color-neon-cyan);
  background: transparent;
  border-radius: var(--radius-full);
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.nav-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--gradient-cyan);
  opacity: 0;
  transition: opacity var(--transition-base);
}

.nav-btn:hover:not(:disabled)::before {
  opacity: 0.2;
}

.nav-btn:hover:not(:disabled) {
  border-color: var(--color-neon-cyan);
  box-shadow: var(--shadow-glow-cyan);
  transform: scale(1.1);
}

.nav-btn:active:not(:disabled) {
  transform: scale(0.95);
}

.nav-btn:disabled {
  opacity: 0.2;
  cursor: not-allowed;
  border-color: var(--color-border-muted);
}

.btn-arrow {
  font-size: 1.5rem;
  color: var(--color-neon-cyan);
  font-weight: 900;
  position: relative;
  z-index: 1;
  transition: all var(--transition-base);
}

.nav-btn:hover:not(:disabled) .btn-arrow {
  color: var(--color-neon-cyan);
  text-shadow: 0 0 10px var(--color-neon-cyan);
}

/* ============================================
   PROGRESS INDICATOR
   ============================================ */

.progress-indicator {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.5rem;
  font-weight: 900;
  letter-spacing: 2px;
}

.current {
  font-size: 2rem;
}

.divider {
  font-size: 1.5rem;
  animation: neonPulse 2s ease-in-out infinite;
}

.total {
  color: var(--color-text-muted);
  font-size: 1.2rem;
}

/* ============================================
   CARDS WRAPPER
   ============================================ */

.cards-wrapper {
  flex: 1;
  overflow: hidden;
  position: relative;
}

/* ============================================
   NEON SWIPE HINT
   ============================================ */

.swipe-hint {
  position: absolute;
  bottom: 3rem;
  left: 50%;
  transform: translateX(-50%);
  background: var(--color-bg-card);
  backdrop-filter: blur(20px);
  border: 2px solid var(--color-neon-pink);
  padding: 1rem 2rem;
  border-radius: var(--radius-full);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
  pointer-events: none;
  animation: hintPulse 3s ease-in-out;
  z-index: var(--z-fixed);
  box-shadow:
    var(--shadow-glow-pink),
    inset 0 0 20px rgba(255, 0, 110, 0.1);
}

.swipe-hint::before {
  content: '';
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: var(--gradient-pink);
  border-radius: var(--radius-full);
  z-index: -1;
  opacity: 0.3;
  filter: blur(10px);
  animation: neonPulse 2s ease-in-out infinite;
}

.hint-icon {
  font-size: 2rem;
  color: var(--color-neon-pink);
  animation: bounce 1s ease-in-out infinite;
}

@keyframes bounce {
  0%, 100% {
    transform: translateY(0);
  }
  50% {
    transform: translateY(-10px);
  }
}

.hint-text {
  color: var(--color-text-secondary);
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
}

@keyframes hintPulse {
  0%, 100% {
    opacity: 0;
    transform: translateX(-50%) translateY(20px);
  }
  20%, 80% {
    opacity: 1;
    transform: translateX(-50%) translateY(0);
  }
}

/* ============================================
   RESPONSIVE DESIGN
   ============================================ */

@media (max-width: 768px) {
  .header {
    padding: 1rem;
  }

  .nav-btn {
    width: 45px;
    height: 45px;
  }

  .btn-arrow {
    font-size: 1.2rem;
  }

  .progress-indicator {
    font-size: 1.2rem;
  }

  .current {
    font-size: 1.5rem;
  }

  .swipe-hint {
    bottom: 2rem;
    padding: 0.75rem 1.5rem;
  }

  .hint-icon {
    font-size: 1.5rem;
  }

  .hint-text {
    font-size: 0.75rem;
  }
}

@media (max-width: 480px) {
  .header {
    padding: 0.75rem;
  }

  .nav-btn {
    width: 40px;
    height: 40px;
  }

  .btn-arrow {
    font-size: 1rem;
  }

  .progress-indicator {
    gap: 0.25rem;
  }

  .current {
    font-size: 1.2rem;
  }

  .divider {
    font-size: 1rem;
  }

  .total {
    font-size: 0.9rem;
  }
}
</style>
