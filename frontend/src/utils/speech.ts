/**
 * Chinese Text-to-Speech using Web Speech API
 * Uses native browser speechSynthesis (no external APIs)
 */

export function speakChinese(text: string, rate: number = 0.8): void {
  if (!text || typeof window === 'undefined') {
    return
  }

  // Check if speech synthesis is supported
  if (!('speechSynthesis' in window)) {
    console.warn('Web Speech API not supported in this browser')
    return
  }

  // Cancel any ongoing speech
  window.speechSynthesis.cancel()

  // Create utterance
  const utterance = new SpeechSynthesisUtterance(text)

  // Set language to Chinese
  utterance.lang = 'zh-CN'
  utterance.rate = rate
  utterance.pitch = 1
  utterance.volume = 1

  // Try to find a Chinese voice
  const voices = window.speechSynthesis.getVoices()
  const chineseVoice = voices.find(voice =>
    voice.lang.startsWith('zh') ||
    voice.lang.includes('chinese') ||
    voice.lang.includes('CN')
  )

  if (chineseVoice) {
    utterance.voice = chineseVoice
  }

  // Speak
  window.speechSynthesis.speak(utterance)
}

/**
 * Preload voices (call this on app mount)
 */
export function preloadVoices(): void {
  if ('speechSynthesis' in window) {
    window.speechSynthesis.getVoices()
  }
}

/**
 * Check if Chinese voice is available
 */
export function hasChineseVoice(): boolean {
  if (!('speechSynthesis' in window)) {
    return false
  }

  const voices = window.speechSynthesis.getVoices()
  return voices.some(voice =>
    voice.lang.startsWith('zh') ||
    voice.lang.includes('chinese') ||
    voice.lang.includes('CN')
  )
}
