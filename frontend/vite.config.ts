import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [vue(), vueJsx()],
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),
    },
  },
  server: {
    port: 5173,
    host: true,
    strictPort: true,
    proxy: {
      // Когда фронтенд в режиме разработки делает запрос на /api/...,
      // Vite Dev Server должен перенаправить его на локальный API-шлюз Docker Compose.
      '/api': {
        // ИСПРАВЛЕНО: Target должен быть именем NGINX-шлюза (gateway) в Docker-сети.
        target: 'http://gateway', 
        changeOrigin: true,
        // ИСПРАВЛЕНО: Убираем rewrite, так как NGINX уже ждет префикс /api/
        // (Ваш NGINX ожидает /api/users/login/, поэтому префикс /api должен остаться).
      },
    },
  },
})
