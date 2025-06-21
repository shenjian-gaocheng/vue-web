<script setup>
import OverlayMask from '@/components/OverlayMask.vue'
import Topbar from '@/components/Topbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import { useResponsiveSidebar } from '@/composables/useResponsiveSidebar'

const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()

import { ref } from 'vue'
import Modal from '@/components/Modal.vue'

const showModal = ref(false)

const doConfirm = () => {
  alert('你点击了确认')
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
      <!-- <div>
      </div> -->
      <button @click="showModal = true">打开弹窗</button>

      <Modal v-model="showModal" title="确认操作" @confirm="doConfirm">
        <p>你确定要继续操作吗？</p>
      </Modal>
    </main>
  </div>
</template>