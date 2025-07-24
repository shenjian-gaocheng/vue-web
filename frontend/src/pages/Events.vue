<script setup>
import LayoutDefault from '@/layouts/LayoutDefault.vue'
</script>

<template>
  <LayoutDefault>
    <div class="layout-page d-flex">
      <div
        :class="[
          'flex-fill',
          'd-flex',
          'flex-column',
          'bg-white',
          'text-center',
          'px-4',
          !isMobile ? 'main-scrollable' : ''
        ]"
        :style="{ paddingTop: isMobile ? '76px' : '16px' }"
      >


      </div>
    </div>
  </LayoutDefault>
</template>