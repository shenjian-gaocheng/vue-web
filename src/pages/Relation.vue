<script setup>
import { ref, onMounted } from 'vue'
import OverlayMask from '../components/OverlayMask.vue'
import Topbar from '../components/Topbar.vue'
import Sidebar from '../components/Sidebar.vue'
import { useResponsiveSidebar } from '../composables/useResponsiveSidebar'

const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()

const groupedMembers = ref({ 'Team SII 现队友': [], 'Team SII 前队友': [], '新生公演 前队友': [] })
const expandedGroups = ref({ 'Team SII 现队友': false, 'Team SII 前队友': false, '新生公演 前队友': false })
// const maxInitial = 3

// const toggleExpanded = group => {
//   expandedGroups.value[group] = !expandedGroups.value[group]
// }

onMounted(async () => {
  try {
    const res = await fetch('http://113.44.8.72:5000/api/teammates')
    const data = await res.json()
    const temp = { 'Team SII 现队友': [], 'Team SII 前队友': [], '新生公演 前队友': [] }

    data.forEach(item => {
      const isSII = item.is_teamsii
      const isNew = item.is_teamnew
      const isActive = item.is_active

      if (isSII && isActive) {
        temp['Team SII 现队友'].push(item)
      } else if (isSII && !isActive) {
        temp['Team SII 前队友'].push(item)
      } else if (isNew && !isSII) {
        temp['新生公演 前队友'].push(item)
      }
    })

    // for (const key in temp) {
    //   temp[key].sort((a, b) => parseInt(b.session) - parseInt(a.session))
    // }

    groupedMembers.value = temp
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
        'd-flex',
        'flex-column',
        'align-items-center',
        'bg-white',
        'text-center',
        !isMobile ? 'main-scrollable' : ''
      ]"
      :style="{
        flex: 1,
        minWidth: 0,
        paddingTop: isMobile ? '76px' : '16px'
      }"
    >
      <div class="mt-5 w-75">
        <h2 class="mb-3">Team SII 现队友</h2>
        <p>周童玥在Team SII的队友，包括正式成员、兼任成员和已分配到Team SII的预备生。</p>
        <p class="text-muted">
          {{ groupedMembers['Team SII 现队友']
            .map(m => m.note ? `${m.name}（${m.note}）` : m.name)
            .join('、') || '暂无成员' }}
        </p>
      </div>

      <div class="mt-5 w-75">
        <h2 class="mb-3">Team SII 前队友</h2>
        <p>周童玥在Team SII的前队友，包括已毕业或退团的正式成员，和已解除兼任的兼任成员。</p>
        <p class="text-muted">
          {{ groupedMembers['Team SII 前队友']
            .map(m => m.note ? `${m.name}（${m.note}）` : m.name)
            .join('、') || '暂无成员' }}
        </p>
      </div>

      <div class="mt-5 mb-5 w-75">
        <h2 class="mb-3">新生公演 前队友</h2>
        <p>周童玥曾经在新生公演（《命运的X号》、《代号XII 2.0》）时期的队友，不包括Team SII的成员。</p>
        <p class="text-muted">
          {{ groupedMembers['新生公演 前队友']
            .map(m => m.note ? `${m.name}（${m.note}）` : m.name)
            .join('、') || '暂无成员' }}
        </p>
      </div>
    </main>
  </div>
</template>