<template>
  <div class="step-2-component">
    <div class="step-header">
      <h2 class="step-title">
        <span class="icon">📖</span>
        НОВЫЕ СЛОВА
      </h2>
      <p class="step-subtitle">Изучите 5 новых слов</p>
    </div>

    <!-- No Data State -->
    <div v-if="!stepData || !words || words.length === 0" class="no-data">
      <p>Нет слов для этого шага.</p>
      <p class="hint">Это может быть потому, что все слова уже выучены.</p>
    </div>

    <!-- Word Display -->
    <div v-else-if="currentWord" class="word-container">
      <div class="progress-indicator">
        <span>Слово {{ currentWordIndex + 1 }} / {{ totalWords }}</span>
        <div class="mini-progress">
          <div class="progress-fill" :style="{ width: progress + '%' }"></div>
        </div>
      </div>

      <div class="word-card">
        <div class="hanzi clickable-word" @click="speakWord" title="Нажмите для озвучки">{{ currentWord.hanzi }}</div>
        <div class="pinyin clickable-word" @click="speakWord" title="Нажмите для озвучки">{{ currentWord.pinyin }}</div>

        <div class="translations">
          <div class="translation">
            <span class="label">RU:</span>
            <span class="text">{{ currentWord.translation_ru }}</span>
          </div>
          <div class="translation">
            <span class="label">KZ:</span>
            <span class="text">{{ currentWord.translation_kz }}</span>
          </div>
        </div>

        <div class="audio-section">
          <button @click="playAudio" class="audio-btn">
            <span class="icon">🔊</span> НОРМАЛЬНАЯ СКОРОСТЬ
          </button>
          <button @click="playAudioSlow" class="audio-btn audio-btn-slow">
            <span class="icon">🐢</span> МЕДЛЕННАЯ СКОРОСТЬ
          </button>
        </div>

        <!-- Pronunciation Practice -->
        <div class="pronunciation-section">
          <p class="pronunciation-prompt">Практикуйте произношение:</p>
          <button @click="repeatPronunciation" class="repeat-btn">
            <span class="icon">🎤</span>
            <span>ПОВТОРИТЬ</span>
          </button>
          <div v-if="pronunciationResult" class="pronunciation-result" :class="{ ok: pronunciationResult === 'OK' }">
            {{ pronunciationResult }}
          </div>
        </div>
      </div>

      <!-- Mini Test -->
      <div class="mini-test">
        <h3>Быстрый тест</h3>
        <p class="quiz-prompt">Выберите правильный перевод:</p>
        <div class="options-grid">
          <button
            v-for="(option, index) in quizOptions"
            :key="index"
            @click="selectOption(index)"
            class="option-btn"
            :class="{
              selected: selectedOption === index,
              correct: showResult && index === correctOption,
              incorrect: showResult && selectedOption === index && index !== correctOption
            }"
            :disabled="showResult"
          >
            {{ option }}
          </button>
        </div>

        <button
          v-if="showResult"
          @click="nextWord"
          class="next-btn"
        >
          СЛЕДУЮЩЕЕ СЛОВО →
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { speakChinese } from '@/utils/speech'

const props = defineProps<{
  stepData: any
  session: any
}>()

const emit = defineEmits(['submit'])

const currentWordIndex = ref(0)
const selectedOption = ref<number | null>(null)
const showResult = ref(false)
const pronunciationResult = ref<string | null>(null)
const wordResults = ref<any[]>([])

const words = computed(() => props.stepData?.words || [])
const currentWord = computed(() => words.value[currentWordIndex.value])
const totalWords = computed(() => props.stepData?.total_words || words.value.length)

const progress = computed(() => {
  return ((currentWordIndex.value + 1) / totalWords.value) * 100
})

// Generate quiz options (1 correct + 3 distractors)
const quizOptions = computed(() => {
  if (!currentWord.value) return []

  const options = [currentWord.value.translation_ru, currentWord.value.translation_kz]

  // Add distractors (simplified - in real app, would fetch from API)
  const distractors = ['Distractor 1', 'Distractor 2']
  options.push(...distractors)

  // Shuffle
  return options.sort(() => Math.random() - 0.5)
})

const correctOption = computed(() => {
  // Both RU and KZ are correct
  if (selectedOption.value === null) return -1
  const selected = quizOptions.value[selectedOption.value]
  if (selected === currentWord.value.translation_ru ||
      selected === currentWord.value.translation_kz) {
    return selectedOption.value
  }
  return -1
})

function selectOption(index: number) {
  if (showResult.value) return

  selectedOption.value = index
  showResult.value = true

  // Store result
  const isCorrect = index === correctOption.value
  wordResults.value.push({
    word_id: currentWord.value.id,
    selected_option_id: index,
    is_correct: isCorrect,
    time_spent_seconds: 0
  })

  // Auto-advance after 1 second
  setTimeout(() => {
    if (currentWordIndex.value < totalWords.value - 1) {
      nextWord()
    } else {
      // Last word completed - submit and move to next step
      completeStep()
    }
  }, 1000)
}

function nextWord() {
  if (currentWordIndex.value < totalWords.value - 1) {
    currentWordIndex.value++
    selectedOption.value = null
    showResult.value = false
    pronunciationResult.value = null
  }
}

function completeStep() {
  emit('submit', {
    words: wordResults.value
  })
}

function playAudio() {
  if (currentWord.value?.hanzi) {
    speakChinese(currentWord.value.hanzi, 0.9)
  }
}

function playAudioSlow() {
  if (currentWord.value?.hanzi) {
    speakChinese(currentWord.value.hanzi, 0.6)
  }
}

function speakWord() {
  if (currentWord.value?.hanzi) {
    speakChinese(currentWord.value.hanzi, 0.9)
  }
}

function repeatPronunciation() {
  // Simulate pronunciation check
  pronunciationResult.value = Math.random() > 0.3 ? 'OK' : 'Try again'

  // Increment pronunciation attempts
  const currentWordResult = wordResults.value.find(w => w.word_id === currentWord.value?.id)
  if (currentWordResult) {
    currentWordResult.pronunciation_attempts = (currentWordResult.pronunciation_attempts || 0) + 1
    if (pronunciationResult.value === 'OK') {
      currentWordResult.pronunciation_ok_count = (currentWordResult.pronunciation_ok_count || 0) + 1
    }
  }
}
</script>

<style scoped>
.step-2-component {
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

.word-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
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

.word-card {
  background: rgba(17, 19, 24, 0.95);
  border: 2px solid rgba(0, 229, 255, 0.3);
  border-radius: var(--radius-xl);
  padding: 3rem 2rem;
  text-align: center;
  box-shadow: var(--shadow-card);
}

.word-card:hover {
  border-color: var(--color-accent-cyan);
  box-shadow: var(--shadow-card), var(--shadow-cyan);
}

.hanzi {
  font-size: 5rem;
  font-weight: 900;
  color: var(--color-text-primary);
  margin-bottom: 1rem;
}

.pinyin {
  font-size: 1.8rem;
  color: var(--color-text-secondary);
  margin-bottom: 2rem;
}

.clickable-word {
  cursor: pointer;
  transition: all 0.3s;
  padding: 0.5rem;
  border-radius: var(--radius-md);
  display: inline-block;
}

.clickable-word:hover {
  transform: scale(1.05);
  color: var(--color-accent-cyan);
}

.translations {
  display: flex;
  justify-content: center;
  gap: 3rem;
  margin-bottom: 2rem;
}

.translation {
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
}

.translation .label {
  font-size: 0.8rem;
  color: var(--color-accent-cyan);
  font-weight: 700;
  letter-spacing: 1px;
}

.translation .text {
  font-size: 1.2rem;
  color: var(--color-text-primary);
  font-weight: 500;
}

.audio-section {
  display: flex;
  justify-content: center;
  gap: 1rem;
  margin-bottom: 2rem;
}

.audio-btn {
  padding: 1rem 1.5rem;
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

.pronunciation-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

.pronunciation-prompt {
  color: var(--color-text-muted);
  font-size: 0.9rem;
  margin: 0;
}

.repeat-btn {
  padding: 0.75rem 1.5rem;
  background: var(--gradient-gold);
  border: none;
  border-radius: var(--radius-md);
  color: var(--color-bg-primary);
  font-weight: 700;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  box-shadow: var(--shadow-gold);
  transition: all 0.3s;
}

.repeat-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-gold), 0 0 15px rgba(245, 197, 66, 0.5);
}

.pronunciation-result {
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm);
  font-weight: 700;
  font-size: 0.9rem;
}

.pronunciation-result.ok {
  background: rgba(0, 255, 100, 0.2);
  color: var(--color-success);
}

.mini-test {
  background: rgba(17, 19, 24, 0.9);
  border: 1px solid rgba(0, 229, 255, 0.2);
  border-radius: var(--radius-xl);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.mini-test h3 {
  color: var(--color-text-primary);
  margin: 0;
  font-size: 1.3rem;
}

.quiz-prompt {
  color: var(--color-text-muted);
  margin: 0;
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

.next-btn,
.complete-btn {
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

.next-btn:hover,
.complete-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-cyan), 0 0 20px rgba(0, 229, 255, 0.5);
}

.complete-btn {
  align-self: center;
  padding: 1.5rem 3rem;
  font-size: 1.2rem;
}

.no-data {
  background: rgba(17, 19, 24, 0.9);
  border: 1px solid rgba(255, 46, 46, 0.3);
  border-radius: var(--radius-xl);
  padding: 3rem 2rem;
  text-align: center;
  color: var(--color-text-primary);
}

.no-data p {
  margin: 0 0 0.5rem 0;
  font-size: 1.1rem;
}

.no-data .hint {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}
</style>
