<template>
  <div class="step-1-component">
    <div class="step-header">
      <h2 class="step-title">
        <span class="icon">🔄</span>
        SRS REVIEW
      </h2>
      <p class="step-subtitle">Review words from previous lessons</p>
    </div>

    <!-- Flashcard -->
    <div v-if="currentCard" class="flashcard-container">
      <div class="flashcard" :class="{ flipped: showAnswer }">
        <div class="card-front">
          <div class="hanzi">{{ currentCard.word.hanzi }}</div>
          <div class="pinyin">{{ currentCard.word.pinyin }}</div>
          <button @click="playAudio" class="audio-btn">
            <span class="icon">🔊</span> PLAY AUDIO
          </button>
        </div>

        <div class="card-back">
          <div class="options-grid">
            <button
              v-for="(option, index) in currentCard.options"
              :key="index"
              @click="selectOption(option.word_id)"
              class="option-btn"
              :class="{
                selected: selectedOptionId === option.word_id,
                correct: showAnswer && option.word_id === currentCard.word.id,
                incorrect: showAnswer && selectedOptionId === option.word_id && option.word_id !== currentCard.word.id
              }"
              :disabled="showAnswer"
            >
              {{ getTranslation(option) }}
            </button>
          </div>
        </div>
      </div>

      <div v-if="showAnswer" class="feedback" :class="{ correct: isCorrect, incorrect: !isCorrect }">
        <div class="feedback-icon">
          {{ isCorrect ? '✓' : '✗' }}
        </div>
        <div class="feedback-text">
          {{ isCorrect ? 'CORRECT!' : 'TRY AGAIN NEXT TIME' }}
        </div>
      </div>

      <button
        v-if="showAnswer && !isLastCard"
        @click="nextCard"
        class="next-btn"
      >
        NEXT CARD →
      </button>

      <button
        v-if="showAnswer && isLastCard"
        @click="completeStep"
        class="next-btn complete-btn"
        :disabled="isSubmitting"
      >
        {{ isSubmitting ? 'SUBMITTING...' : 'COMPLETE STEP →' }}
      </button>
    </div>

    <!-- Progress -->
    <div class="progress-indicator">
      <span>Card {{ currentCardIndex + 1 }} of {{ totalCards }}</span>
      <div class="mini-progress">
        <div class="progress-fill" :style="{ width: progress + '%' }"></div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps<{
  stepData: any
  session: any
}>()

const emit = defineEmits(['submit'])

const authStore = useAuthStore()

const currentCardIndex = ref(0)
const selectedOptionId = ref<number | null>(null)
const showAnswer = ref(false)
const isCorrect = ref(false)
const isSubmitting = ref(false)

const cards = computed(() => props.stepData?.cards || [])
const currentCard = computed(() => cards.value[currentCardIndex.value])
const totalCards = computed(() => props.stepData?.total_cards || cards.value.length)

const progress = computed(() => {
  return ((currentCardIndex.value + 1) / totalCards.value) * 100
})

const isLastCard = computed(() => {
  return currentCardIndex.value >= totalCards.value - 1
})

function getTranslation(option: any) {
  const user = authStore.user
  if (user?.profile?.learning_language === 'KZ') {
    return option.translation_kz
  }
  return option.translation_ru
}

function selectOption(wordId: number) {
  if (showAnswer.value) return

  selectedOptionId.value = wordId
  showAnswer.value = true
  isCorrect.value = wordId === currentCard.value.word.id

  // Auto-advance after showing feedback, unless it's the last card
  if (!isLastCard.value) {
    setTimeout(() => {
      submitAnswer()
    }, 1500)
  }
  // For the last card, let user click "COMPLETE STEP" button manually
}

function submitAnswer() {
  emit('submit', {
    cardId: currentCard.value.id,
    selectedOptionId: selectedOptionId.value,
    currentCardIndex: currentCardIndex.value,
    totalShownCards: totalCards.value
  })
}

function nextCard() {
  if (currentCardIndex.value < totalCards.value - 1) {
    currentCardIndex.value++
    selectedOptionId.value = null
    showAnswer.value = false
  }
}

function completeStep() {
  // Prevent double submission
  if (isSubmitting.value) {
    console.log('Already submitting, ignoring')
    return
  }

  // Submit the last card answer to complete the step
  console.log('completeStep called', {
    currentCard: currentCard.value,
    selectedOptionId: selectedOptionId.value,
    isLastCard: isLastCard.value,
    currentCardIndex: currentCardIndex.value,
    totalCards: totalCards.value
  })

  if (currentCard.value && selectedOptionId.value !== null) {
    isSubmitting.value = true

    const data = {
      cardId: currentCard.value.id,
      selectedOptionId: selectedOptionId.value,
      currentCardIndex: currentCardIndex.value,
      totalShownCards: totalCards.value
    }
    console.log('Emitting submit:', data)

    emit('submit', data)

    // Reset submitting flag after a delay
    setTimeout(() => {
      isSubmitting.value = false
    }, 2000)
  } else {
    console.error('Cannot complete: missing card or selection')
  }
}

function playAudio() {
  if (currentCard.value?.word?.audio_url) {
    const audio = new Audio(currentCard.value.word.audio_url)
    audio.play()
  }
}

onMounted(() => {
  // Initialize from stepData if resuming
  if (props.stepData?.current_card_index) {
    currentCardIndex.value = props.stepData.current_card_index
  }
})
</script>

<style scoped>
.step-1-component {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.step-header {
  text-align: center;
}

.step-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.75rem;
  font-size: 1.5rem;
  color: var(--color-text-primary);
  margin: 0 0 0.5rem 0;
}

.step-title .icon {
  font-size: 2rem;
}

.step-subtitle {
  color: var(--color-text-muted);
  font-size: 1rem;
  margin: 0;
}

.flashcard-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1.5rem;
}

.flashcard {
  width: 100%;
  max-width: 500px;
  aspect-ratio: 3/4;
  background: rgba(17, 19, 24, 0.95);
  border: 2px solid rgba(0, 229, 255, 0.3);
  border-radius: var(--radius-xl);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
  transition: all 0.5s ease;
  box-shadow: var(--shadow-card);
}

.flashcard:hover {
  border-color: var(--color-accent-cyan);
  box-shadow: var(--shadow-card), var(--shadow-cyan);
}

.card-front {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  text-align: center;
}

.hanzi {
  font-size: 4rem;
  font-weight: 900;
  color: var(--color-text-primary);
}

.pinyin {
  font-size: 1.5rem;
  color: var(--color-text-secondary);
}

.audio-btn {
  margin-top: 1rem;
  padding: 0.75rem 1.5rem;
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid var(--color-accent-cyan);
  border-radius: var(--radius-md);
  color: var(--color-accent-cyan);
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.audio-btn:hover {
  background: rgba(0, 229, 255, 0.2);
  box-shadow: var(--shadow-cyan);
}

.card-back {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.options-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1rem;
}

.option-btn {
  padding: 1.5rem 1rem;
  background: rgba(255, 255, 255, 0.05);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: var(--radius-md);
  color: var(--color-text-primary);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
}

.option-btn:hover:not(:disabled) {
  background: rgba(0, 229, 255, 0.1);
  border-color: var(--color-accent-cyan);
}

.option-btn.selected {
  border-color: var(--color-accent-cyan);
  background: rgba(0, 229, 255, 0.15);
}

.option-btn.correct {
  background: rgba(0, 255, 100, 0.2);
  border-color: var(--color-success);
}

.option-btn.incorrect {
  background: rgba(255, 46, 46, 0.2);
  border-color: var(--color-accent-red);
}

.feedback {
  padding: 1rem 2rem;
  border-radius: var(--radius-md);
  display: flex;
  align-items: center;
  gap: 1rem;
  animation: slideIn 0.3s ease;
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(-10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.feedback.correct {
  background: rgba(0, 255, 100, 0.2);
  border: 1px solid var(--color-success);
}

.feedback.incorrect {
  background: rgba(255, 46, 46, 0.2);
  border: 1px solid var(--color-accent-red);
}

.feedback-icon {
  font-size: 2rem;
  font-weight: 900;
}

.feedback.correct .feedback-icon {
  color: var(--color-success);
}

.feedback.incorrect .feedback-icon {
  color: var(--color-accent-red);
}

.feedback-text {
  font-size: 1.2rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.next-btn {
  padding: 1rem 2rem;
  background: var(--gradient-cyber);
  color: var(--color-bg-primary);
  border: none;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 700;
  letter-spacing: 1px;
  cursor: pointer;
  box-shadow: var(--shadow-cyan);
  transition: all 0.3s;
}

.next-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-cyan), 0 0 20px rgba(0, 229, 255, 0.5);
}

.next-btn.complete-btn {
  background: var(--gradient-success);
}

.progress-indicator {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
  color: var(--color-text-muted);
  font-size: 0.9rem;
  text-align: center;
}

.mini-progress {
  width: 200px;
  height: 4px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 2px;
  overflow: hidden;
  margin: 0 auto;
}

.progress-fill {
  height: 100%;
  background: var(--gradient-cyber);
  transition: width 0.3s ease;
}
</style>
