from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ("full_name", "contact_phone", "email", "created_at", "updated_at")
    search_fields = ("full_name", "contact_phone", "email")
    list_filter = ("created_at", "updated_at")
    readonly_fields = ("created_at", "updated_at")
