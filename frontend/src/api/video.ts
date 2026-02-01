import { apiClient } from './client'

// Types for Video App
export interface Video {
  id: number
  creator: {
    id: number
    username: string
    email: string
    profile: any
    followers_count: number
    following_count: number
    is_following: boolean
  }
  video_file: string
  url: string // Добавлено для совместимости с фронтендом
  thumbnail: string
  duration: number
  description: string
  category: VideoCategory
  tags: string[]
  music_title: string
  lesson_number?: number
  lesson_title?: string
  lesson_words?: any[]
  lesson?: {
    lesson_number: number
    title: string
    words: any[]
  } // Добавлено для совместимости
  views_count: number
  likes_count: number
  comments_count: number
  shares_count: number
  is_liked: boolean
  is_saved: boolean
  created_at: string
}

export interface VideoCategory {
  id: number
  name: string
  description: string
}

export interface VideoComment {
  id: number
  video: number
  user: {
    id: number
    username: string
    email: string
    profile: any
  }
  parent?: number
  text: string
  likes_count: number
  is_liked: boolean
  replies: VideoComment[]
  created_at: string
  updated_at: string
  translation_ru?: string | null
  translation_en?: string | null
  translated_at?: string | null
}

export interface VideoHashtag {
  tag: string
  uses_count: number
}

export interface UserFollowing {
  id: number
  follower: any
  following: any
  created_at: string
}

export interface VideoListResponse {
  videos: Video[]
  page: number
  has_more: boolean
  total: number
}

// API functions
export const videoAPI = {
  // Video Feed
  async getFeed(page: number = 1, pageSize: number = 20): Promise<VideoListResponse> {
    return apiClient.get(`/video/videos/feed/?page=${page}&page_size=${pageSize}`)
  },

  async getTrending(): Promise<Video[]> {
    return apiClient.get('/video/videos/trending/')
  },

  async getVideosByCategory(categoryId: number): Promise<Video[]> {
    return apiClient.get(`/video/videos/category/?category=${categoryId}`)
  },

  async getVideosByHashtag(tag: string): Promise<Video[]> {
    return apiClient.get(`/video/videos/hashtag/?tag=${encodeURIComponent(tag)}`)
  },

  async getMyVideos(): Promise<Video[]> {
    return apiClient.get('/video/videos/my_videos/')
  },

  async getSavedVideos(): Promise<Video[]> {
    return apiClient.get('/video/videos/saved/')
  },

  // Video CRUD
  async getVideo(id: number): Promise<Video> {
    return apiClient.get(`/video/videos/${id}/`)
  },

  async createVideo(data: FormData): Promise<Video> {
    return apiClient.post('/video/videos/', data, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  async updateVideo(id: number, data: any): Promise<Video> {
    return apiClient.put(`/video/videos/${id}/`, data)
  },

  async deleteVideo(id: number): Promise<void> {
    return apiClient.delete(`/video/videos/${id}/`)
  },

  // Video Interactions
  async likeVideo(id: number): Promise<{ is_liked: boolean; likes_count: number }> {
    return apiClient.post(`/video/videos/${id}/like/`)
  },

  async bookmarkVideo(id: number): Promise<{ is_saved: boolean }> {
    return apiClient.post(`/video/videos/${id}/bookmark/`)
  },

  async shareVideo(id: number, platform: string): Promise<{ shares_count: number }> {
    return apiClient.post(`/video/videos/${id}/share/`, { platform })
  },

  // Comments
  async getComments(videoId: number): Promise<VideoComment[]> {
    return apiClient.get(`/video/videos/${videoId}/comments/`)
  },

  async createComment(videoId: number, text: string, parentId?: number): Promise<VideoComment[]> {
    return apiClient.post(`/video/videos/${videoId}/comments/`, {
      text,
      parent: parentId
    })
  },

  async likeComment(commentId: number): Promise<{ is_liked: boolean; likes_count: number }> {
    return apiClient.post(`/video/comments/${commentId}/like/`)
  },

  async translateComment(commentId: number, targetLanguage: 'ru' | 'en'): Promise<VideoComment> {
    return apiClient.post(`/video/comments/${commentId}/translate/`, {
      target_language: targetLanguage
    })
  },

  // User Actions
  async getUserFeed(userId: number): Promise<Video[]> {
    return apiClient.get(`/video/users/${userId}/feed/`)
  },

  async followUser(userId: number): Promise<{ is_following: boolean }> {
    return apiClient.post(`/video/users/${userId}/follow/`)
  },

  async reportVideo(videoId: number, reason: string, description?: string): Promise<{ message: string }> {
    return apiClient.post(`/video/videos/${videoId}/report/`, { reason, description })
  },

  // Categories
  async getCategories(): Promise<VideoCategory[]> {
    return apiClient.get('/video/categories-list/')
  },

  // Hashtags
  async getHashtags(): Promise<VideoHashtag[]> {
    return apiClient.get('/video/hashtags/')
  },

  // Admin - Import videos from folder
  async importVideosFromFolder(): Promise<{
    total: number
    imported: number
    skipped: number
    errors: number
    videos: Array<{ title: string; status: string }>
  }> {
    return apiClient.post('/video/admin/import-videos/')
  },
}
