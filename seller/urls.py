from django.contrib import auth
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('become_seller/', views.become_seller, name='become_seller'),
    path('seller_admin/', views.seller_admin, name='seller_admin'),
    path('add_product/', views.add_product, name='add_product'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', views.login_view, name='login_view'),
    path('login_failed/', auth_views.LoginView.as_view(template_name='seller/login_NA.html'), name='login_failed'),

    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate')
]