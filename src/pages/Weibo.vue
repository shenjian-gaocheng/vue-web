<template>
  <div class="weibo-page">
    <div class="glass-panel">
      <h1>微博跳转</h1>
      <div class="weibo-links">
        <a href="https://weibo.com/u/7861137548" target="_blank">小周微博主页</a>
        <a href="https://weibo.com/u/6660861957" target="_blank">应援站微博</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.weibo-page {
  background-image: url('/bg.jpg');
  background-size: cover;
  background-position: center;
  min-height: 100vh;
  display: flex;
  justify-content: flex-end; /* 靠右放置内容 */
  align-items: center;
  padding-right: 8vw; /* 右边留白 */
}

/* 玻璃卡片样式右移+柔化 */
.glass-panel {
  background: rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  -webkit-backdrop-filter: blur(10px);
  border-radius: 20px;
  padding: 32px 48px;
  text-align: center;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
  color: #222;
  max-width: 300px;
}

.glass-panel h1 {
  font-size: 28px;
  margin-bottom: 24px;
  font-weight: 700;
  color: #5a2e1a; /* 更适配背景的棕红色调 */
}

.weibo-links {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.weibo-links a {
  background-color: #ffffffcc; /* 半透明白底 */
  color: #5a2e1a;
  font-weight: 600;
  padding: 12px 20px;
  border-radius: 10px;
  text-decoration: none;
  transition: all 0.3s ease;
  border: 1px solid #5a2e1a;
}

.weibo-links a:hover {
  background-color: #5a2e1a;
  color: white;
  transform: translateX(4px);
}
</style>
