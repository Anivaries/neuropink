# forms.py
from django import forms

from .models import Testimonials, Order


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'address', 'city',
            'postal_code', 'phone', 'email', 'note', 'quantity'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ulica i broj'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+381 60 123 4567'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'vas.email@example.com'}),
            'note': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dodatne informacije...'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonials
        fields = ['first_name', 'last_name', 'review']
        labels = {
            'first_name': 'Ime',
            'last_name': 'Prezime',
            'review': 'Vaša recenzija',
        }
