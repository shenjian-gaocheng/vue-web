<script setup>
import Sidebar from '../components/Sidebar.vue'
import { useResponsiveSidebar } from '../composables/useResponsiveSidebar'

const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()
</script>

<template>
  <div :class="['layout-page', 'd-flex', isMobile ? 'flex-column' : 'flex-row']">
    <Sidebar ref="sidebarRef" :is-mobile="isMobile" v-model:collapsed="isSidebarCollapsed" />
    <main 
      class="flex-fill d-flex justify-content-center align-items-center bg-white text-center"
      :style="{
        paddingTop: !isMobile || isSidebarCollapsed ? '16px' : '76px'
      }"
    >
      <div>
      </div>
    </main>
  </div>
</template>