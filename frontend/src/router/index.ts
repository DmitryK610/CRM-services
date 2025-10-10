// router/index.ts

import { createRouter, createWebHistory } from 'vue-router'

import type { RouteRecordRaw, RouteLocationNormalized, NavigationGuardNext } from 'vue-router'
import { routes } from './routes'
import { useAuthStore } from '@/stores/authStore'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  
  routes: routes as Readonly<RouteRecordRaw[]>,

  scrollBehavior(to, from, savedPosition) {
    if (savedPosition) {
      return savedPosition
    } else {
      return { top: 0, behavior: 'smooth' }
    }
  },
})

router.beforeEach(
  (to: RouteLocationNormalized, from: RouteLocationNormalized, next: NavigationGuardNext) => {
    const authStore = useAuthStore()

    const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)

    // Теперь это значение АКТУАЛЬНОЕ, даже после перезагрузки страницы
    const isAuthenticated = authStore.isAuthenticated

    if (requiresAuth && !isAuthenticated) {
      next({
        name: 'Login',

        query: { redirect: to.fullPath },
      })
    } else if (to.name === 'Login' && isAuthenticated) {
      next({ name: 'Dashboard' })
    } else {
      next()
    }
  },
)

export default router
