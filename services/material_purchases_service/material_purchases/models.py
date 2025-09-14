
from django.db import models
from django.utils.translation import gettext_lazy as _


from shared.enums import PaymentMethod

class MaterialPurchase(models.Model):
	material_id = models.IntegerField(_("ID материала"))
	order_id = models.IntegerField(_("ID клиентского заказа"), blank=True, null=True)
	quantity = models.DecimalField(_("Закупленное количество"), max_digits=10, decimal_places=3)
	total_cost = models.DecimalField(_("Общая стоимость закупки"), max_digits=12, decimal_places=2)
	payment_method = models.CharField(_("Способ оплаты поставщику"), max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.CASH)
	purchase_order_date = models.DateField(_("Дата заказа у поставщика"))
	status = models.CharField(_("Статус получения"), max_length=20)
	received_date = models.DateField(_("Дата получения от поставщика"), blank=True, null=True)
	notes = models.TextField(_("Примечание к закупке"), blank=True, null=True)
	created_at = models.DateTimeField(_("Дата создания записи"), auto_now_add=True)
	updated_at = models.DateTimeField(_("Дата обновления записи"), auto_now=True)

	def __str__(self):
		return f"{_('Закупка')} {self.material_id} ({self.quantity}) {_('от')} {self.purchase_order_date}"

	class Meta:
		verbose_name = _("Закупка материала")
		verbose_name_plural = _("Закупки материалов")
		ordering = ['-purchase_order_date', '-created_at']
