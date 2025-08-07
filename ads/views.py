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