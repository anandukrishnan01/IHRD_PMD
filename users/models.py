from __future__ import annotations

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone

from user_management import settings


class APIUserManager(BaseUserManager):
    """Custom user manager."""

    use_in_migrations = True

    def create_user(self, email, password=None, phone_number='', **extra_fields):
        """Create a user."""
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            phone_number=phone_number,
            **extra_fields
        )

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """Create a superuser."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_verified', True)

        return self.create_user(email, password, **extra_fields)

class APIUser(AbstractBaseUser, PermissionsMixin):
    """Custom user class."""

    USERNAME_FIELD = 'email'

    USER_TYPE_ADMIN = 'admin'

    # username field not used, only here to make django-rest-auth work
    email = models.EmailField(blank=False, unique=True)
    first_name = models.CharField(
        'first name', max_length=50, null=True, blank=True,
    )
    last_name = models.CharField(
        'last name', max_length=50, null=True, blank=True,
    )
    phone_number = models.CharField(max_length=20, verbose_name='phone number')

    is_staff = models.BooleanField(
        'staff status',
        default=False,
        help_text='Designates whether the user can log into this admin site.',
    )
    is_active = models.BooleanField(
        'active',
        default=True,
        help_text='Designates whether this user should be treated as active. '
        'Deselect this instead of deleting accounts.',
    )
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    objects = APIUserManager()

    class Meta:
        """Model meta data."""

        verbose_name = 'user'
        verbose_name_plural = 'users'

    def get_full_name(self):
        """Get full name."""
        full_name = f'{self.first_name} {self.last_name}'
        return full_name.strip()

    def get_short_name(self):
        """Get short name."""
        return self.first_name


class Token(models.Model):
    user_id = models.ForeignKey(
        APIUser, blank=True, null=True, on_delete=models.CASCADE,
    )
    refresh_token = models.TextField(blank=True, null=True)
    access_token = models.TextField(blank=True, null=True)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class UserNotification(models.Model):
    user_id = models.ForeignKey(
        APIUser, blank=True, null=True, on_delete=models.CASCADE,
    )
    notification_text = models.TextField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LoginLog(models.Model):
    user_id = models.ForeignKey(
        APIUser, blank=True, null=True, on_delete=models.CASCADE,
    )
    login_count = models.IntegerField(null=True, blank=True, default=0)
    last_logged_in = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_expired = models.BooleanField(default=False)


class WorldPopulation(models.Model):
    place = models.IntegerField()
    pop1980 = models.IntegerField()
    pop2000 = models.IntegerField()
    pop2010 = models.IntegerField()
    pop2022 = models.IntegerField()
    pop2023 = models.IntegerField()
    pop2030 = models.IntegerField()
    pop2050 = models.IntegerField()
    country = models.CharField(max_length=255)
    area = models.IntegerField()
    landAreaKm = models.IntegerField()
    cca2 = models.CharField(max_length=2)
    cca3 = models.CharField(max_length=3)
    netChange = models.IntegerField(null=True, blank=True)
    growthRate = models.FloatField()
    worldPercentage = models.FloatField(null=True, blank=True)
    density = models.FloatField()
    densityMi = models.FloatField()
    rank = models.IntegerField()