# Drag'n'Scroll Frontend

Vue 3 frontend for the Chinese Learning Application with TikTok-style interface.

## Features

- **TikTok-Style Interface**: Vertical swipe navigation for learning cards
- **SRS Integration**: Spaced repetition system for vocabulary review
- **Real-time Progress**: XP tracking, streaks, and learning statistics
- **Multi-language Support**: Russian and Kazakh translations
- **Responsive Design**: Mobile-first with desktop support

## Tech Stack

- Vue 3 (Composition API)
- TypeScript
- Vite
- Pinia (State Management)
- Vue Router
- Axios

## Setup Instructions

### 1. Prerequisites

- Node.js 18+
- npm or yarn

### 2. Installation

```bash
# Install dependencies
npm install

# or with yarn
yarn install
```

### 3. Configuration

```bash
# Copy .env.example to .env
cp .env.example .env

# Edit .env if needed (default: http://localhost:8000/api)
```

### 4. Development

```bash
# Start dev server
npm run dev

# or with yarn
yarn dev
```

The app will be available at `http://localhost:5173`

### 5. Build for Production

```bash
# Build for production
npm run build

# Preview production build
npm run preview
```

## Project Structure

```
src/
├── api/              # API client and service modules
│   ├── client.ts     # Axios instance with interceptors
│   ├── auth.ts       # Authentication API
│   ├── learning.ts   # Learning session API
│   ├── vocab.ts      # Vocabulary API
│   └── srs.ts        # SRS API
├── components/       # Vue components
│   ├── cards/        # Learning card components
│   │   ├── VocabIntroCard.vue
│   │   ├── VocabRecognizeCard.vue
│   │   ├── GrammarIntroCard.vue
│   │   └── SRSReviewCard.vue
│   └── layout/       # Layout components
│       └── SwipeContainer.vue
├── stores/           # Pinia stores
│   ├── auth.ts       # Authentication state
│   ├── session.ts    # Learning session state
│   └── srs.ts        # SRS state
├── views/            # Page components
│   ├── LoginView.vue
│   ├── RegisterView.vue
│   ├── LearnView.vue
│   ├── LessonView.vue
│   ├── ReviewView.vue
│   ├── ProfileView.vue
│   ├── VocabView.vue
│   └── StatsView.vue
├── router/           # Vue Router config
│   └── index.ts
├── types/            # TypeScript types
│   └── api.ts        # API response types
├── App.vue           # Root component
├── main.ts           # Entry point
└── style.css         # Global styles
```

## Components

### SwipeContainer
Main layout component for TikTok-style vertical navigation.

**Features:**
- Touch/swipe gestures (mobile)
- Keyboard navigation (Arrow keys)
- Mouse wheel support
- Progress indicator

**Usage:**
```vue
<SwipeContainer
  :current-index="currentIndex"
  :total="total"
  @next="nextStep"
  @previous="previousStep"
>
  <template #default>
    <!-- Your card content -->
  </template>
</SwipeContainer>
```

### Card Components

- **VocabIntroCard**: Display new vocabulary words
- **VocabRecognizeCard**: Multiple choice vocabulary quiz
- **GrammarIntroCard**: Grammar rules with examples
- **SRSReviewCard**: Spaced repetition review

## State Management

### Auth Store
Manages user authentication and profile.

```typescript
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
await authStore.login({ username, password })
```

### Session Store
Manages learning sessions and progress.

```typescript
import { useSessionStore } from '@/stores/session'

const sessionStore = useSessionStore()
await sessionStore.loadCurrentSession()
```

### SRS Store
Manages spaced repetition reviews.

```typescript
import { useSRSStore } from '@/stores/srs'

const srsStore = useSRSStore()
await srsStore.loadReviewBatch()
```

## API Integration

The frontend uses Axios with interceptors for:

- Automatic token injection
- Token refresh on 401 errors
- Consistent error handling

## Routing

Protected routes require authentication:
- `/learn` - Current learning session
- `/lesson` - Active lesson
- `/review` - SRS review
- `/vocab` - Vocabulary list
- `/stats` - Statistics
- `/profile` - User profile

Public routes:
- `/login` - Login page
- `/register` - Registration page

## Keyboard Shortcuts

- **Arrow Down / Right**: Next step
- **Arrow Up / Left**: Previous step
- **Space**: Reveal card (in review mode)

## Browser Support

- Chrome/Edge 90+
- Firefox 88+
- Safari 14+
- Mobile browsers (iOS Safari, Chrome Mobile)

## Development

### Type Checking

```bash
npm run type-check
```

### Linting

```bash
npm run lint
```

## Deployment

Build the production bundle and deploy the `dist/` folder to any static hosting service:

- Vercel
- Netlify
- AWS S3 + CloudFront
- GitHub Pages

## License

MIT
