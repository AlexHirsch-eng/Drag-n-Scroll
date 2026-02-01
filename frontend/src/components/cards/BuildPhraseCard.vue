<template>
  <div class="build-phrase-card">
    <div class="bg-effects">
      <div class="grid-pattern"></div>
      <div class="ambient-glow"></div>
    </div>

    <div class="card-content">
      <div class="instruction">
        <div class="ru">{{ stepContent.instruction_ru }}</div>
        <div class="kz">{{ stepContent.instruction_kz }}</div>
      </div>

      <div class="target-phrase">
        <div class="hanzi">{{ stepContent.target_hanzi }}</div>
        <div class="pinyin">{{ stepContent.target_pinyin }}</div>
      </div>

      <div class="word-bank">
        <div
          v-for="option in shuffledOptions"
          :key="option.id"
          @click="selectWord(option)"
          class="word-option"
          :class="{ used: isUsed(option) }"
        >
          <span class="word-text">{{ option.hanzi }}</span>
          <span class="word-border"></span>
        </div>
      </div>

      <div class="answer-area">
        <div
          v-for="(wordId, index) in userAnswer"
          :key="index"
          @click="removeWord(index)"
          class="answer-slot"
        >
          <span class="slot-text">{{ getWordById(wordId)?.hanzi }}</span>
          <span class="slot-border"></span>
        </div>
      </div>

      <div v-if="showResult" class="result">
        <div class="result-icon">{{ isCorrect ? '✓' : '✗' }}</div>
        <div class="result-text">{{ isCorrect ? 'CORRECT!' : 'TRY AGAIN' }}</div>
      </div>

      <button v-if="!showResult" @click="checkAnswer" class="check-btn" :disabled="userAnswer.length === 0">
        <span class="btn-text">CHECK ANSWER</span>
        <span class="btn-glow"></span>
      </button>
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
const userAnswer = ref<number[]>([])
const showResult = ref(false)
const isCorrect = ref(false)

const shuffledOptions = computed(() => {
  const options = [...(stepContent.value.options || [])]
  return options.sort(() => Math.random() - 0.5)
})

function selectWord(option: any) {
  if (!isUsed(option)) {
    userAnswer.value.push(option.id)
  }
}

function removeWord(index: number) {
  userAnswer.value.splice(index, 1)
}

function isUsed(option: any) {
  return userAnswer.value.includes(option.id)
}

function getWordById(id: number) {
  return shuffledOptions.value.find((o: any) => o.id === id)
}

function checkAnswer() {
  const correct = stepContent.value.correct_order || []
  const correctIds = correct.map((_id: number, index: number) => index + 1)

  isCorrect.value = JSON.stringify(userAnswer.value) === JSON.stringify(correctIds)
  showResult.value = true

  emit('answer', { order: userAnswer.value, is_correct: isCorrect.value })

  setTimeout(() => {
    emit('continue')
  }, 1500)
}
</script>

<style scoped>
.build-phrase-card {
  height: 100%;
  width: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: var(--color-bg-primary);
  position: relative;
  overflow: hidden;
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

.grid-pattern {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(245, 197, 66, 0.05) 1px,
    transparent 1px
  ),
    linear-gradient(90deg, rgba(245, 197, 66, 0.05) 1px,
    transparent 1px
  );
  background-size: 30px 30px;
}

.ambient-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 600px;
  height: 600px;
  background: radial-gradient(circle, rgba(245, 197, 66, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: ambientPulse 6s ease-in-out infinite;
}

@keyframes ambientPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; }
}

.card-content {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 2rem;
  max-width: 600px;
  width: 100%;
}

.instruction {
  background: rgba(17, 19, 24, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(245, 197, 66, 0.3);
  padding: 1.5rem 2rem;
  border-radius: var(--radius-xl);
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}

.instruction::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-gold);
  box-shadow: var(--shadow-gold);
}

.ru {
  display: block;
  font-size: 1.3rem;
  color: var(--color-text-primary);
  font-weight: 700;
  margin-bottom: 0.5rem;
  letter-spacing: 1px;
}

.kz {
  display: block;
  font-size: 1rem;
  color: var(--color-text-muted);
  letter-spacing: 0.5px;
}

.target-phrase {
  margin-bottom: 3rem;
}

.hanzi {
  font-size: 3.5rem;
  font-weight: 900;
  color: var(--color-text-primary);
  text-shadow: 0 0 20px var(--color-accent-gold);
  margin-bottom: 0.75rem;
  letter-spacing: 4px;
}

.pinyin {
  font-size: 1.3rem;
  color: var(--color-text-secondary);
  letter-spacing: 2px;
}

.word-bank {
  display: flex;
  flex-wrap: wrap;
  gap: 0.75rem;
  justify-content: center;
  margin-bottom: 2rem;
}

.word-option {
  position: relative;
  background: rgba(17, 19, 24, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(245, 197, 66, 0.3);
  color: var(--color-text-primary);
  padding: 1rem 1.5rem;
  border-radius: var(--radius-lg);
  font-size: 1.5rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  overflow: hidden;
}

.word-option::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-gold);
  transform: scaleX(0);
  transition: transform 0.3s;
}

.word-option:hover:not(.used) {
  background: rgba(245, 197, 66, 0.1);
  border-color: var(--color-accent-gold);
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold);
}

.word-option:hover:not(.used)::before {
  transform: scaleX(1);
}

.word-option.used {
  opacity: 0.2;
  cursor: not-allowed;
  border-color: rgba(245, 197, 66, 0.1);
}

.word-border {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: var(--gradient-gold);
  border-radius: inherit;
  z-index: -1;
  opacity: 0;
  filter: blur(8px);
  transition: opacity 0.3s;
}

.word-option:hover:not(.used) .word-border {
  opacity: 0.3;
}

.answer-area {
  display: flex;
  gap: 0.5rem;
  justify-content: center;
  margin-bottom: 2rem;
  min-height: 70px;
  flex-wrap: wrap;
}

.answer-slot {
  position: relative;
  background: rgba(245, 197, 66, 0.15);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(245, 197, 66, 0.5);
  color: var(--color-text-primary);
  padding: 1rem 1.5rem;
  border-radius: var(--radius-lg);
  font-size: 1.5rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: 0 0 10px rgba(245, 197, 66, 0.2);
}

.answer-slot:hover {
  background: rgba(245, 197, 66, 0.25);
  border-color: var(--color-accent-gold);
  transform: scale(1.05);
  box-shadow: var(--shadow-gold);
}

.slot-border {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: var(--gradient-gold);
  border-radius: inherit;
  z-index: -1;
  opacity: 0;
  filter: blur(10px);
  transition: opacity 0.3s;
}

.answer-slot:hover .slot-border {
  opacity: 0.4;
}

.check-btn {
  position: relative;
  background: var(--gradient-gold);
  border: none;
  color: var(--color-bg-primary);
  padding: 1.25rem 3rem;
  border-radius: var(--radius-md);
  font-size: 1.1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.3s;
  box-shadow: var(--shadow-gold);
}

.check-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow:
    var(--shadow-gold),
    0 0 30px rgba(245, 197, 66, 0.5);
}

.check-btn:disabled {
  opacity: 0.4;
  cursor: not-allowed;
}

.check-btn .btn-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: var(--gradient-gold);
  border-radius: inherit;
  z-index: -1;
  opacity: 0;
  filter: blur(15px);
  transition: opacity 0.3s;
}

.check-btn:hover:not(:disabled) .btn-glow {
  opacity: 0.5;
}

.result {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation: popIn 0.5s ease;
  z-index: 10;
}

.result-icon {
  font-size: 8rem;
  color: var(--color-text-primary);
  margin-bottom: 1rem;
}

.result-icon[style*="✓"] {
  text-shadow: 0 0 30px var(--color-accent-gold), 0 0 60px var(--color-accent-gold);
}

.result-icon[style*="✗"] {
  text-shadow: 0 0 30px var(--color-accent-red);
}

.result-text {
  font-size: 2rem;
  color: var(--color-text-primary);
  font-weight: 900;
  letter-spacing: 2px;
}

@keyframes popIn {
  0% {
    transform: translate(-50%, -50%) scale(0);
    opacity: 0;
  }
  50% {
    transform: translate(-50%, -50%) scale(1.1);
  }
  100% {
    transform: translate(-50%, -50%) scale(1);
    opacity: 1;
  }
}
</style>
