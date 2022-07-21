from vincenty import vincenty

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.utils.text import slugify
from django.shortcuts import redirect, render


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token

from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from .models import Seller
from product.models import Product
from agent.models import Agent
from users.models import CustomUser
from order.models import Order, OrderItem

from .forms import ProductForm

i = 000000
token_value = ""



def become_seller(request):
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

            seller = Seller.objects.create(name=user.username, email=user.email, phone=user.phone, firstname=user.first_name, lastname=user.last_name, address=address, longitude=longitude, latitude=latitude, created_by=user)
            #Email 
            current_site = get_current_site(request)
            htmly = get_template('seller/acc_active_email.html')

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
            #

            return render(request, 'seller/verify.html')

    else:
        form = UserRegisterForm()
    return render(request, 'seller/become_seller.html', {'form': form, 'title':'register here'})


def activate(request, uidb64, token):
    global token_value
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None

    if user is not None and token == token_value:
        user.is_verified = True
        user.is_seller = True
        user.save()
        login(request, user)
        return redirect('seller_admin')
    else:
        return HttpResponse('Activation link is invalid!')


def login_view(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_seller == True:
            login(request, user)

            if request.GET.get('next'):
                return redirect(request.GET.get('next'))
            else:
                return redirect('seller_admin')
        else:
            return redirect('login_failed')
    
    return render(request, 'seller/login.html', {'form':form})


@login_required
def seller_admin(request):
    if request.user.is_seller:
        seller = request.user.seller
        if request.user.is_verified == True:
            products = seller.products.all()
            orders = seller.orders.all()

            for order in orders:
                order.seller_amount = 0
                order.seller_paid_amount = 0
                order.fully_paid = True

                for item in order.items.all():
                    if item.seller == request.user.seller:
                        if item.seller_paid:
                            order.seller_paid_amount += item.get_total_price()
                        else:
                            order.seller_amount += item.get_total_price()
                            order.fully_paid = False
            
            return render(request, 'seller/seller_admin.html', {'seller':seller, 'products':products, 'orders':orders})
        else:
            return render(request, 'seller/seller_admin_fail.html')
    else:
        return redirect('login_failed')

@login_required
def add_product(request):
    if request.user.is_seller:
        x = request.user.seller
        if request.user.is_verified == True:
            global i
            if request.method == 'POST':
                form = ProductForm(request.POST, request.FILES)

                if form.is_valid():
                    product = form.save(commit=False)
                    product.seller = request.user.seller
                    product.slug = slugify(product.title + str(i))
                    i+=1
                    print(product.slug)
                    product.save()

                    return redirect('seller_admin')
            else:
                form = ProductForm()
        else:
            return render(request, 'seller/add_product_fail.html')
    else:
        return render(request, 'seller/login_NA.html')
    
    return render(request, 'seller/add_product.html', {'form':form})