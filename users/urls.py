from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('signup/', views.become_user, name='become_user'),
    path('activateitnow/<slug:uidb64>/<slug:token>/', views.activateitnow, name='activateitnow'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', views.user_login_views, name='user_login_views'),
    path('login_failed/', auth_views.LoginView.as_view(template_name='users/login_NA.html'), name='user_login_failed'),
    path('profile/', views.profile_view, name='profile_view'),
    path('<slug:order_id>/askForRefund/', views.askForRefund, name='askForRefund')
]