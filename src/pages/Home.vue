<script setup>
import { computed, onMounted, ref } from 'vue'
import dayjs from 'dayjs'
import OverlayMask from '@/components/OverlayMask.vue'
import Topbar from '@/components/Topbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import Notification from '@/components/Notification.vue'
import { useResponsiveSidebar } from '@/composables/useResponsiveSidebar'
import { useApi } from '@/composables/fetch'

const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()
const { apiFetch } = useApi()

const stages = ref([])
const loadingStages = ref(false)
const stageError = ref('')
const selectedMonth = ref(dayjs().startOf('month'))
const selectedDateKey = ref(dayjs().format('YYYY-MM-DD'))
const minSelectableDate = dayjs('2023-05-02').startOf('day')
const minMonth = minSelectableDate.startOf('month')
const quickJumpOpen = ref(false)

const weekDays = ['日', '一', '二', '三', '四', '五', '六']

const categoryMeta = {
  'today-stage': { label: '公演', className: 'tag-today-stage' },
  'today-schedule': { label: '行程', className: 'tag-today-schedule' },
  'past-stage': { label: '公演', className: 'tag-past-stage' },
  'past-schedule': { label: '行程', className: 'tag-past-schedule' },
  'future-stage': { label: '公演', className: 'tag-future-stage' },
  'future-schedule': { label: '行程', className: 'tag-future-schedule' },
}

const socialLinks = [
  {
    name: '@SNH48-周童玥-',
    href: 'https://weibo.com/u/7861137548',
    description: '周童玥个人微博',
    className: 'social-weibo',
  },
  {
    name: '@周童玥∠( ᐛ 」∠)_',
    href: 'https://v.douyin.com/R0CZVXm5esU/',
    description: '短视频与日常更新',
    className: 'social-douyin',
  },
  {
    name: '@周童玥_zty',
    href: 'https://space.bilibili.com/3537104390850991',
    description: '视频与搬运内容',
    className: 'social-bilibili',
  },
  {
    name: '@SNH48-周童玥的满月泛周记录厅',
    href: 'https://weibo.com/u/6660861957',
    description: '关注最新应援动态',
    className: 'social-weibo',
  },
  {
    name: '@SNH48-周童玥的宇宙情书',
    href: 'https://space.bilibili.com/3546857020066246',
    description: '视频与搬运内容',
    className: 'social-bilibili',
  },
]

const today = computed(() => dayjs().startOf('day'))

const formatDateKey = (value) => dayjs(value).format('YYYY-MM-DD')

const normalizeDay = (value) => dayjs(value).startOf('day')

const stageBuckets = computed(() => {
  const buckets = {}

  stages.value.forEach((item) => {
    if (!item?.date || !dayjs(item.date).isValid()) {
      return
    }

    const key = formatDateKey(item.date)
    if (!buckets[key]) {
      buckets[key] = []
    }
    buckets[key].push(item)
  })

  return buckets
})

const monthLabel = computed(() => selectedMonth.value.format('YYYY年M月'))

const calendarCells = computed(() => {
  const firstDay = selectedMonth.value.startOf('month')
  const startOffset = firstDay.day()
  const gridStart = firstDay.subtract(startOffset, 'day')

  return Array.from({ length: 42 }, (_, index) => {
    const date = gridStart.add(index, 'day')
    const key = date.format('YYYY-MM-DD')
    const items = stageBuckets.value[key] ?? []

    return {
      key,
      date,
      day: date.date(),
      isCurrentMonth: date.isSame(selectedMonth.value, 'month'),
      isToday: date.isSame(dayjs(), 'day'),
      items,
      categories: Array.from(new Set(items.map((item) => getCategory(item, date))))
        .filter(Boolean),
    }
  })
})

const calendarRows = computed(() => {
  const rows = []
  for (let i = 0; i < calendarCells.value.length; i += 7) {
    rows.push(calendarCells.value.slice(i, i + 7))
  }
  return rows
})

const selectedDayItems = computed(() => stageBuckets.value[selectedDateKey.value] ?? [])

const selectedDayLabel = computed(() => dayjs(selectedDateKey.value).format('YYYY年M月D日'))
const canGoPrevMonth = computed(() => selectedMonth.value.isAfter(minMonth, 'month'))
const minDateKey = computed(() => minSelectableDate.format('YYYY-MM-DD'))

function getCategory(item, date) {
  const day = normalizeDay(date)
  const now = today.value

  if (day.isSame(now, 'day')) {
    return item.is_stage ? 'today-stage' : 'today-schedule'
  }

  if (day.isBefore(now, 'day')) {
    return item.is_stage ? 'past-stage' : 'past-schedule'
  }

  return item.is_stage ? 'future-stage' : 'future-schedule'
}

function getCellTypeMeta(items, date) {
  const day = normalizeDay(date)
  const now = today.value

  let timeKey = 'future'
  if (day.isSame(now, 'day')) {
    timeKey = 'today'
  } else if (day.isBefore(now, 'day')) {
    timeKey = 'past'
  }

  const hasStage = items.some((item) => item.is_stage)
  const hasSchedule = items.some((item) => !item.is_stage)

  if (hasStage && hasSchedule) {
    return { label: '均有', className: `day-type-mixed-${timeKey}` }
  }

  if (hasStage) {
    return { label: '公演', className: `tag-${timeKey}-stage` }
  }

  if (hasSchedule) {
    return { label: '行程', className: `tag-${timeKey}-schedule` }
  }

  return null
}

function selectDay(key) {
  selectedDateKey.value = key
}

function isSelectedRow(row) {
  return row.some((cell) => cell.key === selectedDateKey.value)
}

function getSocialIconClass(className) {
  if (className.includes('weibo')) return 'fab fa-weibo'
  if (className.includes('douyin')) return 'fab fa-tiktok'
  if (className.includes('bilibili')) return 'fab fa-bilibili'
  return 'fas fa-link'
}

function parseToDate(value) {
  if (!value) return null

  if (typeof value === 'number') {
    return new Date(value < 1e12 ? value * 1000 : value)
  }

  if (typeof value === 'string') {
    const d = new Date(value.trim().replace(' ', 'T'))
    return Number.isNaN(d.getTime()) ? null : d
  }

  if (value instanceof Date) return value

  return null
}

function formatLocalTime(dateLike) {
  const date = parseToDate(dateLike)
  if (!date) return '时间未知'

  return new Intl.DateTimeFormat(undefined, {
    hour: '2-digit',
    minute: '2-digit',
    hour12: false,
  }).format(date)
}

function formatItemType(type) {
  if (type === null || type === undefined || String(type).trim() === '') {
    return '未分类'
  }

  const normalized = String(type).trim()
  if (normalized === 'New Members') return '新生公演'
  if (normalized === '11') return '1&1'
  if (normalized === 'Others') return '其它/特殊'
  return normalized
}

function canShowLiveButton(startDateLike) {
  const start = parseToDate(startDateLike)
  if (!start) return false

  const showFrom = new Date(start.getTime() - 30 * 60 * 1000)
  return new Date() >= showFrom
}

function getLiveUrlByVenue(time) {
  if (!time || time === 'SNH') return 'https://live.bilibili.com/48'
  if (time === 'GNZ') return 'https://live.bilibili.com/391199'
  if (time === 'BEJ') return 'https://live.bilibili.com/383045'
  if (time === 'CKG') return 'https://live.bilibili.com/6015846'
  if (time === 'CGT') return 'https://live.bilibili.com/27848865'
  return ''
}

function getDatePhase(dateLike) {
  const target = parseToDate(dateLike)
  if (!target) return 'past'

  const t = new Date(target)
  t.setHours(0, 0, 0, 0)
  const n = new Date()
  n.setHours(0, 0, 0, 0)

  if (t.getTime() > n.getTime()) return 'future'
  if (t.getTime() < n.getTime()) return 'past'
  return 'today'
}

function shouldShowReplayButtons(item) {
  return getDatePhase(item.date) === 'past'
}

function shouldShowLiveButton(item) {
  const phase = getDatePhase(item.date)
  if (phase === 'future') return true
  if (phase === 'today') return true
  return false
}

function getLiveButtonState(item) {
  const phase = getDatePhase(item.date)

  if (phase === 'today' && item.is_stage) {
    return canShowLiveButton(item.date) && !!getLiveUrlByVenue(item.time) ? 'watch' : 'none'
  }

  if (phase === 'today' || phase === 'future') {
    return 'none'
  }

  return 'none'
}

function shiftMonth(offset) {
  const nextMonth = selectedMonth.value.add(offset, 'month').startOf('month')
  selectedMonth.value = nextMonth.isBefore(minMonth, 'month') ? minMonth : nextMonth
  selectedDateKey.value = selectedMonth.value.date(1).format('YYYY-MM-DD')
}

function applyQuickJumpDate(rawDate) {
  const parsed = dayjs(rawDate)
  if (!parsed.isValid()) return

  const minDate = minSelectableDate
  const normalized = parsed.startOf('day').isBefore(minDate, 'day') ? minDate : parsed.startOf('day')

  selectedMonth.value = normalized.startOf('month')
  selectedDateKey.value = normalized.format('YYYY-MM-DD')
  quickJumpOpen.value = false
}

function handleQuickJumpDateChange(event) {
  applyQuickJumpDate(event?.target?.value)
}

function goToToday() {
  selectedMonth.value = dayjs().startOf('month')
  selectedDateKey.value = dayjs().format('YYYY-MM-DD')
}

function loadStages() {
  loadingStages.value = true
  stageError.value = ''

  return apiFetch('/stages')
    .then(({ ok, data }) => {
      if (!ok) {
        stageError.value = data.message || '日历数据加载失败'
        stages.value = []
        return
      }

      stages.value = Array.isArray(data) ? data : []
    })
    .catch(() => {
      stageError.value = '日历数据加载失败，请稍后重试'
      stages.value = []
    })
    .finally(() => {
      loadingStages.value = false
    })
}

onMounted(() => {
  loadStages()
})
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

    <!-- 主内容 -->
    <main
      class="home-main flex-fill d-flex flex-column bg-white px-4"
      :style="{ paddingTop: isMobile ? '76px' : '16px' }"
    >
      <!-- 放在顶部 -->
      <Notification />

      <div class="home-content flex-grow-1">
        <section class="hero-panel text-center">
          <h1 :class="['art-text', isMobile ? 'art-text-mobile' : 'art-text-pc']">
            小星云之家
          </h1>
          <!-- <p class="code">（内测中）</p>
          <p class="code">“这是新月，这是满月，这是——周童玥！”</p>
          <p class="code">神秘代码：158139179</p> -->
        </section>

        <div class="home-body">
          <section class="calendar-panel">
            <div class="calendar-header">
              <div>
                <p class="calendar-kicker">Stage Calendar</p>
                <h2>周童玥公演与行程日历</h2>
              </div>

              <div class="calendar-actions">
                <button
                  type="button"
                  class="calendar-button ghost"
                  :disabled="!canGoPrevMonth"
                  @click="shiftMonth(-1)"
                >
                  上个月
                </button>
                <button type="button" class="calendar-button ghost" @click="goToToday">今天</button>
                <button type="button" class="calendar-button ghost" @click="shiftMonth(1)">下个月</button>
              </div>
            </div>

            <div class="calendar-toolbar">
              <div class="month-jump">
                <button
                  type="button"
                  class="month-pill month-pill-button"
                  @click="quickJumpOpen = !quickJumpOpen"
                >
                  {{ monthLabel }}
                </button>

                <div v-if="quickJumpOpen" class="month-jump-popover">
                  <label class="month-jump-label" for="quick-jump-date">快速切换日期</label>
                  <input
                    id="quick-jump-date"
                    type="date"
                    class="month-jump-input"
                    :min="minDateKey"
                    :value="selectedDateKey"
                    @change="handleQuickJumpDateChange"
                  />
                  <p class="month-jump-hint">最早可选：2023年5月2日</p>
                </div>
              </div>
              <div class="legend">
                <span class="legend-item"><i class="dot tag-today-stage"></i>今日公演</span>
                <span class="legend-item"><i class="dot tag-today-schedule"></i>今日行程</span>
                <span class="legend-item"><i class="dot tag-past-stage"></i>过去公演</span>
                <span class="legend-item"><i class="dot tag-past-schedule"></i>过去日程</span>
                <span class="legend-item"><i class="dot tag-future-stage"></i>将来公演</span>
                <span class="legend-item"><i class="dot tag-future-schedule"></i>将来行程</span>
              </div>
            </div>

            <div v-if="stageError" class="calendar-alert">
              {{ stageError }}
            </div>

            <div class="calendar-grid-wrap">
              <div class="weekday-row">
                <div v-for="weekday in weekDays" :key="weekday" class="weekday-cell">
                  {{ weekday }}
                </div>
              </div>

              <div class="calendar-grid">
                <template v-for="(row, rowIndex) in calendarRows" :key="`row-${rowIndex}`">
                  <button
                    v-for="cell in row"
                    :key="cell.key"
                    type="button"
                    class="day-cell"
                    :class="{
                      'is-current-month': cell.isCurrentMonth,
                      'is-today': cell.isToday,
                      'is-selected': cell.key === selectedDateKey,
                    }"
                    @click="selectDay(cell.key)"
                  >
                    <div class="day-top">
                      <span class="day-number">{{ cell.day }}</span>
                      <span
                        v-if="cell.items.length"
                        class="day-type-badge"
                        :class="getCellTypeMeta(cell.items, cell.date)?.className"
                      >
                        {{ getCellTypeMeta(cell.items, cell.date)?.label }}
                      </span>
                    </div>
                  </button>

                  <div v-if="isMobile && isSelectedRow(row)" class="mobile-selected-panel">
                    <div class="mobile-selected-head">
                      <span class="mobile-selected-title">{{ selectedDayLabel }}</span>
                      <span class="mobile-selected-count">{{ selectedDayItems.length }} 条</span>
                    </div>

                    <div v-if="loadingStages" class="mobile-selected-empty">正在加载...</div>
                    <div v-else-if="!selectedDayItems.length" class="mobile-selected-empty">当日暂无记录</div>
                    <div v-else class="mobile-selected-list">
                      <article
                        v-for="item in selectedDayItems"
                        :key="item.id ?? `${item.title}-${item.date}`"
                        class="mobile-selected-item"
                      >
                        <div class="mobile-selected-top">
                          <span class="mobile-selected-type" :class="categoryMeta[getCategory(item, item.date)]?.className">
                            {{ categoryMeta[getCategory(item, item.date)]?.label }}
                          </span>
                          <span class="mobile-selected-text">{{ `${item.title}（${formatLocalTime(item.date)}）` }}</span>
                        </div>

                        <div class="mobile-selected-actions">
                          <template v-if="shouldShowReplayButtons(item)">
                            <a
                              :href="item.url ? 'https://www.bilibili.com/video/' + item.url : null"
                              target="_blank"
                              class="btn btn-sm"
                              :class="item.url ? 'btn-primary' : 'btn-secondary disabled'"
                              :tabindex="!item.url ? -1 : null"
                              :aria-disabled="!item.url"
                            >
                              完整回放
                            </a>
                            <a
                              :href="item.cut_url ? 'https://www.bilibili.com/video/' + item.cut_url : null"
                              target="_blank"
                              class="btn btn-sm"
                              :class="item.cut_url ? 'btn-warning' : 'btn-secondary disabled'"
                              :tabindex="!item.cut_url ? -1 : null"
                              :aria-disabled="!item.cut_url"
                            >
                              小周cut
                            </a>
                          </template>

                          <template v-else-if="shouldShowLiveButton(item)">
                            <a
                              v-if="getLiveButtonState(item) === 'watch'"
                              :href="getLiveUrlByVenue(item.time)"
                              target="_blank"
                              class="btn btn-sm btn-success"
                            >
                              观看直播
                            </a>
                            <a v-else href="javascript:void(0)" class="btn btn-sm btn-success disabled">
                              暂无直播
                            </a>
                          </template>
                        </div>
                      </article>
                    </div>
                  </div>
                </template>
              </div>
            </div>
          </section>

          <aside class="social-panel">
            <section v-if="!isMobile" class="detail-panel">
              <div class="detail-header">
                <div>
                  <p class="detail-kicker">Selected Day</p>
                  <h3>{{ selectedDayLabel }}</h3>
                </div>
                <span class="detail-badge">{{ selectedDayItems.length }} 条记录</span>
              </div>

              <div v-if="loadingStages" class="detail-empty">正在加载日历数据...</div>
              <div v-else-if="!selectedDayItems.length" class="detail-empty">
                当日没有公演或者行程记录。
              </div>
              <div v-else class="detail-list" :class="{ 'two-items': selectedDayItems.length === 2 }">
                <article v-for="item in selectedDayItems" :key="item.id ?? `${item.title}-${item.date}`" class="detail-item">
                  <div class="detail-item-head">
                    <span
                      class="detail-type"
                      :class="categoryMeta[getCategory(item, item.date)]?.className"
                    >
                      {{ categoryMeta[getCategory(item, item.date)]?.label }}
                    </span>
                    <span v-if="String(item.session) !== '0'" class="detail-session">第{{ item.session }}场</span>
                  </div>
                  <h4>{{ item.title }}</h4>
                  <p class="detail-meta">
                    {{ formatItemType(item.type) }} · {{ formatLocalTime(item.date) }}
                  </p>

                  <div class="detail-actions">
                    <template v-if="shouldShowReplayButtons(item)">
                      <a
                        :href="item.url ? 'https://www.bilibili.com/video/' + item.url : null"
                        target="_blank"
                        class="btn btn-sm"
                        :class="item.url ? 'btn-primary' : 'btn-secondary disabled'"
                        :tabindex="!item.url ? -1 : null"
                        :aria-disabled="!item.url"
                      >
                        完整视频回放
                      </a>

                      <a
                        :href="item.cut_url ? 'https://www.bilibili.com/video/' + item.cut_url : null"
                        target="_blank"
                        class="btn btn-sm"
                        :class="item.cut_url ? 'btn-warning' : 'btn-secondary disabled'"
                        :tabindex="!item.cut_url ? -1 : null"
                        :aria-disabled="!item.cut_url"
                      >
                        小周cut视频
                      </a>
                    </template>

                    <template v-else-if="shouldShowLiveButton(item)">
                      <a
                        v-if="getLiveButtonState(item) === 'watch'"
                        :href="getLiveUrlByVenue(item.time)"
                        target="_blank"
                        class="btn btn-sm btn-success"
                      >
                        观看直播
                      </a>
                      <a v-else href="javascript:void(0)" class="btn btn-sm btn-success disabled">
                        暂无直播
                      </a>
                    </template>
                  </div>
                </article>
              </div>
            </section>

            <div class="social-panel-header">
              <p class="calendar-kicker">Social Links</p>
              <h2>社交平台</h2>
              <!-- <p class="social-intro">
                这里收集常用的官方与应援入口，方便直接跳转查看最新动态。
              </p> -->
            </div>

            <div class="social-list">
              <a
                v-for="link in socialLinks"
                :key="link.href"
                class="social-card"
                :class="link.className"
                :href="link.href"
                target="_blank"
                rel="noreferrer"
              >
                <span class="social-name-row">
                  <i :class="getSocialIconClass(link.className)"></i>
                  <span class="social-name">{{ link.name }}</span>
                </span>
                <!-- <span class="social-desc">{{ link.description }}</span> -->
                <span class="social-arrow">↗</span>
              </a>
            </div>
          </aside>
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.home-main {
  overflow: auto;
  background:
    radial-gradient(circle at top left, rgba(231, 245, 255, 0.92), transparent 34%),
    radial-gradient(circle at top right, rgba(255, 241, 215, 0.74), transparent 28%),
    linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
}

.home-content {
  display: flex;
  flex-direction: column;
  gap: 24px;
  padding-bottom: 32px;
}

.home-body {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 1fr);
  gap: 24px;
  align-items: start;
}

.hero-panel {
  padding: 28px 18px 12px;
}

.calendar-panel {
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 28px;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
  padding: 24px;
  backdrop-filter: blur(12px);
}

.social-panel {
  border: 1px solid rgba(15, 23, 42, 0.08);
  border-radius: 28px;
  background: linear-gradient(180deg, rgba(255, 255, 255, 0.96) 0%, rgba(248, 251, 255, 0.98) 100%);
  box-shadow: 0 24px 60px rgba(15, 23, 42, 0.08);
  padding: 24px;
  position: sticky;
  top: 16px;
}

.social-panel-header h2 {
  margin: 0;
  font-size: 24px;
  color: #0f172a;
}

.social-intro {
  margin: 12px 0 0;
  color: #64748b;
  line-height: 1.7;
}

.social-list {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 20px;
}

@media (min-width: 1101px) {
  .detail-header {
    margin-bottom: 10px;
  }

  .social-panel-header {
    margin-top: 24px;
  }

  .social-list .social-card:nth-child(3) {
    grid-column: 1;
  }

  .social-list .social-card:nth-child(4) {
    grid-column: 1;
  }
}

.social-card {
  position: relative;
  display: grid;
  gap: 6px;
  padding: 16px 18px;
  border-radius: 20px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  text-decoration: none;
  color: #0f172a;
  background: #fff;
  overflow: hidden;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
}

.social-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 18px 30px rgba(15, 23, 42, 0.1);
  border-color: rgba(15, 23, 42, 0.16);
}

.social-card::before {
  content: '';
  position: absolute;
  inset: 0 auto 0 0;
  width: 6px;
  background: #cbd5e1;
}

.social-card.social-weibo::before {
  background: linear-gradient(180deg, #ff7a45, #e11d48);
}

.social-card.social-weibo-alt::before {
  background: linear-gradient(180deg, #fb7185, #be123c);
}

.social-card.social-douyin::before {
  background: linear-gradient(180deg, #22c55e, #0ea5e9);
}

.social-card.social-bilibili::before {
  background: linear-gradient(180deg, #60a5fa, #2563eb);
}

.social-name {
  font-size: 17px;
  font-weight: 800;
  color: #0f172a;
}

.social-name-row {
  display: inline-flex;
  align-items: center;
  gap: 10px;
}

.social-card.social-weibo .social-name-row i,
.social-card.social-weibo-alt .social-name-row i {
  color: #e11d48;
}

.social-card.social-bilibili .social-name-row i {
  color: #2563eb;
}

.social-desc {
  color: #64748b;
  font-size: 13px;
}

.social-arrow {
  position: absolute;
  right: 16px;
  top: 16px;
  color: #94a3b8;
  font-size: 18px;
}

.calendar-header,
.detail-header,
.calendar-toolbar,
.day-top,
.detail-item-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.calendar-kicker,
.detail-kicker {
  margin: 0 0 6px;
  font-size: 12px;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  color: #64748b;
}

.calendar-header h2,
.detail-header h3 {
  margin: 0;
  font-size: 24px;
  color: #0f172a;
}

.calendar-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.calendar-button {
  border: 1px solid rgba(15, 23, 42, 0.12);
  border-radius: 999px;
  background: #ffffff;
  color: #0f172a;
  padding: 10px 16px;
  transition: all 0.2s ease;
}

.calendar-button:hover {
  border-color: rgba(15, 23, 42, 0.2);
  transform: translateY(-1px);
}

.calendar-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  transform: none;
}

.calendar-toolbar {
  flex-wrap: wrap;
  margin: 18px 0 14px;
}

.month-pill,
.detail-badge {
  border-radius: 999px;
  padding: 8px 14px;
  background: #0f172a;
  color: #fff;
  font-size: 13px;
}

.month-jump {
  position: relative;
}

.month-pill-button {
  border: none;
  cursor: pointer;
}

.month-jump-popover {
  position: absolute;
  left: 0;
  top: calc(100% + 8px);
  z-index: 10;
  min-width: 220px;
  padding: 10px;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  box-shadow: 0 12px 28px rgba(15, 23, 42, 0.12);
}

.month-jump-label {
  display: block;
  margin-bottom: 6px;
  font-size: 12px;
  color: #334155;
}

.month-jump-input {
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  padding: 6px 8px;
  font-size: 13px;
}

.month-jump-hint {
  margin: 6px 0 0;
  font-size: 11px;
  color: #64748b;
}

.legend {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 14px;
}

.legend-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #475569;
}

.dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
}

.calendar-alert {
  margin-bottom: 12px;
  padding: 12px 14px;
  border-radius: 16px;
  background: #fff7ed;
  color: #9a3412;
  border: 1px solid #fed7aa;
}

.calendar-layout {
  display: block;
}

.calendar-grid-wrap {
  min-width: 0;
}

.weekday-row,
.calendar-grid {
  display: grid;
  grid-template-columns: repeat(7, minmax(0, 1fr));
  gap: 8px;
}

.weekday-cell {
  text-align: center;
  color: #64748b;
  font-size: 13px;
  font-weight: 600;
  padding-bottom: 2px;
}

.day-cell {
  min-height: 70px;
  border: 1px solid #e2e8f0;
  border-radius: 14px;
  background: #fff;
  padding: 8px 8px;
  text-align: left;
  transition: transform 0.18s ease, box-shadow 0.18s ease, border-color 0.18s ease;
  overflow: hidden;
}

.day-cell:hover {
  transform: translateY(-2px);
  border-color: #cbd5e1;
  box-shadow: 0 14px 28px rgba(15, 23, 42, 0.08);
}

.day-cell.is-current-month {
  background: linear-gradient(180deg, #ffffff 0%, #fbfdff 100%);
}

.day-cell:not(.is-current-month) {
  opacity: 0.45;
}

.day-cell.is-today {
  border-color: #2563eb;
  box-shadow: 0 0 0 1px rgba(37, 99, 235, 0.12) inset;
}

.day-cell.is-selected {
  border-color: #0f172a;
  box-shadow: 0 0 0 2px rgba(15, 23, 42, 0.08) inset, 0 14px 30px rgba(15, 23, 42, 0.1);
}

.day-number {
  font-size: 15px;
  font-weight: 700;
  color: #0f172a;
}

.day-type-badge {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-height: 20px;
  border-radius: 999px;
  padding: 1px 6px;
  color: #fff;
  font-size: 11px;
  font-weight: 700;
}

.mobile-selected-panel {
  display: none;
  grid-column: 1 / -1;
  border: 1px solid rgba(15, 23, 42, 0.1);
  border-radius: 12px;
  background: #ffffff;
  padding: 8px;
}

.mobile-selected-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 8px;
  margin-bottom: 6px;
}

.mobile-selected-title {
  font-size: 0.875rem;
  font-weight: 700;
  color: #0f172a;
}

.mobile-selected-count {
  font-size: 0.875rem;
  color: #64748b;
}

.mobile-selected-list {
  display: flex;
  flex-direction: column;
  gap: 5px;
}

.mobile-selected-item {
  display: flex;
  flex-direction: column;
  align-items: stretch;
  gap: 6px;
  min-width: 0;
}

.mobile-selected-top {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  min-width: 0;
}

.mobile-selected-type {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  border-radius: 999px;
  padding: 1px 5px;
  font-size: 0.875rem;
  font-weight: 700;
  color: #fff;
  flex-shrink: 0;
}

.mobile-selected-text {
  font-size: 0.875rem;
  color: #334155;
  white-space: normal;
  overflow-wrap: anywhere;
  word-break: break-word;
  line-height: 1.35;
}

.mobile-selected-empty {
  font-size: 12px;
  color: #64748b;
}

.mobile-selected-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.day-type-mixed-today {
  background: linear-gradient(135deg, #ef4444, #38bdf8);
}

.day-type-mixed-past {
  background: linear-gradient(135deg, #7c3aed, #94a3b8);
}

.day-type-mixed-future {
  background: linear-gradient(135deg, #d97706, #22c55e);
}

.tag-today-stage,
.tag-stage-now {
  background: linear-gradient(135deg, #ef4444, #f97316);
}

.tag-today-schedule,
.tag-schedule-now {
  background: linear-gradient(135deg, #2563eb, #38bdf8);
}

.tag-past-stage {
  background: linear-gradient(135deg, #7c3aed, #a78bfa);
}

.tag-past-schedule {
  background: linear-gradient(135deg, #64748b, #94a3b8);
}

.tag-future-stage {
  background: linear-gradient(135deg, #d97706, #f59e0b);
}

.tag-future-schedule {
  background: linear-gradient(135deg, #16a34a, #22c55e);
}

.more-tag {
  background: #e2e8f0;
  color: #334155;
}

.detail-panel {
  margin-top: 6px;
  border-radius: 24px;
  border: 1px solid rgba(15, 23, 42, 0.08);
  background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
  padding: 18px;
}

.detail-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

@media (min-width: 1101px) {
  .detail-list.two-items {
    display: grid;
    grid-template-columns: repeat(2, minmax(0, 1fr));
    gap: 12px;
  }
}

.detail-item {
  border-radius: 18px;
  background: #fff;
  padding: 14px;
  border: 1px solid #e2e8f0;
}

.detail-item h4 {
  margin: 10px 0 6px;
  font-size: 16px;
  color: #0f172a;
}

.detail-item-head {
  align-items: flex-start;
}

.detail-type,
.detail-session {
  display: inline-flex;
  align-items: center;
  border-radius: 999px;
  padding: 4px 10px;
  font-size: 12px;
  font-weight: 700;
}

.detail-session {
  background: #eef2ff;
  color: #4338ca;
}

.detail-meta {
  margin: 0;
  color: #64748b;
  font-size: 13px;
}

.detail-actions {
  margin-top: 10px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.detail-empty {
  padding: 20px 10px 10px;
  color: #64748b;
}

@media (max-width: 1100px) {
  .home-body {
    grid-template-columns: 1fr;
  }

  .social-list {
    grid-template-columns: 1fr;
  }

  .detail-panel {
    margin-top: 18px;
  }

  .social-panel {
    position: static;
  }
}

@media (max-width: 768px) {
  .home-main {
    padding-left: 10px !important;
    padding-right: 10px !important;
  }

  .hero-panel {
    padding: 14px 6px 8px;
  }

  .calendar-panel {
    padding: 14px 10px;
    border-radius: 22px;
  }

  .calendar-header,
  .detail-header {
    align-items: flex-start;
    flex-direction: column;
  }

  .social-panel {
    padding: 14px 10px;
    border-radius: 22px;
  }

  .calendar-actions {
    width: 100%;
    display: grid;
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }

  .calendar-button {
    width: 100%;
    padding: 8px 10px;
    font-size: 13px;
  }

  .calendar-toolbar {
    align-items: flex-start;
    flex-direction: column;
    gap: 10px;
    margin: 12px 0 10px;
  }

  .legend {
    gap: 6px 8px;
  }

  .legend-item {
    font-size: 12px;
  }

  .calendar-grid,
  .weekday-row {
    gap: 5px;
  }

  .weekday-cell {
    font-size: 12px;
  }

  .day-cell {
    min-height: 72px;
    padding: 6px 5px;
    border-radius: 12px;
  }

  .day-number {
    font-size: 13px;
  }

  .day-top {
    flex-direction: column;
    align-items: flex-start;
    justify-content: flex-start;
    gap: 4px;
  }

  .day-type-badge {
    min-height: 16px;
    padding: 1px 5px;
    font-size: 10px;
  }

  .mobile-selected-panel {
    display: block;
    margin-top: -1px;
  }

  .detail-header h3,
  .social-panel-header h2,
  .calendar-header h2 {
    font-size: 20px;
  }
}
</style>