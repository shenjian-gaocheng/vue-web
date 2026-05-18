<script setup>
import { ref, onMounted, onUnmounted, nextTick } from 'vue'
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
const authChecked = ref(false)

// ---- 聊天状态 ----
const messages = ref([])   // { role: 'user'|'assistant', text: string, sources?: [] }
const inputText = ref('')
const loading = ref(false)
const errorMessage = ref('')
const chatBox = ref(null)

const scrollToBottom = async () => {
  await nextTick()
  if (chatBox.value) {
    chatBox.value.scrollTop = chatBox.value.scrollHeight
  }
}

const sendMessage = async () => {
  const question = inputText.value.trim()
  if (!question || loading.value) return

  messages.value.push({ role: 'user', text: question })
  inputText.value = ''
  loading.value = true
  errorMessage.value = ''
  scrollToBottom()

  const { ok, status, data } = await apiFetch('/knowledge-base/chat', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, top_k: 5 }),
  })

  loading.value = false

  if (!ok) {
    if (status === 401) {
      isLoggedIn.value = false
      router.push('/admin-login')
      return
    }
    errorMessage.value = data.message || '请求失败，请稍后再试'
    scrollToBottom()
    return
  }

  messages.value.push({
    role: 'assistant',
    text: data.answer,
    sources: data.used_model ? data.matched_sources : [],
  })
  scrollToBottom()
}

// ---- 重建知识库 ----
const rebuilding = ref(false)
const rebuildMessage = ref('')
const rebuildSuccess = ref(false)

const rebuildKnowledgeBase = async () => {
  rebuilding.value = true
  rebuildMessage.value = ''
  const { ok, data } = await apiFetch('/knowledge-base/rebuild', { method: 'POST' })
  rebuilding.value = false
  rebuildSuccess.value = ok
  rebuildMessage.value = ok ? `重建成功：共 ${data.stats?.total_documents ?? '?'} 篇文档` : (data.message || '重建失败')
}

const handleKeydown = (e) => {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault()
    sendMessage()
  }
}

onMounted(async () => {
  await verifyToken()
  authChecked.value = true
  if (!isLoggedIn.value) {
    router.push('/admin-login')
    return
  }
  startPolling()
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
        'position-relative',
        'flex-grow-1',
        'overflow-auto',
        'px-4',
        !isMobile ? 'main-scrollable' : ''
      ]"
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >
      <Notification />

      <div v-if="!authChecked" class="text-muted py-4 text-center">正在校验登录状态...</div>

      <div v-else-if="isLoggedIn" class="row justify-content-center">
        <div class="col-md-10 col-xl-8">
          <h4 class="mb-3">🤖 知识库问答 <small class="text-muted fs-6">（仅限内测用户）</small></h4>

          <!-- 消息列表 -->
          <div
            ref="chatBox"
            class="chat-box border rounded bg-white p-3 mb-3"
            style="height: 60vh; overflow-y: auto;"
          >
            <div v-if="messages.length === 0" class="text-muted text-center mt-5">
              你好！请向我提问关于小周的任何内容～
            </div>

            <div
              v-for="(msg, idx) in messages"
              :key="idx"
              class="mb-3"
              :class="msg.role === 'user' ? 'text-end' : 'text-start'"
            >
              <!-- 气泡 -->
              <span
                class="d-inline-block px-3 py-2 rounded-3 text-start"
                style="max-width: 80%; white-space: pre-wrap; word-break: break-word;"
                :class="msg.role === 'user'
                  ? 'bg-warning text-dark'
                  : 'bg-light border'"
              >{{ msg.text }}</span>

              <!-- 来源标签 -->
              <div
                v-if="msg.sources && msg.sources.length"
                class="mt-1 text-muted small"
              >
                参考来源：
                <span
                  v-for="src in msg.sources"
                  :key="src.id"
                  class="badge bg-secondary me-1"
                >{{ src.source_label }} · {{ src.title }}</span>
              </div>
            </div>

            <!-- 加载中 -->
            <div v-if="loading" class="text-start mb-3">
              <span class="d-inline-block px-3 py-2 rounded-3 bg-light border text-muted">
                思考中…
              </span>
            </div>
          </div>

          <!-- 错误提示 -->
          <div v-if="errorMessage" class="alert alert-danger py-2">{{ errorMessage }}</div>

          <!-- 输入框 -->
          <div class="input-group">
            <textarea
              v-model="inputText"
              class="form-control"
              rows="2"
              placeholder="输入问题，按 Enter 发送，Shift+Enter 换行"
              style="resize: none;"
              @keydown="handleKeydown"
              :disabled="loading"
            ></textarea>
            <button
              class="btn btn-warning"
              @click="sendMessage"
              :disabled="loading || !inputText.trim()"
            >发送</button>
          </div>
          <div class="d-flex align-items-center gap-2 mt-2">
            <div class="text-muted small">本功能基于 DeepSeek 模型，仅根据知识库内容作答。回答仅供参考，无法保证准确性。<br>本站不会保存您的提问内容。</div>
            <button
              class="btn btn-outline-secondary btn-sm ms-auto"
              @click="rebuildKnowledgeBase"
              :disabled="rebuilding"
            >{{ rebuilding ? '重建中…' : '🔄 重建知识库' }}</button>
          </div>
          <div v-if="rebuildMessage" class="small mt-1" :class="rebuildSuccess ? 'text-success' : 'text-danger'">{{ rebuildMessage }}</div>
        </div>
      </div>
    </main>
  </div>
</template>
