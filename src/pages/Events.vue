<script setup>
import { ref, onMounted, computed } from 'vue'
import OverlayMask from '@/components/OverlayMask.vue'
import Topbar from '@/components/Topbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import Notification from '@/components/Notification.vue'
import { useApi } from '@/composables/fetch'
import { useResponsiveSidebar } from '@/composables/useResponsiveSidebar'

const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()

const timelineItems = ref([])

// ===== 年份筛选（只要这几个）=====
const yearOptions = ['all', '2025', '2024', '2023']
const activeYear = ref('all')

const getYear = (rawDate) => (rawDate && rawDate.length >= 4 ? rawDate.slice(0, 4) : '未知')

// 根据 activeYear 过滤：all 就返回全部
const filteredTimelineItems = computed(() => {
  if (activeYear.value === 'all') return timelineItems.value
  return timelineItems.value.filter(it => getYear(it.rawDate) === activeYear.value)
})

// 转换日期格式
const formatCNDateFromYYYYMMDD = (dateStr) => {
  if (!dateStr || dateStr.length !== 8) return ''

  const y = dateStr.slice(0, 4)
  const m = parseInt(dateStr.slice(4, 6), 10)
  const d = parseInt(dateStr.slice(6, 8), 10)

  return `${y}年${m}月${d}日`
}

// 调用api
const { apiFetch } = useApi()

const loadEvents = async () => {
  try {
    const { ok, data } = await apiFetch('/events')
    if (!ok) {
      alert('❌ 活动数据加载失败')
      return
    }

    // ====== 后端 events → 时间线格式 ======
    timelineItems.value = data
      .filter(item => item.is_imp === true)  // 只保留重要事件
      .map(item => ({
        id: item.id,
        rawDate: item.date,  // ⭐ 保留原始 YYYYMMDD
        date: formatCNDateFromYYYYMMDD(item.date),
        title: item.title,
        img: `/${item.img}`,   // 图片需在 public/
        tag: 'SNH48',
        detail: item.detail
      }))
      .sort((a, b) => a.rawDate.localeCompare(b.rawDate))
  } catch (e) {
    console.error('加载失败', e)
  }
}

onMounted(() => {
  loadEvents()
})

const normalizeDetail = (text) => {
  if (!text) return ''
  // 把字面量 \n / \r\n 变成真实换行
  return text.replace(/\\r\\n/g, '\n').replace(/\\n/g, '\n')
}
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
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >
      <Notification />

      <h2 class="timeline-title">周童玥偶像运动会射箭项目录像</h2>
      <div class="video-wrapper">
        <iframe
          src="https://player.bilibili.com/player.html?isOutside=true&aid=115672679977274&bvid=BV1g52XB2E9k&cid=34550255530&p=1"
          scrolling="no"
          frameborder="0"
          allowfullscreen
        ></iframe>
      </div>

      <section class="timeline-section">
        <h2 class="timeline-title">大事年表</h2>
        <p class="text-center">
          除特别注明外，所有图片均来自SNH48公演直播截图，或由SNH48官方微博发布。
        </p>

        <!-- 年份筛选条：全部 / 2025 / 2024 / 2023 -->
        <div class="year-filter">
          <button
            v-for="y in yearOptions"
            :key="y"
            type="button"
            class="year-btn"
            :class="{ active: activeYear === y }"
            @click="activeYear = y"
          >
            {{ y === 'all' ? '全部' : y }}
          </button>
        </div>

        <div class="timeline">
          <div
            v-for="(it, idx) in filteredTimelineItems"
            :key="it.id ?? (it.rawDate + '_' + idx)"
            class="timeline-row"
            :class="{ reverse: idx % 2 === 1 }"
          >
            <!-- 左侧（或右侧）图片卡 -->
            <div class="timeline-media">
              <div class="photo-card">
                <img :src="it.img" :alt="it.title" />
                <!-- <div v-if="it.tag" class="corner-tag">{{ it.tag }}</div> -->
              </div>
            </div>

            <!-- 中轴线与圆点 -->
            <div class="timeline-axis">
              <span class="axis-dot"></span>
            </div>

            <!-- 右侧（或左侧）信息条 -->
            <div class="timeline-info">
              <div class="info-bar">
                <div class="info-date">{{ it.date }}</div>
                <div class="info-sub">{{ it.title }}</div>
                <div class="info-detail">{{ normalizeDetail(it.detail) }}</div>
              </div>
            </div>
          </div>

          <!-- 可选：当前筛选无数据时给个提示 -->
          <div v-if="filteredTimelineItems.length === 0" class="empty-tip">
            正在加载…
          </div>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.video-wrapper {
  width: 100%;
  max-width: 960px;   /* 可选：限制最大宽度 */
  margin: 0 auto;     /* 居中 */
  aspect-ratio: 16 / 9;
}

.video-wrapper iframe {
  width: 100%;
  height: 100%;
  border: none;
}

.timeline-section {
  width: 100%;
  max-width: 1000px;
  margin: 28px auto 40px;
  text-align: left;
}

.timeline-title {
  font-size: 30px;
  font-weight: 700;
  margin: 6px 0 18px;
  text-align: center;
}

/* ===== 年份筛选条 ===== */
.year-filter {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin: 8px 0 16px;
  justify-content: center;
}

.year-btn {
  border: 1px solid #eee;
  background: #fff;
  padding: 8px 14px;
  border-radius: 999px;
  cursor: pointer;
  font-weight: 700;
  color: #444;
}

.year-btn.active {
  border-color: #f2b705;
  background: rgba(242, 183, 5, 0.12);
  color: #111;
}

.empty-tip {
  margin: 18px 0 6px;
  text-align: center;
  color: #888;
  font-size: 14px;
}

/* 容器 */
.timeline {
  position: relative;
  padding: 8px 0;
}

/* 一行：三列（媒体 / 中轴 / 信息） */
.timeline-row {
  display: grid;
  grid-template-columns: 1fr 56px 1fr;
  align-items: center;
  gap: 16px;
  padding: 18px 0;
}

/* 奇偶反转：让内容左右交错 */
.timeline-row.reverse .timeline-media {
  order: 3;
}
.timeline-row.reverse .timeline-info {
  order: 1;
}
.timeline-row.reverse .timeline-axis {
  order: 2;
}

/* ====== 中轴线 ====== */
.timeline-axis {
  position: relative;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.timeline-axis::before {
  content: "";
  position: absolute;
  top: -18px;
  bottom: -18px;
  width: 2px;
  background: #e5e5e5;
  left: 50%;
  transform: translateX(-50%);
}

.axis-dot {
  width: 14px;
  height: 14px;
  border-radius: 999px;
  background: white;
  border: 3px solid #f2b705;
  box-shadow: 0 0 0 4px rgba(240, 90, 119, 0.12);
  /* margin-top: 6px; */
  z-index: 2;
}

/* ====== 图片卡（模仿截图：圆角+描边） ====== */
.photo-card {
  position: relative;
  border-radius: 18px;
  overflow: hidden;
  border: 3px solid #f2b705;
  background: #111;
  max-width: 640px;
  width: 100%;
}

.photo-card img {
  width: 100%;
  height: auto;
  display: block;
}

/* 右上角斜角标（BEJ48） */
.corner-tag {
  position: absolute;
  top: 10px;
  right: -34px;
  transform: rotate(45deg);
  background: #f2b705;
  color: #fff;
  font-weight: 700;
  font-size: 12px;
  padding: 6px 40px;
  letter-spacing: 1px;
}

/* ====== 信息条（粉色渐变 + 左侧红色竖条/横线） ====== */
.timeline-info {
  display: flex;
  justify-content: flex-start;
}

.timeline-row.reverse .timeline-info {
  justify-content: flex-end;
}

.info-bar {
  width: min(640px, 100%);
  background: linear-gradient(
    180deg,
    rgba(242, 183, 5, 0.18),
    rgba(242, 183, 5, 0.08)
  );
  border-left: 6px solid #f2b705;
  padding: 14px 18px;
  border-radius: 10px;
}

.timeline-row.reverse .info-bar {
  border-left: none;
  border-right: 6px solid #f2b705;
}

.info-date {
  font-size: 20px;
  font-weight: 800;
  color: #f2b705; /* 主体黄色 */
  padding-bottom: 10px;
  border-bottom: 2px solid rgba(242, 183, 5, 0.45);
  margin-bottom: 10px;
}

.info-sub {
  font-size: 18px;
  color: #555;
  letter-spacing: 0.5px;
  font-weight: 600;
}

.info-detail {
  padding-top: 8px;
  font-size: 12px;
  color: #555;
  letter-spacing: 0.5px;
  white-space: pre-line;
}

/* ====== 移动端：改为上下堆叠（更好看） ====== */
@media (max-width: 768px) {
  .timeline-row {
    grid-template-columns: 1fr;
    gap: 10px;
  }

  .timeline-axis {
    display: none;
  }

  .timeline-row.reverse .timeline-media,
  .timeline-row.reverse .timeline-info {
    order: initial;
  }

  .timeline-info,
  .timeline-row.reverse .timeline-info {
    justify-content: flex-start;
  }

  .info-bar,
  .timeline-row.reverse .info-bar {
    border-right: none;
    border-left: 6px solid #f2b705;
  }
}
</style>
