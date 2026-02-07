import { apiClient } from './client'
import type {
  User,
  AuthTokens,
  RegisterData,
  LoginData,
  UserProfile,
  UserProgress,
} from '@/types/api'

export const authAPI = {
  async register(data: RegisterData): Promise<{ user: User; tokens: AuthTokens }> {
    return apiClient.post('/auth/users/', data)
  },

  async login(data: LoginData): Promise<AuthTokens & { user: User }> {
    return apiClient.post('/auth/jwt/create/', data)
  },

  async logout(refreshToken: string): Promise<void> {
    return apiClient.post('/auth/logout/', { refresh: refreshToken })
  },

  async refreshToken(refreshToken: string): Promise<{ access: string }> {
    return apiClient.post('/auth/jwt/refresh/', { refresh: refreshToken })
  },

  async getCurrentUser(): Promise<User> {
    return apiClient.get('/auth/users/me/')
  },

  async getProfile(): Promise<UserProfile> {
    return apiClient.get('/user/profile/')
  },

  async updateProfile(data: Partial<UserProfile>): Promise<UserProfile> {
    return apiClient.patch('/user/profile/', data)
  },

  async getProgress(): Promise<UserProgress> {
    const user = await apiClient.get<User>('/user/me/')
    return user.progress as UserProgress
  },

  async getUserById(userId: number): Promise<User> {
    return apiClient.get(`/user/by-id/${userId}/`)
  },
}
