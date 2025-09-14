from django.db import models
from django.utils.translation import gettext_lazy as _
import pika
import json

class Calculation(models.Model):
	owner_id = models.IntegerField(_("Owner ID"))  # id пользователя или компании
	pricelist_id = models.IntegerField(_("Pricelist ID"))
	name = models.CharField(_("Calculation Name"), max_length=255)
	created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("Расчет")
		verbose_name_plural = _("Расчеты")

	def save(self, *args, **kwargs):
		is_new = self.pk is None
		super().save(*args, **kwargs)
		if is_new:
			self.send_calculation_requested_event()

	def send_calculation_requested_event(self):
		connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
		channel = connection.channel()
		channel.queue_declare(queue='calculation_requested')
		event = {
			'calculation_id': self.id,
			'owner_id': self.owner_id,
			'pricelist_id': self.pricelist_id
		}
		channel.basic_publish(
			exchange='',
			routing_key='calculation_requested',
			body=json.dumps(event)
		)
		connection.close()

class CalculationItem(models.Model):
	calculation_id = models.IntegerField(_("Calculation ID"))
	item_name = models.CharField(_("Item Name"), max_length=255)
	unit = models.CharField(_("Unit"), max_length=50)
	quantity = models.DecimalField(_("Quantity"), max_digits=10, decimal_places=3)
	price = models.DecimalField(_("Price"), max_digits=12, decimal_places=2)
	total = models.DecimalField(_("Total"), max_digits=14, decimal_places=2)
	description = models.TextField(_("Description"), blank=True, null=True)

	def save(self, *args, **kwargs):
		self.total = self.quantity * self.price
		super().save(*args, **kwargs)

	def __str__(self):
		return f"{self.item_name} ({self.unit})"

	class Meta:
		verbose_name = _("Позиция расчета")
		verbose_name_plural = _("Позиции расчета")

# Пример обработчика результата (может быть в другом сервисе)
def handle_calculation_result():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='calculation_result')

    def callback(ch, method, properties, body):
        event = json.loads(body)
        print(f"Calculation result received: {event}")
        # Здесь можно обновить Calculation или отправить уведомление

    channel.basic_consume(queue='calculation_result', on_message_callback=callback, auto_ack=True)
    print('Waiting for calculation_result events...')
    channel.start_consuming()
