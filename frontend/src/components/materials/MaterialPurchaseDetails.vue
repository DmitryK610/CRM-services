<template>
  <div class="material-purchase-details-view" :class="{ 'in-modal': !!props.isModal }">
    <h1 class="page-title">Детали закупки материала</h1>

    <div v-if="purchaseStore.isFetchingDetails" class="status-message loading-message">
      <div class="loader"></div> Загрузка деталей закупки...
    </div>
    <div v-else-if="purchaseStore.fetchDetailsError" class="status-message error-message">
      <span class="error-icon">⚠️</span>
      <span class="error-text">Ошибка загрузки деталей закупки: {{ purchaseStore.fetchDetailsError }}</span>
      <button @click="purchaseStore.clearFetchDetailsError()" class="close-error-button" title="Закрыть">×</button>
    </div>
    <div v-else-if="!purchaseDetails" class="status-message no-results-message">
      Детали закупки не найдены.
    </div>
    <div v-else class="details-content">
      <div class="details-section">
        <h2 v-if="!isModal">Основная информация о закупке</h2>
        <div class="details-grid">
          <div class="detail-line">
            <strong>ID:</strong>
            <span>{{ purchaseDetails.id }}</span>
          </div>
          <div class="detail-line">
            <strong>Материал:</strong>
            <span>{{ materialDisplay }}</span>
          </div>
          <div class="detail-line">
            <strong>Артикул:</strong>
            <span>{{ purchaseDetails.material_details?.color_code || '---' }}</span>
          </div>
          <div class="detail-line">
            <strong>Поставщик:</strong>
            <span>{{ purchaseDetails.material_details?.supplier_details?.company_name || '---' }}</span>
          </div>
          <div class="detail-line">
            <strong>Количество:</strong>
            <span>{{ purchaseDetails.quantity }}</span>
          </div>
          <div class="detail-line">
            <strong>Общая стоимость:</strong>
            <span>{{ formatCurrencyRub(purchaseDetails.total_cost) }}</span>
          </div>
          <div class="detail-line">
            <strong>Метод оплаты:</strong>
            <span>{{ getPaymentMethodText(purchaseDetails.payment_method) }}</span>
          </div>
          <div class="detail-line">
            <strong>Дата заказа:</strong>
            <span>{{ formatDate(purchaseDetails.purchase_order_date) }}</span>
          </div>
          <div class="detail-line">
            <strong>Статус:</strong>
            <span>
              <span :class="['status-badge', `status-badge-${purchaseDetails.status}`]">{{
                getStatusText(purchaseDetails.status) }}</span>
            </span>
          </div>
          <div class="detail-line" v-if="purchaseDetails.status === 'received'">
            <strong>Дата получения:</strong>
            <span>{{ formatDate(purchaseDetails.received_date) }}</span>
          </div>
          <div class="detail-line">
            <strong>Связанный заказ:</strong>
            <span>{{ orderDisplay }}</span>
          </div>
          <div class="detail-line note-line" v-if="purchaseDetails.notes">
            <strong>Примечание:</strong>
            <span class="note-value-span">{{ purchaseDetails.notes }}</span>
          </div>
        </div>
      </div>

      <div class="actions-panel" v-if="!isModal">
        <router-link :to="{ name: 'MaterialsView' }" class="btn secondary-button">
          К списку закупок
        </router-link>
        <router-link :to="{ name: 'EditMaterialPurchaseView', params: { id: purchaseDetails.id } }"
          class="btn primary-button">
          Редактировать
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, watch, defineProps } from 'vue';
import { useRoute } from 'vue-router';
import { useMaterialPurchaseStore } from '@/stores/materialPurchaseStore';
import { useMaterialStore } from '@/stores/materialStore';
import type { MaterialPurchase } from '@/types/materialPurchase';

const props = defineProps<{ isModal?: boolean; modalPurchaseId?: number | null }>();
const route = useRoute();
const purchaseStore = useMaterialPurchaseStore();
const materialStore = useMaterialStore();

const purchaseId = computed(() => {
  if (props.modalPurchaseId !== undefined) {
    return props.modalPurchaseId === null ? NaN : Number(props.modalPurchaseId);
  }
  return Number(route.params.id);
});

const purchaseDetails = computed<MaterialPurchase | null>(() => {
  if (isNaN(purchaseId.value)) return null;
  return purchaseStore.getPurchaseById(purchaseId.value);
});

const fetchPurchaseDetailsData = async (id: number) => {
  if (isNaN(id)) {
    console.error('Неверный ID закупки для загрузки:', route.params.id);
    purchaseStore.setError('Неверный ID закупки.');
    return;
  }

  if (!purchaseStore.getPurchaseById(id)) {
    await purchaseStore.fetchMaterialPurchase(id);
  } else {
    purchaseStore.clearError();
  }

  if (materialStore.materials.length === 0 && !materialStore.isLoading) {
    await materialStore.fetchMaterials();
  }
};

onMounted(async () => {
  await fetchPurchaseDetailsData(purchaseId.value);
});

watch(purchaseId, async (newId, oldId) => {
  if (newId && newId !== oldId && !isNaN(newId)) {
    await fetchPurchaseDetailsData(newId);
  }
});

const materialDisplay = computed(() => {
  if (!purchaseDetails.value?.material) return '---';
  if (purchaseDetails.value.material_details?.material_name) {
    return purchaseDetails.value.material_details.material_name;
  }
  const material = materialStore.materials.find(m => m.id === purchaseDetails.value?.material);
  return material ? material.material_name || 'Материал без названия' : `ID материала: ${purchaseDetails.value.material}`;
});

const orderDisplay = computed(() => {
  if (!purchaseDetails.value?.order) return '---';
  if (purchaseDetails.value.order_details?.order_number) {
    return `Заказ №${purchaseDetails.value.order_details.order_number}`;
  }
  return `ID заказа: ${purchaseDetails.value.order}`;
});

const formatCurrencyRub = (value: number | string | undefined | null): string => {
  if (value === undefined || value === null || value === '') return '---';
  const numValue = Number(value);
  if (isNaN(numValue)) {
    console.warn("Attempted to format a non-numeric value as currency:", value);
    return '---';
  }

  try {
    return numValue.toLocaleString('ru-RU', {
      style: 'currency',
      currency: 'RUB',
      minimumFractionDigits: 2,
      maximumFractionDigits: 2
    });
  } catch (e) {
    console.error("Error formatting currency:", value, e);
    return `${numValue.toFixed(2)} ₽`;
  }
};

const getPaymentMethodText = (method: string | null | undefined): string => {
  if (!method) return '---';
  switch (method) {
    case 'cash': return 'Наличные';
    case 'cashless': return 'Безналичные';
    default: return method;
  }
};

const getStatusText = (status: string | null | undefined): string => {
  if (!status) return '---';
  switch (status) {
    case 'not-received': return 'Ожидается';
    case 'received': return 'Получен';
    case 'cancelled': return 'Отменен';
    default: return status;
  }
};

const formatDate = (dateInput: string | Date | null | undefined): string => {
  if (!dateInput) return '---';
  try {
    const date = new Date(dateInput);
    if (isNaN(date.getTime())) { return 'Неверная дата'; }
    return date.toLocaleDateString('ru-RU');
  } catch {
    return 'Ошибка форматирования даты';
  }
};

</script>

<style scoped>
.material-purchase-details-view {
  border: 1px solid #ddd;
  border-radius: 8px;
  padding: 20px;
  margin: 20px auto;
  max-width: 960px;
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  color: #333;
  box-sizing: border-box;
}

.material-purchase-details-view.in-modal {
  padding: 0;
  margin: 0;
  max-width: 100%;
  border: none;
  box-shadow: none;
}

.page-title {
  color: #2c3e50;
  text-align: center;
  margin-top: 0;
  margin-bottom: 24px;
  font-size: 24px;
  font-weight: 600;
  border-bottom: 1px solid #eee;
  padding-bottom: 10px;
}

.details-section {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #eee;
  border-radius: 6px;
  background-color: #f9f9f9;
}

.material-purchase-details-view.in-modal .details-section {
  margin-bottom: 16px;
  padding: 0;
  border: none;
  border-radius: 0;
  background-color: transparent;
}

.details-section h2 {
  color: #555;
  margin-top: 0;
  margin-bottom: 15px;
  font-size: 1.4rem;
  border-bottom: 1px solid #ddd;
  padding-bottom: 8px;
}

.details-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 12px 24px;
}

.detail-line {
  display: flex;
  margin-bottom: 10px;
  line-height: 1.5;
  font-size: 1rem;
  align-items: baseline;
  flex-wrap: nowrap;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.detail-line strong {
  font-weight: bold;
  width: 200px;
  flex-shrink: 0;
  margin-right: 10px;
  text-align: left;
}

.detail-line span {
  flex-grow: 1;
  min-width: 0;
  text-align: left;
  word-break: break-word;
  white-space: normal;
}

.detail-line.note-line {
  flex-direction: column;
  align-items: flex-start;
  white-space: normal;
}

.detail-line.note-line strong {
  width: auto;
  margin-bottom: 8px;
}

.note-value-span {
  display: block;
  width: 100%;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  background-color: #fff;
  white-space: pre-wrap;
  font-size: 0.95rem;
  color: #495057;
  box-sizing: border-box;
  overflow-x: auto;
}

.material-purchase-details-view.in-modal .detail-line {
  position: static;
  align-items: center;
}

.material-purchase-details-view.in-modal .detail-line::after {
  content: '';
  flex: 1 1 auto;
  border-bottom: 1px dotted #e9ecef;
  order: 1;
  margin: 0 8px;
}

.material-purchase-details-view.in-modal .detail-line strong {
  order: 0;
  background: transparent;
  padding: 0;
}

.material-purchase-details-view.in-modal .detail-line > span {
  order: 2;
  text-align: left;
  background: transparent;
  padding: 0;
  flex: 0 0 50%;
}

.material-purchase-details-view.in-modal .detail-line.note-line::after {
  display: none;
}

.actions-panel {
  display: flex;
  gap: 15px;
  margin-top: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.btn {
  padding: 10px 20px;
  border: 1px solid transparent;
  border-radius: 4px;
  cursor: pointer;
  font-size: 0.95rem;
  font-weight: 600;
  transition: background-color 0.2s ease, border-color 0.2s ease, color 0.2s ease;
  text-decoration: none;
  display: inline-block;
  text-align: center;
  box-sizing: border-box;
  white-space: nowrap;
  flex-shrink: 0;
}

.btn.primary-button {
  background-color: #007bff;
  color: white;
  border-color: #007bff;
}

.btn.primary-button:hover {
  background-color: #0056b3;
  border-color: #0056b3;
}

.btn.secondary-button {
  background-color: #6c757d;
  color: white;
  border-color: #6c757d;
}

.btn.secondary-button:hover {
  background-color: #5a6268;
  border-color: #545b62;
}

.status-message {
  padding: 16px;
  border-radius: 8px;
  margin: 20px auto;
  max-width: 960px;
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 1rem;
  font-weight: 500;
  box-sizing: border-box;
}

.loading-message {
  background-color: #e3f2fd;
  color: #1976d2;
}

.error-message {
  background-color: #ffebee;
  color: #d32f2f;
}

.no-results-message {
  background-color: #fff3cd;
  color: #856404;
  text-align: center;
  justify-content: center;
}

.loader {
  border: 3px solid #f3f3f3;
  border-top: 3px solid #3498db;
  border-radius: 50%;
  width: 20px;
  height: 20px;
  animation: spin 1s linear infinite;
  flex-shrink: 0;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message .error-icon {
  font-size: 1.5em;
  flex-shrink: 0;
}

.error-message .error-text {
  flex-grow: 1;
}

.error-message .close-error-button {
  background: none;
  border: none;
  color: inherit;
  font-size: 1.2em;
  cursor: pointer;
  margin-left: 10px;
  padding: 0 5px;
  flex-shrink: 0;
}

.status-badge {
  display: inline-block;
  padding: 3px 8px;
  border-radius: 12px;
  font-size: 0.8em;
  font-weight: bold;
  text-align: center;
  white-space: nowrap;
  vertical-align: middle;
}

.status-badge-not-received {
  background-color: #fff9c4;
  color: #fbc02d;
}

.status-badge-received {
  background-color: #c8e6c9;
  color: #388e3c;
}

.status-badge-cancelled {
  background-color: #ffcdd2;
  color: #c62828;
}

@media (max-width: 768px) {
  .material-purchase-details-view {
    padding: 15px;
    margin: 15px auto;
  }

  .material-purchase-details-view.in-modal {
    padding: 0;
  }

  .page-title {
    font-size: 20px;
    margin-bottom: 20px;
  }

  .details-section {
    padding: 12px;
  }

  .details-section h2 {
    font-size: 1.3rem;
    margin-bottom: 12px;
  }

  .detail-line {
    flex-direction: column;
    align-items: flex-start;
    margin-bottom: 8px;
    white-space: normal;
  }

  .detail-line strong {
    width: auto;
    margin-right: 0;
    margin-bottom: 4px;
  }

  .detail-line span {
    width: 100%;
    text-align: left;
  }

  .material-purchase-details-view.in-modal .detail-line::after {
    display: none;
  }

  .material-purchase-details-view.in-modal .detail-line > span {
    flex-basis: auto;
  }

  .note-value-span {
    padding: 8px;
    font-size: 0.9rem;
  }

  .actions-panel {
    flex-direction: column;
    align-items: stretch;
    gap: 10px;
  }

  .actions-panel .btn {
    width: 100%;
  }

  .status-message {
    padding: 12px;
    font-size: 0.95rem;
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}

@media (max-width: 480px) {
  .material-purchase-details-view {
    padding: 10px;
    margin: 10px auto;
  }

  .page-title {
    font-size: 18px;
    margin-bottom: 15px;
  }

  .details-section h2 {
    font-size: 1.2rem;
  }

  .details-section {
    padding: 10px;
  }

  .detail-line {
    font-size: 0.9rem;
    margin-bottom: 6px;
  }

  .btn {
    padding: 8px 15px;
    font-size: 0.9rem;
  }
}
</style>
