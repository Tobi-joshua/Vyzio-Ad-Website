from django.urls import path, include
from django.contrib.auth.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from ads import views

urlpatterns = [
#path('', views.home_page, name='homepage'),

]