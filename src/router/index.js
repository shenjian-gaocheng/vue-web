import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Weibo from '../pages/Weibo.vue'
import Stages from '../pages/Stages.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/weibo', name: 'Weibo', component: Weibo },
  { path: '/stages', name: 'Stages', component: Stages }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
