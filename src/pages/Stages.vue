<script setup>
import { ref, onMounted } from 'vue'
import Sidebar from '../components/Sidebar.vue'

const groupedStages = ref({ 'Team SII': [], '新生': [], Other: [] })
const expandedGroups = ref({ 'Team SII': false, '新生': false, Other: false })
const maxInitial = 3

const toggleExpanded = group => {
  expandedGroups.value[group] = !expandedGroups.value[group]
}

onMounted(async () => {
  try {
    const res = await fetch('http://127.0.0.1:5000/api/stages')
    const data = await res.json()
    const temp = { 'Team SII': [], '新生': [], Other: [] }

    data.forEach(item => {
      const type = item.type?.trim()
      if (type === 'Team SII') temp['Team SII'].push(item)
      else if (type === '新生' || type === 'New Members') temp['新生'].push(item)
      else temp.Other.push(item)
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
  <div class="d-flex vh-100">
    <Sidebar />

    <main class="flex-grow-1 bg-white px-4 py-3 overflow-auto">
      <div class="w-100">
        <template v-for="(items, group) in groupedStages" :key="group">
          <h4 v-if="items.length" class="mt-4 mb-3">{{ group }} 公演</h4>
          <ul class="list-group mb-3">
            <li
              v-for="(item, index) in (expandedGroups[group] ? items : items.slice(0, maxInitial))"
              :key="item.id || item.session + item.date"
              class="list-group-item"
            >
              <strong>{{ item.date }}</strong>
              （第 {{ item.session }} 场） | {{ item.title }}<br />
              <a :href="item.url" target="_blank">{{ item.url }}</a>
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