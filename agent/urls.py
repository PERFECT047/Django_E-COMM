from django.urls import conf, path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('become_agent/', views.become_agent, name='become_agent'),
    path('agent_admin/', views.agent_admin, name='agent_admin'),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('login/', views.agent_login_view, name='agent_login_view'),
    path('login_failed/', auth_views.LoginView.as_view(template_name='agent/login_NA.html'), name='login_failed'),

    path('activateitnowplease/<slug:uidb64>/<slug:token>/', views.activateitnowplease, name='activateitnowplease'),
    path('confirm_delivery/<slug:current_order_id>/', views.confirm_delivery, name='confirm_delivery'),
    path('verify_confirm_delivery/<slug:delivery_uidb64>/<slug:delivery_token>/<slug:current_order_id>/', views.verify_confirm_delivery, name='verify_confirm_delivery')
]