from users.models import CustomUser
from django.forms import ModelForm

from product.models import Product
from users.forms import UserRegisterationForm

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['category', 'image', 'title', 'description', 'price']
    
from django import forms

from django.contrib.auth.forms import AuthenticationForm



class UserRegisterForm(UserRegisterationForm):
	address = forms.CharField(max_length=255)
	longitude = forms.CharField(max_length=255)
	latitude = forms.CharField(max_length=255)
	class Meta:
		model = CustomUser
		fields = ['username', 'phone', 'first_name', 'last_name', 'email', 'address', 'longitude', 'latitude', 'password1', 'password2']




class LoginForm(AuthenticationForm):
	class Meta:
		model = CustomUser
		fields = ['username', 'password']