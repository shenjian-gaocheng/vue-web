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
          <h1>周童玥的队友</h1>
        </div>

        <div class="mt-5 mx-auto">
          <h2 class="mb-3">Team SII 现队友</h2>
          <p>周童玥在Team SII的队友，包括正式成员、兼任成员和已分配到Team SII的预备生。</p>
          <p class="text-muted">
            曹可甜、陈雨孜、蒋夏羽、芦馨怡、刘诗彤（预备生）、刘增艳、柳雨呈、宁轲、沈小爱、盛乐、田姝丽、由淼、闫明筠、杨心渝、张雷雷、张倩、赵天杨、武博涵（Team X兼任）、李婷（预备生）、刘婧阳（预备生）
          </p>
        </div>

        <div class="mt-5 mx-auto">
          <h2 class="mb-3">Team SII 前队友</h2>
          <p>周童玥在Team SII的前队友，包括已毕业或退团的正式成员，和已解除兼任的兼任成员。</p>
          <p class="text-muted">
            李慧、马玉灵、邵雪聪、朱涵佳、黄恩茹、刘倩倩（原GNZ48 Team NIII兼任，GNZ48荣誉毕业生）、彭嘉敏、黄怡慈（原BEJ48 Team B兼任）、段艺璇（SNH48荣誉毕业生）
          </p>
        </div>

        <div class="mt-5 mb-5 mx-auto">
          <h2 class="mb-3">新生公演 前队友</h2>
          <p>周童玥曾经在新生公演（《命运的X号》、《代号XII 2.0》）时期的队友，不包括Team SII的成员。</p>
          <p class="text-muted">
            林佳怡、禹佳蔚、张月铭、王依柳、熊紫轶、刘小涵、卢晨昕、李虞龙若、温若其、许佳佳、尤可莹、张怡婷、梁怀方、唐程成、王悦垚、王紫澍、叶凡、张瀚引、陈真允一、罗颍宸、温冰冰、吴欣怡、夏奕欣、张曼妮、陈芷晴、潘力帼、陈俞希、金泓言、李妍、李子忻、杨秋野（原名孙莉）、肖彦竹
          </p>
        </div>

        <div class="mt-4 mx-auto">
          <h1>其他关系</h1>
        </div>

        <div class="mt-4 mb-5 mx-auto">
          <p>周童玥在SNH48 GROUP举办的其他所有活动中的队友。</p>
          <p class="text-muted">
            <strong>SNH48 GROUP《最佳拍档》第四季 周童玥的拍档：</strong>庄雅雯（前BEJ48 Team E成员）
          </p>
          <p class="text-muted">
            <strong>SNH48 GROUP《燃烧吧，团魂》第二季 “我说的都队”社团队友：</strong>刘增艳、叶凡（SNH48 Team NII成员）、张倩、唐程成（SNH48 Team NII成员）（周童玥担任该社团队长）
          </p>
        </div>
      </div>

      
    </main>
  </div>
</template>