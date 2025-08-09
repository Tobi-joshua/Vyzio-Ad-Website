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
from vyzio_backend.settings import IMAGEKIT_API
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions

# Upload function, which you're already using
def upload_file_to_imagekit(file_obj, tags):
    filename = file_obj.name
    encoded_file = base64.b64encode(file_obj.read()).decode('utf-8')
    result = IMAGEKIT_API.upload(
        file=encoded_file,
        file_name=filename,
        options=UploadFileRequestOptions(tags=tags)
    )
    return {
        "file_url": result.url,
        "file_id": getattr(result, "file_id", None),
        "file_name": filename
    }



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
    
    def save(self, *args, **kwargs):
        """
        Only upload to ImageKit when:
          - new user (no PK), or
          - no avatar_url yet, or
          - a real file replaced the default
        """
        is_new = self.pk is None
        should_upload = False

        # Only consider upload if avatar isn't the default placeholder
        if self.avatar and self.avatar.name != 'https://bit.ly/3YwXaHM':
            if is_new or not self.avatar_url:
                should_upload = True
            else:
                try:
                    orig = User.objects.get(pk=self.pk)
                    if orig.avatar.name != self.avatar.name:
                        should_upload = True
                except User.DoesNotExist:
                    should_upload = True

        if should_upload:
            try:
                new_url = upload_file_to_imagekit(self.avatar, tags=["user_avatar"])
                if new_url:
                    self.avatar_url = new_url
            except Exception as e:
                print(f"Error uploading avatar to ImageKit: {e}")

        super().save(*args, **kwargs)







""" Represents ad categories (services, products, jobs, etc.)
Allows easy categorization of ads """
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    icon = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)

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
    header_image = models.ImageField(upload_to='ads/header/', null=True, blank=True)
    header_image_url = models.URLField(blank=True, null=True)
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        """
        Upload header_image to ImageKit only when:
          - instance is new, or
          - there is no existing header_image_url, or
          - the header_image file has changed since last save.
        """
        is_new = self.pk is None
        should_upload = False

        if self.header_image:
            # 1) New record or no URL yet ⇒ upload
            if is_new or not self.header_image_url:
                should_upload = True
            else:
                # 2) Existing record: compare stored file name vs. current
                try:
                    orig = Ad.objects.get(pk=self.pk)
                    if orig.header_image.name != self.header_image.name:
                        should_upload = True
                except Ad.DoesNotExist:
                    # fallback: upload if something unexpected happened
                    should_upload = True

        if should_upload:
            try:
                result = upload_file_to_imagekit(self.header_image, tags=['ad_header_image'])
                file_url = result.get('file_url')
                if file_url:
                    self.header_image_url = file_url
            except Exception as e:
                # log and continue without blocking save
                print(f"Error uploading header image to ImageKit: {e}")

        super().save(*args, **kwargs)
    



""" Allows multiple images per ad """
class AdImage(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='ads/extra/')
    image_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return f"Image for {self.ad.title}"
    
    def save(self, *args, **kwargs):
        """
        Upload image to ImageKit only when:
          - instance is new, or
          - there is no existing image_url, or
          - the image file has changed since last save.
        """
        is_new = self.pk is None
        should_upload = False

        if self.image:
            if is_new or not self.image_url:
                should_upload = True
            else:
                try:
                    orig = AdImage.objects.get(pk=self.pk)
                    if orig.image.name != self.image.name:
                        should_upload = True
                except AdImage.DoesNotExist:
                    should_upload = True

        if should_upload:
            try:
                result = upload_file_to_imagekit(self.image, tags=['ad_images'])
                file_url = result.get('file_url')
                if file_url:
                    self.image_url = file_url
            except Exception as e:
                print(f"Error uploading image to ImageKit: {e}")

        super().save(*args, **kwargs)



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
