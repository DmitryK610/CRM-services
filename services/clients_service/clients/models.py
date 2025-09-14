
from django.db import models
from django.utils.translation import gettext_lazy as _

class Client(models.Model):
	full_name = models.CharField(_("Full Name"), max_length=255, db_column='ФИО')
	contact_phone = models.CharField(_("Contact Phone"), max_length=50, db_column='Контактный телефон')
	email = models.EmailField(_("Email"), db_column='электронная почта')
	address = models.TextField(_("Address"), db_column='адрес')
	note = models.TextField(_("Note"), blank=True, null=True, db_column='примечание')
	created_at = models.DateTimeField(_("Created At"), auto_now_add=True, blank=True, null=True)
	updated_at = models.DateTimeField(_("Updated At"), auto_now=True, blank=True, null=True)

	def __str__(self):
		return self.full_name

	class Meta:
		verbose_name = _("Клиент")
		verbose_name_plural = _("Клиенты")
