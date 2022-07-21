from users.models import CustomUser
from django.db import models

class Agent(models.Model):
    name = models.CharField(max_length=255, null=True)
    firstname = models.CharField(max_length=255, null=True)
    lastname = models.CharField(max_length=255, null=True)
    email = models.EmailField(null=True)
    phone = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    longitude = models.CharField(max_length=255, null=True)
    latitude = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.OneToOneField(CustomUser, related_name='agent', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
    
    def __str__(self):
        return self.name