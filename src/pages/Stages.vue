<script setup>
import { ref } from 'vue'
import Sidebar from '../components/Sidebar.vue'

defineProps({
  msg: String,
})

const count = ref(0)
</script>

<template>
  <div class="container">
    <!-- 左侧栏 -->
    <Sidebar />


    <!-- 右侧内容 -->
    <div class="main">
        <div class="main-content">
            建设中
        </div>
    </div>
  </div>
</template>

<style>

html, body {
  margin: 0;
  padding: 0;
  height: 100%;
}

/* 外层左右布局 */
.container {
  display: flex;
  height: 100vh;
  font-family: sans-serif;
}

/* 右栏 */
.main {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  background-color: #fff;
}

.main-content {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
}

/* 艺术字：渐现 + 多彩变换 */
.art-text {
  font-size: 64px;
  font-weight: bold;
  font-family: 'Georgia', 'Times New Roman', serif;
  animation: fadeIn 2s ease-in-out forwards, rainbowColor 10s linear infinite;
  opacity: 0;
  background: linear-gradient(45deg, #a4552c, #d56aa0, #4472ca, #e6b422, #a4552c);
  background-size: 400% 400%;
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
/* 渐现效果 */
@keyframes fadeIn {
  to {
    opacity: 1;
  }
}

/* 多彩颜色渐变 */
@keyframes rainbowColor {
  0% {
    background-position: 0% 50%;
  }
  50% {
    background-position: 100% 50%;
  }
  100% {
    background-position: 0% 50%;
  }
}

/* 神秘代码文字 */
.code {
  font-size: 24px;
  font-weight: bold;
  color: #333;
  margin-top: 20px;
}
</style>