<template>
  <div class="srs-review-card">
    <div class="bg-effects">
      <div class="circuit-overlay"></div>
      <div class="pulse-glow"></div>
    </div>

    <div class="card-content">
      <div class="card-header">
        <h3><span class="bracket">&lt;</span>REVIEW<span class="bracket">/&gt;</span></h3>
        <span class="word-count">{{ words.length }} WORDS</span>
      </div>

      <div class="words-grid">
        <div
          v-for="word in words"
          :key="word.id"
          class="word-item"
          @click="playAudio(word)"
        >
          <span class="word-glow"></span>
          <div class="hanzi">{{ word.hanzi }}</div>
          <div class="pinyin">{{ word.pinyin }}</div>
          <div class="translation">{{ word.translation_ru }}</div>
          <div class="srs-info">
            <span class="level">LVL {{ word.srs_level }}</span>
            <span class="reviews">{{ word.total_reviews }}x</span>
          </div>
        </div>
      </div>

      <div class="card-footer">
        <p class="instruction">TAP WORD TO HEAR PRONUNCIATION</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { SRSReviewItem } from '@/types/api'

defineProps<{
  words: SRSReviewItem[]
}>()

const emit = defineEmits<{
  (e: 'submit', data: any): void
}>()

function playAudio(word: SRSReviewItem) {
  if (word.audio_url) {
    const audio = new Audio(word.audio_url)
    audio.play()
  }
}
</script>

<style scoped>
.srs-review-card {
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

.circuit-overlay {
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
  animation: circuitPulse 10s ease-in-out infinite;
}

@keyframes circuitPulse {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.5; }
}

.pulse-glow {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 700px;
  height: 700px;
  background: radial-gradient(circle, rgba(0, 229, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
  animation: pulse 8s ease-in-out infinite;
}

@keyframes pulse {
  0%, 100% { transform: translate(-50%, -50%) scale(1); opacity: 0.3; }
  50% { transform: translate(-50%, -50%) scale(1.3); opacity: 0.6; }
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
  border-bottom: 1px solid rgba(0, 229, 255, 0.2);
}

.card-header h3 {
  margin: 0;
  font-size: 1.5rem;
  font-weight: 900;
  letter-spacing: 4px;
  color: var(--color-text-primary);
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.card-header .bracket {
  color: var(--color-accent-cyan);
  font-size: 1rem;
  text-shadow: 0 0 10px var(--color-accent-cyan);
}

.word-count {
  background: rgba(0, 229, 255, 0.1);
  border: 1px solid rgba(0, 229, 255, 0.3);
  padding: 0.5rem 1rem;
  border-radius: var(--radius-sm);
  font-size: 0.85rem;
  font-weight: 700;
  letter-spacing: 2px;
  color: var(--color-accent-cyan);
  box-shadow: 0 0 10px rgba(0, 229, 255, 0.2);
}

.words-grid {
  flex: 1;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1.5rem;
  overflow-y: auto;
  padding: 1rem;
}

.word-item {
  position: relative;
  background: rgba(17, 19, 24, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 229, 255, 0.2);
  padding: 1.5rem;
  border-radius: var(--radius-lg);
  text-align: center;
  cursor: pointer;
  transition: all 0.3s;
  overflow: hidden;
}

.word-item::before {
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

.word-item:hover {
  border-color: var(--color-accent-cyan);
  transform: translateY(-4px);
  box-shadow: var(--shadow-cyan);
}

.word-item:hover::before {
  transform: scaleX(1);
}

.word-glow {
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

.word-item:hover .word-glow {
  opacity: 0.3;
}

.hanzi {
  font-size: 2.5rem;
  font-weight: 900;
  color: var(--color-text-primary);
  text-shadow: 0 0 10px var(--color-accent-cyan);
  margin-bottom: 0.5rem;
}

.pinyin {
  font-size: 1rem;
  color: var(--color-text-secondary);
  margin-bottom: 0.75rem;
  letter-spacing: 1px;
}

.translation {
  font-size: 0.95rem;
  color: var(--color-text-primary);
  margin-bottom: 1rem;
  font-weight: 500;
}

.srs-info {
  display: flex;
  justify-content: center;
  gap: 1rem;
  font-size: 0.8rem;
}

.srs-info .level {
  background: rgba(0, 229, 255, 0.15);
  border: 1px solid rgba(0, 229, 255, 0.3);
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-sm);
  color: var(--color-accent-cyan);
  font-weight: 700;
  letter-spacing: 1px;
}

.srs-info .reviews {
  color: var(--color-text-muted);
  font-weight: 600;
}

.card-footer {
  text-align: center;
  padding: 1rem;
  border-top: 1px solid rgba(0, 229, 255, 0.2);
}

.instruction {
  color: var(--color-accent-cyan);
  font-size: 0.85rem;
  font-weight: 600;
  letter-spacing: 2px;
  margin: 0;
  text-shadow: 0 0 10px var(--color-accent-cyan);
}
</style>
