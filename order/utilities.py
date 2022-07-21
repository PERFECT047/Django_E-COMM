import datetime, vincenty
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

from cart.cart import Cart

from .models import Order, OrderItem
from agent.models import Agent

mydict = {'1':'January', '2':'February', '3':'March', '4':'April', '5':'May', '6':'June', '7':'July', '8':'August', '9':'September', '10':'October', '11':'November', '12':'December'}

def checkout(request, first_name, last_name, email, address, zipcode, place, longitude, latitude, phone, amount, user):
    order = Order.objects.create(first_name=first_name, last_name=last_name, email=email, address=address, user=user, zipcode=zipcode, place=place, longitude=longitude, latitude=latitude, phone=phone, paid_amount=amount, date=str(datetime.datetime.now().day) + mydict[str(datetime.datetime.now().month)] + str(datetime.datetime.now().year))

    agents = Agent.objects.all()

    


    for item in Cart(request):
        for agent in agents:
            agent_longitude = float(agent.longitude)
            agent_latitude = float(agent.latitude)
            agent_list = []
            order_list = []
            agent_list.append(agent_longitude)
            agent_list.append(agent_latitude)
            order_list.append(float(longitude))
            order_list.append(float(latitude))
            agent_list = tuple(agent_list)
            order_list = tuple(order_list)
            ans_distance = vincenty.vincenty(agent_list, order_list)
            distance = ans_distance + ans_distance*0.26
            if distance < 20:
                assigned_agent = agent
                order.agents.add(assigned_agent)

        
        OrderItem.objects.create(order=order, product=item['product'], seller=item['product'].seller, agent=assigned_agent, price=item['product'].price, quantity=item['quantity'])
    
        order.sellers.add(item['product'].seller)


    return order

def notify_seller(order):
    from_email = "jayashsatolia@gmail.com"

    for seller in order.sellers.all():
        to_email = seller.created_by.email
        subject = 'New order'
        text_content = 'You have a new order!'
        html_content = render_to_string('order/email_notify_seller.html', {'order': order, 'seller': seller})
        print(html_content)

        msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
        msg.attach_alternative(html_content, 'text/html')
        msg.send()

def notify_customer(order):
    from_email = "jayashsatolia@gmail.com"

    to_email = order.email
    subject = 'Order confirmation'
    text_content = 'Thank you for the order!'
    html_content = render_to_string('order/email_notify_customer.html', {'order': order})
    print(html_content)

    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()