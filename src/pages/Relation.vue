<script setup>
import OverlayMask from '@/components/OverlayMask.vue'
import Topbar from '@/components/Topbar.vue'
import Sidebar from '@/components/Sidebar.vue'
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
        'd-flex',
        'flex-column',
        'align-items-center',
        'bg-white',
        'text-center',
        !isMobile ? 'main-scrollable' : ''
      ]"
      :style="{
        flex: 1,
        minWidth: 0,
        paddingTop: isMobile ? '76px' : '16px'
      }"
    >
      <div class="mt-5 w-75">
        <h2 class="mb-3">Team SII 现队友</h2>
        <p>周童玥在Team SII的队友，包括正式成员、兼任成员和已分配到Team SII的预备生。</p>
        <p class="text-muted">
          陈雨孜、段艺璇、黄怡慈（BEJ48 Team B 兼任）、芦馨怡、刘增艳、宁轲、彭嘉敏、沈小爱、田姝丽、由淼、闫明筠、杨心渝、张雷雷、张倩、赵天杨、冯雪（预备生）、蒋夏羽（预备生）、盛乐（预备生）
        </p>
      </div>

      <div class="mt-5 w-75">
        <h2 class="mb-3">Team SII 前队友</h2>
        <p>周童玥在Team SII的前队友，包括已毕业或退团的正式成员，和已解除兼任的兼任成员。</p>
        <p class="text-muted">
          黄恩茹、李慧、马玉灵、邵雪聪、朱涵佳、刘倩倩（GNZ48 Team NIII 兼任，GNZ48荣誉毕业生）
        </p>
      </div>

      <div class="mt-5 mb-5 w-75">
        <h2 class="mb-3">新生公演 前队友</h2>
        <p>周童玥曾经在新生公演（《命运的X号》、《代号XII 2.0》）时期的队友，不包括Team SII的成员。</p>
        <p class="text-muted">
          林佳怡、武博涵、禹佳蔚、张月铭、王依柳、熊紫轶、刘小涵、吕相宜、卢晨昕、李虞龙若、温若其、许佳佳、尤可莹、张怡婷、梁怀方、唐程成、王悦垚、王紫澍、叶凡、张瀚引、陈真允一、罗颍宸、温冰冰、吴欣怡、夏奕欣、张曼妮、陈芷晴、潘力帼、陈俞希、金泓言、李妍、李子忻、杨秋野（原名孙莉）、肖彦竹
        </p>
      </div>
    </main>
  </div>
</template>