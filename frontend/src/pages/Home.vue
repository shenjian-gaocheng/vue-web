
<script setup>
import LayoutDefault from '@/layouts/LayoutDefault.vue'
import HomeCarousel from '@/components/home/HomeCarousel.vue'
import NewsCards from '@/components/home/NewsCards.vue';
</script>

<template>
  <LayoutDefault>
    <!-- 轮播图组件 -->
    <HomeCarousel />
    
    <section class="main-content">
      <h2>活动资讯</h2>
      <NewsCards />
    </section>
  </LayoutDefault>
</template>

<style scoped>
.main-content {
  padding: 4rem 2rem;
  background: white;
  text-align: center;
}

</style>