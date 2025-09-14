from django.db import models
import pika
import json

class AuditLog(models.Model):
	user = models.CharField(max_length=255, null=True, blank=True, help_text="Пользователь, совершивший действие")
	action = models.CharField(max_length=255, help_text="Тип действия")
	object_type = models.CharField(max_length=255, null=True, blank=True, help_text="Тип объекта")
	object_id = models.CharField(max_length=255, null=True, blank=True, help_text="ID объекта")
	timestamp = models.DateTimeField(auto_now_add=True, help_text="Время события")
	details = models.JSONField(null=True, blank=True, help_text="Дополнительные данные")

	def __str__(self):
		return f"{self.timestamp}: {self.user} - {self.action} ({self.object_type}:{self.object_id})"

# Запускать этот обработчик как отдельный процесс/скрипт

def audit_order_created():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='order_created')

    def callback(ch, method, properties, body):
        event = json.loads(body)
        from .models import AuditLog
        AuditLog.objects.create(
            user=str(event.get('client_id')),
            action='order_created',
            object_type='Order',
            object_id=str(event.get('order_id')),
            details=event
        )
        print(f"Audit log created for order {event.get('order_id')}")

    channel.basic_consume(queue='order_created', on_message_callback=callback, auto_ack=True)
    print('Waiting for order_created events...')
    channel.start_consuming()
