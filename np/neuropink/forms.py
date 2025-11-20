# forms.py
from django import forms


class OrderForm(forms.Form):
    first_name = forms.CharField(
        max_length=100,
        label='Ime',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    last_name = forms.CharField(
        max_length=100,
        label='Prezime',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    address = forms.CharField(
        max_length=200,
        label='Adresa',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Ulica i broj'})
    )
    city = forms.CharField(
        max_length=100,
        label='Grad',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    postal_code = forms.CharField(
        max_length=10,
        label='Poštanski broj',
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    phone = forms.CharField(
        max_length=20,
        label='Broj telefona',
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': '+381 60 123 4567'})
    )
    email = forms.EmailField(
        required=False,
        label='Email adresa',
        widget=forms.EmailInput(
            attrs={'class': 'form-control', 'placeholder': 'vas.email@example.com'})
    )
    note = forms.CharField(
        required=False,
        label='Napomena',
        widget=forms.Textarea(
            attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Dodatne informacije...'})
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        label='Količina',
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
