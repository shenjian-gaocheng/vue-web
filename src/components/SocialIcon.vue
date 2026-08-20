<script setup>
import { computed } from 'vue'
import xhsIcon from '@/assets/xhs.svg'

const props = defineProps({
  className: {
    type: String,
    default: '',
  },
})

const normalizedClass = computed(() => String(props.className || '').toLowerCase())

const isXhs = computed(() => normalizedClass.value.includes('xhs'))

const iconClass = computed(() => {
  if (normalizedClass.value.includes('weibo')) return 'fab fa-weibo'
  if (normalizedClass.value.includes('douyin')) return 'fab fa-tiktok'
  if (normalizedClass.value.includes('bilibili')) return 'fab fa-bilibili'
  return 'fas fa-link'
})

const platformClass = computed(() => {
  if (normalizedClass.value.includes('weibo')) return 'social-icon-weibo'
  if (normalizedClass.value.includes('douyin')) return 'social-icon-douyin'
  if (normalizedClass.value.includes('bilibili')) return 'social-icon-bilibili'
  if (normalizedClass.value.includes('xhs')) return 'social-icon-xhs'
  return 'social-icon-default'
})
</script>

<template>
  <img
    v-if="isXhs"
    :src="xhsIcon"
    alt="小红书"
    :class="['social-icon', 'social-icon-image', platformClass]"
  />
  <i
    v-else
    :class="[iconClass, 'social-icon', 'social-icon-font', platformClass]"
    aria-hidden="true"
  ></i>
</template>

<style scoped>
.social-icon {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
  vertical-align: middle;
}

.social-icon-image {
  width: 0.95em;
  height: 0.95em;
  display: block;
  object-fit: contain;
}

.social-icon-font {
  transform: translateY(0.06em);
}

.social-icon-weibo {
  color: #e11d48;
}

.social-icon-douyin {
  color: #111827;
}

.social-icon-bilibili {
  color: #2563eb;
}

.social-icon-default {
  color: #64748b;
}
</style>