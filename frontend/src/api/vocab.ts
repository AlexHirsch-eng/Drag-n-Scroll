import { apiClient } from './client'
import type {
  Word,
  WordWithProgress,
  GrammarRule,
  Course,
  CourseDay,
  Lesson,
} from '@/types/api'

export const vocabAPI = {
  async getWords(params?: {
    hsk_level?: number
    part_of_speech?: string
    search?: string
    page?: number
  }): Promise<{ results: Word[]; count: number; next: string | null; previous: string | null }> {
    return apiClient.get('/vocab/words/', params)
  },

  async getWord(id: number): Promise<Word> {
    return apiClient.get(`/vocab/words/${id}/`)
  },

  async getMyWords(params?: {
    hsk_level?: number
    srs_level?: number
    status?: 'new' | 'learning' | 'mastered'
    page?: number
  }): Promise<{ results: WordWithProgress[]; count: number }> {
    return apiClient.get('/vocab/my-words/', params)
  },

  async getGrammarRules(params?: {
    hsk_level?: number
    search?: string
  }): Promise<GrammarRule[]> {
    return apiClient.get('/vocab/grammar/', params)
  },

  async getGrammarRule(id: number): Promise<GrammarRule> {
    return apiClient.get(`/vocab/grammar/${id}/`)
  },
}

export const courseAPI = {
  async getCourses(params?: { hsk_level?: number }): Promise<Course[]> {
    return apiClient.get('/course/courses/', params)
  },

  async getCourse(id: number): Promise<Course> {
    return apiClient.get(`/course/courses/${id}/`)
  },

  async getCourseDays(courseId?: number, dayNumber?: number): Promise<CourseDay[]> {
    return apiClient.get('/course/days/', { course_id: courseId, day_number: dayNumber })
  },

  async getCourseDay(id: number): Promise<CourseDay> {
    return apiClient.get(`/course/days/${id}/`)
  },

  async getLessons(courseDayId?: number): Promise<Lesson[]> {
    return apiClient.get('/course/lessons/', { course_day_id: courseDayId })
  },

  async getLesson(id: number): Promise<Lesson> {
    return apiClient.get(`/course/lessons/${id}/`)
  },
}
