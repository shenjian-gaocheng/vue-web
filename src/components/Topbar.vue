<!-- src/components/Topbar.vue -->
<script setup>
const props = defineProps({
  collapsed: Boolean
})
const emit = defineEmits(['update:collapsed'])

const toggle = () => {
  emit('update:collapsed', !props.collapsed)
}
</script>

<template>
  <header
    class="position-fixed top-0 start-0 w-100 bg-warning text-black d-flex align-items-center px-3"
    style="height: 60px; z-index: 1040;"
  >
    <button class="btn btn-sm btn-dark me-3" @click="toggle">
      ☰
    </button>
    <span class="fw-bold">周童玥应援站</span>
  </header>
</template>