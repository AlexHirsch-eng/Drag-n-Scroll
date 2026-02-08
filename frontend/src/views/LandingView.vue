<template>
  <div class="landing-view">
    <!-- Hero Section -->
    <section class="hero">
      <div class="hero-content">
        <h1 class="hero-title">
          <span class="dragon">龍</span>
          <span class="title-text">DRAG'N'SCROLL</span>
        </h1>
        <p class="hero-tagline">
          Master Chinese with AI-Powered Learning
        </p>
        <p class="hero-subtitle">
          TikTok-style interface • Smart SRS • Real Conversations
        </p>
        <div class="hero-ctas">
          <button @click="goToRegister" class="cta-button cta-primary">
            <span class="btn-icon">🚀</span>
            <span class="btn-text">Get Started Free</span>
          </button>
          <button @click="goToApp" class="cta-button cta-secondary">
            <span class="btn-icon">▶</span>
            <span class="btn-text">Open App</span>
          </button>
        </div>
      </div>
      <div class="hero-visual">
        <div class="floating-card card-1">📱</div>
        <div class="floating-card card-2">🧠</div>
        <div class="floating-card card-3">⚡</div>
      </div>
    </section>

    <!-- Features Section -->
    <section class="features-section">
      <div class="section-container">
        <h2 class="section-title">Why Drag'n'Scroll?</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">📱</div>
            <h3 class="feature-title">TikTok-Style Interface</h3>
            <p class="feature-description">
              Swipe through lessons vertically just like your favorite short video app. Intuitive, engaging, and addictive in the best way possible.
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🧠</div>
            <h3 class="feature-title">AI-Powered SRS</h3>
            <p class="feature-description">
              Our smart spaced repetition system learns your weak points and schedules reviews at the perfect time for maximum retention.
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">💬</div>
            <h3 class="feature-title">AI Chat Practice</h3>
            <p class="feature-description">
              Practice real conversations with our AI chatbot. Get instant feedback and improve your speaking skills naturally.
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📚</div>
            <h3 class="feature-title">Video Community</h3>
            <p class="feature-description">
              Share your learning journey, watch others progress, and connect with fellow Chinese learners from around the world.
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">🎯</div>
            <h3 class="feature-title">Gamified Learning</h3>
            <p class="feature-description">
              Earn scrolls, unlock achievements, maintain streaks, and compete with friends. Learning has never been this fun.
            </p>
          </div>
          <div class="feature-card">
            <div class="feature-icon">📖</div>
            <h3 class="feature-title">Structured Curriculum</h3>
            <p class="feature-description">
              Follow a carefully designed learning path from HSK 1 to HSK 6. Build your vocabulary step by step with daily lessons.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section class="how-it-works">
      <div class="section-container">
        <h2 class="section-title">How It Works</h2>
        <div class="steps">
          <div class="step">
            <div class="step-number">1</div>
            <h3 class="step-title">Create Account</h3>
            <p class="step-description">
              Sign up for free in seconds. No credit card required. Start your Chinese learning journey today.
            </p>
          </div>
          <div class="step">
            <div class="step-number">2</div>
            <h3 class="step-title">Learn Daily</h3>
            <p class="step-description">
              Complete short daily lessons tailored to your level. Each session takes just 5-10 minutes of your time.
            </p>
          </div>
          <div class="step">
            <div class="step-number">3</div>
            <h3 class="step-title">Master Chinese</h3>
            <p class="step-description">
              Practice with AI-powered reviews, chat with native speakers, and watch your skills grow day by day.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section class="faq-section">
      <div class="section-container">
        <h2 class="section-title">Frequently Asked Questions</h2>
        <div class="faq-list">
          <div class="faq-item" :class="{ active: activeFaq === 0 }" @click="toggleFaq(0)">
            <div class="faq-question">
              <h3>Is Drag'n'Scroll really free?</h3>
              <span class="faq-icon">{{ activeFaq === 0 ? '−' : '+' }}</span>
            </div>
            <div class="faq-answer" v-show="activeFaq === 0">
              <p>Yes! The core app is completely free to use. You get daily lessons, vocabulary practice, and basic features at no cost. Premium features like unlimited AI chat and advanced analytics are available as optional purchases.</p>
            </div>
          </div>

          <div class="faq-item" :class="{ active: activeFaq === 1 }" @click="toggleFaq(1)">
            <div class="faq-question">
              <h3>How much time do I need per day?</h3>
              <span class="faq-icon">{{ activeFaq === 1 ? '−' : '+' }}</span>
            </div>
            <div class="faq-answer" v-show="activeFaq === 1">
              <p>Just 5-10 minutes per day! Our lessons are designed for busy learners. Complete a quick session during your commute, lunch break, or before bed. Consistency beats intensity.</p>
            </div>
          </div>

          <div class="faq-item" :class="{ active: activeFaq === 2 }" @click="toggleFaq(2)">
            <div class="faq-question">
              <h3>What Chinese level do I need?</h3>
              <span class="faq-icon">{{ activeFaq === 2 ? '−' : '+' }}</span>
            </div>
            <div class="faq-answer" v-show="activeFaq === 2">
              <p>None! Drag'n'Scroll is perfect for absolute beginners. We'll start you from scratch with pinyin and basic greetings, then gradually build up to HSK 1 and beyond.</p>
            </div>
          </div>

          <div class="faq-item" :class="{ active: activeFaq === 3 }" @click="toggleFaq(3)">
            <div class="faq-question">
              <h3>Can I really learn Chinese with an app?</h3>
              <span class="faq-icon">{{ activeFaq === 3 ? '−' : '+' }}</span>
            </div>
            <div class="faq-answer" v-show="activeFaq === 3">
              <p>Yes! While apps work best combined with other learning methods, Drag'n'Scroll provides comprehensive vocabulary, grammar, conversation practice, and character writing. Many users successfully reach conversational level.</p>
            </div>
          </div>

          <div class="faq-item" :class="{ active: activeFaq === 4 }" @click="toggleFaq(4)">
            <div class="faq-question">
              <h3>What is HSK?</h3>
              <span class="faq-icon">{{ activeFaq === 4 ? '−' : '+' }}</span>
            </div>
            <div class="faq-answer" v-show="activeFaq === 4">
              <p>HSK (Hanyu Shuiping Kaoshi) is China's official standardized test of Chinese language proficiency. It ranges from HSK 1 (beginner) to HSK 6 (advanced/master). Drag'n'Scroll prepares you for all levels.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta-section">
      <div class="section-container">
        <h2 class="cta-title">Ready to Start Your Journey?</h2>
        <p class="cta-subtitle">Join thousands of learners mastering Chinese every day</p>
        <button @click="goToRegister" class="cta-button cta-large">
          <span class="btn-icon">🚀</span>
          <span class="btn-text">Start Learning Now - It's Free</span>
        </button>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-content">
        <div class="footer-section">
          <h4>Drag'n'Scroll</h4>
          <p>The most fun way to learn Chinese</p>
        </div>
        <div class="footer-section">
          <h4>Product</h4>
          <a @click="goToApp" class="footer-link">Features</a>
          <a @click="goToRegister" class="footer-link">Pricing</a>
          <a href="https://github.com/AlexHirsch-eng/Drag-n-Scroll" target="_blank" class="footer-link">GitHub</a>
        </div>
        <div class="footer-section">
          <h4>Company</h4>
          <a href="https://github.com/AlexHirsch-eng/Drag-n-Scroll" target="_blank" class="footer-link">About</a>
          <a href="https://github.com/AlexHirsch-eng/Drag-n-Scroll" target="_blank" class="footer-link">Blog</a>
        </div>
      </div>
      <div class="footer-bottom">
        <p>&copy; {{ currentYear }} Drag'n'Scroll. All rights reserved.</p>
        <p class="github-link">
          <a href="https://github.com/AlexHirsch-eng/Drag-n-Scroll" target="_blank">
            ⭐ Star us on GitHub
          </a>
        </p>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const activeFaq = ref<number | null>(null)
const currentYear = computed(() => new Date().getFullYear())

function toggleFaq(index: number) {
  if (activeFaq.value === index) {
    activeFaq.value = null
  } else {
    activeFaq.value = index
  }
}

function goToRegister() {
  router.push('/register')
}

function goToApp() {
  // If user is logged in, go to learn, otherwise go to register
  router.push('/learn')
}
</script>

<style scoped>
.landing-view {
  min-height: 100vh;
  background: var(--color-bg-primary);
  overflow-x: hidden;
}

/* ============================================
   HERO SECTION
   ============================================ */

.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 2rem;
  position: relative;
  background:
    radial-gradient(circle at 20% 50%, rgba(0, 229, 255, 0.1) 0%, transparent 50%),
    radial-gradient(circle at 80% 50%, rgba(255, 46, 46, 0.1) 0%, transparent 50%);
}

.hero-content {
  max-width: 700px;
  text-align: center;
  position: relative;
  z-index: 2;
}

.hero-title {
  font-size: 4rem;
  font-weight: 900;
  margin: 0 0 1rem 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  letter-spacing: 4px;
  animation: fadeInDown 1s ease-out;
}

@keyframes fadeInDown {
  from {
    opacity: 0;
    transform: translateY(-30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.dragon {
  font-size: 5rem;
  color: var(--color-neon-red);
  text-shadow:
    0 0 20px var(--color-neon-red),
    0 0 40px var(--color-neon-red),
    0 0 60px rgba(255, 0, 60, 0.5);
  animation: dragonFloat 6s ease-in-out infinite;
}

@keyframes dragonFloat {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-20px) rotate(3deg);
  }
}

.title-text {
  background: var(--gradient-neon-rainbow);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  font-size: 3rem;
  letter-spacing: 8px;
}

.hero-tagline {
  font-size: 1.5rem;
  margin: 0 0 0.5rem 0;
  color: var(--color-text-secondary);
  font-weight: 600;
  letter-spacing: 2px;
  animation: fadeInDown 1s ease-out 0.2s both;
}

.hero-subtitle {
  font-size: 1.1rem;
  margin: 0 0 2rem 0;
  color: var(--color-text-muted);
  letter-spacing: 1px;
  animation: fadeInDown 1s ease-out 0.4s both;
}

.hero-ctas {
  display: flex;
  gap: 1rem;
  justify-content: center;
  flex-wrap: wrap;
  animation: fadeInUp 1s ease-out 0.6s both;
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.cta-button {
  padding: 1.25rem 2.5rem;
  font-size: 1.1rem;
  font-weight: 700;
  letter-spacing: 2px;
  border: none;
  border-radius: var(--radius-lg);
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 0.75rem;
}

.cta-primary {
  background: var(--gradient-neon-cyber);
  color: var(--color-bg-primary);
  box-shadow: var(--shadow-glow-cyan);
}

.cta-primary:hover {
  transform: translateY(-3px);
  box-shadow:
    var(--shadow-glow-cyan),
    0 0 30px rgba(0, 229, 255, 0.5);
}

.cta-secondary {
  background: transparent;
  border: 2px solid var(--color-neon-cyan);
  color: var(--color-neon-cyan);
}

.cta-secondary:hover {
  background: rgba(0, 229, 255, 0.1);
  transform: translateY(-3px);
  box-shadow: var(--shadow-glow-cyan);
}

.cta-large {
  padding: 1.5rem 3rem;
  font-size: 1.2rem;
}

.btn-icon {
  font-size: 1.3rem;
}

.hero-visual {
  position: absolute;
  width: 100%;
  height: 100%;
  top: 0;
  left: 0;
  pointer-events: none;
  z-index: 1;
}

.floating-card {
  position: absolute;
  background: var(--color-bg-card);
  backdrop-filter: blur(20px);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-xl);
  padding: 2rem;
  font-size: 3rem;
  opacity: 0.1;
  animation: float 6s ease-in-out infinite;
  box-shadow: var(--shadow-card);
}

.card-1 {
  top: 20%;
  left: 10%;
  animation-delay: 0s;
}

.card-2 {
  top: 60%;
  right: 10%;
  animation-delay: 2s;
}

.card-3 {
  bottom: 20%;
  left: 20%;
  animation-delay: 4s;
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-30px) rotate(5deg);
  }
}

/* ============================================
   SECTIONS
   ============================================ */

section {
  padding: 5rem 2rem;
}

.section-container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  font-size: 2.5rem;
  font-weight: 900;
  text-align: center;
  margin: 0 0 3rem 0;
  letter-spacing: 2px;
  background: var(--gradient-neon-cyber);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

/* ============================================
   FEATURES SECTION
   ============================================ */

.features-section {
  background: rgba(0, 0, 0, 0.2);
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}

.feature-card {
  background: var(--color-bg-card);
  backdrop-filter: blur(20px);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-xl);
  padding: 2rem;
  transition: all 0.3s;
  position: relative;
  overflow: hidden;
}

.feature-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 3px;
  background: var(--gradient-neon-cyber);
  transform: scaleX(0);
  transition: transform 0.3s;
}

.feature-card:hover {
  transform: translateY(-5px);
  border-color: var(--color-neon-cyan);
  box-shadow:
    var(--shadow-card),
    var(--shadow-glow-cyan);
}

.feature-card:hover::before {
  transform: scaleX(1);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  color: var(--color-neon-cyan);
}

.feature-description {
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0;
}

/* ============================================
   HOW IT WORKS SECTION
   ============================================ */

.how-it-works {
  background: var(--color-bg-elevated);
}

.steps {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 3rem;
  text-align: center;
}

.step {
  position: relative;
  padding: 2rem;
}

.step-number {
  width: 80px;
  height: 80px;
  background: var(--gradient-neon-cyber);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 900;
  margin: 0 auto 1.5rem;
  box-shadow:
    var(--shadow-glow-cyan),
    0 0 30px rgba(0, 229, 255, 0.3);
}

.step-title {
  font-size: 1.3rem;
  font-weight: 700;
  margin: 0 0 1rem 0;
  color: var(--color-neon-cyan);
}

.step-description {
  color: var(--color-text-secondary);
  line-height: 1.6;
  margin: 0;
}

/* ============================================
   FAQ SECTION
   ============================================ */

.faq-section {
  background: rgba(0, 0, 0, 0.2);
}

.faq-list {
  max-width: 800px;
  margin: 0 auto;
}

.faq-item {
  background: var(--color-bg-card);
  backdrop-filter: blur(20px);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  margin-bottom: 1rem;
  overflow: hidden;
  transition: all 0.3s;
}

.faq-item:hover {
  border-color: var(--color-neon-cyan);
}

.faq-question {
  padding: 1.5rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  cursor: pointer;
  user-select: none;
  gap: 1rem;
  margin: 0;
}

.faq-question h3 {
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
  color: var(--color-text-primary);
  flex: 1;
  text-align: left;
}

.faq-icon {
  font-size: 1.5rem;
  color: var(--color-neon-cyan);
  flex-shrink: 0;
  transition: transform 0.3s;
}

.faq-item:hover .faq-icon {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 1.5rem 1.5rem;
  color: var(--color-text-secondary);
  line-height: 1.6;
  border-top: 1px solid var(--color-border-primary);
}

.faq-answer p {
  margin: 0;
}

/* ============================================
   CTA SECTION
   ============================================ */

.cta-section {
  background: var(--gradient-neon-cyber);
  position: relative;
  overflow: hidden;
}

.cta-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.05)" stroke-width="0.5"/></pattern></defs><rect width="100%" height="100%" fill="url(%23grid)"/></svg>');
  opacity: 0.3;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 900;
  text-align: center;
  margin: 0 0 1rem 0;
  color: var(--color-bg-primary);
  text-shadow: 0 0 20px rgba(0, 229, 255, 0.5);
  position: relative;
  z-index: 1;
}

.cta-subtitle {
  font-size: 1.1rem;
  text-align: center;
  margin: 0 0 2rem 0;
  color: var(--color-bg-primary);
  opacity: 0.9;
  position: relative;
  z-index: 1;
}

/* ============================================
   FOOTER
   ============================================ */

.footer {
  background: var(--color-bg-elevated);
  border-top: 1px solid var(--color-border-primary);
  padding: 3rem 2rem 2rem;
}

.footer-content {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin-bottom: 2rem;
}

.footer-section h4 {
  color: var(--color-neon-cyan);
  margin: 0 0 1rem 0;
  font-size: 1rem;
  letter-spacing: 1px;
}

.footer-section p {
  color: var(--color-text-muted);
  margin: 0;
  line-height: 1.5;
  font-size: 0.9rem;
}

.footer-link {
  display: block;
  color: var(--color-text-muted);
  text-decoration: none;
  margin-bottom: 0.5rem;
  font-size: 0.9rem;
  transition: color 0.3s;
  cursor: pointer;
}

.footer-link:hover {
  color: var(--color-neon-cyan);
}

.footer-bottom {
  max-width: 1200px;
  margin: 0 auto;
  padding-top: 2rem;
  border-top: 1px solid var(--color-border-primary);
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 1rem;
}

.footer-bottom p {
  color: var(--color-text-muted);
  margin: 0;
  font-size: 0.85rem;
}

.github-link a {
  color: var(--color-neon-cyan);
  text-decoration: none;
  transition: color 0.3s;
}

.github-link a:hover {
  color: var(--color-neon-pink);
}

/* ============================================
   RESPONSIVE
   ============================================ */

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }

  .dragon {
    font-size: 3rem;
  }

  .title-text {
    font-size: 2rem;
    letter-spacing: 4px;
  }

  .hero-tagline {
    font-size: 1.2rem;
  }

  .hero-ctas {
    flex-direction: column;
    align-items: center;
  }

  .cta-button {
    width: 100%;
    justify-content: center;
  }

  .section-title {
    font-size: 2rem;
  }

  .steps {
    grid-template-columns: 1fr;
  }

  .footer-content {
    grid-template-columns: 1fr;
  }

  .footer-bottom {
    flex-direction: column;
    text-align: center;
  }

  .floating-card {
    display: none;
  }
}

@media (max-width: 480px) {
  .hero {
    padding: 1rem;
  }

  .section-title {
    font-size: 1.75rem;
  }

  .faq-question {
    padding: 1rem;
  }

  .faq-answer {
    padding: 0 1rem 1rem;
  }
}
</style>
