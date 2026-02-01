<template>
  <div class="home-view">
    <!-- Animated Neon Background -->
    <div class="bg-effects">
      <div class="grid-lines"></div>
      <div class="scanlines"></div>
      <div class="particles"></div>
      <div class="glitch-orbs"></div>
      <div class="dragon-logo">龍</div>
    </div>

    <div class="content">
      <!-- Logo Section -->
      <div class="logo-section">
        <h1 class="logo">
          <span class="dragon">龍</span>
          <span class="logo-text text-gradient-rainbow">DRAG'N'SCROLL</span>
        </h1>
        <p class="tagline">
          <span class="highlight text-glow-cyan">MASTER</span>
          <span class="normal">CHINESE</span>
          <span class="highlight text-glow-pink">WITH POWER</span>
        </p>
        <div class="tech-line"></div>
      </div>

      <!-- Auth Section -->
      <div v-if="!isAuthenticated" class="auth-section">
        <div class="neon-card">
          <div class="card-glow"></div>
          <h2 class="cyber-title">
            <span class="icon">⚡</span>
            <span class="title-text text-gradient-cyan">INITIALIZE</span>
          </h2>
          <p class="subtitle">Begin your journey into Chinese mastery</p>

          <div class="features-grid">
            <div class="feature-item">
              <div class="feature-icon glow-pink">📱</div>
              <div class="feature-text">TikTok Interface</div>
            </div>
            <div class="feature-item">
              <div class="feature-icon glow-cyan">🧠</div>
              <div class="feature-text">AI-Powered SRS</div>
            </div>
            <div class="feature-item">
              <div class="feature-icon glow-yellow">⚡</div>
              <div class="feature-text">Fast Learning</div>
            </div>
          </div>

          <div class="buttons">
            <button @click="goToLogin" class="neon-button neon-button-pink">
              <span class="btn-text">LOGIN</span>
              <span class="btn-glitch"></span>
            </button>
            <button @click="goToRegister" class="neon-button">
              <span class="btn-text">REGISTER</span>
              <span class="btn-glitch"></span>
            </button>
          </div>
        </div>
      </div>

      <!-- Logged In Section -->
      <div v-else class="user-section">
        <div class="neon-card">
          <div class="card-glow"></div>
          <h2 class="cyber-title">
            <span class="icon">🎮</span>
            <span class="title-text text-gradient-rainbow">WELCOME BACK</span>
          </h2>
          <p class="subtitle">{{ user?.username }} is ready to train</p>

          <div class="stats-grid">
            <div class="stat-card stat-pink">
              <div class="stat-value text-glow-pink">{{ progress?.total_xp || 0 }}</div>
              <div class="stat-label">TOTAL XP</div>
              <div class="stat-bar"></div>
            </div>
            <div class="stat-card stat-cyan">
              <div class="stat-value text-glow-cyan">{{ progress?.streak_days || 0 }}</div>
              <div class="stat-label">STREAK</div>
              <div class="stat-bar"></div>
            </div>
            <div class="stat-card stat-yellow">
              <div class="stat-value text-glow-yellow">{{ progress?.current_day || 1 }}</div>
              <div class="stat-label">DAY</div>
              <div class="stat-bar"></div>
            </div>
          </div>

          <div class="actions">
            <button @click="continueLearning" class="neon-button neon-button-large">
              <span class="btn-icon">▶</span>
              <span class="btn-text">CONTINUE TRAINING</span>
              <span class="btn-glitch"></span>
            </button>

            <div class="action-buttons">
              <button @click="goToVocab" class="action-card">
                <span class="card-icon">📚</span>
                <span class="card-text">VOCAB</span>
              </button>
              <button @click="goToReview" class="action-card">
                <span class="card-icon">🔄</span>
                <span class="card-text">REVIEW</span>
              </button>
              <button @click="goToVideos" class="action-card action-card-highlight">
                <span class="card-icon">🎬</span>
                <span class="card-text">VIDEOS</span>
              </button>
              <button @click="goToChat" class="action-card action-card-highlight">
                <span class="card-icon">💬</span>
                <span class="card-text">CHAT</span>
              </button>
              <button @click="goToProfile" class="action-card">
                <span class="card-icon">👤</span>
                <span class="card-text">PROFILE</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const user = computed(() => authStore.user)
const progress = computed(() => authStore.user?.progress)
const isAuthenticated = computed(() => authStore.isAuthenticated)

onMounted(async () => {
  await authStore.loadUser()
})

function goToLogin() {
  router.push('/login')
}

function goToRegister() {
  router.push('/register')
}

function continueLearning() {
  router.push('/learn')
}

function goToVocab() {
  router.push('/vocab')
}

function goToReview() {
  router.push('/review')
}

function goToProfile() {
  router.push('/profile')
}

function goToVideos() {
  router.push('/videos')
}

function goToChat() {
  router.push('/chat')
}
</script>

<style scoped>
.home-view {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
  overflow: hidden;
  background: var(--color-bg-primary);
}

/* ============================================
   NEON BACKGROUND EFFECTS
   ============================================ */

.bg-effects {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  pointer-events: none;
}

.grid-lines {
  position: absolute;
  width: 100%;
  height: 100%;
  background-image:
    linear-gradient(var(--color-neon-cyan-light) 1px, transparent 1px),
    linear-gradient(90deg, var(--color-neon-cyan-light) 1px, transparent 1px);
  background-size: 50px 50px;
  animation: gridMove 20s linear infinite;
}

@keyframes gridMove {
  0% { transform: translate(0, 0); }
  100% { transform: translate(50px, 50px); }
}

.scanlines {
  position: absolute;
  width: 100%;
  height: 100%;
  background: repeating-linear-gradient(
    0deg,
    rgba(0, 0, 0, 0.1) 0px,
    rgba(0, 0, 0, 0.1) 1px,
    transparent 1px,
    transparent 3px
  );
  pointer-events: none;
  opacity: 0.3;
}

.particles {
  position: absolute;
  width: 100%;
  height: 100%;
}

.particles::before,
.particles::after {
  content: '';
  position: absolute;
  width: 4px;
  height: 4px;
  background: var(--color-neon-cyan);
  border-radius: 50%;
  box-shadow:
    0 0 10px var(--color-neon-cyan),
    0 0 20px var(--color-neon-cyan),
    0 0 30px var(--color-neon-cyan);
  animation: float 8s infinite ease-in-out;
}

.particles::before {
  left: 20%;
  top: 30%;
  animation-delay: 0s;
}

.particles::after {
  left: 80%;
  top: 70%;
  animation-delay: 4s;
  background: var(--color-neon-pink);
  box-shadow:
    0 0 10px var(--color-neon-pink),
    0 0 20px var(--color-neon-pink),
    0 0 30px var(--color-neon-pink);
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) translateX(0) scale(1);
    opacity: 1;
  }
  25% {
    transform: translateY(-30px) translateX(15px) scale(1.2);
    opacity: 0.8;
  }
  50% {
    transform: translateY(-60px) translateX(-15px) scale(1);
    opacity: 1;
  }
  75% {
    transform: translateY(-30px) translateX(30px) scale(1.1);
    opacity: 0.9;
  }
}

.glitch-orbs {
  position: absolute;
  width: 100%;
  height: 100%;
}

.glitch-orbs::before,
.glitch-orbs::after {
  content: '';
  position: absolute;
  width: 100px;
  height: 100px;
  border-radius: 50%;
  filter: blur(40px);
  animation: orbFloat 15s infinite ease-in-out;
}

.glitch-orbs::before {
  top: 10%;
  right: 10%;
  background: var(--color-neon-pink);
  opacity: 0.15;
  animation-delay: 0s;
}

.glitch-orbs::after {
  bottom: 10%;
  left: 10%;
  background: var(--color-neon-cyan);
  opacity: 0.15;
  animation-delay: 7.5s;
}

@keyframes orbFloat {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -30px) scale(1.2);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.8);
  }
}

.dragon-logo {
  position: absolute;
  top: 10%;
  right: 15%;
  font-size: 12rem;
  opacity: 0.05;
  color: var(--color-neon-red);
  filter: blur(1px);
  animation: dragonFloat 40s ease-in-out infinite;
  pointer-events: none;
  font-weight: 900;
}

@keyframes dragonFloat {
  0%, 100% { transform: translateY(0) rotate(0deg); }
  25% { transform: translateY(-40px) rotate(3deg); }
  50% { transform: translateY(-20px) rotate(-2deg); }
  75% { transform: translateY(-50px) rotate(1deg); }
}

.content {
  position: relative;
  z-index: 1;
  width: 100%;
  max-width: 700px;
  padding: 2rem;
}

/* ============================================
   LOGO SECTION
   ============================================ */

.logo-section {
  text-align: center;
  margin-bottom: 3rem;
}

.logo {
  font-size: 3.5rem;
  font-weight: 900;
  margin: 0 0 1rem 0;
  text-transform: uppercase;
  letter-spacing: 4px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.5rem;
}

.logo .dragon {
  font-size: 5rem;
  color: var(--color-neon-red);
  text-shadow:
    0 0 20px var(--color-neon-red),
    0 0 40px var(--color-neon-red),
    0 0 60px var(--color-neon-red),
    0 0 80px rgba(255, 0, 60, 0.5);
  animation: neonPulse 3s ease-in-out infinite;
}

.logo-text {
  font-size: 2.5rem;
  letter-spacing: 8px;
}

.tagline {
  font-size: 1rem;
  margin: 1rem 0;
  letter-spacing: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
}

.tagline .highlight {
  font-weight: 700;
  font-size: 1.2rem;
}

.tagline .normal {
  color: var(--color-text-muted);
  font-weight: 400;
}

.tech-line {
  width: 150px;
  height: 3px;
  background: var(--gradient-neon-cyber);
  margin: 2rem auto 0;
  border-radius: var(--radius-full);
  box-shadow: var(--shadow-glow-cyan);
  animation: borderGlow 6s ease-in-out infinite;
}

/* ============================================
   NEON CARD
   ============================================ */

.neon-card {
  position: relative;
  background: var(--color-bg-card);
  backdrop-filter: blur(20px);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-2xl);
  padding: var(--spacing-2xl);
  overflow: hidden;
  transition: all var(--transition-slow);
}

.neon-card::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: var(--gradient-neon-cyber);
  animation: rotateGradient 10s linear infinite;
  opacity: 0;
  transition: opacity var(--transition-slow);
  z-index: -1;
}

@keyframes rotateGradient {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.neon-card:hover {
  border-color: var(--color-neon-cyan);
  box-shadow:
    var(--shadow-card),
    var(--shadow-glow-cyan),
    inset 0 0 30px rgba(0, 245, 255, 0.1);
  transform: translateY(-4px);
}

.neon-card:hover::before {
  opacity: 0.1;
}

.card-glow {
  position: absolute;
  top: -2px;
  left: -2px;
  right: -2px;
  bottom: -2px;
  background: var(--gradient-neon-rainbow);
  border-radius: var(--radius-2xl);
  z-index: -2;
  opacity: 0;
  filter: blur(20px);
  transition: opacity var(--transition-slow);
  animation: rainbowFlow 3s linear infinite;
}

.neon-card:hover .card-glow {
  opacity: 0.3;
}

/* ============================================
   CYBER TITLE
   ============================================ */

.cyber-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  margin: 0 0 0.5rem 0;
  font-size: 2rem;
  letter-spacing: 6px;
}

.cyber-title .icon {
  font-size: 2.5rem;
  animation: neonPulse 2s ease-in-out infinite;
}

.title-text {
  font-weight: 900;
}

.subtitle {
  text-align: center;
  color: var(--color-text-muted);
  margin-bottom: 2rem;
  font-size: 1rem;
  letter-spacing: 1px;
}

/* ============================================
   FEATURES GRID
   ============================================ */

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin-bottom: 2rem;
}

.feature-item {
  background: var(--color-bg-elevated);
  border: 2px solid var(--color-border-primary);
  padding: 2rem 1rem;
  border-radius: var(--radius-lg);
  text-align: center;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.feature-item::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-neon-cyber);
  transform: scaleX(0);
  transition: transform var(--transition-base);
}

.feature-item:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-neon-cyan);
  transform: translateY(-4px);
  box-shadow: var(--shadow-glow-cyan);
}

.feature-item:hover::before {
  transform: scaleX(1);
}

.feature-icon {
  font-size: 2.5rem;
  margin-bottom: 1rem;
  border-radius: var(--radius-full);
  padding: 0.5rem;
  transition: all var(--transition-base);
}

.feature-item:hover .feature-icon {
  transform: scale(1.1) rotate(5deg);
}

.feature-text {
  color: var(--color-text-secondary);
  font-size: 0.9rem;
  font-weight: 600;
  letter-spacing: 1px;
}

/* ============================================
   BUTTONS
   ============================================ */

.buttons {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.neon-button {
  position: relative;
  background: transparent;
  border: 2px solid var(--color-neon-cyan);
  color: var(--color-neon-cyan);
  padding: 1.25rem 2rem;
  font-size: 1.1rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 3px;
  cursor: pointer;
  transition: all var(--transition-base);
  clip-path: polygon(20px 0, 100% 0, 100% calc(100% - 20px), calc(100% - 20px) 100%, 0 100%, 0 20px);
  overflow: hidden;
}

.neon-button::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: var(--gradient-cyan);
  transition: left var(--transition-slow);
  z-index: -1;
}

.neon-button:hover::before {
  left: 0;
}

.neon-button:hover {
  color: var(--color-bg-primary);
  box-shadow: var(--shadow-glow-cyan);
  text-shadow: none;
  transform: translateY(-2px);
}

.neon-button:active {
  transform: translateY(0);
}

.neon-button-pink {
  border-color: var(--color-neon-pink);
  color: var(--color-neon-pink);
}

.neon-button-pink::before {
  background: var(--gradient-pink);
}

.neon-button-pink:hover {
  box-shadow: var(--shadow-glow-pink);
}

.neon-button-large {
  width: 100%;
  padding: 1.75rem;
  font-size: 1.3rem;
  margin-bottom: 2rem;
}

.btn-icon {
  margin-right: 0.75rem;
  font-size: 1.2rem;
}

.btn-text {
  position: relative;
  z-index: 1;
}

/* ============================================
   STATS GRID
   ============================================ */

.stats-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
  margin: 2rem 0;
}

.stat-card {
  background: var(--color-bg-elevated);
  border: 2px solid;
  padding: 2rem 1rem;
  border-radius: var(--radius-lg);
  text-align: center;
  position: relative;
  overflow: hidden;
  transition: all var(--transition-base);
}

.stat-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
}

.stat-pink {
  border-color: var(--color-neon-pink);
}

.stat-pink::before {
  background: var(--gradient-pink);
}

.stat-pink:hover {
  box-shadow: var(--shadow-glow-pink);
  transform: translateY(-4px);
}

.stat-cyan {
  border-color: var(--color-neon-cyan);
}

.stat-cyan::before {
  background: var(--gradient-cyan);
}

.stat-cyan:hover {
  box-shadow: var(--shadow-glow-cyan);
  transform: translateY(-4px);
}

.stat-yellow {
  border-color: var(--color-neon-yellow);
}

.stat-yellow::before {
  background: var(--gradient-yellow);
}

.stat-yellow:hover {
  box-shadow: var(--shadow-glow-yellow);
  transform: translateY(-4px);
}

.stat-value {
  font-size: 2.5rem;
  font-weight: 900;
  margin-bottom: 0.5rem;
  display: block;
}

.stat-label {
  font-size: 0.75rem;
  letter-spacing: 3px;
  color: var(--color-text-muted);
  font-weight: 700;
  text-transform: uppercase;
}

.stat-bar {
  height: 3px;
  background: var(--color-border-primary);
  margin-top: 1rem;
  border-radius: var(--radius-full);
  overflow: hidden;
  position: relative;
}

.stat-pink .stat-bar {
  background: var(--color-neon-pink-light);
}

.stat-cyan .stat-bar {
  background: var(--color-neon-cyan-light);
}

.stat-yellow .stat-bar {
  background: var(--color-neon-yellow-light);
}

/* ============================================
   ACTION BUTTONS
   ============================================ */

.action-buttons {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1rem;
}

.action-card {
  background: var(--color-bg-elevated);
  border: 2px solid var(--color-border-primary);
  padding: 2rem 1rem;
  border-radius: var(--radius-lg);
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: all var(--transition-base);
  position: relative;
  overflow: hidden;
}

.action-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 2px;
  background: var(--gradient-neon-cyber);
  transform: scaleX(0);
  transition: transform var(--transition-base);
}

.action-card:hover {
  background: var(--color-bg-hover);
  border-color: var(--color-neon-cyan);
  box-shadow: var(--shadow-glow-cyan);
  transform: translateY(-4px);
}

.action-card:hover::before {
  transform: scaleX(1);
}

.card-icon {
  font-size: 2.5rem;
  transition: transform var(--transition-base);
}

.action-card:hover .card-icon {
  transform: scale(1.15);
}

.card-text {
  font-size: 0.85rem;
  font-weight: 700;
  color: var(--color-text-secondary);
  letter-spacing: 2px;
  text-transform: uppercase;
}

.action-card-highlight {
  background: linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(180, 0, 255, 0.1) 100%);
  border-color: var(--color-neon-cyan);
  position: relative;
  overflow: hidden;
}

.action-card-highlight::after {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.15), transparent);
  animation: shimmer 3s infinite;
}

@keyframes shimmer {
  0% {
    left: -100%;
  }
  100% {
    left: 100%;
  }
}

.action-card-highlight:hover {
  background: linear-gradient(135deg, rgba(0, 245, 255, 0.2) 0%, rgba(180, 0, 255, 0.2) 100%);
  transform: translateY(-6px) scale(1.05);
  box-shadow:
    0 0 30px var(--color-neon-cyan-glow),
    var(--shadow-glow-cyan);
}

.action-card-highlight .card-text {
  color: var(--color-neon-cyan);
}

/* ============================================
   RESPONSIVE DESIGN
   ============================================ */

@media (max-width: 768px) {
  .logo {
    font-size: 2.5rem;
  }

  .logo .dragon {
    font-size: 4rem;
  }

  .logo-text {
    font-size: 1.8rem;
    letter-spacing: 4px;
  }

  .tagline {
    flex-direction: column;
    gap: 0.5rem;
    letter-spacing: 6px;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .action-buttons {
    grid-template-columns: 1fr;
  }

  .neon-button-large {
    padding: 1.5rem;
    font-size: 1.1rem;
  }
}

@media (max-width: 480px) {
  .content {
    padding: 1rem;
  }

  .neon-card {
    padding: var(--spacing-lg);
  }

  .dragon-logo {
    font-size: 6rem;
  }
}
</style>
