from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,PermissionsMixin)
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken



# Create your models here.
class UserManager(BaseUserManager):
    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError(_("Provide a valid email address"))

    def create_user(self, username, email, password=None, **extra_fields):
        if username is None:
            raise TypeError('Users should have a username')
        if email is None:
            raise TypeError('Users should have an email')

    
        
        
        user = self.model(
            username=username,
            email= self.normalize_email(email),
            **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        if password is None:
            raise TypeError('Password should not be none')
        
        user = self.create_user(username,email,password)
        user.is_superuser=True
        user.is_staff=True
        user.save()
        return user

class User(AbstractBaseUser, PermissionsMixin):
    class StoreOwnerManager(BaseUserManager):
        def get_queryset(self, *args, **kwargs):
            results = super().get_queryset(*args, **kwargs)
            return results.filter(role="STORE_OWNER")

    class ClientManager(BaseUserManager):
        def get_queryset(self, *args, **kwargs):
            results = super().get_queryset(*args, **kwargs)
            return results.filter(role="CLIENT")

    class Role(models.TextChoices):
        STORE_OWNER = "store_owner", _("Owner")
        CLIENT = "client", _("Client")

    username = models.CharField(max_length=200, unique=True,db_index=True)
    first_name = models.CharField(max_length=50)
    is_verified = models.BooleanField(default=False)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username", "role"]

    objects = UserManager()

    @property
    def get_full_name(self):
        return f"{self.first_name.title()} {self.last_name.title()}"

    def get_short_name(self):
        return self.username

    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh= RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

    class Meta:
        ordering = ['-updated_at']

class StoreOwner(User):

    base_role = User.Role.STORE_OWNER
    objects = User.StoreOwnerManager()

    class Meta:
        proxy = True
    
class Client(User):

    base_role = User.Role.CLIENT
    objects = User.ClientManager()
    
    class Meta:
        proxy = True

    

    
