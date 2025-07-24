<script setup>
import '@fortawesome/fontawesome-free/css/all.css'
</script>

<template>
  <footer class="footer">
    <div class="footer-container">
      <div class="footer-column">
        <p>周童玥应援会</p>
        <ul>
          <li><router-link to="/about">关于我们</router-link></li>
          <li><router-link to="/baike">关于周童玥</router-link></li>
          <li><router-link to="/faq">常见问题</router-link></li>
          <li><router-link to="/terms">条款及细则</router-link></li>
          <li><router-link to="/contact">联系我们</router-link></li>
        </ul>
      </div>

      <div class="footer-column">
        <p>周童玥社交账号</p>
        <ul class="social-icons">
          <a href="https://space.bilibili.com/3537104390850991?spm_id_from=333.337.0.0" target="_blank" rel="noopener">
            <img src="@/assets/icons/bilibili.svg" alt="Bilibili" class="custom-icon" />
          </a>
          <a href="https://weibo.com/u/7861137548" target="_blank" rel="noopener">
            <img src="@/assets/icons/weibo.svg" alt="Weibo" class="custom-icon" />
          </a>
          <a href="https://www.douyin.com/user/MS4wLjABAAAA85fHqEle3WCMj0JHlAVr2k5jq892OHh1u4193DL-Bk7-HOHksd_XQaF7oRteMNCE?from_tab_name=main" target="_blank" rel="noopener">
            <img src="@/assets/icons/douyin.svg" alt="Douyin" class="custom-icon" />
          </a>
        </ul>
        
      </div>
    </div>
  </footer>
</template>

<style scoped>
.footer {
  background-color: #000;
  color: #eee;
  padding: 2rem 1rem;
  text-align: left;
  font-family: sans-serif;
  width: 100%;
  position: relative;
}

.footer-container {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-around;
  flex-wrap: wrap;
  text-align: left;
  gap: 2rem;
}

.footer-column {
  flex: 1 1 180px;
}
.footer-column p {
  font-weight: bold;
  color: #fca5a5; /* 柔粉色 */
  margin-bottom: 1rem;
}
.footer-column ul {
  list-style: none;
  padding: 0;
  margin: 0;
}
.footer-column li {
  margin: 0.5rem 0;
}
.footer-column a {
  text-decoration: none;
  color: #ccc;
  transition: color 0.2s;
}
.footer-column a:hover {
  text-decoration: underline;
}

.social-icons {
  display: flex;
  gap: 1rem;
  margin-top: 0.4rem;
}

.social-icons i {
  font-size: 1.5rem;
  color: white;
}
.custom-icon {
  width: 24px;
  height: 24px;
  vertical-align: middle;
}
</style>
