from django.utils import timezone
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxLengthValidator
from django.contrib.auth import get_user_model  # Updated import
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator,MinLengthValidator
from decimal import Decimal
import os
from django.db.models import Avg
import base64
import uuid
import random
import string



from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class User(AbstractUser):
    is_advertiser = models.BooleanField(default=False)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country = models.CharField(max_length=50, null=True, default='USA', db_index=True)
    date_of_birth = models.DateField(blank=True, null=True, help_text="Format: YYYY-MM-DD", db_index=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        default='https://bit.ly/3YwXaHM',
        blank=True,
        null=True
    )
    avatar_url = models.URLField(blank=True, null=True)

    # Override these to avoid reverse accessor clash
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups',
        related_query_name='custom_user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
        related_query_name='custom_user',
    )

    def __str__(self):
        return self.username



""" Represents ad categories (services, products, jobs, etc.)
Allows easy categorization of ads """
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, blank=True)  

    def __str__(self):
        return self.name
    
""" 
Represents a single ad posted by a user

Linked to a category and a user

Contains details like title, description, price, city, status

 """
class Ad(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    city = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='USD') 
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title



""" Allows multiple images per ad """
class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ads/extra/')

    def __str__(self):
        return f"Image for {self.ad.title}"



""" Tracks payments made by users to publish or promote ads

Supports different payment methods and statuses """

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('card', 'Card'),
        ('mobile_money', 'Mobile Money'),
        ('crypto', 'Cryptocurrency'),
    ]

    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('failed', 'Failed'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    crypto_currency = models.CharField(max_length=20, blank=True, null=True)
    currency = models.CharField(max_length=3, default='USD')  
    crypto_address = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} - {self.status}"
