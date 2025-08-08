# Standard Library
import os
import re
import math
import random
import secrets
import string
import base64
import logging
from datetime import datetime, timedelta
from decimal import Decimal
from functools import wraps

# Django Core
from django.contrib import messages
from django.contrib.auth import (
    login, logout, authenticate, update_session_auth_hash, get_user_model
)
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import *
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.db.models import F, Sum, Q, Count, Avg
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.template import loader
from django.utils.encoding import force_bytes, force_str, smart_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
from django.utils.timezone import now
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_http_methods, require_GET

# Third-Party Packages
from rest_framework import status
from rest_framework.decorators import (
    api_view, permission_classes, parser_classes
)
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import *
from rest_framework.views import APIView
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from google.oauth2 import id_token
from google.cloud import tasks_v2
from google.auth.transport import requests as google_requests

# Project Specific
from vyzio_backend import settings
from .models import *
from .serializers import *
from .tasks import *
from .serializers import *


User = get_user_model()



@api_view(["GET"])
def homepage_data(request):
    # Featured ads
    featured_ads = Ad.objects.filter(is_active=True).order_by('-created_at')[:5]
    featured_ads_data = AdSerializer(featured_ads, many=True).data

    # Categories
    categories = Category.objects.all()
    categories_data = CategorySerializer(categories, many=True).data

    # Stats
    stats = {
        "total_ads": Ad.objects.count(),
        "total_users": User.objects.count(),
        "active_ads": Ad.objects.filter(is_active=True).count()
    }

    return Response({
        "message": "Welcome to Vyzio Ads!",
        "featured_ads": featured_ads_data,
        "categories": categories_data,
        "stats": stats,
    })


@api_view(['GET'])
def ads_list(request):
    """
    Retrieve all active ads for Vyzion Ads.
    """
    ads = Ad.objects.filter(is_active=True).order_by('-created_at')
    serializer = AdSerializer(ads, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def ad_detail(request, id):
    try:
        ad = Ad.objects.get(pk=id, is_active=True)
    except Ad.DoesNotExist:
        return Response({"detail": "Ad not found."}, status=status.HTTP_404_NOT_FOUND)

    serializer = AdSerializer(ad)
    return Response(serializer.data)
