import { defineStore } from 'pinia'
import { ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
  const isLoggedIn = ref(false)

  let intervalId = null

  async function logout() {
    isLoggedIn.value = false
    await fetch('https://zty0322.top/api/logout', {
      method: 'POST',
      credentials: 'include'
    }).catch(() => {})
  }

  async function verifyToken() {
    try {
      const res = await fetch('https://zty0322.top/api/verify', {
        credentials: 'include'
      })
      isLoggedIn.value = res.ok
    } catch (err) {
      console.error('验证失败:', err)
      isLoggedIn.value = false
    }
  }

  function startPolling(interval = 10 * 60 * 1000) {
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

  return { isLoggedIn, logout, verifyToken, startPolling, stopPolling }
})