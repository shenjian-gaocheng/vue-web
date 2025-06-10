<!-- components/Sidebar.vue -->
<template>
  <div class="sidebar">
    <img class="avatar" src="/avatar.jpg" alt="小周头像" />
    <nav class="nav">
      <router-link to="/weibo" class="hover:underline">微博</router-link>
      <router-link to="/baike">小周百科</router-link>
      <router-link to="/stages">参加公演列表</router-link>
      <router-link to="/fun">趣事集锦</router-link>
      <router-link to="/relation">团内人物关系</router-link>
      <router-link to="/events">团内大事件</router-link>
    </nav>
  </div>
</template>

<style scoped>
.sidebar {
  width: 260px;
  background-color: #a4552c;
  color: white;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 40px 20px;
}

.avatar {
  width: 130px;
  height: 130px;
  border-radius: 50%;
  border: 4px solid white;
  object-fit: cover;
  margin-bottom: 30px;
}

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
</style>