// src/env.d.ts

/// <reference types="vite/client" />

// 1. ИСПРАВЛЕНИЕ ОШИБКИ TS2339 (для import.meta.env)
// Объявляем интерфейс для переменных окружения Vite
interface ImportMetaEnv {
  // Объявите здесь все переменные VITE_, которые вы используете
  readonly VITE_API_BASE_URL: string
  // Если у вас есть другие переменные, добавьте их (например, VITE_SOME_KEY: string)
}

interface ImportMeta {
  readonly env: ImportMetaEnv
}


// 2. ИСПРАВЛЕНИЕ ОШИБКИ TS7016 (для импорта .vue файлов)
// Объявляем типы для импортируемых Vue-компонентов
declare module '*.vue' {
  import type { DefineComponent } from 'vue'
  // Используем `DefineComponent` для корректной типизации
  const component: DefineComponent<{}, {}, any>
  export default component
}