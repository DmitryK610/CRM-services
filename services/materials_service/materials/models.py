class Supplier(models.Model):
	company_name = models.CharField(_("Company Name"), max_length=255, db_column='названиеКомпании')
	contact_person = models.CharField(_("Contact Person"), max_length=255, db_column='контактноеЛицо')
	email = models.EmailField(_("Email"), db_column='электроннаяПочта')
	supplier_address = models.TextField(_("Supplier Address"), db_column='адресПоставщика')
	phone = models.CharField(_("Phone"), max_length=50, db_column='телефон')
	created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
	note = models.TextField(_("Note"), blank=True, null=True, db_column='примечание')

	def __str__(self):
		return self.company_name

	class Meta:
		verbose_name = _("Поставщик")
		verbose_name_plural = _("Поставщики")

from django.db import models
from django.utils.translation import gettext_lazy as _

class Material(models.Model):
	material_name = models.CharField(_("Material Name"), max_length=255, db_column='названиеМатериала')
	color_code = models.CharField(_("Color Code"), max_length=100, db_column='артикулЦвета')
	supplier_id = models.IntegerField(_("Supplier ID"), db_column='поставщик')
	cost = models.DecimalField(_("Cost per Unit"), max_digits=10, decimal_places=2, db_column='стоимостьЗаЕдиницу')
	note = models.TextField(_("Description"), blank=True, null=True, db_column='описание')
	created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
	image_url = models.URLField(_("Image URL"), max_length=500, blank=True, null=True)

	def __str__(self):
		return f"{self.material_name} ({self.color_code})"

	class Meta:
		verbose_name = _("Камень")
		verbose_name_plural = _("Камни")
