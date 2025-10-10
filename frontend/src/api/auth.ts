import type { User } from '@/types/user'
import { api } from '@/utils/api'

interface LoginRequest {
  username: string
  password: string
}

export interface LoginResponse {
  access?: string
  refresh?: string
  token?: string
  user?: User
}

export async function login(credentials: LoginRequest): Promise<LoginResponse> {
  try {
    const response = await api.postSilent<LoginRequest, LoginResponse>('/users/token/', credentials)

    if (!response) {
      throw new Error('Login response is null')
    }
    return response
  } catch (error: any) {
    throw error
  }
}