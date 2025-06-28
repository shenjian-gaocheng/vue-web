<script setup>
import OverlayMask from '@/components/OverlayMask.vue'
import Topbar from '@/components/Topbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import Notification from '@/components/Notification.vue'
import { useResponsiveSidebar } from '@/composables/useResponsiveSidebar'

const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()
</script>

<template>
  <div class="layout-page d-flex">
    <!-- 顶部栏：仅移动端显示 -->
    <Topbar
      v-if="isMobile"
      :collapsed="isSidebarCollapsed"
      @update:collapsed="isSidebarCollapsed = $event"
    />

    <!-- 遮罩：必须放在 Sidebar 后面、Main 前面 -->
    <OverlayMask
      v-if="isMobile && !isSidebarCollapsed"
      @click="isSidebarCollapsed = true"
    />

    <!-- 侧边栏 -->
    <Sidebar
      :is-mobile="isMobile"
      v-model:collapsed="isSidebarCollapsed"
    />

    <main 
      :class="[
        'position-relative',
        'flex-grow-1',
        'overflow-auto',
        'px-4',
        !isMobile ? 'main-scrollable' : ''
      ]"
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >

      <Notification />

      <!-- 姓名 & 简介 -->
      <div class="text-center mb-4 py-4 bg-light rounded col-md-10 mx-auto">
        <img src="/bg.jpg" alt="" class="mb-4" style="width: 100%; max-width: 600px; height: auto; display: block; margin: 0 auto;">
        <h1 class="fw-bold display-5 mb-1">周童玥</h1>
        <h3 class="text-warning fw-bold">Zhou TongYue</h3>
        <p class="text-muted">TEAM SII（SNH48 十八期生）</p>

        <!-- 社交链接 -->
        <div class="text-center">
          <a href="https://weibo.com/u/7861137548" class="mx-3" target="_blank">
            <i class="fab fa-weibo fa-2x text-danger"></i>
          </a>
          <a href="https://www.douyin.com/user/MS4wLjABAAAA85fHqEle3WCMj0JHlAVr2k5jq892OHh1u4193DL-Bk7-HOHksd_XQaF7oRteMNCE" class="mx-3" target="_blank">
            <i class="fab fa-tiktok fa-2x text-dark"></i>
          </a>
          <a href="https://space.bilibili.com/3537104390850991" class="mx-3" target="_blank">
            <i class="fab fa-bilibili fa-2x text-primary"></i>
          </a>
        </div>
      </div>

      <!-- 基本信息 -->
      <div class="row justify-content-center text-center mt-4 mb-4 g-4">
        <h2 class="mb-4 fw-bold">基本信息</h2>
        <div class="col-md-5">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <h5 class="card-title text-primary mb-3">个人信息</h5>
              <ul class="list-unstyled mb-0 text-start">
                <li><strong>昵称：</strong> 小周</li>
                <li><strong>生日：</strong> 03.22</li>
                <li><strong>星座：</strong> 白羊座</li>
                <li><strong>血型：</strong> -</li>
                <li><strong>身高：</strong> 165 cm</li>
                <li><strong>出生地：</strong> 中国 江苏</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-5">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <h5 class="card-title text-primary mb-3">成员信息</h5>
              <ul class="list-unstyled mb-0 text-start">
                <li><strong>加入时间：</strong> 2023-05-02</li>
                <li><strong>加入所属：</strong> SNH48 十八期生</li>
                <li><strong>升格时间：</strong> 2023-08-26</li>
                <li><strong>最终所属：</strong> SNH48 S队（TEAM SII）</li>
                <li><strong>所属公司：</strong> 上海丝芭文化传媒集团有限公司</li>
                <li><strong>Catch Phrase：</strong> 这是新月，这是满月，这是——【周童玥】！</li>
                <li><strong>应援色：</strong> 💛黄色</li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- 特长 & 兴趣爱好 -->
      <div class="row justify-content-center text-center mt-4 mb-4 g-4">
        <h2 class="mb-4 fw-bold">个人特长及兴趣爱好</h2>
        <div class="col-md-5">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <h5 class="card-title text-primary mb-3">个人特长</h5>
              <ul class="list-unstyled mb-0">
                <li><i class="fas fa-check text-success me-2"></i>琵琶</li>
                <li><i class="fas fa-check text-success me-2"></i>睡觉</li>
              </ul>
            </div>
          </div>
        </div>
        <div class="col-md-5">
          <div class="card shadow-sm h-100">
            <div class="card-body">
              <h5 class="card-title text-primary mb-3">兴趣爱好</h5>
              <ul class="list-unstyled mb-0">
                <ul class="list-unstyled">
                <li><i class="fas fa-heart text-pink me-2"></i>美女</li>
                <li><i class="fas fa-paw text-primary me-2"></i>猫猫狗狗</li>
              </ul>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- 奖项 -->
      <div class="row justify-content-center text-center mt-4 mb-4 g-4">
        <h2 class="mb-4 fw-bold">获奖</h2>
        <div class="text-center mb-4 py-4 bg-light rounded col-md-10 mx-auto">
          <h5 class="m-0 p-0">
            <i class="fas fa-trophy text-warning me-2"></i>2024 SNH48 GROUP 年度青春盛典 No.53
          </h5>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.card {
  border: none;
  background-color: #f8f9fa;
}
hr {
  border-top: 1px solid #dee2e6;
}
</style>