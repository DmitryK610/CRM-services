from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
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

class UserManager(BaseUserManager):
	use_in_migrations = True

	def _create_user(self, username, email, password, **extra_fields):
		if not username:
			raise ValueError("Username must be provided")
		email = self.normalize_email(email)
		user = self.model(username=username, email=email, **extra_fields)
		if password:
			user.set_password(password)
		else:
			user.set_unusable_password()
		user.save(using=self._db)
		return user

	def create_user(self, username, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', False)
		extra_fields.setdefault('is_superuser', False)
		return self._create_user(username, email, password, **extra_fields)

	def create_superuser(self, username, email=None, password=None, **extra_fields):
		extra_fields.setdefault('is_staff', True)
		extra_fields.setdefault('is_superuser', True)

		if extra_fields.get('is_staff') is not True:
			raise ValueError('Superuser must have is_staff=True.')
		if extra_fields.get('is_superuser') is not True:
			raise ValueError('Superuser must have is_superuser=True.')

		return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
	username = models.CharField(_("Username"), max_length=150, unique=True)
	full_name = models.CharField(_("Full Name"), max_length=255)
	email = models.EmailField(_("Email"), unique=True, blank=True, null=True)
	phone = models.CharField(_("Phone"), max_length=50, blank=True, null=True)
	role = models.ForeignKey(Role, on_delete=models.SET_NULL, blank=True, null=True, related_name='users', verbose_name=_("Role"))
	permissions = models.ManyToManyField(Permission, blank=True, related_name='users', verbose_name=_("Permissions"))
	is_active = models.BooleanField(_("Is Active"), default=True)
	is_staff = models.BooleanField(_("Is Staff"), default=False)
	registered_at = models.DateTimeField(_("Registered At"), default=timezone.now)

	objects = UserManager()

	EMAIL_FIELD = 'email'
	USERNAME_FIELD = 'username'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return self.full_name or self.username

	class Meta:
		verbose_name = _("Пользователь")
		verbose_name_plural = _("Пользователи")

	def save(self, *args, **kwargs):
		is_new = self.pk is None
		if not self.registered_at:
			self.registered_at = timezone.now()
		super().save(*args, **kwargs)
		if is_new:
			self.send_user_created_event()

	def send_user_created_event(self):
		role_name = self.role.name if self.role else None
		connection = None
		try:
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
		except Exception:
			pass
		finally:
			if connection:
				try:
					connection.close()
				except Exception:
					pass
