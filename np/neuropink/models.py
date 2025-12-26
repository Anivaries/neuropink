import uuid

from django.db import models
from django.utils import timezone


class Order(models.Model):
    completed_order_by_user = models.BooleanField(default=False)
    access_token = models.UUIDField(
        default=uuid.uuid4, editable=False, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.CharField(max_length=200)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=10)
    phone = models.CharField(max_length=20)
    email = models.EmailField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)
    quantity = models.IntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    order_number = models.IntegerField(unique=True)
    completed = models.BooleanField(default=False)
    poslato = models.BooleanField(default=False)

    def __str__(self):
        return f"Order #{self.id} - {self.first_name} {self.last_name}"


class Testimonials(models.Model):
    first_name = models.CharField(max_length=100, blank=True, null=True)
    last_name = models.CharField(max_length=100, blank=True, null=True)
    review = models.TextField(blank=False, null=False)
    approved = models.BooleanField(default=False)
    rating = models.PositiveSmallIntegerField(default=5)
    created_at = models.DateTimeField(default=timezone.now)
