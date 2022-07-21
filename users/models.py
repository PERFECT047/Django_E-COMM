from io import SEEK_END
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.base import ModelState

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUser(AbstractUser):
    phone = models.CharField(max_length=255)
    is_user = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    longitude = models.CharField(max_length=255, null=True, blank=True)
    latitude = models.CharField(max_length=255, null=True, blank=True)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)