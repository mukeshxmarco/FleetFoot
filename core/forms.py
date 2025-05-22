from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from .utils import CITIES_LIST

PAYMENT_CHOICES = (
    ('C', 'Cash on Delivery'),
)


class CheckoutForm(forms.Form):
    street_address = forms.CharField(
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your street address'
        })
    )
    apartment_address = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter apartment, suite, unit, etc.'
        })
    )
    city = forms.ChoiceField(
        choices=[(c['value'], c['label']) for c in CITIES_LIST], 
        required=True,
        widget=forms.Select(attrs={
            'class': 'form-control'
        })
    )
    zip = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter postal code'
        })
    )
    payment_option = forms.ChoiceField(
        widget=forms.RadioSelect, 
        choices=PAYMENT_CHOICES
    )


class CouponForm(forms.Form):
    code = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Promo code'
    }))


class RefundForm(forms.Form):
    ref_code = forms.CharField()
    message = forms.CharField(widget=forms.Textarea(attrs={
        'rows': 4
    }))
    email = forms.EmailField()
