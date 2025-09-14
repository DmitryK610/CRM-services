from django.utils.translation import gettext_lazy as _
from django.db import models

class OrderStatus(models.TextChoices):
    NEW = 'new', _('Новый')
    CALCULATION_CONFIRMED = 'calculation_confirmed', _('Расчет подтвержден')
    AWAITING_ADVANCE = 'awaiting_advance', _('Ожидает аванса')
    IN_PRODUCTION = 'in_production', _('В производстве')
    READY_FOR_INSTALLATION = 'ready_for_installation', _('Готов к установке')
    AWAITING_INSTALLATION = 'awaiting_installation', _('Ожидает установки')
    INSTALLATION = 'installation', _('Установка')
    COMPLETED = 'completed', _('Выполнен')
    CANCELLED = 'cancelled', _('Отменен')

class PaymentMethod(models.TextChoices):
    CASH = 'cash', _('Наличные')
    CARD = 'card', _('Банковская карта')
    BANK_TRANSFER = 'bank_transfer', _('Банковский перевод')
    ONLINE = 'online', _('Онлайн-платеж')
    CREDIT = 'credit', _('Кредит')
    INSTALLMENT = 'installment', _('Рассрочка')

class PaymentStatus(models.TextChoices):
    PENDING = 'pending', _('Ожидает подтверждения')
    COMPLETED = 'completed', _('Успешно завершен')
    FAILED = 'failed', _('Неудачный платеж')
    REFUNDED = 'refunded', _('Возврат средств')
    PARTIALLY_REFUNDED = 'partially_refunded', _('Частичный возврат')

class AdvancePaymentTypeChoices(models.TextChoices):
    CASH = 'cash', _('Наличные')
    CASHLESS = 'cashless', _('Безналичные')
