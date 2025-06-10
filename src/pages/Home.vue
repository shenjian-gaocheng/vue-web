<script setup>
import { ref } from 'vue'

defineProps({
  msg: String,
})

const count = ref(0)
</script>

<template>
  <div class="container">
    <!-- 左侧栏 -->
    <div class="sidebar">
      <img class="avatar" src="/avatar.jpg" alt="小周头像" />
      <nav class="nav">
        <router-link to="/weibo" class="hover:underline">微博</router-link>
        <router-link to="/baike">小周百科</router-link>
        <router-link to="/fun">趣事集锦</router-link>
        <router-link to="/relation">团内人物关系</router-link>
        <router-link to="/events">团内大事件</router-link>
      </nav>
    </div>

    <!-- 右侧内容 -->
    <div class="main">
        <div class="main-content">
            <h1 class="art-text">周童玥</h1>
            <p class="code">神秘代码：158139179</p>
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

/* 左栏 */
.sidebar {
  width: 260px;
  background-color: #a4552c;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
}

/* 头像样式 */
.avatar {
  width: 130px;
  height: 130px;
  border-radius: 50%;
  border: 4px solid white;
  object-fit: cover;
  margin-bottom: 30px;
}

/* 导航菜单 */
.nav {
  display: flex;
  flex-direction: column;
  gap: 18px;
  font-size: 18px;
  text-align: center;
}

.nav a {
  color: white;
  text-decoration: none;
}

.nav a:hover {
  text-decoration: underline;
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