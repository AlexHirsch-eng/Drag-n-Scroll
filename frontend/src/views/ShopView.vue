<template>
  <div class="shop-view">
    <!-- Back Button -->
    <div class="back-section">
      <button @click="goBack" class="back-btn">
        <span class="icon">←</span>
        <span>НАЗАД ДОМОЙ</span>
      </button>
    </div>

    <!-- Shop Container -->
    <div class="shop-container">
      <!-- Header -->
      <div class="shop-header">
        <h1 class="shop-title">
          <span class="title-icon">🛒</span>
          <span class="title-text">SHOP 商店</span>
        </h1>
        <p class="shop-subtitle">Раскройте свой потенциал в изучении китайского</p>
        <div class="currency-display">
          <img src="/src/images/coin.png" alt="Coins" class="currency-icon">
          <span class="currency-amount">{{ userGems }}</span>
        </div>
      </div>

      <!-- Categories -->
      <div class="categories">
        <button
          v-for="category in categories"
          :key="category.id"
          @click="selectCategory(category.id)"
          :class="['category-btn', { active: selectedCategory === category.id }]"
        >
          <span class="category-icon">{{ category.icon }}</span>
          <span class="category-name">{{ category.name }}</span>
        </button>
      </div>

      <!-- Products Grid -->
      <div class="products-grid">
        <div
          v-for="product in filteredProducts"
          :key="product.id"
          :class="['product-card', product.rarity]"
        >
          <div class="product-badge" v-if="product.badge">{{ product.badge }}</div>
          <div class="product-icon">{{ product.icon }}</div>
          <h3 class="product-name">{{ product.name }}</h3>
          <p class="product-description">{{ product.description }}</p>
          <div class="product-stats" v-if="product.stats">
            <span v-for="stat in product.stats" :key="stat" class="stat-tag">
              {{ stat }}
            </span>
          </div>
          <div class="product-price">
            <img src="/src/images/coin.png" alt="coin" class="price-icon">
            <span class="price-amount">{{ product.price }}</span>
          </div>
          <button
            @click="purchaseProduct(product)"
            :disabled="userGems < product.price || product.owned"
            :class="['purchase-btn', { owned: product.owned }]"
          >
            <span v-if="product.owned">✓ КУПЛЕНО</span>
            <span v-else-if="userGems < product.price">НЕДОСТАТОЧНО МОНЕТ</span>
            <span v-else>КУПИТЬ</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Purchase Modal -->
    <div v-if="showModal" class="modal-overlay" @click="closeModal">
      <div class="modal-content" @click.stop>
        <div class="modal-header">
          <h2>{{ modalProduct?.icon }} {{ modalProduct?.name }}</h2>
          <button @click="closeModal" class="close-btn">✕</button>
        </div>
        <div class="modal-body">
          <p class="modal-description">{{ modalProduct?.description }}</p>
          <div class="modal-price">
            <span class="price-label">Цена:</span>
            <span class="price-value">💎 {{ modalProduct?.price }}</span>
          </div>
          <p class="modal-balance">Ваш баланс: <img src="/src/images/coin.png" alt="coin" class="inline-coin"> {{ userGems }}</p>
        </div>
        <div class="modal-footer">
          <button @click="closeModal" class="cancel-btn">ОТМЕНА</button>
          <button @click="confirmPurchase" class="confirm-btn">ПОДТВЕРДИТЬ ПОКУПКУ</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

interface Product {
  id: number
  name: string
  description: string
  icon: string
  price: number
  category: string
  badge?: string
  rarity: 'common' | 'rare' | 'epic' | 'legendary'
  stats?: string[]
  owned: boolean
}

interface Category {
  id: string
  name: string
  icon: string
}

const userGems = ref(1250)
const selectedCategory = ref('all')
const showModal = ref(false)
const modalProduct = ref<Product | null>(null)

const categories: Category[] = [
  { id: 'all', name: 'Все товары', icon: '📦' },
  { id: 'courses', name: 'Курсы', icon: '📚' },
  { id: 'premium', name: 'Премиум', icon: '⭐' },
  { id: 'hsk', name: 'Подготовка HSK', icon: '🎯' },
  { id: 'practice', name: 'Практика', icon: '💬' },
  { id: 'boosts', name: 'Усилители', icon: '⚡' },
  { id: 'ai-access', name: 'Доступ к ИИ', icon: '🤖' }
]

const products: Product[] = [
  // Courses
  {
    id: 1,
    name: 'Beginner Course',
    description: 'Start your Chinese journey with basics. Pinyin, greetings, and essential vocabulary.',
    icon: '🎒',
    price: 0,
    category: 'courses',
    rarity: 'common',
    badge: 'FREE',
    stats: ['20 Lessons', '100 Words', 'Basic Grammar'],
    owned: true
  },
  {
    id: 2,
    name: 'Intermediate Course',
    description: 'Take your Chinese to the next level. Conversational skills and grammar.',
    icon: '📖',
    price: 500,
    category: 'courses',
    rarity: 'rare',
    stats: ['30 Lessons', '500 Words', 'Grammar'],
    owned: false
  },
  {
    id: 3,
    name: 'Advanced Course',
    description: 'Master Chinese with advanced content. Business, literature, and culture.',
    icon: '🎓',
    price: 1000,
    category: 'courses',
    rarity: 'epic',
    badge: 'POPULAR',
    stats: ['40 Lessons', '1000 Words', 'Business'],
    owned: false
  },

  // Premium
  {
    id: 4,
    name: 'Premium Weekly',
    description: 'Unlock all features for 7 days. Unlimited lessons, no ads, priority support.',
    icon: '⭐',
    price: 200,
    category: 'premium',
    rarity: 'rare',
    stats: ['7 Days', 'All Access', 'No Ads'],
    owned: false
  },
  {
    id: 5,
    name: 'Premium Monthly',
    description: 'Best value! Full access for 30 days. Everything unlimited.',
    icon: '🌟',
    price: 500,
    category: 'premium',
    rarity: 'epic',
    badge: 'BEST VALUE',
    stats: ['30 Days', 'All Access', 'Save 33%'],
    owned: false
  },
  {
    id: 6,
    name: 'Premium Yearly',
    description: 'Ultimate value! Full year of premium access. Limited time offer!',
    icon: '👑',
    price: 3000,
    category: 'premium',
    rarity: 'legendary',
    badge: '-50% OFF',
    stats: ['365 Days', 'All Access', 'Save 50%'],
    owned: false
  },

  // HSK Prep
  {
    id: 7,
    name: 'HSK 1-2 Bundle',
    description: 'Complete preparation for HSK 1 and 2 exams. Essential vocabulary and practice.',
    icon: '🎯',
    price: 300,
    category: 'hsk',
    rarity: 'rare',
    stats: ['300 Words', 'Practice Tests', 'Grammar'],
    owned: false
  },
  {
    id: 8,
    name: 'HSK 3-4 Bundle',
    description: 'Intermediate HSK preparation. Grammar patterns and vocabulary.',
    icon: '🏹',
    price: 600,
    category: 'hsk',
    rarity: 'epic',
    badge: 'POPULAR',
    stats: ['1200 Words', 'Mock Exams', 'Writing'],
    owned: false
  },
  {
    id: 9,
    name: 'HSK 5-6 Bundle',
    description: 'Advanced HSK mastery. Prepare for the highest levels.',
    icon: '🏆',
    price: 1200,
    category: 'hsk',
    rarity: 'legendary',
    stats: ['2500+ Words', 'Advanced', 'Certificates'],
    owned: false
  },

  // Practice
  {
    id: 10,
    name: 'Conversation Pack',
    description: 'Real-life dialogues and scenarios. Practice daily conversations.',
    icon: '💬',
    price: 250,
    category: 'practice',
    rarity: 'rare',
    stats: ['50 Dialogues', 'Audio', 'Topics'],
    owned: false
  },
  {
    id: 11,
    name: 'Writing Master',
    description: 'Learn Chinese characters from scratch. Stroke order and radicals.',
    icon: '✍️',
    price: 400,
    category: 'practice',
    rarity: 'rare',
    stats: ['500 Characters', 'Strokes', 'Radicals'],
    owned: false
  },
  {
    id: 12,
    name: 'Pronunciation Pro',
    description: 'Perfect your tones and pronunciation with audio exercises.',
    icon: '🎤',
    price: 350,
    category: 'practice',
    rarity: 'rare',
    stats: ['Audio Guide', 'Tones', 'Exercises'],
    owned: false
  },

  // Boosts
  {
    id: 13,
    name: 'SCROLLS Boost 2x',
    description: 'Double your SCROLLS for 24 hours. Learn faster!',
    icon: '⚡',
    price: 100,
    category: 'boosts',
    rarity: 'common',
    stats: ['2x SCROLLS', '24 Hours', 'Stackable'],
    owned: false
  },
  {
    id: 14,
    name: 'Streak Freeze',
    description: 'Protect your streak for 1 day. No worries about missing a day.',
    icon: '❄️',
    price: 50,
    category: 'boosts',
    rarity: 'common',
    stats: ['1 Day', 'Streak Save', 'Essential'],
    owned: false
  },
  {
    id: 15,
    name: 'Gems Bundle',
    description: 'Get bonus gems instantly. Great deal!',
    icon: '💎',
    price: 500,
    category: 'boosts',
    rarity: 'epic',
    badge: '+20% BONUS',
    stats: ['600 Gems', 'Instant', 'Bonus'],
    owned: false
  },

  // AI Access
  {
    id: 16,
    name: 'AI Chat - 1 Day',
    description: 'Get access to AI Chat bot for 1 day. Practice Chinese conversations!',
    icon: '🤖',
    price: 50,
    category: 'ai-access',
    rarity: 'common',
    stats: ['1 Day Access', 'Unlimited Chat', 'AI Practice'],
    owned: false
  },
  {
    id: 17,
    name: 'AI Chat - 7 Days',
    description: 'Full access to AI Chat bot for a week. Perfect for intensive practice!',
    icon: '🤖',
    price: 250,
    category: 'ai-access',
    rarity: 'rare',
    badge: 'POPULAR',
    stats: ['7 Days Access', 'Unlimited Chat', 'Save 15%'],
    owned: false
  },
  {
    id: 18,
    name: 'AI Chat - 30 Days',
    description: 'Monthly access to AI Chat bot. Best value for serious learners!',
    icon: '🤖',
    price: 800,
    category: 'ai-access',
    rarity: 'epic',
    badge: 'BEST VALUE',
    stats: ['30 Days Access', 'Unlimited Chat', 'Save 45%'],
    owned: false
  },
  {
    id: 19,
    name: 'AI Chat - Lifetime',
    description: 'Permanent access to AI Chat bot. One-time payment, forever practice!',
    icon: '🤖',
    price: 3000,
    category: 'ai-access',
    rarity: 'legendary',
    badge: 'LIMITED',
    stats: ['Forever Access', 'Unlimited Chat', 'Free Updates'],
    owned: false
  }
]

const filteredProducts = computed(() => {
  if (selectedCategory.value === 'all') {
    return products
  }
  return products.filter(p => p.category === selectedCategory.value)
})

function selectCategory(categoryId: string) {
  selectedCategory.value = categoryId
}

function purchaseProduct(product: Product) {
  if (product.owned || userGems.value < product.price) return
  modalProduct.value = product
  showModal.value = true
}

function closeModal() {
  showModal.value = false
  modalProduct.value = null
}

function confirmPurchase() {
  if (!modalProduct.value) return

  userGems.value -= modalProduct.value.price

  // Handle AI Access purchases
  if (modalProduct.value.category === 'ai-access') {
    const daysMap: Record<number, number> = {
      16: 1,   // 1 Day
      17: 7,   // 7 Days
      18: 30,  // 30 Days
      19: 36500, // Lifetime (100 years)
    }

    const days = daysMap[modalProduct.value.id] || 0
    if (days > 0) {
      authStore.purchaseAIAccess(days)
    }
  } else {
    // Mark other products as owned
    const productIndex = products.findIndex(p => p.id === modalProduct.value!.id)
    if (productIndex !== -1) {
      products[productIndex].owned = true
    }
  }

  closeModal()

  // Show success notification
  setTimeout(() => {
    alert(`🎉 Успешно куплено: ${modalProduct.value?.name}!`)
  }, 100)
}

function goBack() {
  router.push('/')
}
</script>

<style scoped>
.shop-view {
  min-height: 100vh;
  background: var(--color-bg-primary);
  padding: 1rem;
  position: relative;
}

.back-section {
  display: flex;
  justify-content: center;
  margin-bottom: 1rem;
}

.back-btn {
  background: rgba(37, 29, 45, 0.9);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(0, 245, 255, 0.15);
  border-radius: var(--radius-lg);
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  color: var(--color-text-primary);
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  font-weight: 700;
  letter-spacing: 1px;
}

.back-btn:hover {
  transform: translateY(-2px);
  background: rgba(0, 245, 255, 0.15);
  border-color: var(--color-neon-cyan);
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.3);
}

.shop-container {
  max-width: 1400px;
  margin: 0 auto;
}

.shop-header {
  text-align: center;
  padding: 2rem;
  background: var(--color-bg-card);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-2xl);
  margin-bottom: 2rem;
  position: relative;
}

.shop-title {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 1rem;
  font-size: 2.5rem;
  font-weight: 900;
  margin: 0 0 0.5rem 0;
}

.title-icon {
  font-size: 3rem;
}

.title-text {
  background: var(--gradient-neon-rainbow);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.shop-subtitle {
  font-size: 1rem;
  color: var(--color-text-muted);
  margin: 0 0 1.5rem 0;
}

.currency-display {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: rgba(0, 245, 255, 0.1);
  border: 1px solid var(--color-neon-cyan);
  border-radius: var(--radius-full);
  padding: 0.5rem 1.5rem;
  font-size: 1.2rem;
  font-weight: 700;
}

.currency-icon {
  width: 51px;
  height: 51px;
  object-fit: contain;
  animation: coinFloat 2s ease-in-out infinite;
  filter: drop-shadow(0 0 10px rgba(255, 215, 0, 0.6));
}

@keyframes coinFloat {
  0%, 100% {
    transform: translateY(0) rotate(0deg);
  }
  50% {
    transform: translateY(-5px) rotate(180deg);
  }
}

.currency-amount {
  color: #FFD700;
  font-size: 1.5rem;
  font-weight: 900;
}

.categories {
  display: flex;
  gap: 0.75rem;
  flex-wrap: wrap;
  justify-content: center;
  margin-bottom: 2rem;
}

.category-btn {
  background: var(--color-bg-card);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-lg);
  padding: 0.75rem 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  transition: all 0.3s;
  font-size: 0.9rem;
  font-weight: 600;
  color: #E0E7FF;
}

.category-btn:hover {
  border-color: var(--color-neon-cyan);
  transform: translateY(-2px);
  box-shadow: 0 0 15px rgba(0, 245, 255, 0.3);
  color: #00F5FF;
}

.category-btn.active {
  background: rgba(0, 245, 255, 0.2);
  border-color: var(--color-neon-cyan);
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.4);
  color: #00F5FF;
  text-shadow: 0 0 10px rgba(0, 245, 255, 0.5);
}

.category-icon {
  font-size: 1.5rem;
}

.products-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 1.5rem;
}

.product-card {
  background: var(--color-bg-card);
  border: 2px solid var(--color-border-primary);
  border-radius: var(--radius-xl);
  padding: 1.5rem;
  position: relative;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.product-card:hover {
  transform: translateY(-4px);
}

.product-card.common {
  border-color: #9ca3af;
}

.product-card.common:hover {
  box-shadow: 0 0 20px rgba(156, 163, 175, 0.4);
}

.product-card.rare {
  border-color: var(--color-neon-cyan);
}

.product-card.rare:hover {
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.4);
}

.product-card.epic {
  border-color: var(--color-neon-pink);
}

.product-card.epic:hover {
  box-shadow: 0 0 20px rgba(255, 107, 53, 0.4);
}

.product-card.legendary {
  border-color: var(--color-neon-yellow);
  animation: legendaryGlow 3s ease-in-out infinite;
}

@keyframes legendaryGlow {
  0%, 100% {
    box-shadow: 0 0 10px rgba(255, 193, 7, 0.3);
  }
  50% {
    box-shadow: 0 0 25px rgba(255, 193, 7, 0.6);
  }
}

.product-badge {
  position: absolute;
  top: -8px;
  right: -8px;
  background: var(--gradient-pink);
  color: white;
  font-size: 0.7rem;
  font-weight: 900;
  padding: 0.25rem 0.75rem;
  border-radius: var(--radius-full);
  transform: rotate(15deg);
  box-shadow: 0 0 15px rgba(255, 107, 53, 0.5);
  z-index: 1;
}

.product-icon {
  font-size: 4rem;
  text-align: center;
  filter: drop-shadow(0 4px 8px rgba(0, 0, 0, 0.3));
}

.product-name {
  font-size: 1.2rem;
  font-weight: 700;
  margin: 0;
  text-align: center;
  color: #FFFFFF;
}

.product-description {
  font-size: 0.85rem;
  color: #B0B8C8;
  line-height: 1.5;
  flex-grow: 1;
}

.product-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  justify-content: center;
}

.stat-tag {
  background: rgba(0, 245, 255, 0.1);
  border: 1px solid rgba(0, 245, 255, 0.3);
  border-radius: var(--radius-md);
  padding: 0.25rem 0.75rem;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--color-neon-cyan);
}

.product-price {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-size: 1.3rem;
  font-weight: 900;
  background: rgba(0, 0, 0, 0.3);
  border-radius: var(--radius-lg);
  padding: 0.5rem;
}

.price-icon {
  width: 38px;
  height: 38px;
  object-fit: contain;
}

.price-icon {
  font-size: 1.5rem;
}

.price-amount {
  color: #FFD700;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.purchase-btn {
  background: var(--gradient-cyan);
  border: none;
  border-radius: var(--radius-lg);
  padding: 0.75rem;
  font-size: 0.9rem;
  font-weight: 800;
  cursor: pointer;
  transition: all 0.3s;
  letter-spacing: 1px;
}

.purchase-btn:hover:not(:disabled) {
  transform: scale(1.05);
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
}

.purchase-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.purchase-btn.owned {
  background: var(--gradient-neon-rainbow);
  cursor: default;
}

/* Modal */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.8);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  backdrop-filter: blur(5px);
}

.modal-content {
  background: var(--color-bg-card);
  border: 2px solid var(--color-neon-cyan);
  border-radius: var(--radius-2xl);
  padding: 2rem;
  max-width: 500px;
  width: 90%;
  box-shadow: 0 0 50px rgba(0, 245, 255, 0.3);
  animation: modalSlideIn 0.3s ease-out;
}

@keyframes modalSlideIn {
  from {
    opacity: 0;
    transform: translateY(-50px) scale(0.9);
  }
  to {
    opacity: 1;
    transform: translateY(0) scale(1);
  }
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
}

.modal-header h2 {
  font-size: 1.5rem;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  cursor: pointer;
  color: var(--color-text-muted);
  transition: all 0.3s;
}

.close-btn:hover {
  color: var(--color-accent-primary);
  transform: rotate(90deg);
}

.modal-description {
  color: #D0D8E8;
  line-height: 1.6;
  margin-bottom: 1.5rem;
}

.modal-price {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: rgba(0, 0, 0, 0.3);
  padding: 1rem;
  border-radius: var(--radius-lg);
  margin-bottom: 1rem;
}

.price-label {
  font-weight: 600;
  color: #E0E7FF;
}

.price-value {
  font-size: 1.3rem;
  font-weight: 900;
  color: #FFD700;
  text-shadow: 0 0 10px rgba(255, 215, 0, 0.5);
}

.modal-balance {
  text-align: center;
  color: #A0A8C0;
  margin-bottom: 1.5rem;
}

.inline-coin {
  width: 25px;
  height: 25px;
  object-fit: contain;
  vertical-align: middle;
  margin: 0 0.25rem;
}

.modal-footer {
  display: flex;
  gap: 1rem;
}

.cancel-btn,
.confirm-btn {
  flex: 1;
  padding: 0.75rem;
  border: none;
  border-radius: var(--radius-lg);
  font-size: 0.9rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.3s;
}

.cancel-btn {
  background: rgba(255, 107, 53, 0.2);
  border: 1px solid var(--color-accent-primary);
  color: var(--color-text-primary);
}

.cancel-btn:hover {
  background: rgba(255, 107, 53, 0.3);
}

.confirm-btn {
  background: var(--gradient-cyan);
  color: var(--color-bg-primary);
}

.confirm-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 0 20px rgba(0, 245, 255, 0.5);
}

@media (max-width: 768px) {
  .shop-title {
    font-size: 2rem;
  }

  .products-grid {
    grid-template-columns: 1fr;
  }

  .categories {
    gap: 0.5rem;
  }

  .category-btn {
    padding: 0.5rem 1rem;
    font-size: 0.8rem;
  }
}
</style>
