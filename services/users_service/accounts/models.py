from django.db import models
from django.utils.translation import gettext_lazy as _
import pika
import json

class Role(models.Model):
	name = models.CharField(_("Role Name"), max_length=50, unique=True)
	description = models.TextField(_("Description"), blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("Роль")
		verbose_name_plural = _("Роли")

class Permission(models.Model):
	code = models.CharField(_("Permission Code"), max_length=100, unique=True)
	name = models.CharField(_("Permission Name"), max_length=100)
	description = models.TextField(_("Description"), blank=True, null=True)

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = _("Право доступа")
		verbose_name_plural = _("Права доступа")

class User(models.Model):
	full_name = models.CharField(_("Full Name"), max_length=255)
	email = models.EmailField(_("Email"), unique=True)
	phone = models.CharField(_("Phone"), max_length=50, blank=True, null=True)
	password_hash = models.CharField(_("Password Hash"), max_length=255)
	role_id = models.IntegerField(_("Role ID"), blank=True, null=True)
	permission_ids = models.JSONField(_("Permission IDs"), default=list, blank=True)
	is_active = models.BooleanField(_("Is Active"), default=True)
	is_superuser = models.BooleanField(_("Is Superuser"), default=False)
	registered_at = models.DateTimeField(_("Registered At"), auto_now_add=True)
	last_login = models.DateTimeField(_("Last Login"), blank=True, null=True)

	def __str__(self):
		return self.full_name

	class Meta:
		verbose_name = _("Пользователь")
		verbose_name_plural = _("Пользователи")

	def save(self, *args, **kwargs):
		is_new = self.pk is None
		super().save(*args, **kwargs)
		if is_new:
			self.send_user_created_event()

	def send_user_created_event(self):
		# Получаем имя роли пользователя
		role_name = None
		if self.role_id:
			try:
				role = Role.objects.get(id=self.role_id)
				role_name = role.name
			except Role.DoesNotExist:
				role_name = None
		connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))  # host из docker-compose
		channel = connection.channel()
		channel.queue_declare(queue='user_created')
		event = {
			'user_id': self.id,
			'email': self.email,
			'full_name': self.full_name,
			'role_name': role_name
		}
		channel.basic_publish(
			exchange='',
			routing_key='user_created',
			body=json.dumps(event)
		)
		connection.close()
