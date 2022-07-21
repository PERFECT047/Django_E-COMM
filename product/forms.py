from django import forms

class AddTOCart(forms.Form):
    quantity = forms.IntegerField()