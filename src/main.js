import { createApp } from 'vue'
import { createPinia } from 'pinia'
import './style.css'
import App from './App.vue'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import './assets/common.css'

createApp(App)
  .use(router)
  .use(createPinia())
  .mount('#app')
