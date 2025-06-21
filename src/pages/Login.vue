<script setup>
import { ref } from 'vue'
import OverlayMask from '@/components/OverlayMask.vue'
import Topbar from '@/components/Topbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import { useResponsiveSidebar } from '@/composables/useResponsiveSidebar'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

// 响应式侧边栏
const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()

// 引入 Pinia 状态
const auth = useAuthStore()
const { token, isLoggedIn } = storeToRefs(auth)  // 保持响应式
const { logout } = auth             // 非 ref 的函数可直接解构

const username = ref('')
const password = ref('')
const message = ref('')

// 登录
const login = async () => {
  message.value = ''

  if (!username.value || !password.value) {
    message.value = '请输入用户名和密码'
    return
  }

  try {
    const res = await fetch('http://127.0.0.1:5001/api/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      credentials: 'include',
      body: JSON.stringify({
        username: username.value,
        password: password.value
      })
    })

    const data = await res.json()
    if (res.ok) {
      token.value = data.token
      localStorage.setItem('token_zty', token.value)
      isLoggedIn.value = true
      message.value = '✅ 登录成功！'
    } else {
      message.value = data.message || '❌ 登录失败'
    }
  } catch (err) {
    console.error(err)
    message.value = '❌ 网络错误'
  }
}

// 退出登录
const handleLogout = () => {
  logout()
  message.value = '👋 已成功退出登录'
}

</script>

<template>
  <div class="layout-page d-flex">
    <Topbar
      v-if="isMobile"
      :collapsed="isSidebarCollapsed"
      @update:collapsed="isSidebarCollapsed = $event"
    />

    <OverlayMask
      v-if="isMobile && !isSidebarCollapsed"
      @click="isSidebarCollapsed = true"
    />

    <Sidebar
      :is-mobile="isMobile"
      v-model:collapsed="isSidebarCollapsed"
    />

    <main
      :class="[
        'flex-fill',
        'd-flex',
        'justify-content-center',
        'align-items-center',
        'bg-white',
        'text-center',
        !isMobile ? 'main-scrollable' : ''
      ]"
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >
      <div style="width: 300px">
        <template v-if="isLoggedIn">
          <h2>🎉 已登录</h2>
          <button class="btn btn-danger w-100 mt-3" @click="handleLogout">退出登录</button>
        </template>

        <template v-else>
          <h2 class="mb-3">登录</h2>
          <input v-model="username" type="text" placeholder="用户名" class="form-control mb-2" />
          <input v-model="password" type="password" placeholder="密码" class="form-control mb-3" />
          <button @click="login" class="btn btn-primary w-100">登录</button>
        </template>

        <p class="mt-3" :style="{ color: isLoggedIn ? 'green' : 'red' }">{{ message }}</p>
      </div>
    </main>
  </div>
</template>