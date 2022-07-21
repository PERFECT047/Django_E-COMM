from django.forms.models import model_to_dict
from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm



class UserRegisterationForm(UserCreationForm):
    email = forms.EmailField()
    phone = forms.CharField(max_length=255)
    first_name = forms.CharField(max_length = 20)
    last_name = forms.CharField(max_length = 20)
    class Meta:
        model = CustomUser
        fields = ['username', 'phone', 'first_name', 'last_name', 'email', 'password1', 'password2']


class LoginForm(AuthenticationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'password']