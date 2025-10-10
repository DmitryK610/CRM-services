from django.contrib import admin

from .models import MaterialPurchase


@admin.register(MaterialPurchase)
class MaterialPurchaseAdmin(admin.ModelAdmin):
    list_display = (
        "material_id",
        "order_id",
        "quantity",
        "total_cost",
        "payment_method",
        "status",
        "purchase_order_date",
        "received_date",
        "created_at",
    )
    list_filter = (
        "payment_method",
        "status",
        "purchase_order_date",
        "received_date",
        "created_at",
    )
    search_fields = ("material_id", "order_id", "status")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-purchase_order_date", "-created_at")
