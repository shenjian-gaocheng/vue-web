import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

export function useApi() {

  const baseUrl = 'http://118.196.20.148:5000/api'
  const auth = useAuthStore()
  const { token } = storeToRefs(auth)

  const apiFetch = async (path, options = {}) => {
    const headers = options.headers || {}
    if (token.value) {
      headers['Authorization'] = `Bearer ${token.value}`
    }

    const res = await fetch(`${baseUrl}${path}`, {
      ...options,
      headers
    })

    const data = await res.json().catch(() => ({}))  // 防止空响应体时报错
    return { ok: res.ok, status: res.status, data }
  }

  return { apiFetch }
}