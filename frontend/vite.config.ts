import { fileURLToPath, URL } from 'node:url'

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import vueJsx from '@vitejs/plugin-vue-jsx'

// https://vite.dev/config/
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
      '/api': {
        target: process.env.NODE_ENV === 'production' 
          ? 'https://dkor.pro'  // Production: use your domain with HTTPS
          : 'http://localhost:8000',  // Development: local Django server
        changeOrigin: true,
        secure: process.env.NODE_ENV === 'production',
        // rewrite: (path) => path.replace(/^\/api/, ''),
      },
    },
  },
})
