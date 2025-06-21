import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const token = ref(localStorage.getItem('token_zty') || '')
  const isLoggedIn = ref(!!token.value)

  let intervalId = null // ⏱️ 保存轮询 ID

  function logout() {
    token.value = ''
    isLoggedIn.value = false
    localStorage.removeItem('token_zty')
  }

  async function verifyToken() {
    const storedToken = localStorage.getItem('token_zty')
    if (!storedToken) {
      logout()
      return
    }

    try {
      const res = await fetch('http://118.196.20.148:5000/api/verify', {
        headers: { Authorization: `Bearer ${storedToken}` }
      })

      if (res.ok) {
        token.value = storedToken
        isLoggedIn.value = true
      } else {
        logout()
      }
    } catch (err) {
      console.error('验证失败:', err)
      logout()
    }
  }

  function startPolling(interval = 10 * 60 * 1000) { // 默认 10 秒轮询
    stopPolling()
    intervalId = setInterval(() => {
      verifyToken()
    }, interval)
  }

  function stopPolling() {
    if (intervalId) {
      clearInterval(intervalId)
      intervalId = null
    }
  }

  return { token, isLoggedIn, logout, verifyToken, startPolling, stopPolling }
})