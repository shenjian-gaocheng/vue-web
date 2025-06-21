import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

export function useApi() {
//   const baseUrl = 'http://127.0.0.1:5001/api'
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
    return res.json()
  }

  return { apiFetch }
}