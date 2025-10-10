from django.contrib import admin

from .models import Calculation, CalculationItem


@admin.register(Calculation)
class CalculationAdmin(admin.ModelAdmin):
    list_display = ("name", "owner_id", "pricelist_id", "created_at")
    search_fields = ("name", "owner_id", "pricelist_id")
    list_filter = ("created_at",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


@admin.register(CalculationItem)
class CalculationItemAdmin(admin.ModelAdmin):
    list_display = ("calculation_id", "item_name", "unit", "quantity", "price", "total")
    search_fields = ("item_name", "calculation_id")
    list_filter = ("calculation_id",)
