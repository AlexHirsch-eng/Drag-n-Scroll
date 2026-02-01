import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { learningAPI, type LearningSession, type SessionSummaryResponse } from '@/api/learning'

export const useSessionStore = defineStore('session', () => {
  // State
  const mainScreenData = ref<any>(null)
  const currentSession = ref<LearningSession | null>(null)
  const currentStep = ref<number>(1)
  const currentStepData = ref<any>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  // Timer state
  const stepStartTime = ref<number>(Date.now())
  const timeRemaining = ref<number>(0) // in seconds

  // Computed
  const isSessionActive = computed(() => currentSession.value && !currentSession.value.is_completed)
  const sessionProgress = computed(() => {
    if (!currentSession.value) return 0
    return (currentSession.value.current_step / 6) * 100
  })

  // Actions
  async function loadMainScreen() {
    isLoading.value = true
    error.value = null
    try {
      const data = await learningAPI.getMainScreen()
      mainScreenData.value = data
      return data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load main screen'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function loadMainScreenForDay(dayNumber: number, hskLevel?: number) {
    isLoading.value = true
    error.value = null
    try {
      const data = await learningAPI.getMainScreen(dayNumber, hskLevel)
      mainScreenData.value = data
      return data
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to load main screen'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function startSession(courseDayId: number, sessionType: 'A' | 'B') {
    isLoading.value = true
    error.value = null
    try {
      const response = await learningAPI.startSession({
        course_day_id: courseDayId,
        session_type: sessionType
      })
      currentSession.value = response.session
      currentStep.value = response.step
      currentStepData.value = response.data
      stepStartTime.value = Date.now()

      // Set timer based on step type
      setStepTimer(response.step)

      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to start session'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function resumeSession(sessionId: number) {
    isLoading.value = true
    error.value = null
    try {
      const response = await learningAPI.getStepData(sessionId)
      currentSession.value = response.session
      currentStep.value = response.step
      currentStepData.value = response.data
      stepStartTime.value = Date.now()

      setStepTimer(response.step)

      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to resume session'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function submitStep1(cardId: number, selectedOptionId: number, currentCardIndex?: number, totalShownCards?: number) {
    if (!currentSession.value) return

    const timeSpent = Math.floor((Date.now() - stepStartTime.value) / 1000)

    try {
      console.log('Submitting Step 1:', { cardId, selectedOptionId, timeSpent, currentCardIndex, totalShownCards })

      const response = await learningAPI.submitStep1({
        session_id: currentSession.value.id,
        card_id: cardId,
        selected_option_id: selectedOptionId,
        time_spent_seconds: timeSpent,
        current_card_index: currentCardIndex,
        total_shown_cards: totalShownCards
      })

      console.log('Step 1 response:', response)

      // Update session with response data
      currentSession.value = response.session

      // If step is completed, move to next step
      if (response.is_step_completed && response.next_step) {
        console.log('Step completed, moving to step:', response.next_step)
        await moveToStep(response.next_step)
        return response
      }

      // If next card is available, update step data with next card
      if (response.next_card) {
        console.log('Next card available')
        currentStepData.value = {
          ...currentStepData.value,
          current_card_index: (currentStepData.value?.current_card_index || 0) + 1,
        }
      }

      console.log('Step 1 submit done, is_completed:', response.is_step_completed)

      return response
    } catch (err: any) {
      console.error('Step 1 error:', err)
      error.value = err.response?.data?.detail || 'Failed to submit answer'
      throw err
    }
  }

  async function submitStep2(words: any[]) {
    if (!currentSession.value) return

    const timeSpent = Math.floor((Date.now() - stepStartTime.value) / 1000)

    try {
      const response = await learningAPI.submitStep2({
        session_id: currentSession.value.id,
        words: words.map(w => ({
          ...w,
          time_spent_seconds: timeSpent
        }))
      })

      currentSession.value = response.session

      if (response.is_step_completed && response.next_step) {
        await moveToStep(response.next_step)
      }

      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to submit words'
      throw err
    }
  }

  async function submitStep3(builtSentence: string) {
    if (!currentSession.value) return

    const timeSpent = Math.floor((Date.now() - stepStartTime.value) / 1000)

    try {
      const response = await learningAPI.submitStep3({
        session_id: currentSession.value.id,
        built_sentence_hanzi: builtSentence,
        time_spent_seconds: timeSpent
      })

      currentSession.value = response.session

      if (response.is_step_completed && response.next_step) {
        await moveToStep(response.next_step)
      }

      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to submit grammar'
      throw err
    }
  }

  async function submitStep4(selectedOptionIndex: number) {
    if (!currentSession.value) return

    const timeSpent = Math.floor((Date.now() - stepStartTime.value) / 1000)

    try {
      const response = await learningAPI.submitStep4({
        session_id: currentSession.value.id,
        selected_option_index: selectedOptionIndex,
        time_spent_seconds: timeSpent
      })

      currentSession.value = response.session

      if (response.is_step_completed && response.next_step) {
        await moveToStep(response.next_step)
      }

      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to submit dialogue'
      throw err
    }
  }

  async function submitStep5(arrangedWordIds: number[]) {
    if (!currentSession.value) return

    const timeSpent = Math.floor((Date.now() - stepStartTime.value) / 1000)

    try {
      const response = await learningAPI.submitStep5({
        session_id: currentSession.value.id,
        arranged_word_ids: arrangedWordIds,
        time_spent_seconds: timeSpent
      })

      currentSession.value = response.session

      return response
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to submit arrangement'
      throw err
    }
  }

  async function completeSession(): Promise<SessionSummaryResponse> {
    if (!currentSession.value) throw new Error('No active session')

    isLoading.value = true
    error.value = null
    try {
      const summary = await learningAPI.completeSession(currentSession.value.id)
      currentSession.value = summary.session
      return summary
    } catch (err: any) {
      error.value = err.response?.data?.detail || 'Failed to complete session'
      throw err
    } finally {
      isLoading.value = false
    }
  }

  async function moveToStep(step: number) {
    if (!currentSession.value) return

    console.log('moveToStep called with:', step)

    currentStep.value = step
    stepStartTime.value = Date.now()
    setStepTimer(step)

    console.log('Fetching step data for session:', currentSession.value.id)

    // Reload step data from server
    const response = await learningAPI.getStepData(currentSession.value.id)

    console.log('Got step data:', response)

    currentStepData.value = response.data

    console.log('moveToStep complete, currentStep:', currentStep.value, 'stepData:', currentStepData.value)
  }

  function setStepTimer(step: number) {
    // Step durations in seconds
    const durations: Record<number, number> = {
      1: 2 * 60,  // 2 minutes
      2: 8 * 60,  // 8 minutes
      3: 2 * 60,  // 2 minutes
      4: 2 * 60,  // 2 minutes
      5: 1 * 60,  // 1 minute
    }
    timeRemaining.value = durations[step] || 60
  }

  function resetState() {
    mainScreenData.value = null
    currentSession.value = null
    currentStep.value = 1
    currentStepData.value = null
    error.value = null
    timeRemaining.value = 0
  }

  return {
    // State
    mainScreenData,
    currentSession,
    currentStep,
    currentStepData,
    isLoading,
    error,
    timeRemaining,

    // Computed
    isSessionActive,
    sessionProgress,

    // Actions
    loadMainScreen,
    loadMainScreenForDay,
    startSession,
    resumeSession,
    submitStep1,
    submitStep2,
    submitStep3,
    submitStep4,
    submitStep5,
    completeSession,
    moveToStep,
    resetState,
  }
})
