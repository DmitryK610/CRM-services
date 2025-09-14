from django.db import models
from django.utils.translation import gettext_lazy as _
import pika
import json

class Pricelist(models.Model):
	owner_id = models.IntegerField(_("Owner ID"))  # id пользователя или компании
	name = models.CharField(_("Pricelist Name"), max_length=255)
	created_at = models.DateTimeField(_("Created At"), auto_now_add=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("Прайс-лист")
		verbose_name_plural = _("Прайс-листы")

class PricelistItem(models.Model):
	pricelist_id = models.IntegerField(_("Pricelist ID"))
	item_name = models.CharField(_("Item Name"), max_length=255)
	unit = models.CharField(_("Unit"), max_length=50)
	price = models.DecimalField(_("Price"), max_digits=12, decimal_places=2)
	description = models.TextField(_("Description"), blank=True, null=True)

	def __str__(self):
		return f"{self.item_name} ({self.unit})"

	class Meta:
		verbose_name = _("Позиция прайс-листа")
		verbose_name_plural = _("Позиции прайс-листа")

# Запускать этот обработчик как отдельный процесс/скрипт

def create_pricelist_for_admin():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='user_created')

    def callback(ch, method, properties, body):
        event = json.loads(body)
        user_id = event.get('user_id')
        role_name = event.get('role_name')  # предполагается, что роль передаётся в событии
        if role_name == 'admin':
            from .models import Pricelist
            if not Pricelist.objects.filter(owner_id=user_id).exists():
                Pricelist.objects.create(owner_id=user_id, name=f"Default pricelist for user {user_id}")
                print(f"Pricelist created for admin user {user_id}")
            else:
                print(f"Pricelist already exists for user {user_id}")
        else:
            print(f"User {user_id} is not admin, pricelist not created.")

    channel.basic_consume(queue='user_created', on_message_callback=callback, auto_ack=True)
    print('Waiting for user_created events...')
    channel.start_consuming()

# Пример обработчика события изменения прайс-листа

def handle_pricelist_updated():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='pricelist_updated')

    def callback(ch, method, properties, body):
        event = json.loads(body)
        print(f"Pricelist updated: {event}")
        # Здесь можно обновить связанные расчёты или уведомить другие сервисы

    channel.basic_consume(queue='pricelist_updated', on_message_callback=callback, auto_ack=True)
    print('Waiting for pricelist_updated events...')
    channel.start_consuming()
