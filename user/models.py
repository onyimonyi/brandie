from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager, PermissionsMixin)
from datetime import datetime
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    def create_user(self, email,username, password=None, is_active=True,
                    is_staff=False, is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")

        user_obj = self.model(
            email=self.normalize_email(email),
            username = username,
        )
        user_obj.set_password(password)
        user_obj.staff = is_staff
        user_obj.active = is_active
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staff_user(self, username,email, password=None):
        user = self.create_user(
            email,
            username,
            password=password,
            is_staff=True,
        )
        return user

    def create_dispatch_user(self, username, email, password=None):
        user = self.create_user(
            email,
            username,
            password=password,
        )
        return user

    def create_superuser(self,username, email, password=None):
        user = self.create_user(
            email,
            username,
            password=password,
            is_staff=True,
            is_admin=True
        )
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

    class DispatchManager(BaseUserManager):
        def get_queryset(self, *args, **kwargs):
            results = super().get_queryset(*args, **kwargs)
            return results.filter(role="DISPATCH")

    class Role(models.TextChoices):
        STORE_OWNER = "store_owner", _("Owner")
        CLIENT = "client", _("Client")
        DISPATCH = "dispatch", _("Dispatch")

    username = models.CharField(max_length=200, unique=True, db_index=True)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=Role.choices)
    active = models.BooleanField(default=True)
    country = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = UserManager()


    def __str__(self):
        return self.email

    def get_username(self):
        return self.username

    def get_role(self):
        return self.role

    def get_email(self):
        return self.email


    def get_short_name(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_role(self):
        return self.role

    @property
    def is_role(self):
        return self.role

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_active(self):
        return self.active

    @property
    def is_admin(self):
        return self.admin

    def tokens(self):
        refresh = RefreshToken.for_user(self)
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


class Dispatch(User):
    base_role = User.Role.DISPATCH
    objects = User.DispatchManager()

    class Meta:
        proxy = True


class Client(User):
    base_role = User.Role.CLIENT
    objects = User.ClientManager()

    class Meta:
        proxy = True

class Follower_Relation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    country = models.CharField(max_length=225, null=True, blank=True)
    state = models.CharField(max_length=225, null=True, blank=True)
    phone = models.CharField(max_length=225, null=True, blank=True)
    address = models.CharField(max_length=225, null=True, blank=True)
    bio = models.CharField(max_length=225, null=True, blank=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    follower = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='following', blank=True)

    def __str__(self):
        return str(self.user.email)
