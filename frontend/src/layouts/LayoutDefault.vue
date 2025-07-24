<!-- 响应式导航栏 顶部导航/侧边栏导航 -->
<!-- 正文 -->
<!-- 脚注 -->

<template>
  <div class="layout-default">
    <!-- 两个导航同时挂载，CSS 控制显隐 -->
    <NavbarTop    class="nav-desktop" />
    <NavbarMobile class="nav-mobile"  />

    <main class="main-content">
        <slot />
    </main>

    <Footer />
  </div>
</template>

<script setup>
import NavbarTop from '@/components/navigation/NavbarTop.vue'
import NavbarMobile from '@/components/navigation/NavbarMobile.vue'
import Footer from '@/components/Footer.vue'
</script>

<style scoped>
.layout-default {
  width: 100%;
  min-height: 100vh;
  overflow-x: hidden;
}
.main-content {
  box-sizing: border-box;
  height: auto;
  flex: none;
}


/* —— 响应式导航切换 —— */
.nav-desktop { display: none; }
.nav-mobile  { display: block; }

@media (min-width: 769px) {
  .nav-desktop { display: flex; }
  .nav-mobile  { display: none;  }
}

</style>
