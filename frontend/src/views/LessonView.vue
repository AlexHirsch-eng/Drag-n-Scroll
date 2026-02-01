<template>
  <div class="lesson-view">
    <!-- Progress bar -->
    <div class="progress-header">
      <div class="progress-track">
        <div class="progress-bar" :style="{ width: progress + '%' }"></div>
      </div>
      <div class="progress-info">
        <span class="current">{{ currentIndex + 1 }}</span>
        <span class="divider">/</span>
        <span class="total">{{ totalSteps }}</span>
      </div>
    </div>

    <!-- Cards Container -->
    <div class="cards-container" ref="container">
      <transition :name="transitionName" mode="out-in">
        <component
          :is="currentComponent"
          v-if="currentStep"
          :key="currentIndex"
          :step="currentStep"
          @answer="handleAnswer"
          @continue="goNext"
        />
      </transition>
    </div>

    <!-- Loading -->
    <div v-if="isLoading" class="loading-overlay">
      <div class="cyber-loader"></div>
      <div class="loading-text">LOADING...</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import VocabIntroCard from '@/components/cards/VocabIntroCard.vue'
import VocabRecognizeCard from '@/components/cards/VocabRecognizeCard.vue'
import BuildPhraseCard from '@/components/cards/BuildPhraseCard.vue'
import GrammarIntroCard from '@/components/cards/GrammarIntroCard.vue'
import SRSReviewCard from '@/components/cards/SRSReviewCard.vue'
import type { LessonStep } from '@/types/api'

const router = useRouter()

const isLoading = ref(true)
const currentIndex = ref(0)
const transitionName = ref('slide-up')
const container = ref<HTMLElement>()

const steps = ref<LessonStep[]>([])
const currentStep = computed(() => steps.value[currentIndex.value])
const totalSteps = computed(() => steps.value.length)
const progress = computed(() => ((currentIndex.value + 1) / totalSteps.value) * 100)

const currentComponent = computed(() => {
  if (!currentStep.value) return null

  const stepType = currentStep.value.step_type
  switch (stepType) {
    case 'VOCAB_INTRO':
      return VocabIntroCard
    case 'VOCAB_RECOGNIZE':
      return VocabRecognizeCard
    case 'BUILD_PHRASE':
      return BuildPhraseCard
    case 'GRAMMAR_INTRO':
      return GrammarIntroCard
    case 'SRS_REVIEW':
      return SRSReviewCard
    default:
      return VocabIntroCard
  }
})

onMounted(async () => {
  await loadLesson()
  setupKeyboardNavigation()
  setupTouchGestures()
})

async function loadLesson() {
  isLoading.value = true
  try {
    // LessonView is currently not fully implemented
    // Redirecting to learn page for now
    console.warn('LessonView is not fully implemented yet')
    router.push('/learn')
  } catch (error) {
    console.error('Failed to load lesson:', error)
    router.push('/learn')
  } finally {
    isLoading.value = false
  }
}

function handleAnswer(_data: any) {
  // LessonView not fully implemented
  setTimeout(() => {
    goNext()
  }, 1200)
}

function goNext() {
  if (currentIndex.value < totalSteps.value - 1) {
    transitionName.value = 'slide-up'
    currentIndex.value++
  } else {
    finishLesson()
  }
}

function goPrev() {
  if (currentIndex.value > 0) {
    transitionName.value = 'slide-down'
    currentIndex.value--
  }
}

async function finishLesson() {
  // TODO: Implement lesson completion
  router.push('/learn')
}

function setupKeyboardNavigation() {
  const handleKeydown = (e: KeyboardEvent) => {
    if (e.key === 'ArrowDown' || e.key === 'ArrowRight' || e.key === ' ') {
      e.preventDefault()
      goNext()
    } else if (e.key === 'ArrowUp' || e.key === 'ArrowLeft') {
      e.preventDefault()
      goPrev()
    }
  }
  window.addEventListener('keydown', handleKeydown)
}

let touchStartY = 0
let touchStartX = 0

function setupTouchGestures() {
  if (!container.value) return

  container.value.addEventListener('touchstart', (e: TouchEvent) => {
    touchStartY = e.touches[0].clientY
    touchStartX = e.touches[0].clientX
  })

  container.value.addEventListener('touchend', (e: TouchEvent) => {
    const touchEndY = e.changedTouches[0].clientY
    const touchEndX = e.changedTouches[0].clientX

    const deltaY = touchStartY - touchEndY
    const deltaX = touchStartX - touchEndX

    const minSwipeDistance = 50

    if (Math.abs(deltaY) > Math.abs(deltaX)) {
      if (deltaY > minSwipeDistance) {
        goNext()
      } else if (deltaY < -minSwipeDistance) {
        goPrev()
      }
    }
  })
}
</script>

<style scoped>
.lesson-view {
  height: 100vh;
  width: 100vw;
  background: var(--color-bg-primary);
  overflow: hidden;
  position: relative;
}

.progress-header {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 100;
  background: rgba(13, 15, 24, 0.9);
  backdrop-filter: blur(10px);
  border-bottom: 1px solid rgba(0, 229, 255, 0.2);
  padding: 1rem;
}

.progress-track {
  height: 2px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 1px;
  overflow: hidden;
  margin-bottom: 0.5rem;
}

.progress-bar {
  height: 100%;
  background: var(--gradient-cyber);
  box-shadow: 0 0 10px var(--color-accent-cyan);
  transition: width 0.3s ease;
}

.progress-info {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 0.8rem;
  color: var(--color-accent-cyan);
  font-weight: 600;
  letter-spacing: 2px;
}

.progress-info .current {
  font-size: 1rem;
  color: var(--color-text-primary);
}

.progress-info .divider {
  opacity: 0.5;
}

.cards-container {
  height: 100%;
  width: 100%;
  overflow: hidden;
  position: relative;
}

.loading-overlay {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.9);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  z-index: 200;
}

.cyber-loader {
  width: 60px;
  height: 60px;
  border: 3px solid transparent;
  border-top-color: var(--color-accent-cyan);
  border-radius: 50%;
  animation: spin 1s linear infinite;
  box-shadow: 0 0 20px var(--color-accent-cyan);
}

.loading-text {
  margin-top: 1rem;
  color: var(--color-accent-cyan);
  font-size: 0.9rem;
  letter-spacing: 2px;
  font-weight: 600;
  animation: flicker 1.5s infinite;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}

@keyframes flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

/* Slide transitions */
.slide-up-enter-active,
.slide-up-leave-active,
.slide-down-enter-active,
.slide-down-leave-active {
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.slide-up-enter-from {
  transform: translateY(100%);
  opacity: 0;
}

.slide-up-leave-to {
  transform: translateY(-30%);
  opacity: 0;
}

.slide-down-enter-from {
  transform: translateY(-100%);
  opacity: 0;
}

.slide-down-leave-to {
  transform: translateY(30%);
  opacity: 0;
}
</style>
