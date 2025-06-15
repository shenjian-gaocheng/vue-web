<script setup>
import { ref, onMounted } from 'vue'
import OverlayMask from '../components/OverlayMask.vue'
import Topbar from '../components/Topbar.vue'
import Sidebar from '../components/Sidebar.vue'
import ZonedDateTime from '../components/ZonedDateTime.vue'
import { useResponsiveSidebar } from '../composables/useResponsiveSidebar'

const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()

const groupedStages = ref({ 'Team SII': [], '新生': [], '其它': [] })
const expandedGroups = ref({ 'Team SII': false, '新生': false, '其它': false })
const maxInitial = 3

const toggleExpanded = group => {
  expandedGroups.value[group] = !expandedGroups.value[group]
}

onMounted(async () => {
  try {
    const res = await fetch('http://113.44.8.72:5000/api/stages')
    const data = await res.json()
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
      const isCurrent = date <= now && item.is_end === false
    
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
        const sessionDiff = parseInt(b.session) - parseInt(a.session)
        if (sessionDiff !== 0) return sessionDiff

        // session 相同时，再按时间排序
        const dateA = new Date(a.date?.trim())
        const dateB = new Date(b.date?.trim())
        return dateB - dateA  // 时间降序（晚的在前）
      })
    }

    groupedStages.value = temp
  } catch (e) {
    console.error('加载失败', e)
  }
})
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
        'px-5',
        'overflow-auto',
        !isMobile ? 'main-scrollable' : ''
      ]"
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >
      <!-- 公演说明文字（放在所有公演列表之前） -->
      <div class="alert alert-info mb-4" role="note">
        <p class="mb-1">以下是目前本站收录的 <strong>周童玥</strong> 参加的公演及活动列表，包括即将进行、正在进行以及已经结束的公演和活动。</p>
        <p class="mb-1">收录了Team SII公演、新生公演以及其它公演和活动。</p>
        <p class="mb-1">点击右侧按钮可跳转至发布在 B 站的直播或视频页面。</p>
        <p class="mb-1"><strong>观看直播</strong>：SNH48 官方账号正在直播的公演或活动。</p>
        <p class="mb-1"><strong>完整视频回放</strong>：SNH48 官方账号发布的完整视频回放。</p>
        <p class="mb-1"><strong>小周cut视频</strong>：应援会发布的以周童玥为主的剪辑回放。</p>
        <p class="mb-0">如果按钮为灰色，则代表该场公演官方没有上传回放，或是应援会没有制作剪辑。</p>
      </div>
      <div class="w-100">
        <template v-for="(items, group) in groupedStages" :key="group">
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
                    {{ item.session !== '0' ? `第 ${item.session} 场` : '场次未知' }}
                  </div>
                  <ZonedDateTime :datetime="item.date" class="text-muted" />
                </div>

                <!-- 中间：标题 -->
                <div class="flex-grow-1 d-flex justify-content-center align-items-center text-center">
                  <div class="fw-semibold">{{ item.title }}</div>
                </div>

                <!-- 右侧：两个按钮 -->
                <div class="d-flex justify-content-center justify-content-md-end align-items-center gap-2">
                  <!-- 判断 group 是否为“今日公演”，然后提供直播入口 -->
                  <template v-if="group === '今日公演' ">
                    <a
                      href="https://live.bilibili.com/48"
                      target="_blank"
                      class="btn btn-sm btn-success"
                    >
                      观看直播
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
    </main>
  </div>
</template>