from django.contrib import admin

from .models import Order, OrderItem, Payment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "client_id",
        "status",
        "order_date",
        "installation_date",
        "total_amount",
        "created_at",
    )
    list_filter = ("status", "order_date", "installation_date", "created_at")
    search_fields = ("order_number", "client_id", "calculation_id", "note")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-order_date", "-created_at")


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ("order_id", "product_name", "quantity", "unit_price", "total_price")
    search_fields = ("product_name", "order_id")
    list_filter = ("order_id",)


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("order_id", "amount", "payment_date", "payment_method", "status", "created_at")
    list_filter = ("status", "payment_method", "payment_date", "created_at")
    search_fields = ("order_id", "transaction_id")
    readonly_fields = ("created_at", "updated_at")
    ordering = ("-payment_date", "-created_at")
