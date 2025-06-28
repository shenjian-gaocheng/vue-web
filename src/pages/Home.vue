<script setup>
import OverlayMask from '@/components/OverlayMask.vue'
import Topbar from '@/components/Topbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import Notification from '@/components/Notification.vue'
import { useResponsiveSidebar } from '@/composables/useResponsiveSidebar'

const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()
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

    <!-- 主内容 -->
    <main
      class="flex-fill d-flex flex-column bg-white px-4"
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >
      <!-- 放在顶部 -->
      <Notification />

      <!-- 主体内容，撑满空间并居中 -->
      <div class="flex-grow-1 d-flex justify-content-center align-items-center text-center">
        <div>
          <h1 :class="['art-text', isMobile ? 'art-text-mobile' : 'art-text-pc']">
            周童玥应援站
          </h1>
          <p class="code">（内测中）</p>
          <p class="code">“这是新月，这是满月，这是——周童玥！”</p>
          <p class="code">神秘代码：158139179</p>
        </div>
      </div>
    </main>
  </div>
</template>