import vincenty

from agent.models import Agent
from django.conf import settings
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required

from .cart import Cart
from .forms import CheckoutForm
from agent.models import Agent

from order.utilities import checkout, notify_customer, notify_seller

@login_required
def cart_detail(request):
    cart = Cart(request)

    if request.method == 'POST':
        form = CheckoutForm(request.POST)

        if form.is_valid():
            first_name = request.user.first_name
            last_name = request.user.last_name
            email = request.user.email
            phone = request.user.phone
            address = form.cleaned_data['address']
            zipcode = form.cleaned_data['zipcode']
            place = form.cleaned_data['place']
            longitude = form.cleaned_data['longitude']
            latitude = form.cleaned_data['latitude']
            user = request.user

            order = checkout(request, first_name, last_name, email, address, zipcode, place, longitude, latitude, phone, cart.get_total_cost(), user)

            cart.clear()

            notify_customer(order)
            notify_seller(order)

            return redirect('success')
    else:
        form = CheckoutForm()

    remove_from_cart = request.GET.get('remove_from_cart', '')
    change_quantity = request.GET.get('change_quantity', '')
    quantity = request.GET.get('quantity', 0)

    if remove_from_cart:
        cart.remove(remove_from_cart)

        return redirect('cart')
    
    if change_quantity:
        cart.add(change_quantity, quantity, True)

        return redirect('cart')

    return render(request, 'cart/cart.html', {'form': form})

@login_required
def success(request):
    return render(request, 'cart/success.html')