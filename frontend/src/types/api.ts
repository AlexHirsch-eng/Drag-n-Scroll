// API Types matching the Django backend

// User & Auth
export interface User {
  id: number
  username: string
  email: string
  is_staff?: boolean
  profile?: UserProfile
  progress?: UserProgress
  followers_count?: number
  following_count?: number
  likes_received?: number
  created_at: string
  updated_at: string
}

export interface UserProfile {
  learning_language: 'RU' | 'KZ'
  current_hsk_level: number
  created_at: string
  updated_at: string
}

export interface UserProgress {
  current_day: number
  current_lesson: number
  current_step: number
  total_xp: number
  streak_days: number
  last_study_date: string | null
  completed_days: number[]
  created_at: string
  updated_at: string
}

export interface AuthTokens {
  access: string
  refresh: string
}

export interface RegisterData {
  username: string
  email: string
  password: string
  learning_language: 'RU' | 'KZ'
}

export interface LoginData {
  username: string
  password: string
}

// Course
export interface Course {
  id: number
  title: string
  title_zh: string
  description: string
  hsk_level: number
  total_days: number
  order: number
  is_active: boolean
  created_at: string
  updated_at: string
}

export interface CourseDay {
  id: number
  day_number: number
  title: string
  title_zh: string
  description: string
  estimated_minutes: number
  order: number
  created_at: string
  updated_at: string
}

export interface Lesson {
  id: number
  lesson_type: 'VOCABULARY' | 'GRAMMAR' | 'MIXED'
  hsk_level: number
  title: string
  title_zh: string
  description: string
  order: number
  estimated_minutes: number
  created_at: string
  updated_at: string
  steps?: LessonStep[]
}

export interface LessonStep {
  id: number
  step_type: StepType
  title: string
  content: StepContent
  order: number
  estimated_minutes: number
  created_at: string
  updated_at: string
}

export type StepType =
  | 'VOCAB_INTRO'
  | 'VOCAB_RECOGNIZE'
  | 'VOCAB_MATCH'
  | 'GRAMMAR_INTRO'
  | 'BUILD_PHRASE'
  | 'FILL_BLANK'
  | 'SRS_REVIEW'

export interface StepContent {
  words?: Word[]
  question?: WordQuestion
  instruction_ru?: string
  instruction_kz?: string
  target_hanzi?: string
  target_pinyin?: string
  options?: PhraseOption[]
  correct_order?: number[]
  correct_answer?: string
  correct_pairs?: string[][]
  batch_size?: number
  time_limit_seconds?: number
  rules?: GrammarRule[]
}

export interface WordQuestion {
  hanzi: string
  pinyin: string
  audio_url: string
}

export interface PhraseOption {
  id: number
  hanzi: string
  pinyin: string
}

// Vocabulary
export interface Word {
  id: number
  hanzi: string
  pinyin: string
  translation_ru: string
  translation_kz: string
  audio_url: string
  hsk_level: number
  frequency_rank: number | null
  part_of_speech: string
  created_at: string
  updated_at: string
}

export interface WordWithProgress {
  word: Word
  progress: WordProgress
}

export interface WordProgress {
  srs_level: number
  interval_days: number
  next_review_date: string | null
  total_reviews: number
  correct_reviews: number
  accuracy: number
  last_reviewed_at?: string
}

export interface GrammarRule {
  id: number
  title: string
  pattern: string
  explanation_ru: string
  explanation_kz: string
  hsk_level: number
  examples: GrammarExample[]
  created_at: string
  updated_at: string
}

export interface GrammarExample {
  id: number
  sentence_hanzi: string
  sentence_pinyin: string
  translation_ru: string
  translation_kz: string
  audio_url: string
  order: number
}

// Session & Learning
export interface SessionProgress {
  id: number
  course_day: CourseDay
  lesson: Lesson
  started_at: string
  completed_at: string | null
  current_step_index: number
  steps_completed: number
  steps_correct: number
  xp_earned: number
  is_active: boolean
  accuracy: number
  time_spent_minutes: number
}

export interface CurrentSessionResponse {
  course_day: {
    id: number
    day_number: number
    title: string
    estimated_minutes: number
  }
  lesson: {
    id: number
    lesson_type: string
    title: string
    hsk_level: number
  }
  session: {
    id: number
    started_at: string
    current_step_index: number
    steps_completed: number
    steps_correct: number
    xp_earned: number
  }
  next_step: {
    step_number: number
    step_type: StepType
    title: string
    estimated_minutes: number
  } | null
}

export interface SubmitStepRequest {
  session_id: number
  step_id: number
  user_answer: Record<string, any>
  time_spent_seconds?: number
}

export interface SubmitStepResponse {
  is_correct: boolean
  correct_answer?: any
  xp_earned: number
  streak_updated: boolean
  next_step?: {
    step_id: number
    step_type: StepType
    title: string
  }
  session_progress: {
    steps_completed: number
    steps_correct: number
    xp_earned: number
  }
}

export interface FinishSessionResponse {
  session_completed: boolean
  xp_earned: number
  steps_completed: number
  steps_correct: number
  accuracy: number
  time_spent_minutes: number
  next_lesson?: {
    day_number: number
    lesson_id: number
    title: string
  }
}

// SRS
export interface SRSReviewItem {
  id: number
  hanzi: string
  pinyin: string
  translation_ru: string
  translation_kz: string
  audio_url: string
  srs_level: number
  total_reviews: number
  accuracy?: number
  correct_reviews?: number
}

export interface ReviewBatchResponse {
  batch_id: string
  words: SRSReviewItem[]
  total_due: number
  batch_number: number
  total_batches: number
}

export interface SubmitReviewRequest {
  batch_id: string
  reviews: {
    word_id: number
    quality: number
    time_spent_seconds: number
  }[]
}

export interface SubmitReviewResponse {
  reviews_processed: number
  words_updated: {
    word_id: number
    old_srs_level: number
    new_srs_level: number
    old_interval: number
    new_interval: number
    next_review_date: string
  }[]
  xp_earned: number
}

export interface DueCountResponse {
  due_now: number
  due_today: number
  due_this_week: number
  total_learning: number
  total_mastered: number
}

export interface SRSStatsResponse {
  total_words: number
  by_srs_level: Record<string, number>
  retention_rate: number
  avg_reviews_per_word: number
  streak_days: number
  upcoming_reviews: {
    date: string
    count: number
  }[]
}

// API Error
export interface APIError {
  detail?: string
  error?: string
  [key: string]: any
}
