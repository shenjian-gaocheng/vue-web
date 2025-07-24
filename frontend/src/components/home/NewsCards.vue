<template>
  <div class="video-container">
    <div class="video-wrapper">
      <iframe 
        src="https://player.bilibili.com/player.html?bvid=BV1GS7AztEE5&autoplay=0" 
        frameborder="0"
        allowfullscreen
        allow="fullscreen"
      ></iframe>
    </div>
  </div>
</template>

<script setup>
// 空逻辑脚本区域
</script>

<style scoped>
.video-container {
  max-width: 960px;
  margin: 3rem auto;
  padding: 0 1rem;
}

.video-wrapper {
  position: relative;
  width: 100%;
  padding-bottom: 56.25%; /* 16:9 高宽比 */
  height: 0;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 0 10px rgba(0,0,0,0.1);
}

.video-wrapper iframe {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  border: none;
}
</style>
