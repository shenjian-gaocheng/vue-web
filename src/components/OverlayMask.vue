<!-- src/components/OverlayMask.vue -->
<script setup>
const emit = defineEmits(['click'])
</script>

<template>
  <div
    class="position-fixed top-0 start-0 w-100 h-100 bg-dark bg-opacity-50"
    style="z-index: 1045"
    @click="$emit('click')"
  />
</template>