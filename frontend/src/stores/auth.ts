import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authAPI } from '@/api/auth'
import type { User, UserProfile, UserProgress, RegisterData, LoginData } from '@/types/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref<User | null>(null)
  const profile = ref<UserProfile | null>(null)
  const progress = ref<UserProgress | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)
  const isLoading = ref(false)
  const isInitialized = ref(false)
  const isAuthenticated = computed(() => !!user.value && !!accessToken.value)

  // Actions
  async function register(data: RegisterData) {
    try {
      const response = await authAPI.register(data)
      user.value = response.user
      accessToken.value = response.tokens.access
      refreshToken.value = response.tokens.refresh

      localStorage.setItem('access_token', response.tokens.access)
      localStorage.setItem('refresh_token', response.tokens.refresh)

      await loadProfile()
      return true
    } catch (error) {
      console.error('Registration failed:', error)
      throw error
    }
  }

  async function login(data: LoginData) {
    try {
      const response = await authAPI.login(data)
      accessToken.value = response.access
      refreshToken.value = response.refresh

      localStorage.setItem('access_token', response.access)
      localStorage.setItem('refresh_token', response.refresh)

      await loadUser()
      return true
    } catch (error) {
      console.error('Login failed:', error)
      throw error
    }
  }

  async function logout() {
    try {
      if (refreshToken.value) {
        await authAPI.logout(refreshToken.value)
      }
    } catch (error) {
      console.error('Logout failed:', error)
    } finally {
      // Clear local state regardless of API call success
      user.value = null
      profile.value = null
      progress.value = null
      accessToken.value = null
      refreshToken.value = null

      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
    }
  }

  async function loadUser() {
    try {
      const userData = await authAPI.getCurrentUser()
      user.value = userData
      profile.value = userData.profile || null
      progress.value = userData.progress || null
    } catch (error) {
      console.error('Failed to load user:', error)
      throw error
    }
  }

  async function loadProfile() {
    try {
      const [profileData, progressData] = await Promise.all([
        authAPI.getProfile(),
        authAPI.getProgress(),
      ])
      profile.value = profileData
      progress.value = progressData
    } catch (error) {
      console.error('Failed to load profile:', error)
    }
  }

  async function updateProfile(data: Partial<UserProfile>) {
    try {
      const updated = await authAPI.updateProfile(data)
      profile.value = updated
      if (user.value) {
        user.value.profile = updated
      }
    } catch (error) {
      console.error('Failed to update profile:', error)
      throw error
    }
  }

  async function initializeAuth() {
    const access = localStorage.getItem('access_token')
    const refresh = localStorage.getItem('refresh_token')

    if (access && refresh) {
      accessToken.value = access
      refreshToken.value = refresh
      isLoading.value = true
      try {
        await loadUser()
      } catch {
        // Token might be expired, clear auth
        logout()
      } finally {
        isLoading.value = false
        isInitialized.value = true
      }
    } else {
      isInitialized.value = true
    }
  }

  return {
    user,
    profile,
    progress,
    accessToken,
    refreshToken,
    isLoading,
    isInitialized,
    isAuthenticated,
    register,
    login,
    logout,
    loadUser,
    loadProfile,
    updateProfile,
    initializeAuth,
  }
})
