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
        'flex-fill',
        'd-flex',
        'flex-column',
        'bg-white',
        'text-center',
        'px-4',
        !isMobile ? 'main-scrollable' : ''
      ]"
      :style="{
        flex: 1,
        minWidth: 0,
        paddingTop: isMobile ? '76px' : '16px'
      }"
    >
      
      <Notification />

      <div style="max-width: 900px; margin: 0 auto; padding-left: 16px; padding-right: 16px;">
        <div class="mt-4 mx-auto">
          <h1>关于周童玥的满月泛舟记录厅</h1>
        </div>

        <div class="mt-5 mx-auto">
          <h2 class="mb-3">本站主题</h2>
          <!-- <p>周童玥应援站（zty0322.top）是SNH48-周童玥应援会建立的，以介绍、宣传周童玥为主的网站。</p> -->
          <p>周童玥的满月泛舟记录厅（zty0322.top）是由SNH48-周童玥的粉丝建立的，以介绍、宣传周童玥为主的网站。</p>
          <p>包括了介绍周童玥的百科、社交平台链接、以及所有周童玥参加过的公演及团内活动的列表。</p>
        </div>

        <div class="mt-5 mx-auto">
          <h2 class="mb-3">本站声明</h2>
          <p>本站为周童玥的粉丝建立并管理，非周童玥个人官方网站。</p>
          <p>本站仅提供周童玥相关的信息，不提供任何站内互动渠道。</p>
          <p>若对本站有任何意见或建议，请加入神秘代码：158139179。</p>
          <p>若要与周童玥互动，请前往口袋48app，在周童玥的口袋房间和她互动。</p>
        </div>
      </div>
    </main>
  </div>
</template>