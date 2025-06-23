<template>
  <span>{{ formatted }}</span>
</template>

<script setup>
import { computed } from 'vue'
import dayjs from 'dayjs'
import utc from 'dayjs/plugin/utc'
import timezone from 'dayjs/plugin/timezone'

// 初始化插件
dayjs.extend(utc)
dayjs.extend(timezone)

// 处理时间格式，根据当前设备自动转换时区
const props = defineProps({
  datetime: String,
  fromZone: {
    type: String,
    default: 'Asia/Shanghai'
  },
  toZone: {
    type: String,
    default: Intl.DateTimeFormat().resolvedOptions().timeZone
  },
  format: {
    type: String,
    default: 'YYYY-MM-DD HH:mm:ss'
  }
})

// 使用 props.xxx
const formatted = computed(() => {
  try {
    return props.datetime
      ? dayjs(props.datetime).tz(props.zone).format(props.format)
      : '无效时间'
  } catch (e) {
    console.warn('时间格式化出错', e)
    return '格式错误'
  }
})
</script>