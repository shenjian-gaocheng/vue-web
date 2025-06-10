import { createRouter, createWebHistory } from 'vue-router'
import Home from '../pages/Home.vue'
import Weibo from '../pages/Weibo.vue'
import Baike from '../pages/Baike.vue'
import Stages from '../pages/Stages.vue'
import Fun from '../pages/Fun.vue'
import Relation from '../pages/Relation.vue'
import Events from '../pages/Events.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  { path: '/weibo', name: 'Weibo', component: Weibo },
  { path: '/baike', name: 'Baike', component: Baike },
  { path: '/stages', name: 'Stages', component: Stages },
  { path: '/fun', name: 'Fun', component: Fun },
  { path: '/relation', name: 'Relation', component: Relation },
  { path: '/events', name: 'Events', component: Events },
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
