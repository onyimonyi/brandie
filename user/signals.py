import decimal
from builtins import map, str, float
import os
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse

User = get_user_model()
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from .models import (Profile, User)
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance,
                               country=instance.country,
                               state= instance.state,
                               )


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    instance.profile.save()
