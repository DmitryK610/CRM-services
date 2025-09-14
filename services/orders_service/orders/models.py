from django.db import models
from django.utils.translation import gettext_lazy as _
from shared.enums import OrderStatus, PaymentMethod, PaymentStatus, AdvancePaymentTypeChoices
import pika
import json

class Order(models.Model):
	client_id = models.IntegerField(_("Client ID"), db_column='id_клиент')
	calculation_id = models.IntegerField(_("Calculation ID"), blank=True, null=True, db_column='id_расчета')
	total_amount = models.DecimalField(_("Total Amount"), max_digits=12, decimal_places=2, db_column='сумма_заказа')
	material_id = models.IntegerField(_("Material ID"), db_column='id_материал')
	employee_id = models.IntegerField(_("Employee ID"), blank=True, null=True, db_column='id_сотрудника')
	material_quantity = models.DecimalField(_("Material Quantity"), max_digits=10, decimal_places=3, default=0.0, db_column='количество_материала')
	status = models.CharField(_("Status"), max_length=50, choices=OrderStatus.choices, default=OrderStatus.NEW, db_column='статус_заказа')
	advance_payment_amount = models.DecimalField(_("Advance Payment Amount"), max_digits=12, decimal_places=2, blank=True, null=True, db_column='сумма_аванса')
	advance_payment_date = models.DateTimeField(_("Advance Payment Date"), blank=True, null=True, db_column='дата_внесения_аванса')
	installation_date = models.DateTimeField(_("Installation Date"), blank=True, null=True, db_column='дата_установки')
	needs_installation = models.BooleanField(_("Needs Installation"), default=False, db_column='установка')
	needs_delivery = models.BooleanField(_("Needs Delivery"), default=False, db_column='доставка')
	order_number = models.CharField(_("Order Number"), max_length=50, unique=True, blank=True, null=True, db_column='orderNumber')
	created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
	updated_at = models.DateTimeField(_("Updated At"), auto_now=True)
	order_date = models.DateField(_("Order Date"), db_column='дата_заказа')
	note = models.TextField(_("Note"), blank=True, null=True, db_column='примечание')
	advance_payment_type = models.CharField(_("Advance Payment Type"), max_length=50, choices=AdvancePaymentTypeChoices.choices, blank=True, null=True)

	def save(self, *args, **kwargs):
		is_new = self.pk is None
		super().save(*args, **kwargs)
		if is_new:
			self.send_order_created_event()

	def send_order_created_event(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
		channel = connection.channel()
		channel.queue_declare(queue='order_created')
		event = {
			'order_id': self.id,
			'client_id': self.client_id,
			'total_amount': str(self.total_amount),
			'order_date': str(self.order_date)
		}
		channel.basic_publish(
			exchange='',
			routing_key='order_created',
			body=json.dumps(event)
		)
		connection.close()

	def __str__(self):
		return f"{_('Order')} №{self.order_number or self.id} {_('from')} {self.order_date}"

	class Meta:
		verbose_name = _("Заказ")
		verbose_name_plural = _("Заказы")
		ordering = ['-order_date', '-created_at']

class OrderItem(models.Model):
	order_id = models.IntegerField(_("Order ID"))
	product_name = models.CharField(_("Product Name"), max_length=255)
	quantity = models.DecimalField(_("Quantity"), max_digits=10, decimal_places=3)
	unit_price = models.DecimalField(_("Unit Price"), max_digits=10, decimal_places=2)
	total_price = models.DecimalField(_("Total Price"), max_digits=12, decimal_places=2)

	def save(self, *args, **kwargs):
		if self.quantity is not None and self.unit_price is not None:
			self.total_price = self.quantity * self.unit_price
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.product_name} (x{self.quantity}) {_('for order')} {self.order_id}"

	class Meta:
		verbose_name = _("Позиция в заказе")
		verbose_name_plural = _("Позиции в заказе")

class Payment(models.Model):
	order_id = models.IntegerField(_("Order ID"))
	amount = models.DecimalField(_("Amount"), max_digits=12, decimal_places=2)
	payment_date = models.DateField(_("Payment Date"))
	payment_method = models.CharField(_("Payment Method"), max_length=20, choices=PaymentMethod.choices)
	status = models.CharField(_("Status"), max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
	transaction_id = models.CharField(_("Transaction ID"), max_length=255, blank=True, null=True)
	notes = models.TextField(_("Notes"), blank=True, null=True)
	created_by_id = models.IntegerField(_("Created By"), blank=True, null=True)
	created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
	updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

	def __str__(self):
		return f"{_('Payment')} {self.id} {_('amount')} {self.amount} {_('for order')} {self.order_id}"

	class Meta:
		verbose_name = _("Платеж")
		verbose_name_plural = _("Платежи")
		ordering = ['-payment_date', '-created_at']
