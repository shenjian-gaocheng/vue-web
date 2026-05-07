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

const router = useRouter()
const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()
const { apiFetch } = useApi()

const auth = useAuthStore()
const { isLoggedIn } = storeToRefs(auth)
const { verifyToken, startPolling, stopPolling } = auth

const logs = ref([])
const loading = ref(false)
const errorMessage = ref('')
const logFile = ref('')
const limit = ref(200)

const loadLogs = async () => {
  loading.value = true
  errorMessage.value = ''

  const { ok, status, data } = await apiFetch(`/admin/logs?limit=${limit.value}`)

  if (!ok) {
    if (status === 401) {
      isLoggedIn.value = false
      errorMessage.value = '登录已过期，请重新登录'
      router.push('/admin-login')
    } else if (status === 403) {
      errorMessage.value = '当前账号不是管理员，无法查看日志'
    } else {
      errorMessage.value = data.message || '读取日志失败'
    }
    logs.value = []
    loading.value = false
    return
  }

  logs.value = Array.isArray(data.logs) ? data.logs : []
  logFile.value = data.log_file || ''
  loading.value = false
}

onMounted(async () => {
  await verifyToken()
  if (!isLoggedIn.value) {
    router.push('/admin-login')
    return
  }
  startPolling()
  loadLogs()
})

onUnmounted(() => {
  stopPolling()
})
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
        'bg-white',
        'px-4',
        !isMobile ? 'main-scrollable' : ''
      ]"
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >
      <Notification />

      <div class="d-flex flex-wrap justify-content-between align-items-center mb-3 gap-2">
        <div>
          <h2 class="mb-1">管理员操作日志</h2>
          <!-- <p class="mb-0 text-muted small">只展示包含“用户:”的日志记录</p>
          <p v-if="logFile" class="mb-0 text-muted small">日志文件：{{ logFile }}</p> -->
        </div>

        <div class="d-flex align-items-center gap-2">
          <input
            v-model.number="limit"
            type="number"
            class="form-control form-control-sm"
            min="1"
            max="1000"
            style="width: 110px;"
            title="最多显示条数"
          />
          <button class="btn btn-primary btn-sm" @click="loadLogs" :disabled="loading">
            {{ loading ? '加载中...' : '刷新日志' }}
          </button>
        </div>
      </div>

      <div v-if="errorMessage" class="alert alert-danger" role="alert">
        {{ errorMessage }}
      </div>

      <div v-else-if="loading" class="text-muted">正在读取日志...</div>

      <div v-else-if="logs.length === 0" class="text-muted">没有匹配到包含“用户:”的日志。</div>

      <ul v-else class="list-group mb-4">
        <li
          v-for="(line, idx) in logs"
          :key="idx"
          class="list-group-item"
          style="font-family: 'Courier New', monospace; white-space: pre-wrap; word-break: break-word;"
        >
          {{ line }}
        </li>
      </ul>
    </main>
  </div>
</template>