<script setup>
import { ref } from 'vue'

const year = new Date().getFullYear()
const collapsed = ref(false)
</script>

<template>
  <div
    class="d-flex flex-column bg-dark text-white p-3 vh-100"
    :style="{ width: collapsed ? '80px' : '260px', transition: 'width 0.3s' }"
  >
    <!-- 折叠/展开按钮 -->
    <button class="btn btn-sm btn-secondary mb-3 align-self-end" @click="collapsed = !collapsed">
      {{ collapsed ? '▶️' : '◀️' }}
    </button>

    <!-- 头像 -->
    <img
      v-if="!collapsed"
      class="rounded-circle border border-warning mb-4 mx-auto"
      src="https://www.snh48.com/images/member/zp_10290.jpg"
      alt="小周头像"
      style="width: 130px; height: 130px; object-fit: cover;"
    />

    <!-- 导航菜单 -->
    <nav class="nav nav-pills flex-column text-center w-100 mb-auto">
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
    <div class="text-center text-white mt-4 small" v-if="!collapsed">
      &copy; {{ year }} 周童玥应援会<br>部分来源：SNH48.com<br>神秘代码：158139179
    </div>
  </div>
</template>