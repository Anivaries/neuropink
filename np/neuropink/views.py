from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import mail_admins

from .models import Order
from .forms import OrderForm

import random


UNIT_PRICE = 500
DELIVERY = 0


def index(request):
    return render(request, 'index.html')


def generate_order_number():
    while True:
        number = random.randint(100000, 999999)
        if not Order.objects.filter(order_number=number).exists():
            return number


def order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = max(1, form.cleaned_data['quantity'])
            total_price = quantity * UNIT_PRICE + DELIVERY
            order = Order(
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                address=form.cleaned_data['address'],
                city=form.cleaned_data['city'],
                postal_code=form.cleaned_data['postal_code'],
                phone=form.cleaned_data['phone'],
                email=form.cleaned_data['email'],
                note=form.cleaned_data['note'],
                quantity=quantity,
                total_price=total_price,
                order_number=generate_order_number(),
            )
            order.save()
            mail_admins(subject='Narudzba', message='XXXXX narucio')
            return redirect('order_success', order_number=order.order_number)
    else:
        form = OrderForm()

    return render(request, 'order.html', {'form': form})


def order_success(request, order_number):
    return render(request, 'order_success.html', {'order_number': order_number})
