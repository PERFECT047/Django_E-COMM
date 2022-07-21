"""ecom URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django import urls
from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from django.contrib.auth import views as auth_views
from django.conf.urls import url


urlpatterns = [
    # Api Urls 
    path('api-auth/', include('rest_framework.urls')),
    path('accounts_api/', include('users.api.urls')),
    path('product_api/', include('product.api.urls')),
    path('seller_api/', include('seller.api.urls')),

    # General Urls
    path('J@y@$h403/', admin.site.urls),
    path('accounts/', include('users.urls')),
    path('cart/', include('cart.urls')),
    path('agent/', include('agent.urls')),
    path('', include('core.urls')),
    path('seller/', include('seller.urls')),
    path('', include('product.urls')),

    # PassWord Change 
    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='change-password.html'), name='password_change'),
    url('password_change_done/', auth_views.PasswordChangeDoneView.as_view(template_name='change-password-done.html'), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='reset-password.html'), name='password_reset'),
    path('password_reset_done/', auth_views.PasswordResetDoneView.as_view(template_name='reset-password-done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_done/', auth_views.PasswordResetCompleteView.as_view(template_name='reset-password-done.html'), name='password_reset_complete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = 'Company Administration'