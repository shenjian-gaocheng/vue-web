<script setup>
import OverlayMask from '../components/OverlayMask.vue'
import Topbar from '../components/Topbar.vue'
import Sidebar from '../components/Sidebar.vue'
import { useResponsiveSidebar } from '../composables/useResponsiveSidebar'

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
      class="flex-fill d-flex justify-content-center align-items-center bg-white text-center"
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >

      <div>
        <h1 class="art-text">周童玥</h1>
        <p class="code">神秘代码：158139179</p>
      </div>
    </main>
  </div>
</template>