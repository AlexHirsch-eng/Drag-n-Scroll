import axios, { AxiosInstance } from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '/api'

class APIClient {
  private client: AxiosInstance

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
      // Disable caching to prevent stale 404 responses
      paramsSerializer: {
        indexes: null
      }
    })

    // Request interceptor - add auth token
    this.client.interceptors.request.use(
      (config) => {
        const accessToken = localStorage.getItem('access_token')
        if (accessToken) {
          config.headers.Authorization = `Bearer ${accessToken}`
        }
        return config
      },
      (error) => Promise.reject(error)
    )

    // Response interceptor - handle token refresh
    this.client.interceptors.response.use(
      (response) => response,
      async (error: any) => {
        const originalRequest = error.config

        if (error.response?.status === 401 && originalRequest && !originalRequest._retry) {
          originalRequest._retry = true

          try {
            const refreshToken = localStorage.getItem('refresh_token')
            if (refreshToken) {
              const response = await axios.post(`${API_BASE_URL}/auth/jwt/refresh/`, {
                refresh: refreshToken,
              })

              const { access } = response.data
              localStorage.setItem('access_token', access)

              if (originalRequest.headers) {
                originalRequest.headers.Authorization = `Bearer ${access}`
              }

              return this.client(originalRequest)
            }
          } catch (refreshError) {
            // Refresh failed - clear tokens and redirect to login
            localStorage.removeItem('access_token')
            localStorage.removeItem('refresh_token')
            window.location.href = '/login'
            return Promise.reject(refreshError)
          }
        }

        return Promise.reject(error)
      }
    )
  }

  async get<T>(url: string, params?: any) {
    const response = await this.client.get<T>(url, { params })
    return response.data
  }

  async post<T>(url: string, data?: any, config?: any) {
    const response = await this.client.post<T>(url, data, config)
    return response.data
  }

  async patch<T>(url: string, data?: any) {
    const response = await this.client.patch<T>(url, data)
    return response.data
  }

  async put<T>(url: string, data?: any) {
    const response = await this.client.put<T>(url, data)
    return response.data
  }

  async delete<T>(url: string) {
    const response = await this.client.delete<T>(url)
    return response.data
  }
}

export const apiClient = new APIClient()
