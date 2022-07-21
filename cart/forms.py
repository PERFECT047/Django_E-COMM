from django import forms

class CheckoutForm(forms.Form):
    address = forms.CharField(max_length=255)
    zipcode = forms.CharField(max_length=255)
    place = forms.CharField(max_length=255)
    longitude = forms.CharField(max_length=100)
    latitude = forms.CharField(max_length=100)