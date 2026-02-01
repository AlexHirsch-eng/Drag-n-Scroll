import { apiClient } from './client'

// Types for Chat App
export interface ChatRoom {
  id: number
  name: string
  room_type: 'direct' | 'group'
  avatar?: string
  other_user?: {
    id: number
    username: string
    email: string
    profile: any
    avatar?: string
    online?: boolean
  }
  participants_count: number
  last_message_preview?: string
  last_message_sender?: 'me' | 'them'
  last_message_at?: string
  unread_count: number
  created_at: string
  updated_at: string
}

export interface ChatRoomDetail {
  id: number
  name: string
  room_type: 'direct' | 'group'
  avatar?: string
  other_user?: {
    id: number
    username: string
    email: string
    profile: any
    avatar?: string
    online?: boolean
  }
  participants: ChatParticipant[]
  participants_count: number
  unread_count: number
  last_message?: {
    id: number
    text: string
    sender_id: number
    message_type: string
    status: string
    created_at: string
  }
  created_at: string
  updated_at: string
}

export interface ChatParticipant {
  id: number
  user: {
    id: number
    username: string
    email: string
    profile: any
  }
  role: 'admin' | 'member'
  last_read_at: string
  nickname?: string
  joined_at: string
  is_online: boolean
}

export interface ChatMessage {
  id: number
  room: number
  sender_id: number
  sender: {
    id: number
    username: string
    email: string
    profile: any
  }
  message_type: 'text' | 'image' | 'video' | 'audio' | 'file'
  text: string
  attachment?: any
  reply_to?: {
    id: number
    text: string
    sender: string
  }
  status: 'sent' | 'delivered' | 'read'
  created_at: string
  updated_at: string
  translation_ru?: string | null
  translation_en?: string | null
  translation_zh?: string | null
  translated_at?: string | null
}

export interface Story {
  id: number
  user: {
    id: number
    username: string
    email: string
    profile: any
  }
  media_file: string
  media_type: 'image' | 'video'
  thumbnail?: string
  duration?: number
  views_count: number
  is_viewed: boolean
  created_at: string
  expires_at: string
}

export interface SuggestedUser {
  id: number
  username: string
  bio: string
  avatar: string
  online: boolean
}

export interface UserBlock {
  blocker: any
  blocked: any
  created_at: string
}

// API functions
export const chatAPI = {
  // Chat Rooms
  async getChatRooms(): Promise<ChatRoom[]> {
    return apiClient.get('/chat/rooms/')
  },

  async getChatRoom(id: number): Promise<ChatRoomDetail> {
    return apiClient.get(`/chat/rooms/${id}/`)
  },

  async createDirectChat(userId: number): Promise<ChatRoom> {
    return apiClient.post('/chat/rooms/create_direct/', { user_id: userId })
  },

  async createGroupChat(name: string): Promise<ChatRoomDetail> {
    return apiClient.post('/chat/rooms/', { name, room_type: 'group' })
  },

  async addParticipant(roomId: number, userId: number): Promise<{ message: string }> {
    return apiClient.post(`/chat/rooms/${roomId}/add_participant/`, { user_id: userId })
  },

  async leaveRoom(roomId: number): Promise<{ message: string }> {
    return apiClient.post(`/chat/rooms/${roomId}/leave/`)
  },

  // Messages
  async getMessages(roomId: number): Promise<ChatMessage[]> {
    return apiClient.get(`/chat/messages/?room=${roomId}`)
  },

  async sendMessage(roomId: number, text: string, options?: { messageType?: string; replyTo?: number; attachment?: any }): Promise<ChatMessage> {
    return apiClient.post('/chat/messages/', {
      room: roomId,
      text,
      message_type: options?.messageType || 'text',
      reply_to: options?.replyTo,
      attachment: options?.attachment
    })
  },

  async getUnreadMessages(): Promise<ChatMessage[]> {
    return apiClient.get('/chat/messages/unread/')
  },

  async markMessagesRead(roomId: number): Promise<{ message: string }> {
    return apiClient.post(`/chat/rooms/${roomId}/read/`)
  },

  // Suggested Users
  async getSuggestedUsers(): Promise<SuggestedUser[]> {
    return apiClient.get('/chat/users/suggested/')
  },

  // Stories
  async getStories(): Promise<Story[]> {
    return apiClient.get('/chat/stories/')
  },

  async createStory(mediaFile: File, mediaType: string, thumbnail?: File, duration?: number): Promise<Story> {
    const formData = new FormData()
    formData.append('media_file', mediaFile)
    formData.append('media_type', mediaType)
    if (thumbnail) formData.append('thumbnail', thumbnail)
    if (duration) formData.append('duration', duration.toString())

    return apiClient.post('/chat/stories/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  async getStory(storyId: number): Promise<Story> {
    return apiClient.get(`/chat/stories/${storyId}/`)
  },

  async deleteStory(storyId: number): Promise<{ message: string }> {
    return apiClient.delete(`/chat/stories/${storyId}/`)
  },

  async getUserStories(userId: number): Promise<Story[]> {
    return apiClient.get(`/chat/users/${userId}/stories/`)
  },

  async reactToStory(storyId: number, emoji: string): Promise<any> {
    return apiClient.post(`/chat/stories/${storyId}/react/`, { emoji })
  },

  // User Blocking
  async getBlockedUsers(): Promise<UserBlock[]> {
    return apiClient.get('/chat/users/blocked/')
  },

  async blockUser(userId: number): Promise<{ message: string }> {
    return apiClient.post('/chat/users/blocked/', { user_id: userId })
  },

  async unblockUser(userId: number): Promise<{ message: string }> {
    return apiClient.delete(`/chat/users/blocked/${userId}/`)
  },

  // Typing Indicators
  async sendTypingIndicator(roomId: number): Promise<{ message: string }> {
    return apiClient.post('/chat/typing/', { room_id: roomId })
  },

  async getTypingUsers(roomId: number): Promise<any[]> {
    return apiClient.get(`/chat/rooms/${roomId}/typing/`)
  },

  // Message Translation
  async translateMessage(messageId: number, targetLanguage: 'ru' | 'en' | 'zh'): Promise<ChatMessage> {
    return apiClient.post(`/chat/messages/${messageId}/translate/`, {
      target_language: targetLanguage
    })
  },
}
