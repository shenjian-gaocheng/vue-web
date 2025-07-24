<!-- src/components/navigation/NavbarMobile.vue -->
<template>
  <header class="mobile-nav">
    <!-- 顶栏 -->
    <div class="navbar">
      

      <button
        class="hamburger"
        :aria-expanded="isOpen"
        aria-label="切换导航菜单"
        @click="toggle"
      >
        <span class="line" />
        <span class="line" />
        <span class="line" />
      </button>

      <RouterLink to="/" class="brand">周童玥应援会</RouterLink>
    </div>
  </header>

  <!-- 蒙层 + 抽屉 -->
  <transition name="fade">
    <div v-if="isOpen" class="overlay" @click.self="close">
      <transition name="drawer">
        <nav class="drawer" @click.stop>
          <RouterLink
            v-for="(label, path) in navItems"
            :key="path"
            :to="path"
            :class="{ active: route.path === path }"
            @click="close"
          >
            {{ label }}
          </RouterLink>
        </nav>
      </transition>
    </div>
  </transition>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, RouterLink } from 'vue-router'
import { navItems } from '@/components/navigation/navItems.js' 

const route  = useRoute()
const isOpen = ref(false)

const toggle = () => (isOpen.value = !isOpen.value)
const close  = () => (isOpen.value = false)

/* 路由变更后自动关闭抽屉 */
watch(() => route.fullPath, close)
</script>

<style scoped>
/* 顶栏 */
.mobile-nav {
  background:#000; color:#eee; width:100%;
}
.navbar{
  display:flex; justify-content:space-between; align-items:center;
  padding:0.75rem 1rem;
}
.brand{ color:#eee; text-decoration:none; font-weight:600; }

/* 汉堡按钮 */
.hamburger{
  display:flex; flex-direction:column; justify-content:space-between;
  width:24px; height:18px; padding:0; border:none; background:transparent; cursor:pointer;
}
.line{ width:100%; height:2px; background:#eee; }

/* ============ 抽屉 ============ */
.overlay{
  position:fixed; inset:0;            /* 全屏覆盖 */
  background:rgba(0,0,0,.45);         /* 半透明暗化 */
  z-index:999;                        /* 置于最上层 */
  overflow:hidden;                    /* 关闭滚动 */
  display:flex;                       /* 让抽屉可用 flex 占高 */
}
.drawer{
  width:260px; max-width:75%; height:100%;
  background:#111; color:#ddd;
  padding:1rem; box-sizing:border-box;
  display:flex; flex-direction:column; gap:1rem;
}
.drawer a{ color:#ddd; text-decoration:none; }
.drawer a.active, .drawer a:hover{ color:#fff; }

/* ============ 过渡动画 ============ */
.fade-enter-active, .fade-leave-active{
  transition: opacity .25s;
}
.fade-enter-from, .fade-leave-to{ opacity:0; }

.drawer-enter-active, .drawer-leave-active{
  transition: transform .25s ease;
}
.drawer-enter-from, .drawer-leave-to{
  transform: translateX(-100%);
}
</style>
