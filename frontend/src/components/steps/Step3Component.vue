<template>
  <div class="step-3-component">
    <div class="step-header">
      <h2 class="step-title">
        <span class="icon">📝</span>
        ГРАММАТИКА
      </h2>
      <p class="step-subtitle">Составляйте предложения с новым шаблоном</p>
    </div>

    <!-- No Data State -->
    <div v-if="!stepData || !stepData.grammar_rule" class="no-data">
      <p>Нет грамматического упражнения для этого шага.</p>
      <p class="hint">Пожалуйста, вернитесь позже или свяжитесь с поддержкой.</p>
    </div>

    <div v-else class="grammar-container">
      <!-- Grammar Rule -->
      <div class="grammar-rule-card">
        <h3>{{ stepData.grammar_rule.title }}</h3>
        <div class="pattern">{{ stepData.grammar_rule.pattern }}</div>

        <div class="explanation">
          {{ userLanguage === 'KZ' ? stepData.grammar_rule.explanation_kz : stepData.grammar_rule.explanation_ru }}
        </div>

        <div class="examples">
          <div v-for="(example, index) in stepData.grammar_rule.examples" :key="index" class="example">
            <div class="example-hanzi clickable-word" @click="speakHanzi(example.hanzi)" title="Нажмите для озвучки">{{ example.hanzi }}</div>
            <div class="example-pinyin clickable-word" @click="speakHanzi(example.hanzi)" title="Нажмите для озвучки">{{ example.pinyin }}</div>
            <div class="example-translation">{{ userLanguage === 'KZ' ? example.translation_kz : example.translation_ru }}</div>
          </div>
        </div>
      </div>

      <!-- Sentence Building Task -->
      <div class="task-section">
        <h4>Task: {{ stepData.task_prompt }}</h4>

        <!-- Component Bank -->
        <div class="component-bank">
          <div
            v-for="component in stepData.components"
            :key="component.id"
            @click="addComponent(component)"
            class="component-item"
          >
            <span class="component-hanzi">{{ component.hanzi }}</span>
            <span class="component-pinyin">{{ component.pinyin }}</span>
          </div>
        </div>

        <!-- Sentence Builder -->
        <div class="sentence-builder">
          <div class="built-sentence">
            <span
              v-for="(comp, index) in builtSentence"
              :key="index"
              class="built-component"
              @click="removeComponent(index)"
            >
              {{ comp.hanzi }}
            </span>
            <span v-if="builtSentence.length === 0" class="placeholder">
              Нажимайте на компоненты выше, чтобы составить предложение
            </span>
          </div>
        </div>

        <button @click="submitSentence" class="submit-btn" :disabled="builtSentence.length === 0">
          ПРОВЕРИТЬ ОТВЕТ
        </button>

        <!-- Feedback -->
        <div v-if="showResult" class="feedback" :class="{ correct: isCorrect, incorrect: !isCorrect }">
          <div class="feedback-icon">{{ isCorrect ? '✓' : '✗' }}</div>
          <div class="feedback-text">
            {{ isCorrect ? 'ПРАВИЛЬНО!' : 'ПОПРОБУЙТЕ СНОВА' }}
          </div>
          <div v-if="!isCorrect && correctAnswer" class="correct-answer">
            Правильно: {{ correctAnswer }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { speakChinese } from '@/utils/speech'

const props = defineProps<{
  stepData: any
  session: any
}>()

const emit = defineEmits(['submit'])

const authStore = useAuthStore()
const builtSentence = ref<any[]>([])
const showResult = ref(false)
const isCorrect = ref(false)
const correctAnswer = ref('')

const userLanguage = computed(() => {
  return authStore.user?.profile?.learning_language || 'RU'
})

function addComponent(component: any) {
  builtSentence.value.push(component)
}

function removeComponent(index: number) {
  builtSentence.value.splice(index, 1)
}

function submitSentence() {
  if (builtSentence.value.length === 0) return

  // Build sentence from components
  const sentence = builtSentence.value.map(c => c.hanzi).join('')
  correctAnswer.value = props.stepData?.correct_hanzi || ''

  // Check correctness
  isCorrect.value = sentence === correctAnswer.value
  showResult.value = true

  // Auto-submit and move to next step after showing feedback
  setTimeout(() => {
    completeStep()
  }, 2000)
}

function completeStep() {
  const sentence = builtSentence.value.map(c => c.hanzi).join('')

  emit('submit', {
    builtSentence: sentence
  })
}

function speakHanzi(text: string) {
  if (text) {
    speakChinese(text)
  }
}
</script>

<style scoped>
.step-3-component {
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

.grammar-container {
  display: flex;
  flex-direction: column;
  gap: 2rem;
}

.grammar-rule-card {
  background: rgba(17, 19, 24, 0.95);
  border: 2px solid rgba(0, 229, 255, 0.3);
  border-radius: var(--radius-xl);
  padding: 2rem;
  box-shadow: var(--shadow-card);
}

.grammar-rule-card h3 {
  color: var(--color-accent-cyan);
  font-size: 1.5rem;
  margin: 0 0 1rem 0;
}

.pattern {
  background: rgba(0, 229, 255, 0.1);
  border-left: 4px solid var(--color-accent-cyan);
  padding: 1rem 1.5rem;
  color: var(--color-text-primary);
  font-size: 1.2rem;
  font-weight: 600;
  margin-bottom: 1.5rem;
}

.explanation {
  color: var(--color-text-secondary);
  font-size: 1rem;
  line-height: 1.6;
  margin-bottom: 2rem;
}

.examples {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.example {
  background: rgba(255, 255, 255, 0.03);
  border-radius: var(--radius-md);
  padding: 1rem;
}

.example-hanzi {
  font-size: 1.3rem;
  color: var(--color-text-primary);
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.example-pinyin {
  color: var(--color-text-secondary);
  font-size: 1rem;
  margin-bottom: 0.5rem;
}

.clickable-word {
  cursor: pointer;
  transition: all 0.3s;
  padding: 0.5rem;
  border-radius: var(--radius-md);
  display: inline-block;
}

.clickable-word:hover {
  transform: scale(1.03);
  color: var(--color-accent-cyan);
}

.example-translation {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.task-section {
  background: rgba(17, 19, 24, 0.9);
  border: 1px solid rgba(0, 229, 255, 0.2);
  border-radius: var(--radius-xl);
  padding: 2rem;
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.task-section h4 {
  color: var(--color-text-primary);
  margin: 0;
  font-size: 1.2rem;
}

.component-bank {
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: center;
}

.component-item {
  background: rgba(0, 229, 255, 0.1);
  border: 2px solid var(--color-accent-cyan);
  border-radius: var(--radius-md);
  padding: 1rem 1.5rem;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  align-items: center;
}

.component-item:hover {
  background: rgba(0, 229, 255, 0.2);
  transform: translateY(-2px);
  box-shadow: var(--shadow-cyan);
}

.component-hanzi {
  font-size: 1.5rem;
  color: var(--color-text-primary);
  font-weight: 700;
}

.component-pinyin {
  font-size: 0.8rem;
  color: var(--color-text-muted);
}

.sentence-builder {
  background: rgba(0, 0, 0, 0.3);
  border: 2px dashed rgba(255, 255, 255, 0.2);
  border-radius: var(--radius-xl);
  padding: 2rem;
  min-height: 120px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.built-sentence {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.built-component {
  background: var(--gradient-cyber);
  color: var(--color-bg-primary);
  padding: 0.75rem 1.25rem;
  border-radius: var(--radius-md);
  font-size: 1.2rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.built-component:hover {
  transform: scale(1.05);
  box-shadow: var(--shadow-cyan);
}

.placeholder {
  color: var(--color-text-muted);
  font-size: 0.9rem;
}

.submit-btn,
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
  align-self: center;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.submit-btn:hover:not(:disabled),
.next-btn:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-cyan), 0 0 20px rgba(0, 229, 255, 0.5);
}

.feedback {
  padding: 1.5rem;
  border-radius: var(--radius-md);
  display: flex;
  flex-direction: column;
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
  font-size: 3rem;
  font-weight: 900;
}

.feedback.correct .feedback-icon {
  color: var(--color-success);
}

.feedback.incorrect .feedback-icon {
  color: var(--color-accent-red);
}

.feedback-text {
  font-size: 1.3rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.correct-answer {
  color: var(--color-text-muted);
  font-size: 1rem;
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
