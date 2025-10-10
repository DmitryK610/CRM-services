// src/stores/authStore.ts

import { defineStore } from 'pinia';
import { ref, computed } from 'vue';
import type { User } from '@/types/user';
import * as authApi from '@/api/auth';
import type { LoginResponse } from '@/api/auth';

export const useAuthStore = defineStore('auth', () => {
  // Состояния
  const isAuthenticated = ref(false);
  const authToken = ref<string | null>(null);
  const refreshToken = ref<string | null>(null);
  const user = ref<User | null>(null);
  const isLoading = ref(false);
  const error = ref<string | null>(null);

  // Геттеры
  const getUser = computed(() => user.value);
  const getIsLoading = computed(() => isLoading.value);
  const getError = computed(() => error.value);

  /**
   * Сбрасывает состояние аутентификации
   */
  function resetAuthState() {
    isAuthenticated.value = false;
    authToken.value = null;
    refreshToken.value = null;
    user.value = null;
    error.value = null;
    isLoading.value = false;
    localStorage.removeItem('authToken');
    localStorage.removeItem('refreshToken');
    localStorage.removeItem('user');
  }

  /**
   * Действие для входа пользователя
   */
  async function login(username: string, password: string) {
    isLoading.value = true;
    error.value = null;

    try {
      console.log('[authStore] login start', { username });
      const loginResponse = await authApi.login({ username, password }) as LoginResponse;
      const accessToken = loginResponse.token ?? loginResponse.access ?? null;
      const refresh = loginResponse.refresh ?? null;

      if (accessToken) {
        isAuthenticated.value = true;
        authToken.value = accessToken;
        refreshToken.value = refresh;
        user.value = loginResponse.user || null;

        localStorage.setItem('authToken', accessToken);
        if (refresh) {
          localStorage.setItem('refreshToken', refresh);
        } else {
          localStorage.removeItem('refreshToken');
        }

        if (loginResponse.user) {
          localStorage.setItem('user', JSON.stringify(loginResponse.user));
        } else {
          localStorage.removeItem('user');
        }

        console.log('[authStore] login success', {
          username,
          hasAccessToken: Boolean(accessToken),
          hasRefreshToken: Boolean(refresh),
          hasUser: Boolean(loginResponse.user)
        });
      } else {
        error.value = 'Неверный логин или пароль.';
        resetAuthState();
        console.warn('[authStore] login missing token', { username });
      }
    } catch (err: unknown) {
      error.value = err instanceof Error ? err.message : 'Ошибка при выполнении входа.';
      console.error('[authStore] login error', err);
      resetAuthState();
      throw err; // Пробрасываем ошибку для обработки в компоненте при необходимости
    } finally {
      isLoading.value = false;
      console.log('[authStore] login finished', {
        username,
        isAuthenticated: isAuthenticated.value,
        error: error.value
      });
    }
  }

  /**
   * Действие для выхода пользователя
   */
  function logout() {
    resetAuthState();
  }

  /**
   * Проверка аутентификации при загрузке
   */
  function checkAuthOnLoad() {
    const storedToken = localStorage.getItem('authToken');
    const storedRefresh = localStorage.getItem('refreshToken');
    const storedUser = localStorage.getItem('user');

    if (storedToken) {
      isAuthenticated.value = true;
      authToken.value = storedToken;
      refreshToken.value = storedRefresh;

      if (storedUser) {
        try {
          user.value = JSON.parse(storedUser) as User;
        } catch (e) {
          console.error('Ошибка парсинга пользователя:', e);
          logout();
        }
      }
    }
  }

  return {
    isAuthenticated,
    authToken,
    refreshToken,
    user,
    isLoading,
    error,
    getUser,
    getIsLoading,
    getError,
    login,
    logout,
    checkAuthOnLoad,
    resetAuthState // Экспортируем resetAuthState, если нужно использовать в компонентах
  };
});
