import { createRouter, createWebHashHistory } from 'vue-router'
import Home from '@/pages/Home.vue'
// import Weibo from '@/pages/Weibo.vue'
import Portrait from '@/pages/Portrait.vue'
import Baike from '@/pages/Baike.vue'
import Stages from '@/pages/Stages.vue'
// import Fun from '@/pages/Fun.vue'
// import Relation from '@/pages/Relation.vue'
import Events from '@/pages/Events.vue'
import About from '@/pages/About.vue'
import Login from '@/pages/Login.vue'
import AdminLogs from '@/pages/AdminLogs.vue'
import KnowledgeChat from '@/pages/KnowledgeChat.vue'

const routes = [
  { path: '/', name: 'Home', component: Home },
  // { path: '/weibo', name: 'Weibo', component: Weibo },
  { path: '/baike', name: 'Baike', component: Baike },
  { path: '/portrait', name: 'Portrait', component: Portrait },
  { path: '/stages', name: 'Stages', component: Stages },
  // { path: '/fun', name: 'Fun', component: Fun },
  // { path: '/relation', name: 'Relation', component: Relation },
  { path: '/events', name: 'Events', component: Events },
  { path: '/about', name: 'About', component: About },
  { path: '/admin-login', name: 'Login', component: Login },
  { path: '/admin-logs', name: 'AdminLogs', component: AdminLogs },
  { path: '/knowledge-chat', name: 'KnowledgeChat', component: KnowledgeChat },
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
