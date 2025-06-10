import { ref, onMounted, onUnmounted, watchEffect } from 'vue'

export function useResponsiveSidebar() {
  const isMobile = ref(window.innerWidth < 768)
  const isSidebarCollapsed = ref(true)

  const handleResize = () => {
    isMobile.value = window.innerWidth < 768
  }

  onMounted(() => {
    handleResize()
    window.addEventListener('resize', handleResize)
  })

  onUnmounted(() => {
    window.removeEventListener('resize', handleResize)
  })

  // 自动折叠 sidebar
  watchEffect(() => {
    if (isMobile.value) {
      isSidebarCollapsed.value = true
    }
  })

  return {
    isMobile,
    isSidebarCollapsed
  }
}