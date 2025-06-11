import { ref, onMounted, onUnmounted, watchEffect } from 'vue'

export function useResponsiveSidebar() {
  const isMobile = ref(window.innerWidth < 768)
  const isSidebarCollapsed = ref(window.innerWidth < 768) // 初始化根据窗口宽度决定
  const isManuallyToggled = ref(false)

  const handleResize = () => {
    isMobile.value = window.innerWidth < 768
  }

  onMounted(() => {
    window.addEventListener('resize', handleResize)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
  })

  // 如果用户没有手动控制过，则根据 isMobile 自动设置折叠状态
  watchEffect(() => {
    if (!isManuallyToggled.value) {
      isSidebarCollapsed.value = isMobile.value
    }
  })

  // 返回方法让组件能手动控制状态
  const toggleSidebar = () => {
    isSidebarCollapsed.value = !isSidebarCollapsed.value
    isManuallyToggled.value = true
  }

  return {
    isMobile,
    isSidebarCollapsed,
    toggleSidebar
  }
}