from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import mail_admins
from django.http import JsonResponse

from .models import Order, Testimonials
from .forms import OrderForm, TestimonialForm

import random


UNIT_PRICE = 500
DELIVERY = 0


def load_more_testimonials(request):
    offset = int(request.GET.get("offset", 0))
    limit = 10

    data = Testimonials.objects.filter(approved=True).order_by('-created_at')[
        offset:offset + limit]

    testimonials_json = []
    for t in data:
        t_json = {
            "first_name": t.first_name,
            "last_name": t.last_name,
            "review": t.review,
            "rating": t.rating,
            "created_at": t.created_at,
        }

        testimonials_json.append(t_json)

    return JsonResponse({"testimonials": testimonials_json})


def index(request):
    if request.method == 'POST':
        form = TestimonialForm(request.POST)
        if form.is_valid():
            ime = form.cleaned_data['first_name']
            prezime = form.cleaned_data['last_name']
            review = form.cleaned_data['review']
            Testimonials.objects.create(
                first_name=ime,
                last_name=prezime,
                review=review
            )
            return render(request, 'testimonial_success.html')
    else:
        form = TestimonialForm()
        data = Testimonials.objects.filter(
            approved=True).order_by('-created_at')[:10]

        testimonials = [
            {
                "first_name": t.first_name,
                "review": t.review,
                "last_name": t.last_name,
                "rating": t.rating,
                "created_at": t.created_at,
            }
            for t in data
        ]

    return render(request, 'index.html', {'form': form, 'testimonials': testimonials})


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


def testimonial_success(request):
    return render(request, 'testimonial_success.html')

# TODO:
# Prebaciti na HTTPS
# smanjiti dugme za kupovinu na malim ekranima
# ne povecavati velicinu 'vasa recenzija' polja
# popraviti dodavanje prozivoda u korpu
# popraviti izgled cena na malim ekranima
# Dodati mogucnost ostavljanja recenzija (ispod ostalih) https://beliwmedia.com/kako-dodati-google-reviews-recenzije-u-sajt-uputstvo/

# Done
# Prebaciti sliku u html
# Napraviti floating button za kupovinu
# Generisati testemoniale
