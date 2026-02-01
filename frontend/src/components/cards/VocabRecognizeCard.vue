<template>
  <div class="vocab-recognize-card" :class="{ correct: showCorrect, incorrect: showIncorrect }">
    <div class="bg-effects">
      <div class="circuit-grid"></div>
      <div class="glow-point"></div>
    </div>

    <div class="card-content">
      <div class="question">
        <div class="hanzi">{{ stepContent.question?.hanzi }}</div>
        <div class="pinyin">{{ stepContent.question?.pinyin }}</div>
      </div>

      <div class="options" v-if="!showResult">
        <button
          v-for="option in stepContent.options"
          :key="option.id"
          @click="selectOption(option.id)"
          :class="{ selected: selectedOption === option.id }"
          class="option-btn"
        >
          <span class="option-text">{{ option.pinyin }}</span>
          <span class="option-border"></span>
        </button>
      </div>

      <div v-else class="result">
        <div class="result-icon">{{ showCorrect ? '✓' : '✗' }}</div>
        <div class="result-text">{{ showCorrect ? 'CORRECT!' : 'TRY AGAIN' }}</div>
      </div>
    </div>

    <div v-if="showResult" class="continue-hint">
      <span class="hint-text">SWIPE UP FOR NEXT →</span>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import type { LessonStep } from '@/types/api'

const props = defineProps<{
  step: LessonStep
}>()

const emit = defineEmits<{
  (e: 'answer', data: any): void
  (e: 'continue'): void
}>()

const stepContent = computed(() => props.step.content || {})
const selectedOption = ref<number | null>(null)
const showResult = ref(false)
const showCorrect = ref(false)
const showIncorrect = ref(false)

function selectOption(optionId: number) {
  if (showResult.value) return

  selectedOption.value = optionId
  const correct = stepContent.value.correct_answer === String(optionId)

  showResult.value = true
  showCorrect.value = correct
  showIncorrect.value = !correct

  emit('answer', { selected_option: optionId, is_correct: correct })

  setTimeout(() => {
    emit('continue')
  }, 1500)
}
</script>

<style scoped>
.vocab-recognize-card {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: var(--color-bg-primary);
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
}

.vocab-recognize-card.correct {
  background: rgba(0, 229, 255, 0.05);
}

.vocab-recognize-card.correct .bg-effects .glow-point {
  background: radial-gradient(circle, rgba(0, 229, 255, 0.3) 0%, transparent 70%);
}

.vocab-recognize-card.incorrect {
  background: rgba(255, 46, 46, 0.05);
}

.vocab-recognize-card.incorrect .bg-effects .glow-point {
  background: radial-gradient(circle, rgba(255, 46, 46, 0.3) 0%, transparent 70%);
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

.circuit-grid {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(0, 229, 255, 0.03) 1px,
    transparent 1px
  ),
    linear-gradient(90deg, rgba(0, 229, 255, 0.03) 1px,
    transparent 1px
  );
  background-size: 30px 30px;
}

.glow-point {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 500px;
  height: 500px;
  background: radial-gradient(circle, rgba(0, 229, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  transition: background 0.5s;
}

.card-content {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 2rem;
  max-width: 500px;
  width: 100%;
}

.question {
  margin-bottom: 3rem;
}

.hanzi {
  font-size: 6rem;
  font-weight: 900;
  color: var(--color-text-primary);
  text-shadow: 0 0 20px var(--color-accent-cyan);
  line-height: 1;
  margin-bottom: 1rem;
}

.pinyin {
  font-size: 1.8rem;
  color: var(--color-text-secondary);
  font-weight: 500;
  letter-spacing: 2px;
}

.options {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  width: 100%;
}

.option-btn {
  position: relative;
  background: rgba(17, 19, 24, 0.8);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 229, 255, 0.3);
  color: var(--color-text-primary);
  padding: 1.5rem 2rem;
  border-radius: var(--radius-lg);
  font-size: 1.1rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s;
  overflow: hidden;
}

.option-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-cyber);
  transform: scaleX(0);
  transition: transform 0.3s;
}

.option-btn:hover {
  background: rgba(0, 229, 255, 0.1);
  border-color: var(--color-accent-cyan);
  transform: translateY(-2px);
  box-shadow: var(--shadow-cyan);
}

.option-btn:hover::before {
  transform: scaleX(1);
}

.option-btn.selected {
  background: rgba(0, 229, 255, 0.15);
  border-color: var(--color-accent-cyan);
  box-shadow: var(--shadow-cyan);
}

.option-btn.selected::before {
  transform: scaleX(1);
}

.option-text {
  position: relative;
  z-index: 1;
}

.option-border {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: var(--gradient-cyber);
  border-radius: inherit;
  z-index: -1;
  opacity: 0;
  filter: blur(10px);
  transition: opacity 0.3s;
}

.option-btn:hover .option-border,
.option-btn.selected .option-border {
  opacity: 0.3;
}

.result {
  animation: popIn 0.5s ease;
}

.result-icon {
  font-size: 8rem;
  color: var(--color-text-primary);
  text-shadow: 0 0 30px var(--color-accent-cyan);
  margin-bottom: 1rem;
}

.vocab-recognize-card.correct .result-icon {
  color: var(--color-accent-cyan);
  text-shadow: 0 0 30px var(--color-accent-cyan), 0 0 60px var(--color-accent-cyan);
}

.vocab-recognize-card.incorrect .result-icon {
  color: var(--color-accent-red);
  text-shadow: 0 0 30px var(--color-accent-red);
}

.result-text {
  font-size: 2rem;
  color: var(--color-text-primary);
  font-weight: 900;
  letter-spacing: 2px;
}

.vocab-recognize-card.correct .result-text {
  color: var(--color-accent-cyan);
  text-shadow: 0 0 20px var(--color-accent-cyan);
}

.vocab-recognize-card.incorrect .result-text {
  color: var(--color-accent-red);
  text-shadow: 0 0 20px var(--color-accent-red);
}

.continue-hint {
  position: absolute;
  bottom: 3rem;
  left: 0;
  right: 0;
  z-index: 1;
}

.hint-text {
  color: var(--color-accent-cyan);
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 2px;
  animation: fadeInOut 2s infinite;
  text-shadow: 0 0 10px var(--color-accent-cyan);
}

@keyframes popIn {
  0% {
    transform: scale(0);
    opacity: 0;
  }
  50% {
    transform: scale(1.1);
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

@keyframes fadeInOut {
  0%, 100% { opacity: 0.5; }
  50% { opacity: 1; }
}
</style>
