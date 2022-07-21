from .models import CustomUser
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import redirect, render


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import account_activation_token
from django.contrib.auth.models import User


from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterationForm
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template




from django.shortcuts import render

token_value = ""

def become_user(request):
    global token_value
    if request.method == 'POST':
        form = UserRegisterationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_verified = False
            email = form.cleaned_data.get('email')

            #Email 
            current_site = get_current_site(request)
            htmly = get_template('users/acc_active_email.html')

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

            return render(request, 'users/verify.html')

    else:
        form = UserRegisterationForm()
    return render(request, 'users/become_user.html', {'form': form, 'title':'register here'})


def activateitnow(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)

    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and token == token_value:
        user.is_verified = True
        user.is_user = True
        user.save()
        login(request, user)
        return redirect('profile_view')
    else:
        return HttpResponse('Activation link is invalid!')

def user_login_views(request):
    form = AuthenticationForm()
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None and user.is_user == True:
            if user.is_verified:
                login(request, user)

                if request.GET.get('next'):
                    return redirect(request.GET.get('next'))
                else:
                    return redirect('user_login_views')
            else:
                return render(request, 'users/verify.html')
        else:
            return redirect('user_login_failed')
    
    return render(request, 'users/login.html', {'form':form})


@login_required
def profile_view(request):
    if request.user.is_user:
        orders = request.user.orders.all()
        return render(request, 'users/profile.html', {'orders':orders})
    else:
        return render(request, 'users/login_failed.html')

@login_required
def askForRefund(request, order_id):
    if request.user.is_user:
        orders = request.user.orders.all()
        for i in orders:
            if str(i.id) == str(order_id):
                order = i
                break
        
        order.is_replaced = True
        order.is_refunded = True
        order.save()

        return render(request, 'users/refund.html')

