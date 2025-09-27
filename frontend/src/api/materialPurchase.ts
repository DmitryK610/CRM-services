// src/api/materialPurchase.ts

import { api } from '@/utils/api';
import type { MaterialPurchase, MaterialPurchaseCreatePayload, MaterialPurchaseUpdatePayload } from '@/types/materialPurchase'; // Импортируем определенные вами типы

// Интерфейс для пагинированных ответов API (если ваш ViewSet использует пагинацию, как стандартно для DRF)
interface PaginatedResponse<T> {
    count: number;
    next: string | null;
    previous: string | null;
    results: T[];
}

// URL базового эндпоинта для закупок материалов
// Убедитесь, что этот путь соответствует вашим urls.py (например, 'api/material-purchases/')
const API_URL = 'material-purchases/';

// Функция для получения списка закупок материалов
// Может принимать параметры для фильтрации, поиска или пагинации (например, { order_id: 1, search: 'Гранит' })
export async function getMaterialPurchases<T = MaterialPurchase[] | PaginatedResponse<MaterialPurchase>>(params?: any): Promise<T> {
    const endpoint = params ? `${API_URL}?${new URLSearchParams(params)}` : API_URL;
    const data = await api.get<T>(endpoint);
    if (!data) {
        // Возвращаем пустой массив или объект по умолчанию, чтобы избежать ошибок в сторе
        return { count: 0, next: null, previous: null, results: [] } as unknown as T;
    }
    return data;
}

// Функция для получения одной закупки материала по ID
export async function getMaterialPurchase(id: number): Promise<MaterialPurchase> {
    const data = await api.get<MaterialPurchase>(`${API_URL}${id}/`);
    if (!data) throw new Error(`Закупка с ID ${id} не найдена.`);
    return data;
}

// Функция для создания новой закупки материала
export async function createMaterialPurchase(payload: MaterialPurchaseCreatePayload): Promise<MaterialPurchase> {
    const data = await api.post<MaterialPurchaseCreatePayload, MaterialPurchase>(API_URL, payload);
    if (!data) throw new Error('Не удалось создать закупку.');
    return data;
}

// Функция для обновления существующей закупки материала по ID (используем PATCH для частичного обновления)
export async function updateMaterialPurchase(id: number, payload: MaterialPurchaseUpdatePayload): Promise<MaterialPurchase> {
    const data = await api.patch<MaterialPurchaseUpdatePayload, MaterialPurchase>(`${API_URL}${id}/`, payload);
    if (!data) throw new Error('Не удалось обновить закупку.');
    return data;
}

// Функция для удаления закупки материала по ID
export async function deleteMaterialPurchase(id: number): Promise<void> {
    await api.delete(`${API_URL}${id}/`);
}
