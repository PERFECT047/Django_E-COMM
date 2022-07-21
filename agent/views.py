from vincenty import vincenty
import random

from django.shortcuts import render

from .models import Agent
from order.models import Order, OrderItem
from product.models import Product
from users.models import CustomUser
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render, redirect


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token, delivery_token
from django.contrib.auth.models import User


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template


from django.shortcuts import render

from seller.models import Seller

delivery_token_value = ""

def become_agent(request):
    global token_value
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_verified = False
            email = form.cleaned_data.get('email')
            address = form.cleaned_data.get('address')
            longitude = form.cleaned_data.get('longitude')
            latitude = form.cleaned_data.get('latitude')

            agent = Agent.objects.create(name=user.username, email=user.email, phone=user.phone, firstname=user.first_name, lastname=user.last_name, address=address, longitude=longitude, latitude=latitude, created_by=user)


            htmly = get_template('agent/acc_active_email.html')

            ans = {
                    'user':user,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user)
                }

            token_value = str(ans['token'])

            html_content = htmly.render(ans)

            subject, from_email, to = 'Welcome!', 'jayashsatolia403@gmail.com', email

            msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
            msg.attach_alternative(html_content, "text/html")
            msg.send()

            return render(request, 'agent/verify.html')

    else:
        form = UserRegisterForm()
    return render(request, 'users/become_user.html', {'form': form, 'title':'register here'})


def activateitnowplease(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token == token_value:
        user.is_verified = True
        user.is_agent = True
        user.save()
        login(request, user)
        return redirect('agent_admin')
    else:
        return HttpResponse('Activation link is invalid!')


def agent_login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_agent == True:
            login(request, user)

            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('agent_admin')
        else:
            return redirect('login_failed')
    
    return render(request, 'agent/login.html', {'form':form})

@login_required
def agent_admin(request):
    if request.user.is_agent:
        agent = request.user.agent
        if request.user.is_verified == True:
            products = Product.objects.all()
            orders = agent.orders.all()
            
            return render(request, 'agent/agent_admin.html', {'agent':agent, 'products':products, 'orders':orders})
        else:
            return render(request, 'agent/agent_admin_fail.html')
    else:
        return redirect('login_failed')

@login_required
def confirm_delivery(request, current_order_id):
    global delivery_token_value
    if request.user.is_agent:
        agent = request.user.agent
        orders = agent.orders.all()

        for i in orders:
            print(i.id)
            print(current_order_id)
            if str(i.id) == str(current_order_id):
                order = i
                break

        user = order.user
        email = user.email
        htmly = get_template('agent/verify_delivery.html')
        current_order_id = str(current_order_id)

        delivery_ans = {
                'user':user,
                'delivery_uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'delivery_token': delivery_token.make_token(user),
                'order_id': current_order_id
            }

        delivery_token_value = str(delivery_ans['delivery_token'])

        html_content = htmly.render(delivery_ans)

        subject, from_email, to = 'Welcome!', 'jayashsatolia403@gmail.com', email

        msg = EmailMultiAlternatives(subject, html_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

        return redirect('agent_admin')

def verify_confirm_delivery(request, delivery_uidb64, delivery_token, current_order_id):
    try:
        uid = force_text(urlsafe_base64_decode(delivery_uidb64))
        user = CustomUser.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and delivery_token == delivery_token_value:
        orders = user.orders.all()
        for i in orders:
            if str(i.id) == str(current_order_id):
                order = i
        order.is_user_verified = True
        order.is_delivered = True
        order.save()
        return HttpResponse('Thanks For Verification. Take your Order!')
    else:
        return HttpResponse('Activation link is invalid!')