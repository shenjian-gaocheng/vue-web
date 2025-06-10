<template>
  <div class="d-flex flex-column align-items-center bg-dark text-white p-4 vh-100" style="width: 260px;">
    <img class="rounded-circle border border-white mb-4" src="https://www.snh48.com/images/member/zp_10290.jpg" alt="小周头像" style="width: 130px; height: 130px; object-fit: cover;" />
    <nav class="nav nav-pills flex-column text-center w-100">
      <router-link to="/" class="nav-link text-white" active-class="active">主页</router-link>
      <router-link to="/weibo" class="nav-link text-white" active-class="active">微博</router-link>
      <router-link to="/baike" class="nav-link text-white" active-class="active">小周百科</router-link>
      <router-link to="/stages" class="nav-link text-white" active-class="active">参加公演列表</router-link>
      <router-link to="/fun" class="nav-link text-white" active-class="active">趣事集锦</router-link>
      <router-link to="/relation" class="nav-link text-white" active-class="active">团内人物关系</router-link>
      <router-link to="/events" class="nav-link text-white" active-class="active">团内大事件</router-link>
    </nav>
  </div>
</template>
