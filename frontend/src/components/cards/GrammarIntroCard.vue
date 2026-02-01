<template>
  <div class="grammar-intro-card">
    <div class="bg-effects">
      <div class="grid-background"></div>
      <div class="ambient-light"></div>
    </div>

    <div class="card-content">
      <div class="card-header">
        <h3><span class="icon">龍</span>GRAMMAR</h3>
        <span class="rule-count">{{ stepContent.rules?.length || 0 }} RULES</span>
      </div>

      <div class="rules-container">
        <div
          v-for="rule in stepContent.rules"
          :key="rule.id"
          class="rule-item"
        >
          <h4 class="rule-title">{{ rule.title }}</h4>

          <div v-if="rule.pattern" class="rule-pattern">
            <span class="pattern-bracket">&lt;</span>
            {{ rule.pattern }}
            <span class="pattern-bracket">/&gt;</span>
          </div>

          <div class="rule-explanation">
            <p class="ru">{{ rule.explanation_ru }}</p>
            <p class="kz">{{ rule.explanation_kz }}</p>
          </div>

          <div v-if="rule.examples && rule.examples.length > 0" class="examples-section">
            <h5>EXAMPLES</h5>
            <div
              v-for="(example, index) in rule.examples"
              :key="index"
              class="example-item"
            >
              <div class="example-hanzi">{{ example.sentence_hanzi }}</div>
              <div class="example-pinyin">{{ example.sentence_pinyin }}</div>
              <div class="example-translation">
                <span class="ru">{{ example.translation_ru }}</span>
                <span class="kz">{{ example.translation_kz }}</span>
              </div>
              <button
                v-if="example.audio_url"
                @click="playAudio(example.audio_url)"
                class="audio-btn"
              >
                🔊
              </button>
            </div>
          </div>
        </div>
      </div>

      <div class="card-footer">
        <p class="instruction">SWIPE UP TO CONTINUE ▲</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { LessonStep } from '@/types/api'

const props = defineProps<{
  step: LessonStep
}>()

const stepContent = computed(() => props.step.content || {})

function playAudio(url: string) {
  const audio = new Audio(url)
  audio.play()
}
</script>

<style scoped>
.grammar-intro-card {
  height: 100%;
  display: flex;
  flex-direction: column;
  padding: 2rem;
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

.grid-background {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(245, 197, 66, 0.03) 1px,
    transparent 1px
  ),
    linear-gradient(90deg, rgba(245, 197, 66, 0.03) 1px,
    transparent 1px
  );
  background-size: 30px 30px;
  animation: gridMove 15s linear infinite;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(30px, 30px); }
}

.ambient-light {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 800px;
  height: 800px;
  background: radial-gradient(circle, rgba(245, 197, 66, 0.08) 0%, transparent 70%);
  border-radius: 50%;
  animation: ambientPulse 10s ease-in-out infinite;
}

@keyframes ambientPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.4; }
  50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.7; }
}

.card-content {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  flex: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(245, 197, 66, 0.2);
}

.card-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 900;
  letter-spacing: 4px;
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.card-header .icon {
  font-size: 1.8rem;
  color: var(--color-accent-gold);
  text-shadow: 0 0 20px var(--color-accent-gold);
}

.rule-count {
  background: rgba(245, 197, 66, 0.1);
  border: 1px solid rgba(245, 197, 66, 0.3);
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--color-accent-gold);
  box-shadow: 0 0 10px rgba(245, 197, 66, 0.2);
}

.rules-container {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 2rem;
  overflow-y: auto;
  padding: 1rem;
}

.rule-item {
  background: rgba(17, 19, 24, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(245, 197, 66, 0.2);
  padding: 2rem;
  border-radius: var(--radius-xl);
  position: relative;
  overflow: hidden;
}

.rule-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-gold);
  box-shadow: var(--shadow-gold);
}

.rule-title {
  margin: 0 0 1.5rem 0;
  color: var(--color-text-primary);
  font-size: 1.5rem;
  font-weight: 900;
  letter-spacing: 2px;
  text-shadow: 0 0 10px var(--color-accent-gold);
}

.rule-pattern {
  background: rgba(245, 197, 66, 0.1);
  border: 1px solid rgba(245, 197, 66, 0.3);
  padding: 1.25rem;
  border-radius: var(--radius-md);
  font-family: 'Courier New', monospace;
  font-size: 1.1rem;
  margin-bottom: 1.5rem;
  text-align: center;
  color: var(--color-accent-gold);
  font-weight: 700;
  letter-spacing: 2px;
  position: relative;
  box-shadow: inset 0 0 20px rgba(245, 197, 66, 0.1);
}

.rule-pattern .pattern-bracket {
  color: var(--color-accent-gold);
  text-shadow: 0 0 10px var(--color-accent-gold);
}

.rule-explanation {
  margin-bottom: 2rem;
}

.rule-explanation p {
  margin: 0.75rem 0;
  line-height: 1.6;
}

.rule-explanation .ru {
  color: var(--color-text-primary);
  font-weight: 500;
}

.rule-explanation .kz {
  color: var(--color-text-muted);
  font-size: 0.95rem;
}

.examples-section h5 {
  margin: 0 0 1rem 0;
  color: var(--color-text-primary);
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 2px;
}

.example-item {
  background: rgba(245, 197, 66, 0.05);
  border: 1px solid rgba(245, 197, 66, 0.2);
  padding: 1.25rem;
  border-radius: var(--radius-md);
  margin-bottom: 1rem;
  position: relative;
  transition: all 0.3s;
}

.example-item:hover {
  background: rgba(245, 197, 66, 0.1);
  border-color: rgba(245, 197, 66, 0.4);
  box-shadow: 0 0 15px rgba(245, 197, 66, 0.2);
}

.example-hanzi {
  font-size: 1.5rem;
  color: var(--color-text-primary);
  font-weight: 700;
  margin-bottom: 0.5rem;
}

.example-pinyin {
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin-bottom: 0.75rem;
  letter-spacing: 1px;
}

.example-translation {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
  font-size: 0.95rem;
}

.example-translation .ru {
  color: var(--color-text-primary);
  font-weight: 500;
}

.example-translation .kz {
  color: var(--color-text-muted);
}

.audio-btn {
  position: absolute;
  top: 0.75rem;
  right: 0.75rem;
  width: 36px;
  height: 36px;
  border: none;
  background: var(--gradient-gold);
  color: var(--color-bg-primary);
  border-radius: 50%;
  cursor: pointer;
  font-size: 1rem;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  box-shadow: var(--shadow-gold);
}

.audio-btn:hover {
  transform: scale(1.1);
  box-shadow:
    var(--shadow-gold),
    0 0 20px rgba(245, 197, 66, 0.5);
}

.card-footer {
  text-align: center;
  padding: 1rem;
  border-top: 1px solid rgba(245, 197, 66, 0.2);
}

.instruction {
  color: var(--color-accent-gold);
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 2px;
  margin: 0;
  text-shadow: 0 0 10px var(--color-accent-gold);
  animation: bounce 2s infinite;
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-5px); }
}
</style>
