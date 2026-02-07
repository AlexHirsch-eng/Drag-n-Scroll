<template>
  <div class="vocab-intro-card">
    <div class="bg-effects">
      <div class="circuit-pattern"></div>
      <div class="glow-orb"></div>
    </div>

    <div class="card-content">
      <div class="word-display">
        <div class="hanzi clickable-word" @click="speakHanzi" title="Нажмите для озвучки">
          {{ stepContent.words?.[0]?.hanzi }}
        </div>
        <div class="pinyin clickable-word" @click="speakHanzi" title="Нажмите для озвучки">
          {{ stepContent.words?.[0]?.pinyin }}
        </div>
      </div>

      <div class="translation">
        <div class="ru">{{ stepContent.words?.[0]?.translation_ru }}</div>
        <div class="kz">{{ stepContent.words?.[0]?.translation_kz }}</div>
      </div>

      <button @click="playAudio" class="audio-btn">
        <span class="btn-icon">🔊</span>
        <span class="btn-text">ПРОСЛУШАТЬ</span>
        <span class="btn-glow"></span>
      </button>
    </div>

    <div class="swipe-hint">
      <div class="swipe-indicator">
        <span class="arrow">▲</span>
        <span>СВАЙП ВВЕРХ ДЛЯ ПРОДОЛЖЕНИЯ</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import type { LessonStep } from '@/types/api'
import { speakChinese } from '@/utils/speech'

const props = defineProps<{
  step: LessonStep
}>()

const emit = defineEmits<{
  (e: 'continue'): void
}>()

const stepContent = computed(() => props.step.content || {})

function playAudio() {
  const hanzi = stepContent.value.words?.[0]?.hanzi
  if (hanzi) {
    speakChinese(hanzi)
  }
}

function speakHanzi() {
  const hanzi = stepContent.value.words?.[0]?.hanzi
  if (hanzi) {
    speakChinese(hanzi)
  }
}
</script>

<style scoped>
.vocab-intro-card {
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

.circuit-pattern {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(rgba(0, 229, 255, 0.05) 1px,
    transparent 1px
  ),
    linear-gradient(90deg, rgba(0, 229, 255, 0.05) 1px,
    transparent 1px
  );
  background-size: 40px 40px;
  animation: circuitPulse 8s ease-in-out infinite;
}

@keyframes circuitPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.glow-orb {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 400px;
  height: 400px;
  background: radial-gradient(circle, rgba(0, 229, 255, 0.15) 0%, transparent 70%);
  border-radius: 50%;
  animation: orbPulse 4s ease-in-out infinite;
}

@keyframes orbPulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.5; }
  50% { transform: translate(-50%, -50%) scale(1.2); opacity: 0.8; }
}

.card-content {
  position: relative;
  z-index: 1;
  text-align: center;
  padding: 2rem;
}

.word-display {
  margin-bottom: 2rem;
}

.hanzi {
  font-size: 7rem;
  font-weight: 900;
  color: var(--color-text-primary);
  text-shadow:
    0 0 20px var(--color-accent-cyan),
    0 0 40px var(--color-accent-cyan),
    0 0 60px rgba(0, 229, 255, 0.5);
  line-height: 1;
  margin-bottom: 1rem;
  animation: textGlow 2s ease-in-out infinite;
}

@keyframes textGlow {
  0%, 100% { text-shadow: 0 0 20px var(--color-accent-cyan), 0 0 40px var(--color-accent-cyan); }
  50% { text-shadow: 0 0 30px var(--color-accent-cyan), 0 0 60px var(--color-accent-cyan), 0 0 80px rgba(0, 229, 255, 0.5); }
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
  filter: brightness(1.2);
}

.pinyin {
  font-size: 2rem;
  color: var(--color-text-secondary);
  font-weight: 500;
  letter-spacing: 2px;
}

.translation {
  background: rgba(17, 19, 24, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(0, 229, 255, 0.3);
  padding: 2rem 2.5rem;
  border-radius: var(--radius-xl);
  margin-bottom: 2rem;
  position: relative;
  overflow: hidden;
}

.translation::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-cyber);
  box-shadow: var(--shadow-cyan);
}

.ru {
  display: block;
  font-size: 1.8rem;
  color: var(--color-text-primary);
  font-weight: 700;
  margin-bottom: 0.75rem;
  letter-spacing: 1px;
}

.kz {
  display: block;
  font-size: 1.2rem;
  color: var(--color-text-muted);
  letter-spacing: 1px;
}

.audio-btn {
  position: relative;
  background: transparent;
  border: 2px solid var(--color-accent-cyan);
  color: var(--color-accent-cyan);
  padding: 1.25rem 2.5rem;
  border-radius: var(--radius-md);
  font-size: 1rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 2px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.75rem;
  box-shadow: var(--shadow-cyan);
}

.audio-btn:hover {
  background: rgba(0, 229, 255, 0.1);
  box-shadow:
    var(--shadow-cyan),
    var(--shadow-neon);
  transform: translateY(-2px);
}

.audio-btn .btn-icon {
  font-size: 1.3rem;
}

.audio-btn .btn-glow {
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

.audio-btn:hover .btn-glow {
  opacity: 0.5;
}

.swipe-hint {
  position: absolute;
  bottom: 3rem;
  left: 0;
  right: 0;
  z-index: 1;
}

.swipe-indicator {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  color: var(--color-accent-cyan);
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 2px;
  animation: bounce 2s infinite;
}

.swipe-indicator .arrow {
  font-size: 2rem;
  text-shadow: 0 0 10px var(--color-accent-cyan);
}

@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
</style>
