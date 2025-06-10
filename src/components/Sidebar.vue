<script setup>
import { ref, watchEffect } from 'vue'

const props = defineProps({
  isMobile: Boolean
})
const emit = defineEmits(['update:collapsed'])

const year = new Date().getFullYear()
const collapsed = ref(false)

// 自动折叠（移动端）
watchEffect(() => {
  if (props.isMobile) collapsed.value = true
})

// 每次变化就 emit
watchEffect(() => {
  emit('update:collapsed', collapsed.value)
})

</script>

<template>
  <div
    class="sidebar-menu bg-dark text-white p-3"
    :class="[
      props.isMobile
        ? (collapsed ? 'position-static' : 'position-absolute top-0 start-0 z-3 w-100')
        : 'vh-100 d-flex flex-column'
    ]"
    :style="{
      width: !props.isMobile ? (collapsed ? '100px' : '280px') : '100%',
      height: props.isMobile
        ? (collapsed ? '60px' : 'auto')  // 未展开：固定高度；展开：自动撑内容
        : (collapsed ? '100vh' : '100vh'),  // 桌面端不变
      transition: 'all 0.3s ease'
    }"
  >
    <!-- 折叠按钮 -->
    <button
      class="btn btn-sm btn-secondary"
      :class="[
        props.isMobile
          ? 'd-flex justify-content-start align-items-start px-1 py-0'
          : 'align-self-end mb-3'
      ]"
      @click="collapsed = !collapsed"
    >
      <span class="fs-6">{{ collapsed ? '▶️' : '◀️' }}</span>
    </button>

    <!-- 头像 -->
    <img
      v-if="!collapsed && !props.isMobile"
      class="rounded-circle border border-warning mb-4 mx-auto"
      src="https://www.snh48.com/images/member/zp_10290.jpg"
      alt="小周头像"
      style="width: 130px; height: 130px; object-fit: cover;"
    />

    <!-- 菜单 -->
    <nav
      class="nav nav-pills mb-auto"
      :class="props.isMobile ? 'flex-column text-start w-100' : 'flex-column text-center w-100'"
    >
      <router-link
        v-for="(label, path) in {
          '/': '主页',
          '/weibo': '微博',
          '/baike': '小周百科',
          '/stages': '参加公演列表',
          '/fun': '趣事集锦',
          '/relation': '团内人物关系',
          '/events': '团内大事件'
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
    <div class="text-center text-white mt-4 small" v-if="!collapsed && !props.isMobile">
      &copy; {{ year }} 周童玥应援会<br>部分来源：SNH48.com<br>神秘代码：158139179
    </div>
  </div>
</template>