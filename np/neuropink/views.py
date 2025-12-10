from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import mail_admins
from django.http import JsonResponse
from django.utils.html import strip_tags

from .models import Order, Testimonials
from .forms import OrderForm, TestimonialForm

import random

BASE_CENA = 800
JEDNA_KUTIJA = 1000
DVE_KUTIJE = 1800
TRI_KUTIJE = 2400
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


def calculate_price(quantity):
    if quantity == 1:
        return JEDNA_KUTIJA
    elif quantity == 2:
        return DVE_KUTIJE
    elif quantity == 3:
        return TRI_KUTIJE
    return TRI_KUTIJE + BASE_CENA * (quantity - 3)


def order_view(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            quantity = max(1, form.cleaned_data['quantity'])
            total_price = calculate_price(quantity)

            order = form.save(commit=False)
            order.quantity = quantity
            order.total_price = total_price
            order.order_number = generate_order_number()
            order.save()
            mail_admins(subject='Narudzba', message='XXXXX narucio')
            return redirect('order_success', order_number=order.order_number)
    else:
        form = OrderForm()

    return render(request, 'order.html', {'form': form, 'BASE_CENA': BASE_CENA, 'JEDNA_KUTIJA': JEDNA_KUTIJA, 'DVE_KUTIJE': DVE_KUTIJE, 'TRI_KUTIJE': TRI_KUTIJE})


def order_success(request, order_number):
    return render(request, 'order_success.html', {'order_number': order_number})


def testimonial_success(request):
    return render(request, 'testimonial_success.html')

# TODO:
# Prebaciti na HTTPS
# smanjiti dugme za kupovinu na malim ekranima
# popraviti izgled cena na malim ekranima


# Done
# Prebaciti sliku u html
# Napraviti floating button za kupovinu
# Generisati testemoniale
# ne povecavati velicinu 'vasa recenzija' polja
# popraviti dodavanje prozivoda u korpu
# Dodati mogucnost ostavljanja recenzija (ispod ostalih) https://beliwmedia.com/kako-dodati-google-reviews-recenzije-u-sajt-uputstvo/
