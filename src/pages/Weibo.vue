<script setup>
import OverlayMask from '@/components/OverlayMask.vue'
import Topbar from '@/components/Topbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import Notification from '@/components/Notification.vue'
import { useResponsiveSidebar } from '@/composables/useResponsiveSidebar'

const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()
</script>

<template>
  <div class="weibo-page layout-page d-flex">
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
      class="main-area d-flex flex-column justify-content-center align-items-end flex-grow-1 pe-5"
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >

      <div class="glass-panel">
        <h1>微博跳转</h1>
        <div class="weibo-links">
          <a href="https://weibo.com/u/7861137548" target="_blank">小周微博主页</a>
          <a href="https://weibo.com/u/6660861957" target="_blank">应援站微博</a>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.weibo-page {
  background-image: url('/bg.jpg');
  background-size: cover;
  background-position: center;
  width: 100vw;
  height: 100vh;
  display: flex;
}

/* 玻璃卡片样式右移+柔化 */
.glass-panel {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 32px 48px;
  text-align: center;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  color: #222;
  max-width: 300px;
}

.glass-panel h1 {
  font-size: 28px;
  margin-bottom: 24px;
  font-weight: 700;
  color: #5a2e1a; /* 更适配背景的棕红色调 */
}

.weibo-links {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.weibo-links a {
  background-color: #ffffffcc; /* 半透明白底 */
  color: #5a2e1a;
  font-weight: 600;
  padding: 12px 20px;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 1px solid #5a2e1a;
}

.weibo-links a:hover {
  background-color: #5a2e1a;
  color: white;
  transform: translateX(4px);
}
</style>
