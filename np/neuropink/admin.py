from django.contrib import admin

from .models import Order, Testimonials


@admin.register(Testimonials)
class TestimonialsAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name',
                    'approved', 'rating', 'created_at')
    list_filter = ('approved', 'rating', 'created_at')
    search_fields = ('first_name', 'last_name',
                     'review')
    ordering = ('-created_at',)


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
