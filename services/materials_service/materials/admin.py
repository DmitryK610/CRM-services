from django.contrib import admin

from .models import Material, Supplier


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
	list_display = ("material_name", "color_code", "supplier_id", "cost", "created_at")
	list_filter = ("created_at",)
	search_fields = ("material_name", "color_code")
	readonly_fields = ("created_at",)
	ordering = ("-created_at",)
	fieldsets = (
		(None, {
			"fields": ("material_name", "color_code", "supplier_id", "cost", "note", "image_url"),
		}),
		("System", {
			"fields": ("created_at",),
			"classes": ("collapse",),
		}),
	)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
	list_display = ("company_name", "contact_person", "email", "phone", "created_at")
	list_filter = ("created_at",)
	search_fields = ("company_name", "contact_person", "email", "phone")
	readonly_fields = ("created_at",)
	ordering = ("-created_at",)
	fieldsets = (
		(None, {
			"fields": ("company_name", "contact_person", "email", "phone", "supplier_address", "note"),
		}),
		("System", {
			"fields": ("created_at",),
			"classes": ("collapse",),
		}),
	)
