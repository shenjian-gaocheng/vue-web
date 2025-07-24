import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'  

export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')  // 设置路径别名 @ -> src
    }
  },
  server: {
    host: '0.0.0.0',  // 允许局域网访问
    port: 5173        // 你自定义的端口
  }
})