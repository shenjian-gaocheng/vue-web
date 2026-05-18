<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import OverlayMask from '@/components/OverlayMask.vue'
import Topbar from '@/components/Topbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import Notification from '@/components/Notification.vue'
import { useResponsiveSidebar } from '@/composables/useResponsiveSidebar'
import { useApi } from '@/composables/fetch'
import { useAuthStore } from '@/stores/auth'
import { storeToRefs } from 'pinia'

// 响应式侧边栏
const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()

// 引入 Pinia 状态
const auth = useAuthStore()
const { isLoggedIn } = storeToRefs(auth)  // 保持响应式
const { logout, verifyToken, startPolling, stopPolling } = auth            // 非 ref 的函数可直接解构

// 调用api
const { apiFetch } = useApi()
const router = useRouter()

const username = ref('')
const password = ref('')
const message = ref('')
const authChecked = ref(false)

// 轮询监控登录
onMounted(async () => {
  await verifyToken()
  authChecked.value = true
  startPolling()
})

onUnmounted(() => {
  stopPolling()
})


// 登录
const login = async () => {
  message.value = ''

  if (!username.value || !password.value) {
    message.value = '请输入用户名和密码'
    return
  }

  const { ok, data } = await apiFetch('/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    credentials: 'include',
    body: JSON.stringify({
      username: username.value,
      password: password.value
    })
  })

  if (ok) {
    isLoggedIn.value = true
    message.value = '✅ 登录成功！'
  } else {
    message.value = data.message || '❌ 登录失败'
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
        'flex-column',
        'bg-white',
        'text-center',
        'px-4',
        !isMobile ? 'main-scrollable' : ''
      ]"
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >

      <Notification />

      <div
        style="width: 300px; margin: auto"
        class="d-flex flex-column justify-content-center align-items-center flex-grow-1 text-center"
      >
        <template v-if="!authChecked">
          <h2>加载中...</h2>
        </template>

        <template v-else-if="isLoggedIn">
          <h2>🎉 已登录</h2>
          <button class="btn btn-primary w-100 mt-3" @click="router.push('/admin-logs')">查看操作日志</button>
          <button class="btn btn-danger w-100 mt-3" @click="handleLogout">退出登录</button>
        </template>

        <template v-else>
          <h2 class="mb-3">网站管理员登录</h2>
          <input v-model="username" type="text" placeholder="用户名" class="form-control mb-2" />
          <input v-model="password" type="password" placeholder="密码" class="form-control mb-3" />
          <button @click="login" class="btn btn-primary w-100">登录</button>
        </template>

        <p class="mt-3" :style="{ color: isLoggedIn ? 'green' : 'red' }">{{ message }}</p>
      </div>
    </main>
  </div>
</template>