import { defineStore } from 'pinia'
import { ref } from 'vue'
import { srsAPI } from '@/api/srs'
import type {
  ReviewBatchResponse,
  SubmitReviewRequest,
  DueCountResponse,
  SRSStatsResponse,
  SRSReviewItem,
} from '@/types/api'

export const useSRSStore = defineStore('srs', () => {
  // State
  const currentBatch = ref<ReviewBatchResponse | null>(null)
  const currentReviewIndex = ref(0)
  const dueCount = ref<DueCountResponse | null>(null)
  const stats = ref<SRSStatsResponse | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Actions
  async function loadReviewBatch(params?: { batch_size?: number; hsk_level?: number }) {
    isLoading.value = true
    error.value = null
    try {
      const batch = await srsAPI.getReviewBatch(params)
      currentBatch.value = batch
      currentReviewIndex.value = 0
      return batch
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load review batch'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function submitReview(request: SubmitReviewRequest) {
    isLoading.value = true
    error.value = null
    try {
      const response = await srsAPI.submitReview(request)
      currentBatch.value = null
      currentReviewIndex.value = 0
      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to submit review'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function loadDueCount() {
    try {
      const count = await srsAPI.getDueCount()
      dueCount.value = count
      return count
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load due count'
      throw err
    }
  }

  async function loadStats() {
    try {
      const statsData = await srsAPI.getStats()
      stats.value = statsData
      return statsData
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load stats'
      throw err
    }
  }

  function getCurrentCard(): SRSReviewItem | null {
    if (!currentBatch.value || !currentBatch.value.words[currentReviewIndex.value]) {
      return null
    }
    return currentBatch.value.words[currentReviewIndex.value]
  }

  function nextCard() {
    if (currentBatch.value && currentReviewIndex.value < currentBatch.value.words.length - 1) {
      currentReviewIndex.value++
    }
  }

  function previousCard() {
    if (currentReviewIndex.value > 0) {
      currentReviewIndex.value--
    }
  }

  function getProgress() {
    if (!currentBatch.value) return { current: 0, total: 0 }
    return {
      current: currentReviewIndex.value + 1,
      total: currentBatch.value.words.length,
    }
  }

  function reset() {
    currentBatch.value = null
    currentReviewIndex.value = 0
    error.value = null
  }

  return {
    currentBatch,
    currentReviewIndex,
    dueCount,
    stats,
    isLoading,
    error,
    loadReviewBatch,
    submitReview,
    loadDueCount,
    loadStats,
    getCurrentCard,
    nextCard,
    previousCard,
    getProgress,
    reset,
  }
})
