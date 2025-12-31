<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import OverlayMask from '@/components/OverlayMask.vue'
import Topbar from '@/components/Topbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import ZonedDateTime from '@/components/ZonedDateTime.vue'
// import Modal from '@/components/Modal.vue'
import Notification from '@/components/Notification.vue'
import { useResponsiveSidebar } from '@/composables/useResponsiveSidebar'
import { useApi } from '@/composables/fetch'
// import { useAuthStore } from '@/stores/auth'
// import { storeToRefs } from 'pinia'
// import { useRouter } from 'vue-router'

// 增加路由
// const router = useRouter()

// 响应式侧边栏
const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()

// 引入 Pinia 状态
// const auth = useAuthStore()
// const { token, isLoggedIn } = storeToRefs(auth)  // 保持响应式
// const { verifyToken, startPolling, stopPolling } = auth             // 非 ref 的函数可直接解构

// 调用api
const { apiFetch } = useApi()

// 默认弹框关闭
// const showModal = ref(false)
// const selectedItem = ref(null)        // 原始数据，用于页面展示
// const tempItem = ref({})              // 临时副本，仅用于弹框编辑
// function formatDateForInput(datetimeStr) {
//   // 原始格式: "2025-06-15 13:45:00+08:00"
//   // 去掉秒和时区部分
//   return datetimeStr.replace(' ', 'T').slice(0, 16)
// }
// function toISOWithTimezoneOffset(date) {
//   const pad = (num) => String(num).padStart(2, '0')

//   const yyyy = date.getFullYear()
//   const mm = pad(date.getMonth() + 1)
//   const dd = pad(date.getDate())
//   const hh = pad(date.getHours())
//   const min = pad(date.getMinutes())
//   const ss = pad(date.getSeconds())

//   // 假设固定使用北京时间 +08:00
//   return `${yyyy}-${mm}-${dd}T${hh}:${min}:${ss}+08:00`
// }
// const openModal = (item = null) => {
//   if (item) {
//     // 编辑：深拷贝已有项
//     selectedItem.value = item
//     tempItem.value = JSON.parse(JSON.stringify(item))
//     if (tempItem.value.date) {
//       tempItem.value.date = formatDateForInput(tempItem.value.date)
//     }
//   } else {
//     // 新建：初始化默认值
//     selectedItem.value = null
//     tempItem.value = {
//       session: '0',
//       date: '',
//       type: '',
//       title: '',
//       url: '',
//       cut_url: '',
//       is_stage: false,
//       is_end: false,
//     }
//   }
//   showModal.value = true
// }

// const handleConfirm = async () => {
//   // 校验必填字段
//   if (!tempItem.value.title 
//     || !tempItem.value.date 
//     || !tempItem.value.session
//     || !tempItem.value.type
//   ) {
//     alert('❗ 请填写所有必填项')
//     showModal.value = true
//     return
//   }

//   const payload = {
//     session: tempItem.value.session,
//     date: toISOWithTimezoneOffset(new Date(tempItem.value.date)),
//     type: tempItem.value.type,
//     title: tempItem.value.title,
//     url: tempItem.value.url,
//     cut_url: tempItem.value.cut_url,
//     is_stage: tempItem.value.is_stage,
//     is_end: tempItem.value.is_end
//   }

//   let result
//   try {
//     if (selectedItem.value) {
//       // 编辑（PUT）
//       result = await apiFetch(`/stages/${tempItem.value.id}`, {
//         method: 'PUT',
//         headers: {
//           'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(payload)
//       })
//     } else {
//       // 新建（POST）
//       result = await apiFetch('/stages', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json'
//         },
//         body: JSON.stringify(payload)
//       })
//     }

//     const { ok, status, data } = result

//     if (!ok) {
//       if (status === 401) {
//         alert('⚠️ 登录过期，请重新登录')
//         router.push('/login')
//       } else {
//         alert(`❌ ${selectedItem.value ? '修改' : '添加'}失败：${data.message || '服务器错误'}`)
//       }
//       return
//     }

//     alert(`✅ ${selectedItem.value ? '修改' : '添加'}成功`)
//     showModal.value = false
//     loadStages()

//   } catch (err) {
//     // 捕获网络错误
//     alert('❌ 网络连接失败，请检查网络或稍后重试')
//     console.error(err)
//     return
//   }

//   // showModal.value = false
//   // loadStages()
//   // alert(`✅ ${selectedItem.value ? '修改' : '添加'}成功`)
// }

// 刷新登录状态
// window.addEventListener('storage', (event) => {
//   if (event.key === 'token_zty') {
//     const store = useAuthStore()
//     store.isLoggedIn = !(event.newValue === null)
//   }
// })

const groupedStages = ref({ 'Team SII': [], '新生': [], '其它': [] })
const expandedGroups = ref({ 'Team SII': false, '新生': false, '其它': false })
const maxInitial = 3

const toggleExpanded = group => {
  expandedGroups.value[group] = !expandedGroups.value[group]
}

const loadStages = async () => {
  try {
    const { ok, status, data } = await apiFetch('/stages')
    if (!ok) {
      alert(`❌ 请求失败：${data.message || '未知错误'}`)
      return
    }

    const now = new Date()
    const temp = {
      '今日公演': [],
      '今日行程': [],
      '即将开始': [],
      'Team SII 公演': [],
      '新生公演': [],
      '其它公演及活动': []
    }

    data.forEach(item => {
      const type = item.type?.trim()
      const date = new Date(item.date?.trim())
      const isStage = item.is_stage
      const isUpcoming = date > now

      // 判断是否为今日公演，直接按照0时计算
      const today = new Date()
      today.setHours(0, 0, 0, 0)
      const targetDate = new Date(date)
      targetDate.setHours(0, 0, 0, 0)
      const isCurrent = targetDate.getTime() === today.getTime() && item.is_end === false
    
      if (isCurrent && isStage) {
        temp['今日公演'].push(item)
      } else if (isCurrent && !isStage) {
        temp['今日行程'].push(item)
      } else if (isUpcoming) {
        temp['即将开始'].push(item)
      } else if (type === 'Team SII') {
        temp['Team SII 公演'].push(item)
      } else if (type === '新生' || type === 'New Members') {
        temp['新生公演'].push(item)
      } else {
        temp['其它公演及活动'].push(item)
      }
    })

    for (const key in temp) {
      temp[key].sort((a, b) => {
        // const sessionDiff = parseInt(b.session) - parseInt(a.session)
        // if (sessionDiff !== 0) return sessionDiff

        // session 相同时，再按时间排序
        const dateA = new Date(a.date?.trim())
        const dateB = new Date(b.date?.trim())
        return dateB - dateA  // 时间降序（晚的在前）
      })
    }

    groupedStages.value = temp
    filteredStages.value = { ...temp }
  } catch (e) {
    console.error('加载失败', e)
  }
}

// 判断时区
const isEast8 = ref(true)
const timezone = ref('')

onMounted(() => {
  loadStages()  // 加载
  // getTimezoneOffset 返回的是分钟，东八区 = -480
  isEast8.value = new Date().getTimezoneOffset() === -480
  timezone.value = Intl.DateTimeFormat().resolvedOptions().timeZone
  // verifyToken()
  // startPolling()
})

// onUnmounted(() => {
//   stopPolling()
//   isLoggedIn.value = true
// })

// 搜索
const searchQuery = ref("")
const searchSession = ref("")
const searchStart = ref("")
const searchEnd = ref("")
const searchStartType = ref("text")
const searchEndType = ref("text")
const filteredStages = ref({})

const applyFilters = () => {
  const filtered = {}

  for (const group in groupedStages.value) {
    filtered[group] = groupedStages.value[group].filter(item => {
      const matchQuery =
        !searchQuery.value ||
        item.title.includes(searchQuery.value) ||
        item.type.includes(searchQuery.value)

      const matchSession =
        !searchSession.value ||
        item.session === String(searchSession.value)

      const date = new Date(item.date)
      const matchStart = !searchStart.value || date >= new Date(searchStart.value)
      const matchEnd = !searchEnd.value || date <= new Date(new Date(searchEnd.value).getTime() + 86400000)

      return matchQuery && matchSession && matchStart && matchEnd
    })
  }

  filteredStages.value = filtered
}

const clearFilters = () => {
  searchQuery.value = ""
  searchSession.value = ""
  searchStart.value = ""
  searchEnd.value = ""

  // ✅ 重置类型，恢复 placeholder 显示
  searchStartType.value = "text"
  searchEndType.value = "text"

  filteredStages.value = { ...groupedStages.value }
}

// 判断是否距离现在开始30分钟
const parseToDate = (v) => {
  if (!v) return null

  // 数字：可能是秒/毫秒时间戳
  if (typeof v === 'number') {
    return new Date(v < 1e12 ? v * 1000 : v)
  }

  // 字符串：兼容 "YYYY-MM-DD HH:mm:ss" / "YYYY-MM-DD HH:mm" / ISO
  if (typeof v === 'string') {
    const s = v.trim().replace(' ', 'T') // 让 "2025-12-31 19:00" 变成 ISO 友好格式
    const d = new Date(s)
    return isNaN(d.getTime()) ? null : d
  }

  // Date 对象
  if (v instanceof Date) return v

  return null
}

const canShowLiveButton = (startDateLike) => {
  const start = parseToDate(startDateLike)
  if (!start) return false

  const now = new Date()

  // 提前 30 分钟的时间点
  const showFrom = new Date(start.getTime() - 30 * 60 * 1000)

  return now >= showFrom
}

</script>

<template>
  <div class="layout-page d-flex">
    <!-- 顶部栏：仅移动端显示 -->
    <Topbar
      v-if="isMobile"
      :collapsed="isSidebarCollapsed"
      @update:collapsed="isSidebarCollapsed = $event"
    />

    <!-- 遮罩：必须放在 Sidebar 后面、Main 前面 -->
    <OverlayMask
      v-if="isMobile && !isSidebarCollapsed"
      @click="isSidebarCollapsed = true"
    />

    <!-- 侧边栏 -->
    <Sidebar
      :is-mobile="isMobile"
      v-model:collapsed="isSidebarCollapsed"
    />

    <main
      :class="[
        'flex-grow-1',
        'bg-white',
        'px-4',
        'overflow-auto',
        !isMobile ? 'main-scrollable' : ''
      ]"
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >

      <Notification />

      <!-- 公演说明文字（放在所有公演列表之前） -->
      <div class="alert alert-info mb-4" role="note">
        <p class="mb-1">以下是目前本站收录的 <strong>周童玥</strong> 参加的公演及活动列表，包括即将进行、正在进行以及已经结束的公演和活动。</p>
        <p class="mb-1">收录了Team SII公演、新生公演以及其它公演和活动。</p>
        <p class="mb-1">点击右侧按钮可跳转至发布在 B 站的直播或视频页面。</p>
        <p class="mb-1"><strong>观看直播</strong>：SNH48 官方账号正在直播的公演或活动。</p>
        <p class="mb-1"><strong>完整视频回放</strong>：SNH48 官方账号发布的公演完整视频回放。若回放非官方发布，则会在标题注明。</p>
        <p class="mb-1"><strong>小周cut视频</strong>：公演中周童玥相关内容的剪辑回放。</p>
        <p class="mb-0">如果按钮为灰色，则代表该场公演没有回放，或是没有制作剪辑。</p>
      </div>

      <div v-if="!isEast8" class="alert alert-warning mb-4">
        <p class="mb-1">🌍 <strong>注意：</strong>以下公演及活动所标出的时间，是您当前所在位置（{{ timezone }}）的时间，而非北京时间。</p>
      </div>

      <div class="mt-4 mb-3">
        <h3 class="mb-3">按条件筛选</h3>
        <p class="mb-1">可按关键词、场次、时间来筛选特定的公演。</p>
        <p class="mb-1">若要寻找与周童玥相关的重要公演，请在关键词一栏输入 <strong>周童玥</strong> 并搜索。</p> 
      </div>
      <!-- ✅ 外层布局判断，只换布局，不重复内容 -->
      <div
        :class="[
          'mb-4',
          isMobile ? 'row g-2 justify-content-center' : 'd-flex flex-wrap gap-2 justify-content-center'
        ]"
      >
        <div :class="isMobile ? 'col-10' : 'col-auto'">
          <input v-model="searchQuery" class="form-control form-control-sm" placeholder="关键词，如：幻镜-C版" />
        </div>
        <div :class="isMobile ? 'col-10' : 'col-auto'">
          <input v-model="searchSession" type="number" class="form-control form-control-sm" placeholder="场次，如：155" />
        </div>

        <!-- ✅ 日期输入框：统一用 text + 切换成 date -->
        <div :class="isMobile ? 'col-10' : 'col-auto'">
          <input
            v-model="searchStart"
            :type="searchStartType"
            class="form-control form-control-sm"
            placeholder="开始日期"
            @focus="searchStartType = 'date'"
            @blur="() => { if (!searchStart) searchStartType = 'text' }"
          />
        </div>
        <div :class="isMobile ? 'col-10' : 'col-auto'">
          <input
            v-model="searchEnd"
            :type="searchEndType"
            class="form-control form-control-sm"
            placeholder="结束日期"
            @focus="searchEndType = 'date'"
            @blur="() => { if (!searchEnd) searchEndType = 'text' }"
          />
        </div>

        <div :class="isMobile ? 'col-5' : 'col-auto'">
          <button class="btn btn-primary btn-sm w-100" @click="applyFilters">搜索</button>
        </div>
        <div :class="isMobile ? 'col-5' : 'col-auto'">
          <button class="btn btn-outline-primary btn-sm w-100" @click="clearFilters">重置</button>
        </div>
      </div>


      <!-- <template v-if="isLoggedIn">
        <button class="btn btn-success mb-3" @click="() => openModal()">
          ➕ 新建公演或活动记录
        </button>
      </template> -->

      <div class="w-100">
        <!-- 加载状态 -->
        <div v-if="!Object.keys(filteredStages).length" class="text-center text-muted my-4">
          正在加载…
        </div>

        <!-- 数据已加载 -->
        <template v-for="(items, group) in filteredStages" :key="group">
          <h3 v-if="items.length" class="mt-4 mb-3">{{ group }}</h3>
          <ul class="list-group mb-3">
            <li
              v-for="(item, index) in (expandedGroups[group] ? items : items.slice(0, maxInitial))"
              :key="item.id || item.session + item.date"
              class="list-group-item"
              >
              <div class="d-flex flex-column flex-md-row align-items-md-center gap-2">
                <!-- 左侧：场次 + 日期 -->
                <div class="text-center" style="min-width: 100px;">
                  <div class="fw-bold">
                    {{ item.session !== '0' ? `第 ${item.session} 场` : '不计入场次' }}
                  </div>
                  <ZonedDateTime :datetime="item.date" class="text-muted" />
                </div>

                <!-- 中间：标题 -->
                <div class="flex-grow-1 d-flex justify-content-center align-items-center text-center">
                  <div class="fw-semibold">{{ item.title }}</div>
                </div>

                <!-- 右侧：两个按钮 -->
                <div class="d-flex justify-content-center justify-content-md-end align-items-center gap-2">
                  <!-- 判断 group 是否为“今日公演”，且是否距离开场30分钟之内，然后提供直播入口 -->
                  <template v-if="group === '今日公演' && canShowLiveButton(item.date)">
                    <!-- SNH 或 time 为空 -->
                    <a
                      v-if="!item.time || item.time === 'SNH'"
                      href="https://live.bilibili.com/48"
                      target="_blank"
                      class="btn btn-sm btn-success"
                    >
                      观看直播
                    </a>

                    <!-- GNZ -->
                    <a
                      v-else-if="item.time === 'GNZ'"
                      href="https://live.bilibili.com/391199"
                      target="_blank"
                      class="btn btn-sm btn-success"
                    >
                      观看直播
                    </a>

                    <!-- BEJ -->
                    <a
                      v-else-if="item.time === 'BEJ'"
                      href="https://live.bilibili.com/383045"
                      target="_blank"
                      class="btn btn-sm btn-success"
                    >
                      观看直播
                    </a>

                    <!-- CKG -->
                    <a
                      v-else-if="item.time === 'CKG'"
                      href="https://live.bilibili.com/6015846"
                      target="_blank"
                      class="btn btn-sm btn-success"
                    >
                      观看直播
                    </a>

                    <!-- CGT -->
                    <a
                      v-else-if="item.time === 'CGT'"
                      href="https://live.bilibili.com/27848865"
                      target="_blank"
                      class="btn btn-sm btn-success"
                    >
                      观看直播
                    </a>

                    <!-- 默认情况 -->
                    <a
                      v-else
                      href="javascript:void(0)"
                      target="_blank"
                      class="btn btn-sm btn-success disabled"
                    >
                      暂无直播
                    </a>
                  </template>

                  <!-- 如果是“今日公演”，且距离开场超过30分钟，不提供直播入口 -->
                  <template v-else-if="group === '今日公演'">
                    <a href="javascript:void(0)" class="btn btn-sm btn-success disabled">
                      暂无直播
                    </a>
                  </template>

                  <!-- 判断 group 是否为“今日行程”，然后按钮变灰 -->
                  <template v-else-if="group === '今日行程' || group === '即将开始'">
                    <a
                      href=""
                      target="_blank"
                      class="btn btn-sm btn-success disabled"
                    >
                      暂无直播
                    </a>
                  </template>

                  <!-- 否则显示原有两个按钮 -->
                  <template v-else>
                    <a
                      :href="item.url ? 'https://www.bilibili.com/video/' + item.url : null"
                      target="_blank"
                      class="btn btn-sm"
                      :class="item.url ? 'btn-primary' : 'btn-secondary disabled'"
                      :tabindex="!item.url ? -1 : null"
                      :aria-disabled="!item.url"
                    >
                      完整视频回放
                    </a>

                    <a
                      :href="item.cut_url ? 'https://www.bilibili.com/video/' + item.cut_url : null"
                      target="_blank"
                      class="btn btn-sm"
                      :class="item.cut_url ? 'btn-warning' : 'btn-secondary disabled'"
                      :tabindex="!item.cut_url ? -1 : null"
                      :aria-disabled="!item.cut_url"
                    >
                      小周cut视频
                    </a>
                  </template>

                  <!-- ✅ 登录后显示编辑按钮 -->
                  <!-- <template v-if="isLoggedIn">
                    <button class="btn btn-sm btn-outline-dark" @click="() => openModal(item)">
                      编辑
                    </button>
                  </template> -->
                </div>
              </div>
            </li>
          </ul>
          <button
            v-if="items.length > maxInitial"
            class="btn btn-outline-primary btn-sm mb-4"
            @click="toggleExpanded(group)"
          >
            {{ expandedGroups[group] ? '收起' : '展开更多' }}
          </button>
        </template>
      </div>

      <!-- <Modal v-model="showModal" title="编辑项" @confirm="handleConfirm">
        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">时间 <span class="text-danger">*</span><br>（请输入北京时间）</label>
          <div class="col-sm-9">
            <input v-model="tempItem.date" type="datetime-local" class="form-control" />
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">场次 <span class="text-danger">*</span><br>（如果没有场次或不确定，请填写0）</label>
          <div class="col-sm-9">
            <input v-model="tempItem.session" type="number" class="form-control" />
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">标题 <span class="text-danger">*</span></label>
          <div class="col-sm-9">
            <input v-model="tempItem.title" type="text" class="form-control" />
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">队伍 <span class="text-danger">*</span></label>
          <div class="col-sm-9">
            <select v-model="tempItem.type" class="form-select">
              <option disabled value="">请选择队伍</option>
              <option value="Team SII">Team SII</option>
              <option value="New Members">新生公演</option>
              <option value="Team NII">Team NII</option>
              <option value="Team HII">Team HII</option>
              <option value="Team X">Team X</option>
              <option value="Others">其它（特殊公演或非公演）</option>
            </select>
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">是否已结束 <span class="text-danger">*</span></label>
          <div class="col-sm-9 text-start">
            <input v-model="tempItem.is_end" type="checkbox" class="form-check-input" />
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">是否为公演 <span class="text-danger">*</span></label>
          <div class="col-sm-9 text-start">
            <input v-model="tempItem.is_stage" type="checkbox" class="form-check-input" />
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">完整视频回放<br>（请输入SNH48在b站官号发布的公演视频回放bv号）</label>
          <div class="col-sm-9">
            <input v-model="tempItem.url" type="text" class="form-control" />
          </div>
        </div>

        <div class="form-group row mb-2 align-items-center">
          <label class="col-sm-3 col-form-label text-start">小周cut视频<br>（请输入应援会在b站发布的小周cut视频bv号）</label>
          <div class="col-sm-9">
            <input v-model="tempItem.cut_url" type="text" class="form-control" />
          </div>
        </div>
        你可以放任何 slot 内容，甚至是编辑表单
      </Modal> -->
    </main>
  </div>
</template>