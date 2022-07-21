from io import open_code
from django.db.models.fields.related import OneToOneField
from agent.models import Agent
from users.models import CustomUser
from django.db import models

class Seller(models.Model):
    name = models.CharField(max_length=255, null=True)
    firstname = models.CharField(max_length=255, null=True)
    lastname = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)
    latitude = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(CustomUser, related_name='seller', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_balance(self):
        items = self.items.filter(seller_paid=False, order__sellers__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)
    
    def get_paid_amount(self):
        items = self.items.filter(seller_paid=True, order__sellers__in=[self.id])
        return sum((item.product.price * item.quantity) for item in items)