from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import mail_admins
from django.http import JsonResponse
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives
from django.conf import settings
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils import timezone

from .models import Order, OrderFifty, Testimonials
from .forms import OrderForm, OrderFiftyForm, TestimonialForm

import random

BASE_CENA_50 = 400
JEDNA_KUTIJA_50 = 500
DVE_KUTIJE_50 = 900
TRI_KUTIJE_50 = 1200

BASE_CENA = 700
JEDNA_KUTIJA = 900
DVE_KUTIJE = 1600
TRI_KUTIJE = 2100
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
            rating = form.cleaned_data['rating']
            Testimonials.objects.create(
                first_name=ime,
                last_name=prezime,
                review=review,
                rating=rating
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


def calculate_price_fifty(quantity):
    if quantity == 1:
        return JEDNA_KUTIJA_50
    elif quantity == 2:
        return DVE_KUTIJE_50
    elif quantity == 3:
        return TRI_KUTIJE_50
    return TRI_KUTIJE + BASE_CENA_50 * (quantity - 3)


def email_order(order):

    subject = 'Porudžbina'
    from_email = settings.SERVER_EMAIL
    to = [email for _, email in settings.ADMINS]

    order_first_name = order.first_name
    order_last_name = order.last_name
    order_address = order.address
    order_city = order.city
    order_postal_code = order.postal_code
    order_phone = order.phone
    order_email = order.email
    order_note = order.note
    order_quantity = order.quantity
    order_total_price = order.total_price
    order_created_at = order.created_at
    order_number = order.order_number
    text_body = f"""
    Ime i prezime: {order_first_name} {order_last_name}
    Telefon: {order_phone}
    """

    html_body = f"""
    <h2>Nova porudžbina — Neuropink</h2>

    <h3>Kupac</h3>
    <p>
    <strong>Ime i prezime:</strong> {order_first_name} {order_last_name}<br>
    <strong>Telefon:</strong> {order_phone}<br>
    <strong>Email:</strong> {order_email or '/'}
    </p>

    <h3>Adresa isporuke</h3>
    <p>
    {order_address}<br>
    {order_city} {order_postal_code}
    </p>

    <h3>Porudžbina</h3>
    <p>
    <strong>Količina:</strong> {order_quantity}<br>
    <strong>Cena ukupno:</strong> {order_total_price} RSD
    </p>

    <h3>Poruka kupca</h3>
    <p>
    {order_note or '/'}
    </p>

    <hr>

    <p style="font-size: 12px; color: #555;">
    <strong>Broj porudžbine:</strong> {order_number}<br>
    <strong>Kreirano:</strong> {order_created_at}
    </p>
    """

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=to,
    )
    email.attach_alternative(html_body, "text/html")
    email.send()

    # body = f"""
    #         NEUROPINK — NOVA PORUDŽBINA
    #         =========================

    #         Kupac
    #         -----
    #         Ime i prezime : {order_first_name} {order_last_name}
    #         Telefon: {order_phone}
    #         Email: {order_email or '/'}

    #         Adresa isporuke
    #         ---------------
    #         {order_address}
    #         {order_city} {order_postal_code}

    #         Porudžbina
    #         ----------
    #         Količina: {order_quantity}
    #         Cena ukupno: {order_total_price} RSD

    #         Poruka kupca
    #         ------------
    #         {order_note or '/'}

    #         Ostale informacije
    #         ------------------
    #         Broj porudžbine: {order_number}
    #         Kreirano: {order_created_at.strftime('%d.%m.%Y %H:%M')}
    #         """
    # mail_admins(subject='Porudzbina', message=body, )


def email_order_fifty(order):

    subject = 'Porudžbina od 50g - NIJE AKTIVNA PORUDZBINA'
    from_email = settings.SERVER_EMAIL
    to = [email for _, email in settings.ADMINS]

    order_first_name = order.first_name
    order_last_name = order.last_name
    order_address = order.address
    order_city = order.city
    order_postal_code = order.postal_code
    order_phone = order.phone
    order_email = order.email
    order_note = order.note
    order_quantity = order.quantity
    order_total_price = order.total_price
    order_created_at = order.created_at
    order_number = order.order_number
    text_body = f"""
    Ime i prezime: {order_first_name} {order_last_name}
    Telefon: {order_phone}
    """

    html_body = f"""
    <h2>OVO JE PORUDZBINA OD 50 GRAMA. NIJE AKTIVNA PORUDZBINA, SAMO ZA SAKUPLJANJE PODATAKA</h2>

    <h3>Kupac</h3>
    <p>
    <strong>Ime i prezime:</strong> {order_first_name} {order_last_name}<br>
    <strong>Telefon:</strong> {order_phone}<br>
    <strong>Email:</strong> {order_email or '/'}
    </p>

    <h3>Adresa isporuke</h3>
    <p>
    {order_address}<br>
    {order_city} {order_postal_code}
    </p>

    <h3>Porudžbina</h3>
    <p>
    <strong>Količina:</strong> {order_quantity}<br>
    <strong>Cena ukupno:</strong> {order_total_price} RSD
    </p>

    <h3>Poruka kupca</h3>
    <p>
    {order_note or '/'}
    </p>

    <hr>

    <p style="font-size: 12px; color: #555;">
    <strong>Broj porudžbine:</strong> {order_number}<br>
    <strong>Kreirano:</strong> {order_created_at}
    </p>
    """

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_body,
        from_email=from_email,
        to=to,
    )
    email.attach_alternative(html_body, "text/html")
    email.send()


def email_customer(order):
    subject = 'Hvala na porudžbini!'
    html_content = render_to_string('emails/order_confirmation.html', {
        'first_name': order.first_name,
        'last_name': order.last_name,
        'email': order.email,
        'phone': order.phone,
        'address': order.address,
        'city': order.city,
        'postal_code': order.postal_code,
        'quantity': order.quantity,
        'total_price': order.total_price,
        'order_number': order.order_number,
        'note': order.note,
        'created_at': order.created_at.strftime('%d.%m.%Y %H:%M'),
        'current_year': timezone.now().year
    })
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject, text_content, 'noreply@neuropink.rs', [order.email])
    email.attach_alternative(html_content, "text/html")
    email.send()


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
            order.completed_order_by_user = True
            order.save()
            email_order(order)
            # if order.email:
            #     email_customer(order)
            return redirect('order_success', token=order.access_token)
    else:
        form = OrderForm()

    return render(request, 'order.html', {'form': form, 'BASE_CENA': BASE_CENA, 'JEDNA_KUTIJA': JEDNA_KUTIJA, 'DVE_KUTIJE': DVE_KUTIJE, 'TRI_KUTIJE': TRI_KUTIJE})


def order_view_fifty_grams(request):
    if request.method == 'POST':
        form = OrderFiftyForm(request.POST)
        if form.is_valid():
            quantity = max(1, form.cleaned_data['quantity'])
            total_price = calculate_price_fifty(quantity)

            order = form.save(commit=False)
            order.quantity = quantity
            order.total_price = total_price
            order.order_number = generate_order_number()
            order.completed_order_by_user = True
            order.save()
            email_order_fifty(order)
            # if order.email:
            #     email_customer(order)
            return JsonResponse({
                "success": True,
                "message": "Ovaj artikal trenutno nije na stanju!",
            })
    else:
        form = OrderFiftyForm()

    return render(request, 'order_fifty.html', {'form': form, 'BASE_CENA': BASE_CENA_50, 'JEDNA_KUTIJA': JEDNA_KUTIJA_50, 'DVE_KUTIJE': DVE_KUTIJE_50, 'TRI_KUTIJE': TRI_KUTIJE_50})


def order_success(request, token):
    try:
        order = Order.objects.get(access_token=token)
    except Order.DoesNotExist:
        return redirect("/")

    if not order.completed_order_by_user:
        return redirect("/")

    return render(request, 'order_success.html', {'order_number': order.order_number})


def testimonial_success(request):
    return render(request, 'testimonial_success.html')

# TODO:

# smanjiti dugme za kupovinu na malim ekranima
# popraviti izgled cena na malim ekranima


# Done
# Prebaciti sliku u html
# Napraviti floating button za kupovinu
# Generisati testemoniale
# ne povecavati velicinu 'vasa recenzija' polja
# popraviti dodavanje prozivoda u korpu
# Dodati mogucnost ostavljanja recenzija (ispod ostalih) https://beliwmedia.com/kako-dodati-google-reviews-recenzije-u-sajt-uputstvo/
# Prebaciti na HTTPS
