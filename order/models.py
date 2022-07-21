from django.db import models

from product.models import Product
from seller.models import Seller
from users.models import CustomUser
from agent.models import Agent

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    address = models.CharField(max_length = 100)
    zipcode = models.CharField(max_length=50)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=50)
    longitude = models.CharField(max_length=20, null=True)
    latitude = models.CharField(max_length=20, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=0)
    sellers = models.ManyToManyField(Seller, related_name='orders')
    agents = models.ManyToManyField(Agent, related_name='orders')
    user = models.ForeignKey(CustomUser, related_name='orders', on_delete=models.CASCADE, null=True)
    date = models.CharField(max_length=255, null=True)
    is_delivered = models.BooleanField(default=False)
    is_user_verified = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.first_name


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, related_name='items', on_delete=models.CASCADE)
    agent = models.ForeignKey(Agent, related_name='items', on_delete=models.CASCADE, null=True)
    seller_paid = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=8, decimal_places=0)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return '%s' % self.id

    def get_total_price(self):
        return self.price * self.quantity