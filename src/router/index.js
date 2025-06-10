import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Weibo from '../pages/Weibo.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/weibo', name: 'Weibo', component: Weibo }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
