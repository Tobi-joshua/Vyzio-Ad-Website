from django.urls import path, include
from django.contrib.auth.views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from ads import views

urlpatterns = [
     path('homepage/', views.homepage_data, name='homepage-data'),
     path('ads/', views.ads_list, name='ads-list'),
     path('ads/<int:id>/', views.ad_detail, name='ad-detail'),
     path('categories/', views.category_list, name='category-list'),        
     path('categories/create/', views.category_create, name='category-create'), 
     path('categories/<int:pk>/ads/', views.category_ads_list, name='category-ads-list'),
]