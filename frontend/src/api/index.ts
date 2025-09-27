import axios from 'axios';
import type { AxiosRequestConfig } from 'axios';

// Очищает только относительные URL, не трогая абсолютные
const normalizeUrl = (url: string) => url.startsWith('http') ? url : url.replace(/([^:]\/)\/+/g, '$1');

const getBaseURL = () => {
  if (import.meta.env.DEV) {
    // Всегда заканчивается на /
    return (import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000/api').replace(/\/+$/, '') + '/';
  }
  return (import.meta.env.VITE_API_BASE_URL || 'https://dkor.pro/api').replace(/\/+$/, '') + '/';
};

const instance = axios.create({
  baseURL: getBaseURL(),
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

instance.interceptors.request.use(config => {
  config.url = normalizeUrl(config.url || '');
  return config;
});

export const api = {
  get: async <T>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    const response = await instance.get<T>(normalizeUrl(url), config);
    return response.data;
  },
  post: async <T, R>(url: string, data: T, config?: AxiosRequestConfig): Promise<R> => {
    const response = await instance.post<R>(normalizeUrl(url), data, config);
    return response.data;
  },
  put: async <T, R>(url: string, data: T, config?: AxiosRequestConfig): Promise<R> => {
    const response = await instance.put<R>(normalizeUrl(url), data, config);
    return response.data;
  },
  delete: async <T = void>(url: string, config?: AxiosRequestConfig): Promise<T> => {
    const response = await instance.delete<T>(normalizeUrl(url), config);
    return response.data;
  },
};