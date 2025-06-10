<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'

const groupedStages = ref({ 'Team SII': [], '新生': [], '其它': [] })
const expandedGroups = ref({ 'Team SII': false, '新生': false, '其它': false })
const maxInitial = 3

const toggleExpanded = group => {
  expandedGroups.value[group] = !expandedGroups.value[group]
}

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/stages')
    const data = await res.json()
    const temp = { 'Team SII': [], '新生': [], '其它': [] }

    data.forEach(item => {
      const type = item.type?.trim()
      if (type === 'Team SII') temp['Team SII'].push(item)
      else if (type === '新生' || type === 'New Members') temp['新生'].push(item)
      else temp['其它'].push(item)
    })

    for (const key in temp) {
      temp[key].sort((a, b) => parseInt(b.session) - parseInt(a.session))
    }

    groupedStages.value = temp
  } catch (e) {
    console.error('加载失败', e)
  }
})
</script>

<template>
  <div class="layout-page d-flex">
    <Sidebar />

    <main class="main-scrollable flex-grow-1 bg-white px-5 py-3 overflow-auto">
      <!-- 公演说明文字（放在所有公演列表之前） -->
      <div class="alert alert-info mb-4" role="note">
        <p class="mb-1">以下是 <strong>周童玥</strong> 参加的所有公演列表，包括Team SII公演、新生公演以及其它公演。</p>
        <p class="mb-1">点击右侧按钮可跳转至发布在 B 站的视频页面。</p>
        <p class="mb-1"><strong>完整公演视频</strong>：SNH48 官方账号发布的完整回放。</p>
        <p class="mb-0"><strong>小周 cut 视频</strong>：应援会发布的以周童玥为主的剪辑回放。</p>
      </div>
      <div class="w-100">
        <template v-for="(items, group) in groupedStages" :key="group">
          <h3 v-if="items.length" class="mt-4 mb-3">{{ group }} 公演</h3>
          <ul class="list-group mb-3">
            <li
              v-for="(item, index) in (expandedGroups[group] ? items : items.slice(0, maxInitial))"
              :key="item.id || item.session + item.date"
              class="list-group-item"
              >
              <div class="d-flex align-items-center">
                <!-- 左侧：场次 + 日期 -->
                <div class="text-center" style="min-width: 100px;">
                  <div class="fw-bold">第 {{ item.session }} 场</div>
                  <div class="text-muted">{{ item.date }}</div>
                </div>

                <!-- 中间：标题 -->
                <div class="flex-grow-1 text-center">
                  <div class="fw-semibold">{{ item.title }}</div>
                </div>

                <!-- 右侧：两个按钮 -->
                <div class="d-flex align-items-center gap-2">
                  <a
                    :href="item.url ? 'https://www.bilibili.com/video/' + item.url : null"
                    target="_blank"
                    class="btn btn-sm"
                    :class="item.url ? 'btn-primary' : 'btn-secondary disabled'"
                    :tabindex="!item.url ? -1 : null"
                    :aria-disabled="!item.url"
                  >
                    完整公演视频
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
                  <!-- <button class="btn btn-sm btn-outline-secondary">收藏</button> -->
                </div>
              </div>
            </li>
          </ul>
          <button
            v-if="items.length > maxInitial"
            class="btn btn-outline-primary btn-sm mb-4"
            @click="toggleExpanded(group)"
          >
            {{ expandedGroups[group] ? '收起' : '展开更多' }}
          </button>
        </template>
      </div>
    </main>
  </div>
</template>