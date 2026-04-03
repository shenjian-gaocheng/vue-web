<script setup>
import { computed, onMounted, ref } from 'vue'
import OverlayMask from '@/components/OverlayMask.vue'
import Topbar from '@/components/Topbar.vue'
import Sidebar from '@/components/Sidebar.vue'
import Notification from '@/components/Notification.vue'
import { useApi } from '@/composables/fetch'
import { useResponsiveSidebar } from '@/composables/useResponsiveSidebar'

const { isMobile, isSidebarCollapsed } = useResponsiveSidebar()
const { apiFetch } = useApi()

const portraitItems = ref([])
const isLoading = ref(true)
const expandedPortraitKeys = ref([])
const galleryRefs = ref({})
const galleryIndexes = ref({})

const formatYearMonth = (ym) => {
  const year = Math.floor(ym / 100)
  const month = ym % 100
  return `${year}年${month}月`
}

const portraitWebsite = (verCode) => {
  return `https://snh48-group-member-girls-gsz-1301155593.cos.ap-shanghai.myqcloud.com/SNH48_GROUP_MEMBER_GIRLS_GSZ/image/snh48/${verCode}/`
}

const createPortraitTitle = (item, isCurrent) => {
  if (isCurrent) {
    return `当前公式照：${item.name}`
  }
  return `${item.ver_yearmonth}公式照：${item.name}`
}

const orderedPortraitItems = computed(() => {
  const sorted = [...portraitItems.value].sort((a, b) => a.verYearMonth - b.verYearMonth)
  if (sorted.length === 0) {
    return []
  }

  const latestItem = sorted[sorted.length - 1]
  const historyItems = sorted.slice(0, -1)

  return [latestItem, ...historyItems].map((item, index) => ({
    ...item,
    isCurrent: index === 0,
    title: createPortraitTitle(item, index === 0)
  }))
})

const setInitialExpandedPortrait = () => {
  const [currentPortrait] = orderedPortraitItems.value
  expandedPortraitKeys.value = currentPortrait ? [currentPortrait.key] : []
}

const isPortraitExpanded = (item) => {
  if (!isMobile.value) {
    return true
  }
  return expandedPortraitKeys.value.includes(item.key)
}

const togglePortrait = (key) => {
  if (!isMobile.value) {
    return
  }

  if (expandedPortraitKeys.value.includes(key)) {
    expandedPortraitKeys.value = expandedPortraitKeys.value.filter(itemKey => itemKey !== key)
    return
  }

  expandedPortraitKeys.value = [...expandedPortraitKeys.value, key]
}

const setGalleryRef = (key, element) => {
  if (element) {
    galleryRefs.value[key] = element
    return
  }
  delete galleryRefs.value[key]
}

const updateGalleryIndex = (key) => {
  const gallery = galleryRefs.value[key]
  if (!gallery || gallery.clientWidth === 0) {
    return
  }
  galleryIndexes.value[key] = Math.round(gallery.scrollLeft / gallery.clientWidth)
}

const scrollGalleryTo = (key, nextIndex) => {
  const gallery = galleryRefs.value[key]
  if (!gallery) {
    return
  }

  const safeIndex = Math.max(0, Math.min(nextIndex, 3))
  galleryIndexes.value[key] = safeIndex
  gallery.scrollTo({
    left: gallery.clientWidth * safeIndex,
    behavior: 'smooth'
  })
}

const moveGallery = (key, delta) => {
  const currentIndex = galleryIndexes.value[key] ?? 0
  scrollGalleryTo(key, currentIndex + delta)
}

const loadPortraits = async () => {
  isLoading.value = true
  try {
    const { ok, data } = await apiFetch('/portraits')
    if (!ok) {
      alert('❌ 公式照数据加载失败')
      return
    }

    portraitItems.value = (data ?? [])
      .map(item => {
        const baseUrl = portraitWebsite(item.ver_code)
        return {
          id: item.id,
          key: `${item.ver_yearmonth}_${item.ver_code}`,
          verYearMonth: item.ver_yearmonth,
          ver_yearmonth: formatYearMonth(item.ver_yearmonth),
          name: item.name,
          zp: `${baseUrl}zp_10290.jpg`,
          gsImages: [
            `${baseUrl}gs4_10290_1.jpg`,
            `${baseUrl}gs4_10290_2.jpg`,
            `${baseUrl}gs4_10290_3.jpg`,
            `${baseUrl}gs4_10290_4.jpg`
          ]
        }
      })

    setInitialExpandedPortrait()
  } catch (e) {
    console.error('加载失败', e)
  } finally {
    isLoading.value = false
  }
}

onMounted(() => {
  loadPortraits()
})
</script>

<template>
  <div class="layout-page d-flex">
    <Topbar
      v-if="isMobile"
      :collapsed="isSidebarCollapsed"
      @update:collapsed="isSidebarCollapsed = $event"
    />

    <OverlayMask
      v-if="isMobile && !isSidebarCollapsed"
      @click="isSidebarCollapsed = true"
    />

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

      <section class="portrait-section">
        <div class="portrait-header">
          <p class="portrait-kicker">Official Portrait</p>
          <h1 class="portrait-page-title">公式照展示</h1>
          <p class="portrait-desc">桌面端按整组展示当前版本与历史版本，移动端支持折叠查看和横向切换组图。</p>
        </div>

        <div v-if="isLoading" class="empty-tip">正在加载公式照…</div>
        <div v-else-if="orderedPortraitItems.length === 0" class="empty-tip">暂无公式照数据</div>

        <div v-else class="portrait-list">
          <article
            v-for="item in orderedPortraitItems"
            :key="item.key"
            class="portrait-block"
            :class="{ current: item.isCurrent }"
          >
            <button
              v-if="isMobile"
              type="button"
              class="portrait-mobile-toggle"
              @click="togglePortrait(item.key)"
            >
              <span class="portrait-title-wrap">
                <span class="portrait-title">{{ item.title }}</span>
                <span class="portrait-date">{{ item.ver_yearmonth }}</span>
              </span>
              <span class="portrait-toggle-icon">{{ isPortraitExpanded(item) ? '收起' : '展开' }}</span>
            </button>

            <div v-else class="portrait-heading-row">
              <h2 class="portrait-title">{{ item.title }}</h2>
              <span class="portrait-date">{{ item.ver_yearmonth }}</span>
            </div>

            <div v-if="isPortraitExpanded(item)" class="portrait-content">
              <div v-if="!isMobile" class="portrait-desktop-grid">
                <figure class="portrait-card portrait-card-zp">
                  <img :src="item.zp" :alt="`${item.name} 正片`" loading="lazy" />
                  <figcaption>zp</figcaption>
                </figure>

                <figure
                  v-for="(img, index) in item.gsImages"
                  :key="`${item.key}_desktop_${index}`"
                  class="portrait-card"
                >
                  <img :src="img" :alt="`${item.name} gs${index + 1}`" loading="lazy" />
                  <figcaption>{{ `gs${index + 1}` }}</figcaption>
                </figure>
              </div>

              <div v-else class="portrait-mobile-stack">
                <figure class="portrait-card portrait-card-zp portrait-mobile-zp">
                  <img :src="item.zp" :alt="`${item.name} 正片`" loading="lazy" />
                  <figcaption>zp</figcaption>
                </figure>

                <div class="portrait-slider-shell">
                  <div class="portrait-slider-head">
                    <span class="slider-label">gs1 - gs4</span>
                    <div class="slider-actions">
                      <button
                        type="button"
                        class="slider-btn"
                        :disabled="(galleryIndexes[item.key] ?? 0) === 0"
                        @click="moveGallery(item.key, -1)"
                      >
                        上一张
                      </button>
                      <button
                        type="button"
                        class="slider-btn"
                        :disabled="(galleryIndexes[item.key] ?? 0) === 3"
                        @click="moveGallery(item.key, 1)"
                      >
                        下一张
                      </button>
                    </div>
                  </div>

                  <div
                    :ref="element => setGalleryRef(item.key, element)"
                    class="portrait-slider"
                    @scroll="updateGalleryIndex(item.key)"
                  >
                    <figure
                      v-for="(img, index) in item.gsImages"
                      :key="`${item.key}_mobile_${index}`"
                      class="portrait-card portrait-slide"
                    >
                      <img :src="img" :alt="`${item.name} gs${index + 1}`" loading="lazy" />
                      <figcaption>{{ `gs${index + 1}` }}</figcaption>
                    </figure>
                  </div>

                  <div class="slider-dots">
                    <button
                      v-for="(_, index) in item.gsImages"
                      :key="`${item.key}_dot_${index}`"
                      type="button"
                      class="slider-dot"
                      :class="{ active: (galleryIndexes[item.key] ?? 0) === index }"
                      @click="scrollGalleryTo(item.key, index)"
                    >
                      {{ index + 1 }}
                    </button>
                  </div>
                </div>
              </div>
            </div>
          </article>
        </div>
      </section>
    </main>
  </div>
</template>

<style scoped>
.portrait-section {
  width: min(1120px, 100%);
  margin: 0 auto;
  padding: 18px 0 40px;
  text-align: left;
}

.portrait-header {
  margin: 0 auto 28px;
  padding: 24px 28px;
  border-radius: 28px;
  background: linear-gradient(135deg, #fff7dc 0%, #ffffff 45%, #fff1b8 100%);
  border: 1px solid rgba(242, 183, 5, 0.2);
  box-shadow: 0 18px 40px rgba(125, 90, 17, 0.08);
  text-align: center;
}

.portrait-kicker {
  margin: 0 0 6px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.18em;
  text-transform: uppercase;
  color: #9e7b15;
}

.portrait-page-title {
  margin: 0;
  font-size: clamp(30px, 5vw, 46px);
  font-weight: 800;
  color: #332505;
}

.portrait-desc {
  margin: 12px auto 0;
  max-width: 760px;
  font-size: 15px;
  line-height: 1.7;
  color: #6c5a28;
}

.portrait-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.portrait-block {
  border-radius: 24px;
  border: 1px solid #f3e7bf;
  background: linear-gradient(180deg, #fffdf6 0%, #ffffff 100%);
  box-shadow: 0 12px 30px rgba(120, 95, 36, 0.08);
  padding: 24px;
}

.portrait-block.current {
  border-color: rgba(242, 183, 5, 0.45);
  box-shadow: 0 18px 40px rgba(201, 151, 24, 0.18);
}

.portrait-heading-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 16px;
  margin-bottom: 18px;
}

.portrait-title-wrap {
  display: flex;
  flex-direction: column;
  gap: 4px;
  text-align: left;
}

.portrait-title {
  margin: 0;
  font-size: clamp(22px, 3vw, 28px);
  font-weight: 800;
  line-height: 1.3;
  color: #312404;
}

.portrait-date {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  min-width: 98px;
  padding: 7px 12px;
  border-radius: 999px;
  background: rgba(242, 183, 5, 0.14);
  color: #8f6f13;
  font-size: 13px;
  font-weight: 700;
}

.portrait-content {
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.portrait-desktop-grid {
  display: grid;
  grid-template-columns: repeat(5, minmax(0, 1fr));
  gap: 14px;
}

.portrait-mobile-stack {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.portrait-card {
  margin: 0;
  overflow: hidden;
  border-radius: 18px;
  background: #f8f2dd;
  border: 1px solid rgba(242, 183, 5, 0.24);
  box-shadow: 0 10px 24px rgba(121, 98, 38, 0.12);
}

.portrait-card img {
  display: block;
  width: 100%;
  height: auto;
  background: #f6edd0;
}

.portrait-card figcaption {
  padding: 10px 12px;
  font-size: 13px;
  font-weight: 800;
  letter-spacing: 0.08em;
  color: #7d6212;
  text-transform: uppercase;
  text-align: center;
}

.portrait-mobile-toggle {
  width: 100%;
  padding: 0;
  border: none;
  background: transparent;
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  margin-bottom: 14px;
}

.portrait-toggle-icon {
  flex-shrink: 0;
  padding: 8px 12px;
  border-radius: 999px;
  background: rgba(242, 183, 5, 0.14);
  color: #8f6f13;
  font-size: 13px;
  font-weight: 700;
}

.portrait-slider-shell {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.portrait-slider-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
}

.slider-label {
  font-size: 14px;
  font-weight: 800;
  color: #6f5815;
}

.slider-actions {
  display: flex;
  gap: 8px;
}

.slider-btn {
  border: 1px solid rgba(242, 183, 5, 0.28);
  border-radius: 999px;
  background: #fffdf6;
  color: #755c15;
  padding: 8px 12px;
  font-size: 12px;
  font-weight: 700;
}

.slider-btn:disabled {
  opacity: 0.45;
  cursor: not-allowed;
}

.portrait-slider {
  display: flex;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.portrait-slider::-webkit-scrollbar {
  display: none;
}

.portrait-slide {
  flex: 0 0 100%;
  scroll-snap-align: start;
}

.slider-dots {
  display: flex;
  justify-content: center;
  gap: 8px;
}

.slider-dot {
  width: 30px;
  height: 30px;
  border-radius: 999px;
  border: 1px solid rgba(242, 183, 5, 0.28);
  background: #fff;
  color: #8a6f1d;
  font-size: 12px;
  font-weight: 700;
}

.slider-dot.active {
  background: #f2b705;
  border-color: #f2b705;
  color: #fff;
}

.empty-tip {
  padding: 36px 18px;
  border-radius: 20px;
  background: #fff9e8;
  color: #887242;
  font-size: 15px;
  text-align: center;
}

@media (max-width: 768px) {
  .portrait-section {
    padding: 10px 0 28px;
  }

  .portrait-header {
    padding: 22px 18px;
    border-radius: 22px;
  }

  .portrait-block {
    padding: 18px;
    border-radius: 20px;
  }

  .portrait-mobile-toggle {
    margin-bottom: 0;
  }

  .portrait-mobile-zp {
    width: 100%;
  }

  .portrait-slider-head {
    align-items: flex-start;
    flex-direction: column;
  }
}

</style>
