<script setup>
import { ref, onMounted, onUnmounted } from 'vue'

const year = new Date().getFullYear()

const isLandscapeOnMobile = ref(false)

const updateOrientation = () => {
  isLandscapeOnMobile.value =
    // window.innerWidth < 768 && window.innerWidth > window.innerHeight
    window.innerHeight < 600
}

onMounted(() => {
  updateOrientation()
  window.addEventListener('resize', updateOrientation)
})

onUnmounted(() => {
  window.removeEventListener('resize', updateOrientation)
})

const props = defineProps({
  isMobile: Boolean,
  collapsed: Boolean
})
const emit = defineEmits(['update:collapsed'])

const toggle = () => {
  emit('update:collapsed', !props.collapsed)
}

</script>

<template>
  <div
    class="sidebar-menu bg-dark text-white p-3 d-flex flex-column"
    :class="props.isMobile ? 'position-fixed top-0 start-0 h-100' : 'vh-100'"
    :style="{
      zIndex: props.isMobile ? 9999 : 'auto',
      width: props.isMobile
        ? '280px'
        : (props.collapsed ? '100px' : '280px'),
      transform: props.isMobile
        ? (props.collapsed ? 'translateX(-100%)' : 'translateX(0)')
        : 'translateX(0)',
      transition: 'all 0.3s ease',
      height: '100vh'
    }"
  >

    <!-- 折叠按钮：仅桌面端显示 -->
    <button
      v-if="!props.isMobile"
      class="btn btn-sm btn-secondary align-self-end mb-3"
      @click="toggle"
    >
      <span class="fs-6">{{ props.collapsed ? '▶️' : '◀️' }}</span>
    </button>

    <!-- 头像 -->
    <img
      v-if="!collapsed && !isLandscapeOnMobile"
      class="rounded-circle border border-warning mb-4 mx-auto mt-4 mt-md-0"
      src="https://www.snh48.com/images/member/zp_10290.jpg"
      alt="小周头像"
      style="width: 130px; height: 130px; object-fit: cover;"
    />

    <!-- 菜单 -->
    <nav
      class="nav nav-pills flex-column flex-grow-1 w-100"
      :class="props.isMobile ? 'text-start' : 'text-center'"
    >
      <router-link
        v-for="(label, path) in {
          '/': '主页',
          '/weibo': '微博',
          '/baike': '小周百科',
          '/stages': '公演及活动列表',
          // '/fun': '趣事集锦',
          '/relation': '团内人物关系',
          '/about': '关于本站',
          // '/events': '团内大事件'
        }"
        :key="path"
        :to="path"
        class="nav-link"
        v-if="!collapsed || !props.isMobile"
        :class="{
          'bg-warning text-dark fw-bold': $route.path === path,
          'text-white': $route.path !== path
        }"
      >
        <span v-if="!collapsed">{{ label }}</span>
        <span v-else>•</span>
      </router-link>
    </nav>

    <!-- 底部版权 -->
    <div
      class="text-center text-white small mt-4"
      :class="props.isMobile ? 'pt-3' : ''"
      v-if="!collapsed"
    >
      <strong>周童玥的满月泛舟记录厅（内测中）</strong><br />
      &copy; {{ year }} zty0322.top<br />
      部分来源：SNH48.com<br />
      神秘代码：158139179
    </div>
  </div>
</template>