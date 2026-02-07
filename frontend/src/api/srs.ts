import { apiClient } from './client'
import type {
  ReviewBatchResponse,
  SubmitReviewRequest,
  SubmitReviewResponse,
  DueCountResponse,
  SRSStatsResponse,
} from '@/types/api'

export const srsAPI = {
  async getReviewBatch(params?: {
    batch_size?: number
    hsk_level?: number
  }): Promise<ReviewBatchResponse> {
    return apiClient.get('/learning/srs/review-batch/', params)
  },

  async getMistakesBatch(params?: {
    batch_size?: number
    hsk_level?: number
  }): Promise<ReviewBatchResponse> {
    return apiClient.get('/learning/srs/mistakes-batch/', params)
  },

  async submitReview(data: SubmitReviewRequest): Promise<SubmitReviewResponse> {
    return apiClient.post('/learning/srs/submit-review/', data)
  },

  async getDueCount(): Promise<DueCountResponse> {
    return apiClient.get('/learning/srs/due-count/')
  },

  async getStats(): Promise<SRSStatsResponse> {
    return apiClient.get('/learning/srs/stats/')
  },
}
