<template>
  <div class="landing-view">
    <!-- Background Effects -->
    <div class="bg-gradient"></div>
    <div class="bg-blobs">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- Fixed Navbar -->
    <header class="navbar" :class="{ 'navbar-scrolled': isScrolled }">
      <div class="navbar-container">
        <div class="navbar-logo" @click="scrollToTop">
          <span class="logo-icon">龍</span>
          <span class="logo-text">DRAG'N'SCROLL</span>
        </div>
        <nav class="navbar-nav">
          <a @click.prevent="scrollToSection('features')" href="#features" class="nav-link">Features</a>
          <a @click.prevent="scrollToSection('how')" href="#how" class="nav-link">How It Works</a>
          <a @click.prevent="scrollToSection('pricing')" href="#pricing" class="nav-link">Pricing</a>
          <a @click.prevent="scrollToSection('faq')" href="#faq" class="nav-link">FAQ</a>
        </nav>
        <button @click="goToApp" class="navbar-cta">Open App</button>
      </div>
    </header>

    <!-- Hero Section -->
    <section class="hero section-reveal">
      <div class="hero-container">
        <div class="hero-content">
          <h1 class="hero-title">
            <span class="title-dragon">龍</span>
            <span class="title-main">Master Chinese with AI-Powered Learning</span>
          </h1>
          <p class="hero-subtitle">
            TikTok-style interface • Smart SRS • Real Conversations • Daily 5-min lessons
          </p>
          <div class="hero-ctas">
            <button @click="goToApp" class="btn btn-primary">
              <span class="btn-icon">▶</span>
              <span>Open App</span>
            </button>
            <button @click="scrollToSection('how')" class="btn btn-secondary">
              <span class="btn-icon">↓</span>
              <span>How It Works</span>
            </button>
          </div>
        </div>
        <div class="hero-visual">
          <div class="visual-card card-1">
            <img :src="l1" alt="Главная" class="card-image">
            <div class="card-label">Главная</div>
          </div>
          <div class="visual-card card-2">
            <img :src="l2" alt="Уроки" class="card-image">
            <div class="card-label">Уроки</div>
          </div>
          <div class="visual-card card-3">
            <img :src="l5" alt="AI Чат" class="card-image">
            <div class="card-label">AI Чат</div>
          </div>
        </div>
      </div>
    </section>

    <!-- Features Section -->
    <section id="features" class="features section-reveal">
      <div class="features-container">
        <h2 class="section-title">Why Drag'n'Scroll?</h2>
        <div class="features-grid">
          <div class="feature-card glass-card">
            <img :src="l6" alt="Видео" class="feature-image">
            <h3 class="feature-title">Видео уроки</h3>
            <p class="feature-description">
              Листайте видео вертикально как в TikTok. Интуитивно, увлекательно и эффективно.
            </p>
          </div>
          <div class="feature-card glass-card">
            <img :src="l1" alt="Главная" class="feature-image">
            <h3 class="feature-title">Умные повторы</h3>
            <p class="feature-description">
              Система SRS запоминает ваши слабые места и планирует повторы в идеальное время для лучшего запоминания.
            </p>
          </div>
          <div class="feature-card glass-card">
            <img :src="l2" alt="Уроки" class="feature-image">
            <h3 class="feature-title">AI Чат</h3>
            <p class="feature-description">
              Тренируйте реальные разговоры с AI-чатом. Получайте мгновенную обратную связь и улучшайте навыки разговора.
            </p>
          </div>
          <div class="feature-card glass-card">
            <img :src="l4" alt="Видео" class="feature-image">
            <h3 class="feature-title">Сообщество</h3>
            <p class="feature-description">
              Делитесь своим прогрессом, смотрите видео других учеников и общайтесь с изучающими китайский со всего мира.
            </p>
          </div>
          <div class="feature-card glass-card">
            <img :src="l5" alt="AI Чат" class="feature-image">
            <h3 class="feature-title">Геймификация</h3>
            <p class="feature-description">
              Зарабатывайте свитки, открывайте достижения, поддерживайте серию побед и соревнуйтесь с друзьями.
            </p>
          </div>
          <div class="feature-card glass-card">
            <img :src="l3" alt="Профиль" class="feature-image">
            <h3 class="feature-title">Словарь</h3>
            <p class="feature-description">
              Структурированная программа от HSK 1 до HSK 6. Расширяйте словарный запас шаг за шагом с ежедневными уроками.
            </p>
          </div>
        </div>

        <!-- Screenshot Gallery Placeholder -->
        <div class="showcase-section">
          <h3 class="showcase-title">App Screenshots</h3>
          <div class="screenshots-grid">
            <div
              v-for="(screen, index) in screenshots"
              :key="index"
              class="screenshot-placeholder"
            >
              <img
                v-if="screen.loaded"
                :src="screen.src"
                :alt="screen.alt"
                class="screenshot-image"
              />
              <div v-else class="screenshot-placeholder-frame">
                <div class="placeholder-gradient">
                  <div class="placeholder-icon">📱</div>
                  <div class="placeholder-text">{{ screen.alt }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Video Placeholder -->
        <div class="showcase-section">
          <h3 class="showcase-title">See It In Action</h3>
          <div class="video-placeholder">
            <video
              v-if="demoVideoLoaded"
              :src="demoVideoSrc"
              class="demo-video"
              controls
            />
            <div v-else class="video-placeholder-frame">
              <div class="play-button">
                <div class="play-icon">▶</div>
              </div>
              <div class="video-caption">Demo Video Coming Soon</div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- How It Works Section -->
    <section id="how" class="how-it-works section-reveal">
      <div class="how-container">
        <h2 class="section-title">How It Works</h2>
        <div class="steps-container" ref="stepsContainer">
          <div class="steps-progress">
            <div class="progress-line" :style="{ width: progressWidth }"></div>
          </div>
          <div class="steps-list">
            <div
              v-for="(step, index) in steps"
              :key="index"
              class="step-item"
              :class="{ 'step-active': activeStep === index }"
              :ref="el => setStepRef(el, index)"
            >
              <div class="step-marker">
                <div class="step-number">{{ index + 1 }}</div>
              </div>
              <div class="step-content">
                <h3 class="step-title">{{ step.title }}</h3>
                <p class="step-description">{{ step.description }}</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- Pricing Section -->
    <section id="pricing" class="pricing section-reveal">
      <div class="pricing-container">
        <h2 class="section-title">Simple, Transparent Pricing</h2>
        <p class="pricing-subtitle">Choose the plan that fits your learning journey</p>
        <div class="pricing-grid">
          <div class="pricing-card glass-card">
            <div class="pricing-header">
              <h3 class="pricing-title">Starter</h3>
              <div class="pricing-price">Free</div>
              <div class="pricing-period">Forever</div>
            </div>
            <ul class="pricing-features">
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>Daily lessons (5-10 min)</span>
              </li>
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>Basic vocabulary practice</span>
              </li>
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>Spaced repetition reviews</span>
              </li>
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>Progress tracking</span>
              </li>
            </ul>
            <button @click="goToApp" class="pricing-btn">Get Started</button>
          </div>

          <div class="pricing-card pricing-popular glass-card">
            <div class="popular-badge">Most Popular</div>
            <div class="pricing-header">
              <h3 class="pricing-title">Pro</h3>
              <div class="pricing-price">$9.99</div>
              <div class="pricing-period">per month</div>
            </div>
            <ul class="pricing-features">
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>Everything in Starter</span>
              </li>
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>Unlimited AI chat</span>
              </li>
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>Advanced analytics</span>
              </li>
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>Priority support</span>
              </li>
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>No ads</span>
              </li>
            </ul>
            <button @click="goToApp" class="pricing-btn pricing-btn-primary">Upgrade to Pro</button>
          </div>

          <div class="pricing-card glass-card">
            <div class="pricing-header">
              <h3 class="pricing-title">Premium</h3>
              <div class="pricing-price">$99.99</div>
              <div class="pricing-period">per year</div>
            </div>
            <ul class="pricing-features">
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>Everything in Pro</span>
              </li>
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>Save 70% vs monthly</span>
              </li>
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>Exclusive content</span>
              </li>
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>Early access features</span>
              </li>
              <li class="feature-item">
                <span class="check-icon">✓</span>
                <span>VIP support</span>
              </li>
            </ul>
            <button @click="goToApp" class="pricing-btn">Go Premium</button>
          </div>
        </div>
      </div>
    </section>

    <!-- FAQ Section -->
    <section id="faq" class="faq section-reveal">
      <div class="faq-container">
        <h2 class="section-title">Frequently Asked Questions</h2>
        <div class="faq-list">
          <div
            v-for="(item, index) in faqItems"
            :key="index"
            class="faq-item glass-card"
            :class="{ 'faq-active': activeFaq === index }"
            @click="toggleFaq(index)"
          >
            <div class="faq-question">
              <h3 class="faq-question-text">{{ item.question }}</h3>
              <span class="faq-icon">{{ activeFaq === index ? '−' : '+' }}</span>
            </div>
            <div class="faq-answer" v-show="activeFaq === index">
              <p>{{ item.answer }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- CTA Section -->
    <section class="cta section-reveal">
      <div class="cta-container">
        <h2 class="cta-title">Ready to Start Your Journey?</h2>
        <p class="cta-subtitle">Join thousands of learners mastering Chinese every day</p>
        <button @click="goToApp" class="btn btn-cta">
          <span class="btn-icon">🚀</span>
          <span>Start Learning Now - It's Free</span>
        </button>
      </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
      <div class="footer-container">
        <div class="footer-content">
          <div class="footer-section">
            <h4 class="footer-title">Drag'n'Scroll</h4>
            <p class="footer-text">The most fun way to learn Chinese</p>
            <div class="footer-social">
              <a href="https://github.com/AlexHirsch-eng/Drag-n-Scroll" target="_blank" class="social-link">
                <span class="social-icon">⭐</span>
                <span>Star on GitHub</span>
              </a>
            </div>
          </div>
          <div class="footer-section">
            <h4 class="footer-title">Product</h4>
            <a @click="scrollToSection('features')" class="footer-link">Features</a>
            <a @click="scrollToSection('pricing')" class="footer-link">Pricing</a>
            <a href="https://github.com/AlexHirsch-eng/Drag-n-Scroll" target="_blank" class="footer-link">GitHub</a>
          </div>
          <div class="footer-section">
            <h4 class="footer-title">Company</h4>
            <a href="https://github.com/AlexHirsch-eng/Drag-n-Scroll" target="_blank" class="footer-link">About</a>
            <a href="https://github.com/AlexHirsch-eng/Drag-n-Scroll" target="_blank" class="footer-link">Blog</a>
            <a href="mailto:contact@dragnscroll.com" class="footer-link">Contact</a>
          </div>
        </div>
        <div class="footer-bottom">
          <p>&copy; {{ currentYear }} Drag'n'Scroll. All rights reserved.</p>
        </div>
      </div>
    </footer>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import l1 from '@/images/l1.png'
import l2 from '@/images/l2.png'
import l3 from '@/images/l3.png'
import l4 from '@/images/l4.png'
import l5 from '@/images/l5.png'
import l6 from '@/images/l6.png'
import w1 from '@/images/w1.jpeg'
import w2 from '@/images/w2.jpeg'
import w3 from '@/images/w3.jpeg'
import w4 from '@/images/w4.jpeg'
import w5 from '@/images/w5.jpeg'

const router = useRouter()

// State
const isScrolled = ref(false)
const activeFaq = ref<number | null>(null)
const activeStep = ref(0)
const currentYear = computed(() => new Date().getFullYear())
const progressWidth = computed(() => `${(activeStep.value / 2) * 100}%`)

// Asset loading state
const screenshots = ref([
  {
    src: w1,
    alt: 'Скриншот 1',
    loaded: true
  },
  {
    src: w2,
    alt: 'Скриншот 2',
    loaded: true
  },
  {
    src: w3,
    alt: 'Скриншот 3',
    loaded: true
  },
  {
    src: w4,
    alt: 'Скриншот 4',
    loaded: true
  },
  {
    src: w5,
    alt: 'Скриншот 5',
    loaded: true
  }
])

const demoVideoSrc = '/src/assets/demo/demo.mp4'
const demoVideoLoaded = ref(false)

// Steps data
const steps = [
  {
    title: 'Create Account',
    description: 'Sign up for free in seconds. No credit card required. Start your Chinese learning journey today.'
  },
  {
    title: 'Learn Daily',
    description: 'Complete short daily lessons tailored to your level. Each session takes just 5-10 minutes of your time.'
  },
  {
    title: 'Master Chinese',
    description: 'Practice with AI-powered reviews, chat with native speakers, and watch your skills grow day by day.'
  }
]

// FAQ data
const faqItems = [
  {
    question: 'Is Drag\'n\'Scroll really free?',
    answer: 'Yes! The core app is completely free to use. You get daily lessons, vocabulary practice, and basic features at no cost. Premium features like unlimited AI chat and advanced analytics are available as optional purchases.'
  },
  {
    question: 'How much time do I need per day?',
    answer: 'Just 5-10 minutes per day! Our lessons are designed for busy learners. Complete a quick session during your commute, lunch break, or before bed. Consistency beats intensity.'
  },
  {
    question: 'What Chinese level do I need?',
    answer: 'None! Drag\'n\'Scroll is perfect for absolute beginners. We\'ll start you from scratch with pinyin and basic greetings, then gradually build up to HSK 1 and beyond.'
  },
  {
    question: 'Can I really learn Chinese with an app?',
    answer: 'Yes! While apps work best combined with other learning methods, Drag\'n\'Scroll provides comprehensive vocabulary, grammar, conversation practice, and character writing. Many users successfully reach conversational level.'
  },
  {
    question: 'What is HSK?',
    answer: 'HSK (Hanyu Shuiping Kaoshi) is China\'s official standardized test of Chinese language proficiency. It ranges from HSK 1 (beginner) to HSK 6 (advanced/master). Drag\'n\'Scroll prepares you for all levels.'
  },
  {
    question: 'How does the AI chat feature work?',
    answer: 'Our AI chatbot uses advanced language models to simulate real conversations in Chinese. You can practice daily scenarios, get instant corrections, and improve your speaking skills naturally. Available in Pro and Premium plans.'
  }
]

// Refs for scroll tracking
const stepRefs = ref<HTMLElement[]>([])
const stepsContainer = ref<HTMLElement | null>(null)

function setStepRef(el: any, index: number) {
  if (el) {
    stepRefs.value[index] = el
  }
}

// Navigation
function goToApp() {
  router.push('/app')
}

function scrollToTop() {
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function scrollToSection(id: string) {
  const element = document.getElementById(id)
  if (element) {
    const offset = 80 // Navbar height
    const top = element.getBoundingClientRect().top + window.pageYOffset - offset
    window.scrollTo({ top, behavior: 'smooth' })
  }
}

// FAQ toggle
function toggleFaq(index: number) {
  activeFaq.value = activeFaq.value === index ? null : index
}

// Scroll handling
function handleScroll() {
  isScrolled.value = window.scrollY > 50

  // Update active step based on scroll position
  if (stepsContainer.value) {
    const scrollPos = window.pageYOffset + window.innerHeight / 2

    stepRefs.value.forEach((step, index) => {
      if (step) {
        const stepTop = step.getBoundingClientRect().top + window.pageYOffset
        if (scrollPos >= stepTop && scrollPos < stepTop + 300) {
          activeStep.value = index
        }
      }
    })
  }
}

// Intersection Observer for reveal animations
function setupRevealAnimations() {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible')
        }
      })
    },
    {
      threshold: 0.1,
      rootMargin: '0px 0px -50px 0px'
    }
  )

  document.querySelectorAll('.section-reveal').forEach((section) => {
    observer.observe(section)
  })

  return observer
}

// Load assets - images are already imported, no need to fetch
async function loadAssets() {
  // Screenshots are already imported and ready to use
  // Just set them as loaded
  screenshots.value.forEach(screenshot => {
    screenshot.loaded = true
  })

  // Try to load video
  try {
    const response = await fetch(demoVideoSrc)
    if (response.ok) {
      demoVideoLoaded.value = true
    }
  } catch {
    // Keep placeholder
  }
}

// Lifecycle
let revealObserver: IntersectionObserver | null = null

onMounted(() => {
  window.addEventListener('scroll', handleScroll)
  revealObserver = setupRevealAnimations()
  loadAssets()
})

onUnmounted(() => {
  window.removeEventListener('scroll', handleScroll)
  if (revealObserver) {
    revealObserver.disconnect()
  }
})
</script>

<style scoped>
.landing-view {
  min-height: 100vh;
  background: #0a0a0f;
  position: relative;
  overflow-x: hidden;
}

/* ============================================
   BACKGROUND EFFECTS
   ============================================ */

.bg-gradient {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background:
    radial-gradient(ellipse at 20% 30%, rgba(120, 0, 255, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 80% 70%, rgba(0, 229, 255, 0.15) 0%, transparent 50%),
    radial-gradient(ellipse at 50% 50%, rgba(255, 46, 46, 0.08) 0%, transparent 60%);
  z-index: 0;
  pointer-events: none;
}

.bg-blobs {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 0;
  pointer-events: none;
  overflow: hidden;
}

.blob {
  position: absolute;
  border-radius: 50%;
  filter: blur(80px);
  opacity: 0.4;
  animation: blobFloat 20s ease-in-out infinite;
}

.blob-1 {
  width: 600px;
  height: 600px;
  background: rgba(120, 0, 255, 0.3);
  top: -200px;
  left: -200px;
  animation-delay: 0s;
}

.blob-2 {
  width: 500px;
  height: 500px;
  background: rgba(0, 229, 255, 0.3);
  bottom: -150px;
  right: -150px;
  animation-delay: 7s;
}

.blob-3 {
  width: 400px;
  height: 400px;
  background: rgba(255, 46, 46, 0.2);
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  animation-delay: 14s;
}

@keyframes blobFloat {
  0%, 100% {
    transform: translate(0, 0) scale(1);
  }
  33% {
    transform: translate(30px, -50px) scale(1.1);
  }
  66% {
    transform: translate(-20px, 20px) scale(0.9);
  }
}

/* ============================================
   NAVBAR
   ============================================ */

.navbar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  z-index: 1000;
  padding: 1rem 0;
  transition: all 0.3s ease;
}

.navbar-scrolled {
  background: rgba(10, 10, 15, 0.9);
  backdrop-filter: blur(20px);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.navbar-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 2rem;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 2rem;
}

.navbar-logo {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  cursor: pointer;
  transition: transform 0.3s ease;
}

.navbar-logo:hover {
  transform: scale(1.05);
}

.logo-icon {
  font-size: 2rem;
}

.logo-text {
  font-size: 1.2rem;
  font-weight: 900;
  background: linear-gradient(135deg, #00e5ff, #ff2e2e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
}

.navbar-nav {
  display: flex;
  gap: 2rem;
}

.nav-link {
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  font-weight: 600;
  transition: color 0.3s ease;
  cursor: pointer;
}

.nav-link:hover {
  color: #00e5ff;
}

.navbar-cta {
  padding: 0.75rem 1.5rem;
  background: linear-gradient(135deg, #00e5ff, #7800ff);
  border: none;
  border-radius: 50px;
  color: white;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.navbar-cta:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 229, 255, 0.3);
}

/* ============================================
   SECTIONS
   ============================================ */

.section-reveal {
  opacity: 0;
  transform: translateY(30px);
  transition: all 0.7s cubic-bezier(0.4, 0, 0.2, 1);
}

.section-reveal.is-visible {
  opacity: 1;
  transform: translateY(0);
}

section {
  position: relative;
  z-index: 1;
  padding: 6rem 2rem;
}

.section-title {
  font-size: 3rem;
  font-weight: 900;
  text-align: center;
  margin: 0 0 1rem 0;
  background: linear-gradient(135deg, #00e5ff, #7800ff);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
  letter-spacing: 2px;
}

/* ============================================
   HERO SECTION
   ============================================ */

.hero {
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding-top: 6rem;
}

.hero-container {
  max-width: 1200px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 4rem;
  align-items: center;
}

.hero-content {
  z-index: 2;
}

.hero-title {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  margin: 0 0 1.5rem 0;
}

.title-dragon {
  font-size: 5rem;
  color: #ff2e2e;
  text-shadow: 0 0 30px rgba(255, 46, 46, 0.8);
  animation: dragonPulse 3s ease-in-out infinite;
}

@keyframes dragonPulse {
  0%, 100% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.05);
    opacity: 0.8;
  }
}

.title-main {
  font-size: 2.5rem;
  font-weight: 900;
  color: white;
  line-height: 1.2;
}

.hero-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 2rem 0;
  line-height: 1.6;
}

.hero-ctas {
  display: flex;
  gap: 1rem;
}

.btn {
  padding: 1rem 2rem;
  border: none;
  border-radius: 50px;
  font-size: 1.1rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.btn-primary {
  background: linear-gradient(135deg, #00e5ff, #7800ff);
  color: white;
}

.btn-primary:hover {
  transform: translateY(-3px);
  box-shadow: 0 10px 30px rgba(0, 229, 255, 0.4);
}

.btn-secondary {
  background: rgba(255, 255, 255, 0.1);
  color: white;
  border: 2px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
}

.btn-secondary:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.btn-icon {
  font-size: 1.2rem;
}

.hero-visual {
  position: relative;
  height: 500px;
}

.visual-card {
  position: absolute;
  width: 200px;
  height: 380px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(20px);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
  gap: 1rem;
  overflow: hidden;
  animation: floatCard 6s ease-in-out infinite;
}

.card-image {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0.9;
}

.card-1 {
  top: 0;
  left: 0;
  animation-delay: 0s;
}

.card-2 {
  top: 100px;
  right: 50px;
  animation-delay: 2s;
}

.card-3 {
  bottom: 50px;
  left: 50px;
  animation-delay: 4s;
}

@keyframes floatCard {
  0%, 100% {
    transform: translateY(0) rotate(-2deg);
  }
  50% {
    transform: translateY(-20px) rotate(2deg);
  }
}

.card-label {
  font-size: 1rem;
  font-weight: 600;
  color: white;
  text-align: center;
  background: rgba(0, 0, 0, 0.7);
  padding: 0.5rem 1rem;
  border-radius: 20px;
  backdrop-filter: blur(10px);
  position: relative;
  z-index: 1;
  margin-bottom: 1rem;
}

/* ============================================
   FEATURES SECTION
   ============================================ */

.features-container {
  max-width: 1200px;
  margin: 0 auto;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
}

.glass-card {
  background: rgba(255, 255, 255, 0.03);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  padding: 2rem;
  transition: all 0.3s ease;
}

.glass-card:hover {
  background: rgba(255, 255, 255, 0.05);
  border-color: rgba(0, 229, 255, 0.3);
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
}

.feature-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.feature-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
  border-radius: 12px;
  margin-bottom: 1rem;
}

.feature-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0 0 1rem 0;
}

.feature-description {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin: 0;
}

/* Showcase Sections */
.showcase-section {
  margin: 4rem 0;
}

.showcase-title {
  font-size: 2rem;
  font-weight: 700;
  color: white;
  text-align: center;
  margin: 0 0 2rem 0;
}

.screenshots-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 2rem;
}

.screenshot-placeholder {
  aspect-ratio: 9 / 16;
  border-radius: 20px;
  overflow: hidden;
}

.screenshot-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.screenshot-placeholder-frame {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(0, 229, 255, 0.2), rgba(120, 0, 255, 0.2));
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.placeholder-gradient {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 2rem;
}

.placeholder-icon {
  font-size: 4rem;
  opacity: 0.5;
}

.placeholder-text {
  font-size: 1rem;
  color: rgba(255, 255, 255, 0.6);
  text-align: center;
}

.video-placeholder {
  max-width: 800px;
  margin: 0 auto;
  aspect-ratio: 16 / 9;
  border-radius: 20px;
  overflow: hidden;
}

.demo-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.video-placeholder-frame {
  width: 100%;
  height: 100%;
  background: linear-gradient(135deg, rgba(255, 46, 46, 0.2), rgba(120, 0, 255, 0.2));
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 1.5rem;
  position: relative;
}

.play-button {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.3s ease;
}

.play-button:hover {
  background: rgba(255, 255, 255, 0.15);
  transform: scale(1.1);
}

.play-icon {
  font-size: 2rem;
  color: white;
  margin-left: 0.3rem;
}

.video-caption {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.8);
}

/* ============================================
   HOW IT WORKS SECTION
   ============================================ */

.how-container {
  max-width: 900px;
  margin: 0 auto;
}

.steps-container {
  position: relative;
  padding: 2rem 0;
}

.steps-progress {
  position: absolute;
  left: 39px;
  top: 0;
  bottom: 0;
  width: 2px;
  background: rgba(255, 255, 255, 0.1);
}

.progress-line {
  width: 0%;
  height: 100%;
  background: linear-gradient(180deg, #00e5ff, #7800ff);
  transition: width 0.3s ease;
}

.steps-list {
  position: relative;
  display: flex;
  flex-direction: column;
  gap: 3rem;
}

.step-item {
  display: flex;
  gap: 2rem;
  opacity: 0.5;
  transition: all 0.3s ease;
}

.step-item.step-active {
  opacity: 1;
}

.step-marker {
  flex-shrink: 0;
}

.step-number {
  width: 80px;
  height: 80px;
  background: rgba(255, 255, 255, 0.05);
  backdrop-filter: blur(10px);
  border: 2px solid rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: 900;
  color: white;
  transition: all 0.3s ease;
}

.step-active .step-number {
  background: linear-gradient(135deg, #00e5ff, #7800ff);
  border-color: transparent;
  box-shadow: 0 0 30px rgba(0, 229, 255, 0.5);
  transform: scale(1.1);
}

.step-content {
  flex: 1;
  padding-top: 1rem;
}

.step-title {
  font-size: 1.8rem;
  font-weight: 700;
  color: white;
  margin: 0 0 1rem 0;
}

.step-description {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin: 0;
}

/* ============================================
   PRICING SECTION
   ============================================ */

.pricing-container {
  max-width: 1200px;
  margin: 0 auto;
}

.pricing-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.7);
  text-align: center;
  margin: 0 0 3rem 0;
}

.pricing-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
  align-items: start;
}

.pricing-card {
  position: relative;
}

.pricing-popular {
  border-color: rgba(0, 229, 255, 0.5);
  background: rgba(0, 229, 255, 0.05);
}

.popular-badge {
  position: absolute;
  top: -12px;
  left: 50%;
  transform: translateX(-50%);
  background: linear-gradient(135deg, #00e5ff, #7800ff);
  color: white;
  padding: 0.5rem 1.5rem;
  border-radius: 50px;
  font-size: 0.85rem;
  font-weight: 700;
}

.pricing-header {
  text-align: center;
  padding-bottom: 2rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
  margin-bottom: 2rem;
}

.pricing-title {
  font-size: 1.5rem;
  font-weight: 700;
  color: white;
  margin: 0 0 1rem 0;
}

.pricing-price {
  font-size: 3rem;
  font-weight: 900;
  color: white;
  margin: 0.5rem 0;
}

.pricing-period {
  color: rgba(255, 255, 255, 0.6);
  font-size: 1rem;
}

.pricing-features {
  list-style: none;
  padding: 0;
  margin: 0 0 2rem 0;
}

.feature-item {
  display: flex;
  align-items: center;
  gap: 1rem;
  padding: 0.75rem 0;
  color: rgba(255, 255, 255, 0.8);
}

.check-icon {
  color: #00e5ff;
  font-weight: 900;
  font-size: 1.2rem;
}

.pricing-btn {
  width: 100%;
  padding: 1rem;
  background: rgba(255, 255, 255, 0.1);
  border: 2px solid rgba(255, 255, 255, 0.2);
  border-radius: 50px;
  color: white;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s ease;
}

.pricing-btn:hover {
  background: rgba(255, 255, 255, 0.15);
  border-color: rgba(255, 255, 255, 0.3);
}

.pricing-btn-primary {
  background: linear-gradient(135deg, #00e5ff, #7800ff);
  border-color: transparent;
}

.pricing-btn-primary:hover {
  transform: translateY(-2px);
  box-shadow: 0 10px 30px rgba(0, 229, 255, 0.4);
}

/* ============================================
   FAQ SECTION
   ============================================ */

.faq-container {
  max-width: 800px;
  margin: 0 auto;
}

.faq-list {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.faq-item {
  cursor: pointer;
  transition: all 0.3s ease;
}

.faq-item:hover {
  border-color: rgba(0, 229, 255, 0.3);
}

.faq-question {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 1rem;
  padding: 1.5rem;
  margin: 0;
}

.faq-question-text {
  font-size: 1.1rem;
  font-weight: 600;
  color: white;
  margin: 0;
  flex: 1;
  text-align: left;
}

.faq-icon {
  font-size: 1.5rem;
  color: #00e5ff;
  flex-shrink: 0;
  transition: transform 0.3s ease;
}

.faq-active .faq-icon {
  transform: rotate(180deg);
}

.faq-answer {
  padding: 0 1.5rem 1.5rem;
  border-top: 1px solid rgba(255, 255, 255, 0.05);
}

.faq-answer p {
  color: rgba(255, 255, 255, 0.7);
  line-height: 1.6;
  margin: 0;
}

/* ============================================
   CTA SECTION
   ============================================ */

.cta {
  background: linear-gradient(135deg, rgba(0, 229, 255, 0.1), rgba(120, 0, 255, 0.1));
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  border-bottom: 1px solid rgba(255, 255, 255, 0.1);
}

.cta-container {
  max-width: 800px;
  margin: 0 auto;
  text-align: center;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 900;
  color: white;
  margin: 0 0 1rem 0;
}

.cta-subtitle {
  font-size: 1.2rem;
  color: rgba(255, 255, 255, 0.7);
  margin: 0 0 2rem 0;
}

.btn-cta {
  padding: 1.25rem 3rem;
  font-size: 1.2rem;
  background: linear-gradient(135deg, #00e5ff, #7800ff);
  color: white;
}

.btn-cta:hover {
  transform: translateY(-3px);
  box-shadow: 0 15px 40px rgba(0, 229, 255, 0.4);
}

/* ============================================
   FOOTER
   ============================================ */

.footer {
  background: rgba(0, 0, 0, 0.5);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  padding: 4rem 2rem 2rem;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
}

.footer-content {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 3rem;
  margin-bottom: 3rem;
}

.footer-section {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.footer-title {
  color: #00e5ff;
  font-size: 1.1rem;
  font-weight: 700;
  margin: 0;
  letter-spacing: 1px;
}

.footer-text {
  color: rgba(255, 255, 255, 0.6);
  line-height: 1.5;
  margin: 0;
}

.footer-social {
  display: flex;
  gap: 1rem;
}

.social-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: rgba(255, 255, 255, 0.8);
  text-decoration: none;
  transition: color 0.3s ease;
}

.social-link:hover {
  color: #00e5ff;
}

.social-icon {
  font-size: 1.2rem;
}

.footer-link {
  color: rgba(255, 255, 255, 0.6);
  text-decoration: none;
  transition: color 0.3s ease;
  cursor: pointer;
}

.footer-link:hover {
  color: #00e5ff;
}

.footer-bottom {
  padding-top: 2rem;
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  text-align: center;
}

.footer-bottom p {
  color: rgba(255, 255, 255, 0.5);
  font-size: 0.9rem;
  margin: 0;
}

/* ============================================
   RESPONSIVE
   ============================================ */

@media (max-width: 768px) {
  .navbar-nav {
    display: none;
  }

  .hero-container {
    grid-template-columns: 1fr;
    text-align: center;
  }

  .hero-ctas {
    justify-content: center;
  }

  .hero-visual {
    display: none;
  }

  .title-dragon {
    font-size: 3rem;
  }

  .title-main {
    font-size: 1.8rem;
  }

  .section-title {
    font-size: 2rem;
  }

  .features-grid {
    grid-template-columns: 1fr;
  }

  .steps-progress {
    left: 19px;
  }

  .step-number {
    width: 40px;
    height: 40px;
    font-size: 1.2rem;
  }

  .step-title {
    font-size: 1.3rem;
  }

  .pricing-grid {
    grid-template-columns: 1fr;
  }

  .footer-content {
    grid-template-columns: 1fr;
  }
}
</style>
