from django.contrib import admin

from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'first_name',
        'last_name',
        'city',
        'postal_code',
        'phone',
        'quantity',
        'total_price',
        'created_at',
    )
    list_filter = ('city', 'created_at')
    search_fields = ('order_number', 'first_name',
                     'last_name', 'phone', 'email')
    readonly_fields = ('order_number', 'total_price', 'created_at')

    fieldsets = (
        ("Order Information", {
            "fields": ("order_number", "created_at")
        }),
        ("Customer Details", {
            "fields": ("first_name", "last_name", "phone", "email")
        }),
        ("Address", {
            "fields": ("address", "city", "postal_code")
        }),
        ("Order Details", {
            "fields": ("quantity", "total_price", "note")
        }),
    )
